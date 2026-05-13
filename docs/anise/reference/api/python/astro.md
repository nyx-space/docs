---
description: |
    API documentation for modules: anise.astro.

lang: en

classoption: oneside
geometry: margin=1in
papersize: a4

linkcolor: blue
links-as-notes: true
...


# Module `anise.astro` {#anise.astro}


## Classes


### Class `AzElRange` {#anise.astro.AzElRange}

>     class AzElRange(
>         epoch,
>         azimuth_deg,
>         elevation_deg,
>         range_km,
>         range_rate_km_s,
>         obstructed_by=None,
>         mask_deg=None
>     )

A structure that stores the result of Azimuth, Elevation, Range, Range rate calculation.

:type epoch: Epoch
:type azimuth_deg: float
:type elevation_deg: float
:type range_km: float
:type range_rate_km_s: float
:type obstructed_by: Frame, optional
:type mask_deg: float, optional
:rtype: AzElRange


#### Instance variables


##### Variable `azimuth_deg` {#anise.astro.AzElRange.azimuth_deg}

:rtype: float


##### Variable `elevation_deg` {#anise.astro.AzElRange.elevation_deg}

:rtype: float


##### Variable `epoch` {#anise.astro.AzElRange.epoch}

:rtype: Epoch


##### Variable `light_time` {#anise.astro.AzElRange.light_time}

:rtype: Duration


##### Variable `mask_deg` {#anise.astro.AzElRange.mask_deg}

:rtype: float


##### Variable `obstructed_by` {#anise.astro.AzElRange.obstructed_by}

:rtype: Frame


##### Variable `range_km` {#anise.astro.AzElRange.range_km}

:rtype: float


##### Variable `range_rate_km_s` {#anise.astro.AzElRange.range_rate_km_s}

:rtype: float


#### Methods


##### Method `elevation_above_mask_deg` {#anise.astro.AzElRange.elevation_above_mask_deg}

>     def elevation_above_mask_deg(
>         self,
>         /
>     )

Returns the elevation above the terrain mask for this azimuth, in degrees.
If the terrain mask was zero at this azimuth, then the elevation above mask is equal to the elevation_deg field.

:rtype: float


##### Method `is_obstructed` {#anise.astro.AzElRange.is_obstructed}

>     def is_obstructed(
>         self,
>         /
>     )

Returns whether there is an obstruction.

:rtype: bool


##### Method `is_valid` {#anise.astro.AzElRange.is_valid}

>     def is_valid(
>         self,
>         /
>     )

Returns false if the range is less than one millimeter, or any of the angles are NaN.

:rtype: bool


### Class `Covariance` {#anise.astro.Covariance}

>     class Covariance(
>         covar,
>         local_frame
>     )


#### Instance variables


##### Variable `matrix` {#anise.astro.Covariance.matrix}

Returns the 6x6 DCM to rotate a state. If the time derivative of this DCM is defined, this 6x6 accounts for the transport theorem.
Warning: you MUST manually install numpy to call this function.
:rtype: numpy.ndarray


### Class `DataType` {#anise.astro.DataType}

>     class DataType


#### Class variables


##### Variable `Type10SpaceCommandTLE` {#anise.astro.DataType.Type10SpaceCommandTLE}


##### Variable `Type12HermiteEqualStep` {#anise.astro.DataType.Type12HermiteEqualStep}


##### Variable `Type13HermiteUnequalStep` {#anise.astro.DataType.Type13HermiteUnequalStep}


##### Variable `Type14ChebyshevUnequalStep` {#anise.astro.DataType.Type14ChebyshevUnequalStep}


##### Variable `Type15PrecessingConics` {#anise.astro.DataType.Type15PrecessingConics}


##### Variable `Type17Equinoctial` {#anise.astro.DataType.Type17Equinoctial}


##### Variable `Type18ESOCHermiteLagrange` {#anise.astro.DataType.Type18ESOCHermiteLagrange}


##### Variable `Type19ESOCPiecewise` {#anise.astro.DataType.Type19ESOCPiecewise}


##### Variable `Type1ModifiedDifferenceArray` {#anise.astro.DataType.Type1ModifiedDifferenceArray}


##### Variable `Type20ChebyshevDerivative` {#anise.astro.DataType.Type20ChebyshevDerivative}


##### Variable `Type21ExtendedModifiedDifferenceArray` {#anise.astro.DataType.Type21ExtendedModifiedDifferenceArray}


##### Variable `Type2ChebyshevTriplet` {#anise.astro.DataType.Type2ChebyshevTriplet}


##### Variable `Type3ChebyshevSextuplet` {#anise.astro.DataType.Type3ChebyshevSextuplet}


##### Variable `Type5DiscreteStates` {#anise.astro.DataType.Type5DiscreteStates}


##### Variable `Type8LagrangeEqualStep` {#anise.astro.DataType.Type8LagrangeEqualStep}


##### Variable `Type9LagrangeUnequalStep` {#anise.astro.DataType.Type9LagrangeUnequalStep}


### Class `DragData` {#anise.astro.DragData}

>     class DragData(
>         area_m2,
>         coeff_drag=None
>     )


#### Instance variables


##### Variable `area_m2` {#anise.astro.DragData.area_m2}

Atmospheric drag area in m^2 -- default 0.0
:rtype: float


##### Variable `coeff_drag` {#anise.astro.DragData.coeff_drag}

Drag coefficient (C_d) -- default 2.2
:rtype: float


#### Methods


##### Method `from_asn1` {#anise.astro.DragData.from_asn1}

>     def from_asn1(
>         data
>     )

Decodes an ASN.1 DER encoded byte array into a DragData object.

:type data: bytes
:rtype: DragData


##### Method `to_asn1` {#anise.astro.DragData.to_asn1}

>     def to_asn1(
>         self,
>         /
>     )

Encodes this DragData object into an ASN.1 DER encoded byte array.

:rtype: bytes


### Class `DynamicFrame` {#anise.astro.DynamicFrame}

>     class DynamicFrame

Dynamic frames in ANISE are encoded as a packed integer within the frame's orientation ID.

### Encoding format

The identifier is a 32-bit signed integer packed as four bytes:
```text
  0xA0 FF AA BB
```
Where:

 - <code>0xA0</code>: ANISE dynamic frame prefix.
 - <code>FF</code>: Frame family identifier (e.g., Earth Mean of Date, Body True of Date).
 - <code>AA</code>: Primary payload (e.g., precession model for Earth frames, or the high byte of a source ID).
 - <code>BB</code>: Secondary payload (e.g., nutation model for Earth frames, or the low byte of a source ID).

### Frame families

```text
  0xA0 E0 AA 00   Earth Mean Equator, Mean Equinox of Date (MOD)
  0xA0 E1 AA BB   Earth True Equator, True Equinox of Date (TOD)
  0xA0 E2 AA BB   Earth True Equator, Mean Equinox of Date (TEME)

  0xA0 B0 SS SS   Body Mean of Date
  0xA0 B1 SS SS   Body True of Date
```

The `E*` families are Earth-specific models. The `B*` families are generic celestial-body pole models.

### Earth payload

For Earth frames, <code>AA</code> encodes the precession / bias-precession model:

```text
  0x00   IAU 1976 / FK5 precession
  0x01   IAU 2000 precession-bias model
  0x03   IAU 2006 precession-bias model
```

*(Note: <code>0x02</code> is intentionally reserved and unused).*

For Earth TOD and TEME frames, <code>BB</code> encodes the nutation model:

```text
  0x00   IAU 1980 nutation
  0x01   IAU 2000A nutation
  0x02   IAU 2000B nutation
  0x03   IAU 2006 / 2000A-compatible nutation
```

For Earth MOD frames, <code>BB</code> is reserved and must strictly be <code>0x00</code>.

Earth MOD uses the selected precession model only. Earth TOD composes the selected precession and nutation models.
Earth TEME first builds the corresponding true-equator/true-equinox frame, then rotates about the true Z-axis by the equation of the equinoxes to replace the true equinox with the mean equinox.

For Earth TEME, the equation of the equinoxes model is strictly derived from the selected nutation model:

```text
  IAU1980  -> EQEQ94
  IAU2000A -> EE00A
  IAU2000B -> EE00B
  IAU2006A  -> EE06A
```

This aligns with the SOFA/SOFARS sidereal-time identity:
`apparent sidereal time = mean sidereal time + equation of the equinoxes`.

### Body payload

For generic body frames, <code>AA BB</code> is interpreted as a single unsigned 16-bit source orientation ID:

```text
  source_id = u16::from_be_bytes([AA, BB])
```

While the public enum stores this as an <code>i32</code> for seamless integration with ANISE and NAIF ID routing, the compact bitmask fundamentally restricts the payload.
The source ID MUST be strictly positive and fall within the `0..=65535` range.

This perfectly accommodates standard celestial-body orientation IDs (e.g., <code>301</code> for the Moon, or <code>31001</code> for a lunar ME-style frame). **It cannot represent negative spacecraft IDs or deeply nested user-defined SPICE frames.**

**Warning:** Out-of-range body source IDs will fail silently via bitwise truncation. Callers must treat the <code>u16</code> bound as a strict mathematical contract.

Body TOD and MOD frames use the source orientation model solely to establish the body's pole direction. The source prime meridian (twist) angle is explicitly ignored.

- **Body True of Date** uses the full source pole model, inclusive of periodic trigonometric terms.
- **Body Mean of Date** uses the mean source pole model, zeroing out periodic trigonometric terms in the pole right ascension and declination.

For body TOD/MOD, the dynamic frame axes evaluate as follows via the same Euler rotations code at the PCK-defined IAU frames:

```text
  Z = source pole direction
  X = normalize(parent_Z × Z)
  Y = Z × X
```

If `parent_Z × Z` evaluates as singular (i.e., the pole aligns with the inertial Z-axis), the fallback perfectly mirrors the Ansys STK specification:

```text
  Y = normalize(Z × parent_X)
  X = Y × Z
```

### Interaction with <code>[Frame](#anise.astro.Frame "anise.astro.Frame")</code> fields

- `Frame::frozen_epoch`: If set, evaluates the dynamic models (precession, nutation, pole right ascension/declination) at the specified epoch rather than the integration time, freezing the frame inertially.
- `Frame::force_inertial`: If <code>true</code>, the time derivative of the resulting Direction Cosine Matrix (DCM) is explicitly zeroed out. The built-in Earth MOD/TOD constants are defined as inertial in the ANISE constants.


#### Descendants

