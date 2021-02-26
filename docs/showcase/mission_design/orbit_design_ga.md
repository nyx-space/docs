# Orbit design from a genetic algorithm

[![View project code](https://img.shields.io/badge/Nyx-View_project_code-3d84e8?logo=rust)](https://gitlab.com/nyx-space/showcase/orbit_design_ga/)
[![Gitpod Run on the cloud](https://img.shields.io/badge/Gitpod-Run_on_the_cloud-blue?logo=gitpod)](https://gitpod.io/#https://gitlab.com/nyx-space/showcase/orbit_design_ga){.right}

[**Jump to results**](#results)

## Goal
We would like an orbit which flies over a point of interest on the Earth such that it can see that object from different angles. Let's assume that we can fly over that object regardless of the time of day (e.g. if we had a SAR sensor for imaging).

In the following, I detail each iteration and how the problem was build. Each of the steps received their own commit on the repo, so you can track the development of the script there.

### Constraints
Let's start by defining the target object: the Eiffel Tower, located at 48.8584° N, 2.2945° E. We want to the spacecraft to see it from different angles over a one-day period. More specifically, we want the spaceraft will fly over this landmark once over that period with the following elevation:

+ 75 - 90 degrees
+ 60 - 75 degrees
+ 45 - 60 degrees

!!! note
    This code was developed when Nyx version 1 was still in development. Therefore, the `Cargo.toml` file, which tracks the dependencies of the project, refers to a custom path on my computer. You should replace the `nyx-space` dependency in that file to `nyx-space = "1"`.

## Initial guess

### Initial orbit setup
Let's start by importing `nyx` and a bunch of stuff needed for mission design:

```rust
extern crate nyx_space as nyx;

use nyx::md::ui::*;
```

Now let's define a LEO orbit specifying an altitude of 500 km. The definition of an orbit from Keplerian elements always follows the order: semi-major axis (km), eccentricity (no unit), inclination (degrees), right ascension of the ascending node (degrees), argument of periapse (degrees), true anomaly (degrees), epoch, and frame.

```rust
// Load the NASA NAIF DE438 planetary ephemeris.
let cosm = Cosm::de438();
// Grab the Earth Mean Equator J2000 frame
let eme2k = cosm.frame("EME2000");
// Set the initial start time of the scenario
let epoch = Epoch::from_gregorian_tai_at_noon(2021, 2, 25);
// Nearly circular orbit (ecc of 0.01), inclination of 49 degrees and TA at 30.0
let orbit = Orbit::keplerian_alt(500.0, 0.01, 49.0, 0.0, 0.0, 30.0, epoch, eme2k);
```

!!! note
    We defined the initial inclination to be 49 degrees: we know from basic two-body dynamics that this implies the ground track of the spacecraft will reach a maximum latitude of 49 degrees. So this is a good initial guess that we might be able to fly over the Eiffel Tower at the proper inclination we'd like.

### Define the landmark
Let's define the Eiffel Tower. It is fixed to the Earth, so we're specifying the IAU Earth frame. Nyx only has high-fidelity frames, so none of the educational ECEF or ECI frames here.

!!! tip
    Anything that is defined on the surface of a celestial body in terms of latitude, longitude and height is created using the `GroundStation` structure. That structure is defined in the orbit determination module of Nyx, so make sure to import that: `use nyx::od::ui::GroundStation;`.

```rust
// Define the landmark by specifying a name, a latitude, a longitude,
// an altitude (in km) and a frame. Note that we're also "cloning"
// the Cosm: don't worry, it's a shared object, so we're just cloning the
// the reference to it in memory, and never loading it more than once.
let landmark = GroundStation::from_point(
    "Eiffel Tower".to_string(),
    36.0544,
    112.1402,
    0.0,
    cosm.frame("IAU Earth"),
    cosm.clone(),
);

// Let's print this landmark to make sure we've created it correctly.
println!("{}", landmark);
```

For good measure, let's run this and make sure it works.

```
$ cargo run
   Compiling nyx-space v0.1.0-beta2 (/home/chris/Workspace/rust/nyx)
   Compiling orbit_design_ga v0.1.0 (/home/chris/Workspace/nyx-space/showcase/orbit_design_ga)
warning: unused variable: `orbit`
  --> src/main.rs:34:9
   |
34 |     let orbit = Orbit::keplerian_alt(500.0, 0.01, 49.0, 0.0, 0.0, 30.0, epoch, eme2k);
   |         ^^^^^ help: if this is intentional, prefix it with an underscore: `_orbit`
   |
   = note: `#[warn(unused_variables)]` on by default

warning: 1 warning emitted

    Finished dev [unoptimized + debuginfo] target(s) in 2.85s
     Running `target/debug/orbit_design_ga`
[Earth IAU Fixed] Eiffel Tower (lat.: 36.05 deg    long.: 112.14 deg    alt.: 0.00 m)
$ 
```

### Propagation
For the moment, we'll just use two body dynamics. Note that Nyx _always_ propagates the dynamics even if there is a simple analytical solution like in two body dynamics.

```rust
// Let's specify the force model to be two body dynamics
// And use the default propagator setup: a variable step Runge-Kutta 8-9
let setup = Propagator::default(OrbitalDynamics::two_body());

// Use the setup to seed a propagator with the initial state we defined above.
let mut prop = setup.with(orbit);
// Now let's propagate and generate the trajectory so we can analyse it.
let (final_state, traj) = prop.for_duration_with_traj(1 * TimeUnit::Day)?;

// Printing the state with `:o` will print its Keplerian elements
println!("{:o}", final_state);
```

### Elevation computation from trajectory
One of the best analysis features of Nyx is being able to play with trajectories generated from a propagation segment. One can iterate through the trajectory with a simple `for` loop.

```rust
// Finally, let's query the trajectory every other minute,
// compute the elevation and store the minimum and maximum
// elevation for that whole day.
let mut min_el = std::f64::INFINITY;
let mut max_el = std::f64::NEG_INFINITY;
let mut min_dt = epoch;
let mut max_dt = epoch;
for state in traj.every(2 * TimeUnit::Minute) {
    // Compute the elevation
    let (elevation, _) = landmark.elevation_of(&state);
    if elevation > max_el {
        max_el = elevation;
        max_dt = state.epoch();
    }

    if elevation < min_el {
        min_el = elevation;
        min_dt = state.epoch();
    }
}

println!("Min elevation {:.2} degrees @ {}", min_el, min_dt);
println!("Max elevation {:.2} degrees @ {}", max_el, max_dt);
```

Let's run this to see what those initial values are.

```
$ cargo run
   Compiling orbit_design_ga v0.1.0 (/home/chris/Workspace/nyx-space/showcase/orbit_design_ga)
    Finished dev [unoptimized + debuginfo] target(s) in 1.46s
     Running `target/debug/orbit_design_ga`
[Earth IAU Fixed] Eiffel Tower (lat.: 48.86 deg    long.: 2.29 deg    alt.: 0.00 m)
[Earth J2000] 2021-02-26T12:00:00 TAI   sma = 6878.136300 km    ecc = 0.010000  inc = 49.000000 deg     raan = 0.000000 deg     aop = 0.000000 deg      ta = 109.485866 deg
Min elevation -86.49 degrees @ 2021-02-26T10:58:00 TAI
Max elevation 58.63 degrees @ 2021-02-25T20:08:00 TAI

```

On my computer, this scenario takes 7.89 seconds to run, which is a bit slow for my liking. So speed it up, tell Rust to compile this in `release` mode by running with `cargo run --release`. This whole analysis then runs in 0.75 seconds.

## Buckets for the desired elevation angles
So far, we have a pretty poor initial guess, and we aren't even checking if we fit in the buckets!

Let's define the buckets as specified in the goals above.

We change the trajectory iteration code to the following:

```rust

// Let's keep track of the max elevation for each bucket
let mut el_bw_45_60 = std::f64::NEG_INFINITY;
let mut el_bw_45_60_epoch = epoch;
let mut el_bw_60_75 = std::f64::NEG_INFINITY;
let mut el_bw_60_75_epoch = epoch;
let mut el_bw_75_90 = std::f64::NEG_INFINITY;
let mut el_bw_75_90_epoch = epoch;
for state in traj.every(2 * TimeUnit::Minute) {
    // Compute the elevation
    let (elevation, _) = landmark.elevation_of(&state);
    if elevation >= 75.0 && elevation > el_bw_75_90 {
        el_bw_75_90 = elevation;
        el_bw_75_90_epoch = state.epoch();
    } else if elevation >= 60.0 && elevation > el_bw_60_75 {
        el_bw_60_75 = elevation;
        el_bw_60_75_epoch = state.epoch();
    } else if elevation >= 45.0 && elevation > el_bw_45_60 {
        el_bw_45_60 = elevation;
        el_bw_45_60_epoch = state.epoch();
    }
}

println!("Buckets");
println!("75.0+: {:.2} @ {}", el_bw_75_90, el_bw_75_90_epoch);
println!("60.0+: {:.2} @ {}", el_bw_60_75, el_bw_60_75_epoch);
println!("45.0+: {:.2} @ {}", el_bw_45_60, el_bw_45_60_epoch);
```

And as expected (because we didn't change the initial state), this initial guess is still as bad as earlier.

```
$ cargo run
   Compiling orbit_design_ga v0.1.0 (/home/chris/Workspace/nyx-space/showcase/orbit_design_ga)
    Finished dev [unoptimized + debuginfo] target(s) in 1.46s
     Running `target/debug/orbit_design_ga`
[Earth IAU Fixed] Eiffel Tower (lat.: 48.86 deg    long.: 2.29 deg    alt.: 0.00 m)
[Earth J2000] 2021-02-26T12:00:00 TAI   sma = 6878.136300 km    ecc = 0.010000  inc = 49.000000 deg     raan = 0.000000 deg     aop = 0.000000 deg      ta = 109.485866 deg
Buckets
75.0+: -inf @ 2021-02-25T12:00:00 TAI
60.0+: -inf @ 2021-02-25T12:00:00 TAI
45.0+: 58.63 @ 2021-02-25T20:08:00 TAI

```
## Buckets per orbit
Let's search for these elevations on a per-orbit basis: we'll probably want this in the genetic algorithm, not sure. I can always remove it.

For this, we'll be using two super useful features of Nyx. First, we'll iterate through the trajectory between specific times using `traj.every_between(...)`. Second, we'll be incrementing the start time just by adding the orbital period to the initial time: all of the fancy stuff is handled under the hood.

```rust
// Let's create a variable which stores the start of the orbit.
let mut orbit_start = epoch;
let mut orbit_cnt = 1;
loop {
    // Let's keep track of the max elevation for each bucket
    let mut el_bw_45_60 = std::f64::NEG_INFINITY;
    let mut el_bw_45_60_epoch = epoch;
    let mut el_bw_60_75 = std::f64::NEG_INFINITY;
    let mut el_bw_60_75_epoch = epoch;
    let mut el_bw_75_90 = std::f64::NEG_INFINITY;
    let mut el_bw_75_90_epoch = epoch;

    // Iterate through the trajectory between the bounds.
    for state in traj.every_between(
        2 * TimeUnit::Minute,
        orbit_start,
        orbit_start + orbit.period(),
    ) {
        // Compute the elevation
        let (elevation, _) = landmark.elevation_of(&state);
        if elevation >= 75.0 && elevation > el_bw_75_90 {
            el_bw_75_90 = elevation;
            el_bw_75_90_epoch = state.epoch();
        } else if elevation >= 60.0 && elevation > el_bw_60_75 {
            el_bw_60_75 = elevation;
            el_bw_60_75_epoch = state.epoch();
        } else if elevation >= 45.0 && elevation > el_bw_45_60 {
            el_bw_45_60 = elevation;
            el_bw_45_60_epoch = state.epoch();
        }
    }

    println!("Buckets in orbit #{}", orbit_cnt);
    if el_bw_75_90.is_finite() {
        println!("75.0+: {:.2} @ {}", el_bw_75_90, el_bw_75_90_epoch);
    } else {
        println!("75.0+: nothing found");
    }
    if el_bw_60_75.is_finite() {
        println!("60.0+: {:.2} @ {}", el_bw_60_75, el_bw_60_75_epoch);
    } else {
        println!("60.0+: nothing found");
    }
    if el_bw_45_60.is_finite() {
        println!("45.0+: {:.2} @ {}", el_bw_45_60, el_bw_45_60_epoch);
    } else {
        println!("45.0+: nothing found");
    }

    // Increment the counters
    orbit_cnt += 1;
    orbit_start += orbit.period();

    if orbit_start >= final_state.epoch() {
        break;
    }
}
```

## Genetic algorithm
**Recap:** At this stage, we can find the maximum elevation of the landmark for each orbit. This is cool, but it doesn't give a solution to the best orbit we need to properly image the Eiffel Tower from different elevations.

One options is brute force: iterate through a ton of different initial states. It would work, and frankly it wouldn't be _that_ slow because Nyx is blazing fast. In fact, since each propagation is 0.75 seconds in release mode, it would take about 40 minutes on ten CPU core to test every inclination from 0 to 90 degrees and every AoP from 0 to 360 degrees (with 1 degree increments).

## Results
_todo_

--8<-- "includes/Abbreviations.md"