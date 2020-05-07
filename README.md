# Demo of the use of reversed model to study basins of attraction

This is a reboot of [earlier work](http://ginsim.org/basins-reverse) using the CoLoMoTo notebook.

The python notebook uses [bioLQM](http://colomoto.org/biolqm) to construct reversed logical models and then calls
[BoolSim](https://www.vital-it.ch/research/software/boolSim) to identify attractors of the original model and their
backward reachable states using the reversed model (weak basins of attractions).

Operations on sets of states then allow to compute the strong basin of attraction for each attractor.

Further analysis enables to study the boundaries of these basins.

This notebook can be launched using the [CoLoMoTo Docker image](http://colomoto.org/notebook) or directly in mybinder:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aurelien-naldi/reversed-model-demo/master?filepath=reverse-demo)

