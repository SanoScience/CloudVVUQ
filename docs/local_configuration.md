## General configuration (Executor)
- Set max load value in executor.run method to a smaller value than configured max concurrency.  
```python
executor.run(samples, max_load=256)  
```
- Specify your cloud provider to authorize your simulations using provided credentials.
```python
executor.run(samples, max_load=256, cloud_provider="aws")
```
- Max TCP value in CloudConnector class (e.g. when require >1000 concurrent simulations). Default 1000. (high level config - work in progress)  
```python
aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=1000),  
```
- Timeout value for simulations in CloudConnector class. Default 1 hour. (high level config - work in progress)  
```python
timeout=aiohttp.ClientTimeout(total=3600)) as session:  
```

## Executor configuration

In order to run simulations using CloudVVUQ you need to:  
1. Provide list of samples.
    ```python
    samples = [{"x": 1, "y": 2}, {"x": 2, "y": 3} ...]
    ```
2. Create Executor and specify endpoint:
    ```python
    url = "http://localhost:8080/2015-03-31/functions/function/invocations"
    executor = Executor(url)
    ```
3. Run simulations and wait for it to finish
    ```python
    outputs = executor.run(samples, max_load=256, cloud_provider="aws")
    ```
   

## EasyExecutor configuration

*EasyExecutor* is responsible for providing EasyVVUQ-related methods and extends *Executor* general functionality.

In order to run EasyVVUQ script as CloudVVUQ you need to:  
1. Define sampler and its variances (as you would with EasyVVUQ)
    ```python
    sampler = uq.sampling.SCSampler(vary=vary, polynomial_order=3)
    ```
2. Create EasyExecutor and attach sampler:
    ```python
    executor = EasyExecutor(url)
    executor.set_sampler(sampler, params)
    ```
3. Draw samples
    ```python
    executor.set_sampler(sampler, params)
    ```
4. Run simulations and wait for it to finish
    ```python
    outputs = executor.run(samples, max_load=256, cloud_provider="aws")
    ```
5. Create EasyVVUQ-native campaign object
    ```python
    campaign = executor.create_campaign("campaign_name", 
                                        input_columns=['F', 'L', 'a', 'D', 'd', 'E'],
                                        output_columns=['g1', 'g2', 'g3'])
    ```
From now on you can work on EasyVVUQ object (apply analysis etc.)