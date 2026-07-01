# Mission Design

This tutorial demonstrates how to configure propagators, handle perturbations like atmospheric drag and solar radiation pressure (SRP), use spherical harmonics, and perform simple Monte Carlo propagations in Nyx.

## Propagate with Perturbations

Here is a guide on how to propagate a spacecraft's orbit over time while accounting for Solar Radiation Pressure (SRP) and atmospheric drag. Note that this demonstrates simple propagation segments, not the more complex sequencing available in Nyx Premium.

```python
import logging
from nyx_space import DragData, ExportCfg, Mass, Spacecraft, SRPData
from nyx_space.anise import MetaAlmanac
from nyx_space.anise.analysis import Condition, Event, OrbitalElement, ScalarExpr
from nyx_space.anise.astro import Orbit
from nyx_space.anise.constants import CelestialObjects, Frames
from nyx_space.mission_design import (
    AccelModels,
    AtmDensity,
    Drag,
    Dynamics,
    ForceModels,
    GravityFieldConfig,
    IntegratorMethod,
    IntegratorOptions,
    PointMasses,
    Propagator,
    SolarPressure,
)
from nyx_space.monte_carlo import MvnSpacecraft, StateDispersion, StateParameter
from nyx_space.time import Duration, Epoch, Unit

# Step 1: Define Integrator Options
# We default to a variable step integrator. This ensures numerical accuracy
# without wasting CPU cycles on regions of the orbit where dynamics change slowly.
opts = IntegratorOptions()

# Step 2: Define the Environment
# Define which celestial bodies exert a point-mass gravitational pull.
accel_models = AccelModels(
    point_masses=PointMasses(
        celestial_objects=[
            CelestialObjects.EARTH,
            CelestialObjects.MOON,
            CelestialObjects.SUN,
        ]
    )
)

# Step 3: Configure Non-Gravitational Force Models
almanac = MetaAlmanac.latest()

# Define Atmospheric Drag. We use the MSIS-00 empirical atmosphere model.
drag = Drag(AtmDensity.msis00())

# Define Solar Radiation Pressure (SRP).
# We configure this to account for eclipses cast by the Earth and the Moon.
srp = SolarPressure(
    [Frames.EARTH_J2000, Frames.MOON_J2000], almanac, estimate=False
)
force_models = ForceModels(drag=drag, srp=srp)

# Step 4: Assemble the Dynamics
# The dynamics aggregate the gravitational and non-gravitational models.
dynamics = Dynamics(accel_models, force_models)

# Initialize the propagator with the defined dynamics and the Runge-Kutta 8(9) integrator.
# The Almanac provides the necessary ephemerides for the celestial bodies and frame transformations.
propagator = Propagator(dynamics, almanac, IntegratorMethod.RungeKutta89, opts)

# Step 5: Define the Initial Spacecraft State
eme2k = almanac.frame_info(Frames.EME2000)
orbit = Orbit.from_keplerian(
    sma_km=6800.0,
    ecc=1e-4,
    inc_deg=45.0,
    raan_deg=60.0,
    aop_deg=75.0,
    ta_deg=90.0,
    epoch=Epoch("2030-12-29 01:02:03 TDB"),
    frame=eme2k,
)

# Define the physical characteristics of the spacecraft necessary to compute drag and SRP.
my_sc = Spacecraft(
    orbit,
    Mass(dry_mass_kg=123.0),
    SRPData(area_m2=10.0, coeff_reflectivity=1.2),
    DragData(area_m2=10.0, coeff_drag=2.0),
)

# Step 6: Execute Propagations
# Scenario A: Propagate until a specific temporal epoch.
target_epoch = Epoch("2030-12-30 01:02:03 UTC")
result_epoch = propagator.until_epoch(my_sc, target_epoch, trajectory=True)

# The trajectory may be converted to an ANISE Ephemeris, e.g. for serialization to a BSP/OEM file.
ephem = result_epoch.trajectory.to_ephemeris("MySpacecraftTraj", ExportCfg())

# Scenario B: Propagate until a specific orbital event (apoapsis).
# This demonstrates the root-finding capabilities of Nyx to stop exactly at an event.
result_event = propagator.until_event(
    my_sc, Event.apoapsis(), max_duration=Duration("1 day")
)
```

## Configure Spherical Harmonics

This example configures a high-fidelity spherical harmonic gravity field model for precise near-Earth propagation.

```python
# Assuming 'almanac' is loaded
eme2k = almanac.frame_info(Frames.EME2000)

# Define a low-Earth orbit using Cartesian state vectors
orbit = Orbit(
    5442.1625926801835,
    -4068.9498468206248,
    -13.456851447751518,
    2.8581975428173836,
    3.8097859312745794,
    6.002126693122689,
    Epoch("2025-08-25 11:55:44 UTC"),
    eme2k,
)
spacecraft = Spacecraft(orbit)

# Step 1: Define the Gravity Field Configuration
# We apply the EGM2008 gravity model (degree 10, order 10).
# The frame must be Earth-fixed (e.g., ITRF93) for the field to rotate with the planet.
accel_models = AccelModels(
    point_masses=PointMasses(
        celestial_objects=[CelestialObjects.MOON, CelestialObjects.SUN]
    ),
    gravity_field=GravityFieldConfig(
        degree=10,
        order=10,
        filepath="../data/01_planetary/EGM2008_to2190_TideFree.gz",
        frame=Frames.EARTH_ITRF93.to_frameuid(),
    ),
)

# Step 2: Propagate
# For high-precision gravity fields, Dormand-Prince 7-8 is a robust choice.
dynamics = Dynamics(accel_models)
propagator = Propagator(dynamics, almanac, IntegratorMethod.DormandPrince78)

final_state = propagator.for_duration(spacecraft, Unit.Day * 1)
```

## Execute Simple Monte Carlo

Generate a multi-variate dispersion of initial orbital states and propagate them in parallel to analyze trajectory divergence.

```python
import polars as pl

# Define the multivariate normal dispersion
disp = [
    StateDispersion.zero_mean(
        StateParameter.Element(OrbitalElement.SemiMajorAxis), 15.0
    ),
    StateDispersion.zero_mean(
        StateParameter.Element(OrbitalElement.Eccentricity), 1e-6
    ),
]

# Generate dispersed variants based on the distributions
mvn = MvnSpacecraft(spacecraft, disp)
dispersed_spacecraft = mvn.sample(100, seed=123)

# Configure the propagator
accel_models = AccelModels(
    point_masses=PointMasses(
        celestial_objects=[CelestialObjects.EARTH, CelestialObjects.MOON]
    ),
)
srp = SolarPressure([Frames.EARTH_J2000], almanac, estimate=False)
dynamics = Dynamics(accel_models, force_models=ForceModels(srp))
propagator = Propagator(dynamics, almanac, IntegratorMethod.RungeKutta89)

# Execute the single segment Monte Carlo
# Propagate each spacecraft until it hits its 25th occurrence of Local Solar Time equaling 6.0 hours.
results = propagator.many_until_event(
    dispersed_spacecraft,
    Event(ScalarExpr.LocalSolarTime(), Condition.Equals(6.0), Duration("1 ms")),
    trajectory=False,
    trigger=25,
    max_duration=Duration("1 day"),
)

# Analyze Results
df_data = {"Epoch (UTC)": [], "LTAN (deg)": []}
for rslt in results:
    df_data["Epoch (UTC)"] += [rslt.state.orbit.epoch.to_datetime()]
    df_data["LTAN (deg)"] += [rslt.state.orbit.ltan_deg()]

df = pl.DataFrame(df_data)
print(df.describe())
```
