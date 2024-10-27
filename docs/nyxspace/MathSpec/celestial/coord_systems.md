# Coordinate systems

## Ephemerides

Nyx uses the SPICE developmental ephemerides (DE440) for all ephemeris handling via ANISE, a modern rewrite of NAIF's SPICE.

Learn all about [ANISE here](../../../anise/).

## Rotations and attitude frames

### VNC

The **VNC frame** is a trajectory-centered coordinate system ideal for analyzing spacecraft motion relative to its velocity vector and orbital plane. It is particularly useful for planning maneuvers, such as ensuring a spacecraft burns in the anti-velocity direction during a finite burn.

The VNC frame is right-handed and orthonormal, with axes that are mutually perpendicular and unit-length. In some contexts, such as GMAT, it is also referred to as the VNB frame.

The transformation from the inertial frame to the VNC frame can be represented by a $3 \times 3$ rotation matrix $[C]$. This matrix is constructed using the components of the unit vectors:

1. Velocity, $\mathbf{\hat{v}}$: aligned with the spacecraft's velocity vector in its current frame
2. Normal, $\mathbf{\hat{n}}$: aligned with the orbital momentum, and perpendicular to the orbital plane.
3. Cross-track, $\mathbf{\hat{c}}$: completes the orthonormal basis, perpendicular to both $\mathbf{\hat{v}}$ and $\mathbf{\hat{n}}$.

$$
[C]= \left[\begin{matrix} 
\hat{v}_x & \hat{n}_x & \hat{c}_x \\ 
\hat{v}_y & \hat{n}_y & \hat{c}_y \\ 
\hat{v}_z & \hat{n}_z & \hat{c}_z \\ 
\end{matrix} \right]
$$

In practice, you can retrieve this rotation matrix by calling [`dcm_from_vnc_to_inertial`](https://docs.rs/anise/latest/anise/astro/orbit/type.Orbit.html#method.dcm_from_vnc_to_inertial) on an `Orbit` structure, or [`dcm3x3_from_vnc_to_inertial`](https://docs.rs/anise/latest/anise/astro/orbit/type.Orbit.html#method.dcm3x3_from_vnc_to_inertial) for the $3 \times 3$ DCM only.

### RIC

$$
[C] = R_3(-\Omega)\times R_1(-i)\times R_3(-u)
$$


### RCN
We start by computing the unit vectors of the radius and orbit momentum.

$$\mathbf{\hat{r}} = \frac{\mathbf{r}}{r}$$

$$\mathbf{\hat{n}} = \frac{\mathbf{h}}{h}$$

Complete the orthonormal basis:

$$\mathbf{\hat{c}} = \mathbf{\hat{r}} \times \mathbf{\hat{n}}$$

$$
[C]= \left[\begin{matrix}
\hat{r}_x & \hat{c}_x & \hat{n}_x \\
\hat{r}_y & \hat{c}_y & \hat{n}_y \\
\hat{r}_z & \hat{c}_z & \hat{n}_z \\
\end{matrix}
\right]
$$

#### Example

```
let dcm_vnc2inertial = orbit.dcm_from_traj_frame(Frame::VNC)?;
let vector_inertial = dcm_vnc2inertial * vector_vnc;
```

!!! note
    The $6 \times 6$ DCM includes the time derivative of the rotation matrix. ANISE computes this time derivative by a finite difference of the $3 \times 3$ DCMs one millisecond before and after the current epoch.

--8<-- "includes/Abbreviations.md"