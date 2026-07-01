# ANISE

ANISE is a modern rewrite of NAIF SPICE, written in Rust and providing interfaces to other languages including Python.

## Goal

By the end of this tutorial, you will know how to use your custom frame kernels (FK) and text planetary constant kernels (TPC) in ANISE.

Let's start by installing ANISE: `pip install anise`

## Data structure

SPICE supports text-based kernels. These allow for easy modification and inclusion of documentation directly in the text file. The way SPICE handles these is by keeping a file handler open on the file while it's loaded. This causes a number of issues, such as potential file locking problems, increased risk of data corruption in cases of unexpected software termination, and increased difficulty in managing concurrent access, especially pertinent in the context of onboard flight software. To prevent these issues, ANISE maintains a pointer to the data contained in these files in memory (via a memory mapping or a heap allocation). Moreover, ANISE ensures that the data it uses allows for immediate random access, which is a method of accessing data at any point in memory with equal speed, independent of its location, thereby speeding up searches within the kernel data. To facilitate this, the data is stored in a platform-independent binary structure using the ASN.1 DER specification (the telecommunications industry standard for 20+ years). ASN.1 offers advantages like well-defined data structures, robust encoding schemes, and ease of interoperability across different platforms, making it a reliable choice for storing kernel data.

This approach allows ANISE to parse through the FK and TPC equivalents significantly faster than SPICE, while storing the same information.

However, this also means that ANISE cannot load the text files directly. Instead, these must be converted into the ANISE format, respectively PCA and EPA for "Planetary Constants ANISE" kernel and "Euler Parameter ANISE" kernel. Euler parameters (also known as quaternion parameters) offer a compact and non-redundant representation of orientations in three dimensions. They differ from quaternions in their normalization constraint and are slightly more robust to numerical errors in some computational scenarios.

