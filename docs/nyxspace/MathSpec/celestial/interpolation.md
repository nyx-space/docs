# Interpolated trajectories
This section is focused on the generation of interpolated trajectories by propagators in Nyx.

Interpolated trajectories are computed in parallel leading to a negligible impact in computational performance. **All of the event finding requires an interpolated trajectory.**

Trajectories store a interpolation splines created from a Hermite interpolation (written from scratch and validated against NumPy). Specifically, the algorithm works by curve fitting the provided states in position, velocity, and fuel mass (when interpolating a spacecraft trajectory instead of just an orbital trajectory). This curve fit will generate a _Hermite series_ which is then converted into a _generic polynomial_. Note that none of these operations require memory allocations (and rely on Rust's [`const generic`](https://rust-lang.github.io/rfcs/2000-const-generics.html) feature).

??? info "Technical note"
    Starting a propagator with the `for_duration_with_traj()` will return the final state of the propagation and the associated trajectory. This only works for states which also implement the [`InterpState` trait](https://docs.rs/nyx-space/latest/nyx_space/md/trajectory/trait.InterpState.html).

    The segments in a trajectory are organized in a binary tree map allowing for blazing fast access to any segment of the trajectory.

!!! warning "Limitations"
    1. To support generating the trajectories in parallell and storing them in a binary tree, it was necessary to choose an indexing method independent of the duration of the interpolation spline. This has been chosen to be the _centiseconds_ (10 milliseconds) since the start of the trajectory, the start being the very first state used to seed the trajectory. This means that if two splines last _less than 10 ms_, one will **overwrite** the other in the binary tree, meaning that part of the trajectory will **not** be queryable.
    1. Changing the frame of a trajectory follows the Shannon Nyquist sampling theorem. However, this will introduce _some imprecision_ nevertheless. Multiple conversions (e.g. from EME2000 to Moon J2000 back to EME2000) will accumulate errors quickly.
    1. Trajectories can currently only be generated with forward propagation. (Fixed in version 1.1.)

## Ephemeris

1. Propagate a LEO orbit with STM for 31 days in two body dynamics and request the propagator to generate the trajectory on the fly.
1. Compute the average SMA of that orbit by sampling the trajectory every 1 day (this ensures that the compiler does not remove the trajectory querying section from the test).
1. Check that the first and last state of the trajectory are strictly equal to the input propagator state and output propagator state.
1. Check that querying a trajectory one nanosecond after its end state returns an error.
1. Request a new propagation from the initial state but without generating the trajectory and read every intermediate state from that propagation. For each state, compute the radius and velocity differences between each of those states and the interpolated states at those exact times.
1. Ensure that the interpolation error in position is less than 1 micrometer and the error in velocity is less than 1 micrometer per second.
1. Convert the whole trajectory to its equivalent in the Moon J2000 frame (called `Luna` in Nyx). Convert that new trajectory back into the Earth Mean Equator J2000 frame (`EME2000`).
1. Sample that "double converted" trajectory every five minutes and compare each of those states with the initial interpolated trajectory.
1. Ensure that the interpolation error in position is less than 1 micrometer and the error in velocity is less than 1 micrometer per second.

All of the above is computed in 0.9 seconds on a standard desktop computer.

!!! note
    If propagating with the STM, then the trajectory will also include the STM for that specific step forward.

!!! check "Validation"
    ```sh
    $ RUST_LOG=info RUST_BACKTRACE=1 /usr/bin/time cargo test traj_ephem --release -- --nocapture
     INFO  nyx_space::propagators::propagator > Propagating for 30 days 23 h 59 min 60 s 0 ms -0.021928026217210607 ns until 2021-02-01T12:00:00 UTC
    Average SMA: 7712.186 km        Should be: 7712.186
    [tests/propagation/trajectory.rs:46] sum_sma / cnt - start_state.sma() = 0.000000245786395680625
    Ephem: Trajectory from 2021-01-01T12:00:00 UTC to 2021-02-01T12:00:00 UTC (30 days 23 h 59 min 60 s 0 ms -0.021928026217210607 ns, or 2678400.000 s) [4613 splines]
     INFO  nyx_space::propagators::propagator > Propagating for 30 days 23 h 59 min 60 s 0 ms -0.021928026217210607 ns until 2021-02-01T12:00:00 UTC
    [traj_ephem] Maximum interpolation error: pos: 2.25e-8 m                vel: 1.98e-11 m/s
     INFO  nyx_space::md::trajectory::traj    > Converted trajectory from Earth J2000 to Moon J2000 in 189 ms
    ephem_luna Trajectory from 2021-01-01T12:00:00 UTC to 2021-02-01T12:00:00 UTC (30 days 23 h 59 min 60 s 0 ms -0.021928026217210607 ns, or 2678400.000 s) [11203 splines]
     INFO  nyx_space::md::trajectory::traj    > Converted trajectory from Moon J2000 to Earth J2000 in 448 ms
    (...)

    [traj_ephem] Maximum interpolation error after double conversion: pos: 1.27e-1 m                vel: 4.41e-7 m/s
    test propagation::trajectory::traj_ephem ... ok

    test result: ok. 1 passed; 0 failed; 1 ignored; 0 measured; 116 filtered out; finished in 0.94s
    ```


## Spacecraft trajectory

!!! check "Validation"
    ```sh
    $ RUST_LOG=info RUST_BACKTRACE=1 /usr/bin/time cargo test traj_spacecraft --release -- --nocapture
    (...)

    [traj_spacecraft] Maximum interpolation error: pos: 1.75e-7 m           vel: 1.35e-6 m/s                fuel: 1.14e-10 g                full state: 3.06e-8 (no unit)
     INFO  nyx_space::md::trajectory::traj         > Converted trajectory from Earth J2000 to Moon J2000 in 1 ms
     INFO  nyx_space::md::trajectory::traj         > Converted trajectory from Moon J2000 to Earth J2000 in 3 ms
    [traj_ephem] Maximum interpolation error after double conversion: pos: 5.76e-2 m                vel: 1.52e-7 m/s
    test traj_spacecraft ... ok
    
    test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 2 filtered out; finished in 0.35s
    ```
## Navigation trajectory

Version 1.1 will allow generating navigation as well.