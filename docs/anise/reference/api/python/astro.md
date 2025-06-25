
    
# Module `anise.astro` {#anise.astro}

    
## Sub-modules

* [anise.astro.constants](#anise.astro.constants)

    
## Classes

    
### Class `AzElRange` {#anise.astro.AzElRange}

>     class AzElRange(
>         epoch,
>         azimuth_deg,
>         elevation_deg,
>         range_km,
>         range_rate_km_s,
>         obstructed_by=None
>     )

A structure that stores the result of Azimuth, Elevation, Range, Range rate calculation.

:type epoch: Epoch
:type azimuth_deg: float
:type elevation_deg: float
:type range_km: float
:type range_rate_km_s: float
:type obstructed_by: Frame, optional
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

    
##### Variable `obstructed_by` {#anise.astro.AzElRange.obstructed_by}

:rtype: Frame

    
##### Variable `range_km` {#anise.astro.AzElRange.range_km}

:rtype: float

    
##### Variable `range_rate_km_s` {#anise.astro.AzElRange.range_rate_km_s}

:rtype: float

    
#### Methods

    
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
:type mu_km3_s2: float, optional
:type shape: Ellipsoid, optional
:rtype: Frame

    
#### Instance variables

    
##### Variable `ephemeris_id` {#anise.astro.Frame.ephemeris_id}

:rtype: int

    
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

    
##### Method `is_celestial` {#anise.astro.Frame.is_celestial}

>     def is_celestial(
>         self,
>         /
>     )

Returns whether this is a celestial frame

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

    
### Class `Occultation` {#anise.astro.Occultation}

>     class Occultation(
>         ...
>     )

Stores the result of an occultation computation with the occulation percentage
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
>         x_km,
>         y_km,
>         z_km,
>         vx_km_s,
>         vy_km_s,
>         vz_km_s,
>         epoch,
>         frame
>     )

Defines a Cartesian state in a given frame at a given epoch in a given time scale. Radius data is expressed in kilometers. Velocity data is expressed in kilometers per second.
Regardless of the constructor used, this struct stores all the state information in Cartesian coordinates as these are always non singular.

Unless noted otherwise, algorithms are from GMAT 2016a [StateConversionUtil.cpp](https://github.com/ChristopherRabotin/GMAT/blob/37201a6290e7f7b941bc98ee973a527a5857104b/src/base/util/StateConversionUtil.cpp).

:type x_km: float
:type y_km: float
:type z_km: float
:type vx_km_s: float
:type vy_km_s: float
:type vz_km_s: float
:type epoch: Epoch
:type frame: Frame
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

    
##### Variable `vz_km` {#anise.astro.Orbit.vz_km}

:type vz_km_s: float
:rtype: None

    
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
:rtype: None

    
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

Adjusts the true anomaly of this orbit using the mean anomaly.

##### Astrodynamics note
This is not a true propagation of the orbit. This is akin to a two body propagation ONLY without any other force models applied.
Use Nyx for high fidelity propagation.

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
:rtype: numpy.array

    
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
>         /,
>         _from
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

:type _from: float
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

    
##### Method `fpa_deg` {#anise.astro.Orbit.fpa_deg}

>     def fpa_deg(
>         self,
>         /
>     )

Returns the flight path angle in degrees

:rtype: float

    
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
>         angular_velocity,
>         epoch,
>         frame
>     )

Creates a new Orbit from the latitude (φ), longitude (λ) and height (in km) with respect to the frame's ellipsoid given the angular velocity.

**Units:** degrees, degrees, km, rad/s
NOTE: This computation differs from the spherical coordinates because we consider the flattening of body.
Reference: G. Xu and Y. Xu, "GPS", DOI 10.1007/978-3-662-50367-6_2, 2016

:type latitude_deg: float
:type longitude_deg: float
:type height_km: float
:type angular_velocity: float
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

Returns the period in seconds

:rtype: Duration

    
##### Method `raan_deg` {#anise.astro.Orbit.raan_deg}

>     def raan_deg(
>         self,
>         /
>     )

Returns the right ascension of the ascending node in degrees

:rtype: float

    
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
1. Compute the RIC DCM of self
2. Rotate self into the RIC frame
3. Rotation other into the RIC frame
4. Compute the difference between these two states
5. Strip the astrodynamical information from the frame, enabling only computations from <code>CartesianState</code>

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

    
##### Method `velocity_declination_deg` {#anise.astro.Orbit.velocity_declination_deg}

>     def velocity_declination_deg(
>         self,
>         /
>     )

Returns the velocity declination of this orbit in degrees

