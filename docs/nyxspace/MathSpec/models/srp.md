# Solar radiation pressure

SRP is implemented as a `ForceModel`, meaning that the implementation computes a force from which the instantaneous mass of the spacecraft is subsequently divided to apply an acceleration. Therefore, as opposed to most formulations in the literature, we will use a force formulation.

Currently, Nyx only supports spherical SRP model.

## Nomenclature

+ $\mathbf{r_\odot}$: vector from the Sun to the spacecraft, in km
+ $\mathbf{\hat r_\odot}$: unit vector of $\mathbf{r_\odot}$, unitless
+ $k$: shaddowing factor, 1.0 in full illumination and 0.0 in full shadow [^1], unitless
+ $\phi$: mean solar flux at 1 AU, defaults to 1367.0, in $\frac{W}{m^2}$
+ $C_r$: coefficient of reflectivity of the spacecraft, unitless
+ $\mathcal{A}$: SRP area of the spacecraft, in $m^2$
+ $c$: the speed of light in meters per second, set to 299,792,458.0

Note that $C_r$ and $\mathcal{A}$ are stored in the "context" passed to the EOM function and therefore can vary between integration steps.

## Algorithm

First, we compute the position of the Sun as seen from the spacecraft, and its unit vector, respectively $\mathbf{r_\odot}$ and $\mathbf{\hat r_\odot}$. Then, we compute the shadowing factor, $k$, using the [eclipse model](../celestial/eclipse.md).

Compute the norm of Sun vector in AU, $||\mathbf{r_\odot}||_{\text{AU}}$ by dividing the $\mathbf{r_\odot}$ vector by 1 AU.

Compute the flux pressure as follows:

$$\Phi_{\text{SRP}} = \frac{k\phi}{c} \left(\frac{1.0}{||\mathbf{r_\odot}||_{\text{AU}}} \right)^2$$

Finally, return the SRP force [^2]:

$$ \mathbf{F}_{\text{SRP}} = C_r \mathcal{A} \Phi_{\text{SRP}} \mathbf{\hat r_\odot}$$

!!! note
    Although the above derivation mentions the Sun, Nyx trivially supports any other light source regardless of the integration frame.

??? check "Validation"
    Nyx has three validation scenarios for the SRP computation to ensure that we test full illumination (`srp_earth_full_vis`), long penumbra passages (`srp_earth_meo_ecc_inc`), and very short penumbra passages (`srp_earth_penumbra`). In all of the test cases, we propagate a spacecraft for 24 **days** to ensure that a high amount of error can accumulate if the modeling is incorrect. The worst absolute position error is _high_ compared to GMAT: 287 meters.

    I have deemed this error _acceptable_ and attributed it to the following factors:

    + the difference in constants; [^3]
    + the difference in the penumbra percentage calculation method;
    + the fact that GMAT performs its penumbra calculation with respect to the spacecraft integration frame position instead of the spacecraft position itself, which I think might lead to an accumulation of rounding errors.

    Please **email me** your recommendations to further check this model.

    Case | RSS position (m) | RSS velocity (m/s) 
    --|---|--
    Full visibility | 0.488578 | 0.000081
    MEO | 1.381728 | 0.000470
    LEO | 5.980461 | 0.006447

    ```bash
    $ RUST_BACKTRACE=1 cargo test --release -- srp_earth_ --nocapture
    (...)
    Error accumulated in full sunlight over 24 days 0 h 0 min 0 s : 0.488578 m      0.000081 m/s
    test mission_design::force_models::srp_earth_full_vis ... ok
    [Earth J2000] 2000-01-25T00:00:00 TAI   sma = 13999.490721 km   ecc = 0.500183  inc = 19.999552 deg     raan = 359.999754 deg   aop = 0.008741 deg      ta = 228.062192 deg     300 kg
    Error accumulated in ecc+inc MEO (with penumbras) over 24 days 0 h 0 min 0 s : 1.381728 m       0.000470 m/s
    test mission_design::force_models::srp_earth_meo_ecc_inc ... ok
    [Earth J2000] 2000-01-25T00:00:00 TAI   sma = 6999.999433 km    ecc = 0.000118  inc = 0.000736 deg      raan = 293.379260 deg   aop = 90.482624 deg     ta = 252.626454 deg     300 kg
    Error accumulated in circular equatorial LEO (with penumbras) over 24 days 0 h 0 min 0 s : 5.980461 m   0.006447 m/s
    test mission_design::force_models::srp_earth_leo ... ok
    
    test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 96 filtered out; finished in 10.51s
    ```
    

[^1]: Computation of the shadowing factor uses the Eclipse computation derived [here](../celestial/eclipse.md).
[^2]: The code multiplies the value by 1e-3 to convert from $\frac{m}{s^2}$ to $\frac{km}{s^2}$.
[^3]: For example GMAT uses an older definition of 1 AU which is 700 meters different from the IAU definition: changing that will bring down this maximum error by over 30 meters (to around 250 meters).

--8<-- "includes/Abbreviations.md"