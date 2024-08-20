# Module `astro`

    
## Classes

    
### Class `AzElRange`

>     class AzElRange(
>         epoch,
>         azimuth_deg,
>         elevation_deg,
>         range_km,
>         range_rate_km_s
>     )

A structure that stores the result of Azimuth, Elevation, Range, Range rate calculation.

# Algorithm

    
#### Instance variables

    
##### Variable `azimuth_deg`

Return an attribute of instance, which is of type owner.

    
##### Variable `elevation_deg`

Return an attribute of instance, which is of type owner.

    
##### Variable `epoch`

Return an attribute of instance, which is of type owner.

    
##### Variable `range_km`

Return an attribute of instance, which is of type owner.

    
##### Variable `range_rate_km_s`

Return an attribute of instance, which is of type owner.

    
#### Methods

    
##### Method `is_valid`

>     def is_valid(
>         self,
>         /
>     )

Returns false if the range is less than one millimeter, or any of the angles are NaN.

    
### Class `Ellipsoid`

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

    
#### Instance variables

    
##### Variable `polar_radius_km`

Return an attribute of instance, which is of type owner.

    
##### Variable `semi_major_equatorial_radius_km`

Return an attribute of instance, which is of type owner.

    
##### Variable `semi_minor_equatorial_radius_km`

Return an attribute of instance, which is of type owner.

    
#### Methods

    
##### Method `flattening`

>     def flattening(
>         self,
>         /
>     )

Returns the flattening ratio, computed from the mean equatorial radius and the polar radius

    
##### Method `is_sphere`

>     def is_sphere(
>         self,
>         /
>     )

    
##### Method `is_spheroid`

>     def is_spheroid(
>         self,
>         /
>     )

    
##### Method `mean_equatorial_radius_km`

>     def mean_equatorial_radius_km(
>         self,
>         /
>     )

Returns the mean equatorial radius in kilometers

    
### Class `Frame`

>     class Frame(
>         ephemeris_id,
>         orientation_id,
>         mu_km3_s2=None,
>         shape=None
>     )

A Frame uniquely defined by its ephemeris center and orientation. Refer to FrameDetail for frames combined with parameters.

    
#### Instance variables

    
##### Variable `ephemeris_id`

Return an attribute of instance, which is of type owner.

    
##### Variable `orientation_id`

Return an attribute of instance, which is of type owner.

    
##### Variable `shape`

Shape of the geoid of this frame, only defined on geodetic frames

    
#### Methods

    
##### Method `ephem_origin_id_match`

>     def ephem_origin_id_match(
>         self,
>         /,
>         other_id
>     )

Returns true if the ephemeris origin is equal to the provided ID

    
##### Method `ephem_origin_match`

>     def ephem_origin_match(
>         self,
>         /,
>         other
>     )

Returns true if the ephemeris origin is equal to the provided frame

    
##### Method `flattening`

>     def flattening(
>         self,
>         /
>     )

Returns the flattening ratio (unitless)

    
##### Method `is_celestial`

>     def is_celestial(
>         self,
>         /
>     )

Returns whether this is a celestial frame

    
##### Method `is_geodetic`

>     def is_geodetic(
>         self,
>         /
>     )

Returns whether this is a geodetic frame

    
##### Method `mean_equatorial_radius_km`

>     def mean_equatorial_radius_km(
>         self,
>         /
>     )

Returns the mean equatorial radius in km, if defined

    
##### Method `mu_km3_s2`

>     def mu_km3_s2(
>         self,
>         /
>     )

Returns the gravitational parameters of this frame, if defined

    
##### Method `orient_origin_id_match`

>     def orient_origin_id_match(
>         self,
>         /,
>         other_id
>     )

Returns true if the orientation origin is equal to the provided ID

    
##### Method `orient_origin_match`

>     def orient_origin_match(
>         self,
>         /,
>         other
>     )

Returns true if the orientation origin is equal to the provided frame

    
##### Method `polar_radius_km`

>     def polar_radius_km(
>         self,
>         /
>     )

Returns the polar radius in km, if defined

    
##### Method `semi_major_radius_km`

>     def semi_major_radius_km(
>         self,
>         /
>     )

Returns the semi major radius of the tri-axial ellipoid shape of this frame, if defined

    
##### Method `strip`

>     def strip(
>         self,
>         /
>     )

Removes the graviational parameter and the shape information from this frame.
Use this to prevent astrodynamical computations.

    
##### Method `with_ephem`

>     def with_ephem(
>         self,
>         /,
>         new_ephem_id
>     )

Returns a copy of this Frame whose ephemeris ID is set to the provided ID

    
##### Method `with_mu_km3_s2`

>     def with_mu_km3_s2(
>         self,
>         /,
>         mu_km3_s2
>     )

Returns a copy of this frame with the graviational parameter set to the new value.

    
##### Method `with_orient`

