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

totaltime = params['totaltime']
dt = params['dt']
Lx = params['Lx']
Ly = params['Ly']

dx = params['dx']

mesh = fp.PeriodicGrid2D(Lx=Lx, dx=dx, Ly=Ly, dy=dx)
x, y = mesh.cellCenters[0], mesh.cellCenters[1]
X, Y = mesh.faceCenters[0], mesh.faceCenters[1]

elapsed = fp.Variable(name="$t$", value=0.)

phi = fp.CellVariable(mesh=mesh, name="$phi$", value=0., hasOld=True)

Delta_f = 1. / (15 * fp.numerix.sqrt(2.))

r = params['factor'] * 5
phi.setValue(1., where=(x - Lx/2.)**2 + (y - Lx/2.)**2 <= r**2)

# following examples/phase/simple.py

dmPhidPhi = 4 + 30 * (1 - 2 * phi) * Delta_f
S1 = dmPhidPhi * phi * (1 - phi) + mPhi * (1 - 2 * phi)
S0 = mPhi * phi * (1 - phi) - S1 * phi

eq = (fp.TransientTerm() == 
      fp.DiffusionTerm(coeff=1.) + S0 + fp.ImplicitSourceTerm(coeff=S1))

with open(data['stats.txt'].make().abspath, 'a') as f:
    f.write("\t".join(["time", "fraction", "energy"]) + "\n")

start = time.time()

while elapsed.value <= totaltime:
    phi.updateOld()
    for sweep in range(5):
        eq.sweep(var=phi, dt=dt)
    elapsed.value = elapsed() + dt
    with open(data['stats.txt'].make().abspath, 'a') as f:
        f.write("{}\t{}\t{}\n".format(t, 
                                      (phi.cellVolumeAverage * mesh.numberOfCells).value,
                                      (ftot.cellVolumeAverage * mesh.numberOfCells).value))

end = time.time()

data.categories["solvetime"] = end - start
