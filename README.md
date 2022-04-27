# CloudVVUQ (very alpha version)
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
3. Deploy GC Function source code to Cloud, copy url to code or use currently provided one.
```python
url = "https://europe-west1-sano-332607.cloudfunctions.net/test_simulation_http"
```
4. Upload your desired simulation file to storage.
5. Use *Executor* class for running simulations: 
   - create EasyVVUQ sampler with parameters
   - create instance of *Executor* class
   - draw samples from sampler 
   - use *executor.run()* or *executor.run_batch_mode()* to start simulations
6. Create EasyVVUQ *Campaign* object  and analyze.
7. When in doubt follow scripts in examples directory.
