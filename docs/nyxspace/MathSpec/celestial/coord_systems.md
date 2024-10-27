# Coordinate systems

## Rotations and attitude frames

### VNC Frame

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

Here are the two coordinate frame descriptions following the same style:

### RIC Frame

The **RIC frame** is a trajectory-centered coordinate system ideal for analyzing spacecraft motion relative to its position vector and orbital plane. It is particularly useful for relative navigation and rendezvous operations, where spacecraft position relative to a target is critical.

The RIC frame is right-handed and orthonormal, with axes that are mutually perpendicular and unit-length.

The transformation from the inertial frame to the RIC frame can be represented by a $3 \times 3$ rotation matrix $[C]$. This matrix is constructed using the components of the unit vectors:

1. Radial, $\mathbf{\hat{r}}$: aligned with the spacecraft's position vector in its current frame
2. In-track, $\mathbf{\hat{i}}$: perpendicular to both $\mathbf{\hat{r}}$ and $\mathbf{\hat{c}}$, completing the orthonormal basis
3. Cross-track, $\mathbf{\hat{c}}$: aligned with the orbital momentum, perpendicular to the orbital plane

$$
[C]= \left[\begin{matrix} 
\hat{r}_x & \hat{i}_x & \hat{c}_x \\ 
\hat{r}_y & \hat{i}_y & \hat{c}_y \\ 
\hat{r}_z & \hat{i}_z & \hat{c}_z \\ 
\end{matrix} \right]
$$

In practice, you can retrieve this rotation matrix by calling [`dcm_from_ric_to_inertial`](https://docs.rs/anise/latest/anise/astro/orbit/type.Orbit.html#method.dcm_from_ric_to_inertial) on an `Orbit` structure, or [`dcm3x3_from_ric_to_inertial`](https://docs.rs/anise/latest/anise/astro/orbit/type.Orbit.html#method.dcm3x3_from_ric_to_inertial) for the $3 \times 3$ DCM only.

### RCN Frame

The **RCN frame** is a trajectory-centered coordinate system ideal for analyzing spacecraft motion relative to its position vector and orbital plane. It is particularly useful for closed-loop guidance of finite maneuvers, like in the Q-Law or Ruggiero low-thrust guidance laws.

The RCN frame is right-handed and orthonormal, with axes that are mutually perpendicular and unit-length.

The transformation from the inertial frame to the RCN frame can be represented by a $3 \times 3$ rotation matrix $[C]$. This matrix is constructed using the components of the unit vectors:

1. Radial, $\mathbf{\hat{r}}$: aligned with the spacecraft's position vector in its current frame
2. Cross-track, $\mathbf{\hat{c}}$: perpendicular to both $\mathbf{\hat{r}}$ and $\mathbf{\hat{n}}$, completing the orthonormal basis
3. Normal, $\mathbf{\hat{n}}$: aligned with the orbital momentum, perpendicular to the orbital plane

$$
[C]= \left[\begin{matrix} 
\hat{r}_x & \hat{c}_x & \hat{n}_x \\ 
\hat{r}_y & \hat{c}_y & \hat{n}_y \\ 
\hat{r}_z & \hat{c}_z & \hat{n}_z \\ 
\end{matrix} \right]
$$

In practice, you can retrieve this rotation matrix by calling [`dcm_from_rcn_to_inertial`](https://docs.rs/anise/latest/anise/astro/orbit/type.Orbit.html#method.dcm_from_rcn_to_inertial) on an `Orbit` structure, or [`dcm3x3_from_rcn_to_inertial`](https://docs.rs/anise/latest/anise/astro/orbit/type.Orbit.html#method.dcm3x3_from_rcn_to_inertial) for the $3 \times 3$ DCM only.


!!! note
    The $6 \times 6$ DCM includes the time derivative of the rotation matrix. ANISE computes this time derivative by a finite difference of the $3 \times 3$ DCMs one millisecond before and after the current epoch. These permutations are handled via [`at_epoch`](https://docs.rs/anise/latest/anise/astro/orbit/type.Orbit.html#method.at_epoch), a two-body approximation of the orbital state using its mean anomaly.

## Ephemerides

Nyx uses the NASA/JPL Developmental Ephemerides version 440 (DE440) by default for all ephemeris handling. The implementation is multi-threaded via ANISE, a modern rewrite of NAIF's SPICE.

Learn all about [ANISE here](../../../anise/index.md).


--8<-- "includes/Abbreviations.md"