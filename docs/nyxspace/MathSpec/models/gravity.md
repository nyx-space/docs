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
    In summary, Nyx matches GMAT at **micrometer or better** accuracy in each component of the position and **nanometer per second accuracy or better** in each component of the velocity. Note that both GMAT and Nyx propagate the state in kilometers. Further, on a 64 bit floating point representation (used by both Nyx and GMAT), the best possible matching is 2e-16 kilometers, or 2e-13 meters, or 0.2 picometers.

    The two body dynamics are validated against GMAT using the GMAT values for $\mu$. The validation scenario propagates a LEO spacecraft forward in time for one day using an adaptive step RK89 numerical integrator. It compares the final result with the result from the GMAT. It then propagates this final state by one day and ensures that the difference between the back-propagated state and the initial state has an RSS error of less than 10 millimeters (1e-5 km).[^1] The RSS error from the back-propagation is actually 1.38 millimeters. The following table shows the _absolute_ errors on the same platform.

    X (km)  | Y (km)  | Z (km)  | VX (km/s) | VY (km/s) | VZ (km/s)
    --|---|---|---|---|--
    6e-12  | 8e-10 | 1e-9 | 1e-12 | 1e-13 | 5e-13

    ```bash
    $ RUST_BACKTRACE=1 cargo test --release -- val_two_ --nocapture
       Compiling nyx-space v1.0.0-alpha.2 (/home/chris/Workspace/rust/nyx)
        Finished release [optimized] target(s) in 6.37s
         Running target/release/deps/nyx_space-f0273a0ad4832aca
    
    running 0 tests
    
    test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 30 filtered out; finished in 0.00s
    
         Running target/release/deps/nyxcli-ec6c9ca3b3fa86db
    
    running 0 tests
    
    test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
    
         Running target/release/deps/lib-731ac57663b8679f
    
    running 1 test
    ==> val_two_body_dynamics absolute errors
    6e-12   8e-10   1e-9    1e-12   7e-13   5e-13
    RTN:  [Earth J2000] 2000-01-01T12:00:00 TAI     position = [-2436.449999, -2436.450001, 6891.037000] km velocity = [5.088611, -5.088611, -0.000000] km/s
    INIT: [Earth J2000] 2000-01-01T12:00:00 TAI     position = [-2436.450000, -2436.450000, 6891.037000] km velocity = [5.088611, -5.088611, 0.000000] km/s
    [Earth J2000] 2000-01-01T12:00:00 TAI   sma = 7712.186236 km    ecc = 0.001000  inc = 63.434003 deg     raan = 135.000000 deg   aop = 90.000000 deg     ta = 0.000000 deg
    [tests/mission_design/orbitaldyn.rs:53] err_r = 0.000001381643705733031
    test mission_design::orbitaldyn::val_two_body_dynamics ... ok
    
    ```

## Multibody
This computation happens in the `PointMasses` models. It is the generalization of the equation from the previous "two-body" section.

