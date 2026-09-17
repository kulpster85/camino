# Installation

!!! note "Placeholder page"
    This page will later include a full install guide, optional dependencies, and notes for local development.

## Basic installation

```bash
pip install -e ".[dev]"
```

## Notes

CAMINO depends on JAX-based optical modelling and may require a compatible Python environment. The docs build itself is intentionally flexible and does not import the full package at build time.
