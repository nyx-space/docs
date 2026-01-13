# Instrument Kernels

Instrument Kernels allow you to define sensors, cameras, and antennas attached to a spacecraft.

## The `Instrument` Object

An `Instrument` defines the sensor's geometry relative to the spacecraft bus.

### Mounting
The mounting is defined by a rigid transformation from the **Spacecraft Body Frame** to the **Instrument Frame**.
- **`q_to_i`**: A quaternion (rotation) describing the orientation.
- **`offset_i`**: A translation vector (lever arm) from the spacecraft center of mass to the sensor origin.

### Field of View (FOV)
The FOV defines the sensitive volume of the instrument.
- **Conical**: Circular FOV (e.g., dish antennas, LIDARs). Defined by a `half_angle_deg`.
- **Rectangular**: Box FOV (e.g., camera sensors). Defined by `x_half_angle_deg` (Width) and `y_half_angle_deg` (Height). Assumes the boresight is +Z.

## Functionality

### FOV Margin
ANISE can compute the **FOV Margin**, which is the angle between the target and the nearest FOV boundary.
- **Positive**: Target is inside.
- **Negative**: Target is outside.
- **Zero**: Target is exactly on the edge.

This property is continuous, making it suitable for the **Analysis Engine's** event finder. You can solve for `margin = 0` to find exact entry/exit times.

### Footprints
The `footprint` method projects the FOV boundary onto a target planetary body (Ellipsoid).
- Raycasts the FOV edges.
- Intersects with the target shape.
- Returns a list of points (lat/lon/alt) forming the polygon of the footprint on the surface.

This accounts for the full chain:
`Inertial -> Spacecraft Body -> Instrument -> Ray -> Target Inertial -> Target Fixed`.
