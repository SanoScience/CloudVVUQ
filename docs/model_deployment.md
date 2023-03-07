## Model deployment

### AWS Lambda

1. Go to Lambda service.
2. Choose AWS region the closest to you.
3. Click "Create function".
4. Choose a deployment option and name the function.
    1. if you choose **author-from-scratch** then specify your runtime language and use defaults.
    2. if you choose **container image** then select you container image from Elastic Container Registry (see "Docker image deployment" how to upload docker image).
5. Click "Create function" and wait for it to be created.
6. If you decided to **author-from-scratch** then see next sections to see how you can deploy your code.
7. Proceed to function configuration.
   1. In general configuration set timeout longer than your model execution maximum time.
   2. Allocate enough memory for your function.
   3. Go to Function URL and enable it.
8. Model is deployed.

#### Copy-paste deployment

Probably easiest and most intuitive deployment mode. Just create a hello-world function using web console then replace the code using built-in code editor. Not the best option for large code bases and many dependencies.

Create the following structure in the code-editor:
```
model_name
│   model.py
│   wrapper.py    
```

You can make use of folders and add additional files as long as you can correctly call the main model's method from the wrapper. 

#### Zip file deployment
[Documentation](https://docs.aws.amazon.com/lambda/latest/dg/configuration-function-zip.html)

Create the following structure and zip **files** inside:
```
lambda
│   model.py
│   wrapper.py    
```
Then you can upload the zip file into the lambda functions using web console.
If your archive is bigger than 50 MB you must first upload the archive to S3 and then when deploying lambda you specify S3 url to archive.

There are alternative deployment modes. Check it out especially if you need dependencies not provided by layers. [Guide](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html)  

#### Docker image deployment

*Is this section we expect that you have ready-to-deploy container image. If not check the "Docker image creation and deployment
" section first.*

First you have to upload built image to AWS Elastic Container Registry: [Guide](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html)  
1. Authenticate the Docker CLI to your Amazon ECR registry  
2. Tag your image `docker tag SOURCE_IMAGE REPOSITORY_NAME/IMAGE_NAME`  
3. Push image docker `push REPOSITORY_NAME/IMAGE_NAME`  

### Google Cloud Functions

1. Go to Cloud Functions service.
2. Fill the configuration:
   1. Name the function
   2. Choose GCP region the closest to you.
   3. Verify that HTTPS trigger with authentication is selected as a trigger.
   4. Expand "Runtime, build, connections and security setting section"
      1. Allocate enough memory for your function.
      2. Set the timeout longer than your model execution maximum time
      3. Set upper limit for maximum number of instances (1000 is fine).
      4. Choose the runtime service account. Have one created that allows only GC Function invocations (remember about the principle of the least privilege). [Documentation](https://cloud.google.com/iam/docs/understanding-service-accounts)
   5. Click next
   6. Choose runtime language, entry point, insert your code by either pasting or uploading a zip archive. 
   7. Click deploy and wait for it to be ready.
3. Model is deployed.

#### Copy-paste deployment

Probably easiest and most intuitive deployment mode. Just modify a hello-world function using web console then replace the code using built-in code editor. Not the best option for large code bases and many dependencies.

Create the following structure in the code-editor:
```
model_name
│   model.py
|   requirements.txt
│   wrapper.py  (aka main.py)    
```
Insert your dependencies in requirements.txt file. They will be installed during the deployment.
You can make use of folders and add additional files as long as you can correctly call the main model's method from the wrapper. 


#### Zip archive deployment

Create the following structure and zip **files** inside:
```
function
│   model.py
|   requirements.txt
│   wrapper.py  (aka main.py)     
```

Then you can upload the zip file into the GC Function using web console.

### Google Cloud Run


### Docker image creation and deployment
[Documentation](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-images.html)

1. Have docker installed locally - [Download and installation guide](https://docs.docker.com/get-docker/)
2. Create a Dockerfile in your project (make use of boilerplate code provided below). Example project structure:
```
project
|   Dockerfile
│   requirements.txt
│   wrapper.py
|   model.py    
```
3. Build your image, use cli in project's directory
```
docker build .
```
4. (Optional but recommended) Test image locally
```
docker run -p 8080:8080 <image_id>
```
Replace image_id. You can list all image ids using
```
docker images
```
If your image is running as a container you can paste 
```python
url = "http://127.0.0.1:8080"
```
into you local (client) code where you have CloudVVUQ installed and try to compute a single sample.
```python
outputs = executor.run(samples[1], max_load=1)
```

- Possible misconfigurations and remedies:  
    - request does not reach the container
        - check if port 8080 is opened  
    - container crashed due to misconfigured paths  
        - check if you correctly imported your model in the wrapper code  
        - check if all dependencies are installed

### Docker image templates 

#### AWS Lambda using AWS base-image

```dockerfile
FROM public.ecr.aws/lambda/python:3.9

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY model.py ${LAMBDA_TASK_ROOT}

CMD [ "app.handler" ]
```

#### Google Cloud Run

```dockerfile
FROM python:3.10-slim

ADD app/requirements.txt .
RUN pip3 install -r requirements.txt

COPY /app /app
WORKDIR /app
EXPOSE 8080:8080

CMD ["python3", "main.py"]
```
