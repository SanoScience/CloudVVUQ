import os
import chaospy as cp
import easyvvuq as uq
from matplotlib import pyplot as plt

from cloudvvuq.easy_executor import EasyExecutor

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../../credentials/credentials.json'

# url = "http://127.0.0.1:8080"  # Local Docker container
# url = "http://localhost:8080/2015-03-31/functions/function/invocations"  # Local AWS lambda container
# url = "https://cloudvvuq-ymkbuh6guq-ew.a.run.app"  # Cloud Run - Python
# url = "https://europe-west1-sano-332607.cloudfunctions.net/TubeDeflection"  # Cloud Functions - Python
# url = "https://dx6qs64nzckbqqfh73g4m5ssqq0yjmhz.lambda-url.eu-central-1.on.aws/"  # AWS Lambda Image
url = "https://ueo7uf62rzbu5t2bypcjis7qi40tnqpz.lambda-url.eu-central-1.on.aws/"  # AWS Lambda Layer

params = {
    "F": {"type": "float", "default": 1.0},
    "L": {"type": "float", "default": 1.5},
    "a": {"type": "float", "min": 0.7, "max": 1.2, "default": 1.0},
    "D": {"type": "float", "min": 0.75, "max": 0.85, "default": 0.8},
    "d": {"type": "float", "default": 0.1},
    "E": {"type": "float", "default": 200000}
}
vary = {
    "F": cp.Normal(1, 0.1),
    "L": cp.Normal(1.5, 0.01),
    "a": cp.Uniform(0.7, 1.2),
    "D": cp.Triangle(0.75, 0.8, 0.85),
}

sampler = uq.sampling.SCSampler(vary=vary, polynomial_order=3)

executor = EasyExecutor(url)

executor.set_sampler(sampler, params)
samples = executor.draw_samples()
outputs = executor.run(samples, max_load=256, cloud_provider="aws")

campaign = executor.create_campaign("tube_deflection", input_columns=['F', 'L', 'a', 'D', 'd', 'E'],
                                    output_columns=['g1', 'g2', 'g3'])

campaign.apply_analysis(
    uq.analysis.SCAnalysis(
        sampler=campaign.get_active_sampler(),
        qoi_cols=["g1", 'g2', 'g3']
    )
)

results = campaign.get_last_analysis()
plt.axis('off')

results.plot_sobols_treemap('g1', figsize=(10, 10), filename="plots/result_g1.png")
results.plot_sobols_treemap('g2', figsize=(10, 10), filename="plots/result_g2.png")
results.plot_sobols_treemap('g3', figsize=(10, 10), filename="plots/result_g3.png")
