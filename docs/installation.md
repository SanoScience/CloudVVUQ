### New conda environment and use CloudVVUQ dir

1. Clone CloudVVUQ repository
2. Create environment:  
    ```bash
    conda create --name CloudVVUQ  
    ```  
    ```bash
    conda activate CloudVVUQ
    ```
3. Install required packages:  
    ```bash
    conda install --file requirements.txt  
    ```
   
### Use existing environment
1. Clone CloudVVUQ repository
2. Activate your environment
3. Get path to CloudVVUQ wheel file, replace it in the command below. 
   ```bash
   pip install "path/to/cloudvvuq/dist/cloudvvuq-*.whl"
   ```
4. Run it to install CloudVVUQ module
   