>     def with_orient(
>         self,
>         /,
>         new_orient_id
>     )

Returns a copy of this Frame whose orientation ID is set to the provided ID

    
### Class `Orbit`

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

    
#### Instance variables

    
##### Variable `epoch`

Return an attribute of instance, which is of type owner.

    
##### Variable `frame`

Return an attribute of instance, which is of type owner.

    
##### Variable `vx_km_s`

Return an attribute of instance, which is of type owner.

    
##### Variable `vy_km_s`

Return an attribute of instance, which is of type owner.

    
##### Variable `vz_km_s`

Return an attribute of instance, which is of type owner.

    
##### Variable `x_km`

Return an attribute of instance, which is of type owner.

    
##### Variable `y_km`

Return an attribute of instance, which is of type owner.

    
##### Variable `z_km`

Return an attribute of instance, which is of type owner.

    
#### Methods

    
##### Method `add_aop_deg`

>     def add_aop_deg(
>         self,
>         /,
>         delta_aop_deg
>     )

Returns a copy of the state with a provided AOP added to the current one

    
##### Method `add_apoapsis_periapsis_km`

>     def add_apoapsis_periapsis_km(
>         self,
>         /,
>         delta_ra_km,
>         delta_rp_km
>     )

Returns a copy of this state with the provided apoasis and periapsis added to the current values

    
##### Method `add_ecc`

>     def add_ecc(
>         self,
>         /,
>         delta_ecc
>     )

Returns a copy of the state with a provided ECC added to the current one

    
##### Method `add_inc_deg`

>     def add_inc_deg(
>         self,
>         /,
>         delta_inc_deg
>     )

Returns a copy of the state with a provided INC added to the current one

    
##### Method `add_raan_deg`

>     def add_raan_deg(
>         self,
>         /,
>         delta_raan_deg
>     )

Returns a copy of the state with a provided RAAN added to the current one

    
##### Method `add_sma_km`

>     def add_sma_km(
>         self,
>         /,
>         delta_sma
>     )

Returns a copy of the state with a provided SMA added to the current one

    
##### Method `add_ta_deg`

>     def add_ta_deg(
>         self,
>         /,
>         delta_ta_deg
>     )

Returns a copy of the state with a provided TA added to the current one

    
##### Method `aol_deg`

>     def aol_deg(
>         self,
>         /
>     )

Returns the argument of latitude in degrees

NOTE: If the orbit is near circular, the AoL will be computed from the true longitude
instead of relying on the ill-defined true anomaly.

    
##### Method `aop_deg`

>     def aop_deg(
>         self,
>         /
>     )

Returns the argument of periapsis in degrees

    
##### Method `apoapsis_altitude_km`

>     def apoapsis_altitude_km(
>         self,
>         /
>     )

Returns the altitude of apoapsis (or apogee around Earth), in kilometers.

    
##### Method `apoapsis_km`

>     def apoapsis_km(
>         self,
>         /
>     )

Returns the radius of apoapsis (or apogee around Earth), in kilometers.

    
##### Method `at_epoch`

>     def at_epoch(
>         self,
>         /,
>         new_epoch
>     )

Adjusts the true anomaly of this orbit using the mean anomaly.

##### Astrodynamics note
This is not a true propagation of the orbit. This is akin to a two body propagation ONLY without any other force models applied.
Use Nyx for high fidelity propagation.

    
##### Method `c3_km2_s2`

>     def c3_km2_s2(
>         self,
>         /
>     )

Returns the $C_3$ of this orbit in km^2/s^2

    
##### Method `declination_deg`

>     def declination_deg(
>         self,
>         /
>     )

Returns the declination of this orbit in degrees

    
##### Method `distance_to_km`

>     def distance_to_km(
>         self,
>         /,
>         other
>     )

Returns the distance in kilometers between this state and another state, if both frame match (epoch does not need to match).

    
##### Method `ea_deg`

>     def ea_deg(
>         self,
>         /
>     )

Returns the eccentric anomaly in degrees

This is a conversion from GMAT's StateConversionUtil::TrueToEccentricAnomaly

    
##### Method `ecc`

>     def ecc(
>         self,
>         /
>     )

Returns the eccentricity (no unit)

    
##### Method `energy_km2_s2`

>     def energy_km2_s2(
>         self,
>         /
>     )

Returns the specific mechanical energy in km^2/s^2

    
##### Method `eq_within`

>     def eq_within(
>         self,
>         /,
>         other,
>         radial_tol_km,
>         velocity_tol_km_s
>     )

Returns whether this orbit and another are equal within the specified radial and velocity absolute tolerances

    
##### Method `fpa_deg`

>     def fpa_deg(
>         self,
>         /
>     )

Returns the flight path angle in degrees

    
##### Method `from_cartesian`

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

    
##### Method `from_keplerian`

