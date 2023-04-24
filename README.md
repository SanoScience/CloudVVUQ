# CloudVVUQ
What:  
**CloudVVUQ** - python library which allows running simulations **in parallel** and in the **cloud** with EasyVVUQ functionality.    

Why:  
To **speed up** VVUQ and sensitivity analysis (SA) computations using serverless compute services and extend EasyVVUQ library.   

How:  
VVUQ and SA processes require many independent executions of analyzed model. This step is an **embarrassingly-parallel** problem and can be **parallelized** using **serverless** computing.

For who:  
**Scientists** with some technical background already running VVUQ and SA processes on HPC or local machines. 

Performance:  
Using this library you can speed your calculations hundreds or thousands of times.

How to use:  
1. Have access to one or more cloud providers and choose suitable service for your model.  
2. Prepare your model for cloud (see model_preparation section).  
3. Install CloudVVUQ locally.  
4. Prepare script that starts CloudVVUQ executor / Adapt your existing EasyVVUQ script.  
5. Deploy the model (see model_deployment section). Test it on smaller scale.  
6. Launch full-scale simulations.   
 
## Documentation
To run docs:
```bash
mkdocs serve
```

## Acknowledgments

This work is supported by the European Union’s Horizon 2020 research and innovation programme under grant agreement Sano No 857533 and carried out within the International Research Agendas programme of the Foundation for Polish Science, co-financed by the European Union under the European Regional Development Fund.  
This work is also partly supported by the European Union’s Horizon 2020 research and innovation programme under grant agreement ISW No 101016503.

## License

The library is published under the MIT license. However, the *examples* directory is published under the LGPLv3 license.
