## AWS Lambda 

- CPU proportional to memory (1769 MB == 1 vCPU - [study](https://www.sentiatechblog.com/aws-re-invent-2020-day-3-optimizing-lambda-cost-with-multi-threading))
- Broad but limited set of [available runtimes](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html) 

## Lambda specific configuration

- Allow function url in configuration

### Lambda limits - [docs](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html)

- 15 minutes - max timeout value
- 1000 concurrent instances (possible to request quota increase)

### Lambda layers - [docs](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)

- Used to add dependencies (e.g. numpy, pandas) to your functions (deployed as a zip file)

### Lambda container images - [docs](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html)

- Alternative deployment type for Lambda. Easier to package code with its dependencies
- More customizable option than layers. Allows running code in languages not supported by Lambda (e.g. Matlab, Octave)
- Requires additional development work to create a Dockerfile and image push to Elastic Container Registry (ECR)