For details about the data set structure, refer to the API documentation: [`DataSet`](https://docs.rs/anise/latest/anise/structure/dataset/struct.DataSet.html). The `EulerParameterDataSet` and the `PlanetaryDataSet` are concrete implementations of this `DataSet` structure.

### Version compatibility

ANISE guarantees not to change the structure of these kernels between patch versions (e.g., version `0.3.0` and version `0.3.99` are guaranteed to have compatible kernels). However, until version `1.0.0`, the structure _may_ change and if so, the updated version of the default PCA and EPA files will be added to the Nyx Space cloud.

Since version `0.1.0`, the structure of the kernels has _not_ changed. However, the ANISE version is encoded at the start of each kernel. This is only used if the data set cannot be properly decoded to inform the user of the expected ANISE version and the one that they're trying to load. In other words, although there is a version `0.3` of the PCK08 and PCK11 kernels, the files used in version `0.1.0` are still compatible.

## Planetary Constant ANISE kernels

Planetary Constant ANISE (PCA) kernels (or a "data set") include a lookup table for random access via a name or an ID, metadata, and, more importantly, the actual planetary data itself. This data includes gravitational parameters, the shape of the triaxial ellipsoid, phase angle polynomials for the prime meridian, pole right ascension and declination, and more. You'll find all of the specifications in the API documentation: [`PlanetaryData`](https://docs.rs/anise/latest/anise/structure/planetocentric/struct.PlanetaryData.html).

In the previous tutorials, we focused on fetching the frame information from the Almanac. This operation reads the PCA to return a copy of this information. This is why a PCA is provided in the `latest.dhall` configuration file for an Almanac.

The Planetary Data structure includes the gravitational data. _However_, the SPICE TPC files contain _either_ ellipsoid definition information _or_ gravitational data. Therefore, to build a PCA, ANISE requires _both_ versions of the TPCs.

Let's go ahead and build a PCA file from the NAIF `pck0008.tpc` and the `gm_de431.tpc` files.


```python
from anise.utils import convert_tpc
convert_tpc?
```


    [0;31mSignature:[0m [0mconvert_tpc[0m[0;34m([0m[0mpck_file_path[0m[0;34m,[0m [0mgm_file_path[0m[0;34m,[0m [0manise_output_path[0m[0;34m,[0m [0moverwrite[0m[0;34m=[0m[0;32mNone[0m[0;34m)[0m[0;34m[0m[0;34m[0m[0m
    [0;31mDocstring:[0m
    Converts two KPL/TPC files, one defining the planetary constants as text, and the other defining the gravity parameters, into the PlanetaryDataSet equivalent ANISE file.
    KPL/TPC files must be converted into "PCA" (Planetary Constant ANISE) files before being loaded into ANISE.
    [0;31mType:[0m      builtin_function_or_method



```python
convert_tpc("../../data/pck00008.tpc", "../../data/gm_de431.tpc", "demo08.pca", True)
```

    Skipping 802: no gravity data
    Skipping 806: no gravity data
    Skipping 9511010: no gravity data
    Skipping 514: no gravity data
    Skipping 714: no gravity data
    Skipping 509: no gravity data
    Skipping 707: no gravity data
    Skipping 711: no gravity data
    Skipping 804: no gravity data
    Skipping 2431010: no gravity data
    Skipping 506: no gravity data
    Skipping 710: no gravity data
    Skipping 712: no gravity data
    Skipping 612: no gravity data
    Skipping 618: no gravity data
    Skipping 713: no gravity data
    Skipping 803: no gravity data
    Skipping 508: no gravity data
    Skipping 515: no gravity data
    Skipping 715: no gravity data
    Skipping 511: no gravity data
    Skipping 706: no gravity data
    Skipping 516: no gravity data
    Skipping 507: no gravity data
    Skipping 614: no gravity data
    Skipping 808: no gravity data
    Skipping 805: no gravity data
    Skipping 807: no gravity data
    Skipping 513: no gravity data
    Skipping 2000216: no gravity data
    Skipping 613: no gravity data
    Skipping 708: no gravity data
    Skipping 512: no gravity data
    Skipping 709: no gravity data
    Skipping 510: no gravity data


    Added 49 items


We now have a PCA called `demo08.pca` which includes 49 entries. This file is compatible with _any_ machine you run ANISE on, little or big endian (which is _not_ the case of the DAF/BSP or DAF/BPC files).

Let's load this file in an Almanac.


```python
from anise import Almanac
almanac = Almanac("demo08.pca")
almanac
```




    Almanac: #SPK = 0	#BPC = 0	PlanetaryData with 49 ID mappings and 0 name mappings (@0x559b4af30800)



Since we don't have anything loaded other than these planetary constants, we can't do a whole lot, but we can query the Almanac for the shape and gravitational data by using `frame_info`.


```python
from anise.astro.constants import Frames
iau_jupiter_frame = almanac.frame_info(Frames.IAU_JUPITER_FRAME)
iau_jupiter_frame
```




    body 599 IAU_JUPITER (μ = 126686534.9218008 km^3/s^2, eq. radius = 71492 km, polar radius = 66854 km, f = 0.0648743915403122) (@0x7fe814070310)




```python
iau_jupiter_frame.mu_km3_s2()
```




    126686534.9218008



### Exercise: Modifying the gravitational parameter of the Earth frame

+ Make a copy of the `gm_de431.tpc` file and remove everything but the Earth GM.
+ Set the Earth GM to the one used by GMAT: `398600.4415` km^3/s^2
+ Make a copy of the `pck00008.tpc` file, removing everything except Earth related data.
+ Build a new PCA file using these two new files
+ Load a default Almanac and an empty Almanac where you'll load these two files into, along with the `DE440s.bsp` file.
+ Query the Cartesian state of the Earth at any time of your choosing from both of these Almanac. The state should be the same, since it'll be from the DE440s.bsp.
+ Observe how the frame graviational parameter information of both will differ.
+ Finally, using the `at_epoch` function on both of these state, perform a two-body propagation for both and notice how the graviational parameter affects the result.

## Euler Parameter ANISE kernel

Euler parameters are a normalized quaternion. In fact, in the ANISE code in Rust, `EulerParameter` is an alias for `Quaternion`. Euler parameters are useful for defining fixed rotations, e.g. the rotation from the Moon Principal Axes frame to the Moon Mean Earth frame.

Euler Parameter ANISE kernels (EPA) can be used to store these fixed rotations between frames, and reference them either by their ID or by their name. **They are the equivalent of SPICE's `FK` text files.**

Until [#175](https://github.com/nyx-space/anise/issues/175), rotation data is _not_ exposed to Python.

### How to build EPA files

However, it's possible to convert an FK file into the EPA file using the following function.


```python
from anise.utils import convert_fk
convert_fk?
```


    [0;31mSignature:[0m
    [0mconvert_fk[0m[0;34m([0m[0;34m[0m
    [0;34m[0m    [0mfk_file_path[0m[0;34m,[0m[0;34m[0m
    [0;34m[0m    [0manise_output_path[0m[0;34m,[0m[0;34m[0m
    [0;34m[0m    [0mshow_comments[0m[0;34m=[0m[0;32mNone[0m[0;34m,[0m[0;34m[0m
    [0;34m[0m    [0moverwrite[0m[0;34m=[0m[0;32mNone[0m[0;34m,[0m[0;34m[0m
    [0;34m[0m[0;34m)[0m[0;34m[0m[0;34m[0m[0m
    [0;31mDocstring:[0m
    Converts a KPL/FK file, that defines frame constants like fixed rotations, and frame name to ID mappings into the EulerParameterDataSet equivalent ANISE file.
    KPL/FK files must be converted into "PCA" (Planetary Constant ANISE) files before being loaded into ANISE.
    [0;31mType:[0m      builtin_function_or_method


On the Nyx Space Cloud, you'll find the `moon.fk` file, which includes the mapping between the Moon PA and Moon ME frame. The latest Almanac also includes the high precision Moon ME frame. Hence, with default data, you can rotate an object from any frame into the high precision Moon ME frame.

## Exercise

Using tutorial 04, compute the azimuth, elevation, and range of the [Shackleton](https://en.wikipedia.org/wiki/Shackleton_(crater)) crater on the Moon to the city of Paris, France.

Here are the general steps:

1. Load the latest Almanac, and check (by printing it) that it includes both EPA and PCA data. Else, load the `moon_fk.epa` file from the Nyx Space Cloud using a `MetaFile` with the URL <http://public-data.nyxspace.com/anise/v0.4/moon_fk.epa>.
2. Define a time series over a year with a granularity of 12 hours. This crater is on the South Pole of the Moon, and its visibility is often below the horizon of an object as far north as Paris.
3. For each epoch, define Paris as an `Orbit` instance from its longitude and latitude (recall that the constants include the mean Earth angular rotation rate), in the IAU_EARTH frame. Also, build the crater in the IAU_MOON frame.
4. Finally, call the `AER` function of the Almanac with each epoch to compute the AER data. Plot it!


```python

```
