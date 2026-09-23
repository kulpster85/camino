# Worked example

The quickest runnable walkthrough for this repository is the downloadable notebook [`camino_quickstart.ipynb`](camino_quickstart.ipynb).

It shows how to:

- install and import CAMINO in a notebook environment
- generate a small synthetic defocused exposure
- provide local filter-throughput tables without depending on external data packages
- load an exposure with `camino.exposure_from_defocus_file`
- evaluate wavelength bins with `camino.calc_throughput`
- confirm where dLux enters the CAMINO workflow through `camino.SinglePointFilterFit`

For the complete local setup, real-data expectations, and dLux compatibility notes, see [How to run CAMINO](../how_to_run.md).
