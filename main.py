import os
import chaospy as cp
import easyvvuq as uq
from matplotlib import pyplot as plt

from src.executor import Executor

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials/credentials.json'
url = "https://europe-west1-sano-332607.cloudfunctions.net/test_simulation_http"

params = {
    "F": {"type": "float", "default": 1.0},
    "L": {"type": "float", "default": 1.5},
    "a": {"type": "float", "min": 0.7, "max": 1.2, "default": 1.0},
    "D": {"type": "float", "min": 0.75, "max": 0.85, "default": 0.8},
    "d": {"type": "float", "default": 0.1},
    "E": {"type": "float", "default": 200000},
    "outfile": {"type": "string", "default": "/tmp/output.json"}
}
vary = {
    "F": cp.Normal(1, 0.1),
    "L": cp.Normal(1.5, 0.01),
    "a": cp.Uniform(0.7, 1.2),
    "D": cp.Triangle(0.75, 0.8, 0.85),
}

sampler = uq.sampling.SCSampler(vary=vary, polynomial_order=3)

executor = Executor(url, "inputs/beam")
executor.set_sampler(sampler, params)

inputs = executor.draw_samples(256)
# inputs = [inputs[i % len(inputs)] for i in range(10000)]

outputs = executor.run_batch_mode(inputs, 50)

print(outputs)
campaign = executor.create_campaign("tube_deflection")

campaign.apply_analysis(
    uq.analysis.SCAnalysis(
        sampler=campaign.get_active_sampler(),
        qoi_cols=["g1", 'g2', 'g3']
    )
)

results = campaign.get_last_analysis()
plt.axis('off')

if not os.path.exists("results"):
    os.makedirs("results")
results.plot_sobols_treemap('g1', figsize=(10, 10), filename="results/result_g1.png")
results.plot_sobols_treemap('g2', figsize=(10, 10), filename="results/result_g2.png")
results.plot_sobols_treemap('g3', figsize=(10, 10), filename="results/result_g3.png")
