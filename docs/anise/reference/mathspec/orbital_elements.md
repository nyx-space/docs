This page summarizes how the orbital elements are computed in ANISE. Note that Nyx uses ANISE for all orbital computations.

## Representation
ANISE stores all of the orbit information as a Cartesian state, in units of kilometer and kilometer per second, because it is a non-singular representation of an orbit. In Rust, the `Orbit` structure is an alias for `CartesianState`, and are interchangable one for one. In Python, only `Orbit` is exposed as a class. An `Orbit` includes the radius vector, the velocity vector, the frame, and the epoch.

## Initialization methods

An orbit may be initialized from its Cartesian position and velocity components (from 64-bit floating point values or from a vector of that type), from Keplerian orbital elements where the phasing parameter is the true anomaly or mean anomaly, or from its geodetic elements (latitude, longitude and height compared to the reference ellipsoid of the frame, requires the mean angular speed of the object). The initializer also includes an epoch (cf. [Time MathSpec](../../../hifitime/index.md)) and a frame.

As discussed above, the state is stored in Cartesian form. Hence, initializing in Keplerian form will trigger the conversion of the state from Keplerian orbital element into Cartesian orbital elements. This method _supports_ hyperbolic, circular inclined, circular equatorial, and the common elliptical orbits. The eccentricity tolerance is set to $1e^{-11}$, i.e. if the eccentricity is below that number, then the orbit is considered circular and the appropriate conversions to Cartesian will be triggered.

Vallado's geodetic to Cartesian initializer is also implemented allowing the initialization of a state known only by its longitude, laltitude and height above the reference ellipsoid of that rocky celestial object.

Finally, one may also initialize a new orbit from a previous orbit via `with_sma_km`, `with_ecc`, `with_inc_deg`, `with_raan_deg`, `with_aop_deg`, `with_ta_deg`: these copy a previous orbit but change the requested Keplerian orbital element to the requested value. Analogous methods exist with `add` instead of `with` which will add the provided value to the current Keplerian element value. For example `some_orbit.add_inc_deg(-10.0)` will create a new orbit where the inclination 10 degrees lower than `some_orbit`'s inclination.

Please refer to the API reference of the language you're working with for additional details.

## Accessor methods
In the following, the position coordinates are referred to as $x,y,z$ and the velocity components as $v_x,v_y,v_z$. More generally, $\gamma_x$, $\gamma_y$, $\gamma_z$ respectively refer to the x, y, and z component of the $\gamma$ vector.

All accessor methods include the unit in which the result is returned. All setter methods include the units in the documentation and/or in the name of the argument, e.g. `sma_km`.

### Argument of latitude (`aol_deg`)
The true longitude is an alternate phasing element. ANISE will return this angle between 0 and 360 degrees.

1. If the eccentricity is below the eccentricity tolerance:

    $$ u = \lambda - \Omega $$

2. Else:

    $$ u = \omega + \nu $$


### Argument of periapsis (`aop_deg`)
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

### C3 (`c3_km2_s2`)
Computes the $C_3$ of this orbit:

$$ C_3= -\frac \mu a$$

### Declination (`declination_deg`)
Returned in degrees between $[-180;180]$.

$$ \delta = \sin^{-1} \frac z {||\mathbf r||} $$