:rtype: float

    
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
1. Compute the VNC DCM of self
2. Rotate self into the VNC frame
3. Rotation other into the VNC frame
4. Compute the difference between these two states
5. Strip the astrodynamical information from the frame, enabling only computations from <code>CartesianState</code>

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

    
# Module `anise.astro.constants` {#anise.astro.constants}

    
## Classes

    
### Class `CelestialObjects` {#anise.astro.constants.CelestialObjects}

>     class CelestialObjects(
>         ...
>     )

    
#### Class variables

    
##### Variable `EARTH` {#anise.astro.constants.CelestialObjects.EARTH}

    
##### Variable `EARTH_MOON_BARYCENTER` {#anise.astro.constants.CelestialObjects.EARTH_MOON_BARYCENTER}

    
##### Variable `JUPITER` {#anise.astro.constants.CelestialObjects.JUPITER}

    
##### Variable `JUPITER_BARYCENTER` {#anise.astro.constants.CelestialObjects.JUPITER_BARYCENTER}

    
##### Variable `MARS` {#anise.astro.constants.CelestialObjects.MARS}

    
##### Variable `MARS_BARYCENTER` {#anise.astro.constants.CelestialObjects.MARS_BARYCENTER}

    
##### Variable `MERCURY` {#anise.astro.constants.CelestialObjects.MERCURY}

    
##### Variable `MOON` {#anise.astro.constants.CelestialObjects.MOON}

    
##### Variable `NEPTUNE` {#anise.astro.constants.CelestialObjects.NEPTUNE}

    
##### Variable `NEPTUNE_BARYCENTER` {#anise.astro.constants.CelestialObjects.NEPTUNE_BARYCENTER}

    
##### Variable `PLUTO_BARYCENTER` {#anise.astro.constants.CelestialObjects.PLUTO_BARYCENTER}

    
##### Variable `SATURN` {#anise.astro.constants.CelestialObjects.SATURN}

    
##### Variable `SATURN_BARYCENTER` {#anise.astro.constants.CelestialObjects.SATURN_BARYCENTER}

    
##### Variable `SOLAR_SYSTEM_BARYCENTER` {#anise.astro.constants.CelestialObjects.SOLAR_SYSTEM_BARYCENTER}

    
##### Variable `SUN` {#anise.astro.constants.CelestialObjects.SUN}

    
##### Variable `URANUS` {#anise.astro.constants.CelestialObjects.URANUS}

    
##### Variable `URANUS_BARYCENTER` {#anise.astro.constants.CelestialObjects.URANUS_BARYCENTER}

    
##### Variable `VENUS` {#anise.astro.constants.CelestialObjects.VENUS}

    
### Class `Frames` {#anise.astro.constants.Frames}

>     class Frames(
>         ...
>     )

    
#### Class variables

    
##### Variable `EARTH_ECLIPJ2000` {#anise.astro.constants.Frames.EARTH_ECLIPJ2000}

    
##### Variable `EARTH_ITRF93` {#anise.astro.constants.Frames.EARTH_ITRF93}

    
##### Variable `EARTH_J2000` {#anise.astro.constants.Frames.EARTH_J2000}

    
##### Variable `EARTH_MOON_BARYCENTER_J2000` {#anise.astro.constants.Frames.EARTH_MOON_BARYCENTER_J2000}

    
##### Variable `EME2000` {#anise.astro.constants.Frames.EME2000}

    
##### Variable `IAU_EARTH_FRAME` {#anise.astro.constants.Frames.IAU_EARTH_FRAME}

    
##### Variable `IAU_JUPITER_FRAME` {#anise.astro.constants.Frames.IAU_JUPITER_FRAME}

    
##### Variable `IAU_MARS_FRAME` {#anise.astro.constants.Frames.IAU_MARS_FRAME}

    
##### Variable `IAU_MERCURY_FRAME` {#anise.astro.constants.Frames.IAU_MERCURY_FRAME}

    
##### Variable `IAU_MOON_FRAME` {#anise.astro.constants.Frames.IAU_MOON_FRAME}

    
##### Variable `IAU_NEPTUNE_FRAME` {#anise.astro.constants.Frames.IAU_NEPTUNE_FRAME}

    
##### Variable `IAU_SATURN_FRAME` {#anise.astro.constants.Frames.IAU_SATURN_FRAME}

    
##### Variable `IAU_URANUS_FRAME` {#anise.astro.constants.Frames.IAU_URANUS_FRAME}

    
##### Variable `IAU_VENUS_FRAME` {#anise.astro.constants.Frames.IAU_VENUS_FRAME}

    
##### Variable `JUPITER_BARYCENTER_J2000` {#anise.astro.constants.Frames.JUPITER_BARYCENTER_J2000}

    
##### Variable `MARS_BARYCENTER_J2000` {#anise.astro.constants.Frames.MARS_BARYCENTER_J2000}

    
##### Variable `MERCURY_J2000` {#anise.astro.constants.Frames.MERCURY_J2000}

    
##### Variable `MOON_J2000` {#anise.astro.constants.Frames.MOON_J2000}

    
##### Variable `MOON_ME_DE421_FRAME` {#anise.astro.constants.Frames.MOON_ME_DE421_FRAME}

    
##### Variable `MOON_ME_DE440_ME421_FRAME` {#anise.astro.constants.Frames.MOON_ME_DE440_ME421_FRAME}

    
##### Variable `MOON_ME_FRAME` {#anise.astro.constants.Frames.MOON_ME_FRAME}

    
##### Variable `MOON_PA_DE421_FRAME` {#anise.astro.constants.Frames.MOON_PA_DE421_FRAME}

    
##### Variable `MOON_PA_DE440_FRAME` {#anise.astro.constants.Frames.MOON_PA_DE440_FRAME}

    
##### Variable `MOON_PA_FRAME` {#anise.astro.constants.Frames.MOON_PA_FRAME}

    
##### Variable `NEPTUNE_BARYCENTER_J2000` {#anise.astro.constants.Frames.NEPTUNE_BARYCENTER_J2000}

    
##### Variable `PLUTO_BARYCENTER_J2000` {#anise.astro.constants.Frames.PLUTO_BARYCENTER_J2000}

    
##### Variable `SATURN_BARYCENTER_J2000` {#anise.astro.constants.Frames.SATURN_BARYCENTER_J2000}

    
##### Variable `SSB_J2000` {#anise.astro.constants.Frames.SSB_J2000}

    
##### Variable `SUN_J2000` {#anise.astro.constants.Frames.SUN_J2000}

    
##### Variable `URANUS_BARYCENTER_J2000` {#anise.astro.constants.Frames.URANUS_BARYCENTER_J2000}

    
##### Variable `VENUS_J2000` {#anise.astro.constants.Frames.VENUS_J2000}

    
### Class `Orientations` {#anise.astro.constants.Orientations}

