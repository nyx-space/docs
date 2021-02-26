# Orbit design from a genetic algorithm

[![View project code](https://img.shields.io/badge/Nyx_v.1-View_project_code-3d84e8?logo=rust)](https://gitlab.com/nyx-space/showcase/orbit_design_ga/)
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

One options is brute force: iterate through a ton of different initial states. It would work and frankly it wouldn't be _that_ slow[^1] because Nyx is blazing fast.

However, let's setup a genetic algorithm using the crate [oxigen](https://docs.rs/oxigen/). Not shown here in the snippets below, but we've added `oxigen = "2"` and `rand = {version = "0.7", features = ["small_rng"]}` to the Cargo.toml dependency file.

We're using a genetic algorithm because it works great for optimization problems where there isn't a gradient. At first thought, I can't think of a gradient approach to solving this "multiple elevation buckets" problem. If there is one, let me know!

### Genetic algorithm fitness function
We'll change the buckets idea a bit. The problem with the current implementation is that we only store the maximum elevation. Really, we should be determining the usefulness of our initial orbit by simply by the number of times we've hit the bucket during the whole propagation of one day. Then, we can define the cost function as the sum of these hits. But we also need to emphasize however that a single pass in any of the buckets is great.

Let's define the fitness function as follows:

+ 100 points for the first item in each bucket;
+ 1 point for each subsequent item.

For example, if there's one passage between 45 and 60, two between 60 and 75, but none above 75, then the fitness of that individual is $(100)+(100+1)+(0)=201$. This should work decently well because we're sampling the trajectory the same number of times each trajectory. The search will also be faster because we don't have to advance through the trajectory orbit-by-orbit.

We change the elevation count to the following:

```rust
// Let's keep track of the max elevation for each bucket
let mut el_bw_45_60: u32 = 0;
let mut el_bw_60_75: u32 = 0;
let mut el_bw_75_90: u32 = 0;

// Iterate through the trajectory between the bounds.
for state in traj.every(2 * TimeUnit::Minute) {
    // Compute the elevation
    let (elevation, _) = landmark.elevation_of(&state);
    if elevation >= 75.0 {
        // Fun syntax to increment the value by some number in a conditional way
        el_bw_75_90 += if el_bw_75_90 == 0 { 100 } else { 1 };
    } else if elevation >= 60.0 {
        el_bw_60_75 += if el_bw_60_75 == 0 { 100 } else { 1 };
    } else if elevation >= 45.0 {
        el_bw_45_60 += if el_bw_45_60 == 0 { 100 } else { 1 };
    }
}

let sum_fitness = el_bw_45_60 + el_bw_60_75 + el_bw_75_90;

println!("Fitness = {}", sum_fitness);
```

The original orbit has a fitness score of $105$.

### Initial guess for the genome
With all genetic algorithms, one needs to specify the genes which are used to vary the population. In our case, we'll only vary the initial orbit. My hunch is that an orbit which solves this problem adequately is nearly a sun-synchronous orbit, but not quite. Let's setup the genome such that it allows variation of the eccentricity, inclination, argument of periapse and RAAN.

However, this is my first time trying to use a genetic algorithm, so I'll simply change the inclination first and increase the size of the genome later. So the genome will have a unique gene of type `f64`. I'll be using the [onemax](https://github.com/Martin1887/oxigen/blob/master/onemax-oxigen/src/main.rs) implementation as an example.

Let's create a new file which will implement oxigen's [Genotype trait](https://docs.rs/oxigen/2.2.0/oxigen/genotype/trait.Genotype.html). The whole file is [a bit long](https://gitlab.com/nyx-space/showcase/orbit_design_ga/-/blob/6c7c973eca164a76273707eb64d8ad3a736f3009/src/genotype.rs), so here I'll simply paste on the `fitness` function and the updated `main` function. All I did was copy the code from the previous main function into the fitness function and accounted for the genes.

=== "`genome.rs`"
    ```rust
    fn fitness(&self) -> f64 {
        // For now, we'll redefine everything here.
    
        // Load the NASA NAIF DE438 planetary ephemeris.
        let cosm = Cosm::de438();
        // Grab the Earth Mean Equator J2000 frame
        let eme2k = cosm.frame("EME2000");
        // Set the initial start time of the scenario
        let epoch = Epoch::from_gregorian_tai_at_noon(2021, 2, 25);
        // Define the state with an altitude above the reference frame.
        // Nearly circular orbit (ecc of 0.01), inclination of 49 degrees and TA at 30.0
        let orbit = Orbit::keplerian_alt(
            500.0,
            0.01,
            49.0 + self.genes[0],
            0.0,
            0.0,
            30.0,
            epoch,
            eme2k,
        );
    
        // Define the landmark by specifying a name, a latitude, a longitude, an altitude (in km) and a frame.
        // Note that we're also "cloning" the Cosm: don't worry, it's a shared object, so we're just cloning the
        // the reference to it in memory, and never loading it more than once.
        let landmark = GroundStation::from_point(
            "Eiffel Tower".to_string(),
            48.8584,
            2.2945,
            0.0,
            cosm.frame("IAU Earth"),
            cosm.clone(),
        );
    
        // Let's specify the force model to be two body dynamics
        // And use the default propagator setup: a variable step Runge-Kutta 8-9
        let setup = Propagator::default(OrbitalDynamics::two_body());
    
        // Use the setup to seed a propagator with the initial state we defined above.
        let mut prop = setup.with(orbit);
        // Now let's propagate for a week and generate the trajectory so we can analyse it.
        let (_, traj) = prop.for_duration_with_traj(1 * TimeUnit::Day).unwrap();
    
        // Let's keep track of the max elevation for each bucket
        let mut el_bw_45_60: u32 = 0;
        let mut el_bw_60_75: u32 = 0;
        let mut el_bw_75_90: u32 = 0;
    
        // Iterate through the trajectory between the bounds.
        for state in traj.every(2 * TimeUnit::Minute) {
            // Compute the elevation
            let (elevation, _) = landmark.elevation_of(&state);
            if elevation >= 75.0 {
                // Fun syntax to increment the value by some number in a conditional way
                el_bw_75_90 += if el_bw_75_90 == 0 { 100 } else { 1 };
            } else if elevation >= 60.0 {
                el_bw_60_75 += if el_bw_60_75 == 0 { 100 } else { 1 };
            } else if elevation >= 45.0 {
                el_bw_45_60 += if el_bw_45_60 == 0 { 100 } else { 1 };
            }
        }
    
        let sum_fitness = el_bw_45_60 + el_bw_60_75 + el_bw_75_90;
    
        println!("{} => {:o} => {}", self, orbit, sum_fitness);
    
        f64::from(sum_fitness)
    }
    ```

=== "`main.rs`"
    ```rust
    fn main() {
        let problem_size: usize = 1;
        let population_size = problem_size * 8;
        let log2 = (f64::from(problem_size as u32) * 4_f64).log2().ceil();
        let (solutions, generation, _progress, _population) =
            GeneticExecution::<f64, OrbitIndividual>::new()
                .population_size(population_size)
                .genotype_size(problem_size)
                .mutation_rate(Box::new(MutationRates::Linear(SlopeParams {
                    start: f64::from(problem_size as u32) / (8_f64 + 2_f64 * log2) / 100_f64,
                    bound: 0.005,
                    coefficient: -0.0002,
                })))
                .selection_rate(Box::new(SelectionRates::Linear(SlopeParams {
                    start: log2 - 2_f64,
                    bound: log2 / 1.5,
                    coefficient: -0.0005,
                })))
                .select_function(Box::new(SelectionFunctions::Cup))
                .run();
    
        println!("Finished in the generation {}", generation);
        for sol in &solutions {
            println!("{}", sol);
        }
    }
    ```

This converges in the **first generation**!

```
$ cargo run --release
   Compiling orbit_design_ga v0.1.0 (/home/chris/Workspace/nyx-space/showcase/orbit_design_ga)
    Finished release [optimized] target(s) in 3.52s
     Running `target/release/orbit_design_ga`
[0.5595646111692654] => [Earth J2000] 2021-02-25T12:00:00 TAI   sma = 6878.136300 km    ecc = 0.010000  inc = 49.559565 deg     raan = 0.000000 deg     aop = 360.000000 deg    ta = 30.000000 deg => 206
[1.8047327480852193] => [Earth J2000] 2021-02-25T12:00:00 TAI   sma = 6878.136300 km    ecc = 0.010000  inc = 50.804733 deg     raan = 360.000000 deg   aop = 360.000000 deg    ta = 30.000000 deg => 207
[4.937132954499962] => [Earth J2000] 2021-02-25T12:00:00 TAI    sma = 6878.136300 km    ecc = 0.010000  inc = 53.937133 deg     raan = 360.000000 deg   aop = 360.000000 deg    ta = 30.000000 deg => 313
[8.733245489773708] => [Earth J2000] 2021-02-25T12:00:00 TAI    sma = 6878.136300 km    ecc = 0.010000  inc = 57.733245 deg     raan = 360.000000 deg   aop = 0.000000 deg      ta = 30.000000 deg => 317
[6.560870232109691] => [Earth J2000] 2021-02-25T12:00:00 TAI    sma = 6878.136300 km    ecc = 0.010000  inc = 55.560870 deg     raan = 360.000000 deg   aop = 360.000000 deg    ta = 30.000000 deg => 215
[1.9207503374182244] => [Earth J2000] 2021-02-25T12:00:00 TAI   sma = 6878.136300 km    ecc = 0.010000  inc = 50.920750 deg     raan = 0.000000 deg     aop = 360.000000 deg    ta = 30.000000 deg => 207
[8.140198536077483] => [Earth J2000] 2021-02-25T12:00:00 TAI    sma = 6878.136300 km    ecc = 0.010000  inc = 57.140199 deg     raan = 360.000000 deg   aop = 360.000000 deg    ta = 30.000000 deg => 317
[1.9670620359924451] => [Earth J2000] 2021-02-25T12:00:00 TAI   sma = 6878.136300 km    ecc = 0.010000  inc = 50.967062 deg     raan = 360.000000 deg   aop = 0.000000 deg      ta = 30.000000 deg => 208
Finished in the generation 0
[4.937132954499962]
[8.733245489773708]
[8.140198536077483]

```

### Making the problem harder
This was too easy. Let's add more buckets, provide a higher reward for the first hit ($1000$ point reward), and vary more parameters: inc, ecc, RAAN and AoP.

To avoid changing the eccentricity by something too crazy, let's only change it by 1% of the random value. Angles still vary by ten times the random number.

All that has really changed is the way we handle the buckets. We now have five buckets of different elevations: 45-55; 55-65; 65-75; 75-85; 85-90. We consider an initial orbit to be a solution only if its fitness is greater than $5000$, so it must pass through the five buckets.

```rust
// (...)

// Let's keep track of the max elevation for each bucket:
// 45-55; 55-65; 65-75; 75-85; 85-90
// We'll store them in a vector
let mut elevations = vec![0, 0, 0, 0, 0];

// Iterate through the trajectory between the bounds.
for state in traj.every(2 * TimeUnit::Minute) {
    // Compute the elevation
    let (elevation, _) = landmark.elevation_of(&state);
    let bucket_idx = if elevation >= 85.0 {
        0
    } else if elevation >= 75.0 {
        1
    } else if elevation >= 65.0 {
        2
    } else if elevation >= 55.0 {
        3
    } else if elevation >= 45.0 {
        4
    } else {
        // We don't care about this elevation
        continue;
    };
    if elevations[bucket_idx] == 0 {
        elevations[bucket_idx] += 1000;
    } else {
        elevations[bucket_idx] += 1
    }
}

let sum_fitness: u32 = elevations.iter().sum();

// (...)
```

This finds a solutions in 2 to 4 generations, depending on the run. It takes less than a minute to propagate hundreds of spacecraft (in two body dynamics of course).

## Results

To summarize, we've seen how Nyx can be combined with a genetic algorithm quite trivially and how to build the problem up from nothing. Here, we've varied the inclination, eccentricity, RAAN and AoP.

Now that we know the genetic algorithm can find a solution, let's clean up the code and make sure to test the solution found by the GA. The only change was adding an `impl` for `OrbitIndividual` and moving the fitness calculation in there. This allows checking the solutions found.

Of course, the genetic algorithm is a probabilistic solution, so it won't always converge on the same solution. Here are five runs with different solutions.

Click the following button to run these cases yourself directly on the cloud! [![Gitpod Run on the cloud](https://img.shields.io/badge/Gitpod-Run_on_the_cloud-blue?logo=gitpod)](https://gitpod.io/#https://gitlab.com/nyx-space/showcase/orbit_design_ga)

!!! note
    It took me about five hours from the first line of code until the end of this post. I can't imagine solving this problem with STK or GMAT in that time, yet I know the latter very well.


#### Case 1
Solution found in the 0th generation:

| ecc  | inc (deg) | RAAN (deg) | AoP (deg) |
| -- | -- | -- | -- |
| 0.013294  | 57.545662 | 2.336691 | 0.953208 |

| 45-55  | 55-65 | 65-75 | 75-85 | 85-90 |
| -- | -- | -- | -- | -- |
| 10  | 5 | 3 | 1 | 1 |

??? info "Output"

        Finished in the generation 0
        [Earth J2000] 2021-02-25T12:00:00 TAI   sma = 6878.136300 km    ecc = 0.013294  inc = 57.545662 deg     raan = 2.336691 deg     aop = 0.953208 deg      ta = 30.000000 deg
        45-55: 10     55-65: 5     65-75: 3     75-85: 1     85-90: 1
        Fitness: 5015

#### Case 2
Solution found in the 0th generation:

| ecc  | inc (deg) | RAAN (deg) | AoP (deg) |
| -- | -- | -- | -- |
| 0.011963  | 53.376785 | 5.376642 | 6.973544 |

| 45-55  | 55-65 | 65-75 | 75-85 | 85-90 |
| -- | -- | -- | -- | -- |
| 6  | 3 | 1 | 1 | 1 |

??? info "Output"
        Finished in the generation 0
        [Earth J2000] 2021-02-25T12:00:00 TAI   sma = 6878.136300 km    ecc = 0.011963  inc = 53.376785 deg     raan = 5.376642 deg     aop = 6.973544 deg      ta = 30.000000 deg
        45-55: 6        55-65: 3        65-75: 1        75-85: 1        85-90: 1
        Fitness: 5007

#### Case 3
Solution found in the 2nd generation:

| ecc  | inc (deg) | RAAN (deg) | AoP (deg) |
| -- | -- | -- | -- |
| 0.018035  | 57.507162 | 0.460785 | 2.268064 |

| 45-55  | 55-65 | 65-75 | 75-85 | 85-90 |
| -- | -- | -- | -- | -- |
| 10  | 5 | 3 | 1 | 1 |

??? info "Output"
        Finished in the generation 2
        [Earth J2000] 2021-02-25T12:00:00 TAI   sma = 6878.136300 km    ecc = 0.018035  inc = 57.507162 deg     raan = 0.460785 deg     aop = 2.268064 deg      ta = 30.000000 deg
        45-55: 10       55-65: 5        65-75: 3        75-85: 1        85-90: 1
        Fitness: 5015

#### Case 4
Solution found in the 0th generation:

| ecc  | inc (deg) | RAAN (deg) | AoP (deg) |
| -- | -- | -- | -- |
| 0.017843  | 53.885220 | 7.111687 | 5.823606 |

| 45-55  | 55-65 | 65-75 | 75-85 | 85-90 |
| -- | -- | -- | -- | -- |
| 7  | 3 | 1 | 1 | 1 |

??? info "Output"
        Finished in the generation 0
        [Earth J2000] 2021-02-25T12:00:00 TAI   sma = 6878.136300 km    ecc = 0.017843  inc = 53.885220 deg     raan = 7.111687 deg     aop = 5.823606 deg      ta = 30.000000 deg
        45-55: 7        55-65: 3        65-75: 1        75-85: 1        85-90: 1
        Fitness: 5008
    
#### Case 5
Solution found in the 0th generation:

| ecc  | inc (deg) | RAAN (deg) | AoP (deg) |
| -- | -- | -- | -- |
| 0.018346  | 57.788652 | 0.979918 | 9.990995 |

| 45-55  | 55-65 | 65-75 | 75-85 | 85-90 |
| -- | -- | -- | -- | -- |
| 9  | 6 | 2 | 1 | 1 |

??? info "Output"
        Finished in the generation 0
        [Earth J2000] 2021-02-25T12:00:00 TAI   sma = 6878.136300 km    ecc = 0.018346  inc = 57.788652 deg     raan = 0.979918 deg     aop = 9.990995 deg      ta = 30.000000 deg
        45-55: 9        55-65: 6        65-75: 2        75-85: 1        85-90: 1
        Fitness: 5014



[^1]: In fact, since each propagation is 0.75 seconds in release mode, it would take about 40 minutes on ten CPU core to test every inclination from 0 to 90 degrees and every AoP from 0 to 360 degrees (with 1 degree increments).

--8<-- "includes/Abbreviations.md"