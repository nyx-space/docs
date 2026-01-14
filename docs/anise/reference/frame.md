# Frame Reference

Frames define the coordinate systems used for all calculations in ANISE. Every position, velocity, and rotation is defined with respect to a specific Frame.

## Frame Identification

ANISE is compatible with the standard NAIF ID system. You can refer to frames using:

1. **Integer IDs**: e.g., `399` for Earth.
2. **Predefined Constants**: e.g., `anise::constants::frames::EARTH_J2000`.
3. **Names**: In some interfaces (like Python), strings can be used if they have been registered in the `Almanac`.

## Frame Safety

The `Frame` object in ANISE is more than just an ID; it's a validated descriptor. When you create an `Orbit`, it is "tagged" with a `Frame`.

```rust
let frame = almanac.frame_info(EARTH_J2000)?;
let orbit = Orbit::cartesian(x, y, z, vx, vy, vz, epoch, frame);
```

If you attempt to perform a math operation between two orbits in different frames, ANISE will either:

- **Automatic Transform**: Some APIs will automatically transform the state to a common frame if the `Almanac` is provided.
- **Error**: If no `Almanac` is provided to resolve the relationship, ANISE will refuse to perform the operation to prevent physical errors.

## Metadata

A `Frame` object retrieved via `almanac.frame_info()` contains data retrieved from the loaded datasets (SPK, PCK, BPC):

- **`mu_km3_s2`**: The gravitational parameter ($GM$) of the center body in $km^3/s^2$.
- **`shape`**: A tri-axial `Ellipsoid` defining the body's semi-major, semi-minor, and polar radii. It provides methods for surface intersection testing and calculating lighting angles (emission, solar incidence).
- **`ephemeris_id`**: The NAIF ID used for translation and trajectory lookups.
- **`orientation_id`**: The NAIF ID used for rotation lookups.

### Orientation and Phase Angles

For planetocentric (body-fixed) frames, ANISE uses the loaded PCK or BPC data to determine the body's orientation. This is defined by three key phase angles:

1. **Right Ascension (RA)** of the body's north pole.
2. **Declination (Dec)** of the body's north pole.
3. **Prime Meridian (W)** location at the given epoch.

These angles are often modeled as polynomials in time (e.g., $RA = RA_0 + RA_1 \Delta t + RA_2 \Delta t^2 \dots$). ANISE evaluates these to compute the exact rotation matrix between inertial and body-fixed frames.

