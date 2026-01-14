# Azimuth, Elevation, and Range (AER)

AER provides the relative orientation and distance between an observer (transmitter) and a target (receiver). In ANISE, this is typically computed from a ground station (`Location`) toward a spacecraft or another celestial body.

## The `AzElRange` Struct

This structure stores the result of an AER calculation.

- **`epoch`**: The time at which the calculation was performed.
- **`azimuth_deg`**: The horizontal angle from North (clockwise), between 0 and 360 degrees.
- **`elevation_deg`**: The angle above the horizon, between -180 and 180 degrees (typically -90 to 90).
- **`range_km`**: The Euclidean distance between the observer and the target.
- **`range_rate_km_s`**: The instantaneous speed along the line of sight (positive if moving away).
- **`light_time`**: The one-way light time (calculated as `range / c`).
- **`mask_deg`**: The elevation of the terrain mask at this azimuth.
- **`obstructed_by`**: If the view is blocked by a celestial body, this field identifies the body.

### Helper Methods
- `is_valid()`: Returns true if the range is $> 1$ mm and angles are finite.
- `is_obstructed()`: Returns true if there is a celestial obstruction or if the target is below the terrain mask.
- `elevation_above_mask_deg()`: Returns the difference between the target's elevation and the local terrain mask elevation.

## Almanac Functions

The `Almanac` provides several functions to compute AER:

| Function | Description |
| :--- | :--- |
| `azimuth_elevation_range_sez` | Computes AER between two `Orbit` objects. |
| `azimuth_elevation_range_sez_from_location` | Computes AER using a `Location` object as the transmitter. |
| `azimuth_elevation_range_sez_from_location_id` | Uses a location ID from a loaded Location Kernel. |
| `azimuth_elevation_range_sez_from_location_name` | Uses a location name (alias) from a loaded Location Kernel. |

## Mathematical Implementation

ANISE follows the algorithm described in **Vallado, Section 4.4.3** for SEZ (South-East-Zenith) coordinate transformations.

### 1. Line-of-Sight Calculation
If an `obstructing_body` is provided, ANISE first performs an ellipsoid intersection test. A line segment is drawn from the transmitter to the receiver. If this segment intersects the body's tri-axial ellipsoid, the `obstructed_by` field is populated, and the calculation reflects the obstruction.

### 2. SEZ Frame Transformation

The transmitter's state is used to define a local **SEZ frame**:

- **Zenith (Z)**: Normal to the reference ellipsoid at the transmitter's location.
- **South (S)**: Points toward the South pole of the central body.
- **East (E)**: Completes the right-handed system ($E = Z \times S$).

### 3. Coordinate Rotation
Both the transmitter ($\mathbf{r}_{tx}$) and receiver ($\mathbf{r}_{rx}$) position vectors are rotated into this SEZ frame. The relative vector is computed as:
$$\boldsymbol{\rho}_{sez} = \mathbf{r}_{rx\_sez} - \mathbf{r}_{tx\_sez}$$

### 4. Angle Computation

- **Range**: $\rho = \|\boldsymbol{\rho}_{sez}\|$
- **Elevation**: $\phi = \arcsin\left(\frac{\rho_z}{\rho}\right)$
- **Azimuth**: $A = \operatorname{atan2}(\rho_y, -\rho_x)$

The range-rate $\dot{\rho}$ is computed by projecting the relative velocity vector onto the unit line-of-sight vector:
$$\dot{\rho} = \frac{\boldsymbol{\rho} \cdot \mathbf{v}_{rel}}{\rho}$$

## Testing and Validation

### Rust Tests
Validated in `anise/src/almanac/aer.rs`:
- `verif_edge_case`: Ensures stability when transmitter and receiver are at the same location.
- `gmat_verif`: Validates range and range-rate results against GMAT (General Mission Analysis Tool) for DSN station Madrid.

### Python Tests
Validated in `anise-py/tests/test_analysis.py`:
- `test_location_accesses`: Demonstrates building a location kernel, loading it, and calculating visibility/AER for the Lunar Reconnaissance Orbiter (LRO).
- The `report_visibility_arcs` function uses these computations to determine contact windows.
