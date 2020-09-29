# Phase Field Benchmark Problems for Nucleation

*Add DOI Link for this repository to include in paper. Can we do that in time?*

This repository contains supplementary material and code necessary to
run some of the examples from the paper entitled *Phase Field
Benchmark Problems for Nucleation* authored by *W. Wu et al.* (not yet
submitted).

## Overview

During the development of the nucleation benchmark problem a number of
implementations from different codes were used to ascertain the
accuracy and robustness of both the benchmark specification and the
numerical results from the specification. The nucleation benchmark is
an important addition to the existing phase field benchmarks on the
[PFHub website][PFHub] as it describes the initial stages of many
thermodynamic processes. For more details about the benchmark and the
specification for the benchmark problem consults the paper for a
details description and the [PFHub website][PFHub] for a concise
specification and further results and examples of implementations.

Four different codes are used to implement the benchmark
specification. The results from each of these codes indicate good
convergence demonstrating the overall robustness of the
specification. The four codes include [MOOSE][MOOSE], [FiPy][FiPy],
[PRISMS-PF] and an unpublished custom finite difference code. Each of
these are in a separate directory (['moose'](moose/README.md),
['fipy'](fipy/README.md), ['prisms-pf'][primsms-pf/README.md) and
['custom'](custom/README.md)) with detailed installation and usage
instructions. The included examples do not cover every example
implemented in the paper, but a few relevant examples. It is hoped
that other examples from the paper can be implemented by editing the
input files.

The development of this repostiory is an ongoing process and probably
will only be completed after the paper has already been published.

## Feedback

## Credits

## License

Read the [terms of use](./LICENSE.md).

[PFHub]: https://pages.nist.gov/pfhub/
[MOOSE]: https://www.mooseframework.org/
[FiPy]: https://www.ctcms.nist.gov/fipy/
