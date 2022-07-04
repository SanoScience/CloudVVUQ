import chaospy as cp
import numpy as np
import matplotlib.pylab as plt


def plot_Te(results, title=None):
    # plot the calculated Te: mean, with std deviation, 1, 10, 90 and 99%
    plt.figure()
    rho = results.describe('rho', 'mean')
    plt.plot(rho, results.describe('te', 'mean'), 'b-', label='Mean')
    plt.plot(rho, results.describe('te', 'mean') - results.describe('te', 'std'), 'b--', label='+1 std deviation')
    plt.plot(rho, results.describe('te', 'mean') + results.describe('te', 'std'), 'b--')
    plt.fill_between(rho, results.describe('te', 'mean') - results.describe('te', 'std'),
                     results.describe('te', 'mean') + results.describe('te', 'std'), color='b', alpha=0.2)
    plt.plot(rho, results.describe('te', '10%'), 'b:', label='10 and 90 percentiles')
    plt.plot(rho, results.describe('te', '90%'), 'b:')
    plt.fill_between(rho, results.describe('te', '10%'), results.describe('te', '90%'), color='b', alpha=0.1)
    plt.fill_between(rho, results.describe('te', '1%'), results.describe('te', '99%'), color='b', alpha=0.05)
    plt.legend(loc=0)
    plt.xlabel('rho [$m$]')
    plt.ylabel('Te [$eV$]')
    if title:
        plt.title(title)
    plt.savefig('plots/Te.png')


def plot_ne(results, title=None):
    # plot the calculated ne: mean, with std deviation, 1, 10, 90 and 99%
    plt.figure()
    rho = results.describe('rho', 'mean')
    plt.plot(rho, results.describe('ne', 'mean'), 'b-', label='Mean')
    plt.plot(rho, results.describe('ne', 'mean') - results.describe('ne', 'std'), 'b--', label='+1 std deviation')
    plt.plot(rho, results.describe('ne', 'mean') + results.describe('ne', 'std'), 'b--')
    plt.fill_between(rho, results.describe('ne', 'mean') - results.describe('ne', 'std'),
                     results.describe('ne', 'mean') + results.describe('ne', 'std'), color='b', alpha=0.2)
    plt.plot(rho, results.describe('ne', '10%'), 'b:', label='10 and 90 percentiles')
    plt.plot(rho, results.describe('ne', '90%'), 'b:')
    plt.fill_between(rho, results.describe('ne', '10%'), results.describe('ne', '90%'), color='b', alpha=0.1)
    plt.fill_between(rho, results.describe('ne', '1%'), results.describe('ne', '99%'), color='b', alpha=0.05)
    plt.legend(loc=0)
    plt.xlabel('rho [$m$]')
    plt.ylabel('ne [$m^{-3}$]')
    if title:
        plt.title(title)
    plt.savefig('plots/ne.png')


def plot_sobols_first(results, title=None, field='te'):
    # plot the first Sobol results
    plt.figure()
    rho = results.describe('rho', 'mean')
    for k in results.sobols_first()[field].keys():
        plt.plot(rho, results.sobols_first()[field][k], label=k)
    plt.legend(loc=0)
    plt.xlabel('rho [$m$]')
    plt.ylabel('sobols_first')
    if title:
        plt.title(field + ': ' + title)
    plt.savefig('plots/sobols_first_%s.png' % field)


def plot_sobols_second(results, title=None, field='te'):
    # plot the second Sobol results
    plt.figure()
    rho = results.describe('rho', 'mean')
    for k1 in results.sobols_second()[field].keys():
        for k2 in results.sobols_second()[field][k1].keys():
            plt.plot(rho, results.sobols_second()[field][k1][k2], label=k1 + '/' + k2)
    plt.legend(loc=0, ncol=2)
    plt.xlabel('rho [$m$]')
    plt.ylabel('sobols_second')
    if title:
        plt.title(field + ': ' + title)
    plt.savefig('plots/sobols_second_%s.png' % field)


def plot_sobols_total(results, title=None, field='te'):
    # plot the total Sobol results
    plt.figure()
    rho = results.describe('rho', 'mean')
    for k in results.sobols_total()[field].keys():
        plt.plot(rho, results.sobols_total()[field][k], label=k)
    plt.legend(loc=0)
    plt.xlabel('rho [$m$]')
    plt.ylabel('sobols_total')
    if title:
        plt.title(field + ': ' + title)
    plt.savefig('plots/sobols_total_%s.png' % field)


def plot_distribution(results, results_df, title=None):
    te_dist = results.raw_data['output_distributions']['te']
    rho_norm = results.describe('rho_norm', 'mean')
    plt.subplots(3, 3, figsize=(12, 12))
    ip = 0
    for i in [np.maximum(0, int(i - 1))
              for i in np.linspace(0, 1, 9) * rho_norm.shape]:
        ip += 1
        plt.subplot(3, 3, ip)
        pdf_raw_samples = cp.GaussianKDE(results_df.te[i])
        pdf_kde_samples = cp.GaussianKDE(te_dist.samples[i])
        plt.hist(results_df.te[i], density=True, bins=50, label='histogram of raw samples', alpha=0.25)
        if hasattr(te_dist, 'samples'):
            plt.hist(te_dist.samples[i], density=True, bins=50, label='histogram of kde samples', alpha=0.25)

        plt.plot(np.linspace(pdf_raw_samples.lower, pdf_raw_samples.upper),
                 pdf_raw_samples.pdf(np.linspace(pdf_raw_samples.lower, pdf_raw_samples.upper)),
                 label='PDF (raw samples)')
        plt.plot(np.linspace(pdf_kde_samples.lower, pdf_kde_samples.upper),
                 pdf_kde_samples.pdf(np.linspace(pdf_kde_samples.lower, pdf_kde_samples.upper)),
                 label='PDF (kde samples)')

        plt.legend(loc=0)
        plt.xlabel('Te [$eV$]')
        plt.title('Distributions for rho_norm = %0.4f' % (rho_norm[i]))
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.925, wspace=0.4, hspace=0.3)
    if title:
        plt.suptitle(title)
    plt.savefig('plots/distribution_function.png')
