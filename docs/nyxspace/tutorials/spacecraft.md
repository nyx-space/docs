# Spacecraft Definition

This tutorial explores the basic definitions of spacecraft, including properties like mass, drag, solar radiation pressure (SRP), and defining dispersed spacecraft for Monte Carlo simulations.

## Defining a Spacecraft

```python
from nyx_space import DragData, Mass, Spacecraft, SRPData
from nyx_space.anise import MetaAlmanac
from nyx_space.anise.analysis import OrbitalElement
from nyx_space.anise.astro import Orbit
from nyx_space.anise.constants import Frames
from nyx_space.anise.time import Epoch
from nyx_space.monte_carlo import MvnSpacecraft, StateDispersion, StateParameter

almanac = MetaAlmanac.latest()
eme2k = almanac.frame_info(Frames.EME2000)

# Define an orbit
orbit = Orbit.from_keplerian(
    6800.0, 1e-4, 45.0, 60.0, 75.0, 90.0, Epoch("2020-02-29 01:02:03 TDB"), eme2k
)

# A simple spacecraft with just an orbit
sc = Spacecraft(orbit)

# A spacecraft with defined mass (in kg)
sc_mass = Spacecraft(orbit, Mass(123.0))

# A spacecraft with mass, SRP (area, coefficient of reflectivity), and Drag (area, drag coefficient)
sc_mass_srp_drag = Spacecraft(
    orbit, Mass(123.0), SRPData(10.0, 1.2), DragData(10.0, 2.0)
)

# Test serialization and deserialization to ASN1 format
sc_mass2 = Spacecraft.from_asn1(sc_mass.to_asn1())
sc_mass_srp_drag2 = Spacecraft.from_asn1(sc_mass_srp_drag.to_asn1())
```

## Multivariate Normal Spacecraft

Nyx supports defining dispersions for Monte Carlo simulations using a multivariate normal distribution.

```python
# Define state dispersions
disp = [
    StateDispersion.zero_mean(
        StateParameter.Element(OrbitalElement.SemiMajorAxis), 15.0
    ),
    StateDispersion.zero_mean(StateParameter.Element(OrbitalElement.RAAN), 5.0),
]

# Create a Multivariate Normal Spacecraft
mvn = MvnSpacecraft(sc, disp)

# Sample 1000 dispersed spacecraft based on the defined distributions
dispersed = mvn.sample(1000, 123)
```
