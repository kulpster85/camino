# Concepts and workflow

CAMINO performs forward modelling and inference of defocused point-spread
functions (PSFs) from telescope exposures. The model connects the optical
state of the telescope, represented by the amplitude and phase of a
pupil-plane complex field, to the measured detector image through physical
optical propagation, detector sampling, and image-formation effects.

This page collects the assumptions, notation, and background needed to
understand the CAMINO model and the associated inference workflow.

## Physical context

The wavefront-sensing and control (WFC&S) problem for a segmented telescope
spans a large dynamic range, from the coarse misalignment immediately after
deployment to the final diffraction-limited state. For JWST, early deployment
stages used geometric and centroid-based techniques to locate and position
the segment images. Large coarse piston errors were subsequently corrected
using dispersed fringe sensing with the Dispersed Hartman Sensor, which
measures relative segment piston through wavelength-dependent interference
patterns. Global solutions were then obtained through least-squares
reconstruction across the segments.

CAMINO addresses the later, high-precision regime in which the optical state
can be inferred from the detailed morphology of defocused PSFs. The weak-lens
observations considered here produce extended, approximately annular PSFs
rather than sharply peaked in-focus images. This makes robust localisation
and physically consistent optical propagation important parts of the
inference process.

## Optical representation

### Pupil-plane field

The optical field at the entrance pupil is represented as a complex field

$$
U(x,y) = A(x,y)\,\exp\left[i\,\phi(x,y)\right],
$$

where:

- $A(x,y)$ is the amplitude transmission of the pupil;
- $\phi(x,y)$ is the optical phase;
- $x$ and $y$ are transverse coordinates in the pupil plane.

The phase is determined by the optical path difference (OPD). Thus the
pupil-plane state contains both the amplitude structure of the aperture and
the phase structure of the wavefront.

The forward model propagates this complex field to the detector plane. Because
the complex field is retained during propagation, both amplitude and phase
information contribute to the resulting intensity pattern.

### ABCD matrices and linear canonical transforms

CAMINO uses a physical-optics description based on the scalar diffraction
approximation. Optical propagation is represented using the Collins
diffraction integral in the framework of linear canonical transforms (LCTs).

A first-order optical system is described by an ABCD ray-transfer matrix,

$$
\begin{pmatrix}
x_2 \\
\theta_2
\end{pmatrix}
=
\begin{pmatrix}
A & B \\
C & D
\end{pmatrix}
\begin{pmatrix}
x_1 \\
\theta_1
\end{pmatrix},
$$

where $x$ is the transverse spatial coordinate and $\theta$ is the
propagation angle relative to the optical axis.

For a general ABCD system with $B\ne0$, the propagated field can be written
as the Collins diffraction integral,

