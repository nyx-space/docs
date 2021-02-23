# Gravity

All propagation in Nyx is subjected to two-body gravity, with an option to add on other gravity forces from other objects as needed. The GM parameters for all celestial bodies are those used by NASA JPL. Nyx stores these gravitational parameters in the `XB` file provided with Nyx. In the future, Nyx will used another file format, designed to be flight-software ready, faster, and totally open-source (note that XBs are already 6-8 times faster than SPICE BSP files).

This model will propagate the state in Cartesian form, as it does not suffer from singularities.

## Two-body
Each orbit or spacecraft is represented with respect to a frame, a copy of which is stored with said object. The equations of motion will use the GM parameter of that frame for all computations.

Provided an input vector of position and velocity, the equations of motion will compute the time derivative as follows. The vectors $\mathbf{r}$ and $\mathbf{v}$ are respectively the position and velocity of the spacecraft. The $t$ subscript refers to the current time and $t'$ the next time in the direction of the propagator (i.e. $t>t^\prime$ if propagating forward and $t< t^\prime$ when propagating backward).

$$\dot{\mathbf{r}}_{t'} = \mathbf{v}_t$$

$$\dot{\mathbf{v}}_{t'} = -\mu\frac{\mathbf{r}_t}{|\mathbf{r}_t|^3}$$

!!! important
    If you want to specify a different GM for a given frame, it is important to modify the frame prior to initializing a spacecraft state with that frame. A shortcut to using the GMAT GMs is to initialize the `Cosm` as `Cosm::de438_gmat()` instead of `Cosm::de438()`.

??? check "Validation"
    Validation is true.

## Multibody
This computation happens in the `PointMasses` models. It is the generalization of the equation from the previous "two-body" section.

This model does not affect the velocity components of the time derivative, only the acceleration of the next propagator step, noted as $\dot{\mathbf{v}}_{t'}$. As such it is implemented as an `AccelModel`.

In the following, $\mathbf{r_{ij}}$ is the position of the $i$-th celestial body as seen from the integration frame at the integration time. The $\mathbf{r_{j}}$ vector is the position of the spacecraft as seen from the $i$-th celestial body.

$$\mathbf{r_{j}} = \mathbf{r}_t - \mathbf{r_{ij}}$$

$$\dot{\mathbf{v}}_{t'} = \dot{\mathbf{v}}_{t'} - \mu_i \left( \frac{\mathbf{r_j}}{|\mathbf{r_j}|^3} - \frac{\mathbf{r_{ij}}}{|\mathbf{r_{ij}}|^3} \right)$$


--8<-- "includes/Abbreviations.md"