import os

import chaospy as cp
import easyvvuq as uq

import pickle
import numpy as np
import matplotlib.pylab as plt
from cloudvvuq.easy_executor import EasyExecutor

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../../credentials/credentials.json'
url = "https://europe-west1-sano-332607.cloudfunctions.net/Ishigami"  # Cloud Functions


def ishigamiSA(a, b):
    """
    Exact sensitivity indices of the Ishigami function for given a and b.
    From https://openturns.github.io/openturns/master/examples/meta_modeling/chaos_ishigami.html
    """
    var = 1.0 / 2 + a ** 2 / 8 + b * np.pi ** 4 / 5 + b ** 2 * np.pi ** 8 / 18
    S1 = (1.0 / 2 + b * np.pi ** 4 / 5 + b ** 2 * np.pi ** 8 / 50) / var
    S2 = (a ** 2 / 8) / var
    S3 = 0
    S13 = b ** 2 * np.pi ** 8 / 2 * (1.0 / 9 - 1.0 / 25) / var
    exact = {
        'expectation': a / 2,
        'variance': var,
        'S1': (1.0 / 2 + b * np.pi ** 4 / 5 + b ** 2 * np.pi ** 8.0 / 50) / var,
        'S2': (a ** 2 / 8) / var,
        'S3': 0,
        'S12': 0,
        'S23': 0,
        'S13': S13,
        'S123': 0,
        'ST1': S1 + S13,
        'ST2': S2,
        'ST3': S3 + S13
    }
    return exact


Ishigami_a = 7.0
Ishigami_b = 0.1
exact = ishigamiSA(Ishigami_a, Ishigami_b)

params = {
    "x1": {"type": "float", "min": -np.pi, "max": np.pi, "default": 0.0},
    "x2": {"type": "float", "min": -np.pi, "max": np.pi, "default": 0.0},
    "x3": {"type": "float", "min": -np.pi, "max": np.pi, "default": 0.0},
    "a": {"type": "float", "min": Ishigami_a, "max": Ishigami_a, "default": Ishigami_a},
    "b": {"type": "float", "min": Ishigami_b, "max": Ishigami_b, "default": Ishigami_b},
}

vary = {
    "x1": cp.Uniform(-np.pi, np.pi),
    "x2": cp.Uniform(-np.pi, np.pi),
    "x3": cp.Uniform(-np.pi, np.pi)
}


def run_campaign(sc_order=2):
    sampler = uq.sampling.SCSampler(vary=vary, polynomial_order=sc_order)
    executor = EasyExecutor(url)
    executor.set_sampler(sampler, params)

    samples = executor.draw_samples()
    outputs = executor.run(samples, batch_size=400)

    campaign = executor.create_campaign("ishigami", input_columns=['x1', 'x2', 'x3', 'a', 'b'],
                                        output_columns=['ishigami'])

    results_df = campaign.get_collation_result()
    results = campaign.analyse(qoi_cols=["ishigami"])

    return results_df, results, sc_order, campaign.get_active_sampler().count


# Calculate the stochastic collocation expansion for a range of orders
R = {}
for sc_order in range(1, 15):
    R[sc_order] = {}
    (R[sc_order]['results_df'],
     R[sc_order]['results'],
     R[sc_order]['order'],
     R[sc_order]['number_of_samples']) = run_campaign(sc_order=sc_order)


# save the results
pickle.dump(R, open('collected_results.pickle', 'bw+'))


# plot the convergence of the mean and standard deviation to that of the highest order
mean_analytic = exact['expectation']
std_analytic = np.sqrt(exact['variance'])

O = [R[r]['order'] for r in list(R.keys())]
plt.figure()
plt.semilogy([o for o in O],
             [np.abs(R[o]['results'].describe('ishigami', 'mean') - mean_analytic) for o in O],
             'o-', label='mean')
plt.semilogy([o for o in O],
             [np.abs(R[o]['results'].describe('ishigami', 'std') - std_analytic) for o in O],
             'o-', label='std')
plt.xlabel('SC order')
plt.ylabel('RMSerror compared to analytic')
plt.legend(loc=0)
plt.savefig('plots/Convergence_mean_std.png')


# plot the convergence of the first sobol to that of the highest order
sobol_first_exact = {'x1': exact['S1'], 'x2': exact['S2'], 'x3': exact['S3']}
O = [R[r]['order'] for r in list(R.keys())]
plt.figure()
for v in list(R[O[0]]['results'].sobols_first('ishigami').keys()):
    plt.semilogy([o for o in O],
                 [np.abs(R[o]['results'].sobols_first('ishigami')[v] - sobol_first_exact[v]) for o in O],
                 'o-',
                 label=v)
plt.xlabel('SC order')
plt.ylabel('ABSerror for 1st sobol compared to analytic')
plt.legend(loc=0)
plt.savefig('plots/Convergence_sobol_first.png')


# prepare the test data
sampler = uq.sampling.quasirandom.LHCSampler(vary=vary, count=100)
executor_test = EasyExecutor(url)
executor_test.set_sampler(sampler, params)
samples = executor_test.draw_samples(1000)
executor_test.run(samples)
campaign_test = executor_test.create_campaign("ishigami_test", input_columns=['x1', 'x2', 'x3', 'a', 'b'],
                                              output_columns=['ishigami'])
test_df = campaign_test.get_collation_result()


# calculate the SC surrogates
test_points = test_df[campaign_test.get_active_sampler().vary.get_keys()]
test_results = np.squeeze(test_df['ishigami'].values)
test_predictions = {}
for i in list(R.keys()):
    test_predictions[i] = np.squeeze(np.array(R[i]['results'].surrogate()(test_points)['ishigami']))


# plot the convergence of the surrogate
_o = []
_RMS = []
for r in R.values():
    _RMS.append((np.sqrt(((test_predictions[r['order']] - test_results) ** 2).mean())))
    _o.append(r['order'])

plt.figure()
plt.semilogy(_o, _RMS, 'o-')
plt.xlabel('SC order')
plt.ylabel('RMS error for the SC surrogate')
plt.legend(loc=0)
plt.savefig('plots/Convergence_SC_surrogate.png')