This model does not affect the velocity components of the time derivative, only the acceleration of the next propagator step, noted as $\dot{\mathbf{v}}_{t'}$. As such it is implemented as an `AccelModel`.

In the following, $\mathbf{r_{ij}}$ is the position of the $i$-th celestial body as seen from the integration frame at the integration time. The $\mathbf{r_{j}}$ vector is the position of the spacecraft as seen from the $i$-th celestial body.

$$\mathbf{r_{j}} = \mathbf{r}_t - \mathbf{r_{ij}}$$

$$\dot{\mathbf{v}}_{t'} = \dot{\mathbf{v}}_{t'} - \mu_i \left( \frac{\mathbf{r_j}}{|\mathbf{r_j}|^3} - \frac{\mathbf{r_{ij}}}{|\mathbf{r_{ij}}|^3} \right)$$

??? check "Validation"
    In summary, Nyx matches GMAT at **100 micrometer or better** accuracy in position (typically tens of micrometers) and **2 micrometer per second or better** (typically 100 nanometers per second) accuracy in velocity for a one day propagation. The largest errors are seen when propagating in a non-optimal frame, specifically, propagating a low lunar orbiter in the EME2000 frame.

    The validation of the multibody dynamics inherently includes the validation of the computation of the position of celestial objects. These are currently stored in a proprietary protobuf format, but another open-source format (with FSW in mind) is in the works and will be released before the end of 2021.

    The GMAT validation scenarios are available on the repository in `tests/GMAT_scripts/propagators`.

    The following scenario permutations are tested:
    + Earth-Moon Halo orbit, Low Lunar Orbiter, and LEO
    + RK8 10s time step, or RK89 with adaptive step size
    + Earth & Moon point masses, or Earth, Moon, Sun and Jupiter
    + Cislunar trajectory using an RK4 fixed step of 0.5 seconds with Earth, Moon and Sun gravity, propagated for 36 hours
    
    RSS position errors are in **meters**, RSS velocity errors in **meters per second**, but component errors are in kilometers and kilometers per second.
    
    Case | RSS position (m) | RSS velocity (m/s) | Adaptive/Fixed | Point masses | Prop. start date | X (km)  | Y (km)  | Z (km)  | VX (km/s) | VY (km/s) | VZ (km/s)
    --|---|---|---|---|---|---|---|---|---|---|--
    E-M Halo | 1.71624e-4 | 1.58051e-9 | Fixed | Earth Moon  | 2020-01-01 | 6e-8  |  2e-7  |  5e-8    | 1e-12 |  6e-13 |  9e-13
    E-M Halo | 3.21844e-4 | 1.08012e-9 | Adaptive | Earth Moon | 2002-02-07 | 1e-8  |  3e-7  |  1e-7  |  1e-12  | 1e-14 |  3e-14
    E-M Halo | 1.68523e-4 | 1.59021e-9 | Fixed | Earth Moon Sun Jupiter | 2020-01-01 | 5e-8  |  2e-7  |  5e-8  |  1e-12 |  6e-13 |  9e-13
    E-M Halo | 1.79139e-4 | 5.16179e-10 | Adaptive | Earth Moon Sun Jupiter | 2002-02-07 | 4e-9   | 2e-7 |  6e-8  |  5e-13 |  3e-14 |  2e-15
    LLO | 3.69863e-4 | 4.94220e-10 | Adaptive | Earth Moon | 2002-02-07 | 1e-7  |  3e-7  |  8e-8    |5e-13  | 1e-13 |  6e-14
    LLO | 9.86846e-4 | 1.51935e-9 | Adaptive | Earth Moon Sun Jupiter | 2002-02-07 | 4e-7  |  9e-7  |  2e-7  |  1e-12 |  4e-13  | 1e-13
    LEO | 2.62910e-3 | 2.45180e-6 | Adaptive | Earth Moon Sun Jupiter | 2020-01-01 | 2e-8  |  2e-6  |  2e-6    |2e-9  |  1e-9  |  9e-10
    LEO | 4.78574e-4 | 4.46347e-7 | Adaptive | Earth Sun Jupiter (_no_ Moon!) | 2020-01-01 | 3e-9  |  3e-7    | 4e-7  |  3e-10  | 2e-10 |  2e-10
    Cislunar | 1.01787e-4 | 1.22381e-7 | Fixed | Earth Moon Sun | 2022-11-27 | 3e-8  |  8e-8  | 5e-8  | 1e-10 | 4e-11  | 3e-11

    Rerun the Halo validation with `RUST_BACKTRACE=1 cargo test --release -- val_halo --nocapture`. Rerun the LLO validation with `RUST_BACKTRACE=1 cargo test --release -- val_llo --nocapture`. Rerun the LEO validation with `RUST_BACKTRACE=1 cargo test --release -- val_leo_multi --nocapture`.

[^1]: This is the accuracy GMAT expects from a back propagation, as detailed in the [GMAT_V&V_ProcessAndResults.pdf](/assets/pdf/GMAT_VV_ProcessAndResults.pdf) file.

--8<-- "includes/Abbreviations.md"