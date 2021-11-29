# Targeting
Nyx provides a Newton-Raphson differential corrector as a targeting method, validated against GMAT. Upon request by the user Nyx will use the hyperdual formulation of the partial derivatives, as detailed in "AAS-21-715 Hyperdual Numbers for Arbitrary Orbit Targeting", Rabotin 2021 (cf. the [paper](/assets/pdf/aas-21-715/AAS21-715-paper.pdf) and [presentation](/assets/pdf/aas-21-715/AAS21-715-presentation.pdf)). Otherwise, the method will use finite differencing. [This section](#newton-raphson-differential-corrector) provides a refresher on the Newton Raphson differential corrector.

**TL;DR:** Nyx implements literally the same algorithm as GMAT 2021a. I spent a considerable amount of time reading and comparing the GMAT code with the targeting code of Nyx.

!!! info "Options"
    1. Supported variables cf below
    1. Max iterations
    1. Min max values, step size, etc.
    1. Multiplication and additive factors

!!! warning "Limitations"
    1. Only inertial frame and VNC frame are supported for targeting using finite differencing. Hyperdual targeting only works in the same frame as the propagation.
    1. For now, targeting can only find _instantaneous corrections_ (e.g. impulsive maneuvers or position changes). Work is in progress to implement Jacob William's algorithm to convert an impulsive maneuver into a finite burn maneuver (as done in NASA Copernicus).
    1. When using the hyperdual formulation, the eigenvalues of the state transition matrix are used to determine whether this is a stable linearization or not. If not, a warning will be shown. Unless the trajectory is quite non-linear between the correction epoch and the objectives epoch (i.e. the epoch at which the state correction is done and the epoch at which the objectives are to be matched), then you can probably ignore that warning. If you're unsure, call the [`apply`](https://docs.rs/nyx-space/latest/nyx_space/md/targeter/struct.Targeter.html#method.apply) function of the target with the solution to make sure that the solution is indeed correct.

## Configuration
### Objectives

Targeter objectives ([API documentation](https://docs.rs/nyx-space/latest/nyx_space/md/targeter/struct.Objective.html)) are build from the following, all defined in the same units as the parameter:

 + a state parameter to be targeted;
 + a desired value;
 + a precision of the targeting;
 + a tolerance
 + an additive factor (defaults to `0.0`); and
 + a multiplicative factor (default to `1.0`).

The following table summarizes all of the [state parameters](https://docs.rs/nyx-space/latest/nyx_space/md/enum.StateParameter.html) which can be targeted. These are the same as the parameters which can be searched in a trajectory.

!!! info "Default precision"
    + Eccentricity: 1e-5
    + Non-anomaly angles (AoL, declination, etc.): 1e-1 degrees
    + Anomaly angles (true anomaly, mean anomaly, slant angle, etc.): 1e-3 degrees
    + Distances (SMA, BdotT, etc.): 1e-3 kilometers
    + Velocities ($c_3$, vmag, etc.): 1e-3 kilometers per second
    + Specific energy: 1e-3
    + Fuel mass: 1e-3 kg
    + Orbital period: 1e-1 seconds

    Of course, one can change the precision of the targeting when create the objective with the `Objective::within_tolerance` builder.

Parameter | Comments
--|--
AoL | Argument of Latitude (deg)
AoP | Argument of Periapse (deg)
Apoapsis | Apoapsis, shortcut for TA == 180.0
ApoapsisRadius | Radius of apoapsis (km)
BdotR | B-Plane B⋅R
BdotT | B-Plane B⋅T
BLTOF | B-Plane LTOF
C3 | C_3 in (km/s)^2
Declination | Declination (deg)
EccentricAnomaly | Eccentric anomaly (deg)
Eccentricity | Eccentricity (no unit)
Energy | Specific energy
FlightPathAngle | Flight path angle (deg)
GeodeticHeight | Geodetic height (km)
GeodeticLatitude | Geodetic latitude (deg)
GeodeticLongitude | Geodetic longitude (deg)
Hmag | Orbital momentum
HX | X component of the orbital momentum vector
HY | Y component of the orbital momentum vector
HZ | Z component of the orbital momentum vector
HyperbolicAnomaly | Hyperbolic anomaly (deg), only valid for hyperbolic orbits
Inclination | Inclination (deg)
MeanAnomaly | Mean anomaly (deg)
Periapsis | Periapsis, shortcut for TA == 0.0
PeriapsisRadius | Radius of periapse (km)
Period | Orbital period (s)
RightAscension | Right ascension (deg)
RAAN | Right ascension of the ascending node (deg)
Rmag | Norm of the radius vector
SemiParameter | Semi parameter (km)
SlantAngle | Computes the slant angle by returning the arccos of the dot product between state's radius vector and the provided vector coordinates (x,y,z in km). The vector will be normalized if needed.
SMA | Semi major axis (km)
SemiMinorAxis | Semi minor axis (km)
TrueAnomaly | True anomaly
TrueLongitude | True longitude
VelocityDeclination | Velocity declination (deg)
Vmag | Norm of the velocity vector (km/s)
X | X component of the radius (km)
Y | Y component of the radius (km)
Z | Z component of the radius (km)
VX | X component of the velocity (km/s)
VY | Y component of the velocity (km/s)
VZ | Z component of the velocity (km/s)

## Validation
The twelve GMAT scenarios used in this validation can be found [here](https://gitlab.com/nyx-space/nyx/-/tree/master/tests/GMAT_scripts/targeting). Validation was done on GMAT R2021a.

You can run these validation cases with `RUST_LOG=info RUST_BACKTRACE=1 cargo test $TESTCASE --release -- --nocapture`, e.g. `RUST_LOG=info RUST_BACKTRACE=1 cargo test tgt_sma_ecc --release -- --nocapture` for the SMA and ECC targeting scenario.

If the solution is **bolded**, it means that Nyx found a solution that is better than GMAT, i.e. uses less $\Delta$v.

Scenario | Test case  | Solution | Absolute diff with GMAT | Targeting error | Clock time
--|---|---|---|---|--
Mnvr to achieve SMA 8100km, ECC 0.4 |  `tgt_sma_ecc` | **3068.966 m/s** | 47.110530 m/s | $\Delta$sma < 1m; $\Delta$ecc < 1e-5 | 0.03 s
Mnvr to achieve SMA 8100km, ECC 0.4 (hyperdual form) |  `tgt_hd_sma_ecc` | **3093.975 m/s** | 22.101972 m/s | $\Delta$sma < 1m; $\Delta$ecc < 1e-5 | 0.01 s
Mnvr to achieve $C_3$ -5.0, $\delta$ 5.0 deg |  `tgt_c3_decl` | **2383.776 m/s** | 1.928149 m/s | $\Delta$c3 = 0.011; $\Delta$δ = 0.001 | 0.04 s
VNC Mnvr to achieve $C_3$ -5.0, $\delta$ 5.0 deg |  `tgt_vnc_c3_decl` | 2386.856 m/s | 1.151360 m/s | $\Delta$c3 = 0.005; $\Delta$δ = 0.007 | 0.04 s
VNC Mnvr to achieve SMA 8100km, ECC 0.4 |  `tgt_vnc_sma_ecc` | **3115.247 m/s** | 0.829603 m/s | $\Delta$sma < 1m; $\Delta$ecc < 1e-5 | 0.03 s
Mnvr to achieve AoP 65.0 from periapse |  `tgt_aop_from_peri` | **121.979 m/s** | 0.000001 m/s | $\Delta$aop = 0.01 deg | 0.02 s
Mnvr to achieve AoP 65.0 from apoapse |  `tgt_aop_from_apo` | **117.723 m/s** | 0.000001 m/s | $\Delta$aop = 0.003 deg | 0.01 s
Mnvr to achieve ECC 0.4 from apoapse |  `tgt_ecc_from_apo` | **772.148 m/s** | 0.000013 m/s |  $\Delta$ecc < 1e-5 | 0.01 s
Mnvr to achieve ECC 0.4 from periapse |  `tgt_ecc_from_peri` | 692.675 m/s | 0.000194 m/s |  $\Delta$ecc < 1e-5 | 0.05 s
Mnvr to achieve RAAN 65.0 from apoapse |  `tgt_raan_from_apo` | 304.300 m/s | 0.852967 m/s |  $\Delta$raan = 0.08 | 0.01 s
Mnvr to achieve RAAN 65.0 from periapse |  `tgt_raan_from_peri` | 456.552 m/s | 5.446556 m/s |  $\Delta$raan = 0.0004 | 0.02 s
Mnvr to achieve SMA 8100km from periapse |  `tgt_sma_from_peri` | **35.504 m/s** | 0.000103 m/s | $\Delta$sma < 1m | 0.02 s
Mnvr to achieve SMA 8100km from apoapse |  `tgt_sma_from_apo` | **53.120 m/s** | < 1e-5 m/s | $\Delta$sma < 1m | 0.02 s
Mnvr to achieve SMA 8100km from periapse (hyperdual form) |  `tgt_hd_sma_from_peri` | 35.505 m/s | 0.000825 m/s | $\Delta$sma < 1m | 0.01 s
Mnvr to achieve Lunar $B_T$ 5022.265km $B_R$ 13135.798km for Earth gravity assist |  `tgt_b_plane_earth_gravity_assist_with` | 319.557 m/s | 0.459335 m/s | $\Delta B_T$ < 1m $\Delta B_R$ < 1m | 0.01 s

## Newton-Raphson differential corrector 
A Newton-Raphson differential corrector applies the Newton-Raphson root finding algorithm to trajectory design to satisfy some objectives ($\mathbf \Gamma^*$) provided some control variables ($\mathbf U$). The control variables must be independent of each other while the objectives must vary with a variation in the controls. The algorithm will iteratively compute small corrections to the control vector until the objectives are met with sufficient precision, typically defined by the user.

Let $\mathbf \Gamma^*$ be the vector of desired objectives at time $t_f$ and $\mathbf \Gamma_f$ be the achieved objectives at time $t_f$, and let $\mathbf U_i$ be the control vector at time $t_i$, where $t_f\geq t_i$. Given some control vector $\mathbf U_i$ applied at time $t_i$, the trajectory is propagated until time $t_f$ where the objectives $\mathbf \Gamma_f$ are computed. Then, the objective error vector is computed, as in the equation below. Note that at the first iteration, the control vector is typically provided by the user, but a vector of zeros also works. Also note that, most commonly for impulsive maneuver design, the control vector is simply a change in the velocity vector, i.e. $\mathbf{U_i} = \Delta \mathbf v_i$.

\begin{equation}
\label{err_vec}
\mathbf{\Delta \Gamma} = \mathbf \Gamma_f - \mathbf \Gamma^*
\end{equation}

This error vector, $\mathbf{\Delta \Gamma}$, must be mapped back to the controls at time $t_i$. This is done by computing the Jacobian of the controls with respect to the objectives, sometimes called the sensitivity matrix. The equation below shows a Jacobian with $n$ control variables and $m$ objectives. An easy method to remember how to organize the Jacobian is that the component of the numerator remains fixed navigating left to right (like an arrow pointing right) and the component of the denominator remains fixed going from top to bottom (like an arrow pointing downward).

\begin{equation}
\label{jac_obj}
\mathbf J = \frac{\partial \mathbf \Gamma_f}{\partial \mathbf U_i} = \begin{bmatrix}
    \frac{\partial \Gamma_{f_0}}{\partial U_{i_0}} &\dots &\frac{\partial \Gamma_{f_0}}{\partial U_{i_n}} \\
    \vdots & \ddots & \vdots\\
    \frac{\partial \Gamma_{f_m}}{\partial U_{i_0}} &\dots &\frac{\partial \Gamma_{f_m}}{\partial U_{i_n}} \\
\end{bmatrix}
\end{equation}



The following equation shows how the error in objectives and the inverted Jacobian is used to update the controls variables for the next iteration of the Newton-Raphson algorithm.

\begin{equation}
\label{jac_map}
\begin{aligned}
\mathbf{\delta U_{i+1}} = \left(\frac{\partial \mathbf \Gamma_f}{\partial \mathbf U_i}\right)^{-1} \cdot \mathbf{\Delta \Gamma} &= \frac{\partial \mathbf U_i}{\partial \mathbf \Gamma_f} \cdot \left( \mathbf \Gamma_f - \mathbf \Gamma^* \right) \\
\mathbf{U_{i+1}} &= \mathbf{U_i} + \mathbf{\delta U_{i+1}}
\end{aligned}
\end{equation}

Note that if the number of control variables and the number of objectives do not match, a Moore-Penrose pseudo-inverse must be used. If there are more control variables than objectives, the following equation applies, otherwise use the equation just after that.

\begin{equation}
\label{pseudo_inv0}
\mathbf{J}^{-1} \simeq \mathbf{J}^T\cdot\left(\mathbf{J}\cdot \mathbf{J}^T\right)^{-1}
\end{equation}

\begin{equation}
\label{pseudo_inv1}
\mathbf{J}^{-1} \simeq \left(\mathbf{J}^T\cdot \mathbf{J}\right)^{-1}\cdot\mathbf{J}^T
\end{equation}

### Applying hyperdual numbers to targeting
As seen previously, hyperdual numbers allow machine-precision computation of the state transition matrix. Moreover, they can also be used to compute the partial derivatives of any orbital element with respect to the Cartesian orbit representation. Therefore, we can rewrite each component of the Jacobian with those intermediate steps as is done in the equation below, where $\mathbf X_i$ is the Cartesian state at the time $t_i$ when the control vector $\mathbf U_i$ is applied and $\mathbf X_f$ is the Cartesian state at the time $t_f$ when the objectives $\mathbf \Gamma_f$ are computed. It is important to note that the following equation is used to replace each component of the Jacobian one at a time.

\begin{equation}
\label{jac_dual}
\frac{\partial \mathbf \Gamma_f}{\partial \mathbf U_i} = \frac{\partial \mathbf \Gamma_f}{\partial \mathbf X_i} \cdot \frac{\partial \mathbf X_i}{\partial \mathbf U_i} = \frac{\partial \mathbf \Gamma_f}{\partial \mathbf X_f} \cdot \frac{\partial \mathbf X_f}{\partial \mathbf X_i} \cdot \frac{\partial \mathbf X_i}{\partial \mathbf U_i} = \frac{\partial \mathbf \Gamma_f}{\partial \mathbf X_f} \cdot  \Phi(t_i, t_f) \cdot \frac{\partial \mathbf X_i}{\partial \mathbf U_i}
\end{equation}

For example, the following equation shows how to change the orbital energy $\xi$ by a change in velocity in the same frame as the state transition matrix, where $V_{i_x}$ is the X component of the velocity vector at time $t_i$. 

\begin{equation}
\label{jac_energy}
\frac{\partial \mathbf \xi_f}{\partial V_{i_x}} = \frac{\partial \mathbf \xi_f}{\partial \mathbf X_f} \cdot \frac{\partial \mathbf X_f}{\partial \mathbf X_i} \cdot \frac{\partial \mathbf X_i}{\partial V_{i_x}}
\end{equation}

The following equation shows how this formulation would replace the full Jacobian where the objective is a specific orbital energy and the control vector is simply all three components of the velocity in the frame of the STM. One will note that $\frac{\partial \mathbf X_f}{\partial \mathbf X_i} \cdot \frac{\partial \mathbf X_i}{\partial V_{i_x}}$ is simply the fourth column of the state transition matrix when the states are represented as Cartesian vectors. Therefore, in the next equation the simplification to $\frac{\partial \mathbf X_f}{\partial V_{i_x}}$ is used.

\begin{equation}
\label{jac_dual_full}
\frac{\partial \xi_f}{\partial \mathbf V_i} = \begin{bmatrix}
    \frac{\partial \xi_f}{\partial \mathbf X_f} \cdot \frac{\partial \mathbf X_f}{\partial V_{i_x}} & \frac{\partial \xi_f}{\partial \mathbf X_f} \cdot \frac{\partial \mathbf X_f}{\partial V_{i_y}} & \frac{\partial \xi_f}{\partial \mathbf X_f} \cdot \frac{\partial \mathbf X_f}{\partial V_{i_z}}
\end{bmatrix}
\end{equation}

Continuing with this example, one would perform the pseudoinverse as detailed above. Applying a Newton-Raphson differential correction, a single propagation would be performed from $t_i$ to $t_f$, time at which the energy error would be computed. The iteration is described below.

\begin{equation}
\label{jac_map_dual}
\mathbf{\delta V_{i+1}} = \left(\frac{\partial \xi_f}{\partial \mathbf V_i}\right)^{-1} \cdot \mathbf{\Delta \xi} \quad\quad
\mathbf{V_{i+1}} = \mathbf{V_i} + \mathbf{\delta V_{i+1}}
\end{equation}
