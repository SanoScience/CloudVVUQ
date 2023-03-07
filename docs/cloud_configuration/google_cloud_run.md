## Google Cloud Run (GCR)

- Containers not Functions
- CPU and memory are independent
- For more resource-demanding models

### GCR limits - [docs](https://cloud.google.com/run/quotas)

- 60min - max timeout value

### GCR

- More customizable option than GC Functions. Allows running code in languages not supported by GCF (e.g. Matlab, Octave)
- Requires additional development work to create a Dockerfile and image push to Google Container Registry
