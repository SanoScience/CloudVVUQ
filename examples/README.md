# Directory containing examples of CloudVVUQ usage

In example directory you can find many simulation tutorials. Tutorial usually consists of:
- tutorial_script.py
- Cloud Functions (CF) source code you should use to deploy simulation on this service
- Cloud Run (CR) source code with a Dockerfile used to build image for this service


### How to create Docker image with app:

To build image:
- run `docker build .` from directory with Dockerfile

### How to upload built image to Google Container Registry: [Guide](https://cloud.google.com/container-registry/docs/pushing-and-pulling)
- Have a GCP CLI connected to project [Guide](https://cloud.google.com/sdk/docs/install-sdk)
- Register gcloud as a Docker credential helper - [Guide](https://cloud.google.com/sdk/gcloud/reference/auth/configure-docker) 
- Tag image `docker tag SOURCE_IMAGE HOSTNAME/PROJECT-ID/IMAGE`
- Push image `docker push HOSTNAME/PROJECT-ID/IMAGE`

### How to upload built image to AWS Elastic Container Registry: [Guide](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html)
- Authenticate the Docker CLI to your Amazon ECR registry
- Tag your image `docker tag SOURCE_IMAGE REPOSITORY_NAME/IMAGE_NAME`
- Push image `docker push REPOSITORY_NAME/IMAGE_NAME`


### How to create container with app for local usage:
- Copy simulation file from examples directory (e.g. ishigami.py) to app dir
- Build image `docker build .` from directory with Dockerfile or `docker build -f path/to/Dockerfile .` from other directory 
- Create container `docker run -p 8080:8080 image_id` (replace 8080 with your port mapping)

## How to create Dockerfile suitable for AWS Lambda: [Guide](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html)  
### Case 1 - Using AWS-provided base image: [Guide](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html)
- Find suitable image on [ECR Public Gallery](https://gallery.ecr.aws/lambda)
- Copy your application files and install dependencies
- Add `CMD ["app.handler"]`

### Case 2 - Using your own base image: [Guide](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html)
- Install aws-lambda-cpp build dependencies
- Add Runtime interface client (awslambdaric for python)
- Add AWS Lambda Runtime Interface Emulator (optional - for local testing only required)
- Add `CMD ["app.handler"]`

## How to create layers for AWS Lambda [Guide](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)
- Download dependencies from pypi.org along with "manylinux" wheel files. Unpack packages.
- Create directory called python and put everything there.
- Zip python directory. Name as you like.
- Upload directly to lambda if package is <50MB else upload to S3 beforehand.
- Layer is ready to set up on lambda - remember about setting correct compatibilities.

## General tips:
- For optimal performance on AWS Lambda set memory to >1769MB (1vCPU) [More info](https://stackoverflow.com/questions/66522916/aws-lambda-memory-vs-cpu-configuration)
- For optimal performance on GCF set memory to 2GB (1vCPU) - [More info](https://cloud.google.com/functions/docs/configuring/memory)
- AWS default lambda timeout is 3 seconds, remember to increase it for your needs (max 15 min) [More info](https://docs.aws.amazon.com/lambda/latest/dg/configuration-function-common.html)
- GCF maximal timeout is 9min for 1st generation, 60 min (HTTP) or 9 min (event-driven) for 2nd generation [More info](https://cloud.google.com/functions/docs/configuring/timeout)
- When using AWS Lambda with layers you may need to set env variable: `PYTHONPATH=/var/runtime:/opt/python`
- When writing Dockerfile ADD is better that COPY for requirements.txt because COPY doesn't cache packages (download every time)
- Number tcp_connections in aiohttp.TCPConnector is an upper limit for concurrency
- When testing locally GC Functions code you need flask api, for deployment you don't. Only add "request" parameter in the function handler.