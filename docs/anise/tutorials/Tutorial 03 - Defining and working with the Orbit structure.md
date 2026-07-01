# ANISE

ANISE is a modern rewrite of NAIF SPICE, written in Rust and providing interfaces to other languages including Python.

Evidently, this tutorial applies to the Python usage of ANISE.

## Goal
By the end of this tutorial, you should know how to initialize an `Orbit` structure, how to retrieve any of the available orbital elements, and compute the future state of that orbit in the future assuming two body propagation (i.e. _no perturbation of any kind_).

For comprehensive and high-fidelity astrodynamics, orbit estimation, and other spaceflight dynamics functionalities essential in real-world missions, consider using [Nyx](https://github.com/nyx-space/nyx/). Nyx has been the choice for several cislunar missions and lunar landers, and, like ANISE, is also open-source and free to use.

Let's start by installing ANISE: `pip install anise`

## Load the latest Almanac

As seen the tutorial #2, we'll just download the latest data using the MetaAlmanac.


```python
from anise import MetaAlmanac

almanac = MetaAlmanac("../../data/latest.dhall").process()

almanac
```




    Almanac: #SPK = 1	#BPC = 2	PlanetaryData with 49 ID mappings and 0 name mappings (@0x5587ec685530)



## Orbit structure

The `Orbit` structure is an alias for `CartesianState`, which is only available under that name in Rust. In fact, `Orbit` will _always_ store the information in its Cartesian form because it's a non-singular representation of an orbit, regardless of whether it's elliptical, hyperbolic, equatorial and circular, etc.

An orbit is defined by its position, velocity, an epoch, and a frame.

As we saw in tutorial #1, we can import the frames as they're defined with their ephemeris and orientation IDs. However, recall that ANISE does not provide _any_ default values for the gravitational parameter or shape of the geoid in these frames and they need to be loaded from the Almanac.

Let's grab the frame information from the almanac.


```python
from anise.astro.constants import Frames
eme2k = almanac.frame_info(Frames.EME2000)
print(Frames.EME2000)
# Only the loaded frame has the gravitational parameter and shape information
print(eme2k)
```

    Earth J2000
    Earth J2000 (μ = 398600.435436096 km^3/s^2, eq. radius = 6378.14 km, polar radius = 6356.75 km, f = 0.0033536422844278)


Orbits can be initialized in several ways. The simplest is to initialize it from its cartesian data, provided in kilometers and kilometers per second.


```python
from anise.astro import Orbit
Orbit?
```


    [0;31mInit signature:[0m [0mOrbit[0m[0;34m([0m[0mx_km[0m[0;34m,[0m [0my_km[0m[0;34m,[0m [0mz_km[0m[0;34m,[0m [0mvx_km_s[0m[0;34m,[0m [0mvy_km_s[0m[0;34m,[0m [0mvz_km_s[0m[0;34m,[0m [0mepoch[0m[0;34m,[0m [0mframe[0m[0;34m)[0m[0;34m[0m[0;34m[0m[0m
    [0;31mDocstring:[0m
    Defines a Cartesian state in a given frame at a given epoch in a given time scale. Radius data is expressed in kilometers. Velocity data is expressed in kilometers per second.
    Regardless of the constructor used, this struct stores all the state information in Cartesian coordinates as these are always non singular.

    Unless noted otherwise, algorithms are from GMAT 2016a [StateConversionUtil.cpp](https://github.com/ChristopherRabotin/GMAT/blob/37201a6290e7f7b941bc98ee973a527a5857104b/src/base/util/StateConversionUtil.cpp).
    [0;31mType:[0m           type
    [0;31mSubclasses:[0m



```python
from anise.time import Epoch

epoch = Epoch("2010-12-21 02:03:04 TDB") # Let's create an epoch in the TDB time system

# And initialize the orbit from an arbitrary position and velocity.

from_cartesian = Orbit.from_cartesian(
            5_946.673548288958,
            1_656.154606023661,
            2_259.012129598249,
            -3.098683050943824,
            4.579534132135011,
            6.246541551539432,
            epoch,
            eme2k
        )
print(from_cartesian)
```

    [Earth J2000] 2010-12-21T02:01:57.816398952 UTC	position = [5946.673548, 1656.154606, 2259.012130] km	velocity = [-3.098683, 4.579534, 6.246542] km/s


Oftentimes, we know the scientific mission of a spacecraft, so we initialize it from its Keplerian parameters and not its Cartesian state.

All of the orbit initializers start with `from_...`, making it easy to spot if you have an autocompletion enabled (you should!).


```python
Orbit.from_keplerian?
```


    [0;31mSignature:[0m [0mOrbit[0m[0;34m.[0m[0mfrom_keplerian[0m[0;34m([0m[0msma[0m[0;34m,[0m [0mecc[0m[0;34m,[0m [0minc[0m[0;34m,[0m [0mraan[0m[0;34m,[0m [0maop[0m[0;34m,[0m [0mta[0m[0;34m,[0m [0mepoch[0m[0;34m,[0m [0mframe[0m[0;34m)[0m[0;34m[0m[0;34m[0m[0m
    [0;31mDocstring:[0m
    Creates a new Orbit around the provided Celestial or Geoid frame from the Keplerian orbital elements.

    **Units:** km, none, degrees, degrees, degrees, degrees

    NOTE: The state is defined in Cartesian coordinates as they are non-singular. This causes rounding
    errors when creating a state from its Keplerian orbital elements (cf. the state tests).
    One should expect these errors to be on the order of 1e-12.
    [0;31mType:[0m      builtin_function_or_method



```python
from_keplerian = Orbit.from_keplerian(
    7_712.186_117_895_041,
    0.158_999_999_999_999_95,
    53.75369,
    1.998_632_864_211_17e-5,
    359.787_880_000_004,
    25.434_003_407_751_188,
    epoch,
    eme2k
)
print(from_keplerian)
```

    [Earth J2000] 2010-12-21T02:01:57.816398952 UTC	position = [5946.673549, 1656.154605, 2259.012130] km	velocity = [-3.098683, 4.579534, 6.246542] km/s


### Exercise #1

We won't go through all of the initializers, so use your autocompletion to try the following ones out:

+ `from_keplerian_mean_anomaly`
+ `from_keplerian_apsis_radii`
+ `from_keplerian_altitude`
+ `from_latlongalt`

**Objective:** Create and initialize an Orbit structure with given orbital elements.

**Tasks:**
 1. Input specific orbital elements to define an orbit, including hyperbolic orbits (eccentricity greater than 1)
 2. Display the initialized orbit’s parameters and notice how initializing from the Keplerian parameters won't return _exactly_ the same Keplerian data, as it's converted back and forth from its Keplerian representation to its Cartesian representation.

**Learning Goal:** Understand how to define an orbit in ANISE and interpret its parameters.

## Fields of the orbit class

The orbit class provides direct access to a large range of orbital parameters, including the semi major axis, the true longitude, the orbital period, and so on. All of these accessors include the parameter along with the unit in which it is returned. Let's look at a few more common ones.


```python
from_cartesian.sma_altitude_km(), from_cartesian.aol_deg(), from_cartesian.energy_km2_s2(), from_cartesian.periapsis_altitude_km()
```




    (1334.0462758738768,
     25.221883407752955,
     -25.842246360350657,
     107.80853340089652)




```python
# The orbital period (and the light time) is returned as a Hifitime Duration, enabling trivial computations
from anise.time import Unit

print(from_keplerian.period())
print(from_keplerian.period().round(Unit.Second*1))
print(from_keplerian.period().to_seconds())

print(from_keplerian.light_time())
```

    1 h 52 min 20 s 269 ms 114 μs 912 ns
    1 h 52 min 20 s
    6740.269114912
    21 ms 926 μs 330 ns


**Importantly**, all of the orbital parameter computations require the frame data to be initialized, otherwise an exception will be raised specifying what data was not available. In almost all cases, this happens because you use the constant frame definition without fetching the frame information from the Almanac, or your Almanac does not include any planetary constants.

The Orbit structure supports the equality operation, and it'll check that the epoch, frame, and Cartesian state match to within the centimeter level in position and centimeter per second level in velocity.

If that precision is different than the one you wish, you can use the `eq_within` function providing a tolerance in kilometers and kilometers per second.


```python
from_keplerian == from_cartesian
```




    True




```python
from_keplerian.eq_within?
```


    [0;31mSignature:[0m [0mfrom_keplerian[0m[0;34m.[0m[0meq_within[0m[0;34m([0m[0mother[0m[0;34m,[0m [0mradial_tol_km[0m[0;34m,[0m [0mvelocity_tol_km_s[0m[0;34m)[0m[0;34m[0m[0;34m[0m[0m
    [0;31mDocstring:[0m Returns whether this orbit and another are equal within the specified radial and velocity absolute tolerances
    [0;31mType:[0m      builtin_function_or_method


### Exercise #2

**Objective:** Convert between different sets of orbital elements.

**Tasks:**
 1. Using the `add_...` methods (e.g. `add_sma`), see how the Cartesian elements change (accessible as getters like `x_km`).
 2. Analyze how changes in one element affect others.

**Learning Goal:** Gain proficiency in working with various orbital element formats.

## Two body propagation

### Important disclaimer

Two body propagation is a _tool_ and should not be mistaken for a complete representation of real-world scenarios. In actual mission design, the exclusive use of two-body propagation is _physically incorrect and the wrong approach_. This is because a spacecraft or celestial body is invariably influenced by a multitude of factors. These include gravitational forces from other celestial bodies, as well as subtler forces like solar radiation pressure, atmospheric drag, and gravity fields (as, e.g., spherical harmonic modeling), which account for the uneven distribution of a celestial object's mass. **ANISE will only ever support two-body propagation. For high-fidelity astrodynamics, including orbit estimation, the recommended resource is Nyx. Nyx has been integral to several high-profile lunar missions, offering the necessary models for accurate space mission analysis, planning, and operations.**

### Usage

Using the two body propagator in ANISE is super straight-forward: simply call `at_epoch` on an `Orbit` instance. This uses the current mean anomaly of this instance to compute its future mean anomaly using only the time difference between the current epoch and the future epoch.

Of course, this converts from the internal Cartesian representation to its Keplerian representation, and back again, so some level of error in the Keplerian orbital elements will be seen, but it should be minimal.


```python
current_sma_km = from_keplerian.sma_km()
current_true_anomaly_deg = from_keplerian.ta_deg()
current_mean_anomaly_deg = from_keplerian.ma_deg()
future_state = from_keplerian.at_epoch(from_keplerian.epoch + Unit.Day*1.7565)
# Let's see how much these two Keplerian orbital elements have changed
future_sma_km = future_state.sma_km()
future_true_anomaly_deg = future_state.ta_deg()
future_mean_anomaly_deg = future_state.ma_deg()
```


```python
print(f"Error in SMA:\t{abs(current_sma_km - future_sma_km)} km")
print(f"Propagated true anomaly:\t{abs(current_true_anomaly_deg - future_true_anomaly_deg)} deg")
print(f"Propagated mean anomaly:\t{abs(current_mean_anomaly_deg - future_mean_anomaly_deg)} deg")
```

    Error in SMA:	9.094947017729282e-13 km
    Propagated true anomaly:	172.3281610410407 deg
    Propagated mean anomaly:	185.63718609798167 deg


### Exercise #3

All Almanac translation/transform queries return an instance of `Orbit`, populated with the relevant frame information from the Almanac, so gaining familiarity with this structure is important.

**Objective:** Simulate the orbit of a body over time using two-body propagation.

**Tasks:**
 1. Fetch the state of a celestial object, like the Moon, at the epoch of your choice.
 2. Use the Orbit instance's `at_epoch` to propagate the position of that object forward in time, assuming it was subjected only to two body dynamics.
 3. Fetch the state of that same object from the Almanac at that other time, and look at the difference in Cartesian state and orbital elements.

**Learning Goal:** Understand the basics of orbital propagation and its limitations.


```python

```
