# Orbit Determination

This tutorial explains how to run tracking data through a scalar orbit determination filter to estimate a spacecraft's position, velocity, and coefficient of reflectivity.

## Executing an Orbit Determination Filter

```python
from nyx_space import ExportCfg, Spacecraft
from nyx_space.anise import MetaAlmanac
from nyx_space.anise.analysis import OrbitalElement
from nyx_space.anise.astro import Orbit
from nyx_space.anise.constants import CelestialObjects, Frames
from nyx_space.mission_design import (
    AccelModels,
    Dynamics,
    GravityFieldConfig,
    PointMasses,
    Propagator,
)
from nyx_space.monte_carlo import StateDispersion, StateParameter
from nyx_space.orbit_determination import (
    GroundStation,
    GroundTrackingArcSim,
    Handoff,
    KalmanVariant,
    LocalFrame,
    Location,
    MeasurementType,
    ProcessNoise,
    Scheduler,
    SigmaRejection,
    SpacecraftEstimate,
    SpacecraftODProcess,
    StochasticNoise,
    TrkConfig,
)
from nyx_space.time import Epoch, Unit

almanac = MetaAlmanac.latest()
eme2k = almanac.frame_info(Frames.EME2000)

# Step 1: Build a reference trajectory
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

# Step 2: Disperse this spacecraft state to create an initial filter error
disp = [
    StateDispersion.zero_mean(
        StateParameter.Element(OrbitalElement.SemiMajorAxis), 1.0
    ),
    StateDispersion.zero_mean(
        StateParameter.Element(OrbitalElement.Eccentricity), 1e-6
    ),
]

# Builds a zero mean estimate from these dispersions
estimate = SpacecraftEstimate.from_dispersions(
    nominal_state=spacecraft, dispersions=disp, seed=123
)

# Propagate to generate the ground-truth trajectory.
accel_models = AccelModels(
    point_masses=PointMasses(
        celestial_objects=[CelestialObjects.MOON, CelestialObjects.SUN]
    ),
    gravity_field=GravityFieldConfig(
        degree=10,
        order=10,
        filepath="../data/01_planetary/EGM2008_to2190_TideFree.gz",
        frame=Frames.IAU_EARTH_FRAME.to_frameuid(),
    ),
)
dynamics = Dynamics(accel_models)
propagator = Propagator(dynamics, almanac)
traj = propagator.for_duration(spacecraft, Unit.Day * 1, trajectory=True).trajectory

# Step 3: Configure Stochastic Measurement Noise, generate tracking data.
stochastic_noises = {
    MeasurementType.Range: StochasticNoise(name="Range"),
    MeasurementType.Doppler: StochasticNoise(name="Doppler"),
}

# Step 4: Build the ground station network
gs0 = GroundStation(
    name="Paris, FR",
    location=Location(
        latitude_deg=48.8566,
        longitude_deg=2.3522,
        height_km=0.4,
        frame=Frames.IAU_EARTH_FRAME.to_frameuid(),
        terrain_mask=[],
        terrain_mask_ignored=True,
    ),
    stochastic_noises=stochastic_noises,
)

gs1 = GroundStation(
    "Denver, CO",
    Location(
        39.7420, -104.9915, 1.8, Frames.IAU_EARTH_FRAME.to_frameuid(), [], True
    ),
    stochastic_noises,
)

# Step 5: Define Tracking Schedules
configs = {
    "Paris, FR": TrkConfig(Scheduler(Handoff.Greedy)),
    "Denver, CO": TrkConfig(Scheduler(Handoff.Greedy)),
}

network = {"Paris, FR": gs0, "Denver, CO": gs1}
trk_sim = GroundTrackingArcSim(network, traj, configs)
trk_sim.build_schedule(almanac)

# Step 6: Generate synthetic measurements
trk_arc = trk_sim.generate_measurements(almanac)

# Step 7: Run the orbit determination filter
od_proc_deviation = SpacecraftODProcess(
    propagator, KalmanVariant.DeviationTracking, network
)
od_dev_sol = od_proc_deviation.process_arc(estimate, trk_arc)

# Export the whole orbit determination solution into a single Parquet file.
od_dev_sol.to_parquet("od_dev.pq", ExportCfg(False))

# Step 8: Running the smoother
smoothed = od_dev_sol.smooth(almanac)

# Reference update algorithm setup
process_noise = ProcessNoise.from_velocity_m_s(
    vx_m_s=1e-6,
    vy_m_s=1e-6,
    vz_m_s=1e-6,
    noise_duration=Unit.Second * 1,
    disable_time=Unit.Hour * 2,
    local_frame=LocalFrame.Inertial,
)
od_proc = SpacecraftODProcess(
    propagator, KalmanVariant.ReferenceUpdate, network, process_noise=process_noise
)
od_sol = od_proc.process_arc(estimate, trk_arc)
od_sol.to_parquet("od_ref_update.pq", ExportCfg(False))

# Export definitive ephemeris to OEM
definitive_ephem = od_sol.to_ephemeris("Test OD Spacecraft")
oem_filepath = "definitive_ephem.oem"
definitive_ephem.write_ccsds_oem(oem_filepath)
```
