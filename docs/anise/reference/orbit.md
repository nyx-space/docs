# Orbit and State Reference

In ANISE, an `Orbit` represents the full state of an object at a specific time within a specific coordinate frame.

## The `Orbit` Struct

An `Orbit` consists of:

- **State Vector**: Position and Velocity ($\mathbf{r}, \mathbf{v}$).
- **Epoch**: The time at which the state is defined (using `hifitime`).
- **Frame**: The reference frame in which the vectors are expressed.

## Initialization

You can initialize an `Orbit` from various representations, including with the following initializers. Refer to <https://docs.rs/anise/latest/anise/astro/orbit/type.Orbit.html> for the exhaustive list, which includes Keplerian altitudes, Keplerian apses radii, Keplerian mean anomaly, etc.

### Cartesian
`Orbit::cartesian(x, y, z, vx, vy, vz, epoch, frame)`
Directly sets the position and velocity in km and km/s.

### Keplerian
`Orbit::keplerian(sma, ecc, inc, raan, aop, true_anomaly, epoch, frame)`
Calculates the state from classical orbital elements.
- **Note**: Requires the frame to have a defined gravitational parameter ($\mu$).

### Geodetic / LatLongAlt
`Orbit::try_latlongalt(lat, lon, alt, epoch, frame)`
Defines a state relative to a body's surface. Useful for ground stations.

## Common Operations

### `transform_to`
`almanac.transform_to(orbit, target_frame, aberration)`
Returns a new `Orbit` expressed in the `target_frame`. This accounts for both translation and rotation of the frames.

### Orbital Elements

You can extract orbital elements from an `Orbit` object:

- `sma_km()`, `ecc()`, `inc_deg()`, `raan_deg()`, `aop_deg()`, `ta_deg()`
- **Other Anomalies**: `ma_deg()` (Mean Anomaly), `ea_deg()` (Eccentric Anomaly).
- **Other Parameters**: `periapsis_km()`, `apoapsis_km()`, `hmag()` (Specific Angular Momentum).
- **Python**: Accessible as methods (e.g., `orbit.sma_km()`).


### Propagation (Two-Body)

ANISE provides basic two-body propagation for quick estimates:

- `at_epoch(new_epoch)`: Propagates the orbit to a new time using Keplerian motion.
- **Warning**: For high-fidelity propagation including J2, solar radiation pressure, etc., use a dedicated propagator like those found in the `Nyx` library.
