This section focuses on building interpolated trajectories by propagators in Nyx.

For details on interpolation methods for trajectories, including [Chebyshev](../../../anise/reference/mathspec/interpolation/chebyshev.md), [Lagrange](../../../anise/reference/mathspec/interpolation/lagrange.md), and [Hermite](../../../anise/reference/mathspec/interpolation/hermite.md) interpolators, refer the [ANISE math spec reference on interpolation](../../../anise/reference/mathspec/interpolation/index.md).

Interpolated trajectories are computed in parallel leading to a negligible impact in computational performance. To build a trajectory from a propagation event, call the [`for_duration_with_traj()`](https://rustdoc.nyxspace.com/nyx_space/propagators/struct.PropInstance.html#method.for_duration_with_traj) function on the propagator. Note that all of the event finding requires an interpolated trajectory.

Trajectories in Nyx are a simple list of discrete states interpolated using the [Hermite interpolation](../../../anise/reference/mathspec/interpolation/hermite.md). They are akin to the NASA/SPICE Hermite Type 13 interpolator.

Spacecraft trajectories can be transformed into another frame by transforming each of the individual states into the desired frame.

!!! warning
    Transforming a trajectory into another frame _is different_ from propagating the original spacecraft in that other frame. A propagator will advance with a different step depending on the central body, refe to [the reference on propagator](../../../nyxspace/MathSpec/propagators.md).
    
    For example, propagating a spacecraft defined in the Earth Mean J2000 (EME2000) inertial frame when accounting for the point mass gravity of the Earth and the Moon and transforming that trajectory into a Moon J2000 centered frame will lead to a different trajectory that propagating that same inertial state defined in the Moon J2000 frame.

## Trajectory Ephemeris Integration Test

Details of the `traj_ephem_forward` integration test.

### Test Configuration

- Initial epoch: 2021-01-01 12:00:00 UTC
- Initial state: LEO orbit in Earth J2000 frame
- Propagation duration: 31 days
- Dynamics: Two-body
- Integration method: variable step Runge-Kutta 8-9

### Success Criteria

| Metric | Requirement |
|--------|-------------|
| Position Error (Direct) | 0 m |
| Velocity Error (Direct) | 0 m/s |
| Position Error (Post frame conv.) | < 1 m |
| Velocity Error (Post frame conv.) | < 0.01 m/s |
| Temporal Precision | < 1 μs |

### Test Structure

#### Trajectory Generation and Basic Validation

   - Builds a trajectory
   - Validates conservation of semi-major axis
   - Verifies initial and final states match propagation
   - Ensures STM (State Transition Matrix) is properly unset
   - Confirms interpolation bounds are respected

#### Interpolation Accuracy

   - Parallel truth generation
   - Compares interpolated states against truth trajectory
   - Validates position and velocity errors at exact timesteps
   - Expected accuracy: machine precision for stored states

#### Persistence Testing

   - Exports trajectory to Parquet format
   - Includes eclipse event detection
   - Reloads trajectory and verifies:
     - State count consistency
     - Temporal boundaries
     - State vector equality
     - Microsecond-level epoch precision

#### Frame Transformation Validation

   - Double conversion test: Earth J2000 → Moon J2000 → Earth J2000
   - Samples every 5 minutes
   - Validates:
     - Temporal consistency
     - Position error < 1 meter
     - Velocity error < 0.01 m/s


!!! check "Run log"
    ```sh
    $ RUST_LOG=info RUST_BACKTRACE=1 /usr/bin/time cargo test traj_ephem --release -- --nocapture
    INFO  nyx_space::propagators::instance > Propagating for 31 days until 2021-02-01T12:00:00 UTC
    INFO  nyx_space::propagators::instance >       ... done in 247 ms 822 μs 611 ns
    [TIMING] 293 ms 488 μs 896 ns
    Average SMA: 7712.186 km        Should be: 7712.186
    Ephem: Trajectory in Earth J2000 (μ = 398600.435436096 km^3/s^2, eq. radius = 6378.14 km, polar radius = 6356.75 km, f = 0.0033536422844278) from 2021-01-01T12:00:00 UTC to 2021-02-01T12:00:00 UTC (31 days, or 2678400.000 s) [32289 states]
    INFO  nyx_space::propagators::instance > Propagating for 31 days until 2021-02-01T12:00:00 UTC
    INFO  nyx_space::propagators::instance >       ... done in 274 ms 970 μs 367 ns
    [traj_ephem] Maximum error on exact step: pos: 0.00e0 m         vel: 0.00e0 m/s
    INFO  nyx_space::md::trajectory::traj  > Exporting trajectory to parquet file...
    INFO  nyx_space::md::trajectory::traj  > Serialized 32289 states from 2021-01-01T12:00:00 UTC to 2021-02-01T12:00:00 UTC
    INFO  nyx_space::md::trajectory::traj  > Evaluating 1 event(s)
    INFO  nyx_space::md::trajectory::traj  > Trajectory written to /home/chris/Workspace/nyx-space/nyx/output_data/ephem_forward-2024-10-27T06-36-19.parquet in 2 s 245 ms 95 μs 680 ns
    INFO  nyx_space::io::trajectory_data   > File: /home/chris/Workspace/nyx-space/nyx/output_data/ephem_forward-2024-10-27T06-36-19.parquet
    INFO  nyx_space::io::trajectory_data   > Created on: 2024-10-27T06:36:20.258980864 UTC
    INFO  nyx_space::io::trajectory_data   > nyx-space License: AGPL 3.0
    INFO  nyx_space::io::trajectory_data   > Created by: Chris Rabotin (chris) on Linux
    INFO  nyx_space::io::trajectory_data   > Purpose: Trajectory data
    INFO  nyx_space::io::trajectory_data   > Generated by: Nyx v2.0.0-rc
    INFO  nyx_space::md::trajectory::sc_traj > Converted trajectory from Earth J2000 (μ = 398600.435436096 km^3/s^2, eq. radius = 6378.14 km, polar radius = 6356.75 km, f = 0.0033536422844278) to Moon J2000 in 300 ms: Trajectory in Moon J2000 (μ = 4902.800066163796 km^3/s^2, radius = 1737.4 km) from 2021-01-01T12:00:00 UTC to 2021-02-01T12:00:00 UTC (31 days, or 2678400.000 s) [32289 states]
    ephem_luna Trajectory in Moon J2000 (μ = 4902.800066163796 km^3/s^2, radius = 1737.4 km) from 2021-01-01T12:00:00 UTC to 2021-02-01T12:00:00 UTC (31 days, or 2678400.000 s) [32289 states]
    INFO  nyx_space::md::trajectory::sc_traj > Converted trajectory from Moon J2000 (μ = 4902.800066163796 km^3/s^2, radius = 1737.4 km) to Earth J2000 (μ = 398600.435436096 km^3/s^2, eq. radius = 6378.14 km, polar radius = 6356.75 km, f = 0.0033536422844278) in 299 ms: Trajectory in Earth J2000 (μ = 398600.435436096 km^3/s^2, eq. radius = 6378.14 km, polar radius = 6356.75 km, f = 0.0033536422844278) from 2021-01-01T12:00:00 UTC to 2021-02-01T12:00:00 UTC (31 days, or 2678400.000 s) [32289 states]
    Ephem back: Trajectory in Earth J2000 (μ = 398600.435436096 km^3/s^2, eq. radius = 6378.14 km, polar radius = 6356.75 km, f = 0.0033536422844278) from 2021-01-01T12:00:00 UTC to 2021-02-01T12:00:00 UTC (31 days, or 2678400.000 s) [32289 states]
    2.328666121016051e-11
    Eval: total mass = 0.000 kg @  [Earth J2000] 2021-01-01T12:05:00 UTC    position = [-834.810409, -3848.218391, 6622.529651] km  velocity = [5.519092, -4.261593, -1.778298] km/s  Coast
    Conv: total mass = 0.000 kg @  [Earth J2000] 2021-01-01T12:05:00 UTC    position = [-834.810409, -3848.218391, 6622.529651] km  velocity = [5.519092, -4.261593, -1.778298] km/s  Coast 0.000 m

    (...)

    [traj_ephem] Maximum interpolation error after double conversion: pos: 3.76e-8 m                vel: 1.13e-9 m/s
    test propagation::trajectory::traj_ephem_forward ... ok
    ```
