from matplotlib import pyplot as plt

import fipy as fp

__all__ = ['plot_avrami', 'plot_energy', 'plot_fraction', 'plot_phi']

def load_stats(record):
    """Load stats.txt TSV file associated with `record`
    
    Returns
    ------
    time, fraction, energy : tuple of array
    """
    fname = "Data/{}/stats.txt".format(record["label"])
    return fp.numerix.loadtxt(fname, unpack=True)
    
def plot_avrami(record):
    tt, fraction, energy = load_stats(record)
    plt.loglog(tt, -fp.tools.log10(1-fraction),
               label="$\Delta t = {}$".format(record["--dt"]))

def plot_energy(record):
    tt, fraction, energy = load_stats(record)
    plt.plot(tt, energy,
             label="$\Delta t = {}$".format(record["--dt"]))

def plot_fraction(record):
    tt, fraction, energy = load_stats(record)
    plt.plot(tt, fraction,
             label="$\Delta f = {} \Delta f_0$".format(record["--factor"]))

def plot_phi(record, timestep=5000.0):
    fname = "Data/{}/t={}.tar.gz".format(record["label"], timestep)
    phi, = fp.tools.dump.read(fname)
    vw = fp.Viewer(vars=phi)
    vw.plot()
