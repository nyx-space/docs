# Almanac Reference

The `Almanac` is the primary interface for ANISE. It serves as the context for all ephemeris, orientation, and physical constant lookups.

The following is a _small subset_ of all the functions available in the Almanac. Please refer to <https://docs.rs/anise/latest/anise/almanac/struct.Almanac.html> for the exhaustive list: Python functions are (almost) always named identically.

## Key Concepts

- **Thread Safety**: The `Almanac` is `Send + Sync`, meaning it can be safely shared across threads.
- **Data Encapsulation**: It stores loaded kernel data internally; there is no global pool.
- **Method Chaining**: Loading methods often use a builder pattern or return a new handle for easy initialization.

## Loading Data

The `Almanac` supports loading various kernel types. You can load files directly or allow ANISE to "guess" the file type.

### `load`
Loads any supported ANISE or SPICE file.
- **Rust**: `almanac.load("path/to/file")?`
- **Python**: `almanac.load("path/to/file")`

### Specialized Loaders
If you know the file type, you can use specialized loaders for better performance or specific configuration:
- `with_spk(spk)`: Add SPK (ephemeris) data.
- `with_bpc(bpc)`: Add BPC (high-precision orientation) data.
- `with_planetary_data(pca)`: Add an ANISE planetary constant data kernel (gravity and tri-axial ellipsoid constants and low-fidelity orientation).
- `with_location_data(lka)`: Add an ANISE location data kernel (landmarks defined by their latitude, longitude, and height above the ellipsoid on a given body fixed frame).
- `with_instrument_data(ika)`: Add an ANISE instrument kernel (an instrument is defined by its rotation quaternion/EP, its offset from the body center, and its field of view).

## Coordinate Transformations

The most common use of the `Almanac` is to transform positions and velocities between frames.

### `transform_to`
Transforms an `Orbit` (state vector) into a different frame at its own epoch.
- **Parameters**: `orbit`, `target_frame`, `aberration`.
- **Returns**: A new `Orbit` in the target frame.

### `translate`
Calculates the relative position and velocity between two frames.
- **Parameters**: `target`, `observer`, `epoch`, `aberration`.
- **Returns**: A `StateVector` (Position + Velocity).

### `rotate`
Calculates the rotation (DCM) from one orientation frame to another.
- **Parameters**: `target`, `observer`, `epoch`.
- **Returns**: A 3x3 Direction Cosine Matrix.

## Physical Constants

The `Almanac` also stores physical data for bodies defined in the kernels.

### `frame_info`
Retrieves a `Frame` object containing metadata for a given NAIF ID.
- **Includes**: Gravitational parameter ($\mu$), body radii, and frame type.

### `angular_velocity_deg_s`
Returns the angular velocity vector in deg/s of the from_frame wrt to the to_frame.

## Built-in Constants

ANISE provides a set of common NAIF IDs and frames in the `constants` module for ease of use (e.g., `EARTH_J2000`, `SUN_J2000`, `MOON_J2000`).
