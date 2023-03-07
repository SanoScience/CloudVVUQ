## Tube Deflection example

Adapted for CloudVVUQ from EasyVVUQ tutorials. Original tutorial [here](https://github.com/UCL-CCS/EasyVVUQ/blob/dev/tutorials/basic_tutorial.ipynb).

The examples/tube_deflection directory contains ready-to-deploy source code for deployment types such as:

- Google Cloud Functions (Python)
- Google Cloud Run (Python)
- Google Cloud Run (source code translated to Octave)
- AWS Lambda (zip with layers)
- AWS Lambda (image)

All are compatible with tube_deflection_tutorial.py script. Deploy the code to your service and use your new endpoint in the script.  
Remember to configure executor.run (max load and proper provider).