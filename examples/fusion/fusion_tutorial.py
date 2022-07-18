import os
import pickle

import easyvvuq as uq

from fusion_plot import *
from cloudvvuq.easy_executor import EasyExecutor

url = "http://127.0.0.1:8080"  # Local Docker container
# url = "https://cloudvvuq-ymkbuh6guq-ew.a.run.app"  # Cloud Run

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../../credentials/credentials.json'


def define_params():
    return {
        "Qe_tot": {"type": "float", "min": 1.0e6, "max": 50.0e6, "default": 2e6},
        "H0": {"type": "float", "min": 0.00, "max": 1.0, "default": 0},
        "Hw": {"type": "float", "min": 0.01, "max": 100.0, "default": 0.1},
        "Te_bc": {"type": "float", "min": 10.0, "max": 1000.0, "default": 100},
        "chi": {"type": "float", "min": 0.01, "max": 100.0, "default": 1},
        "a0": {"type": "float", "min": 0.2, "max": 10.0, "default": 1},
        "R0": {"type": "float", "min": 0.5, "max": 20.0, "default": 3},
        "E0": {"type": "float", "min": 1.0, "max": 10.0, "default": 1.5},
        "b_pos": {"type": "float", "min": 0.95, "max": 0.99, "default": 0.98},
        "b_height": {"type": "float", "min": 3e19, "max": 10e19, "default": 6e19},
        "b_sol": {"type": "float", "min": 2e18, "max": 3e19, "default": 2e19},
        "b_width": {"type": "float", "min": 0.005, "max": 0.025, "default": 0.01},
        "b_slope": {"type": "float", "min": 0.0, "max": 0.05, "default": 0.01},
        "nr": {"type": "integer", "min": 10, "max": 1000, "default": 100},
        "dt": {"type": "float", "min": 1e-3, "max": 1e3, "default": 100},
    }


def define_vary():
    vary_all = {
        "Qe_tot": cp.Uniform(1.8e6, 2.2e6),
        "H0": cp.Uniform(0.0, 0.2),
        "Hw": cp.Uniform(0.1, 0.5),
        "chi": cp.Uniform(0.8, 1.2),
        "Te_bc": cp.Uniform(80.0, 120.0),
        "a0": cp.Uniform(0.9, 1.1),
        "R0": cp.Uniform(2.7, 3.3),
        "E0": cp.Uniform(1.4, 1.6),
        "b_pos": cp.Uniform(0.95, 0.99),
        "b_height": cp.Uniform(5e19, 7e19),
        "b_sol": cp.Uniform(1e19, 3e19),
        "b_width": cp.Uniform(0.015, 0.025),
        "b_slope": cp.Uniform(0.005, 0.020)
    }
    vary_2 = {
        "Qe_tot": cp.Uniform(1.8e6, 2.2e6),
        "Te_bc": cp.Uniform(80.0, 120.0)
    }
    vary_5 = {
        "Qe_tot": cp.Uniform(1.8e6, 2.2e6),
        "H0": cp.Uniform(0.0, 0.2),
        "Hw": cp.Uniform(0.1, 0.5),
        "chi": cp.Uniform(0.8, 1.2),
        "Te_bc": cp.Uniform(80.0, 120.0)
    }
    vary_10 = {
        "Qe_tot": cp.Uniform(1.8e6, 2.2e6),
        "H0": cp.Uniform(0.0, 0.2),
        "Hw": cp.Uniform(0.1, 0.5),
        "chi": cp.Uniform(0.8, 1.2),
        "Te_bc": cp.Uniform(80.0, 120.0),
        "b_pos": cp.Uniform(0.95, 0.99),
        "b_height": cp.Uniform(5e19, 7e19),
        "b_sol": cp.Uniform(1e19, 3e19),
        "b_width": cp.Uniform(0.015, 0.025),
        "b_slope": cp.Uniform(0.005, 0.020)
    }
    return vary_5


def run_pce_case(pce_order=2):
    sampler = uq.sampling.PCESampler(vary=define_vary(), polynomial_order=pce_order)
    executor = EasyExecutor(url)
    executor.set_sampler(sampler, params=define_params())
    samples = executor.draw_samples()
    outputs = executor.run(samples, max_load=300)

    campaign = executor.create_campaign("fusion",
                                        input_columns=list(define_vary().keys()),
                                        output_columns=["te", "ne", "rho", "rho_norm"])

    results_df = campaign.get_collation_result()
    results = campaign.analyse(qoi_cols=["te", "ne", "rho", "rho_norm"])

    return results_df, results, pce_order, campaign.get_active_sampler().count


