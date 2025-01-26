# Task 2

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    ```
2. Navigate to the project directory:
    ```sh
    cd /home/diaa/hyveTasks/task2
    ```
3. Build the Docker image:
    ```sh
    docker build -t task2 .
    ```

## Running the Application

To run the application, use the following command:
```sh
docker run -d -p 8000:8000 task2
```

This will start the application in a Docker container and map port 8000 of the container to port 8000 on your host machine.

## Postman Collection

A Postman collection example is provided to help you test the API endpoints. You can find the collection file in the `postman` directory of the project.
