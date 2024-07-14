## Para correr con Docker:
1. Instalar [docker](https://www.docker.com/get-started/)
2. Posicionarse en la carpeta `seg_inf_tp`
3. Crear una cuenta en [ngrok](https://ngrok.com/) y conseguir un [auth token](https://dashboard.ngrok.com/tunnels/authtokens). Una vez obtenido, crear un archivo `.env` siguiendo el ejemplo de `.env.example` y setear `NGROK_AUTH_TOKEN` con el auth token
4. Crear la imagen de docker corriendo
    ```
    docker build -t flask_docker .
    ```
5. Correr la imagen con el comando
    ```
    docker run -p 5000:5000 flask_docker
    ```
6. En un navegador, se debería poder entrar con http://localhost:5000/


## Para correr sin Docker:
1. Instalar Python
2. Posicionarse en la carpeta `seg_inf_tp` e instalar las dependencias con el `requirements.txt`
3. Posicionarse en la carpeta `seg_inf_tp/src` y correr `python3 backend.py`
4. Crear una cuenta, instalar [ngrok](https://ngrok.com/) y configurarlo para poder usarlo siguiendo el [instructivo de su documentación](https://dashboard.ngrok.com/get-started/setup/linux)
5. En otra terminal, correr 
    ```
    ngrok http 5000
    ```