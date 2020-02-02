from matplotlib import pyplot as plt

import fipy as fp

__all__ = ['plot_avrami', 'plot_energy', 'plot_fraction', 'plot_count', 'plot_phi']

def load_stats_r1(record):
    """Load stats.txt TSV file associated with `record`

    Loads results from r1 benchmark

    Returns
    ------
    time, fraction, energy : tuple of array
    """
    fname = "Data/{}/stats.txt".format(record["label"])
    return fp.numerix.loadtxt(fname, unpack=True)

def load_stats_r2(record):
    """Load stats.txt TSV file associated with `record`

    Loads results from r2 benchmark

    Returns
    ------
    time, fraction, particle_count, energy : tuple of array
    """
    fname = "Data/{}/stats.txt".format(record["label"])
    return fp.numerix.loadtxt(fname, skiprows=1, unpack=True)

def load_stats(record, rev):
    if rev == 1:
        tt, fraction, energy = load_stats_r1(record)
        particle_count = None
    elif rev == 2:
        tt, fraction, particle_count, energy = load_stats_r2(record)

    return tt, fraction, particle_count, energy

def plot_avrami(record, rev=1):
    tt, fraction, particle_count, energy = load_stats(record, rev=rev)
    plt.loglog(tt, -fp.tools.log10(1-fraction),
               label="$\Delta t = {}$".format(record["--dt"]))

def plot_energy(record, rev=1):
    tt, fraction, particle_count, energy = load_stats(record, rev=rev)
    plt.plot(tt, energy,
             label="$\Delta t = {}$".format(record["--dt"]))

def plot_fraction(record, rev=1):
    tt, fraction, particle_count, energy = load_stats(record, rev=rev)
    plt.plot(tt, fraction,
             label="$\Delta f = {} \Delta f_0$".format(record["--factor"]))

def plot_count(record, rev=2):
    tt, fraction, particle_count, energy = load_stats(record, rev=rev)
    plt.plot(tt, particle_count,
             linestyle="", marker=".", markersize=1,
             label="$\Delta t = {}$".format(record["--dt"]))

def plot_phi(record, timestep=5000.0):
    fname = "Data/{}/t={}.tar.gz".format(record["label"], timestep)
    phi, = fp.tools.dump.read(fname)
    vw = fp.Viewer(vars=phi)
    vw.plot()