* [anise.astro.DynamicFrame.BodyMeanOfDate](#anise.astro.DynamicFrame.BodyMeanOfDate)
* [anise.astro.DynamicFrame.BodyTrueOfDate](#anise.astro.DynamicFrame.BodyTrueOfDate)
* [anise.astro.DynamicFrame.EarthMeanOfDate](#anise.astro.DynamicFrame.EarthMeanOfDate)
* [anise.astro.DynamicFrame.EarthTrueEquatorMeanEquinox](#anise.astro.DynamicFrame.EarthTrueEquatorMeanEquinox)
* [anise.astro.DynamicFrame.EarthTrueOfDate](#anise.astro.DynamicFrame.EarthTrueOfDate)


#### Class variables


##### Variable `BodyMeanOfDate` {#anise.astro.DynamicFrame.BodyMeanOfDate}


##### Variable `BodyTrueOfDate` {#anise.astro.DynamicFrame.BodyTrueOfDate}


##### Variable `EarthMeanOfDate` {#anise.astro.DynamicFrame.EarthMeanOfDate}


##### Variable `EarthTrueEquatorMeanEquinox` {#anise.astro.DynamicFrame.EarthTrueEquatorMeanEquinox}


##### Variable `EarthTrueOfDate` {#anise.astro.DynamicFrame.EarthTrueOfDate}


#### Methods


##### Method `from_frame_id` {#anise.astro.DynamicFrame.from_frame_id}

>     def from_frame_id(
>         frame_id
>     )


##### Method `to_frame_id` {#anise.astro.DynamicFrame.to_frame_id}

>     def to_frame_id(
>         self,
>         /
>     )


### Class `EarthNutationModel` {#anise.astro.EarthNutationModel}

>     class EarthNutationModel


#### Class variables


##### Variable `IAU1980` {#anise.astro.EarthNutationModel.IAU1980}


##### Variable `IAU2000A` {#anise.astro.EarthNutationModel.IAU2000A}


##### Variable `IAU2000B` {#anise.astro.EarthNutationModel.IAU2000B}


##### Variable `IAU2006A` {#anise.astro.EarthNutationModel.IAU2006A}


### Class `EarthPrecessionModel` {#anise.astro.EarthPrecessionModel}

>     class EarthPrecessionModel


#### Class variables


##### Variable `IAU1976` {#anise.astro.EarthPrecessionModel.IAU1976}


##### Variable `IAU2000` {#anise.astro.EarthPrecessionModel.IAU2000}


##### Variable `IAU2006` {#anise.astro.EarthPrecessionModel.IAU2006}


### Class `Ellipsoid` {#anise.astro.Ellipsoid}

>     class Ellipsoid(
>         semi_major_equatorial_radius_km,
>         polar_radius_km=None,
>         semi_minor_equatorial_radius_km=None
>     )

Only the tri-axial Ellipsoid shape model is currently supported by ANISE.
This is directly inspired from SPICE PCK.
> For each body, three radii are listed: The first number is
> the largest equatorial radius (the length of the semi-axis
> containing the prime meridian), the second number is the smaller
> equatorial radius, and the third is the polar radius.

Example: Radii of the Earth.

   BODY399_RADII     = ( 6378.1366   6378.1366   6356.7519 )

:type semi_major_equatorial_radius_km: float
:type polar_radius_km: float, optional
:type semi_minor_equatorial_radius_km: float, optional
:rtype: Ellipsoid


#### Instance variables


##### Variable `polar_radius_km` {#anise.astro.Ellipsoid.polar_radius_km}

:rtype: float


##### Variable `semi_major_equatorial_radius_km` {#anise.astro.Ellipsoid.semi_major_equatorial_radius_km}

:rtype: float


##### Variable `semi_minor_equatorial_radius_km` {#anise.astro.Ellipsoid.semi_minor_equatorial_radius_km}

:rtype: float


#### Methods


##### Method `flattening` {#anise.astro.Ellipsoid.flattening}

>     def flattening(
>         self,
>         /
>     )

Returns the flattening ratio, computed from the mean equatorial radius and the polar radius

:rtype: float


##### Method `is_sphere` {#anise.astro.Ellipsoid.is_sphere}

>     def is_sphere(
>         self,
>         /
>     )

Returns true if the polar radius is equal to the semi minor radius.

:rtype: bool


##### Method `is_spheroid` {#anise.astro.Ellipsoid.is_spheroid}

>     def is_spheroid(
>         self,
>         /
>     )

Returns true if the semi major and minor radii are equal

:rtype: bool


##### Method `mean_equatorial_radius_km` {#anise.astro.Ellipsoid.mean_equatorial_radius_km}

>     def mean_equatorial_radius_km(
>         self,
>         /
>     )

Returns the mean equatorial radius in kilometers

:rtype: float


### Class `Ephemeris` {#anise.astro.Ephemeris}

>     class Ephemeris(
>         orbit_list,
>         object_id
>     )

Initializes a new Ephemeris from the list of Orbit instances and a given object ID.

In Python if you need to build an ephemeris with covariance, initialize with an empty list of
orbit instances and then insert each EphemerisRecord with covariance.

:type orbit_list: list
:type object_id: str


#### Instance variables


##### Variable `degree` {#anise.astro.Ephemeris.degree}

:rtype: int


##### Variable `interpolation` {#anise.astro.Ephemeris.interpolation}

:rtype: str


#### Methods


##### Method `at` {#anise.astro.Ephemeris.at}

>     def at(
>         self,
>         /,
>         epoch,
>         almanac
>     )

Interpolates the ephemeris state and covariance at the provided epoch.

##### Orbit Interpolation
The orbital state is interpolated using high-fidelity numeric methods consistent
with SPICE standards:

* **Type 9 (Lagrange):** Uses an Nth-order Lagrange polynomial interpolation on
  unequal time steps. It interpolates each of the 6 state components (position
  and velocity) independently.

* **Type 13 (Hermite):** Uses an Nth-order Hermite interpolation. This method
  explicitly uses the velocity data (derivatives) to constrain the interpolation
  of the position, ensuring that the resulting position curve is smooth and
  dynamically consistent with the velocity.

##### Covariance Interpolation (Log-Euclidean)
If covariance data is available, this method performs **Log-Euclidean Riemannian
Interpolation**. Unlike standard linear element-wise interpolation, this approach
respects the geometric manifold of Symmetric Positive Definite (SPD) matrices.

This guarantees that:

1. **Positive Definiteness:** The interpolated covariance matrix is always mathematically
   valid (all eigenvalues are strictly positive), preventing numerical crashes in downstream filters.
2. **Volume Preservation:** It prevents the artificial "swelling" (determinant increase)
   of uncertainty that occurs when linearly interpolating between two valid matrices.
   The interpolation follows the "geodesic" (shortest path) on the curved surface of
   covariance matrices.

:type epoch: Epoch
:type almanac: Almanac
:rtype: EphemerisRecord


##### Method `covar_at` {#anise.astro.Ephemeris.covar_at}

>     def covar_at(
>         self,
>         /,
>         epoch,
>         local_frame,
>         almanac
>     )

Interpolate the ephemeris covariance at the provided epoch.

This method implements a "Rotate-Then-Interpolate" strategy to avoid physical
artifacts when interpolating rotating covariances.


1. Finds the nearest covariance before and after the requested epoch.
2. Rotates BOTH endpoints into the requested <code>local\_frame</code>.
3. Interpolates between the two stable matrices using Log-Euclidean Riemannian interpolation.

:type epoch: Epoch
:type local_frame: LocalFrame
:type almanac: Almanac
:rtype: Covariance


##### Method `domain` {#anise.astro.Ephemeris.domain}

>     def domain(
>         self,
>         /
>     )

Returns the time domain of this ephemeris.

:rtype: tuple


##### Method `end_epoch` {#anise.astro.Ephemeris.end_epoch}

>     def end_epoch(
>         self,
>         /
>     )

:rtype: Epoch


##### Method `from_ccsds_oem_file` {#anise.astro.Ephemeris.from_ccsds_oem_file}

>     def from_ccsds_oem_file(
>         path
>     )

Initializes a new Ephemeris from a file path to CCSDS OEM file.

:type path: str
:rtype: Ephemeris


##### Method `from_stk_e_file` {#anise.astro.Ephemeris.from_stk_e_file}

>     def from_stk_e_file(
>         path
>     )

Initializes a new Ephemeris from a file path to Ansys STK .e file.

:type path: str
:rtype: Ephemeris


##### Method `get_object_id` {#anise.astro.Ephemeris.get_object_id}

>     def get_object_id(
>         self,
>         /
>     )

:rtype: str


##### Method `includes_covariance` {#anise.astro.Ephemeris.includes_covariance}

>     def includes_covariance(
>         self,
>         /
>     )

Returns true if all of the data in this ephemeris includes covariance.

This is a helper function which isn't used in other functions.

:rtype: bool


##### Method `insert` {#anise.astro.Ephemeris.insert}

>     def insert(
>         self,
>         /,
>         record
>     )

Inserts a new ephemeris entry to this ephemeris (it is automatically sorted chronologically).
:type record: EphemerisRecord
:rtype: None


##### Method `insert_orbit` {#anise.astro.Ephemeris.insert_orbit}

>     def insert_orbit(
>         self,
>         /,
>         orbit
>     )

Inserts a new orbit (without covariance) to this ephemeris (it is automatically sorted chronologically).
:type orbit: Orbit
:rtype: None


##### Method `len` {#anise.astro.Ephemeris.len}

>     def len(
>         self,
>         /
>     )

Returns the number of states

:rtype: int


##### Method `nearest_after` {#anise.astro.Ephemeris.nearest_after}

>     def nearest_after(
>         self,
>         /,
>         epoch,
>         almanac
>     )

Returns the nearest entry after the provided time

:type epoch: Epoch
:type almanac: Almanac
:rtype: EphemerisRecord


##### Method `nearest_before` {#anise.astro.Ephemeris.nearest_before}

>     def nearest_before(
>         self,
>         /,
>         epoch,
>         almanac
>     )

Returns the nearest entry before the provided time

:type epoch: Epoch
:type almanac: Almanac
:rtype: EphemerisRecord


##### Method `nearest_covar_after` {#anise.astro.Ephemeris.nearest_covar_after}

>     def nearest_covar_after(
>         self,
>         /,
>         epoch,
>         almanac
>     )

Returns the nearest covariance after the provided epoch as a tuple (Epoch, Covariance)

:type epoch: Epoch
:type almanac: Almanac
:rtype: tuple


##### Method `nearest_covar_before` {#anise.astro.Ephemeris.nearest_covar_before}

>     def nearest_covar_before(
>         self,
>         /,
>         epoch,
>         almanac
>     )

Returns the nearest covariance before the provided epoch as a tuple (Epoch, Covariance)

:type epoch: Epoch
:type almanac: Almanac
:rtype: tuple


##### Method `nearest_orbit_after` {#anise.astro.Ephemeris.nearest_orbit_after}

>     def nearest_orbit_after(
>         self,
>         /,
>         epoch,
>         almanac
>     )

Returns the nearest orbit after the provided time

:type epoch: Epoch
:type almanac: Almanac
:rtype: Orbit


##### Method `nearest_orbit_before` {#anise.astro.Ephemeris.nearest_orbit_before}

>     def nearest_orbit_before(
>         self,
>         /,
>         epoch,
>         almanac
>     )

Returns the nearest orbit before the provided time

:type epoch: Epoch
:type almanac: Almanac
:rtype: Orbit


##### Method `object_id` {#anise.astro.Ephemeris.object_id}

>     def object_id(
>         self,
>         /
>     )

:rtype: str


##### Method `orbit_at` {#anise.astro.Ephemeris.orbit_at}

>     def orbit_at(
>         self,
>         /,
>         epoch,
>         almanac
>     )

Interpolate the ephemeris at the provided epoch, returning only the orbit.

:type epoch: Epoch
:type almanac: Almanac
:rtype: Orbit


##### Method `resample` {#anise.astro.Ephemeris.resample}

>     def resample(
>         self,
>         /,
>         ts,
>         almanac
>     )

Resample this ephemeris, with covariance, at the provided time series

:type ts: TimeSeries
:type almanac: Almanac
:rtype: Ephemeris


##### Method `set_object_id` {#anise.astro.Ephemeris.set_object_id}

>     def set_object_id(
>         self,
>         /,
>         object_id
>     )

:type object_id: str


##### Method `start_epoch` {#anise.astro.Ephemeris.start_epoch}

>     def start_epoch(
>         self,
>         /
>     )

:rtype: Epoch


##### Method `transform` {#anise.astro.Ephemeris.transform}

>     def transform(
>         self,
>         /,
>         new_frame,
>         almanac
>     )

Transforms this ephemeris into another frame, and rotates the covariance to that frame if the orientations are different.
NOTE: The Nyquist-Shannon theorem is NOT applied here, so the new ephemeris may not be as precise as the original one.
NOTE: If the orientations are different, the covariance will always be in the Inertial frame of the new frame.

:type new_frame: Frame
:type almanac: Almanac
:rtype: Ephemeris


##### Method `write_ccsds_oem` {#anise.astro.Ephemeris.write_ccsds_oem}

>     def write_ccsds_oem(
>         self,
>         /,
>         path,
>         originator=None,
>         object_name=None
>     )

Exports this Ephemeris to CCSDS OEM at the provided path, optionally specifying an originator and/or an object name

:type path: str
:type originator: str, optional
:type object_name: str, optional
:rtype: None


##### Method `write_spice_bsp` {#anise.astro.Ephemeris.write_spice_bsp}

>     def write_spice_bsp(
>         self,
>         /,
>         naif_id,
>         output_fname,
>         data_type
>     )

Converts this ephemeris to SPICE BSP/SPK file in the provided data type, saved to the provided output_fname.

:type naif_id: int
:type output_fname: str
:type data_type: DataType
:rtype: None


### Class `EphemerisRecord` {#anise.astro.EphemerisRecord}

>     class EphemerisRecord(
>         orbit,
>         covar
>     )

An ephemeris record which can be inserted into an Ephemeris for export to SPICE BSP or CCSDS OEM.

:type orbit: Orbit
:type covar: Covariance


#### Instance variables


##### Variable `covar` {#anise.astro.EphemerisRecord.covar}

Optional covariance associated with this orbit
:rtype: Covariance


##### Variable `orbit` {#anise.astro.EphemerisRecord.orbit}

Orbit of this ephemeris entry
:rtype: Orbit


#### Methods


##### Method `covar_in_frame` {#anise.astro.EphemerisRecord.covar_in_frame}

>     def covar_in_frame(
>         self,
>         /,
>         local_frame
>     )

Returns the covariance in the desired orbit local frame, or None if this record does not define a covariance.

:type local_frame: LocalFrame
:rtype: Covariance


##### Method `sigma_for` {#anise.astro.EphemerisRecord.sigma_for}

>     def sigma_for(
>         self,
>         /,
>         oe
>     )

Returns the 1-sigma uncertainty (Standard Deviation) for a given orbital element.

The result is in the unit of the parameter (e.g., km for SMA, degrees for angles).

This method uses the [OrbitGrad] structure (Hyperdual numbers) to compute the
Jacobian of the element with respect to the inertial Cartesian state, and then
rotates the covariance into that hyperdual dual space: J * P * J^T.

:type oe: OrbitalElement
:rtype: float


### Class `Frame` {#anise.astro.Frame}

>     class Frame(
>         ephemeris_id,
>         orientation_id,
>         mu_km3_s2=None,
>         shape=None
>     )

A Frame uniquely defined by its ephemeris center and orientation. Refer to FrameDetail for frames combined with parameters.

:type ephemeris_id: int
:type orientation_id: int
:type force_inertial: bool
:type mu_km3_s2: float, optional
:type shape: Ellipsoid, optional
:type frozen_epoch: Epoch, optional
:rtype: Frame


#### Instance variables


##### Variable `ephemeris_id` {#anise.astro.Frame.ephemeris_id}

:rtype: int


##### Variable `force_inertial` {#anise.astro.Frame.force_inertial}


##### Variable `frozen_epoch` {#anise.astro.Frame.frozen_epoch}

:rtype: Epoch


##### Variable `orientation_id` {#anise.astro.Frame.orientation_id}

:rtype: int


##### Variable `shape` {#anise.astro.Frame.shape}

:rtype: Ellipsoid


#### Methods


##### Method `ephem_origin_id_match` {#anise.astro.Frame.ephem_origin_id_match}

>     def ephem_origin_id_match(
>         self,
>         /,
>         other_id
>     )

Returns true if the ephemeris origin is equal to the provided ID

:type other_id: int
:rtype: bool


##### Method `ephem_origin_match` {#anise.astro.Frame.ephem_origin_match}

>     def ephem_origin_match(
>         self,
>         /,
>         other
>     )

Returns true if the ephemeris origin is equal to the provided frame

:type other: Frame
:rtype: bool


##### Method `flattening` {#anise.astro.Frame.flattening}

>     def flattening(
>         self,
>         /
>     )

Returns the flattening ratio (unitless)

:rtype: float


##### Method `from_asn1` {#anise.astro.Frame.from_asn1}

>     def from_asn1(
>         data
>     )

Decodes an ASN.1 DER encoded byte array into a Frame.

:type data: bytes
:rtype: Frame


##### Method `is_celestial` {#anise.astro.Frame.is_celestial}

>     def is_celestial(
>         self,
>         /
>     )

Returns whether this is a celestial frame

:rtype: bool


##### Method `is_dynamic` {#anise.astro.Frame.is_dynamic}

>     def is_dynamic(
>         self,
>         /
>     )

Returns true if this is a dynamic frame, e.g. Mean/True of Date/Epoch

:rtype: bool


##### Method `is_geodetic` {#anise.astro.Frame.is_geodetic}

>     def is_geodetic(
>         self,
>         /
>     )

Returns whether this is a geodetic frame

:rtype: bool


##### Method `mean_equatorial_radius_km` {#anise.astro.Frame.mean_equatorial_radius_km}

>     def mean_equatorial_radius_km(
>         self,
>         /
>     )

Returns the mean equatorial radius in km, if defined

:rtype: float


##### Method `mu_km3_s2` {#anise.astro.Frame.mu_km3_s2}

>     def mu_km3_s2(
>         self,
>         /
>     )

Returns the gravitational parameters of this frame, if defined

:rtype: float


##### Method `orient_origin_id_match` {#anise.astro.Frame.orient_origin_id_match}

>     def orient_origin_id_match(
>         self,
>         /,
>         other_id
>     )

Returns true if the orientation origin is equal to the provided ID

:type other_id: int
:rtype: bool


##### Method `orient_origin_match` {#anise.astro.Frame.orient_origin_match}

>     def orient_origin_match(
>         self,
>         /,
>         other
>     )

Returns true if the orientation origin is equal to the provided frame

:type other: Frame
:rtype: bool


##### Method `polar_radius_km` {#anise.astro.Frame.polar_radius_km}

>     def polar_radius_km(
>         self,
>         /
>     )

Returns the polar radius in km, if defined

:rtype: float


##### Method `semi_major_radius_km` {#anise.astro.Frame.semi_major_radius_km}

>     def semi_major_radius_km(
>         self,
>         /
>     )

Returns the semi major radius of the tri-axial ellipoid shape of this frame, if defined

:rtype: float


##### Method `strip` {#anise.astro.Frame.strip}

>     def strip(
>         self,
>         /
>     )

Removes the graviational parameter and the shape information from this frame.
Use this to prevent astrodynamical computations.

:rtype: None


##### Method `to_asn1` {#anise.astro.Frame.to_asn1}

>     def to_asn1(
>         self,
>         /
>     )

Encodes this Frame into an ASN.1 DER encoded byte array.

:rtype: bytes


##### Method `with_ephem` {#anise.astro.Frame.with_ephem}

>     def with_ephem(
>         self,
>         /,
>         new_ephem_id
>     )

Returns a copy of this Frame whose ephemeris ID is set to the provided ID

:type new_ephem_id: int
:rtype: Frame


##### Method `with_mu_km3_s2` {#anise.astro.Frame.with_mu_km3_s2}

>     def with_mu_km3_s2(
>         self,
>         /,
>         mu_km3_s2
>     )

Returns a copy of this frame with the graviational parameter set to the new value.

:type mu_km3_s2: float
:rtype: Frame


##### Method `with_orient` {#anise.astro.Frame.with_orient}

>     def with_orient(
>         self,
>         /,
>         new_orient_id
>     )

Returns a copy of this Frame whose orientation ID is set to the provided ID

:type new_orient_id: int
:rtype: Frame


### Class `FrameUid` {#anise.astro.FrameUid}

>     class FrameUid(
>         ephemeris_id,
>         orientation_id
>     )

A unique frame reference that only contains enough information to build the actual Frame object.
It cannot be used for any computations, is it be used in any structure apart from error structures.

:type ephemeris_id: int
:type orientation_id: int


#### Instance variables


##### Variable `force_inertial` {#anise.astro.FrameUid.force_inertial}


##### Variable `frozen_epoch` {#anise.astro.FrameUid.frozen_epoch}

:rtype: Epoch


### Class `LocalFrame` {#anise.astro.LocalFrame}

>     class LocalFrame


#### Class variables


##### Variable `Inertial` {#anise.astro.LocalFrame.Inertial}


##### Variable `RCN` {#anise.astro.LocalFrame.RCN}


##### Variable `RIC` {#anise.astro.LocalFrame.RIC}


##### Variable `VNC` {#anise.astro.LocalFrame.VNC}


### Class `Location` {#anise.astro.Location}

>     class Location(
>         latitude_deg,
>         longitude_deg,
>         height_km,
>         frame,
>         terrain_mask,
>         terrain_mask_ignored
>     )

Location is defined by its latitude, longitude, height above the geoid, mean angular rotation of the geoid, and a frame UID.
If the location includes a terrain mask, it will be used for obstruction checks when computing azimuth and elevation.
**Note:** The mean Earth angular velocity is <code>0.004178079012116429</code> deg/s.

:type latitude_deg: float
:type longitude_deg: float
:type height_km: float
:type frame: FrameUid
:type terrain_mask: list
:type terrain_mask_ignored: bool


#### Instance variables


##### Variable `height_km` {#anise.astro.Location.height_km}

:rtype: float


##### Variable `latitude_deg` {#anise.astro.Location.latitude_deg}

:rtype: float


##### Variable `longitude_deg` {#anise.astro.Location.longitude_deg}

:rtype: float


##### Variable `terrain_mask` {#anise.astro.Location.terrain_mask}

:rtype: list


##### Variable `terrain_mask_ignored` {#anise.astro.Location.terrain_mask_ignored}

:rtype: bool


#### Methods


##### Method `elevation_mask_at_azimuth_deg` {#anise.astro.Location.elevation_mask_at_azimuth_deg}

>     def elevation_mask_at_azimuth_deg(
>         self,
>         /,
>         azimuth_deg
>     )

Returns the elevation mask at the provided azimuth, does NOT account for whether the mask is ignored or not.

:type azimuth_deg: float
:rtype: float


##### Method `from_dhall` {#anise.astro.Location.from_dhall}

>     def from_dhall(
>         repr
>     )

Loads a Location from its Dhall representation

:type repr: str
:rtype: Location


##### Method `to_dhall` {#anise.astro.Location.to_dhall}

>     def to_dhall(
>         self,
>         /
>     )

Returns the Dhall representation of this Location

:rtype: str


### Class `Mass` {#anise.astro.Mass}

>     class Mass(
>         dry_mass_kg,
>         prop_mass_kg=None,
>         extra_mass_kg=None
>     )

Defines a spacecraft mass a the sum of the dry (structural) mass and the propellant mass, both in kilogram


#### Instance variables


##### Variable `dry_mass_kg` {#anise.astro.Mass.dry_mass_kg}

Structural mass of the spacecraft, in kg
:rtype: float


##### Variable `extra_mass_kg` {#anise.astro.Mass.extra_mass_kg}

Extra mass like unusable propellant mass of the spacecraft, in kg
:rtype: float


##### Variable `prop_mass_kg` {#anise.astro.Mass.prop_mass_kg}

Propellant mass of the spacecraft, in kg
:rtype: float


#### Methods


##### Method `abs` {#anise.astro.Mass.abs}

>     def abs(
>         self,
>         /
>     )

Returns a Mass structure that is guaranteed to be physically correct
:rtype: Mass


##### Method `from_asn1` {#anise.astro.Mass.from_asn1}

>     def from_asn1(
>         data
>     )

Decodes an ASN.1 DER encoded byte array into a Mass object.

:type data: bytes
:rtype: Mass


##### Method `is_valid` {#anise.astro.Mass.is_valid}

>     def is_valid(
>         self,
>         /
>     )

Returns true if all the masses are greater or equal to zero
:rtype: bool


##### Method `to_asn1` {#anise.astro.Mass.to_asn1}

>     def to_asn1(
>         self,
>         /
>     )

Encodes this Mass object into an ASN.1 DER encoded byte array.

:rtype: bytes


##### Method `total_mass_kg` {#anise.astro.Mass.total_mass_kg}

>     def total_mass_kg(
>         self,
>         /
>     )

Returns the total mass in kg
:rtype: float


### Class `Occultation` {#anise.astro.Occultation}

>     class Occultation

Stores the result of an occultation computation with the occultation percentage
Refer to the [MathSpec](https://nyxspace.com/nyxspace/MathSpec/celestial/eclipse/) for modeling details.


#### Instance variables


##### Variable `back_frame` {#anise.astro.Occultation.back_frame}

:rtype: Frame


##### Variable `epoch` {#anise.astro.Occultation.epoch}

:rtype: Epoch


##### Variable `front_frame` {#anise.astro.Occultation.front_frame}

:rtype: Frame


##### Variable `percentage` {#anise.astro.Occultation.percentage}

:rtype: float


#### Methods


##### Method `factor` {#anise.astro.Occultation.factor}

>     def factor(
>         self,
>         /
>     )

Returns the percentage as a factor between 0 and 1

:rtype: float


##### Method `is_eclipse_computation` {#anise.astro.Occultation.is_eclipse_computation}

>     def is_eclipse_computation(
>         self,
>         /
>     )

Returns true if the back object is the Sun, false otherwise

:rtype: bool


##### Method `is_obstructed` {#anise.astro.Occultation.is_obstructed}

>     def is_obstructed(
>         self,
>         /
>     )

Returns true if the occultation percentage is greater than or equal 99.999%

:rtype: bool


##### Method `is_partial` {#anise.astro.Occultation.is_partial}

>     def is_partial(
>         self,
>         /
>     )

Returns true if neither occulted nor visible (i.e. penumbra for solar eclipsing)

:rtype: bool


##### Method `is_visible` {#anise.astro.Occultation.is_visible}

>     def is_visible(
>         self,
>         /
>     )

Returns true if the occultation percentage is less than or equal 0.001%

:rtype: bool


### Class `Orbit` {#anise.astro.Orbit}

>     class Orbit(
>         *args
>     )

Defines a Cartesian state in a given frame at a given epoch in a given time scale. Radius data is expressed in kilometers. Velocity data is expressed in kilometers per second.
Regardless of the constructor used, this struct stores all the state information in Cartesian coordinates as these are always non singular.

Unless noted otherwise, algorithms are from GMAT 2016a [StateConversionUtil.cpp](https://github.com/ChristopherRabotin/GMAT/blob/37201a6290e7f7b941bc98ee973a527a5857104b/src/base/util/StateConversionUtil.cpp).

:type args: tuples
:rtype: Orbit


#### Instance variables


##### Variable `epoch` {#anise.astro.Orbit.epoch}

:rtype: Epoch


##### Variable `frame` {#anise.astro.Orbit.frame}

:rtype: Frame


##### Variable `vx_km_s` {#anise.astro.Orbit.vx_km_s}

:rtype: float


##### Variable `vy_km_s` {#anise.astro.Orbit.vy_km_s}

:rtype: float


##### Variable `vz_km_s` {#anise.astro.Orbit.vz_km_s}

:rtype: float


##### Variable `x_km` {#anise.astro.Orbit.x_km}

:rtype: float


##### Variable `y_km` {#anise.astro.Orbit.y_km}

:rtype: float


##### Variable `z_km` {#anise.astro.Orbit.z_km}

:rtype: float


#### Methods


##### Method `abs_difference` {#anise.astro.Orbit.abs_difference}

>     def abs_difference(
>         self,
>         /,
>         other
>     )

Returns the absolute position and velocity differences in km and km/s between this orbit and another.
Raises an error if the frames do not match (epochs do not need to match).

:type other: Orbit
:rtype: typing.Tuple


##### Method `abs_pos_diff_km` {#anise.astro.Orbit.abs_pos_diff_km}

>     def abs_pos_diff_km(
>         self,
>         /,
>         other
>     )

Returns the absolute position difference in kilometer between this orbit and another.
Raises an error if the frames do not match (epochs do not need to match).

:type other: Orbit
:rtype: float


##### Method `abs_vel_diff_km_s` {#anise.astro.Orbit.abs_vel_diff_km_s}

>     def abs_vel_diff_km_s(
>         self,
>         /,
>         other
>     )

Returns the absolute velocity difference in kilometer per second between this orbit and another.
Raises an error if the frames do not match (epochs do not need to match).

:type other: Orbit
:rtype: float


##### Method `add_aop_deg` {#anise.astro.Orbit.add_aop_deg}

>     def add_aop_deg(
>         self,
>         /,
>         delta_aop_deg
>     )

Returns a copy of the state with a provided AOP added to the current one

:type delta_aop_deg: float
:rtype: Orbit


##### Method `add_apoapsis_periapsis_km` {#anise.astro.Orbit.add_apoapsis_periapsis_km}

>     def add_apoapsis_periapsis_km(
>         self,
>         /,
>         delta_ra_km,
>         delta_rp_km
>     )

Returns a copy of this state with the provided apoasis and periapsis added to the current values

:type delta_ra_km: float
:type delta_rp_km: float
:rtype: Orbit


##### Method `add_ecc` {#anise.astro.Orbit.add_ecc}

>     def add_ecc(
>         self,
>         /,
>         delta_ecc
>     )

Returns a copy of the state with a provided ECC added to the current one

:type delta_ecc: float
:rtype: Orbit


##### Method `add_inc_deg` {#anise.astro.Orbit.add_inc_deg}

>     def add_inc_deg(
>         self,
>         /,
>         delta_inc_deg
>     )

Returns a copy of the state with a provided INC added to the current one

:type delta_inc_deg: float
:rtype: Orbit


##### Method `add_raan_deg` {#anise.astro.Orbit.add_raan_deg}

>     def add_raan_deg(
>         self,
>         /,
>         delta_raan_deg
>     )

Returns a copy of the state with a provided RAAN added to the current one

:type delta_raan_deg: float
:rtype: Orbit


##### Method `add_sma_km` {#anise.astro.Orbit.add_sma_km}

>     def add_sma_km(
>         self,
>         /,
>         delta_sma_km
>     )

Returns a copy of the state with a provided SMA added to the current one

:type delta_sma_km: float
:rtype: Orbit


##### Method `add_ta_deg` {#anise.astro.Orbit.add_ta_deg}

>     def add_ta_deg(
>         self,
>         /,
>         delta_ta_deg
>     )

Returns a copy of the state with a provided TA added to the current one

:type delta_ta_deg: float
:rtype: Orbit


##### Method `altitude_km` {#anise.astro.Orbit.altitude_km}

>     def altitude_km(
>         self,
>         /
>     )

Returns the altitude in km

:rtype: float


##### Method `aol_deg` {#anise.astro.Orbit.aol_deg}

>     def aol_deg(
>         self,
>         /
>     )

Returns the argument of latitude in degrees

NOTE: If the orbit is near circular, the AoL will be computed from the true longitude
instead of relying on the ill-defined true anomaly.

:rtype: float


##### Method `aop_brouwer_short_deg` {#anise.astro.Orbit.aop_brouwer_short_deg}

>     def aop_brouwer_short_deg(
>         self,
>         /
>     )

Returns the Brouwer-short mean Argument of Perigee in degrees.

:rtype: float


##### Method `aop_deg` {#anise.astro.Orbit.aop_deg}

>     def aop_deg(
>         self,
>         /
>     )

Returns the argument of periapsis in degrees

:rtype: float


##### Method `apoapsis_altitude_km` {#anise.astro.Orbit.apoapsis_altitude_km}

>     def apoapsis_altitude_km(
>         self,
>         /
>     )

Returns the altitude of apoapsis (or apogee around Earth), in kilometers.

:rtype: float


##### Method `apoapsis_km` {#anise.astro.Orbit.apoapsis_km}

>     def apoapsis_km(
>         self,
>         /
>     )

Returns the radius of apoapsis (or apogee around Earth), in kilometers.

:rtype: float


##### Method `at_epoch` {#anise.astro.Orbit.at_epoch}

>     def at_epoch(
>         self,
>         /,
>         new_epoch
>     )

Adjusts the equinoctial mean longitude this orbit via the mean motion.

##### Astrodynamics note
This is not a true propagation of the orbit. This is akin to a two body propagation ONLY without any other force models applied.
Use Nyx for high fidelity propagation. This implementation uses equinoctial elements and should be well behaved for circular equatorial orbits.

:type new_epoch: Epoch
:rtype: Orbit


##### Method `c3_km2_s2` {#anise.astro.Orbit.c3_km2_s2}

>     def c3_km2_s2(
>         self,
>         /
>     )

Returns the $C_3$ of this orbit in km^2/s^2

:rtype: float


##### Method `cartesian_pos_vel` {#anise.astro.Orbit.cartesian_pos_vel}

>     def cartesian_pos_vel(
>         self,
>         /
>     )

Returns this state as a Cartesian vector of size 6 in [km, km, km, km/s, km/s, km/s]

Note that the time is **not** returned in the vector.
:rtype: numpy.ndarray


##### Method `dcm3x3_from_rcn_to_inertial` {#anise.astro.Orbit.dcm3x3_from_rcn_to_inertial}

>     def dcm3x3_from_rcn_to_inertial(
>         self,
>         /
>     )

Builds the rotation matrix that rotates from this state's inertial frame to this state's RCN frame (radial, cross, normal)

##### Frame warning
If the stattion is NOT in an inertial frame, then this computation is INVALID.

##### Algorithm
1. Compute \hat{r}, \hat{h}, the unit vectors of the radius and orbital momentum.
2. Compute the cross product of these
3. Build the DCM with these unit vectors
4. Return the DCM structure

:rtype: DCM


##### Method `dcm3x3_from_ric_to_inertial` {#anise.astro.Orbit.dcm3x3_from_ric_to_inertial}

>     def dcm3x3_from_ric_to_inertial(
>         self,
>         /
>     )

Builds the rotation matrix that rotates from this state's inertial frame to this state's RIC frame

##### Frame warning
If the state is NOT in an inertial frame, then this computation is INVALID.

##### Algorithm
1. Build the c vector as the normalized orbital momentum vector
2. Build the i vector as the cross product of \hat{r} and c
3. Build the RIC DCM as a 3x3 of the columns [\hat{r}, \hat{i}, \hat{c}]
4. Return the DCM structure **without** accounting for the transport theorem.

:rtype: DCM


##### Method `dcm3x3_from_topocentric_to_body_fixed` {#anise.astro.Orbit.dcm3x3_from_topocentric_to_body_fixed}

>     def dcm3x3_from_topocentric_to_body_fixed(
>         self,
>         /
>     )

Builds the rotation matrix that rotates from the topocentric frame (SEZ) into the body fixed frame of this state.

##### Frame warning
If the state is NOT in a body fixed frame (i.e. ITRF93), then this computation is INVALID.

##### Source
From the GMAT MathSpec, page 30 section 2.6.9 and from <code>Calculate\_RFT</code> in <code>TopocentricAxes.cpp</code>, this returns the
rotation matrix from the topocentric frame (SEZ) to body fixed frame.
In the GMAT MathSpec notation, R_{IF} is the DCM from body fixed to inertial. Similarly, R{FT} is from topocentric
to body fixed.

:rtype: DCM


##### Method `dcm3x3_from_vnc_to_inertial` {#anise.astro.Orbit.dcm3x3_from_vnc_to_inertial}

>     def dcm3x3_from_vnc_to_inertial(
>         self,
>         /
>     )

Builds the rotation matrix that rotates from this state's inertial frame to this state's VNC frame (velocity, normal, cross)

##### Frame warning
If the stattion is NOT in an inertial frame, then this computation is INVALID.

##### Algorithm
1. Compute \hat{v}, \hat{h}, the unit vectors of the radius and orbital momentum.
2. Compute the cross product of these
3. Build the DCM with these unit vectors
4. Return the DCM structure.

:rtype: DCM


##### Method `dcm_from_rcn_to_inertial` {#anise.astro.Orbit.dcm_from_rcn_to_inertial}

>     def dcm_from_rcn_to_inertial(
>         self,
>         /
>     )

Builds the rotation matrix that rotates from this state's inertial frame to this state's RCN frame (radial, cross, normal)

##### Frame warning
If the stattion is NOT in an inertial frame, then this computation is INVALID.

##### Algorithm
1. Compute \hat{r}, \hat{h}, the unit vectors of the radius and orbital momentum.
2. Compute the cross product of these
3. Build the DCM with these unit vectors
4. Return the DCM structure with a 6x6 DCM with the time derivative of the VNC frame set.

##### Note on the time derivative
If the pre or post states cannot be computed, then the time derivative of the DCM will _not_ be set.
Further note that most astrodynamics tools do *not* account for the time derivative in the RIC frame.

:rtype: DCM


##### Method `dcm_from_ric_to_inertial` {#anise.astro.Orbit.dcm_from_ric_to_inertial}

>     def dcm_from_ric_to_inertial(
>         self,
>         /
>     )

Builds the rotation matrix that rotates from this state's inertial frame to this state's RIC frame

##### Frame warning
If the state is NOT in an inertial frame, then this computation is INVALID.

##### Algorithm
1. Compute the state data one millisecond before and one millisecond assuming two body dynamics
2. Compute the DCM for this state, and the pre and post states
3. Build the c vector as the normalized orbital momentum vector
4. Build the i vector as the cross product of \hat{r} and c
5. Build the RIC DCM as a 3x3 of the columns [\hat{r}, \hat{i}, \hat{c}], for the post, post, and current states
6. Compute the difference between the DCMs of the pre and post states, to build the DCM time derivative
7. Return the DCM structure with a 6x6 state DCM.

##### Note on the time derivative
If the pre or post states cannot be computed, then the time derivative of the DCM will _not_ be set.
Further note that most astrodynamics tools do *not* account for the time derivative in the RIC frame.

:rtype: DCM


##### Method `dcm_from_topocentric_to_body_fixed` {#anise.astro.Orbit.dcm_from_topocentric_to_body_fixed}

>     def dcm_from_topocentric_to_body_fixed(
>         self,
>         /
>     )

Builds the rotation matrix that rotates from the topocentric frame (SEZ) into the body fixed frame of this state.

##### Frame warnings
+ If the state is NOT in a body fixed frame (i.e. ITRF93), then this computation is INVALID.
+ (Usually) no time derivative can be computed: the orbit is expected to be a body fixed frame where the <code>at\_epoch</code> function will fail. Exceptions for Moon body fixed frames.

##### UNUSED Arguments
+ <code>from</code>: ID of this new frame. Only used to set the "from" frame of the DCM. -- No longer used since 0.5.3

##### Source
From the GMAT MathSpec, page 30 section 2.6.9 and from <code>Calculate\_RFT</code> in <code>TopocentricAxes.cpp</code>, this returns the
rotation matrix from the topocentric frame (SEZ) to body fixed frame.
In the GMAT MathSpec notation, R_{IF} is the DCM from body fixed to inertial. Similarly, R{FT} is from topocentric
to body fixed.

:rtype: DCM


##### Method `dcm_from_vnc_to_inertial` {#anise.astro.Orbit.dcm_from_vnc_to_inertial}

>     def dcm_from_vnc_to_inertial(
>         self,
>         /
>     )

Builds the rotation matrix that rotates from this state's inertial frame to this state's VNC frame (velocity, normal, cross)

##### Frame warning
If the stattion is NOT in an inertial frame, then this computation is INVALID.

##### Algorithm
1. Compute \hat{v}, \hat{h}, the unit vectors of the radius and orbital momentum.
2. Compute the cross product of these
3. Build the DCM with these unit vectors
4. Compute the difference between the DCMs of the pre and post states (+/- 1 ms), to build the DCM time derivative
4. Return the DCM structure with a 6x6 DCM with the time derivative of the VNC frame set.

##### Note on the time derivative
If the pre or post states cannot be computed, then the time derivative of the DCM will _not_ be set.
Further note that most astrodynamics tools do *not* account for the time derivative in the RIC frame.

:rtype: DCM


##### Method `dcm_to_inertial` {#anise.astro.Orbit.dcm_to_inertial}

>     def dcm_to_inertial(
>         self,
>         /,
>         local_frame
>     )

Returns the DCM to rotate this orbit from the provided local frame to the inertial frame.

:type local_frame: LocalFrame
:rtype: DCM


##### Method `declination_deg` {#anise.astro.Orbit.declination_deg}

>     def declination_deg(
>         self,
>         /
>     )

Returns the declination of this orbit in degrees

:rtype: float


##### Method `distance_to_km` {#anise.astro.Orbit.distance_to_km}

>     def distance_to_km(
>         self,
>         /,
>         other
>     )

Returns the distance in kilometers between this state and another state, if both frame match (epoch does not need to match).

:type other: Orbit
:rtype: float


##### Method `duration_to_radius` {#anise.astro.Orbit.duration_to_radius}

>     def duration_to_radius(
>         self,
>         /,
>         radius_km
>     )

Calculates the duration to reach a specific radius in the orbit.

This function computes the time it will take for the orbiting body to reach
the given <code>radius\_km</code> from its current position. The calculation assumes
two-body dynamics and considers the direction of motion.

##### Assumptions & Limitations

- Assumes pure Keplerian motion.
- For elliptical orbits, if the radius is reachable at two points (ascending and descending parts
  of the orbit), this function calculates the time to reach the radius corresponding to the
  true anomaly in <code>\[0, PI]</code> (typically the ascending part or up to apoapsis if starting past periapsis).
- For circular orbits, if the radius is within the apoapse and periapse, then a duration of zero is returned.
- For hyperbolic/parabolic orbits, the true anomaly at radius is also computed in <code>\[0, PI]</code>. If this
  point is in the past, the function returns an error, as it doesn't look for solutions on the
  departing leg if `nu > PI` would be required (unless current TA is already > PI and target radius is further along).
  The current implementation strictly uses the <code>acos</code> result, so <code>nu\_rad\_at\_radius</code> is always `0 <= nu <= PI`.
  This means it finds the time to reach the radius on the path from periapsis up to the point where true anomaly is PI.

:type radius_km: float
:rtype: Duration


##### Method `ea_deg` {#anise.astro.Orbit.ea_deg}

>     def ea_deg(
>         self,
>         /
>     )

Returns the eccentric anomaly in degrees

This is a conversion from GMAT's StateConversionUtil::TrueToEccentricAnomaly

:rtype: float


##### Method `ecc` {#anise.astro.Orbit.ecc}

>     def ecc(
>         self,
>         /
>     )

Returns the eccentricity (no unit)

:rtype: float


##### Method `ecc_brouwer_short` {#anise.astro.Orbit.ecc_brouwer_short}

>     def ecc_brouwer_short(
>         self,
>         /
>     )

Returns the Brouwer-short mean eccentricity.

:rtype: float


##### Method `energy_km2_s2` {#anise.astro.Orbit.energy_km2_s2}

>     def energy_km2_s2(
>         self,
>         /
>     )

Returns the specific mechanical energy in km^2/s^2

:rtype: float


##### Method `eq_within` {#anise.astro.Orbit.eq_within}

>     def eq_within(
>         self,
>         /,
>         other,
>         radial_tol_km,
>         velocity_tol_km_s
>     )

Returns whether this orbit and another are equal within the specified radial and velocity absolute tolerances

:type other: Orbit
:type radial_tol_km: float
:type velocity_tol_km_s: float
:rtype: bool


##### Method `equinoctial_a_km` {#anise.astro.Orbit.equinoctial_a_km}

>     def equinoctial_a_km(
>         self,
>         /
>     )

Returns the equinoctial semi-major axis (a) in km.

:rtype: float


##### Method `equinoctial_elements` {#anise.astro.Orbit.equinoctial_elements}

>     def equinoctial_elements(
>         self,
>         /
>     )

Returns the six equinoctial elements in order: sma (km), h, k, p, q, lambda (deg)

:rtype: list[float]


##### Method `equinoctial_h` {#anise.astro.Orbit.equinoctial_h}

>     def equinoctial_h(
>         self,
>         /
>     )

Returns the equinoctial element h (ecc * sin(aop + raan)).

:rtype: float


##### Method `equinoctial_k` {#anise.astro.Orbit.equinoctial_k}

>     def equinoctial_k(
>         self,
>         /
>     )

Returns the equinoctial element k (ecc * cos(aop + raan)).

:rtype: float


##### Method `equinoctial_lambda_mean_deg` {#anise.astro.Orbit.equinoctial_lambda_mean_deg}

>     def equinoctial_lambda_mean_deg(
>         self,
>         /
>     )

Returns the equinoctial mean longitude (lambda = raan + aop + ma) in degrees.

:rtype: float


##### Method `equinoctial_p` {#anise.astro.Orbit.equinoctial_p}

>     def equinoctial_p(
>         self,
>         /
>     )

Returns the equinoctial element p (sin(inc/2) * sin(raan)).

:rtype: float


##### Method `equinoctial_q` {#anise.astro.Orbit.equinoctial_q}

>     def equinoctial_q(
>         self,
>         /
>     )

Returns the equinoctial element q (sin(inc/2) * cos(raan)).

:rtype: float


##### Method `fpa_deg` {#anise.astro.Orbit.fpa_deg}

>     def fpa_deg(
>         self,
>         /
>     )

Returns the flight path angle in degrees

:rtype: float


##### Method `from_asn1` {#anise.astro.Orbit.from_asn1}

>     def from_asn1(
>         data
>     )

Decodes an ASN.1 DER encoded byte array into a CartesianState (Orbit).

:type data: bytes
:rtype: Orbit


##### Method `from_cartesian` {#anise.astro.Orbit.from_cartesian}

>     def from_cartesian(
>         x_km,
>         y_km,
>         z_km,
>         vx_km_s,
>         vy_km_s,
>         vz_km_s,
>         epoch,
>         frame
>     )

Creates a new Cartesian state in the provided frame at the provided Epoch.

**Units:** km, km, km, km/s, km/s, km/s

:type x_km: float
:type y_km: float
:type z_km: float
:type vx_km_s: float
:type vy_km_s: float
:type vz_km_s: float
:type epoch: Epoch
:type frame: Frame
:rtype: Orbit


##### Method `from_cartesian_npy` {#anise.astro.Orbit.from_cartesian_npy}

>     def from_cartesian_npy(
>         pos_vel,
>         epoch,
>         frame
>     )

Creates a new Cartesian state from a numpy array, an epoch, and a frame.

**Units:** km, km, km, km/s, km/s, km/s

:type pos_vel: np.array
:type epoch: Epoch
:type frame: Frame
:rtype: Orbit


##### Method `from_equinoctial` {#anise.astro.Orbit.from_equinoctial}

>     def from_equinoctial(
>         sma_km,
>         h,
>         k,
>         p,
>         q,
>         lambda_deg,
>         epoch,
>         frame
>     )

Attempts to create a new Orbit from the Equinoctial orbital elements.

##### Implementation notes
Note that this function computes the Keplerian elements from the equinoctial and then
calls the try_keplerian_mean_anomaly initializer.

:type sma_km: float
:type h: float
:type k: float
:type p: float
:type q: float
:type lambda_deg: float
:type epoch: Epoch
:type frame: Frame
:rtype: Orbit


##### Method `from_keplerian` {#anise.astro.Orbit.from_keplerian}

>     def from_keplerian(
>         sma_km,
>         ecc,
>         inc_deg,
>         raan_deg,
>         aop_deg,
>         ta_deg,
>         epoch,
>         frame
>     )

Creates a new Orbit around the provided Celestial or Geoid frame from the Keplerian orbital elements.

**Units:** km, none, degrees, degrees, degrees, degrees

NOTE: The state is defined in Cartesian coordinates as they are non-singular. This causes rounding
errors when creating a state from its Keplerian orbital elements (cf. the state tests).
One should expect these errors to be on the order of 1e-12.

:type sma_km: float
:type ecc: float
:type inc_deg: float
:type raan_deg: float
:type aop_deg: float
:type ta_deg: float
:type epoch: Epoch
:type frame: Frame
:rtype: Orbit


##### Method `from_keplerian_altitude` {#anise.astro.Orbit.from_keplerian_altitude}

>     def from_keplerian_altitude(
>         sma_altitude_km,
>         ecc,
>         inc_deg,
>         raan_deg,
>         aop_deg,
>         ta_deg,
>         epoch,
>         frame
>     )

Creates a new Orbit from the provided semi-major axis altitude in kilometers

:type sma_altitude_km: float
:type ecc: float
:type inc_deg: float
:type raan_deg: float
:type aop_deg: float
:type ta_deg: float
:type epoch: Epoch
:type frame: Frame
:rtype: Orbit


##### Method `from_keplerian_apsis_altitude` {#anise.astro.Orbit.from_keplerian_apsis_altitude}

>     def from_keplerian_apsis_altitude(
>         apo_alt_km,
>         peri_alt_km,
>         inc_deg,
>         raan_deg,
>         aop_deg,
>         ta_deg,
>         epoch,
>         frame
>     )

Creates a new Orbit from the provided altitudes of apoapsis and periapsis, in kilometers

:type apo_alt_km: float
:type peri_alt_km: float
:type inc_deg: float
:type raan_deg: float
:type aop_deg: float
:type ta_deg: float
:type epoch: Epoch
:type frame: Frame
:rtype: Orbit


##### Method `from_keplerian_apsis_radii` {#anise.astro.Orbit.from_keplerian_apsis_radii}

>     def from_keplerian_apsis_radii(
>         r_a_km,
>         r_p_km,
>         inc_deg,
>         raan_deg,
>         aop_deg,
>         ta_deg,
>         epoch,
>         frame
>     )

Attempts to create a new Orbit from the provided radii of apoapsis and periapsis, in kilometers

:type r_a_km: float
:type r_p_km: float
:type inc_deg: float
:type raan_deg: float
:type aop_deg: float
:type ta_deg: float
:type epoch: Epoch
:type frame: Frame
:rtype: Orbit


##### Method `from_keplerian_mean_anomaly` {#anise.astro.Orbit.from_keplerian_mean_anomaly}

>     def from_keplerian_mean_anomaly(
>         sma_km,
>         ecc,
>         inc_deg,
>         raan_deg,
>         aop_deg,
>         ma_deg,
>         epoch,
>         frame
>     )

Initializes a new orbit from the Keplerian orbital elements using the mean anomaly instead of the true anomaly.

##### Implementation notes
This function starts by converting the mean anomaly to true anomaly, and then it initializes the orbit
using the keplerian(..) method.
The conversion is from GMAT's MeanToTrueAnomaly function, transliterated originally by Claude and GPT4 with human adjustments.

:type sma_km: float
:type ecc: float
:type inc_deg: float
:type raan_deg: float
:type aop_deg: float
:type ma_deg: float
:type epoch: Epoch
:type frame: Frame
:rtype: Orbit


##### Method `from_latlongalt` {#anise.astro.Orbit.from_latlongalt}

>     def from_latlongalt(
>         latitude_deg,
>         longitude_deg,
>         height_km,
>         epoch,
>         frame
>     )

Creates a new Orbit from the latitude (φ), longitude (λ) and height (in km) with respect to the frame's ellipsoid, and with ZERO angular velocity in this frame.
Use this initializer for creating a fixed point in the ITRF93 frame for example: the correct angular velocity will be applied when transforming this to EME2000 for example.

Refer to [try_latlongalt_omega] if you need to build a fixed point with a non-zero angular velocity in the definition frame.

NOTE: This computation differs from the spherical coordinates because we consider the flattening of body.
Reference: G. Xu and Y. Xu, "GPS", DOI 10.1007/978-3-662-50367-6_2, 2016

:type latitude_deg: float
:type longitude_deg: float
:type height_km: float
:type epoch: Epoch
:type frame: Frame
:rtype: Orbit


##### Method `from_latlongalt_omega` {#anise.astro.Orbit.from_latlongalt_omega}

>     def from_latlongalt_omega(
>         latitude_deg,
>         longitude_deg,
>         height_km,
>         angular_velocity_rad_s,
>         epoch,
>         frame
>     )

Creates a new Orbit from the latitude (φ), longitude (λ) and height (in km) with respect to the frame's ellipsoid given the angular velocity vector.
NOTE: Only specify the angular velocity if there's an EXTRA angular velocity of the lat/long/alt point in the provided frame.

Consider using the [Almanac]'s [angular_velocity_wrt_j2000_rad_s] function or [angular_velocity_rad_s] to retrieve the exact angular velocity vector between two orientations.
Example: build a lat/long/alt point referenced in the ITRF93 frame but by specifying the Frame as the EME2000 frame and providing the angular velocity between the ITRF93 and EME2000 frame at the desired time.

NOTE: This computation differs from the spherical coordinates because we consider the flattening of body.
Reference: G. Xu and Y. Xu, "GPS", DOI 10.1007/978-3-662-50367-6_2, 2016

:type latitude_deg: float
:type longitude_deg: float
:type height_km: float
:type angular_velocity_rad_s: np.array
:type epoch: Epoch
:type frame: Frame
:rtype: Orbit


##### Method `height_km` {#anise.astro.Orbit.height_km}

>     def height_km(
>         self,
>         /
>     )

Returns the geodetic height in km.

Reference: Vallado, 4th Ed., Algorithm 12 page 172.

:rtype: float


##### Method `hmag` {#anise.astro.Orbit.hmag}

>     def hmag(
>         self,
>         /
>     )

Returns the norm of the orbital momentum

:rtype: float


##### Method `hx` {#anise.astro.Orbit.hx}

>     def hx(
>         self,
>         /
>     )

Returns the orbital momentum value on the X axis

:rtype: float


##### Method `hy` {#anise.astro.Orbit.hy}

>     def hy(
>         self,
>         /
>     )

Returns the orbital momentum value on the Y axis

:rtype: float


##### Method `hyperbolic_anomaly_deg` {#anise.astro.Orbit.hyperbolic_anomaly_deg}

>     def hyperbolic_anomaly_deg(
>         self,
>         /
>     )

Returns the hyperbolic anomaly in degrees between 0 and 360.0
Returns an error if the orbit is not hyperbolic.

:rtype: float


##### Method `hz` {#anise.astro.Orbit.hz}

>     def hz(
>         self,
>         /
>     )

Returns the orbital momentum value on the Z axis

:rtype: float


##### Method `inc_brouwer_short_deg` {#anise.astro.Orbit.inc_brouwer_short_deg}

>     def inc_brouwer_short_deg(
>         self,
>         /
>     )

Returns the Brouwer-short mean inclination in degrees.

:rtype: float


##### Method `inc_deg` {#anise.astro.Orbit.inc_deg}

>     def inc_deg(
>         self,
>         /
>     )

Returns the inclination in degrees

:rtype: float


##### Method `is_brouwer_short_valid` {#anise.astro.Orbit.is_brouwer_short_valid}

>     def is_brouwer_short_valid(
>         self,
>         /
>     )

Returns whether this state satisfies the requirement to compute the Mean Brouwer Short orbital
element set.

This is a conversion from GMAT's StateConversionUtil::CartesianToBrouwerMeanShort.
The details are at the log level <code>info</code>.
NOTE: Mean Brouwer Short are only defined around Earth. However, <code>nyx</code> does *not* check the
main celestial body around which the state is defined (GMAT does perform this verification).

:rtype: bool


##### Method `latitude_deg` {#anise.astro.Orbit.latitude_deg}

>     def latitude_deg(
>         self,
>         /
>     )

Returns the geodetic latitude (φ) in degrees. Value is between -180 and +180 degrees.

##### Frame warning
This state MUST be in the body fixed frame (e.g. ITRF93) prior to calling this function, or the computation is **invalid**.

:rtype: float


##### Method `latlongalt` {#anise.astro.Orbit.latlongalt}

>     def latlongalt(
>         self,
>         /
>     )

Returns the geodetic latitude, geodetic longitude, and geodetic height, respectively in degrees, degrees, and kilometers.

##### Algorithm
This uses the Heikkinen procedure, which is not iterative. The results match Vallado and GMAT.

:rtype: typing.Tuple


##### Method `light_time` {#anise.astro.Orbit.light_time}

>     def light_time(
>         self,
>         /
>     )

Returns the light time duration between this object and the origin of its reference frame.

:rtype: Duration


##### Method `longitude_360_deg` {#anise.astro.Orbit.longitude_360_deg}

>     def longitude_360_deg(
>         self,
>         /
>     )

Returns the geodetic longitude (λ) in degrees. Value is between 0 and 360 degrees.

##### Frame warning
This state MUST be in the body fixed frame (e.g. ITRF93) prior to calling this function, or the computation is **invalid**.

:rtype: float


##### Method `longitude_deg` {#anise.astro.Orbit.longitude_deg}

>     def longitude_deg(
>         self,
>         /
>     )

Returns the geodetic longitude (λ) in degrees. Value is between -180 and 180 degrees.

##### Frame warning
This state MUST be in the body fixed frame (e.g. ITRF93) prior to calling this function, or the computation is **invalid**.

:rtype: float


##### Method `ltan_deg` {#anise.astro.Orbit.ltan_deg}

>     def ltan_deg(
>         self,
>         /
>     )

Returns the Longitude of the Ascending Node (LTAN), or an error of equatorial orbits

:rtype: float


##### Method `ma_brouwer_short_deg` {#anise.astro.Orbit.ma_brouwer_short_deg}

>     def ma_brouwer_short_deg(
>         self,
>         /
>     )

Returns the Brouwer-short mean Mean Anomaly in degrees.

:rtype: float


##### Method `ma_deg` {#anise.astro.Orbit.ma_deg}

>     def ma_deg(
>         self,
>         /
>     )

Returns the mean anomaly in degrees

This is a conversion from GMAT's StateConversionUtil::TrueToMeanAnomaly

:rtype: float


##### Method `mean_motion_deg_s` {#anise.astro.Orbit.mean_motion_deg_s}

>     def mean_motion_deg_s(
>         self,
>         /
>     )

Returns the mean motion in degrees per seconds

:rtype: float


##### Method `periapsis_altitude_km` {#anise.astro.Orbit.periapsis_altitude_km}

>     def periapsis_altitude_km(
>         self,
>         /
>     )

Returns the altitude of periapsis (or perigee around Earth), in kilometers.

:rtype: float


##### Method `periapsis_km` {#anise.astro.Orbit.periapsis_km}

>     def periapsis_km(
>         self,
>         /
>     )

Returns the radius of periapsis (or perigee around Earth), in kilometers.

:rtype: float


##### Method `period` {#anise.astro.Orbit.period}

>     def period(
>         self,
>         /
>     )

Returns the period

:rtype: Duration


##### Method `raan_brouwer_short_deg` {#anise.astro.Orbit.raan_brouwer_short_deg}

>     def raan_brouwer_short_deg(
>         self,
>         /
>     )

Returns the Brouwer-short mean Right Ascension of the Ascending Node in degrees.

:rtype: float


##### Method `raan_deg` {#anise.astro.Orbit.raan_deg}

>     def raan_deg(
>         self,
>         /
>     )

Returns the right ascension of the ascending node in degrees

:rtype: float


##### Method `radius_km` {#anise.astro.Orbit.radius_km}

>     def radius_km(
>         self,
>         /
>     )

radius vector in km

:rtype: np.array


##### Method `rel_difference` {#anise.astro.Orbit.rel_difference}

>     def rel_difference(
>         self,
>         /,
>         other
>     )

Returns the relative difference between this orbit and another for the position and velocity, respectively the first and second return values.
Both return values are UNITLESS because the relative difference is computed as the absolute difference divided by the rmag and vmag of this object.
Raises an error if the frames do not match, if the position is zero or the velocity is zero.

:type other: Orbit
:rtype: typing.Tuple


##### Method `rel_pos_diff` {#anise.astro.Orbit.rel_pos_diff}

>     def rel_pos_diff(
>         self,
>         /,
>         other
>     )

Returns the relative position difference (unitless) between this orbit and another.
This is computed by dividing the absolute difference by the norm of this object's radius vector.
If the radius is zero, this function raises a math error.
Raises an error if the frames do not match or  (epochs do not need to match).

:type other: Orbit
:rtype: float


##### Method `rel_vel_diff` {#anise.astro.Orbit.rel_vel_diff}

>     def rel_vel_diff(
>         self,
>         /,
>         other
>     )

Returns the absolute velocity difference in kilometer per second between this orbit and another.
Raises an error if the frames do not match (epochs do not need to match).

:type other: Orbit
:rtype: float


##### Method `ric_difference` {#anise.astro.Orbit.ric_difference}

>     def ric_difference(
>         self,
>         /,
>         other
>     )

Returns a Cartesian state representing the RIC difference between self and other, in position and velocity (with transport theorem).
Refer to dcm_from_ric_to_inertial for details on the RIC frame.

##### Algorithm
1. Compute the difference between <code>other</code> and <code>self</code>
2. Compute the RIC DCM of <code>self</code>
3. Rotate the difference into the RIC frame of <code>self</code>
4. Strip the astrodynamical information from the frame, enabling only computations from <code>CartesianState</code>

:type other: Orbit
:rtype: Orbit


##### Method `right_ascension_deg` {#anise.astro.Orbit.right_ascension_deg}

>     def right_ascension_deg(
>         self,
>         /
>     )

Returns the right ascension of this orbit in degrees

:rtype: float


##### Method `rmag_km` {#anise.astro.Orbit.rmag_km}

>     def rmag_km(
>         self,
>         /
>     )

Returns the magnitude of the radius vector in km

:rtype: float


##### Method `rms_radius_km` {#anise.astro.Orbit.rms_radius_km}

>     def rms_radius_km(
>         self,
>         /,
>         other
>     )

Returns the root sum squared (RMS) radius difference between this state and another state, if both frames match (epoch does not need to match)

:type other: Orbit
:rtype: float


##### Method `rms_velocity_km_s` {#anise.astro.Orbit.rms_velocity_km_s}

>     def rms_velocity_km_s(
>         self,
>         /,
>         other
>     )

Returns the root sum squared (RMS) velocity difference between this state and another state, if both frames match (epoch does not need to match)

:type other: Orbit
:rtype: float


##### Method `rss_radius_km` {#anise.astro.Orbit.rss_radius_km}

>     def rss_radius_km(
>         self,
>         /,
>         other
>     )

Returns the root mean squared (RSS) radius difference between this state and another state, if both frames match (epoch does not need to match)

:type other: Orbit
:rtype: float


##### Method `rss_velocity_km_s` {#anise.astro.Orbit.rss_velocity_km_s}

>     def rss_velocity_km_s(
>         self,
>         /,
>         other
>     )

Returns the root mean squared (RSS) velocity difference between this state and another state, if both frames match (epoch does not need to match)

:type other: Orbit
:rtype: float


##### Method `semi_minor_axis_km` {#anise.astro.Orbit.semi_minor_axis_km}

>     def semi_minor_axis_km(
>         self,
>         /
>     )

Returns the semi minor axis in km, includes code for a hyperbolic orbit

:rtype: float


##### Method `semi_parameter_km` {#anise.astro.Orbit.semi_parameter_km}

>     def semi_parameter_km(
>         self,
>         /
>     )

Returns the semi parameter (or semilatus rectum)

:rtype: float


##### Method `set_aop_deg` {#anise.astro.Orbit.set_aop_deg}

>     def set_aop_deg(
>         self,
>         /,
>         new_aop_deg
>     )

Mutates this orbit to change the AOP

:type new_aop_deg: float
:rtype: None


##### Method `set_ecc` {#anise.astro.Orbit.set_ecc}

>     def set_ecc(
>         self,
>         /,
>         new_ecc
>     )

Mutates this orbit to change the ECC

:type new_ecc: float
:rtype: None


##### Method `set_inc_deg` {#anise.astro.Orbit.set_inc_deg}

>     def set_inc_deg(
>         self,
>         /,
>         new_inc_deg
>     )

Mutates this orbit to change the INC

:type new_inc_deg: float
:rtype: None


##### Method `set_raan_deg` {#anise.astro.Orbit.set_raan_deg}

>     def set_raan_deg(
>         self,
>         /,
>         new_raan_deg
>     )

Mutates this orbit to change the RAAN

:type new_raan_deg: float
:rtype: None


##### Method `set_sma_km` {#anise.astro.Orbit.set_sma_km}

>     def set_sma_km(
>         self,
>         /,
>         new_sma_km
>     )

Mutates this orbit to change the SMA

:type new_sma_km: float
:rtype: None


##### Method `set_ta_deg` {#anise.astro.Orbit.set_ta_deg}

>     def set_ta_deg(
>         self,
>         /,
>         new_ta_deg
>     )

Mutates this orbit to change the TA

:type new_ta_deg: float
:rtype: None


##### Method `sma_altitude_km` {#anise.astro.Orbit.sma_altitude_km}

>     def sma_altitude_km(
>         self,
>         /
>     )

Returns the SMA altitude in km

:rtype: float


##### Method `sma_brouwer_short_km` {#anise.astro.Orbit.sma_brouwer_short_km}

>     def sma_brouwer_short_km(
>         self,
>         /
>     )

Returns the Brouwer-short mean semi-major axis in km.

:rtype: float


##### Method `sma_km` {#anise.astro.Orbit.sma_km}

>     def sma_km(
>         self,
>         /
>     )

Returns the semi-major axis in km

:rtype: float


##### Method `ta_deg` {#anise.astro.Orbit.ta_deg}

>     def ta_deg(
>         self,
>         /
>     )

Returns the true anomaly in degrees between 0 and 360.0

NOTE: This function will emit a warning stating that the TA should be avoided if in a very near circular orbit
Code from <https://github.com/ChristopherRabotin/GMAT/blob/80bde040e12946a61dae90d9fc3538f16df34190/src/gmatutil/util/StateConversionUtil.cpp#L6835>

LIMITATION: For an orbit whose true anomaly is (very nearly) 0.0 or 180.0, this function may return either 0.0 or 180.0 with a very small time increment.
This is due to the precision of the cosine calculation: if the arccosine calculation is out of bounds, the sign of the cosine of the true anomaly is used
to determine whether the true anomaly should be 0.0 or 180.0. **In other words**, there is an ambiguity in the computation in the true anomaly exactly at 180.0 and 0.0.

:rtype: float


##### Method `ta_dot_deg_s` {#anise.astro.Orbit.ta_dot_deg_s}

>     def ta_dot_deg_s(
>         self,
>         /
>     )

Returns the time derivative of the true anomaly computed as the 360.0 degrees divided by the orbital period (in seconds).

:rtype: float


##### Method `tlong_deg` {#anise.astro.Orbit.tlong_deg}

>     def tlong_deg(
>         self,
>         /
>     )

Returns the true longitude in degrees

:rtype: float


##### Method `to_asn1` {#anise.astro.Orbit.to_asn1}

>     def to_asn1(
>         self,
>         /
>     )

Encodes this CartesianState (Orbit) into an ASN.1 DER encoded byte array.

:rtype: bytes


##### Method `velocity_declination_deg` {#anise.astro.Orbit.velocity_declination_deg}

>     def velocity_declination_deg(
>         self,
>         /
>     )

Returns the velocity declination of this orbit in degrees

:rtype: float


##### Method `velocity_km_s` {#anise.astro.Orbit.velocity_km_s}

>     def velocity_km_s(
>         self,
>         /
>     )

velocity vector in km/s

:rtype: np.array


##### Method `vinf_periapsis_km` {#anise.astro.Orbit.vinf_periapsis_km}

>     def vinf_periapsis_km(
>         self,
>         /,
>         turn_angle_degrees
>     )

Returns the radius of periapse in kilometers for the provided turn angle of this hyperbolic orbit.
Returns an error if the orbit is not hyperbolic.

:type turn_angle_degrees: float
:rtype: float


##### Method `vinf_turn_angle_deg` {#anise.astro.Orbit.vinf_turn_angle_deg}

>     def vinf_turn_angle_deg(
>         self,
>         /,
>         periapsis_km
>     )

Returns the turn angle in degrees for the provided radius of periapse passage of this hyperbolic orbit
Returns an error if the orbit is not hyperbolic.

:type periapsis_km: float
:rtype: float


##### Method `vmag_km_s` {#anise.astro.Orbit.vmag_km_s}

>     def vmag_km_s(
>         self,
>         /
>     )

Returns the magnitude of the velocity vector in km/s

:rtype: float


##### Method `vnc_difference` {#anise.astro.Orbit.vnc_difference}

>     def vnc_difference(
>         self,
>         /,
>         other
>     )

Returns a Cartesian state representing the VNC difference between self and other, in position and velocity (with transport theorem).
Refer to dcm_from_vnc_to_inertial for details on the VNC frame.

##### Algorithm
1. Compute the difference between <code>other</code> and <code>self</code>
2. Compute the VNC DCM of <code>self</code>
3. Rotate the difference into the VNC frame of <code>self</code>
4. Strip the astrodynamical information from the frame, enabling only computations from <code>CartesianState</code>

:type other: Orbit
:rtype: Orbit


##### Method `with_aop_deg` {#anise.astro.Orbit.with_aop_deg}

>     def with_aop_deg(
>         self,
>         /,
>         new_aop_deg
>     )

Returns a copy of the state with a new AOP

:type new_aop_deg: float
:rtype: Orbit


##### Method `with_apoapsis_periapsis_km` {#anise.astro.Orbit.with_apoapsis_periapsis_km}

>     def with_apoapsis_periapsis_km(
>         self,
>         /,
>         new_ra_km,
>         new_rp_km
>     )

Returns a copy of this state with the provided apoasis and periapsis

:type new_ra_km: float
:type new_rp_km: float
:rtype: Orbit


##### Method `with_ecc` {#anise.astro.Orbit.with_ecc}

>     def with_ecc(
>         self,
>         /,
>         new_ecc
>     )

Returns a copy of the state with a new ECC

:type new_ecc: float
:rtype: Orbit


##### Method `with_inc_deg` {#anise.astro.Orbit.with_inc_deg}

>     def with_inc_deg(
>         self,
>         /,
>         new_inc_deg
>     )

Returns a copy of the state with a new INC

:type new_inc_deg: float
:rtype: Orbit


##### Method `with_raan_deg` {#anise.astro.Orbit.with_raan_deg}

>     def with_raan_deg(
>         self,
>         /,
>         new_raan_deg
>     )

Returns a copy of the state with a new RAAN

:type new_raan_deg: float
:rtype: Orbit


##### Method `with_sma_km` {#anise.astro.Orbit.with_sma_km}

>     def with_sma_km(
>         self,
>         /,
>         new_sma_km
>     )

Returns a copy of the state with a new SMA

:type new_sma_km: float
:rtype: Orbit


##### Method `with_ta_deg` {#anise.astro.Orbit.with_ta_deg}

>     def with_ta_deg(
>         self,
>         /,
>         new_ta_deg
>     )

Returns a copy of the state with a new TA

:type new_ta_deg: float
:rtype: Orbit


### Class `SRPData` {#anise.astro.SRPData}

>     class SRPData(
>         area_m2,
>         coeff_reflectivity=None
>     )


#### Instance variables


##### Variable `area_m2` {#anise.astro.SRPData.area_m2}

Solar radiation pressure area in m^2 -- default 0.0
:rtype: float


##### Variable `coeff_reflectivity` {#anise.astro.SRPData.coeff_reflectivity}

Solar radiation pressure coefficient of reflectivity (C_r) -- default 1.8
:rtype: float


#### Methods


##### Method `from_asn1` {#anise.astro.SRPData.from_asn1}

>     def from_asn1(
>         data
>     )

Decodes an ASN.1 DER encoded byte array into an SRPData object.

:type data: bytes
:rtype: SRPData


##### Method `to_asn1` {#anise.astro.SRPData.to_asn1}

>     def to_asn1(
>         self,
>         /
>     )

Encodes this SRPData object into an ASN.1 DER encoded byte array.

:rtype: bytes


### Class `TerrainMask` {#anise.astro.TerrainMask}

>     class TerrainMask(
>         azimuth_deg,
>         elevation_mask_deg
>     )

TerrainMask is used to compute obstructions during AER calculations.

:type azimuth_deg: float
:type elevation_mask_deg: float


#### Instance variables


##### Variable `azimuth_deg` {#anise.astro.TerrainMask.azimuth_deg}

:rtype: float


##### Variable `elevation_mask_deg` {#anise.astro.TerrainMask.elevation_mask_deg}

:rtype: float


#### Methods


##### Method `from_flat_terrain` {#anise.astro.TerrainMask.from_flat_terrain}

>     def from_flat_terrain(
>         elevation_mask_deg
>     )

Creates a flat terrain mask with the provided elevation mask in degrees

:type elevation_mask_deg: float
:rtype: list

-----
Generated by *pdoc* 0.11.6 (<https://pdoc3.github.io>).
