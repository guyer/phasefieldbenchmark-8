# script based on 
# Benchmark problems for nucleation
# Tamas Pusztai
# September 25, 2019

import os
import sys
import time
import yaml

import datreant.core as dtr

import fipy as fp
from fipy.tools import parallelComm
from fipy.meshes.factoryMeshes import _dnl

from fipy.tools.debug import PRINT

yamlfile = sys.argv[1]

with open(yamlfile, 'r') as f:
    params = yaml.load(f)

try:
    from sumatra.projects import load_project
    project = load_project(os.getcwd())
    record = project.get_record(params["sumatra_label"])
    output = record.datastore.root
except:
    # either there's no sumatra, no sumatra project, or no sumatra_label
    # this will be the case if this script is run directly
    output = os.getcwd()

if parallelComm.procID == 0:
    print "storing results in {0}".format(output)
    data = dtr.Treant(output)
else:
    class dummyTreant(object):
        categories = dict()

    data = dummyTreant()

# solve

savetime = params['savetime']
totaltime = params['totaltime']
dt = params['dt']

Lx = params['Lx']
Ly = params['Ly']

dx, nx = _dnl(dx=params['dx'], nx=None, Lx=Lx)
dy, ny = _dnl(dx=params['dx'], nx=None, Lx=Ly)

mesh = fp.Grid2D(dx=dx, nx=nx, dy=dy, ny=ny)
x, y = mesh.cellCenters[0], mesh.cellCenters[1]
X, Y = mesh.faceCenters[0], mesh.faceCenters[1]

elapsed = fp.Variable(name="$t$", value=0.)

phi = fp.CellVariable(mesh=mesh, name="$phi$", value=0., hasOld=True)

Delta_f = 1. / (6 * fp.numerix.sqrt(2.))

ftot = (0.5 * phi.grad.mag**2
        + phi**2 * (1 - phi)**2
        - Delta_f * phi**3 * (10 - 15 * phi + 6 * phi**2))

for xx, yy in fp.numerix.random.random(size=(100, 2)):
    r = fp.numerix.sqrt((x - xx * Lx)**2 + (y - yy * Ly)**2)

    r0 = params['factor'] * 2
    phi.setValue(phi + (1 - fp.numerix.tanh((r - r0) / fp.numerix.sqrt(2.))) / 2)

phi.setValue(1., where=phi > 1.)

# viewer = fp.Viewer(vars=phi) #, datamin=0., datamax=1.)
# viewer.plot()

# following examples/phase/simple.py

mPhi = -2 * (1 - 2 * phi) + 30 * phi * (1 - phi) * Delta_f
dmPhidPhi = 4 + 30 * (1 - 2 * phi) * Delta_f
S1 = dmPhidPhi * phi * (1 - phi) + mPhi * (1 - 2 * phi)
S0 = mPhi * phi * (1 - phi) - S1 * phi

eq = (fp.TransientTerm() == 
      fp.DiffusionTerm(coeff=1.) + S0 + fp.ImplicitSourceTerm(coeff=S1))

phiAvg = (phi.cellVolumeAverage).value
volumes = fp.CellVariable(mesh=mesh, value=mesh.cellVolumes)
F = (ftot.cellVolumeAverage * volumes.sum()).value

if parallelComm.procID == 0:
    with open(data['stats.txt'].make().abspath, 'a') as f:
        f.write("\t".join(["time", "fraction", "energy"]) + "\n")
        f.write("{}\t{}\t{}\n".format(elapsed, phiAvg, F))

if parallelComm.procID == 0:
    fname = data["t={}.tar.gz".format(elapsed)].make().abspath
else:
    fname = None

fname = parallelComm.bcast(fname)
fp.tools.dump.write((phi,), filename=fname)

while elapsed.value <= savetime:
    phi.updateOld()
    for sweep in range(5):
        eq.sweep(var=phi, dt=dt)
    elapsed.value = elapsed() + dt
    phiAvg = (phi.cellVolumeAverage).value
    F = (ftot.cellVolumeAverage * volumes.sum()).value
    if parallelComm.procID == 0:
        with open(data['stats.txt'].make().abspath, 'a') as f:
            f.write("{}\t{}\t{}\n".format(elapsed, phiAvg, F))
    parallelComm.Barrier()
    if elapsed.value == savetime:
        if parallelComm.procID == 0:
            fname = data["t={}.tar.gz".format(elapsed)].make().abspath
        else:
            fname = None

        fname = parallelComm.bcast(fname)

        fp.tools.dump.write((phi,), filename=fname)
        if savetime < totaltime:
            savetime = totaltime
        else:
            break
#     viewer.plot()

