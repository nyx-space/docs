# Versions
This page lists the versions of Nyx and the changes you should expect between them. Nyx uses [semantic versioning](https://semver.org/): `major.minor.patch`. You will _not_ encounter any breaking changes between versions which share the same major version. For example, whatever code you develop for version `1.0.0` will also work for version `1.159.0`.

You may find an approximate roadmap [here](https://gitlab.com/nyx-space/nyx/-/milestones). It's important to note that Chris Rabotin develops this toolkit on his free time and is not paid for this development. Therefore milestone deadlines tend to slip.

## Version 1.0.0
[Milestone](https://gitlab.com/nyx-space/nyx/-/milestones/17)

**Previous version:** 0.0.23

+ Propagations can now generate interpolated trajectories (using a Lagrange interpolation). This follows a multithreaded [Map-Reduce](https://en.wikipedia.org/wiki/MapReduce) pattern so no computational slowdown is noticeable.
+ Event finding has been moved to interpolated trajectories allowing for significantly increased precision. For example, Nyx can now detect an upcoming Eclipse event as soon as the Penumbra reaches 2% of shadowing. It is also possible to search for any orbital event in any celestial frame.
+ Propagation conditional stopping has been moved to the interpolated trajectories allowing for propagation until a specific event in another frame. For example, Nyx can propagate a spacecraft in the EME2000 frame but stop the propagation on the third passage after true anomaly in a Moon J2000 frame is at 35.2 degrees.
+ B-Plane targeting for interplanetary mission design
+ Direct multiple shooting for low-thrust optimization
+ Full refactoring of `Dynamics`, which is how the equations of motions are modeled.
+ Switch to hifitime 2.x. This computes time using fractions allowing for picosecond precision, likely one of the more precise time computation software so far.
+ Import/export trajectories from STK, GMAT, or a custom format.
+ Thorough documentation (this website is new!).