if __name__ == '__main__':
    R = {}
    for pce_order in range(1, 7):  # todo run in range(1,7) and update plots
        R[pce_order] = {}
        (R[pce_order]['results_df'],
         R[pce_order]['results'],
         R[pce_order]['order'],
         R[pce_order]['number_of_samples']) = run_pce_case(pce_order=pce_order)

        pickle.dump(R, open(f'collected_results{pce_order}.pickle', 'bw'))

    # plot the convergence of the mean and standard deviation to that of the highest order
    last = -1
    O = [R[r]['order'] for r in list(R.keys())]
    if len(O[0:last]) > 0:
        plt.figure()
        plt.semilogy([o for o in O[0:last]],
                     [np.sqrt(np.mean((R[o]['results'].describe('te', 'mean') -
                                       R[O[last]]['results'].describe('te', 'mean')) ** 2)) for o in O[0:last]],
                     'o-', label='mean')
        plt.semilogy([o for o in O[0:last]],
                     [np.sqrt(np.mean((R[o]['results'].describe('te', 'std') -
                                       R[O[last]]['results'].describe('te', 'std')) ** 2)) for o in O[0:last]],
                     'o-', label='std')
        plt.xlabel('PCE order')
        plt.ylabel('RMSerror compared to order=%s' % (O[last]))
        plt.legend(loc=0)
        plt.savefig('plots/Convergence_mean_std.png')

    # plot the convergence of the first sobol to that of the highest order
    last = -1
    O = [R[r]['order'] for r in list(R.keys())]
    if len(O[0:last]) > 0:
        plt.figure()
        O = [R[r]['order'] for r in list(R.keys())]
        for v in list(R[O[last]]['results'].sobols_first('te').keys()):
            plt.semilogy([o for o in O[0:last]],
                         [np.sqrt(np.mean((R[o]['results'].sobols_first('te')[v] -
                                           R[O[last]]['results'].sobols_first('te')[v]) ** 2)) for o in O[0:last]],
                         'o-',
                         label=v)
        plt.xlabel('PCE order')
        plt.ylabel('RMSerror for 1st sobol compared to order=%s' % (O[last]))
        plt.legend(loc=0)
        plt.savefig('plots/Convergence_sobol_first.png')

    # plot a standard set of graphs for the highest order case
    last = -1
    title = 'fusion test case with PCE order = %i' % list(R.values())[last]['order']
    plot_Te(list(R.values())[last]['results'], title=title, )
    plot_ne(list(R.values())[last]['results'], title=title)
    plot_sobols_first(list(R.values())[last]['results'], title=title)
    plot_sobols_second(list(R.values())[last]['results'], title=title)
    plot_sobols_total(list(R.values())[last]['results'], title=title)
    plot_distribution(list(R.values())[last]['results'], list(R.values())[last]['results_df'], title=title)
    plot_sobols_first(list(R.values())[last]['results'], title=title, field='ne')
    plot_sobols_second(list(R.values())[last]['results'], title=title, field='ne')
    plot_sobols_total(list(R.values())[last]['results'], title=title, field='ne')

    # plot the convergence of the surrogate based on the PCE points ()
    _o = []
    _RMS = []
    for r in R.values():
        results_df = r['results_df']
        results = r['results']
        te_surrogate = np.squeeze(np.array(results.surrogate()(results_df[results.inputs])['te']))
        te_samples = np.array(results_df['te'])
        _RMS.append((np.sqrt((((te_surrogate - te_samples) / te_samples) ** 2).mean())))
        _o.append(r['order'])

    plt.figure()
    plt.semilogy(_o, _RMS, 'o-')
    plt.xlabel('PCE order')
    plt.ylabel('fractional RMS error for the PCE surrogate')
    plt.legend(loc=0)
    plt.savefig('plots/Convergence_surrogate.png')

    # prepare the test data
    sampler = uq.sampling.quasirandom.LHCSampler(vary=define_vary(), count=100)
    executor = EasyExecutor(url, "inputs/fusion.py")
    executor.set_sampler(sampler, params=define_params())
    inputs = executor.draw_samples(1000)
    outputs = executor.run(inputs, max_load=100)

    test_campaign = executor.create_campaign("fusion_pce",
                                             input_columns=list(define_vary().keys()),
                                             output_columns=["te", "ne", "rho", "rho_norm"])

    test_df = test_campaign.get_collation_result()

    # calculate the PCE surrogates
    test_points = test_df[test_campaign.get_active_sampler().vary.get_keys()]
    test_results = test_df['te'].values
    test_predictions = {}
    for i in list(R.keys()):
        test_predictions[i] = np.squeeze(np.array(R[i]['results'].surrogate()(test_points)['te']))

    # plot the performance of the PCE surrogates
    for i in list(R.keys()):
        plt.semilogy(R[i]['results'].describe('rho', 'mean'),
                     np.sqrt(((test_predictions[i] - test_results) ** 2).mean(axis=0)) / test_results.mean(axis=0),
                     label='PCE order %s with %s samples' % (R[i]['order'], R[i]['number_of_samples']))
    plt.xlabel('rho [m]')
    plt.ylabel('fractional RMS for predicted Te')
    plt.legend(loc=0)
    plt.title('Performance of the PCE surrogate')
    plt.savefig('plots/PCE_surrogate.png')

    # plot the convergence of the surrogate based on 1000 random points
    _o = []
    _RMS = []
    for r in R.values():
        _RMS.append((np.sqrt((((test_predictions[r['order']] - test_results) / test_results) ** 2).mean())))
        _o.append(r['order'])

    plt.figure()
    plt.semilogy(_o, _RMS, 'o-')
    plt.xlabel('PCE order')
    plt.ylabel('fractional RMS error for the PCE surrogate')
    plt.legend(loc=0)
    plt.savefig('plots/Convergence_PCE_surrogate.png')
