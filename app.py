from flask import Flask, jsonify
import random

app = Flask(__name__)

# Dictionary to store each agent's generated random number
agent_data = {
    "agent_1": None,
    "agent_2": None,
    "agent_3": None
}

# Global variable to track how many attempts it takes to reach consensus
attempts = 0

# Function to generate a random number for agents
# Using a small range (1-5) for simplicity
def generate_random_number():
    return random.randint(1, 5)

# Function to log consensus attempts into a file
def log_attempt(status, attempts, agent_values, consensus_number=None):
    # Open the log file in append mode to log each attempt
    with open('attempts.txt', 'a') as log_file:
        if status == "Consensus Reached":
            log_file.write(f"Attempt {attempts}: {status} - Consensus on number {consensus_number} (Values: {agent_values})\n")
        else:
            log_file.write(f"Attempt {attempts}: {status} - (Values: {agent_values})\n")

# Endpoint for agents to generate their random number
@app.route('/agent/<agent_id>/random', methods=['GET'])
def agent_random(agent_id):
    if agent_id in agent_data:
        # Generate a new random number for the specified agent
        agent_data[agent_id] = generate_random_number()
        return jsonify({"agent": agent_id, "random_number": agent_data[agent_id]})
    # Return an error if the agent ID is invalid
    return jsonify({"error": "Invalid agent ID"}), 404

# Endpoint to check for consensus among the agents
@app.route('/coordinator/check_consensus', methods=['GET'])
def check_consensus():
    global attempts  # Use the global 'attempts' variable
    attempts += 1  # Increment the attempt count each time this endpoint is called

    # Ensure all agents have generated a number before checking consensus
    if None in agent_data.values():
        return jsonify({"error": "Some agents have not generated numbers yet"}), 400
    
    # Collect the numbers generated by all agents
    numbers = list(agent_data.values())

    # Count occurrences of each number
    number_counts = {num: numbers.count(num) for num in set(numbers)}
    # Check if there is a majority (at least 2 agents have the same number)
    majority_number = [num for num, count in number_counts.items() if count >= 2]

    # Log and respond based on whether consensus was reached
    if majority_number:
        log_attempt("Consensus Reached", attempts, agent_data, consensus_number=majority_number[0])
        return jsonify({
            "status": "Consensus Reached",
            "consensus_number": majority_number[0],
            "attempts": attempts
        })
    else:
        # If no consensus, generate new random numbers for all agents
        for agent in agent_data:
            agent_data[agent] = generate_random_number()
        log_attempt("No Consensus", attempts, agent_data)
        return jsonify({
            "status": "No Consensus",
            "attempts": attempts,
            "new_values": agent_data
        })

# Main function to start the Flask app
# Runs in debug mode for easier development and troubleshooting
if __name__ == '__main__':
    app.run(debug=True)
