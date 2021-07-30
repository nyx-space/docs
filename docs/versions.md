# Versions
This page lists the versions of Nyx and the changes you should expect between them. Nyx uses [semantic versioning](https://semver.org/): `major.minor.patch`. You will _not_ encounter any breaking changes between versions which share the same major version. For example, whatever code you develop for version `1.0.0` will also work for version `1.159.0`.

You may find an approximate roadmap [here](https://gitlab.com/nyx-space/nyx/-/milestones). It's important to note that Chris Rabotin develops this toolkit on his free time and is not paid for this development. Therefore milestone deadlines tend to slip.

## Version 1.0.0-beta.1
[Milestone](https://gitlab.com/nyx-space/nyx/-/milestones/17)

**Previous version:** 0.0.23

### New features
+ Propagations can now generate interpolated trajectories (using a Lagrange interpolation). This follows a multithreaded [Map-Reduce](https://en.wikipedia.org/wiki/MapReduce) pattern so no computational slowdown is noticeable.
+ B-Plane targeting for interplanetary mission design
+ Import/export trajectories from STK, GMAT, or a custom format.
+ Thorough documentation (this website is new!).
+ Orbit determination can now iterate on a solution until convergence


### Improvements
+ Event finding has been moved to interpolated trajectories allowing for significantly increased precision. For example, Nyx can now detect an upcoming Eclipse event as soon as the Penumbra reaches 2% of shadowing. It is also possible to search for any orbital event in any celestial frame.
+ Propagation conditional stopping has been moved to the interpolated trajectories allowing for propagation until a specific event in another frame. For example, Nyx can propagate a spacecraft in the EME2000 frame but stop the propagation on the third passage after true anomaly in a Moon J2000 frame is at 35.2 degrees.
+ Full refactoring of `Dynamics`, which is how the equations of motions are modeled.
+ Switch to hifitime 2.x. This computes time using fractions allowing for picosecond precision, likely one of the more precise time computation software so far.
+ Removed most dynamic memory allocations

### Bug fixes
+ Fixed eclipsing computation and solar radiation pressure computation, validated against GMAT
+ Fixed body fixed rotations to/from inertial frames correctly account for the transport theorem, now validated against SPICE
+ Fixed spherical harmonics when the integration frame has a different center than the harmonics frame (it now performs the translation correctly instead of only doing a rotation which was wrong).
+ Fixed topocentric frame computation, now validated against GMAT for OD measurement generation
+ Fixed hyperdual number dynamics gradient computation to exactly match the real numbers computation
+ Fixed smoothing, but SNC is not yet accounted for in smoothing

--8<-- "includes/Abbreviations.md"