>     class Orientations(
>         ...
>     )

    
#### Class variables

    
##### Variable `ECLIPJ2000` {#anise.astro.constants.Orientations.ECLIPJ2000}

    
##### Variable `IAU_EARTH` {#anise.astro.constants.Orientations.IAU_EARTH}

    
##### Variable `IAU_JUPITER` {#anise.astro.constants.Orientations.IAU_JUPITER}

    
##### Variable `IAU_MARS` {#anise.astro.constants.Orientations.IAU_MARS}

    
##### Variable `IAU_MERCURY` {#anise.astro.constants.Orientations.IAU_MERCURY}

    
##### Variable `IAU_MOON` {#anise.astro.constants.Orientations.IAU_MOON}

    
##### Variable `IAU_NEPTUNE` {#anise.astro.constants.Orientations.IAU_NEPTUNE}

    
##### Variable `IAU_SATURN` {#anise.astro.constants.Orientations.IAU_SATURN}

    
##### Variable `IAU_URANUS` {#anise.astro.constants.Orientations.IAU_URANUS}

    
##### Variable `IAU_VENUS` {#anise.astro.constants.Orientations.IAU_VENUS}

    
##### Variable `ITRF93` {#anise.astro.constants.Orientations.ITRF93}

    
##### Variable `J2000` {#anise.astro.constants.Orientations.J2000}

    
##### Variable `MOON_ME` {#anise.astro.constants.Orientations.MOON_ME}

    
##### Variable `MOON_ME_DE421` {#anise.astro.constants.Orientations.MOON_ME_DE421}

    
##### Variable `MOON_ME_DE440_ME421` {#anise.astro.constants.Orientations.MOON_ME_DE440_ME421}

    
##### Variable `MOON_PA` {#anise.astro.constants.Orientations.MOON_PA}

    
##### Variable `MOON_PA_DE421` {#anise.astro.constants.Orientations.MOON_PA_DE421}

    
##### Variable `MOON_PA_DE440` {#anise.astro.constants.Orientations.MOON_PA_DE440}

    
### Class `UsualConstants` {#anise.astro.constants.UsualConstants}

>     class UsualConstants(
>         ...
>     )

    
#### Class variables

    
##### Variable `MEAN_EARTH_ANGULAR_VELOCITY_DEG_S` {#anise.astro.constants.UsualConstants.MEAN_EARTH_ANGULAR_VELOCITY_DEG_S}

    
##### Variable `MEAN_MOON_ANGULAR_VELOCITY_DEG_S` {#anise.astro.constants.UsualConstants.MEAN_MOON_ANGULAR_VELOCITY_DEG_S}

    
##### Variable `SPEED_OF_LIGHT_KM_S` {#anise.astro.constants.UsualConstants.SPEED_OF_LIGHT_KM_S}

-----
Generated by *pdoc* 0.11.6 (<https://pdoc3.github.io>).
