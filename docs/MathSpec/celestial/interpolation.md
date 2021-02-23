# Interpolated trajectories
This section is focused on the generation of interpolated trajectories by propagators in Nyx.

Interpolated trajectories are computed in parallel causing a negligible impact in computational performance. All of the event finding requires an interpolated trajectory. Trajectories all use a Lagrange interpolation, provided by the [bacon-sci](https://crates.io/crates/bacon-sci) crate. The interpolation algorithm was thoroughly verified by Chris Rabotin (who even made a minor contribution to the bacon-sci crate).

!!! info "Technical note"
    Starting a propagator with the `for_duration_with_traj()` will return the final state of the propagation and the associated trajectory. If the initial state only included acceleration models, the output trajectory is of kind `Ephemeris`. If any acceleration models were enabled, the output trajectory is of kind `ScTraj`. Finally, if using a custom `StateType` for the propagation, then the interpolated trajectory is simply a generic `Trajectory<StateType>` where 32 items from the propagator will be accumulated into a trajectory segment.

    The segments in a trajectory are organized in a binary tree map allowing for blazing fast access to any segment of the trajectory. Trajectories are organized in segments of 32 propagation states (or 16 for a spacecraft trajectory, which ensures continuity of the fuel interpolation).

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

All of the above is computed in 5.7 seconds on a standard desktop computer.

!!! note
    If propagating with the STM, then the trajectory will also include the STM for that specific step forward.

??? check "Validation"
    ```sh
    $ RUST_LOG=info RUST_BACKTRACE=1 /usr/bin/time cargo test traj_ephem --release -- --nocapture
    (...)
    
    Average SMA: 7712.186 km
    [traj_ephem] Maximum interpolation error: pos: 5.50e-8 m    vel: 7.89e-8 m/s                full state: 7.24e-5 (no unit)
    [traj_ephem] Maximum interpolation error after double conversion: pos: 4.30e-8 m    vel: 1.53e-11 m/s    full state: 7.91e-6 (no unit)
    test traj_ephem ... ok
    
    test result: ok. 1 passed; 0 failed; 1 ignored; 0 measured; 1 filtered out; finished in 5.70s
    ```


## Spacecraft trajectory

??? check "Validation"
    ```sh
    $ RUST_LOG=info RUST_BACKTRACE=1 /usr/bin/time cargo test traj_spacecraft --release -- --nocapture
    (...)

    Mode changed from Coast to Thrust @ 2021-01-01T12:00:37 TAI
    [traj_spacecraft] Maximum interpolation error: pos: 1.21e-7 m    vel: 7.28e-7 m/s    fuel: 5.44e-8 g         full state: 1.07e-9 (no unit)
    [traj_ephem] Maximum interpolation error after double conversion: pos: 1.29e-7 m    vel: 7.28e-7 m/s
    test traj_spacecraft ... ok
    
    test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 2 filtered out; finished in 0.35s
    ```
## Navigation trajectory

When running a Navigation, the OD Process can output an interpolation of the estimates and their covariances. This allows subsequent sampling of the navigation trajectory.