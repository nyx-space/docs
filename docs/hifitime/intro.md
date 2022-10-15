
Hifitime is a time management library available in Rust and Python designed for scientific use or in programs that require high accuracy in time computations. It provides several main constructs:

+ `Duration`: a positive or negative duration with nanosecond precision
+ `Epoch`: a datetime with the time scale used to initialize it [^1]
+ `TimeScale`: an enum storing the different time scales (or "time systems") supported by hifitime
+ `TimeSeries`: an iterable structure that yields epochs at a fixed interval between a starting and ending datetime

This library guarantees exactly one nanosecond of precision in all epochs and duration computations for 65,536 years, centered on 01-JAN-1900 TAI. Refer to the [design](/hifitime/design/) for details.

In addition to extensive unit and integration testing, hifitime is formally verified for operations on epochs and durations using the [`Kani`](https://model-checking.github.io/kani/) model checking.

## Time scales

Time scales (or "time systems" in the ESA lingo) are best explained by IAU SOFA:

!!! quote
    Calculations in any scientific discipline may involve precise time, but what sets astronomy apart is the number and variety of time scales that have to be used.

    There are several reasons for this: astronomers must continue to deal with the very phenomena that lie behind obsolete time scales, in particular the rotation of the Earth and the motions of the planets; as new time scales have been introduced, continuity with the past has been preserved, leaving in the various astronomical time scales a fossil record of former offsets and rates; and in astronomical applications the physical context of the “clock” matters, whether it is on Earth, moving or stationary, or on a spacecraft.
    
    -- "SOFA Time Scales and Calendar Tools", Document version 1.61, section 3.1

Hifitime supports the following time scales:

+ Temps Atomique International (TAI)
+ Universal Coordinated Time (UTC)
+ Terrestrial Time (TT)
+ Ephemeris Time (ET) without the small perturbations as per NASA/NAIF SPICE leap seconds kernel
+ Dynamic Barycentric Time (TDB), a higher fidelity ephemeris time
+ Global Positioning System (GPS), and UNIX

## Comparison with SPICE

1. Hifitime and SPICE perform the same computation for Ephemeris Time, i.e. the error between hifitime and SPICE in Ephemeris Time is constrained only by the precision of the SPICE representation.
1. SPICE stores epochs in a single double-precision value (64-bit floats). This leads to considerable loss in precision when initializing epochs that are far from the 01 JAN 2000 ET.
1. SPICE only supports the Ephemeris Time and UTC time scales, whereas hifitime also supports several other commonly used scales.
1. Hifitime can also trivially be used in embedded systems, even for UTC conversions, without the need of an external file. SPICE requires parsing of the text file of leap seconds (e.g. `naif00012.tls`) prior to converting to/from a UTC datetime.
1. Hifitime supports initializing and formatting epochs in RFC3339 and ISO8601 formats, in addition to the NAIF formats starting with `MJD`, `SEC`, or `JD`.
1. SPICE incorrectly assumes that the difference between TAI and UTC is _nine_ seconds prior to the first leap second of 1972. Hifitime uses the SOFA leap seconds when requested.
1. SPICE uses an approximation of ET instead of TDB which does not include the small perturbations.
1. Hifitime stores its base epoch in TAI whereas NAIF uses an approximation of ET.

!!! quote
    Leap seconds pose tricky problems for software writers, and consequently there are concerns that these events put safety-critical systems at risk. The correct solution is for designers to base such systems on TAI or some other glitch-free time scale, not UTC, but this option is often overlooked until it is too late.
    
    -- "SOFA Time Scales and Calendar Tools", Document version 1.61, section 3.5.1

## Comparison with SOFA

1. SOFA stores datetimes as a tuple of two double-precision floats (on 64-bits each). Instead, hifitime stores datetimes as a duration since J1900 TAI, and a duration is stored as a tuple of a signed 16-bit integer and an unsigned 64-bit integer.
1. SOFA supports the TCB and TCG time scales, which hifitime does not support.
1. SOFA supports the unpredictable `UT1` time scale, which hifitime does not support.

## Figures

The following figures show the deviation of different time with respect to TAI scales from 01 January 1970 until 01 January 2023.

--8<-- "includes/time-scale-deviation.html"

--8<-- "includes/time-scale-deviation-no-utc.html"

--8<-- "includes/time-scale-deviation-tdb-et.html"

[^1]: Note that hifitime does not support date-agnostic epochs or time-agnostic epochs, only a combination of both.

--8<-- "includes/Abbreviations.md"