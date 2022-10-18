# Coordinate systems

## Ephemerides
_TODO_

## Rotations and attitude frames
### Trajectory centered frames
Nyx supports the RIC, VNC and RCN trajectory frames. These frames are right-handed and orthonormal. To retrieve the $3\times 3$ rotation matrix of these frames, call the `dcm_from_traj_frame` function on an `Orbit` structure.

Here is how Nyx computes these frames, where $\Omega$ refers to the [RAAN](/MathSpec/celestial/orbital_elements/#right-ascension-of-the-ascending-node-raan), $i$ to the [inclination](/MathSpec/celestial/orbital_elements/#inclination-inc), and $u$ to the [argument of latitude](/MathSpec/celestial/orbital_elements/#argument-of-latitude-aol). Moreover, $R_1$, $R_2$, $R_3$ respectively correspond to a rotation about the first, second and third axes.

#### RIC

$$
[C] = R_3(-\Omega)\times R_1(-i)\times R_3(-u)
$$

#### VNC
We start by computing the unit vectors of the velocity and orbit momentum.

$$\mathbf{\hat{v}} = \frac{\mathbf{v}}{v}$$

$$\mathbf{\hat{n}} = \frac{\mathbf{h}}{h}$$

Complete the orthonormal basis:

$$\mathbf{\hat{c}} = \mathbf{\hat{v}} \times \mathbf{\hat{n}}$$

$$
[C]= \left[\begin{matrix}
\hat{v}_x & \hat{n}_x & \hat{c}_x \\
\hat{v}_y & \hat{n}_y & \hat{c}_y \\
\hat{v}_z & \hat{n}_z & \hat{c}_z \\
\end{matrix}
\right]
$$

!!! note
    The VNC frame is called VNB in GMAT.

#### RCN
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

--8<-- "includes/Abbreviations.md"