>     def from_keplerian(
>         sma,
>         ecc,
>         inc,
>         raan,
>         aop,
>         ta,
>         epoch,
>         frame
>     )

Creates a new Orbit around the provided Celestial or Geoid frame from the Keplerian orbital elements.

**Units:** km, none, degrees, degrees, degrees, degrees

NOTE: The state is defined in Cartesian coordinates as they are non-singular. This causes rounding
errors when creating a state from its Keplerian orbital elements (cf. the state tests).
One should expect these errors to be on the order of 1e-12.

    
##### Method `from_keplerian_altitude`

>     def from_keplerian_altitude(
>         sma_altitude,
>         ecc,
>         inc,
>         raan,
>         aop,
>         ta,
>         epoch,
>         frame
>     )

Creates a new Orbit from the provided semi-major axis altitude in kilometers

    
##### Method `from_keplerian_apsis_altitude`

>     def from_keplerian_apsis_altitude(
>         apo_alt,
>         peri_alt,
>         inc,
>         raan,
>         aop,
>         ta,
>         epoch,
>         frame
>     )

Creates a new Orbit from the provided altitudes of apoapsis and periapsis, in kilometers

    
##### Method `from_keplerian_apsis_radii`

>     def from_keplerian_apsis_radii(
>         r_a,
>         r_p,
>         inc,
>         raan,
>         aop,
>         ta,
>         epoch,
>         frame
>     )

Attempts to create a new Orbit from the provided radii of apoapsis and periapsis, in kilometers

    
##### Method `from_keplerian_mean_anomaly`

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

    
##### Method `from_latlongalt`

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

    
##### Method `height_km`

>     def height_km(
>         self,
>         /
>     )

Returns the geodetic height in km.

Reference: Vallado, 4th Ed., Algorithm 12 page 172.

    
##### Method `hmag`

>     def hmag(
>         self,
>         /
>     )

Returns the norm of the orbital momentum

    
##### Method `hx`

>     def hx(
>         self,
>         /
>     )

Returns the orbital momentum value on the X axis

    
##### Method `hy`

>     def hy(
>         self,
>         /
>     )

Returns the orbital momentum value on the Y axis

    
##### Method `hyperbolic_anomaly_deg`

>     def hyperbolic_anomaly_deg(
>         self,
>         /
>     )

Returns the hyperbolic anomaly in degrees between 0 and 360.0
Returns an error if the orbit is not hyperbolic.

    
##### Method `hz`

>     def hz(
>         self,
>         /
>     )

Returns the orbital momentum value on the Z axis

    
##### Method `inc_deg`

>     def inc_deg(
>         self,
>         /
>     )

Returns the inclination in degrees

    
##### Method `is_brouwer_short_valid`

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

    
##### Method `latitude_deg`

>     def latitude_deg(
>         self,
>         /
>     )

Returns the geodetic latitude (φ) in degrees. Value is between -180 and +180 degrees.

##### Frame warning
This state MUST be in the body fixed frame (e.g. ITRF93) prior to calling this function, or the computation is **invalid**.

    
##### Method `latlongalt`

>     def latlongalt(
>         self,
>         /
>     )

Returns the geodetic latitude, geodetic longitude, and geodetic height, respectively in degrees, degrees, and kilometers.

##### Algorithm
This uses the Heikkinen procedure, which is not iterative. The results match Vallado and GMAT.

    
##### Method `light_time`

>     def light_time(
>         self,
>         /
>     )

Returns the light time duration between this object and the origin of its reference frame.

    
##### Method `longitude_deg`

>     def longitude_deg(
>         self,
>         /
>     )

Returns the geodetic longitude (λ) in degrees. Value is between 0 and 360 degrees.

##### Frame warning
This state MUST be in the body fixed frame (e.g. ITRF93) prior to calling this function, or the computation is **invalid**.

    
##### Method `ma_deg`

>     def ma_deg(
>         self,
>         /
>     )

Returns the mean anomaly in degrees

This is a conversion from GMAT's StateConversionUtil::TrueToMeanAnomaly

    
##### Method `periapsis_altitude_km`

>     def periapsis_altitude_km(
>         self,
>         /
>     )

Returns the altitude of periapsis (or perigee around Earth), in kilometers.

    
##### Method `periapsis_km`

>     def periapsis_km(
>         self,
>         /
>     )

Returns the radius of periapsis (or perigee around Earth), in kilometers.

    
##### Method `period`

>     def period(
>         self,
>         /
>     )

Returns the period in seconds

    
##### Method `raan_deg`

>     def raan_deg(
>         self,
>         /
>     )

Returns the right ascension of the ascending node in degrees

    
##### Method `ric_difference`

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

    
##### Method `right_ascension_deg`

>     def right_ascension_deg(
>         self,
>         /
>     )

