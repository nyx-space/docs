# Location Kernels

Location Kernels (`.lka` files) allow you to define ground stations, observatories, or other points of interest on the surface of a celestial body.

## The `Location` Object

A location is defined by its geodetic coordinates:

- `latitude_deg`: Geodetic latitude.
- `longitude_deg`: Geodetic longitude (positive East).
- `height_km`: Altitude above the reference ellipsoid.
- `frame`: The central body frame (e.g., `ITRF93` for Earth, `IAU_MOON` for Moon).

## Terrain Masks

Real-world ground stations do not have a perfect 0-degree horizon. Mountains or buildings may obstruct the view.
ANISE supports **Terrain Masks** to account for this.

A `TerrainMask` is a list of Azimuth/Elevation pairs.
- **Azimuth**: The start of the mask segment.
- **Elevation**: The minimum elevation required for visibility in that segment.

If a mask is provided, `ElevationFromLocation` computations will account for it, and visibility searches will use it as the "horizon" limit.

## Working with `.lka` Files

ANISE uses a custom Dhall-based or binary format for loading locations.

### Loading (Rust/Python)

```python
# Python
almanac = Almanac("de440.bsp").load("dsn_stations.lka")

# Now you can reference locations by ID or Name
azel = almanac.azimuth_elevation_range_sez_from_location_name(
    orbit_state,
    "DSS-65"
)
```

### Creating (Python)

You can create location files programmatically:

```python
from anise.astro import Location, TerrainMask, FrameUid

# Define a mask
mask = [TerrainMask(0.0, 5.0), TerrainMask(180.0, 10.0)]

# Create location
dss65 = Location(
    latitude_deg=40.427,
    longitude_deg=4.250,
    height_km=0.834,
    frame=FrameUid(399, 399), # Earth
    terrain_mask=mask,
    terrain_mask_ignored=False
)

# Export
entry = LocationDhallSetEntry(dss65, id=65, alias="DSS-65")
dhallset = LocationDhallSet([entry])
dhallset.to_dataset().save_as("my_locations.lka", True)
```
