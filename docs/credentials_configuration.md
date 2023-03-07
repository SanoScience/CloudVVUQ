## Credentials
Getting credentials to authorize CloudVVUQ invocation is the first step.
Depending on the cloud provider you use there are many ways to do this.
Currently, CloudVVUQ supports authorization with two cloud providers:

- **AWS**  
- **GCP**

It is possible to extend this list by implementing authorization method for your provider in authorizer.py.

### AWS credentials
Full list of possible credentials configurations and documentation is [here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html)  
The easiest and most CloudVVUQ-compatible method would be using:  
- shared credentials file ( ~/.aws/credentials )  
- environment variables

### GCP credentials
- Create a service account with appropriate permissions (e.g. cloudfunctions.functions.invoke)
- Create a key for this account -> download credentials file
- Set a environmental variable in script with path to credentials file:
  ```py
  os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials/gcp_creds.json'
  ```