Returns the right ascension of this orbit in degrees

    
##### Method `rmag_km`

>     def rmag_km(
>         self,
>         /
>     )

Returns the magnitude of the radius vector in km

    
##### Method `rss_radius_km`

>     def rss_radius_km(
>         self,
>         /,
>         other
>     )

Returns the root mean squared (RSS) radius difference between this state and another state, if both frames match (epoch does not need to match)

    
##### Method `rss_velocity_km_s`

>     def rss_velocity_km_s(
>         self,
>         /,
>         other
>     )

Returns the root mean squared (RSS) velocity difference between this state and another state, if both frames match (epoch does not need to match)

    
##### Method `semi_minor_axis_km`

>     def semi_minor_axis_km(
>         self,
>         /
>     )

Returns the semi minor axis in km, includes code for a hyperbolic orbit

    
##### Method `semi_parameter_km`

>     def semi_parameter_km(
>         self,
>         /
>     )

Returns the semi parameter (or semilatus rectum)

    
##### Method `set_aop_deg`

>     def set_aop_deg(
>         self,
>         /,
>         new_aop_deg
>     )

Mutates this orbit to change the AOP

    
##### Method `set_ecc`

>     def set_ecc(
>         self,
>         /,
>         new_ecc
>     )

Mutates this orbit to change the ECC

    
##### Method `set_inc_deg`

>     def set_inc_deg(
>         self,
>         /,
>         new_inc_deg
>     )

Mutates this orbit to change the INC

    
##### Method `set_raan_deg`

>     def set_raan_deg(
>         self,
>         /,
>         new_raan_deg
>     )

Mutates this orbit to change the RAAN

    
##### Method `set_sma_km`

>     def set_sma_km(
>         self,
>         /,
>         new_sma_km
>     )

Mutates this orbit to change the SMA

    
##### Method `set_ta_deg`

>     def set_ta_deg(
>         self,
>         /,
>         new_ta_deg
>     )

Mutates this orbit to change the TA

    
##### Method `sma_altitude_km`

>     def sma_altitude_km(
>         self,
>         /
>     )

Returns the SMA altitude in km

    
##### Method `sma_km`

>     def sma_km(
>         self,
>         /
>     )

Returns the semi-major axis in km

    
##### Method `ta_deg`

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

    
##### Method `ta_dot_deg_s`

>     def ta_dot_deg_s(
>         self,
>         /
>     )

Returns the time derivative of the true anomaly computed as the 360.0 degrees divided by the orbital period (in seconds).

    
##### Method `tlong_deg`

>     def tlong_deg(
>         self,
>         /
>     )

Returns the true longitude in degrees

    
##### Method `velocity_declination_deg`

>     def velocity_declination_deg(
>         self,
>         /
>     )

Returns the velocity declination of this orbit in degrees

    
##### Method `vinf_periapsis_km`

>     def vinf_periapsis_km(
>         self,
>         /,
>         turn_angle_degrees
>     )

Returns the radius of periapse in kilometers for the provided turn angle of this hyperbolic orbit.
Returns an error if the orbit is not hyperbolic.

    
##### Method `vinf_turn_angle_deg`

>     def vinf_turn_angle_deg(
>         self,
>         /,
>         periapsis_km
>     )

Returns the turn angle in degrees for the provided radius of periapse passage of this hyperbolic orbit
Returns an error if the orbit is not hyperbolic.

    
##### Method `vmag_km_s`

>     def vmag_km_s(
>         self,
>         /
>     )

Returns the magnitude of the velocity vector in km/s

    
##### Method `with_aop_deg`

>     def with_aop_deg(
>         self,
>         /,
>         new_aop_deg
>     )

Returns a copy of the state with a new AOP

    
##### Method `with_apoapsis_periapsis_km`

>     def with_apoapsis_periapsis_km(
>         self,
>         /,
>         new_ra_km,
>         new_rp_km
>     )

Returns a copy of this state with the provided apoasis and periapsis

    
##### Method `with_ecc`

>     def with_ecc(
>         self,
>         /,
>         new_ecc
>     )

Returns a copy of the state with a new ECC

    
##### Method `with_inc_deg`

>     def with_inc_deg(
>         self,
>         /,
>         new_inc_deg
>     )

Returns a copy of the state with a new INC

    
##### Method `with_raan_deg`

>     def with_raan_deg(
>         self,
>         /,
>         new_raan_deg
>     )

Returns a copy of the state with a new RAAN

    
##### Method `with_sma_km`

>     def with_sma_km(
>         self,
>         /,
>         new_sma_km
>     )

Returns a copy of the state with a new SMA

    
##### Method `with_ta_deg`

>     def with_ta_deg(
>         self,
>         /,
>         new_ta_deg
>     )

Returns a copy of the state with a new TA

-----
Generated by *pdoc* 0.10.0 (<https://pdoc3.github.io>).
