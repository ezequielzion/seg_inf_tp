## Para correr con Docker:
1. Instalar [docker](https://www.docker.com/get-started/)
2. Posicionarse en la carpeta `seg_inf_tp` y crear un archivo `.env` siguiendo el ejemplo de `.env.example`
3. En el archivo `.env`, crear la variable `PORT` y setear el puerto deseado. Recomendamos el puerto 5000.
4. Crear una cuenta en [ngrok](https://ngrok.com/) y conseguir un [auth token](https://dashboard.ngrok.com/tunnels/authtokens). Una vez obtenido, setear `NGROK_AUTH_TOKEN` en el archivo `.env` con el mismo
5. Correr el script 
    ```
    run.sh
    ```
6. En un navegador, se debería poder entrar con `http://localhost:{{PORT}}`


## Para correr sin Docker:
1. Instalar Python
2. Posicionarse en la carpeta `seg_inf_tp` e instalar las dependencias con el `requirements.txt`
3. Posicionarse en la carpeta `seg_inf_tp/src` y correr `python3 backend.py`
4. Crear una cuenta, instalar [ngrok](https://ngrok.com/) y configurarlo para poder usarlo siguiendo el [instructivo de su documentación](https://dashboard.ngrok.com/get-started/setup/linux)
5. En otra terminal, correr 
    ```
    ngrok http 5000
    ```