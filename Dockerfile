# docker_start by pulling the python image
FROM python:3.12.4-bookworm

# Set the working directory in the container
WORKDIR /app

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# Install the dependencies and packages in the requirements file
RUN pip3 install -r /app/requirements.txt

# Install wget and download ngrok
RUN apt-get update && apt-get install -y wget && \
    wget -q https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz && \
    tar xvzf ngrok-v3-stable-linux-amd64.tgz && \
    mv ngrok /usr/local/bin

# Copy every content from the local file to the image
COPY . /app

# Run the application
COPY docker_start.sh /app/docker_start.sh
COPY .env /app/.env
RUN chmod +x /app/docker_start.sh
CMD ["/app/docker_start.sh"]