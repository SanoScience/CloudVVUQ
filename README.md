# CloudVVUQ
Python library to run simulations on cloud with EasyVVUQ functionality

### Prepare conda environment

1. Clone this repository
2. Create environment

```bash
conda create --name CloudVVUQ
conda activate CloudVVUQ
```

3. Install required packages

```bash
conda install --file requirements.txt
```

### User Guide:
1. Download credentials file from your project's service-account (required storage upload/access and cloud function invoke permissions)
2. Install *credentials.json* file in project's root or create credentials dir. In code set path accordingly:
```python
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials/credentials.json'
```
3. Deploy GC Function source code to Cloud:
- Cloud Functions (fast and easy, limited dependencies and runtime languages)
- Cloud Run (required docker image with application, unlimited dependencies and runtime languages)

Copy your deployed application url. Example:
```python
url = "https://europe-west1-project-id.cloudfunctions.net/Simulation"
```
or 
```python
url = "https://cloudrun_app_name-ymkbuh6guq-ew.a.run.app"
```
4. Use *Executor* class for running simulations: 
   - define parameters and create EasyVVUQ sampler with vary
   - create instance of *Executor* class
   - add parameters and sampler to your executor
   - draw samples from sampler 
   - use *executor.run(samples)* to start simulations
5. Create EasyVVUQ *Campaign* object and analyze.  

When in doubt follow scripts in examples directory.
