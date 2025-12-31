# Docker Setup Guide

This guide explains how to use Docker to run the Physical AI & Humanoid Robotics course materials.

## Prerequisites

- Docker Desktop or Docker Engine installed
- Docker Compose (included with Docker Desktop)
- For GPU support: NVIDIA GPU + nvidia-docker

## Quick Start

### 1. Build all images

```bash
cd my-book
docker-compose build
```

### 2. Run the Documentation Website

```bash
docker-compose up docs
```

Visit: http://localhost:3000

### 3. Run individual modules

**Module 1 - ROS 2 Fundamentals**:
```bash
docker-compose run module-1
```

**Module 2 - Gazebo Physics**:
```bash
docker-compose run module-2
```

**Module 3 - Isaac & Navigation (GPU required)**:
```bash
docker-compose run --gpus all module-3
```

**Module 4 - Vision-Language-Action (GPU required)**:
```bash
docker-compose run --gpus all module-4
```

## Building Individual Modules

### Build only Module 1
```bash
docker build -f docker/Dockerfile.module-1 -t physical-ai-book:module-1 .
docker run -it physical-ai-book:module-1
```

### Build only Documentation
```bash
docker build -f docker/Dockerfile.docs -t physical-ai-book:docs .
docker run -p 3000:3000 physical-ai-book:docs
```

## Environment Variables

### Module Configuration

Set custom environment variables when running containers:

```bash
docker run -e ROS_DISTRO=humble -it physical-ai-book:module-1
```

## GPU Support

### For NVIDIA GPUs

1. Install nvidia-docker:
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

2. Run with GPU:
```bash
docker-compose run --gpus all module-3
# or
docker run --gpus all -it physical-ai-book:module-3
```

## Volume Mounting

Mount your own workspace:

```bash
docker run -v /path/to/your/ros2_ws:/root/ros2_ws -it physical-ai-book:module-1
```

## Networking

### Access ROS 2 across containers

Enable host network mode:

```bash
docker run --network host -it physical-ai-book:module-1
```

## Common Issues

### Issue: "Cannot find docker daemon"
**Solution**: Ensure Docker Desktop is running or Docker Engine is active.

### Issue: "Permission denied" running docker
**Solution**: Add your user to the docker group:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Issue: GPU not detected
**Solution**: Verify NVIDIA GPU support:
```bash
docker run --rm --gpus all nvidia/cuda:12.2.2-runtime-ubuntu22.04 nvidia-smi
```

### Issue: "Out of memory" in container
**Solution**: Increase Docker memory limit in Docker Desktop settings.

## Cleanup

Remove containers:
```bash
docker-compose down
```

Remove images:
```bash
docker rmi physical-ai-book:module-1
docker rmi physical-ai-book:module-2
docker rmi physical-ai-book:module-3
docker rmi physical-ai-book:module-4
```

Remove all unused Docker resources:
```bash
docker system prune -a
```

## Advanced Usage

### Build with custom Dockerfile
```bash
docker build -f custom-dockerfile -t my-image:tag .
```

### Run with bash instead of default command
```bash
docker run -it --entrypoint /bin/bash physical-ai-book:module-1
```

### View docker logs
```bash
docker logs <container-id>
```

### Execute command in running container
```bash
docker exec -it <container-id> /bin/bash
```

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker)
