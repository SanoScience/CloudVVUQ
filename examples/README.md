## Directory containing examples of CloudVVUQ usage

In example directory you can find many simulation tutorials. Tutorial usually consists of:
- tutorial_script.py
- Cloud Functions (CF) source code you should use to deploy simulation on this service
- Cloud Run (CR) source code with a Dockerfile used to build image for this service


### How to create Docker image with app and upload it to Cloud Run:

To build image:
- run `docker build .` from directory with Dockerfile

To upload built image to Container Registry:
[Guide](https://cloud.google.com/container-registry/docs/pushing-and-pulling).
- have a GCP CLI connected to project [Guide](https://cloud.google.com/sdk/docs/install-sdk)
- register gcloud as a Docker credential helper - [Guide](https://cloud.google.com/sdk/gcloud/reference/auth/configure-docker) 
- tag image `docker tag SOURCE_IMAGE HOSTNAME/PROJECT-ID/IMAGE`
- push image `docker push HOSTNAME/PROJECT-ID/IMAGE`

To create container with app for local usage:
- copy simulation file from examples directory (e.g. ishigami.py) to app dir
- build image `docker build .` from directory with Dockerfile
- create container `docker run -p 8080:8080 image_id` (replace 8080 with your port mapping)