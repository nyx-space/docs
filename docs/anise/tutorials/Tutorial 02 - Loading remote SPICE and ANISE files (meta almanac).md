# ANISE

ANISE is a modern rewrite of NAIF SPICE, written in Rust and providing interfaces to other languages include Python.

Evidently, this tutorial applies to the Python usage of ANISE.

## Goal
By the end of this tutorial, you should be able to know how to load local and remotes files using the `MetaAlmanac` structure, and know how to save and reload that meta configuration.

Let's start by installing ANISE: `pip install anise`

## Introduction

SPICE files, such as development ephemerides, are often substantial in size. Typically, they are stored on shared resources, with links circulated among teams who require access. This process can be cumbersome for end-users, who must ensure they are using the correct file and that it loads properly, irrespective of the script’s execution path.

The `MetaAlmanac` addresses this challenge by facilitating the initialization of an Almanac using both local and remote files. Remote files are automatically downloaded to the user's application data cache folder (`AppData` on Windows, `~/.local/share/cache` on Linux). For these files, the MetaAlmanac verifies the integrity of any local copy by comparing its CRC32 checksum with that of the remote file.

Furthermore, the MetaAlmanac guarantees the use of the most up-to-date versions of these files. An example is the daily Earth Orientation Parameters published by JPL, termed the "high precision Earth rotation" kernel. The MetaAlmanac enables users to seamlessly access the latest version of these files.


