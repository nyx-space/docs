# Orbital elements

Ths computation of orbital element is either a clone of the NASA GMAT C++ code or of the Vallado algorithms (4-th edition). The [validation for the computation](#validation) of all elements is listed at the bottom of this page, apart for the B-Plane validation, which at the bottom of the B-Plane section [here](#b-plane-b_plane).

API documentation available [here](https://docs.rs/nyx-space/*/nyx_space/celestia/struct.Orbit.html).

## Storage
Nyx stores all of the orbit information as a Cartesian state (units of kilometer and kilometer per second) because it is a non-singular representation of an orbit. Furthermore, all propagation using `OrbitalDynamics`, its acceleration models, and its force models is in Cartesian form for the same reason.

## Initialization methods

An orbit may be initialized from its Cartesian position and velocity components (from 64 bit floating point values or from a vector of that type), from Keplerian orbital elements where the phasing parameter is the true anomaly, or from its geodesic elements (latitude, longitude and height compared to the reference ellipsoid of the frame[^1]). The initializer also includes an epoch (cf. [Time MathSpec](/MathSpec/time/)) and a frame (cf. [Frame MathSpec](/MathSpec/celestial/coord_systems/)).

As discussed above, the state is stored in Cartesian form. Hence, initializing in Keplerian form will trigger the conversion of the state from Keplerian orbital element into Cartesian orbital elements. This method _does support_ hyperbolic, circular inclined, circular equatorial, and the common elliptical orbits. The eccentricity tolerance is set to $1e^{-11}$, i.e. if the eccentricity is below that number, then the orbit is considered circular and the appropriate conversions to Cartesian will be triggered. The algorithm implementation is available [here](https://docs.rs/nyx-space/*/nyx_space/celestia/struct.Orbit.html#method.keplerian), but to convince yourself that it works, probably best to check out the [validation](#validation) below.

Vallado's geodetic to Cartesian initializer is also implemented allowing the initialization of a state known only by its longitude, laltitude and height above the reference ellipsoid of that rocky celestial object.

Finally, one may also initialize a new orbit from a previous orbit via `with_sma`, `with_ecc`, `with_inc`, `with_raan`, `with_aop`, `with_ta`: these copy a previous orbit but change the requested Keplerian orbital element to the requested value. Analogous methods exist with `add` instead of `with` which will add the provided value to the current Keplerian element value. For example `some_orbit.add_inc(-10.0)` will create a new orbit where the inclination 10 degrees lower than `some_orbit`'s inclination.

## Accessor methods
In the following, the position coordinates are referred to as $x,y,z$ and the velocity components as $v_x,v_y,v_z$. More generally, $\gamma_x$, $\gamma_y$, $\gamma_z$ respectively refer to the x, y, and z component of the $\gamma$ vector.

### Argument of latitude (`aol`)
The true longitude is an alternate phasing element. Nyx will return this angle between 0 and 360 degrees.

1. If the eccentricity is below the eccentricity tolerance:

    $$ u = \lambda - \Omega $$

2. Else:

    $$ u = \omega + \nu $$


### Argument of periapsis (`aop`)
The argument of periapsis is computed as follows and is returned in degrees:

1. Rotate the momentum vector:

    \begin{equation}
    \mathbf n = \begin{bmatrix}
        0 \\
        0 \\
        1 \\
    \end{bmatrix} \times \mathbf h
    \end{equation}

2. Compute the AoP:

    $$ \omega = \cos ^{-1} \left(\frac{\mathbf n \cdot \mathbf e}{|\mathbf n| \times e}\right) $$

3. Perform a quadrant check: if $e_z$ is less then zero, return the AoP as $2\pi - \omega$ instead.

### B-plane (`b_plane`)
This function will return an error (`NyxError::NotHyperbolic`) if called on a non-hyperbolic orbit. In other words, to compute the B-plane of an orbit, convert it to the desired planetary inertial frame first.

!!! warning
    Nyx will _not_ check whether the frame of the orbit is hyperbolic. This is up to the user.

The algorithm is identical to that outlined in the GMAT MathSpec, section 3.2.7, paraphrased here.

The $\mathbf B$ vector is defined from the center of mass of the desired central body to the incoming hyperbolic asymptote: B is perpendicular to the incoming asymptote.
We define $\mathbf {\hat S}$ as a unit vector in the direction of the incoming asymptot and $\mathbf{\hat T}$ as the unit vector perpendicular to $\mathbf {\hat S}$ such that $\mathbf {\hat T}$ lies in the $xy$ plane of the frame in which is represented this orbit. $\mathbf {\hat R}$ is a unit vector perpendicular to both $\mathbf {\hat T}$ and $\mathbf {\hat S}$.

We define $B_T=\mathbf B \cdot \mathbf {\hat T}$ and $B_R=\mathbf B \cdot \mathbf {\hat R}$. The method was adopted from work by Kizner

1. Compute the eccentricity unit vector, the momentum unit vector, and their cross product:

    $$ \mathbf{\hat e} = \frac {\mathbf{e}}{e}
    \quad\quad \mathbf{\hat h} = \frac {\mathbf{h}}{h} \quad\quad \mathbf{\hat n} = \mathbf{\hat h}\times \mathbf{\hat e}$$

2. Compute the $\mathbf{\hat S}$, $\mathbf B$, $\mathbf{\hat T}$ and $\mathbf{\hat R}$ vectors, where $b$ is the [semi-minor axis](#semi-minor-axis-semi_minor_axis).


    $$ \mathbf{\hat S} = \frac {\mathbf{\hat e}} {e} + \sqrt{1 - \left(\frac {1} {e}\right)^2} \mathbf{\hat n}$$

    $$ \mathbf{\hat T} = \frac {\mathbf{\hat S} \times \mathbf{\hat k}} { || \mathbf{\hat S} \times \mathbf{\hat k} ||} $$
    
    $$ \mathbf{B} = b \left(\sqrt{1- \left(\frac 1 e \right)^2 \mathbf{\hat e}} - \frac 1 e \mathbf{\hat n} \right)$$

    $$ \mathbf{\hat R} = \mathbf{\hat S} \times \mathbf{\hat T}$$

3. Compute the B plane parameters

    $$B_T=\mathbf B \cdot \mathbf {\hat T} \quad\quad B_R=\mathbf B \cdot \mathbf {\hat R}$$

??? check "Validation"
    The validation was done by following the `Ex_LunarTransfer.script` GMAT example script, from which we've added the export of the B Plane parameters (B dot R, B dot T, B Vector Mag, B Vector Angle and C3).
    The validation test is called `val_b_plane_gmat`. It propagates the initial orbit of the script until Earth periapse and generates the trajectory.
    **Note:** in that example, GMAT will use all of the force models available (high fidelity drag, SRP, all celestial objects) but we only use the point masses of Earth, Moon, Sun and Jupiter. This leads to a small error (less than 500 meters) for the B Plane. For each of the nine exported states (from some Earth apoapse to the Earth periapse), we check that the B plane and C3 parameters computed by Nyx are within 500 meters of error (due to force model differences) for positions and less than 0.1 millidegrees for B vector angle.
    
    ```
    cargo test val_b_plane_gmat --release -- --nocapture
    ```

#### B Vector Angle (`angle`)
Returns the angle of the B plane, in degrees between $[0;360]$.

$$ \theta = \tan^{-1} \frac {B_R}{B_T} $$

#### B Vector magnitude (`mag`)
Returns the magnitude of the B vector in kilometers.

$$||\mathbf B|| = \sqrt{B_T^2 + B_R^2}$$

#### B Plane frame from inertial frame (`inertial_to_bplane`)
Returns the DCM to convert to this B-Plane frame from the inertial frame (with identical central bodies).

\begin{equation}
\mathbf{C} = \begin{bmatrix}
    \hat S_x &\hat S_y &\hat S_z \\
    \hat T_x &\hat T_y &\hat T_z \\
    \hat R_x &\hat R_y &\hat R_z \\
\end{bmatrix}
\end{equation}

#### Linearized Time of Flight (`ltof`)
Returns a `Duration` object corresponding to the linearized time of flight as computed in "Closed loop terminal guidance navigation for a kinetic impactor spacecraft.", Bhaskaran & Kennedy (2014). Acta Astronautica, 103, 322–332 (doi:10.1016/j.actaastro.2014.02.024).[^2]

$$L_{TOF}=\frac{\mathbf B \cdot \mathbf {\hat S}} {||\mathbf v||}$$

### C3
Computes the $C_3$ of this orbit:

$$ C_3= -\frac \mu a$$

### Declination (`declination`)
Returned in degrees between $[-180;180]$.

$$ \delta = \sin^{-1} \frac z {||\mathbf r||} $$

### Distance between two orbits `distance_to`
The distance in kilometers between two states, computed as follows (where $r$ and $r'$ respectively refer to the `this` state and the `other` state).

$$\sqrt {(r_x-r^\prime_x)^2+(r_y-r^\prime_y)^2+(r_z-r^\prime_z)^2} $$

### Eccentricity (`evec`, `ecc`)
Respectively, the eccentricity vector and its magnitude (i.e. the eccentricity)

$$ \mathbf e = \left(||\mathbf v||^2 - \frac{\mu}{||\mathbf r||}\right) \cdot \mathbf r - \frac{\mathbf r \cdot \mathbf v}{\mu}\cdot \mathbf v$$

For the rest of the MathSpec, let $e = ||\mathbf e||$.

### Eccentric anomaly (`ea`)
Nyx returns this parameter ($E$) in degrees.

1. Compute the sine of the eccentric anomaly

    $$\sin E = \frac{\sqrt{1 - e^2} \sin\nu} {1 + e \cos \nu}$$

2. Compute the cosine of the eccentric anomaly

    $$\cos E = \frac{e + \cos\nu} {1 + e \cos \nu}$$

3. Returns the quadrant-checked tangent of those angles (`atan2`), converted to degrees.

!!! note
    This is a conversion from GMAT's `StateConversionUtil::TrueToEccentricAnomaly`.

### Flight path angle (`fpa`)

1. Compute the sine of the FPA, $f$:

    $$ \sin f = \frac{e \sin \nu} {\sqrt{1 + 2e\cos\nu + e^2}} $$

2. Compute the cosine of the FPA, $f$:

    $$ \cos f = \frac{1 + e \cos \nu} {\sqrt{1 + 2e\cos\nu + e^2}} $$

3. Returns the quadrant-checked tangent of those angles (`atan2`), converted to degrees.

### Geodetic height (`geodetic_height`)
The parameter is returned in kilometers.
This is computed using the Vallado approach, Algorithm 12 page 172 in the 4-th edition. This accounts for the correction when near the poles. It's a notch complex to write up, so please refer to the [code](https://docs.rs/nyx-space/*/nyx_space/celestia/struct.Orbit.html#method.geodetic_height) or Vallado for implementation details. As you'll note from the Validation section, it has been validated against Vallado examples.

!!! warning
    This function requires that the orbit already be in a body fixed frame. Nyx will _not_ check that.

### Geodetic latitude (`geodetic_latitude`)
The parameter is returned in degrees between $[-180;180]$.
This is computed using the Vallado iterative approach, Algorithm 12 page 172 in the 4-th edition. It accounts for the flattening of the ellipsoid and its semi-major axis. It's a notch complex to write up, so please refer to the [code](https://docs.rs/nyx-space/*/nyx_space/celestia/struct.Orbit.html#method.geodetic_latitude) or Vallado for implementation details. As you'll note from the Validation section, it has been validated against Vallado examples.

!!! warning
    This function requires that the orbit already be in a body fixed frame. Nyx will _not_ check that.

### Geodetic longitude (`geodetic_longitude`)
This is computed using G. Xu and Y. Xu, "GPS", DOI 10.1007/978-3-662-50367-6_2, 2016, but the validation against the Vallado examples proves to be correct. The following uses the quadrant-checked arctan (`atan2`). The angle is returned in degrees and is between $[0;360]$.

$$ \lambda = \tan^{-1} \frac{y}{x} $$

!!! warning
    This function requires that the orbit already be in a body fixed frame. Nyx will _not_ check that.

### Hyperbolic anomaly (`hyperbolic_anomaly`)
Computes the hyperbolic anomaly for this hyperbolic orbit in degrees between $[0;360]$, or will return an error (`NyxError::NotHyperbolic`) if the orbit is not hyperbolic.

$$ H = \sinh^{-1}\left( \frac{\sin(\nu) \sqrt{e^2 -1}} {1 + e\cos\nu} \right)$$

### Inclination (`inc`)
The inclination of this orbit, returned in degrees.

$$ i = \cos^{-1} \left(\frac {h_z}{|\mathbf h|}\right)$$

### Mean anomaly (`ma`)

1. If the eccentricity is below 1, the mean anomaly $M$ is computed as follows

    $$ M = E-e\sin E $$

2. If the eccentricity is strictly above 1:

    $$ M = \sinh^{-1} \frac {\sin\nu \sqrt{e^2 - 1} }{1 + e \cos\nu} $$

!!! note
    This is a conversion from GMAT's `StateConversionUtil::TrueToMeanAnomaly`. This function _does support_ the mean anomaly for hyperbolic orbits (but not for parabolic orbits).

### Momentum vector (`hvec`, `hmag`, `hx`, `hy`, `hz`)
The momentum vector, its magnitude, and its X, Y and Z components.

$$\mathbf{h} = \mathbf r \times \mathbf v$$

### Orbital energy (`energy`)
The orbit's energy:

$$ \xi = \frac {||\mathbf v||^2}{2} - \frac{\mu}{\mathbf r} $$

### Orbital period (`period`)
The orbital period, returned as high-precision `Duration` structure:

$$\mathcal{P} = 2\pi \sqrt{\frac{a^3}{\mu}}$$

### Radius of apoapsis (`apoapsis`)
The radius of apoapsis in kilometers:

$$ r_p = a (1+e) $$

### Radius of periapsis (`periapsis`)
The radius of periapsis in kilometers:

$$ r_p = a (1-e) $$

### Radius unit vector (`r_hat`)
Unit vector in the direction of the radius vector.

\begin{equation}
\frac {\mathbf{r}} {|r|}
\end{equation}

### Radius vector (`radius`, `rmag`)
The radius vector, in kilometers.

\begin{equation}
\mathbf{r} = \begin{bmatrix}
    x \\
    y \\
    z \\
\end{bmatrix}
\end{equation}

The magnitude of the radius vector in kilometers.

$$r = ||\mathbf r|| = \sqrt{x^2+y^2+z^2}$$

### Right ascension (`right_ascension`)
Returned in degrees between $[0;360]$.

$$\alpha = \tan^{-1} \frac y x $$

### Right ascension of the ascending node (`raan`)
The right ascension of the ascending node and is returned in degrees:

1. Rotate the momentum vector:

    \begin{equation}
    \mathbf n = \begin{bmatrix}
        0 \\
        0 \\
        1 \\
    \end{bmatrix} \times \mathbf h
    \end{equation}

2. Compute the RAAN:

    $$ \Omega = \cos ^{-1} \left( \frac {n_x}{|\mathbf n|} \right) $$

3. Perform a quadrant check: if $n_y$ is less then zero, return the AoP as $2\pi - \Omega$ instead.

### Semi major axis (`sma`)
The semi major axis, returned in kilometers.

$$a = \frac{-\mu}{2\xi}$$

### Semi minor axis (`semi_minor_axis`)
Returns the semi minor axis in kilometers for hyperbolic and elliptical orbits (will fail for a perfectly circular orbit).

If the eccentricity is less than $1.0$:

$$ b = \sqrt{(a e)^2 - a^2} $$

Else:

$$ b = \frac {h^2} {\mu \sqrt{e^2 - 1}} $$

### Semi parameter (`semi_parameter`)
The semilatus rectum, in kilometers

$$ p = a (1-e^2) $$

### True anomaly (`ta`)
The true anomaly is computed as follows and is returned in degrees.

1. Compute $\cos \nu$.

    We also check that the value is bounded between $[-1;1]$ (as it should be mathematically but rounding issues on computers may cause problems): if not, depending on the value of $\cos \nu$ the phasing is set to either 0 or 180 degrees.

    $$ \cos \nu = \mathbf e \cdot \frac {\mathbf r}{e \times ||\mathbf r|| } $$

2. Compute the true anomaly with a quadrant check.
    1. If the arccos of $\nu$ fails (NaN), then a warning is emited and return 0 degrees.
    2. Else if $\mathbf r \cdot \mathbf v < 0$, return $2\pi - \nu$.
    1. Else, return $\nu$.

!!! warning
    If the eccentricity is below the eccentricity tolerance, a warning is emitted stating that the true anomaly is ill-defined for circular orbits.

### True longitude (`tlong`)
The true longitude is an alternate phasing element. Nyx will return this angle between 0 and 360 degrees.

$$\lambda = \omega + \Omega + \nu$$


### Velocity declination (`velocity_declination`)
Returned in degrees between $[-180;180]$.

$$ \delta = \sin^{-1} \frac {v_z} {||\mathbf v||} $$

### Velocity vector (`velocity`, `vmag`)
The velocity vector, in kilometers per second.

\begin{equation}
\mathbf{v} = \begin{bmatrix}
    v_x \\
    v_y \\
    v_z \\
\end{bmatrix}
\end{equation}

The magnitude of the velocity vector in kilometers per second.

$$v = ||\mathbf v|| = \sqrt{v_x^2+v_y^2+v_z^2}$$

### Velocity unit vector (`v_hat`)
Unit vector in the direction of the velocity vector.

\begin{equation}
\frac {\mathbf{v}} {|v|}
\end{equation}

## Validation

This validation compares the computations of orbital elements in nyx with those in GMAT. Each scenario script is in the subfolder [state](https://gitlab.com/nyx-space/nyx/-/tree/master/tests/GMAT_scripts/state).

The following table corresponds to the **absolute errors** between the Nyx computations and those of GMAT. I'll save you the read: the absolute errors are precisely zero for a 64-bit floating point representation (`double` in C).

??? check "Validation"
    To run all of these test cases, clone the Nyx repo and execute the following command:
    ```
    cargo test state_def_circ_eq -- --nocapture
    cargo test state_def_circ_inc -- --nocapture
    cargo test state_def_ellip -- --nocapture
    cargo test geodetic -- --nocapture
    ```

!!! Methodology
    The validation is trivially the following: a spacecraft is defined in GMAT in the EarthMJ2000Eq frame by its Cartesian state. There is a "Propagate" segment of strictly zero seconds. The desired orbital state computations are exported to a report file.

### From a Cartesian state

Element / Scenario  | circular inclined  | circular equatorial  | elliptical
--|---|---|--
Earth.Energy  | 0.0 | 0.0 | 0.0
Earth.OrbitPeriod | 0.0 | 0.0 | 0.0
Earth.HX  | 0.0  | 0.0 | 0.0
Earth.HY  | 0.0  | 0.0 | 0.0
Earth.HZ  | 0.0  | 0.0 | 0.0
Earth.SMA  | 0.0  | 0.0 | 0.0
Earth.ECC  |  0.0 | 0.0 | 0.0
EarthMJ2000Eq.INC  | 0.0 | 0.0  | 0.0
EarthMJ2000Eq.RAAN  | 0.0  | 0.0  | 0.0
EarthMJ2000Eq.AOP  | 0.0 | 0.0 | 0.0
Earth.TA  | 0.0 | 0.0 | 0.0
Earth.TLONG | 0.0 | 0.0 | 0.0
Earth.EA | 0.0 | 0.0 | 0.0
Earth.MA | 0.0 | 0.0 | 0.0
Earth.RadApo | 0.0 | 0.0 | 0.0
Earth.RadPer | 0.0 | 0.0 | 0.0
Earth.SemilatusRectum | 0.0 | 0.0 | 0.0


### From a Keplerian state

Element / Scenario  | circular inclined  | circular equatorial  | elliptical
--|---|---|--
Earth.X  | 0.0 | 0.0 | 0.0
Earth.Y  | 0.0 | 0.0 | 0.0
Earth.Z  | 0.0 | 0.0 | 0.0
Earth.VX  | 0.0 | 0.0 | 0.0
Earth.VY  | 0.0 | 0.0 | 0.0
Earth.VZ  | 0.0 | 0.0 | 0.0
Earth.Energy  | 0.0 | 0.0 | 0.0
Earth.OrbitPeriod | 0.0 | 0.0 | 0.0
Earth.HX  | 0.0 | 0.0 | 0.0
Earth.HY  | 0.0 | 0.0 |0.0
Earth.HZ  | 0.0 | 0.0 | 0.0
Earth.SMA  | 0.0 | 0.0 | 0.0
Earth.ECC  | 0.0 | 0.0 | 0.0
EarthMJ2000Eq.INC | 0.0 | 0.0 | 0.0
EarthMJ2000Eq.RAAN | 0.0 | 0.0 | 0.0
EarthMJ2000Eq.AOP | 0.0 | 0.0 | 0.0
Earth.TA  | 0.0 | 0.0 | 0.0
Earth.TLONG | 0.0 | 0.0 | 0.0
Earth.EA | 0.0 | 0.0 | 0.0
Earth.MA | 0.0 | 0.0 | 0.0
Earth.RadApo | 0.0 | 0.0 | 0.0
Earth.RadPer | 0.0 | 0.0 | 0.0
Earth.SemilatusRectum | 0.0 | 0.0 | 0.0

### From geodesic
!!! check "Validation"
    ```
    $ cargo test geodetic -- --nocapture
        Compiling nyx-space v1.0.0-alpha.1 (/home/chris/Workspace/rust/nyx)
    Finished test [unoptimized + debuginfo] target(s) in 35.70s
    (...)
        Running target/debug/deps/lib-48ccd68343ebbebb

    running 1 test
    [tests/cosmic/state.rs:341] eme2k.semi_major_radius() = 6378.1363
    latitude (φ): 0.00e0
    longitude (λ): 0.00e0
    height: 0.00e0
    r_i: 0.00e0
    r_j: 0.00e0
    r_k: 0.00e0
    r_i: 0.00e0
    r_j: 0.00e0
    r_k: 0.00e0
    latitude (φ): 0.00e0
    longitude (λ): 0.00e0
    height: 0.00e0
    test cosmic::state::geodetic_vallado ... ok
    ```

## Partial (`OrbitDual`)
Nyx is all about using dual numbers![^3] An `OrbitDual` object can be created from a normal `Orbit` structure in order to retrieve the exact partials of many orbital elements with respect to each component of the position and velocity. These can be combined for achieving specific targets and is used for achieving B-Plane targets.

List of available partials, always with respect to the position components x,y,z and the velocity components vx, vy, vz. Each of these partials are accessible via their respective `wtr_PARAM()` function.

+ magnitude of radius vector `rmag`
+ magnitude of velocity vector `vmag`
+ X component of the orbital momentum `hx`
+ Y component of the orbital momentum `hy`
+ Z component of the orbital momentum `hz`
+ magnitude of orbital momentum vector `hmag`
+ orbital energy `energy`
+ eccentricity `ecc`
+ inclination `inc`
+ argument of periapsis `aop`
+ right ascension of the ascending node `raan`
+ true anomaly `ta`
+ true longitude `tlong`
+ argument of latitude `aol`
+ periapsis 
+ apoapsis
+ eccentric anomaly `ea`
+ flight path angle `fpa`
+ mean anomaly `ma`
+ semi parameter `semi_parameter`
+ geodetic longitude `geodetic_longitude`
+ geodetic latitude `geodetic_latitude`
+ geodetic height `geodetic_height`
+ right ascension `right_ascension`
+ decliation `decliation`
+ semi minor axis `semi_minor_axis`
+ velocity decliation `velocity_decliation`
+ $C_3$ `c3`
+ hyperbolic anomaly `hyperbolic_anomaly`

[^1]: Nyx allows initialization from geodesic elements only for the following celestial bodies: Mercury, Venus, Earth, Luna/Earth Moon, and Mars. Although the Jupiter, Saturn, Uranus, and Neptune also have an angular velocity defined in Nyx, they do not have an ellipsoid flatenning parameter.
[^2]: Two other computation methods were attempted (McMahon and Jah). The first prevented convergence of the shooting algorithm and the second led to near infinite LTOF.
[^3]: Please refer to [Dual Numbers](/MathSpec/appendix/dual_numbers) for a primer on dual number theory.
--8<-- "includes/Abbreviations.md"