### Distance between two orbits `distance_to`
The distance in kilometers between two states, computed as follows (where $r$ and $r'$ respectively refer to the `this` state and the `other` state).

$$\sqrt {(r_x-r^\prime_x)^2+(r_y-r^\prime_y)^2+(r_z-r^\prime_z)^2} $$

### Eccentricity (`evec`, `ecc`)
Respectively, the eccentricity vector and its magnitude (i.e. the eccentricity)

$$ \mathbf e = \left(||\mathbf v||^2 - \frac{\mu}{||\mathbf r||}\right) \cdot \mathbf r - \frac{\mathbf r \cdot \mathbf v}{\mu}\cdot \mathbf v$$

For the rest of the MathSpec, let $e = ||\mathbf e||$.

### Eccentric anomaly (`ea_deg`)
ANISE returns this parameter ($E$) in degrees.

1. Compute the sine of the eccentric anomaly

    $$\sin E = \frac{\sqrt{1 - e^2} \sin\nu} {1 + e \cos \nu}$$

2. Compute the cosine of the eccentric anomaly

    $$\cos E = \frac{e + \cos\nu} {1 + e \cos \nu}$$

3. Returns the quadrant-checked tangent of those angles (`atan2`), converted to degrees.

!!! note
    This is a conversion from GMAT's `StateConversionUtil::TrueToEccentricAnomaly`.

### Flight path angle (`fpa_deg`)

1. Compute the sine of the FPA, $f$:

    $$ \sin f = \frac{e \sin \nu} {\sqrt{1 + 2e\cos\nu + e^2}} $$

2. Compute the cosine of the FPA, $f$:

    $$ \cos f = \frac{1 + e \cos \nu} {\sqrt{1 + 2e\cos\nu + e^2}} $$

3. Returns the quadrant-checked tangent of those angles (`atan2`), converted to degrees.

### Geodetic parameters (`latlongalt`)

Using the non-iterative Heikkinen procedure (as recommended by Zhu), the latitude, longitude, and height compared to ellipsoid are returned in that order from this function. The algorithm is detailed on Wikipedia at [this permalink](https://en.wikipedia.org/w/index.php?title=Geographic_coordinate_conversion&oldid=1188033720#The_application_of_Ferrari's_solution). The results match Vallado and GMAT, but the computation is about twice as fast.

!!! warning
    This function requires that the orbit already be in a body fixed frame. ANISE will _not_ check that.

### Geodetic height (`height_km`)

A helper function to `latlongalt`, returns the height in kilometers.


### Geodetic latitude (`latitude_deg`)

A helper function to `latlongalt`, returns the latitude in degrees between $[-180;180]$.

### Geodetic longitude (`longitude_deg`)

The angle is returned in degrees between $[0;360]$.

$$ \lambda = \tan^{-1} \frac{y}{x} $$

!!! warning
    This function requires that the orbit already be in a body fixed frame. ANISE will _not_ check that.

### Hyperbolic anomaly (`hyperbolic_anomaly_deg`)
Computes the hyperbolic anomaly for this hyperbolic orbit in degrees between $[0;360]$, or will return an error (`NyxError::NotHyperbolic`) if the orbit is not hyperbolic.

$$ H = \sinh^{-1}\left( \frac{\sin(\nu) \sqrt{e^2 -1}} {1 + e\cos\nu} \right)$$

### Inclination (`inc_deg`)
The inclination of this orbit, returned in degrees.

$$ i = \cos^{-1} \left(\frac {h_z}{|\mathbf h|}\right)$$

### Mean anomaly (`ma_deg`)

1. If the eccentricity is below 1, the mean anomaly $M$ is computed as follows

    $$ M = E-e\sin E $$

2. If the eccentricity is strictly above 1:

    $$ M = \sinh^{-1} \frac {\sin\nu \sqrt{e^2 - 1} }{1 + e \cos\nu} $$

!!! note
    This is a conversion from GMAT's `StateConversionUtil::TrueToMeanAnomaly`. This function _does support_ the mean anomaly for hyperbolic orbits (but not for parabolic orbits).

### Momentum vector (`hvec`, `hmag`, `hx`, `hy`, `hz`)
The momentum vector, its magnitude, and its X, Y and Z components.

$$\mathbf{h} = \mathbf r \times \mathbf v$$

### Orbital energy (`energy_km2_s2`)
The orbit's energy:

$$ \xi = \frac {||\mathbf v||^2}{2} - \frac{\mu}{\mathbf r} $$

### Orbital period (`period`)
The orbital period, returned as high-precision `Duration` structure:

$$\mathcal{P} = 2\pi \sqrt{\frac{a^3}{\mu}}$$

### Radius of apoapsis (`apoapsis_km`)
The radius of apoapsis in kilometers:

$$ r_p = a (1+e) $$

### Radius of periapsis (`periapsis_km`)
The radius of periapsis in kilometers:

$$ r_p = a (1-e) $$

### Radius unit vector (`r_hat`)
Unit vector in the direction of the radius vector.

\begin{equation}
\frac {\mathbf{r}} {|r|}
\end{equation}

### Radius vector (`radius_km`, `rmag_km`)
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

### Right ascension (`right_ascension_deg`)
Returned in degrees between $[0;360]$.

$$\alpha = \tan^{-1} \frac y x $$

### Right ascension of the ascending node (`raan_deg`)
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

### Semi major axis (`sma_km`)
The semi major axis, returned in kilometers.

$$a = \frac{-\mu}{2\xi}$$

### Semi minor axis (`semi_minor_axis_km`)
Returns the semi minor axis in kilometers for hyperbolic and elliptical orbits (will fail for a perfectly circular orbit).

If the eccentricity is less than $1.0$:

$$ b = \sqrt{(a e)^2 - a^2} $$

Else:

$$ b = \frac {h^2} {\mu \sqrt{e^2 - 1}} $$

### Semi parameter (`semi_parameter_km`)
The semilatus rectum, in kilometers

$$ p = a (1-e^2) $$

### True anomaly (`ta_deg`)
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

### True longitude (`tlong_deg`)
The true longitude is an alternate phasing element. ANISE will return this angle between 0 and 360 degrees.

$$\lambda = \omega + \Omega + \nu$$


### Velocity declination (`velocity_declination_deg`)
Returned in degrees between $[-180;180]$.

$$ \delta = \sin^{-1} \frac {v_z} {||\mathbf v||} $$

### Velocity vector (`velocity_km_s`, `vmag_km_s`)
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

This validation compares the computations of orbital elements in ANISE with those in GMAT. Each scenario script is in the subfolder [state](https://gitlab.com/nyx-space/nyx/-/tree/master/tests/GMAT_scripts/state).

The following table corresponds to the **absolute errors** between the ANISE computations and those of GMAT. I'll save you the read: the absolute errors are precisely zero for a 64-bit floating point representation (`double` in C).

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

--8<-- "includes/Abbreviations.md"