```python
from anise import MetaAlmanac

MetaAlmanac?
```


    [0;31mInit signature:[0m [0mMetaAlmanac[0m[0;34m([0m[0mmaybe_path[0m[0;34m=[0m[0;32mNone[0m[0;34m)[0m[0;34m[0m[0;34m[0m[0m
    [0;31mDocstring:[0m
    A structure to set up an Almanac, with automatic downloading, local storage, checksum checking, and more.

    # Behavior
    If the URI is a local path, relative or absolute, nothing will be fetched from a remote. Relative paths are relative to the execution folder (i.e. the current working directory).
    If the URI is a remote path, the MetaAlmanac will first check if the file exists locally. If it exists, it will check that the CRC32 checksum of this file matches that of the specs.
    If it does not match, the file will be downloaded again. If no CRC32 is provided but the file exists, then the MetaAlmanac will fetch the remote file and overwrite the existing file.
    The downloaded path will be stored in the "AppData" folder.
    [0;31mFile:[0m           ~/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages/anise/__init__.py
    [0;31mType:[0m           type
    [0;31mSubclasses:[0m


## MetaAlmanac configuration

As seen in the previous cell, a MetaAlmanac is typically initialized using a path to a configuration file (the `maybe_path` argument).

The configuration file is written in [`Dhall`](https://dhall-lang.org/), an exceptional configuration language known for its safety, expressiveness, and maintainability. Dhall's design simplifies the process of configuring complex systems, making it a standout choice for tasks like initializing the MetaAlmanac.

Let's see what this looks like:


```python
with open("../../data/latest.dhall") as f:
    for line in f.readlines():
        print(line.strip())
```

    -- Latest planetary ephemerides, planetary constants, high precision Moon rotation, and daily Earth orientation parameter
    { files =
    [ { crc32 = Some 1921414410
    , uri = "http://public-data.nyxspace.com/anise/de440s.bsp"
    }
    , { crc32 = Some 2899443223
    , uri = "http://public-data.nyxspace.com/anise/v0.4/pck11.pca"
    }
    , { crc32 = Some 2133296540
    , uri = "http://public-data.nyxspace.com/anise/v0.4/moon_fk.epa"
    }
    , { crc32 = Some 1817759242
    , uri = "http://public-data.nyxspace.com/anise/moon_pa_de440_200625.bpc"
    }
    , { crc32 = None Natural
    , uri =
    "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_latest_high_prec.bpc"
    }
    ]
    }


This is the default MetaAlmanac: it grabs the development ephemerides `DE440s` from the public cloud of Nyx Space, grab a copy of the high fidelity Moon Principal Axes frame, grabs the planetary constant ANISE file `pck08.pca`. It also downloads the latest high precision Earth rotation parameters from JPL.

The MetaAlmanac comes with a shortcut to download the latest info above without needing a copy of the Dhall file.


```python
almanac = MetaAlmanac.latest()
almanac.describe(bpc=True)
```

    === BPC #0 ===
    ┌─────────────────────────┬───────────────────────────────────┬───────────────────────────────────┬───────────────────────────┬────────────────────┬───────┬────────────────┐
    │ Name                    │ Start epoch                       │ End epoch                         │ Duration                  │ Interpolation kind │ Frame │ Inertial frame │
    ├─────────────────────────┼───────────────────────────────────┼────────────────────────────��──────┼───────────────────────────┼────────────────────┼───────┼────────────────┤
    │ Earth PCK, ITRF93 Frame │ 2000-01-01T00:01:04.183912847 TDB │ 2002-09-26T21:18:50.632952778 TDB │ 999 days 21 h 17 min 46 s │ Chebyshev Triplet  │ 3000  │ 17             │
    ├─────────────────────────┼───────────────────────────────────┼───────────────────────────────────┼───────────────────────────┼────────────────────┼───────┼────────────────┤
    │ Earth PCK, ITRF93 Frame │ 2002-09-26T21:18:50.632952778 TDB │ 2005-06-22T18:36:37.081996238 TDB │ 999 days 21 h 17 min 46 s │ Chebyshev Triplet  │ 3000  │ 17             │
    ├─────────────────────────┼───────────────────────────────────┼───────────────────────────────────┼───────────────────────────┼────────────────────┼───────┼────────────────┤
    │ Earth PCK, ITRF93 Frame │ 2005-06-22T18:36:37.081996238 TDB │ 2008-03-18T15:54:23.531035669 TDB │ 999 days 21 h 17 min 46 s │ Chebyshev Triplet  │ 3000  │ 17             │
    ├─────────────────────────┼─────────────────────���─────────────┼───────────────────────────────────┼───────────────────────────┼────────────────────┼───────┼────────────────┤
    │ Earth PCK, ITRF93 Frame │ 2008-03-18T15:54:23.531035669 TDB │ 2010-12-13T13:12:09.980072814 TDB │ 999 days 21 h 17 min 46 s │ Chebyshev Triplet  │ 3000  │ 17             │
    ├─────────────────────────┼───────────────────────────────────┼───────────────────────────────────┼───────────────────────────┼────────────────────┼───────┼────────────────┤
    │ Earth PCK, ITRF93 Frame │ 2010-12-13T13:12:09.980072814 TDB │ 2013-09-08T10:29:56.429117874 TDB │ 999 days 21 h 17 min 46 s │ Chebyshev Triplet  │ 3000  │ 17             │
    ├─────────────────────────┼───────────────────────────────────┼───────────────────────────────────┼───────────────────────────┼────────────────────┼───────┼────────────────┤
    │ Earth PCK, ITRF93 Frame │ 2013-09-08T10:29:56.429117874 TDB │ 2016-06-04T07:47:42.878162558 TDB │ 999 days 21 h 17 min 46 s │ Chebyshev Triplet  │ 3000  │ 17             │
    ├─────────────────────────┼───────────────────────────────────┼───────────────────────────────────┼───────────────────────────┼────────────────────┼───────┼────────────────┤
    │ Earth PCK, ITRF93 Frame │ 2016-06-04T07:47:42.878162558 TDB │ 2019-03-01T05:05:29.327196302 TDB │ 999 days 21 h 17 min 46 s │ Chebyshev Triplet  │ 3000  │ 17             │
    ├─────────────────────────┼───────────────────────────────────┼───────────────────────────────────┼──��────────────────────────┼────────────────────┼───────┼────────────────┤
    │ Earth PCK, ITRF93 Frame │ 2019-03-01T05:05:29.327196302 TDB │ 2021-11-25T02:23:15.776233885 TDB │ 999 days 21 h 17 min 46 s │ Chebyshev Triplet  │ 3000  │ 17             │
    ├─────────────────────────┼───────────────────────────────────┼───────────────────────────────────┼───────────────────────────┼────────────────────┼───────┼────────────────┤
    │ Earth PCK, ITRF93 Frame │ 2021-11-25T02:23:15.776233885 TDB │ 2024-04-19T00:01:09.185602312 TDB │ 875 days 21 h 37 min 53 s │ Chebyshev Triplet  │ 3000  │ 17             │
    └─────────────────────────┴───────────────────────────────────┴───────────────────────────────────┴───────────────────────────┴────────────────────┴───────┴────────────────┘
    === BPC #1 ===
    ┌───────────┬───────────────────────────────────┬───────────────────────────────────┬─────────────┬─────────────────��──┬───────┬────────────────┐
    │ Name      │ Start epoch                       │ End epoch                         │ Duration    │ Interpolation kind │ Frame │ Inertial frame │
    ├───────────┼───────────────────────────────────┼───────────────────────────────────┼─────────────┼────────────────────┼───────┼────────────────┤
    │ de440.nio │ 1449-12-26T23:59:59.999860483 TDB │ 2426-02-15T23:59:59.999891009 TDB │ 320000 days │ Chebyshev Triplet  │ 31008 │ 1              │
    ├───────────┼───────────────────────────────────┼──���────────────────────────────────┼─────────────┼────────────────────┼───────┼────────────────┤
    │ de440.nio │ 2426-02-15T23:59:59.999891009 TDB │ 2650-01-24T23:59:59.999798018 TDB │ 81792 days  │ Chebyshev Triplet  │ 31008 │ 1              │
    └───────────┴───────────────────────────────────┴───────────────────────────────────┴─────────────┴────────────────────┴───────┴────────────────┘


The data downloaded from Nyx Space cloud has a checksum in the configuration file: that's because we know exactly what this data should be. Hence, if the data is modified in your local copy, the MetaAlmanac will download it again and replace your local copy. However, the JPL data changes daily, so we don't store a checksum in the config file, ensuring that the latest data is always downloaded.

ANISE also provides a local config file to use the data stored in a copy of the repo.


```python
with open("../../data/local.dhall") as f:
    for line in f.readlines():
        print(line.strip())
```

    -- Default Almanac
    { files =
    [ { crc32 = None Natural, uri = "../../data/de440s.bsp" }
    , { crc32 = None Natural, uri = "../../data/pck08.pca" }
    ]
    }


The CRC32 integrity number is not set for local paths because in any case, the MetaAlmanac does not know where to fetch another version where the checksum should match.

## Using the MetaAlmanac

The MetaAlmanac is designed to work seamlessly with the Alamac itself. In the following example, we'll use the latest MetaAlmanac (the same that's in `latest.dhall`) and see that it can be used to return the Almanac directly.


```python
meta = MetaAlmanac.load("../../data/latest.dhall")
print(meta)
```

    MetaAlmanac { files: [MetaFile { uri: "http://public-data.nyxspace.com/anise/de440s.bsp", crc32: Some(1921414410) }, MetaFile { uri: "http://public-data.nyxspace.com/anise/v0.4/pck11.pca", crc32: Some(2899443223) }, MetaFile { uri: "http://public-data.nyxspace.com/anise/v0.4/moon_fk.epa", crc32: Some(2133296540) }, MetaFile { uri: "http://public-data.nyxspace.com/anise/moon_pa_de440_200625.bpc", crc32: Some(1817759242) }, MetaFile { uri: "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_latest_high_prec.bpc", crc32: None }] }



```python
almanac = meta.process()
print(almanac)
```

    Almanac: #SPK = 1	#BPC = 2	PlanetaryData with 54 ID mappings and 0 name mappings	EulerParameterData with 3 ID mappings and 3 name mappings


Trivial! We now see that the loaded Almanac has one loaded SPK file (the de440s file), one BPC file (the latest Earth high precision rotation), and 49 planetary data mappings, loaded from the `pck08.pca`.

Even simpler, you can just call the `latest()` class method which will call the `latest.dhall` equivalent, without requiring a local configuration file.


```python
print(MetaAlmanac.latest())
```

    Almanac: #SPK = 1	#BPC = 2	PlanetaryData with 54 ID mappings and 0 name mappings	EulerParameterData with 3 ID mappings and 3 name mappings


## Building a MetaAlmanac config

Building a Dhall configuration for ANISE can be approached in two ways. The most direct method is to craft a Dhall file manually. However, given the complexity often associated with writing in Dhall, ANISE offers a more user-friendly alternative through the `MetaFile` class. This option simplifies the process of creating the necessary data, catering to users who may find direct Dhall scripting challenging.


```python
from anise import MetaFile
MetaFile?
```


    [0;31mInit signature:[0m [0mMetaFile[0m[0;34m([0m[0muri[0m[0;34m,[0m [0mcrc32[0m[0;34m=[0m[0;32mNone[0m[0;34m)[0m[0;34m[0m[0;34m[0m[0m
    [0;31mFile:[0m           ~/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages/anise/__init__.py
    [0;31mType:[0m           type
    [0;31mSubclasses:[0m



```python
# Let's initialize a new empty MetaAlmanac.
new_meta = MetaAlmanac()
new_meta.process() # Note that you can always initialize an empty MetaAlmanac because you can initialize an empty Almanac
```




    Almanac: #SPK = 0	#BPC = 0 (@0x5582525a9d10)




```python
# Create MetaFile instances
local_de = MetaFile("../../data/de440s.bsp")
jpl_moon_rotation = MetaFile("https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/moon_pa_de440_200625.bpc")
non_existing = MetaFile("https://google.com/non/existing/pck08.pca")
# Add them to the meta almanac
new_meta.files = [local_de, jpl_moon_rotation, non_existing]
# And print what this configuration would be:
new_meta.dumps()
```




    '{ files = [{ crc32 = None Natural, uri = "../../data/de440s.bsp" }, { crc32 = None Natural, uri = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/moon_pa_de440_200625.bpc" }, { crc32 = None Natural, uri = "https://google.com/non/existing/pck08.pca" }] }'



Note that the MetaAlmanac will raise an error in case it cannot download the files. Let's try to load the configuration we just specified.


```python
# You can call a specific file's `process` method to handle this specific file
non_existing.process?
```


    [0;31mSignature:[0m [0mnon_existing[0m[0;34m.[0m[0mprocess[0m[0;34m([0m[0;34m)[0m[0;34m[0m[0;34m[0m[0m
    [0;31mDocstring:[0m
    Processes this MetaFile by downloading it if it's a URL.

    This function modified `self` and changes the URI to be the path to the downloaded file.
    [0;31mType:[0m      builtin_function_or_method



```python
# This does nothing because it's a local file
local_de.process()
```


```python
# Trying to download the non existing file will throw an exception
non_existing.process()
```


    ---------------------------------------------------------------------------

    Exception                                 Traceback (most recent call last)

    Cell In[13], line 2
          1 # Trying to download the non existing file will throw an exception
    ----> 2 non_existing.process()


    Exception: fetching https://google.com/non/existing/pck08.pca returned 404 Not Found



```python
# Trying to process the full meta almanac with an erroneous meta file will also throw an exception.
new_meta.process()
```


    ---------------------------------------------------------------------------

    Exception                                 Traceback (most recent call last)

    Cell In[14], line 2
          1 # Trying to process the full meta almanac with an erroneous meta file will also throw an exception.
    ----> 2 new_meta.process()


    Exception: processing file #2 (MetaFile { uri: "https://google.com/non/existing/pck08.pca", crc32: None }) caused an error: fetching https://google.com/non/existing/pck08.pca returned 404 Not Found


## Directly loading a MetaFile

Say you have an `Almanac` loaded with some of your files. And then you'd like to load one file that is stored remotely. You may do so directly with the `load_from_metafile` method of the Almanac.

**Note:** an Almanac may only load _one_ planetary constants kernel and _one_ Euler parameters kernel. As such, if your Almanac already includes one of these, loading another one will _replace it_. Refer to tutorial #05 on how to build your own PCA and EPA files that include everything you need.


```python
from anise import Almanac
only_de440s = Almanac("../../data/de440s.bsp").load("../../data/pck11.pca")
print(only_de440s)
# Now load a PCA from the Nyx Space cloud
de440s_and_moon = only_de440s.load_from_metafile(MetaFile("http://public-data.nyxspace.com/anise/v0.4/moon_fk.epa", 2133296540))
print(de440s_and_moon)
```

    Almanac: #SPK = 1	#BPC = 0	PlanetaryData with 54 ID mappings and 0 name mappings
    Almanac: #SPK = 1	#BPC = 0	PlanetaryData with 54 ID mappings and 0 name mappings	EulerParameterData with 3 ID mappings and 3 name mappings


To confirm that we've loaded the Moon FK file, let's grab the frame info from the Moon ME and Moon PA frames.


```python
from anise.astro.constants import Frames
print(de440s_and_moon.frame_info(Frames.MOON_ME_FRAME))
print(de440s_and_moon.frame_info(Frames.MOON_PA_FRAME))
```

    Moon MOON_ME (μ = 4902.800066163796 km^3/s^2, radius = 1737.4 km)
    Moon MOON_PA (μ = 4902.800066163796 km^3/s^2, radius = 1737.4 km)


## Exercises

### Learning Goals:

1. Understand the structure and syntax of Dhall configuration files.
1. Learn how to use the MetaFile tool for easier configuration creation.
1. Gain insight into how different configurations affect the MetaAlmanac's operation.


### 1. Manual Dhall Configuration:

+ Create a simple Dhall configuration file.
+ Include basic elements like a specific ephemerides file and a custom planetary constant file.
+ Load this configuration into the MetaAlmanac, observe the behavior, and query the loaded Almanac itself.

### 2. Using MetaFile:

+ Use the `MetaFile` class to generate the same configuration.
+ Compare the process of using MetaFile with manual Dhall file creation.
+ Load the generated configuration into the MetaAlmanac.

_Note:_ Almanac, MetaFile, and MetaAlmana all support the equality operation in Python.
