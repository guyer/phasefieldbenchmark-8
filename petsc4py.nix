{ lib, fetchPypi, pythonPackages, openmpi, hdf5, petsc }:

pythonPackages.buildPythonPackage rec {
  version = "3.13.0";
  pname = "petsc4py";

  src = fetchPypi {
    inherit pname version;
    sha256 = "0f8gcicc7ilr2p3mhg2bjyk8kfpd0x9bd0bcmkpjyx9f21qizqmc";
  };

  buildInputs = [
    pythonPackages.cython
    openmpi
    hdf5
    petsc
  ];

  PETSC_DIR = "${petsc.out}";

  propagatedBuildInputs = [
    pythonPackages.numpy
  ];

  meta = with lib; {
    homepage = "https://bitbucket.org/petsc/petsc4py/";
    description = "Python bindings for PETSc.";
    license = licenses.bsd2;
  };
}
