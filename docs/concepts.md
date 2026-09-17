# Concepts and workflow

!!! note "Placeholder page"
    This page will later explain the central definitions and the end-to-end inference workflow in detail.

## Definitions

This section will describe the core abstractions used by CAMINO, including:

- OPD and pupil-plane quantities
- defocus and optical propagation terms
- PSFs and post-processing cutouts
- the role of WLP8/WLM8 pupil states
- filter throughput and spectral weighting
- exposure-level data objects and parameter keys

## End-to-end workflow

This section will walk through the overall pipeline:

1. read and validate an exposure
2. build the model from the current parameter set
3. generate a forward-modeled PSF
4. compare with observed cutouts
5. optimise or diagnose the parameter values
6. inspect convergence and residuals

## Parameter keying

The model stores parameters by exposure and by physical concept; later documentation will explain how `get_key` and `map_param` are used to share or isolate values across observations.
