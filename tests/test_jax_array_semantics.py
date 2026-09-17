import jax
import jax.numpy as jnp
import pytest

import dLux as dl

import camino


@pytest.mark.parametrize("dtype", [jnp.float32, jnp.float64])
def test_pixel_anisotropy_keeps_jax_array(dtype):
    psf = dl.PSF(jnp.ones((8, 8), dtype=dtype), pixel_scale=1.0)
    out = camino.PixelAnisotropy(order=1).apply(psf)
    assert isinstance(out.data, jax.Array)
    assert out.data.shape == psf.data.shape
    assert jnp.asarray(out.data).dtype == jnp.asarray(out.data).dtype


def test_jacfwd_returns_jax_array():
    model = camino.ModelParams({"x": jnp.array([1.0, 2.0], dtype=jnp.float32)})
    jac = model.jacfwd(lambda m: jnp.sum(m.x**2))
    assert isinstance(jac, jax.Array)
    assert jac.dtype == jnp.float32
    assert jac.shape == (2,)


def test_jwst_primary_normalises_with_jax_norm():
    wavefront = type("Wavefront", (), {})()
    wavefront.amplitude = jnp.array([3.0, 4.0], dtype=jnp.float32)
    wavefront.phase = jnp.zeros_like(wavefront.amplitude)
    wavefront.wavenumber = jnp.array(1.0, dtype=jnp.float32)
    wavefront.set = lambda keys, values: {"amplitude": values[0], "phase": values[1]}

    optic = camino.JWSTPrimary(
        transmission=jnp.ones_like(wavefront.amplitude),
        opd=jnp.zeros_like(wavefront.amplitude),
    )
    out = optic.apply(wavefront)

    assert isinstance(out["amplitude"], jax.Array)
    assert jnp.isclose(jnp.linalg.norm(out["amplitude"]), 1.0)
