# Orbit design from a genetic algorithm

[![View project code](https://img.shields.io/badge/Nyx_v.1-View_project_code-3d84e8?logo=rust)](https://gitlab.com/nyx-space/showcase/gmat_lunar_transfer/)
[![Gitpod Run on the cloud](https://img.shields.io/badge/Gitpod-Run_on_the_cloud-blue?logo=gitpod)](https://gitpod.io/#https://gitlab.com/nyx-space/showcase/gmat_lunar_transfer){.right}

[**Jump to results and plot**](#results)

## Introduction
**This is step by step guide to basic interplanetary mission design with Nyx using B-Plane targeting.** This is a clone of GMAT's `Ex_LunarTransfer.script` example script provided with GMAT 2020a. By the end of this guide, you'll see how to setup a B-Plane targeting in Nyx using either the TOML scenario setup[^1] or the pure Rust setup. The former is especially useful to work with a simple scenario without much customization

## Spacecraft setup

=== "Nyx (Rust)"

    ``` rust
    // Initialize the cosm which stores the ephemeris
    let cosm = Cosm::de438();
    // Grab the frames we'll use
    let eme2k = cosm.frame("EME2000");
    let iau_earth = cosm.frame("IAU Earth");
    // Define the epoch
    let epoch = Epoch::from_gregorian_utc(2014, 7, 22, 11, 29, 10, 811_000);
    // Define the initial orbit
    let orbit = Orbit::cartesian(
        -137380.1984338506,
        75679.87867537055,
        21487.63875187856,
        -0.2324532014235503,
        -0.4462753967758019,
        0.08561205662877103,
        epoch,
        eme2k,
    );

    // Define the spacecraft
    let sat = Spacecraft::new(orbit, 1000.0, 0.0, 1.0, 15.0, 1.7, 2.2);
    ```

=== "Nyx (CLI)"
    _TODO_ in version beta-2.

=== "GMAT"

    ``` matlab
    Create Spacecraft Sat;
    GMAT Sat.DateFormat = UTCGregorian;
    GMAT Sat.Epoch = '22 Jul 2014 11:29:10.811';
    GMAT Sat.CoordinateSystem = EarthMJ2000Eq;
    GMAT Sat.DisplayStateType = Cartesian;
    GMAT Sat.X = -137380.1984338506;
    GMAT Sat.Y = 75679.87867537055;
    GMAT Sat.Z = 21487.63875187856;
    GMAT Sat.VX = -0.2324532014235503;
    GMAT Sat.VY = -0.4462753967758019;
    GMAT Sat.VZ = 0.08561205662877103;
    GMAT Sat.DryMass = 1000;
    GMAT Sat.Cd = 2.2;
    GMAT Sat.Cr = 1.7;
    GMAT Sat.DragArea = 15;
    GMAT Sat.SRPArea = 1;
    ```

## Set up acceleration and force models

=== "Nyx (Rust)"

    ``` rust
    // Set up the harmonics first because we need to pass them to the overarching orbital dynamics
    // Load the harmonics from the JGM3 file (GMAT uses the JGM2 in this case).
    // It's gunzipped (hence `true` as the last parameter)
    let stor = HarmonicsMem::from_cof("JGM3.cof.gz", 20, 20, true)?;
    // Set up the orbital dynamics: we need to specify the models one by one here
    // because the usual functions wrap the dynamics so that they can be used in a Monte Carlo
    // setup.
    let orbital_dyn = OrbitalDynamics::new(vec![
        // Note that we are only accounting for Sun, Moon and Jupiter, in addition to the integration frame's GM
        PointMasses::new(
            eme2k,
            &[Bodies::Sun, Bodies::Luna, Bodies::JupiterBarycenter],
            cosm.clone(),
        ),
        // Specify that these harmonics are valid only in the IAU Earth frame. We're using the
        Harmonics::from_stor(iau_earth, stor, cosm.clone()),
    ]);


    // Set up SRP and Drag second, because we need to pass them to the overarching spacecraft dynamics
    let srp = SolarPressure::default(eme2k, cosm.clone());
    let drag = Drag::std_atm1976(cosm.clone());
    // Set up the spacecraft dynamics
    let sc_dyn = SpacecraftDynamics::from_models(orbital_dyn, vec![srp, drag]);
    ```

=== "Nyx (CLI)"
    _TODO_ in version beta-2.

=== "GMAT"

    ``` matlab
    Create ForceModel AllForces;
    GMAT AllForces.CentralBody = Earth;
    GMAT AllForces.PrimaryBodies = {Earth};
    GMAT AllForces.PointMasses = {Sun, Luna, Venus, Mars, Jupiter, Saturn, Uranus, Neptune};
    GMAT AllForces.SRP = On;
    GMAT AllForces.RelativisticCorrection = Off;
    GMAT AllForces.ErrorControl = RSSStep;
    GMAT AllForces.GravityField.Earth.Degree = 20;
    GMAT AllForces.GravityField.Earth.Order = 20;
    GMAT AllForces.GravityField.Earth.StmLimit = 100;
    GMAT AllForces.GravityField.Earth.PotentialFile = 'JGM2.cof';
    GMAT AllForces.GravityField.Earth.TideModel = 'None';
    GMAT AllForces.SRP.Flux = 1367;
    GMAT AllForces.SRP.SRPModel = Spherical;
    GMAT AllForces.SRP.Nominal_Sun = 149597870.691;
    GMAT AllForces.Drag.AtmosphereModel = MSISE90;
    GMAT AllForces.Drag.HistoricWeatherSource = 'ConstantFluxAndGeoMag';
    GMAT AllForces.Drag.PredictedWeatherSource = 'ConstantFluxAndGeoMag';
    GMAT AllForces.Drag.CSSISpaceWeatherFile = '../samples/SupportFiles/CSSI_2004To2026.txt';
    GMAT AllForces.Drag.SchattenFile = 'SchattenPredict.txt';
    GMAT AllForces.Drag.F107 = 150;
    GMAT AllForces.Drag.F107A = 150;
    GMAT AllForces.Drag.MagneticIndex = 3;
    GMAT AllForces.Drag.SchattenErrorModel = 'Nominal';
    GMAT AllForces.Drag.SchattenTimingModel = 'NominalCycle';
    GMAT AllForces.Drag.DragModel = 'Spherical';
    ```

## Propagate until periapse

=== "Nyx (Rust)"

    ``` rust
    // Propagate until periapse
    let prop = Propagator::default(sc_dyn);

    let (out, traj) = prop
        .with(sat)
        .until_event(0.5 * TimeUnit::Day, &Event::periapsis(), 0)
        .unwrap();
    ```

=== "Nyx (CLI)"
    _TODO_ in version beta-2.

=== "GMAT"

    ``` matlab
    Create Propagator EarthFull;
    GMAT EarthFull.FM = AllForces;
    GMAT EarthFull.Type = RungeKutta89;
    GMAT EarthFull.InitialStepSize = 60;
    GMAT EarthFull.Accuracy = 9.999999999999999e-12;
    GMAT EarthFull.MinStep = 0.001;
    GMAT EarthFull.MaxStep = 45000;
    GMAT EarthFull.MaxStepAttempts = 50;
    GMAT EarthFull.StopIfAccuracyIsViolated = true;

    % (...)

    BeginMissionSequence;

    %------------------------------
    %  Propagate to Earth periapsis
    %------------------------------
    
    Propagate 'Prop to Perigee' EarthFull(Sat) {Sat.Periapsis};

    % (...)
    ```

[^1]: If this footnote still exists, then the TOML setup hasn't yet been added to this tutorial. I'm currently reworking how the TOML is handled.

--8<-- "includes/Abbreviations.md"