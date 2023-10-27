This repository contains files and instructions to build a Docker image using Buildah, run it with Podman, and upload the built image to DockerHub registry.

## Prerequisites

- **Buildah** should be installed.
- **Podman** should be installed.
- **DockerHub** account for image upload.

## Building the Docker Image

To build the Docker image using Buildah, follow these steps:

1. Clone this repository.
2. Navigate to the directory containing the Dockerfile.
3. Run the following command:


    buildah bud -t your-image-name .

    Replace `your-image-name` with the desired name for your Docker image.

## Starting a Container

To run a container using Podman from the built image, use the following command:


podman run -d -p 8080:80 your-image-name


Uploading the Image to DockerHub Registry
To upload the built image to DockerHub, use the following steps:

Log in to your DockerHub account using the command:


buildah login docker.io
Follow the prompts to log in with your DockerHub credentials.

Push the image to DockerHub:

buildah push your-image-name docker://your-dockerhub-username/your-repo-name:tag
