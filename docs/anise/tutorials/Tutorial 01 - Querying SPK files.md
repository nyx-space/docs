# ANISE

ANISE is a modern rewrite of NAIF SPICE, written in Rust and providing interfaces to other languages including Python.

Evidently, this tutorial applies to the Python usage of ANISE.

## Goal
By the end of this tutorial, you should be able to know how to load local files and query the Almanac for the position and velocity of different celestial objects at different times, expressed in different time systems.

Let's start by installing ANISE: `pip install anise`

## Introduction


```python
import anise
```

ANISE allows one to query SPICE files, like those created by JPL, for position and rotation information. A contrario to SPICE, ANISE is fully thread safe. To support this, ANISE has an object called the `Almanac` which stores all of the loaded files, whereas SPICE would have a single thread-unsafe shared context.

Let's import that class.


```python
from anise import Almanac
Almanac?
```


    [0;31mInit signature:[0m [0mAlmanac[0m[0;34m([0m[0mpath[0m[0;34m)[0m[0;34m[0m[0;34m[0m[0m
    [0;31mDocstring:[0m
    An Almanac contains all of the loaded SPICE and ANISE data.

    # Limitations
    The stack space required depends on the maximum number of each type that can be loaded.
    [0;31mFile:[0m           ~/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages/anise/__init__.py
    [0;31mType:[0m           type
    [0;31mSubclasses:[0m


As much as possible, the functions and classes in ANISE are documented. In typical Python, you can do `help(Almanac)` and in Jupyter notebook, you can simply enter the name of what you're seeking help on followed by a question mark, and execute the cell (Ctrl+Enter).

Let's load on the files provided in the ANISE repo. Note that ANISE supports automatically downloading remote files as well, but that is the topic of another tutorial.


```python
almanac = Almanac("../../data/de440s.bsp")
print(almanac)
```

    Almanac: #SPK = 1	#BPC = 0


You may also use the `describe` function to see the details of what is loaded, optionally showing only some of the loaded data.


```python
almanac.describe?
```


    [0;31mSignature:[0m
    [0malmanac[0m[0;34m.[0m[0mdescribe[0m[0;34m([0m[0;34m[0m
    [0;34m[0m    [0mspk[0m[0;34m=[0m[0;32mNone[0m[0;34m,[0m[0;34m[0m
    [0;34m[0m    [0mbpc[0m[0;34m=[0m[0;32mNone[0m[0;34m,[0m[0;34m[0m
    [0;34m[0m    [0mplanetary[0m[0;34m=[0m[0;32mNone[0m[0;34m,[0m[0;34m[0m
    [0;34m[0m    [0mtime_scale[0m[0;34m=[0m[0;32mNone[0m[0;34m,[0m[0;34m[0m
    [0;34m[0m    [0mround_time[0m[0;34m=[0m[0;32mNone[0m[0;34m,[0m[0;34m[0m
    [0;34m[0m[0;34m)[0m[0;34m[0m[0;34m[0m[0m
    [0;31mDocstring:[0m
    Pretty prints the description of this Almanac, showing everything by default. Default time scale is TDB.
    If any parameter is set to true, then nothing other than that will be printed.
    [0;31mType:[0m      builtin_function_or_method



```python
almanac.describe(bpc=True) # This will print nothing because no BPC is loaded
almanac.describe(spk=True)
```

    === SPK #0 ===
    ┌────────────────┬─────────────────────────────┬───────────────────────────────┬───────────────────────────────────┬───────────────────────────────────┬─────────────┬────────────────────┐
    │ Name           │ Target                      │ Center                        │ Start epoch                       │ End epoch                         │ Duration    │ Interpolation kind │
    ├────────────────┼─────────────────────────────┼───────────────────────────────┼───────────────────────────────────┼───────────────────────────────────┼─────────────┼────────────────────┤
    │ DE-0440LE-0440 │ Mercury J2000               │ Solar System Barycenter J2000 │ 1849-12-26T00:00:00.000046818 TDB │ 2150-01-21T23:59:59.999955683 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Venus J2000                 │ Solar System Barycenter J2000 │ 1849-12-26T00:00:00.000046818 TDB │ 2150-01-21T23:59:59.999955683 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Earth-Moon Barycenter J2000 │ Solar System Barycenter J2000 │ 1849-12-26T00:00:00.000046818 TDB │ 2150-01-21T23:59:59.999955683 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Mars Barycenter J2000       │ Solar System Barycenter J2000 │ 1849-12-26T00:00:00.000046818 TDB │ 2150-01-21T23:59:59.999955683 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Jupiter Barycenter J2000    │ Solar System Barycenter J2000 │ 1849-12-26T00:00:00.000046818 TDB │ 2150-01-21T23:59:59.999955683 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Saturn Barycenter J2000     │ Solar System Barycenter J2000 │ 1849-12-26T00:00:00.000046818 TDB │ 2150-01-21T23:59:59.999955683 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Uranus Barycenter J2000     │ Solar System Barycenter J2000 │ 1849-12-26T00:00:00.000046818 TDB │ 2150-01-21T23:59:59.999955683 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Neptune Barycenter J2000    │ Solar System Barycenter J2000 │ 1849-12-26T00:00:00.000046818 TDB │ 2150-01-21T23:59:59.999955683 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Pluto Barycenter J2000      │ Solar System Barycenter J2000 │ 1849-12-26T00:00:00.000046818 TDB │ 2150-01-21T23:59:59.999955683 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Sun J2000                   │ Solar System Barycenter J2000 │ 1849-12-26T00:00:00.000046818 TDB │ 2150-01-21T23:59:59.999955683 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Moon J2000                  │ Earth-Moon Barycenter J2000   │ 1849-12-26T00:00:00.000046818 TDB │ 2150-01-21T23:59:59.999955683 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Earth J2000                 │ Earth-Moon Barycenter J2000   │ 1849-12-26T00:00:00.000046818 TDB │ 2150-01-21T23:59:59.999955683 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ body 199 J2000              │ Mercury J2000                 │ 1849-12-26T00:00:00.000046818 TDB │ 2150-01-21T23:59:59.999955683 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ body 299 J2000              │ Venus J2000                   │ 1849-12-26T00:00:00.000046818 TDB │ 2150-01-21T23:59:59.999955683 TDB │ 109600 days │ Chebyshev Triplet  │
    └────────────────┴─────────────────────────────┴───────────────────────────────┴───────────────────────────────────┴───────────────────────────────────┴─────────────┴────────────────────┘


As of version 0.2.2, in Python, one can only perform transformations, and simple translations, but not extract the rotation information like the DCM (it is only available in Rust for now). What this means in practice is that one can query for the state of the Moon in the Earth body fixed frame (IAU Earth for example), and ANISE will perform all of the required transformations, but you cannot only query for the rotation parameters.

**To query something, we need several pieces of information:**

1. The epoch (or "datetime") at which to compute the state;
2. The frames we want the observer and target to be in;
3. The aberration corrections desired.


## Time management
For time management, ANISE uses [Hifitime](https://nyxspace.com/hifitime/intro/), arguably the most precise time management library in the world. Let's create an epoch by importing the hifitime classes, which are re-exported from ANISE.


```python
from anise.time import Epoch

epoch_utc = Epoch("2010-12-21T03:04:05")
print(epoch_utc)

epoch_tai = Epoch("2010-12-21T03:04:05 TAI")
print(epoch_tai)
print(epoch_tai.timedelta(epoch_utc)) # This will print the number of leap seconds between UTC and TAI.
```

    2010-12-21T03:04:05 UTC
    2010-12-21T03:03:31 UTC
    -34 s


We created an Epoch in the TAI and in the UTC time scales. UTC is a glitchy time scale, which is never used in astrodynamics or astronomy. If the notion of a time scale is new to you, that's fine, just please read the Hifitime link above which explains the concept of time scales and why they are so important.

So if UTC is not used in astrodynamics, what is? Well that would be the GPST time scale for low Earth orbiters and the TDB time scale for most things out of LEO.


```python
epoch = epoch_utc

print(f"{epoch} is {epoch.to_gpst_duration()} after the GPS reference time of {Epoch.init_from_gpst_nanoseconds(0)}")

print(f"{epoch} is {epoch.to_tdb_duration()} after the Dynamical Barycentric Time reference time of {Epoch.init_from_tdb_seconds(0.0)}")
```

    2010-12-21T03:04:05 UTC is 11307 days 3 h 4 min 20 s after the GPS reference time of 1980-01-06T00:00:00 UTC
    2010-12-21T03:04:05 UTC is 4006 days 15 h 5 min 11 s 183 ms 602 μs 262 ns after the Dynamical Barycentric Time reference time of 2000-01-01T11:58:55.816072704 UTC


^^^ That is one of the most useful features of Hifitime: seamless conversion between time scales, all with nanosecond precision, and for ~65,000 centuries around 01 January 1900.

At this point, we've got one epoch. More analysis requires us to check stuff at different times.

To do so, Hifitime provides arithmetics on epochs. Let's try that out.


```python
from anise.time import Duration, Unit

print(epoch + Duration("1.567 days 20 ns"))
print(epoch + Unit.Day*1.567 + Unit.Nanosecond*20)
```

    2010-12-22T16:40:33.800000020 UTC
    2010-12-22T16:40:33.800000020 UTC


Durations can be initialized using either their string representation using standard unit abbreviations.

If we know exactly that we want to sample a certain number of times between two epoch, we can either write a for loop and add a duration, or we can use the `TimeSeries` class of Hifitime.


```python
from anise.time import TimeSeries

start = Epoch("2010-12-21T03:04:05")

for epoch_from_series in TimeSeries(start=start, end=start + Unit.Day*4, step=Unit.Hour*3.7, inclusive=True):
    print(epoch_from_series)
```

    2010-12-21T03:04:05 UTC
    2010-12-21T06:46:05 UTC
    2010-12-21T10:28:05 UTC
    2010-12-21T14:10:05 UTC
    2010-12-21T17:52:05 UTC
    2010-12-21T21:34:05 UTC
    2010-12-22T01:16:05 UTC
    2010-12-22T04:58:05 UTC
    2010-12-22T08:40:05 UTC
    2010-12-22T12:22:05 UTC
    2010-12-22T16:04:05 UTC
    2010-12-22T19:46:05 UTC
    2010-12-22T23:28:05 UTC
    2010-12-23T03:10:05 UTC
    2010-12-23T06:52:05 UTC
    2010-12-23T10:34:05 UTC
    2010-12-23T14:16:05 UTC
    2010-12-23T17:58:05 UTC
    2010-12-23T21:40:05 UTC
    2010-12-24T01:22:05 UTC
    2010-12-24T05:04:05 UTC
    2010-12-24T08:46:05 UTC
    2010-12-24T12:28:05 UTC
    2010-12-24T16:10:05 UTC
    2010-12-24T19:52:05 UTC
    2010-12-24T23:34:05 UTC


Finally, as a last bit of this introduction on time, let's demonstrate how durations can be rounded in hifitime.
Most humans don't usually care about nanosecond precision, so we can round those away.


```python
orig = Duration("13 d 5.6 h 23 ns")
print(orig)

print(orig.round(Unit.Day*1)) # Rounded to the nearest day

print(orig.floor(Unit.Second*1)) # Floored to the nearest second

print(orig.ceil(Unit.Century*0.25)) # Ceiled to the nearest quarter of a century
```

    13 days 5 h 36 min 23 ns
    13 days
    13 days 5 h 36 min
    9131 days 6 h


### Learning exercise

Your exercise is simple: create two dates in different time systems, run a time series over them at your desired time step, and print the difference between the start date and "current" date of the iterator as the printing happens. Don't hesitate to look at the [Python user guide of Hifitime](https://nyxspace.com/hifitime/python/).


## Frame management

Frames are absolutely crucial in astrodynamics. They defined the point of origin and the orientation of that frame for each state.

In terms of orientation, one will typically use the J2000 orientation. This is an inertial frame (well, quasi-inertial) which is tilted by about 23 degrees compared to the Ecliptic frame. The Ecliptic frame can be thought of as the average plane in which all of the planets rotate around the Sun. As such, the J2000 frame can be thought of the frame where the Z axis points _on average_ in the direction of the axis of rotation of the Earth.

If a state is communicated in the "J2000 frame" without any centeral object provided, it's safe to assume that's the "EME2000" frame, which is the Earth Mean Equator J2000 orientation frame.

There are _lots_ of frames, since one can define any frame with any center and any orientation. ANISE tries to help out: you can create a frame simply specifying its central object (as it NAIF ID) and its orientation ID (also matches the NAIF IDs). ANISE also provides constants for most common frames.


```python
from anise.astro.constants import Frames
dir(Frames) # List of built-in frames
```




    ['EARTH_ECLIPJ2000',
     'EARTH_ITRF93',
     'EARTH_J2000',
     'EARTH_MOON_BARYCENTER_J2000',
     'EME2000',
     'IAU_EARTH_FRAME',
     'IAU_JUPITER_FRAME',
     'IAU_MARS_FRAME',
     'IAU_MERCURY_FRAME',
     'IAU_MOON_FRAME',
     'IAU_NEPTUNE_FRAME',
     'IAU_SATURN_FRAME',
     'IAU_URANUS_FRAME',
     'IAU_VENUS_FRAME',
     'JUPITER_BARYCENTER_J2000',
     'MARS_BARYCENTER_J2000',
     'MERCURY_J2000',
     'MOON_J2000',
     'NEPTUNE_BARYCENTER_J2000',
     'PLUTO_BARYCENTER_J2000',
     'SATURN_BARYCENTER_J2000',
     'SSB_J2000',
     'SUN_J2000',
     'URANUS_BARYCENTER_J2000',
     'VENUS_J2000',
     '__class__',
     '__delattr__',
     '__dir__',
     '__doc__',
     '__eq__',
     '__format__',
     '__ge__',
     '__getattribute__',
     '__getstate__',
     '__gt__',
     '__hash__',
     '__init__',
     '__init_subclass__',
     '__le__',
     '__lt__',
     '__module__',
     '__ne__',
     '__new__',
     '__reduce__',
     '__reduce_ex__',
     '__repr__',
     '__setattr__',
     '__sizeof__',
     '__str__',
     '__subclasshook__']




```python
# One can build a frame from its ephemeris and orientation IDs, which are the same as the NAIF codes.
# For example, ephemeris center 3 is the Earth Moon Barycenter, and orientation 1 is J2000
from anise.astro import Frame
custom_frame = Frame(3, 1)
print(custom_frame)
print(custom_frame == Frames.EARTH_MOON_BARYCENTER_J2000)
```

    Earth-Moon Barycenter J2000
    True



```python
eme2k = Frames.EARTH_J2000
dir(eme2k)
```




    ['__class__',
     '__delattr__',
     '__dir__',
     '__doc__',
     '__eq__',
     '__format__',
     '__ge__',
     '__getattribute__',
     '__getnewargs__',
     '__getstate__',
     '__gt__',
     '__hash__',
     '__init__',
     '__init_subclass__',
     '__le__',
     '__lt__',
     '__module__',
     '__ne__',
     '__new__',
     '__reduce__',
     '__reduce_ex__',
     '__repr__',
     '__setattr__',
     '__sizeof__',
     '__str__',
     '__subclasshook__',
     'ephem_origin_id_match',
     'ephem_origin_match',
     'ephemeris_id',
     'flattening',
     'is_celestial',
     'is_geodetic',
     'mean_equatorial_radius_km',
     'mu_km3_s2',
     'orient_origin_id_match',
     'orient_origin_match',
     'orientation_id',
     'polar_radius_km',
     'semi_major_radius_km',
     'shape',
     'with_ephem',
     'with_orient']



Frames include _potentially_ a lot of information. This is because the frame data is used to compute orbital elements, which we'll cover later on.

However, ANISE does not provide any defaults for this data. You must load a Planetary Constants ANISE ("PCA") file for ANISE to know that these exist. Otherwise, you'll get an exception:


```python
eme2k.mu_km3_s2()
```


    ---------------------------------------------------------------------------

    Exception                                 Traceback (most recent call last)

    Cell In[14], line 1
    ----> 1 eme2k.mu_km3_s2()


    Exception: retrieving gravitational parameter requires the frame Earth J2000 to have mu_km3_s2 defined



```python
# Let's load the PCA
almanac = almanac.load("../../data/pck08.pca")
```

**VERY IMPORTANT:** Note how we've _reassigned_ the `almanac` variable in the `load` call. This is _also_ part of the thread safety: the almanac structure is _read only_ and the reassignment is what allows us to grab a reference to the almanac that has the newly loaded file.

(Note that this also means you can have _multiple_ Almanac objects and compare the data loaded into them, similar to a "BOA" for those familiar with JPL MONTE.)


```python
print(eme2k.mu_km3_s2())
```


    ---------------------------------------------------------------------------

    Exception                                 Traceback (most recent call last)

    Cell In[16], line 1
    ----> 1 print(eme2k.mu_km3_s2())


    Exception: retrieving gravitational parameter requires the frame Earth J2000 to have mu_km3_s2 defined


Uh! One way for ANISE to be thread safe without mutexes is for the data to be stored solely in the almanac structure. So loading the data in the almanac is not sufficient: we need to retrieve it.



```python
loaded_eme2k = almanac.frame_info(eme2k)
print(loaded_eme2k)
```

    Earth J2000 (μ = 398600.435436096 km^3/s^2, eq. radius = 6378.14 km, polar radius = 6356.75 km, f = 0.0033536422844278)


All of this data was created from the KPL/TPC files that NAIF provides. Another tutorial will guide you through modifying these.

### Exercise #1

1. Investigate what are some of the available fields in this loaded EME2000 frame.
2. Load the Venus J2000 frame and repeat point 1.

## Querying the almanac

So we've already seen how to build an epoch, and how to find a frame. Let's now quickly look into aberration corrections. The best explanation you'll find is that from NAIF itself: <https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/abcorr.html>.


```python
from anise import Aberration
Aberration?
```


    [0;31mInit signature:[0m [0mAberration[0m[0;34m([0m[0mname[0m[0;34m)[0m[0;34m[0m[0;34m[0m[0m
    [0;31mDocstring:[0m
    Represents the aberration correction options in ANISE.

    In space science and engineering, accurately pointing instruments (like optical cameras or radio antennas) at a target is crucial. This task is complicated by the finite speed of light, necessitating corrections for the apparent position of the target.

    This structure holds parameters for aberration corrections applied to a target's position or state vector. These corrections account for the difference between the target's geometric (true) position and its apparent position as observed.

    # Rule of tumb
    In most Earth orbits, one does _not_ need to provide any aberration corrections. Light time to the target is less than one second (the Moon is about one second away).
    In near Earth orbits, e.g. inner solar system, preliminary analysis can benefit from enabling unconverged light time correction. Stellar aberration is probably not required.
    For deep space missions, preliminary analysis would likely require both light time correction and stellar aberration. Mission planning and operations will definitely need converged light-time calculations.

    For more details, <https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/abcorr.html>.

    # SPICE Validation

    The validation test `validate_jplde_de440s_aberration_lt` checks 101,000 pairs of ephemeris computations and shows that the unconverged Light Time computation matches the SPICE computations almost all the time.
    More specifically, the 99th percentile of error is less than 5 meters, the 75th percentile is less than one meter, and the median error is less than 2 millimeters.
    [0;31mFile:[0m           ~/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages/anise/__init__.py
    [0;31mType:[0m           type
    [0;31mSubclasses:[0m



```python
lt_aber = Aberration("LT") # This is the same as the LT enum in SPICE.
lt_aber
```




    LT (@0x7fd4c0478ee0)




```python
# If you want the details of what will be computed, using the string representation instead of the `__repr__`:
print(lt_aber)
```

    unconverged light-time aberration



```python
# Looking at the documentation here can be quite useful
almanac.translate?
```


    [0;31mSignature:[0m [0malmanac[0m[0;34m.[0m[0mtranslate[0m[0;34m([0m[0mtarget_frame[0m[0;34m,[0m [0mobserver_frame[0m[0;34m,[0m [0mepoch[0m[0;34m,[0m [0mab_corr[0m[0;34m=[0m[0;32mNone[0m[0;34m)[0m[0;34m[0m[0;34m[0m[0m
    [0;31mDocstring:[0m
    Returns the Cartesian state of the target frame as seen from the observer frame at the provided epoch, and optionally given the aberration correction.

    # SPICE Compatibility
    This function is the SPICE equivalent of spkezr: `spkezr(TARGET_ID, EPOCH_TDB_S, ORIENTATION_ID, ABERRATION, OBSERVER_ID)`
    In ANISE, the TARGET_ID and ORIENTATION are provided in the first argument (TARGET_FRAME), as that frame includes BOTH
    the target ID and the orientation of that target. The EPOCH_TDB_S is the epoch in the TDB time system, which is computed
    in ANISE using Hifitime. THe ABERRATION is computed by providing the optional Aberration flag. Finally, the OBSERVER
    argument is replaced by OBSERVER_FRAME: if the OBSERVER_FRAME argument has the same orientation as the TARGET_FRAME, then this call
    will return exactly the same data as the spkerz SPICE call.

    # Warning
    This function only performs the translation and no rotation whatsoever. Use the `transform` function instead to include rotations.

    # Note
    This function performs a recursion of no more than twice the [MAX_TREE_DEPTH].
    [0;31mType:[0m      builtin_function_or_method



```python
# The transform function will also compute the rotations where needed.
almanac.transform?
```


    [0;31mSignature:[0m [0malmanac[0m[0;34m.[0m[0mtransform[0m[0;34m([0m[0mtarget_frame[0m[0;34m,[0m [0mobserver_frame[0m[0;34m,[0m [0mepoch[0m[0;34m,[0m [0mab_corr[0m[0;34m=[0m[0;32mNone[0m[0;34m)[0m[0;34m[0m[0;34m[0m[0m
    [0;31mDocstring:[0m
    Returns the Cartesian state needed to transform the `from_frame` to the `to_frame`.

    # SPICE Compatibility
    This function is the SPICE equivalent of spkezr: `spkezr(TARGET_ID, EPOCH_TDB_S, ORIENTATION_ID, ABERRATION, OBSERVER_ID)`
    In ANISE, the TARGET_ID and ORIENTATION are provided in the first argument (TARGET_FRAME), as that frame includes BOTH
    the target ID and the orientation of that target. The EPOCH_TDB_S is the epoch in the TDB time system, which is computed
    in ANISE using Hifitime. THe ABERRATION is computed by providing the optional Aberration flag. Finally, the OBSERVER
    argument is replaced by OBSERVER_FRAME: if the OBSERVER_FRAME argument has the same orientation as the TARGET_FRAME, then this call
    will return exactly the same data as the spkerz SPICE call.

    # Note
    The units will be those of the underlying ephemeris data (typically km and km/s)
    [0;31mType:[0m      builtin_function_or_method



```python
state = almanac.translate(Frames.EARTH_J2000, Frames.SSB_J2000, epoch, None)
print(state)
```

    [Solar System Barycenter J2000] 2010-12-21T03:04:05 UTC	position = [2006351.284308, 135110969.586735, 58576035.963861] km	velocity = [-30.254436, 0.375013, 0.163924] km/s


**TA DA!** We've just queried the almanac (i.e. the DE440s.bsp file) to get the position of the Earth in the J2000 frame as seen from the solar system barycenter ("SSB") in the J2000 frame, at the epoch we defined earlier, and when no aberration correction is performed.


```python
state = almanac.translate(Frames.EARTH_J2000, Frames.SSB_J2000, epoch, Aberration("LT"))
print(state.light_time())
```

    8 min 11 s 259 ms 84 μs 389 ns


Calling "light_time" will return a Hifitime duration instance. You can grab the exact seconds by converting that high precision duration into the unit of your choice:


```python
print(state.light_time().to_unit(Unit.Day))
print(state.light_time().to_unit(Unit.Second))
print(state.light_time().to_seconds())
```

    0.005685869032280092
    491.259084389
    491.259084389


## Exercises

1. Query the position of the Earth at different times using a time series. Note that the DE440s file is only valid for 200 years centered on 1950.
2. Query the position of Venus as seen from the Earth, both in the J2000 frame, and make a plot of the light time between these two planets throughout a given year.


```python

```