$$
U(x') =
\frac{1}{i\lambda B}
\exp\left(\frac{i\pi D x'^2}{\lambda B}\right)
\int U(x)
\exp\left(\frac{i\pi A x^2}{\lambda B}\right)
\exp\left(-\frac{i2\pi xx'}{\lambda B}\right)\,dx.
$$

Here:

- $U(x)$ and $U(x')$ are the complex fields at the input and output planes;
- $x$ and $x'$ are the transverse coordinates in those planes;
- $\lambda$ is the wavelength;
- $A$, $B$, $C$, and $D$ are the ABCD matrix elements;
- $B$ has units of length and sets the scale of the diffraction integral.

The quadratic phase factors are the input and output chirps. The cross-term
contains the Fourier-transform kernel, with spatial-frequency scaling set by
$\lambda B$.

For the optical system considered here, propagation is represented by a
thin lens followed by free-space propagation. The corresponding matrices are

$$
M_{\mathrm{lens}}(f) =
\begin{pmatrix}
1 & 0 \\
-1/f & 1
\end{pmatrix},
\qquad
M_{\mathrm{free}}(L) =
\begin{pmatrix}
1 & L \\
0 & 1
\end{pmatrix},
$$

where $f$ is the focal length and $L$ is the propagation distance from the
lens to the detector plane. The complete system is therefore

$$
M =
M_{\mathrm{free}}(L)\,M_{\mathrm{lens}}(f)
=
\begin{pmatrix}
1-L/f & L \\
-1/f & 1
\end{pmatrix}.
$$

This matrix determines the LCT parameters used for numerical propagation.

### Matrix Fourier transform

The Collins integral is evaluated numerically using a separable
chirp-transform-chirp representation,

$$
U_{\mathrm{out}}
=
C_{\mathrm{post}}\,
\mathcal{F}_{\mathrm{MFT}}
\left[
C_{\mathrm{pre}}\,U_{\mathrm{in}}
\right],
$$

where $C_{\mathrm{pre}}$ and $C_{\mathrm{post}}$ are the quadratic phase
factors determined by the ABCD coefficients and
$\mathcal{F}_{\mathrm{MFT}}$ is a matrix Fourier transform (MFT).

An MFT is used rather than a fast Fourier transform (FFT) because the input
and output sampling rates can be specified independently. This allows the
numerical detector grid to be matched directly to the physical detector
pixel scale and optical geometry, rather than imposing the sampling
relationship associated with an FFT.

The propagation operators are differentiable, allowing derivatives of the
forward model with respect to optical and exposure-level parameters.

## Defocus

Defocus is represented physically by changing the propagation distance rather
than by inserting an approximate quadratic phase term into the pupil.

In the absence of defocus, the detector plane is at the nominal focal plane,
so

$$
L=f.
$$

A defocus displacement $\Delta z$ is represented by

$$
L=f+\Delta z.
$$

The corresponding optical system matrix is

$$
M(\Delta z)
=
M_{\mathrm{free}}(f+\Delta z)\,
M_{\mathrm{lens}}(f)
=
\begin{pmatrix}
1-(f+\Delta z)/f & f+\Delta z \\
-1/f & 1
\end{pmatrix}.
$$

This treats defocus as a displacement of the observation plane and preserves
the full propagation operator. It therefore does not rely on the
near-focus approximations associated with representing defocus solely as a
quadratic pupil-plane phase.

For weak-lensing NIRCam observations, the nominal defocus states are discrete
pupil configurations such as **WLP8** and **WLM8**. The corresponding
$\Delta z$ values are nevertheless exposure-dependent model parameters and
can be refined during inference to account for uncertainty in the actual
optical configuration.

## Detector sampling and image formation

### Detector-plane sampling

The propagated field is evaluated on a discrete grid representing the
physical detector sampling.

Let:

- $\theta$ be an angular coordinate on the sky;
- $x$ be the corresponding physical coordinate in the focal plane;
- $f$ be the effective focal length.

Under the paraxial approximation,

$$
x=f\,\theta.
$$

For a detector with angular pixel scale $\Delta\theta$ in radians per pixel,
the corresponding physical sampling is

$$
\Delta x=f\,\Delta\theta.
$$

CAMINO uses an oversampling factor of $s=4$, giving an effective numerical
sampling of

$$
\Delta x_{\mathrm{eff}}=\frac{\Delta x}{s}.
$$

The propagated field is consequently evaluated on a grid with

$$
N_{\mathrm{out}}=s\,N_{\mathrm{psf}},
$$

and spacing $\Delta x_{\mathrm{eff}}$ in each dimension.

The distinction between the optical propagation grid and the native detector
grid is important: propagation can be performed at an oversampled resolution
before detector-level transformations are applied.

### PSF and normalisation

The detector measures intensity corresponding to the squared modulus of the
propagated complex field,

$$
I_{\mathrm{model}}(x,y)=\left|U(x,y)\right|^2.
$$

The resulting PSF is normalised to unit flux over the valid detector region,

$$
P(x,y)
=
\frac{I_{\mathrm{model}}(x,y)}
{\sum_{x,y} I_{\mathrm{model}}(x,y)}.
$$

The normalised PSF therefore describes the spatial distribution of the
source photons independently of the total source flux.

The observed image is modelled as

$$
I_{\mathrm{obs}}(x,y)
=
f\,P(x,y)+b+\epsilon(x,y),
$$

where:

- $f$ is the total source flux;
- $b$ is a spatially uniform background level;
- $\epsilon(x,y)$ represents measurement noise.

For a fixed PSF, the model is linear in $f$ and $b$. These two quantities can
therefore be determined analytically for each exposure using weighted linear
least squares,

$$
\sum_{x,y}
\frac{
\left[I_{\mathrm{obs}}(x,y)-fP(x,y)-b\right]^2
}{
\sigma^2(x,y)
},
$$

where $\sigma(x,y)$ is the per-pixel uncertainty from the calibrated
exposure's `ERR` array.

Analytically solving for flux and background reduces the dimensionality of
the optimisation problem. The solution is conditioned on the current PSF
model and is therefore recomputed as the forward model changes.

### Sub-pixel positioning

Each exposure also has a source position relative to the detector grid,
represented by a sub-pixel offset

$$
(\delta x,\delta y).
$$

Rather than translating the final image as a post-processing operation, this
offset is incorporated into the pupil-plane field as a phase tilt before
propagation. Under Fourier optics, this corresponds to a shift of the PSF in
the image plane.

This keeps source positioning inside the differentiable forward model and
ensures that the positional parameters are treated consistently with the
optical propagation.

### Detector response

After propagation and PSF normalisation, detector effects are represented as
modular pixel-level transformations. Depending on the instrument model,
these can include:

- geometric rotations;
- intra-pixel sensitivity variations;
- downsampling to the native detector resolution.

The resulting forward model maps the pupil-plane optical state to detector
intensity through a sequence of propagation, sampling, and detector-response
operations.

## PSF localisation and cutout extraction

The inference operates on fixed-size PSF cutouts extracted from calibrated
full-frame exposures. The localisation procedure is model-independent and
is designed for extended, defocused PSFs in crowded fields.

### Background and source mask

For each calibrated science image $I_{ij}$, the background level is estimated
using the median,

$$
m=\operatorname{median}(I_{ij}),
$$

and the dispersion is estimated from the median absolute deviation (MAD),

$$
\sigma
=
1.4826\,
\operatorname{median}\left(|I_{ij}-m|\right).
$$

Pixels containing significant source flux are identified using an adaptive
threshold. The usual threshold is approximately $5\sigma$, reduced to about
$3\sigma$ if there is insufficient source support.

### Coarse-to-fine localisation

An initial flux-weighted centroid is calculated from the full detector frame.
The centroid is then iteratively refined using successively smaller square
windows with side lengths

$$
L=1024,\quad512,\quad256\ {\rm pixels}.
$$

At each stage, the updated centroid defines the centre of the next window.
This coarse-to-fine procedure reduces sensitivity to neighbouring sources and
large-scale background structure while retaining the extended morphology of
the defocused PSF.

The final centroid is calculated from the masked flux,

$$
(i_0,j_0)
=
\frac{
\sum_{i,j}M_{ij}I_{ij}(i,j)
}{
\sum_{i,j}M_{ij}I_{ij}
},
$$

where $M_{ij}$ is the thresholded source mask.

### Cutout convention

Once the PSF centre has been determined, its coordinates are rounded to the
nearest detector pixel and a fixed $128\times128$ pixel cutout is extracted
around that location.

No additional sub-pixel centring is performed at this stage. This avoids
introducing a translation that could interact with the asymmetric aberration
pattern of the PSF.

If the extraction window reaches the detector edge, missing pixels are padded
with the previously estimated background value $m$.

The resulting cutouts therefore have a common geometry while retaining the
complete defocused PSF morphology required by the inference model.

## System parameterisation

The forward model separates parameters describing the underlying optical
state from exposure-dependent image-formation parameters.

### Global optical parameters

The pupil-plane phase, and hence the underlying OPD, is treated as a global
parameter shared across the exposures in an inference set. This assumes that
the telescope's underlying optical state does not vary significantly over
the time span represented by those observations.

The pupil amplitude can likewise be parameterised to allow small deviations
from the nominal aperture model. Such variations represent residual
throughput inhomogeneities and can be regularised to favour physically
plausible structure consistent with the segmented telescope aperture.

### Exposure-dependent parameters

Each exposure may have its own nuisance and configuration parameters,
including:

- total source flux $f$;
- background level $b$;
- sub-pixel source position $(\delta x,\delta y)$;
- defocus offset $\Delta z$.

This separation allows observations with different image-formation
conditions to constrain a common underlying wavefront while retaining
exposure-specific quantities where required.

## OPD and exposure association

The optical state used by the model can be associated with archived
observations through the telescope wavefront-sensing data.

A uniform Coordinated Universal Time (UTC) grid can be used to identify the
nearest OPD solution at a given observation time, using
`load_wss_opd_by_date`. OPD metadata can retain the observation ID, filename,
detector, and optical configuration, allowing the inferred wavefront state
to be correlated directly with the corresponding archived exposure.

Duplicate OPD realisations are removed, and OPD values outside the desired
epoch are excluded.

For the NIRCam weak-lens configuration considered here, candidate exposures
are selected from imaging observations using the F212N filter and the WLP8
and WLM8 pupil elements. Exposures are grouped by pupil configuration and
sorted by acquisition order. A representative weak-lens pair can then be
selected by acquisition date, providing a self-consistent, minimally
redundant pair of focus-diverse images for each sampled wavefront state.

## End-to-end workflow

The concepts above combine into the following forward-modelling and
inference workflow:

1. **Load and validate an exposure.**  
   Read the calibrated exposure and its associated metadata, including the
   detector configuration, filter, pupil state, and uncertainty information.

2. **Localise the PSF.**  
   Estimate the background and source mask, then locate the defocused PSF
   using the coarse-to-fine centroiding procedure.

3. **Extract the cutout.**  
   Round the final centre to the nearest detector pixel and extract the
   standard $128\times128$ pixel region, padding detector-edge regions with
   the estimated background where necessary.

4. **Construct the pupil-plane model.**  
   Combine the aperture amplitude and the inferred global phase/OPD to form
   the complex pupil-plane field.

5. **Apply exposure-specific parameters.**  
   Incorporate the relevant defocus state and sub-pixel source position for
   the exposure.

6. **Propagate the field.**  
   Apply the ABCD/LCT propagation, using the MFT implementation to map the
   pupil-plane sampling onto the detector-plane sampling.

7. **Form and normalise the PSF.**  
   Compute $|U|^2$ and normalise the result to unit flux.

8. **Apply detector response.**  
   Apply the relevant detector-level transformations, including any
   geometric, intra-pixel, and downsampling operations.

9. **Fit exposure-level flux and background.**  
   Given the current PSF, solve analytically for the source flux and
   background using the calibrated per-pixel uncertainties.

10. **Compare model and data.**  
    Evaluate the residuals or objective function between the forward-modelled
    image and the observed PSF cutout.

11. **Optimise or diagnose the optical parameters.**  
    Update the parameters describing the shared optical state and
    exposure-dependent quantities, or inspect the current model without
    optimisation.

12. **Inspect convergence and residuals.**  
    Examine the inferred parameters, model PSFs, and residual structure to
    diagnose whether the model adequately describes the observed exposures.

## Parameter keying

CAMINO stores model parameters in a way that distinguishes both their
physical meaning and the exposures to which they apply.

A parameter can therefore be associated with an individual exposure or
shared across multiple exposures. The `get_key` and `map_param` mechanisms
provide the interface for defining and accessing these relationships.

Conceptually, parameter keying separates two questions:

- **What physical quantity does this parameter represent?**
- **Which observations share the same value of that quantity?**

Global optical quantities such as the pupil-plane phase can therefore be
shared across a focus-diverse observation set, while quantities such as flux,
background, position, and residual defocus can remain exposure-specific.

This parameter-sharing structure is part of the inference model rather than
a post-processing convention: it determines which observations jointly
constrain each physical parameter.
