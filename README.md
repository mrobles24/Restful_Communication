# Practica 2 Restful_Communication

## Descripción General

Este programa simula la comunicación asincrónica entre tres agentes utilizando la arquitectura RESTful con el framework Flask. Existen 3 agentes, donde cada uno de ellos genera un número aleatorio y, a través de un proceso de consenso coordinado, intentan llegar a un acuerdo sobre cuál es el número mayoritario (es decir, que al menos dos agentes generen el mismo número). Si se alcanza el consenso, el proceso lo registra como exitoso, si no, los agentes pueden generar nuevos números aleatorios y vuelven a intentarlo hasta que logran un acuerdo. El programa registra cada intento en un archivo de texto llamado attempts.txt.

## Cómo Funciona
1. **Generación de números aleatorios**: 
   - Cada uno de los tres agentes puede generar un número aleatorio entre 1 y 5 a través de sus respectivos endpoints (`/agent/<agent_id>/random`).
   - Los números generados se almacenan en el servidor.

2. **Coordinación y verificación de consenso**:
   - El coordinador (a través del endpoint `/coordinator/check_consensus`) verifica si al menos dos agentes han generado el mismo número.
   - Si se alcanza el consenso, se registra el resultado (número de consenso) y se devuelve la respuesta indicando el éxito.
   - Si no hay consenso, se generan nuevos números aleatorios para los tres agentes y se vuelve a intentar. Este proceso se repite hasta que se alcanza un acuerdo.
   
3. **Registro de intentos**:
   - Cada intento de consenso, ya sea exitoso o fallido, se registra en un archivo llamado `attempts.txt`. El archivo incluye detalles como el número del intento, los valores generados por los agentes, y si se alcanzó o no el consenso.

## Cómo Ejecutar
1. Se arranca una terminal y se accede al directorio que contiene el programa.
2. Iniciamos el servidor con: `python3 -m flask run` (como esta guardado como app.py, flask ya detecta a que programa apuntar)
3. Abrimos otra terminal para interactuar con los endpoints. 
4. En la segunda terminal lanzamos el siguiente comando para que los agentes generen numeros aleatorios `curl http://127.0.0.1:5000/agent/agent_N/random`, cambiando N por 1,2 y 3 sucesivamente.
5. Para cada comando, se hace un print con el número generado
6. Una vez lanzados los tres comandos, verificamos en el endpoint de consenso si se ha llegado a un acuerdo o no `curl http://127.0.0.1:5000/coordinator/check_consensus`.
7. Cuando lanzemos el comando, se hace un print con el resultado y se guarda en el archivo `attempts.txt`.
8. Se puede repetir el proceso el número de veces que se quiera ya que en el archivo .txt se iran registrando los consensos, positivos o negativos.

## Notas
- El programa no finaliza hasta que no se finaliza el proceso flask usando ctrl+c o ctrl+z.
- El archivo .txt se crea en el primer check de consenso y es en este archivo donde se van guardando en lineas nuevas los diferentes checks.
- El archivo, una vez realizadas diferentes ejecuciones, se parecerá al siguiente ejemplo:
  
  ![image](https://github.com/user-attachments/assets/cf8f4abd-43b1-4943-a585-f8d60fa78fcd)
