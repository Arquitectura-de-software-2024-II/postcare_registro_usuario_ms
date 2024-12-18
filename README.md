# postcare_registro_usuario_ms
## Installation

To install and run this project using Docker, follow these steps:

1. **Clone the repository:**
    ```sh
    git clone https://github.com/Arquitectura-de-software-2024-II/postcare_registro_usuario_ms.git .
    ```

2. **Build the Docker image:**
    ```sh
    docker build -t postcare_registro_usuario_ms .
    ```

3. **Run the Docker container:**
    ```sh
    docker run -d -p 8000:8000 --name "postcare_registro_usuario_ms" postcare_registro_usuario_ms
    ```

Your application should now be running at `http://localhost:8000`.