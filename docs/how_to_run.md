# How to run CAMINO

This repository already depends on [dLux](https://github.com/LouisDesdoigts/dLux), but CAMINO adds its own JWST/NIRCam-specific helpers on top of the general dLux modelling stack. The fastest way to get started is to install CAMINO in an isolated environment, run the tests, and then open the bundled quickstart notebook.

## 1. Create a local environment

CAMINO requires Python 3.10 or newer. For notebook work, install the development extras so that Jupyter and the docs tooling are available too.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

That installation pulls in dLux from GitHub via the dependency declared in `pyproject.toml`.

## 2. Sanity-check the repository

Run the existing test suite before trying real data or notebook work:

```bash
pytest tests
```

## 3. Open the runnable example notebook

The repository now includes a self-contained notebook at [`docs/examples/camino_quickstart.ipynb`](examples/camino_quickstart.ipynb). Start Jupyter and open that file:

```bash
jupyter lab docs/examples/camino_quickstart.ipynb
```

The notebook creates a synthetic JWST-like defocused exposure, writes a small local filter-throughput table, and exercises the current public CAMINO entry points:

- `camino.exposure_from_defocus_file`
- `camino.calc_throughput`
- `camino.SinglePointFilterFit`
- `camino.get_pupil`

Because the example writes its own throughput table and FITS file, it does **not** require the optional `amigo` package or any external calibration data.

## 4. Switch from synthetic data to a real exposure

When you move from the notebook's synthetic example to real data, keep these interfaces in mind:

### FITS expectations

`camino.exposure_from_defocus_file(...)` expects:

- a primary header with `OBS_ID` and `PUPIL`
- ideally a `FILTER` keyword (otherwise CAMINO falls back to `F212N` with a warning)
- one of `MJD-AVG`, `EXPMID`, or `EXPSTART` if you want a numeric observation time
- an image extension named `SCI`
- an image extension named `ERR`

### Throughput tables

`camino.calc_throughput(...)` looks for two-column filter tables named `{FILTER}.dat`. Each file should contain:

1. wavelength in Angstroms
2. throughput weight

You can either:

- pass `filters_dir=/path/to/filter_tables`, or
- install the optional dependency that provides the default filter directory used by CAMINO.

## 5. How CAMINO relates to dLux and the dLux tutorials

CAMINO is intended to run **with** dLux, not instead of it. In the current codebase, CAMINO directly imports and uses dLux types such as `dl.Optic`, `dl.PointSource`, `dl.PSF`, `dl.Spectrum`, and detector-layer base classes.

### Can I use the dLux getting-started tutorial in the same environment?

Yes. After installing CAMINO, you can usually run the dLux introductory notebook in the same environment because CAMINO already installs dLux itself. The one extra step is to install the tutorial-only packages that are imported there but are not part of CAMINO's base dependencies:

```bash
python -m pip install optax matplotlib tqdm
```

If you want to be explicit about the dLux version used by this repository, reinstall the same dependency source that CAMINO declares:

```bash
python -m pip install --upgrade 'dLux @ git+https://github.com/LouisDesdoigts/dLux.git'
```

### Is CAMINO a drop-in replacement for the dLux tutorial notebook?

Not exactly. The dLux tutorial at <https://github.com/LouisDesdoigts/dLux_tutorials/blob/main/tutorials/introductory/getting_started.ipynb> teaches the general dLux modelling workflow. CAMINO builds on that foundation, but its main entry points are specialised for JWST/NIRCam-style exposures, cutouts, throughput tables, and inference helpers.

A practical way to use both projects together is:

1. work through the dLux tutorial to learn the core optics objects and modelling style
2. use `docs/examples/camino_quickstart.ipynb` to learn the CAMINO-specific data-loading and throughput workflow
3. combine the two when you are ready to build a custom forward model around your own dLux optics configuration

## 6. Build the docs locally

If you want to preview the documentation site after making changes, use the existing docs workflow locally:

```bash
python docs/scripts/generate_api_mds.py
zensical build -f mkdocs.yml --strict
```
