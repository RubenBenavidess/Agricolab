# Agricolab LLM API

### 0. Requirements

As first, make sure to have installed and configured nvidia toolkit. You can check it on: [text](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

### 1. Build image
make build
### Or Windows
docker build -f backend-llm/Dockerfile.fastapi -t fastapi-image .

### 2. Run container
make run
### Or Windows
docker run --gpus all --name agricolab_api -p 8000:8000 fastapi-image

### 3. Use it on
http://localhost:8080/docs

### 4. Test it
