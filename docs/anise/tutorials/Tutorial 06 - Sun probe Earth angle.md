# ANISE

ANISE is a modern rewrite of NAIF SPICE, written in Rust and providing interfaces to other languages including Python.

Evidently, this tutorial applies to the Python usage of ANISE.

## Goal
By the end of this tutorial, you should know how to build a data frame containing the Sun probe Earth angle of a given spacecraft BSP and plot that information. Your exercise will be to confirm that this calculation is correct by computing the Sun elevation at nadir below the spacecraft as detailed in tutorial 04.## Loading the latest orientation and planetary data

Let's start by installing ANISE: `pip install anise`

## Load a BSP containing a spacecraft trajectory

In this tutorial, we will use the `gmat-hermite.bsp` file which contains some trajectory data build in GMAT and used in ANISE for validation purposes. Although the Sun probe Earth angle _typically_ applies to spacecraft trajectories, the calculation works for any two objects.


```python
from anise import MetaAlmanac
almanac = MetaAlmanac.latest().load("../../data/gmat-hermite.bsp")
almanac.describe(spk=True)
```

    === SPK #0 ===
    ┌─────────────┬──────────────────────┬─────────────┬───────────────────────────────────┬───────────────────────────────────┬────────────┬──────────────────────┐
    │ Name        │ Target               │ Center      │ Start epoch                       │ End epoch                         │ Duration   │ Interpolation kind   │
    ├─────────────┼──────────────────────┼─────────────┼───────────────────────────────────┼───────────────────────────────────┼────────────┼──────────────────────┤
    │ SPK_SEGMENT │ body -10000001 J2000 │ Earth J2000 │ 2000-01-01T12:00:32.183927328 TDB │ 2000-01-01T15:20:32.183931556 TDB │ 3 h 20 min │ Hermite Unequal Step │
    └─────────────┴──────────────────────┴─────────────┴───────────────────────────────────┴───────────────────────────────────┴────────────┴──────────────────────┘
    === SPK #1 ===
    ┌────────────────┬─────────────────────────────┬─────────��─────────────────────┬───────────────────────────────────┬───────────────────────────────────┬─────────────┬────────────────────┐
    │ Name           │ Target                      │ Center                        │ Start epoch                       │ End epoch                         │ Duration    │ Interpolation kind │
    ├────────────────┼─────────────────────────────┼───────────────────────────────┼───────────────────────────────────┼───────────────────��───────────────┼─────────────┼────────────────────┤
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


We have successfully loaded two BSP files, one with the planetary data and the other with spacecraft data. We now know that this spacecraft has the ID `-10000001`. We can actually query the Almanac for the precise start and stop epochs (returned as hifitime `Epoch` objects) of this ID in our loaded files.


```python
start_epoch, stop_epoch = almanac.spk_domain(-10000001)
print(start_epoch, stop_epoch)
```

    2000-01-01T11:59:28.000000021 UTC 2000-01-01T15:19:28.000000226 UTC


The Sun Probe Earth angle is the angle between a probe and the Sun and the probe the Earth. It allows one to know whether the point exactly nadir (i.e. below) the spacecraft is illuminated by the Sun or not. This is helpful information if the spacecraft carries a visible light camera and needs to take pictures when it's daytime below the spacecraft.

Let's look at the signature of this function.


```python
almanac.sun_angle_deg?
```


    [0;31mSignature:[0m [0malmanac[0m[0;34m.[0m[0msun_angle_deg[0m[0;34m([0m[0mtarget_id[0m[0;34m,[0m [0mobserver_id[0m[0;34m,[0m [0mepoch[0m[0;34m)[0m[0;34m[0m[0;34m[0m[0m
    [0;31mDocstring:[0m
    Returns the angle (between 0 and 180 degrees) between the observer and the Sun, and the observer and the target body ID.
    This computes the Sun Probe Earth angle (SPE) if the probe is in a loaded, its ID is the "observer_id", and the target is set to its central body.

    # Geometry
    If the SPE is greater than 90 degrees, then the celestial object below the probe is in sunlight.

    ## Sunrise at nadir
    ```text
    Sun
     |  \
     |   \
     |    \
     Obs. -- Target
    ```
    ## Sun high at nadir
    ```text
    Sun
     \
      \  __ θ > 90
       \     \
        Obs. ---------- Target
    ```

    ## Sunset at nadir
    ```text
             Sun
           /
          /  __ θ < 90
         /    /
     Obs. -- Target
    ```

    # Algorithm
    1. Compute the position of the Sun as seen from the observer
    2. Compute the position of the target as seen from the observer
    3. Return the arccosine of the dot product of the norms of these vectors.
    [0;31mType:[0m      builtin_function_or_method


One will note that this function is generic to what the "probe" SPK ID is ("observer") and what its central object should be instead of Earth ("target").

The other crucial point here is that this is one of the few functions where the object _ID_ is required instead of a frame. This is because the Almanac will compute everything in the J2000 frame. Don't worry, if you have frame objects instead, you may use the `sun_angle_deg_from_frame` function instead.

Let's see what is the SPE of our spacecraft at the start of the trajectory.



```python
from anise.astro.constants import CelestialObjects
almanac.sun_angle_deg(-10000001, CelestialObjects.EARTH, start_epoch)
```




    83.87312777296376



A angle of less than 90 degrees means that the nadir point is in the darkness. Let's look at the evolution of the SPE over the duration of the trajectory.

## Package installation for plotting


```python
%pip install "polars[plot]" hvplot geoviews # geoviews for geographic data
```

    Requirement already satisfied: polars[plot] in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (0.20.4)
    Requirement already satisfied: hvplot in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (0.9.1)
    Collecting geoviews
      Downloading geoviews-1.11.0-py2.py3-none-any.whl (511 kB)
    [2K     [38;2;114;156;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m511.2/511.2 kB[0m [31m690.4 kB/s[0m eta [36m0:00:00[0m kB/s[0m eta [36m0:00:01[0m:01[0m
    [?25hRequirement already satisfied: bokeh>=1.0.0 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from hvplot) (3.3.3)
    Requirement already satisfied: colorcet>=2 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from hvplot) (3.0.1)
    Requirement already satisfied: holoviews>=1.11.0 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from hvplot) (1.18.1)
    Requirement already satisfied: pandas in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from hvplot) (2.1.4)
    Requirement already satisfied: numpy>=1.15 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from hvplot) (1.26.3)
    Requirement already satisfied: packaging in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from hvplot) (23.2)
    Requirement already satisfied: panel>=0.11.0 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from hvplot) (1.3.6)
    Requirement already satisfied: param<3.0,>=1.12.0 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from hvplot) (2.0.1)
    Collecting cartopy>=0.18.0 (from geoviews)
      Downloading Cartopy-0.22.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (11.9 MB)
    [2K     [38;2;114;156;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m11.9/11.9 MB[0m [31m14.1 MB/s[0m eta [36m0:00:00[0mm eta [36m0:00:01[0m[36m0:00:01[0m
    [?25hCollecting shapely (from geoviews)
      Downloading shapely-2.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.5 MB)
    [2K     [38;2;114;156;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m2.5/2.5 MB[0m [31m54.5 MB/s[0m eta [36m0:00:00[0m31m72.7 MB/s[0m eta [36m0:00:01[0m
    [?25hCollecting pyproj (from geoviews)
      Downloading pyproj-3.6.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (8.6 MB)
    [2K     [38;2;114;156;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m8.6/8.6 MB[0m [31m13.8 MB/s[0m eta [36m0:00:00[0mm eta [36m0:00:01[0m0:01[0m:01[0m
    [?25hRequirement already satisfied: xyzservices in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from geoviews) (2023.10.1)
    Requirement already satisfied: Jinja2>=2.9 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from bokeh>=1.0.0->hvplot) (3.1.2)
    Requirement already satisfied: contourpy>=1 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from bokeh>=1.0.0->hvplot) (1.2.0)
    Requirement already satisfied: pillow>=7.1.0 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from bokeh>=1.0.0->hvplot) (10.2.0)
    Requirement already satisfied: PyYAML>=3.10 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from bokeh>=1.0.0->hvplot) (6.0.1)
    Requirement already satisfied: tornado>=5.1 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from bokeh>=1.0.0->hvplot) (6.4)
    Collecting matplotlib>=3.4 (from cartopy>=0.18.0->geoviews)
      Downloading matplotlib-3.8.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (11.6 MB)
    [2K     [38;2;114;156;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m11.6/11.6 MB[0m [31m47.7 MB/s[0m eta [36m0:00:00[0mm eta [36m0:00:01[0m[36m0:00:01[0m
    [?25hCollecting pyshp>=2.1 (from cartopy>=0.18.0->geoviews)
      Downloading pyshp-2.3.1-py2.py3-none-any.whl (46 kB)
    [2K     [38;2;114;156;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m46.5/46.5 kB[0m [31m14.8 MB/s[0m eta [36m0:00:00[0m
    [?25hRequirement already satisfied: pyct>=0.4.4 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from colorcet>=2->hvplot) (0.5.0)
    Requirement already satisfied: pyviz-comms>=0.7.4 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from holoviews>=1.11.0->hvplot) (3.0.0)
    Requirement already satisfied: python-dateutil>=2.8.2 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from pandas->hvplot) (2.8.2)
    Requirement already satisfied: pytz>=2020.1 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from pandas->hvplot) (2023.3.post1)
    Requirement already satisfied: tzdata>=2022.1 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from pandas->hvplot) (2023.4)
    Requirement already satisfied: markdown in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from panel>=0.11.0->hvplot) (3.5.2)
    Requirement already satisfied: markdown-it-py in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from panel>=0.11.0->hvplot) (3.0.0)
    Requirement already satisfied: linkify-it-py in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from panel>=0.11.0->hvplot) (2.0.2)
    Requirement already satisfied: mdit-py-plugins in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from panel>=0.11.0->hvplot) (0.4.0)
    Requirement already satisfied: requests in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from panel>=0.11.0->hvplot) (2.31.0)
    Requirement already satisfied: tqdm>=4.48.0 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from panel>=0.11.0->hvplot) (4.66.1)
    Requirement already satisfied: bleach in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from panel>=0.11.0->hvplot) (6.1.0)
    Requirement already satisfied: typing-extensions in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from panel>=0.11.0->hvplot) (4.9.0)
    Requirement already satisfied: certifi in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from pyproj->geoviews) (2023.11.17)
    Requirement already satisfied: MarkupSafe>=2.0 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from Jinja2>=2.9->bokeh>=1.0.0->hvplot) (2.1.3)
    Collecting cycler>=0.10 (from matplotlib>=3.4->cartopy>=0.18.0->geoviews)
      Downloading cycler-0.12.1-py3-none-any.whl (8.3 kB)
    Collecting fonttools>=4.22.0 (from matplotlib>=3.4->cartopy>=0.18.0->geoviews)
      Downloading fonttools-4.47.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (4.9 MB)
    [2K     [38;2;114;156;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m4.9/4.9 MB[0m [31m49.5 MB/s[0m eta [36m0:00:00[0m31m56.4 MB/s[0m eta [36m0:00:01[0m
    [?25hCollecting kiwisolver>=1.3.1 (from matplotlib>=3.4->cartopy>=0.18.0->geoviews)
      Downloading kiwisolver-1.4.5-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (1.4 MB)
    [2K     [38;2;114;156;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m1.4/1.4 MB[0m [31m47.4 MB/s[0m eta [36m0:00:00[0m
    [?25hCollecting pyparsing>=2.3.1 (from matplotlib>=3.4->cartopy>=0.18.0->geoviews)
      Downloading pyparsing-3.1.1-py3-none-any.whl (103 kB)
    [2K     [38;2;114;156;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m103.1/103.1 kB[0m [31m42.5 MB/s[0m eta [36m0:00:00[0m
    [?25hRequirement already satisfied: six>=1.5 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from python-dateutil>=2.8.2->pandas->hvplot) (1.16.0)
    Requirement already satisfied: webencodings in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from bleach->panel>=0.11.0->hvplot) (0.5.1)
    Requirement already satisfied: uc-micro-py in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from linkify-it-py->panel>=0.11.0->hvplot) (1.0.2)
    Requirement already satisfied: mdurl~=0.1 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from markdown-it-py->panel>=0.11.0->hvplot) (0.1.2)
    Requirement already satisfied: charset-normalizer<4,>=2 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from requests->panel>=0.11.0->hvplot) (3.3.2)
    Requirement already satisfied: idna<4,>=2.5 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from requests->panel>=0.11.0->hvplot) (3.6)
    Requirement already satisfied: urllib3<3,>=1.21.1 in /home/chris/Workspace/nyx-space/anise/anise-py/.venv/lib64/python3.11/site-packages (from requests->panel>=0.11.0->hvplot) (2.1.0)
    Installing collected packages: shapely, pyshp, pyproj, pyparsing, kiwisolver, fonttools, cycler, matplotlib, cartopy, geoviews
    Successfully installed cartopy-0.22.0 cycler-0.12.1 fonttools-4.47.2 geoviews-1.11.0 kiwisolver-1.4.5 matplotlib-3.8.2 pyparsing-3.1.1 pyproj-3.6.1 pyshp-2.3.1 shapely-2.0.2

    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m A new release of pip is available: [0m[31;49m23.1.2[0m[39;49m -> [0m[32;49m23.3.2[0m
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m To update, run: [0m[32;49mpip install --upgrade pip[0m
    Note: you may need to restart the kernel to use updated packages.


## Evolution of SPE over time

We'll plot the change in Sun probe Earth angle over time. We'll also grab the latitude and longitude data so we can plot the position of the spacecraft above the Earth at those times (as a separate plot).


```python
from anise.time import TimeSeries, Unit, Epoch
from anise.astro import Frame
from anise.astro.constants import Frames, Orientations

import polars as pl
from datetime import datetime

def hifitime_to_datetime(e: Epoch) -> datetime:
    return datetime.fromisoformat(str(e).replace(" UTC", "")[:23])

epochs = []
spe_deg = []
lat_deg = []
long_deg = []

# Let's be sure to load the PCK data, which includes the frame information such as the shape of
# the ellipsoid and how to compute the rotation of the body fixed frames
almanac = almanac.load("../../data/pck08.pca")

SC_ID = -10000001
SC_J2K = Frame(SC_ID, Orientations.J2000)

for epoch in TimeSeries(start_epoch, stop_epoch, Unit.Minute*1, inclusive=True):
    epochs += [hifitime_to_datetime(epoch)]
    spe_deg += [almanac.sun_angle_deg(CelestialObjects.EARTH, SC_ID, epoch)]
    # Grab position of the spacecraft in the IAU Earth frame
    sc_iau_earth = almanac.transform(SC_J2K, Frames.IAU_EARTH_FRAME, epoch)
    lat_deg += [sc_iau_earth.latitude_deg()]
    long_deg += [sc_iau_earth.longitude_deg()]
```


```python
# Build the data frame
df = pl.DataFrame(
    {
        'Epoch': epochs,
        'Sun Probe Earth angle (deg)': spe_deg,
        'Latitude (deg)': lat_deg,
        'Longitude (deg)': long_deg
    }
)
```


```python
import hvplot.polars
from bokeh.models.formatters import DatetimeTickFormatter

formatter = DatetimeTickFormatter(days='%d/%m') # Make the world a better place

df.hvplot(x="Epoch", y="Sun Probe Earth angle (deg)", xformatter=formatter,
          title="Sun probe Earth angle over time", hover_cols=["Latitude (deg)", "Longitude (deg)"])
```






<div id='p2696'>
  <div id="a9b07ef4-1563-4f6b-82f6-d1775f043b78" data-root-id="p2696" style="display: contents;"></div>
</div>
<script type="application/javascript">(function(root) {
  var docs_json = {"c4d768b9-cc45-4f15-b361-986c2a46aa8c":{"version":"3.3.3","title":"Bokeh Application","roots":[{"type":"object","name":"Row","id":"p2696","attributes":{"name":"Row04004","tags":["embedded"],"stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"type":"object","name":"ImportedStyleSheet","id":"p2699","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.6/dist/css/loading.css"}},{"type":"object","name":"ImportedStyleSheet","id":"p2767","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.6/dist/css/listpanel.css"}},{"type":"object","name":"ImportedStyleSheet","id":"p2697","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.6/dist/bundled/theme/default.css"}},{"type":"object","name":"ImportedStyleSheet","id":"p2698","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.6/dist/bundled/theme/native.css"}}],"min_width":700,"margin":0,"sizing_mode":"stretch_width","align":"start","children":[{"type":"object","name":"Spacer","id":"p2700","attributes":{"name":"HSpacer04011","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"p2699"},{"id":"p2697"},{"id":"p2698"}],"margin":0,"sizing_mode":"stretch_width","align":"start"}},{"type":"object","name":"Figure","id":"p2708","attributes":{"width":700,"height":300,"margin":[5,10],"sizing_mode":"fixed","align":"start","x_range":{"type":"object","name":"Range1d","id":"p2701","attributes":{"tags":[[["Epoch","Epoch",null]],[]],"start":946727968000.0,"end":946739967999.0001,"reset_start":946727968000.0,"reset_end":946739967999.0001}},"y_range":{"type":"object","name":"Range1d","id":"p2702","attributes":{"tags":[[["Sun Probe Earth angle (deg)","Sun Probe Earth angle (deg)",null]],{"type":"map","entries":[["invert_yaxis",false],["autorange",false]]}],"start":2.5590908527804554,"end":177.392232338912,"reset_start":2.5590908527804554,"reset_end":177.392232338912}},"x_scale":{"type":"object","name":"LinearScale","id":"p2718"},"y_scale":{"type":"object","name":"LinearScale","id":"p2719"},"title":{"type":"object","name":"Title","id":"p2711","attributes":{"text":"Sun probe Earth angle over time","text_color":"black","text_font_size":"12pt"}},"renderers":[{"type":"object","name":"GlyphRenderer","id":"p2760","attributes":{"data_source":{"type":"object","name":"ColumnDataSource","id":"p2751","attributes":{"selected":{"type":"object","name":"Selection","id":"p2752","attributes":{"indices":[],"line_indices":[]}},"selection_policy":{"type":"object","name":"UnionRenderers","id":"p2753"},"data":{"type":"map","entries":[["Epoch",{"type":"ndarray","array":{"type":"bytes","data":"AACgS6yNa0IAAOxorI1rQgDgN4asjWtCAOCDo6yNa0IA4M/ArI1rQgDgG96sjWtCAOBn+6yNa0IA4LMYrY1rQgDg/zWtjWtCAOBLU62Na0IA4JdwrY1rQgDg442tjWtCAOAvq62Na0IA4HvIrY1rQgDgx+WtjWtCAOATA66Na0IA4F8gro1rQgDgqz2ujWtCAOD3Wq6Na0IA4EN4ro1rQgDgj5WujWtCAODbsq6Na0IA4CfQro1rQgDgc+2ujWtCAOC/Cq+Na0IA4Asor41rQgDgV0WvjWtCAOCjYq+Na0IA4O9/r41rQgDgO52vjWtCAOCHuq+Na0IA4NPXr41rQgDgH/WvjWtCAOBrErCNa0IA4LcvsI1rQgDgA02wjWtCAOBParCNa0IA4JuHsI1rQgDg56SwjWtCAOAzwrCNa0IA4H/fsI1rQgDgy/ywjWtCAOAXGrGNa0IA4GM3sY1rQgDgr1SxjWtCAOD7cbGNa0IA4EePsY1rQgDgk6yxjWtCAODfybGNa0IA4CvnsY1rQgDgdwSyjWtCAODDIbKNa0IA4A8/so1rQgDgW1yyjWtCAOCnebKNa0IA4POWso1rQgDgP7SyjWtCAOCL0bKNa0IA4Nfuso1rQgDgIwyzjWtCAOBvKbONa0IA4LtGs41rQgDgB2SzjWtCAOBTgbONa0IA4J+es41rQgDg67uzjWtCAOA32bONa0IA4IP2s41rQgDgzxO0jWtCAOAbMbSNa0IA4GdOtI1rQgDgs2u0jWtCAOD/iLSNa0IA4EumtI1rQgDgl8O0jWtCAODj4LSNa0IA4C/+tI1rQgDgexu1jWtCAODHOLWNa0IA4BNWtY1rQgDgX3O1jWtCAOCrkLWNa0IA4PettY1rQgDgQ8u1jWtCAOCP6LWNa0IA4NsFto1rQgDgJyO2jWtCAOBzQLaNa0IA4L9dto1rQgDgC3u2jWtCAOBXmLaNa0IA4KO1to1rQgDg79K2jWtCAOA78LaNa0IA4IcNt41rQgDg0yq3jWtCAOAfSLeNa0IA4Gtlt41rQgDgt4K3jWtCAOADoLeNa0IA4E+9t41rQgDgm9q3jWtCAODn97eNa0IA4DMVuI1rQgDgfzK4jWtCAODLT7iNa0IA4BdtuI1rQgDgY4q4jWtCAOCvp7iNa0IA4PvEuI1rQgDgR+K4jWtCAOCT/7iNa0IA4N8cuY1rQgDgKzq5jWtCAOB3V7mNa0IA4MN0uY1rQgDgD5K5jWtCAOBbr7mNa0IA4KfMuY1rQgDg8+m5jWtCAOA/B7qNa0IA4Iskuo1rQgDg10G6jWtCAOAjX7qNa0IA4G98uo1rQgDgu5m6jWtCAOAHt7qNa0IA4FPUuo1rQgDgn/G6jWtCAODrDruNa0IA4Dcsu41rQgDgg0m7jWtCAODPZruNa0IA4BuEu41rQgDgZ6G7jWtCAOCzvruNa0IA4P/bu41rQgDgS/m7jWtCAOCXFryNa0IA4OMzvI1rQgDgL1G8jWtCAOB7bryNa0IA4MeLvI1rQgDgE6m8jWtCAOBfxryNa0IA4KvjvI1rQgDg9wC9jWtCAOBDHr2Na0IA4I87vY1rQgDg21i9jWtCAOAndr2Na0IA4HOTvY1rQgDgv7C9jWtCAOALzr2Na0IA4FfrvY1rQgDgowi+jWtCAODvJb6Na0IA4DtDvo1rQgDgh2C+jWtCAODTfb6Na0IA4B+bvo1rQgDga7i+jWtCAOC31b6Na0IA4APzvo1rQgDgTxC/jWtCAOCbLb+Na0IA4OdKv41rQgDgM2i/jWtCAOB/hb+Na0IA4Muiv41rQgDgF8C/jWtCAOBj3b+Na0IA4K/6v41rQgDg+xfAjWtCAOBHNcCNa0IA4JNSwI1rQgDg32/AjWtCAOArjcCNa0IA4HeqwI1rQgDgw8fAjWtCAOAP5cCNa0IA4FsCwY1rQgDgpx/BjWtCAODzPMGNa0IA4D9awY1rQgDgi3fBjWtCAODXlMGNa0IA4COywY1rQgDgb8/BjWtCAOC77MGNa0IA4AcKwo1rQgDgUyfCjWtCAOCfRMKNa0IA4Othwo1rQgDgN3/CjWtCAOCDnMKNa0IA4M+5wo1rQgDgG9fCjWtCAOBn9MKNa0IA4LMRw41rQgDg/y7DjWtC"},"shape":[201],"dtype":"float64","order":"little"}],["Sun Probe Earth angle (deg)",{"type":"ndarray","array":{"type":"bytes","data":"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"},"shape":[201],"dtype":"float64","order":"little"}],["Sun_Probe_Earth_angle_left_parenthesis_deg_right_parenthesis",{"type":"ndarray","array":{"type":"bytes","data":"AqM+4PAHWEBJ99DcUTBXQO3HgyFHWVZAoN7p396CVUBYe/iIJq1UQIcL9lMr2FNA4dMQyfoDU0BTtLFXozBSQLbCzwA1XlFAPDlgH8KMUEAXaDi6wHhPQKw9WslT2k1A6Of01X0+TECqTzZkj6VKQIZxBG/uD0lAslMnrB1+R0APiAGNxvBFQHe6FTTHaERAGgAeMkbnQkDs/2C3zm1BQPM6ay/y/D9AZkQy0kk4PUB420oClpU6QD176szXHzhAB8AHgynmNUAHdlh7qPwzQCEwO0NjfDJAXkJ1bbqAMUCqLDmk5iAxQHrUTXllZzFA+SUZhTVNMkDVAfNqMb0zQE5SmvtqnDVAATLE0UvRN0DtHuWL30Y6QDIVUhBA7TxAa0uAKsi4P0D/F+3lhFBBQJbQcG70z0JAyw8QO3dYRED7ZzjMZuhFQIFKV4KGfkdArFooouUZSUDK1qhbyrlKQBrdLfqiXUxAl4ShTPsETkAS3Bz3dK9PQMAIKeVgrlBAkT29w0+GUUDkEtZSal9SQLfRIeeWOVNAEav57b0UVED7ftMayfBUQKY2RLSizVVAgQvs9DSrVkBfwYB3aYlXQGQ3qaQoaFhAPNE3GllHWUBFJQ8D3yZaQPxR8VObBltAQFFl32rmW0Cp+RMuJcZcQJAE7QCbpV1AuGiRWZSEXkAzQH7SzWJfQC1KZ3z6H2BA58rxmNGNYECjuSY9q/pgQA8x6HUzZmFAA8rRsvvPYUCFyklpbzdiQCeLHCfDm2JAjbX7gNv7YkDcoAIEKVZjQGV1LWJ4qGNA7guqob/vY0DxHKGfCyhkQLozUiLeTGRARmLOaFRaZEB7xqisz05kQGW/mZLWK2RA98PEo0X1Y0DYCH8lpq9jQCUz6JL8XmNAqTvxhWIGY0DOJE2UFqhiQKtvjFKvRWJAIhKZH0zgYUDZiDsfunhhQFNkgvuND2FAiUYiSzWlYEARV+E/AjpgQDaWphJnnF9AfT8cb/PDXkAuzTDt9epdQAmx/V2rEV1AlwgPz0Q4XEAoYnxI6l5bQG15Jta8hVpANIeXEtisWUCTQdJYU9RYQDEDardC/FdAmryht7ckV0CUzYUGwk1WQMCYzApwd1VAhsT4b8+hVECDWpmu7cxTQJDv3ZjY+FJAxZv98p4lUkAYbZAgUVNRQKvjy/ABglBAwpZHMI9jT0DBc1/SecVNQPDJP80FKkxA9sQTo4WRSkAM5BjPYfxIQH4MtTQga0dAl4rDWm7eRUD/8ZiyL1dEQF5VL8SR1kJA3YSe9iheQUB0iyKzM+A/QEsNTV+oHj1AGfVhmMt/OkBnd99j0g44QNax9LMQ2zVAXKizq9P4M0DRBtYlLYEyQEvQOOchjzFAJpRH/BM5MUCp7/WGaYgxQElOPwFNdTJA6iIUm13qM0CDMXfd7cw1QDbR3b7WAzhA6DjOEYx6OkDNM51qdiE9QACOImkm7T9AdHidlqhqQUDAJuqX+OlCQFEtEvhOckRA3eWd0AkCRkANTmx075dHQIx1PQwRM0lAbEsd/rXSSkACKuNZTXZMQMe4/2djHU5AUDdqE5rHT0DG7ZioUbpQQHmiGnceklFAkah8rRZrUkCWM/OVIEVTQOgBJI0kIFRAeLQrMAz8VEByyEipwdhVQAez0RAvtlZArC6k1z2UV0BTTMQz1nJYQGFSEIbeUVlA5ko9rzoxWkAY12BJyxBbQPFWV7ds8FtASSn79vXPXEABvtobN69dQNA7TEz3jV5AmRbJCvJrX0BLXrC9aSRgQPe4PpYZkmBA0JdvVsb+YEBZdjlsGmphQHnUixel02FAkpi41M46YkBqO4MkyJ5iQA2o2SNw/mJAWJU7PDBYY0DX1IORzKljQGHxNvsy8GNAY39Zh20nZEArfbQwCUtkQI3d+HpCV2RA6SsYm6RKZECjYVSZ0yZkQNRdy/qv72NAAX9PrrWpY0CBJyf511hjQMPmDWwiAGNA7AwTB8qhYkDFYW1SXz9iQJLnT/z92WFA2Zpp73ByYUC6s6iASwlhQDVpTHv6nmBAuqsrmc8zYEDobGmKEpBfQAbwftWvt15Abnb2ScPeXUDtOfOwiQVdQPhCiyA0LFxAkrKotOpSW0BuL9CUznlaQB4Gonz7oFlA"},"shape":[201],"dtype":"float64","order":"little"}],["Latitude_left_parenthesis_deg_right_parenthesis",{"type":"ndarray","array":{"type":"bytes","data":"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"},"shape":[201],"dtype":"float64","order":"little"}],["Longitude_left_parenthesis_deg_right_parenthesis",{"type":"ndarray","array":{"type":"bytes","data":"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"},"shape":[201],"dtype":"float64","order":"little"}]]}}},"view":{"type":"object","name":"CDSView","id":"p2761","attributes":{"filter":{"type":"object","name":"AllIndices","id":"p2762"}}},"glyph":{"type":"object","name":"Line","id":"p2757","attributes":{"tags":["apply_ranges"],"x":{"type":"field","field":"Epoch"},"y":{"type":"field","field":"Sun Probe Earth angle (deg)"},"line_color":"#30a2da","line_width":2}},"selection_glyph":{"type":"object","name":"Line","id":"p2763","attributes":{"tags":["apply_ranges"],"x":{"type":"field","field":"Epoch"},"y":{"type":"field","field":"Sun Probe Earth angle (deg)"},"line_color":"#30a2da","line_width":2}},"nonselection_glyph":{"type":"object","name":"Line","id":"p2758","attributes":{"tags":["apply_ranges"],"x":{"type":"field","field":"Epoch"},"y":{"type":"field","field":"Sun Probe Earth angle (deg)"},"line_color":"#30a2da","line_alpha":0.1,"line_width":2}},"muted_glyph":{"type":"object","name":"Line","id":"p2759","attributes":{"tags":["apply_ranges"],"x":{"type":"field","field":"Epoch"},"y":{"type":"field","field":"Sun Probe Earth angle (deg)"},"line_color":"#30a2da","line_alpha":0.2,"line_width":2}}}}],"toolbar":{"type":"object","name":"Toolbar","id":"p2717","attributes":{"tools":[{"type":"object","name":"WheelZoomTool","id":"p2706","attributes":{"tags":["hv_created"],"renderers":"auto","zoom_together":"none"}},{"type":"object","name":"HoverTool","id":"p2707","attributes":{"tags":["hv_created"],"renderers":[{"id":"p2760"}],"tooltips":[["Epoch","@{Epoch}{%F %T}"],["Sun Probe Earth angle (deg)","@{Sun_Probe_Earth_angle_left_parenthesis_deg_right_parenthesis}"],["Latitude (deg)","@{Latitude_left_parenthesis_deg_right_parenthesis}"],["Longitude (deg)","@{Longitude_left_parenthesis_deg_right_parenthesis}"]],"formatters":{"type":"map","entries":[["@{Epoch}","datetime"]]}}},{"type":"object","name":"SaveTool","id":"p2742"},{"type":"object","name":"PanTool","id":"p2743"},{"type":"object","name":"BoxZoomTool","id":"p2744","attributes":{"overlay":{"type":"object","name":"BoxAnnotation","id":"p2745","attributes":{"syncable":false,"level":"overlay","visible":false,"left":{"type":"number","value":"nan"},"right":{"type":"number","value":"nan"},"top":{"type":"number","value":"nan"},"bottom":{"type":"number","value":"nan"},"left_units":"canvas","right_units":"canvas","top_units":"canvas","bottom_units":"canvas","line_color":"black","line_alpha":1.0,"line_width":2,"line_dash":[4,4],"fill_color":"lightgrey","fill_alpha":0.5}}}},{"type":"object","name":"ResetTool","id":"p2750"}],"active_drag":{"id":"p2743"},"active_scroll":{"id":"p2706"}}},"left":[{"type":"object","name":"LinearAxis","id":"p2737","attributes":{"ticker":{"type":"object","name":"BasicTicker","id":"p2738","attributes":{"mantissas":[1,2,5]}},"formatter":{"type":"object","name":"BasicTickFormatter","id":"p2739"},"axis_label":"Sun Probe Earth angle (deg)","major_label_policy":{"type":"object","name":"AllLabels","id":"p2740"}}}],"below":[{"type":"object","name":"DatetimeAxis","id":"p2720","attributes":{"ticker":{"type":"object","name":"DatetimeTicker","id":"p2721","attributes":{"num_minor_ticks":5,"tickers":[{"type":"object","name":"AdaptiveTicker","id":"p2722","attributes":{"num_minor_ticks":0,"mantissas":[1,2,5],"max_interval":500.0}},{"type":"object","name":"AdaptiveTicker","id":"p2723","attributes":{"num_minor_ticks":0,"base":60,"mantissas":[1,2,5,10,15,20,30],"min_interval":1000.0,"max_interval":1800000.0}},{"type":"object","name":"AdaptiveTicker","id":"p2724","attributes":{"num_minor_ticks":0,"base":24,"mantissas":[1,2,4,6,8,12],"min_interval":3600000.0,"max_interval":43200000.0}},{"type":"object","name":"DaysTicker","id":"p2725","attributes":{"days":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]}},{"type":"object","name":"DaysTicker","id":"p2726","attributes":{"days":[1,4,7,10,13,16,19,22,25,28]}},{"type":"object","name":"DaysTicker","id":"p2727","attributes":{"days":[1,8,15,22]}},{"type":"object","name":"DaysTicker","id":"p2728","attributes":{"days":[1,15]}},{"type":"object","name":"MonthsTicker","id":"p2729","attributes":{"months":[0,1,2,3,4,5,6,7,8,9,10,11]}},{"type":"object","name":"MonthsTicker","id":"p2730","attributes":{"months":[0,2,4,6,8,10]}},{"type":"object","name":"MonthsTicker","id":"p2731","attributes":{"months":[0,4,8]}},{"type":"object","name":"MonthsTicker","id":"p2732","attributes":{"months":[0,6]}},{"type":"object","name":"YearsTicker","id":"p2733"}]}},"formatter":{"type":"object","name":"DatetimeTickFormatter","id":"p2734","attributes":{"days":"%d/%m"}},"axis_label":"Epoch","major_label_policy":{"type":"object","name":"AllLabels","id":"p2735"}}}],"center":[{"type":"object","name":"Grid","id":"p2736","attributes":{"axis":{"id":"p2720"},"grid_line_color":null}},{"type":"object","name":"Grid","id":"p2741","attributes":{"dimension":1,"axis":{"id":"p2737"},"grid_line_color":null}}],"min_border_top":10,"min_border_bottom":10,"min_border_left":10,"min_border_right":10,"output_backend":"webgl"}},{"type":"object","name":"Spacer","id":"p2765","attributes":{"name":"HSpacer04012","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"p2699"},{"id":"p2697"},{"id":"p2698"}],"margin":0,"sizing_mode":"stretch_width","align":"start"}}]}}],"defs":[{"type":"model","name":"ReactiveHTML1"},{"type":"model","name":"FlexBox1","properties":[{"name":"align_content","kind":"Any","default":"flex-start"},{"name":"align_items","kind":"Any","default":"flex-start"},{"name":"flex_direction","kind":"Any","default":"row"},{"name":"flex_wrap","kind":"Any","default":"wrap"},{"name":"justify_content","kind":"Any","default":"flex-start"}]},{"type":"model","name":"FloatPanel1","properties":[{"name":"config","kind":"Any","default":{"type":"map"}},{"name":"contained","kind":"Any","default":true},{"name":"position","kind":"Any","default":"right-top"},{"name":"offsetx","kind":"Any","default":null},{"name":"offsety","kind":"Any","default":null},{"name":"theme","kind":"Any","default":"primary"},{"name":"status","kind":"Any","default":"normalized"}]},{"type":"model","name":"GridStack1","properties":[{"name":"mode","kind":"Any","default":"warn"},{"name":"ncols","kind":"Any","default":null},{"name":"nrows","kind":"Any","default":null},{"name":"allow_resize","kind":"Any","default":true},{"name":"allow_drag","kind":"Any","default":true},{"name":"state","kind":"Any","default":[]}]},{"type":"model","name":"drag1","properties":[{"name":"slider_width","kind":"Any","default":5},{"name":"slider_color","kind":"Any","default":"black"},{"name":"value","kind":"Any","default":50}]},{"type":"model","name":"click1","properties":[{"name":"terminal_output","kind":"Any","default":""},{"name":"debug_name","kind":"Any","default":""},{"name":"clears","kind":"Any","default":0}]},{"type":"model","name":"copy_to_clipboard1","properties":[{"name":"fill","kind":"Any","default":"none"},{"name":"value","kind":"Any","default":null}]},{"type":"model","name":"FastWrapper1","properties":[{"name":"object","kind":"Any","default":null},{"name":"style","kind":"Any","default":null}]},{"type":"model","name":"NotificationAreaBase1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0}]},{"type":"model","name":"NotificationArea1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"notifications","kind":"Any","default":[]},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0},{"name":"types","kind":"Any","default":[{"type":"map","entries":[["type","warning"],["background","#ffc107"],["icon",{"type":"map","entries":[["className","fas fa-exclamation-triangle"],["tagName","i"],["color","white"]]}]]},{"type":"map","entries":[["type","info"],["background","#007bff"],["icon",{"type":"map","entries":[["className","fas fa-info-circle"],["tagName","i"],["color","white"]]}]]}]}]},{"type":"model","name":"Notification","properties":[{"name":"background","kind":"Any","default":null},{"name":"duration","kind":"Any","default":3000},{"name":"icon","kind":"Any","default":null},{"name":"message","kind":"Any","default":""},{"name":"notification_type","kind":"Any","default":null},{"name":"_destroyed","kind":"Any","default":false}]},{"type":"model","name":"TemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"BootstrapTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"MaterialTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]}]}};
  var render_items = [{"docid":"c4d768b9-cc45-4f15-b361-986c2a46aa8c","roots":{"p2696":"a9b07ef4-1563-4f6b-82f6-d1775f043b78"},"root_ids":["p2696"]}];
  var docs = Object.values(docs_json)
  if (!docs) {
    return
  }
  const py_version = docs[0].version.replace('rc', '-rc.').replace('.dev', '-dev.')
  function embed_document(root) {
    var Bokeh = get_bokeh(root)
    Bokeh.embed.embed_items_notebook(docs_json, render_items);
    for (const render_item of render_items) {
      for (const root_id of render_item.root_ids) {
	const id_el = document.getElementById(root_id)
	if (id_el.children.length && (id_el.children[0].className === 'bk-root')) {
	  const root_el = id_el.children[0]
	  root_el.id = root_el.id + '-rendered'
	}
      }
    }
  }
  function get_bokeh(root) {
    if (root.Bokeh === undefined) {
      return null
    } else if (root.Bokeh.version !== py_version) {
      if (root.Bokeh.versions === undefined || !root.Bokeh.versions.has(py_version)) {
	return null
      }
      return root.Bokeh.versions.get(py_version);
    } else if (root.Bokeh.version === py_version) {
      return root.Bokeh
    }
    return null
  }
  function is_loaded(root) {
    var Bokeh = get_bokeh(root)
    return (Bokeh != null && Bokeh.Panel !== undefined)
  }
  if (is_loaded(root)) {
    embed_document(root);
  } else {
    var attempts = 0;
    var timer = setInterval(function(root) {
      if (is_loaded(root)) {
        clearInterval(timer);
        embed_document(root);
      } else if (document.readyState == "complete") {
        attempts++;
        if (attempts > 200) {
          clearInterval(timer);
	  var Bokeh = get_bokeh(root)
	  if (Bokeh == null || Bokeh.Panel == null) {
            console.warn("Panel: ERROR: Unable to run Panel code because Bokeh or Panel library is missing");
	  } else {
	    console.warn("Panel: WARNING: Attempting to render but not all required libraries could be resolved.")
	    embed_document(root)
	  }
        }
      }
    }, 25, root)
  }
})(window);</script>




```python
df.hvplot.points('Longitude (deg)', 'Latitude (deg)', geo=True, color='red', tiles='ESRI', xlim=(0, 360), ylim=(-60, 60), hover_cols=["Epoch", "Sun Probe Earth angle (deg)"])
```






<div id='p2520'>
  <div id="b83cf433-199e-4405-83c3-69b1578a0d1d" data-root-id="p2520" style="display: contents;"></div>
</div>
<script type="application/javascript">(function(root) {
  var docs_json = {"24340461-f171-489f-80b9-24867c79915b":{"version":"3.3.3","title":"Bokeh Application","roots":[{"type":"object","name":"Row","id":"p2520","attributes":{"name":"Row03735","tags":["embedded"],"stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"type":"object","name":"ImportedStyleSheet","id":"p2523","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.6/dist/css/loading.css"}},{"type":"object","name":"ImportedStyleSheet","id":"p2608","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.6/dist/css/listpanel.css"}},{"type":"object","name":"ImportedStyleSheet","id":"p2521","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.6/dist/bundled/theme/default.css"}},{"type":"object","name":"ImportedStyleSheet","id":"p2522","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.6/dist/bundled/theme/native.css"}}],"margin":0,"sizing_mode":"stretch_width","align":"start","children":[{"type":"object","name":"Spacer","id":"p2524","attributes":{"name":"HSpacer03741","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"p2523"},{"id":"p2521"},{"id":"p2522"}],"margin":0,"sizing_mode":"stretch_width","align":"start"}},{"type":"object","name":"Figure","id":"p2553","attributes":{"width":null,"height":null,"margin":[5,10],"sizing_mode":"fixed","align":"start","x_range":{"type":"object","name":"Range1d","id":"p2534","attributes":{"tags":[[["Longitude","Longitude",null]],[]],"start":-19981848.59739268,"end":19981848.59739268,"reset_start":-19981848.59739268,"reset_end":19981848.59739268,"min_interval":5}},"y_range":{"type":"object","name":"Range1d","id":"p2535","attributes":{"tags":[[["Latitude","Latitude",null]],{"type":"map","entries":[["invert_yaxis",false],["autorange",false]]}],"start":-8399737.667179434,"end":8399737.667179434,"reset_start":-8399737.667179434,"reset_end":8399737.667179434,"min_interval":5}},"x_scale":{"type":"object","name":"LinearScale","id":"p2563"},"y_scale":{"type":"object","name":"LinearScale","id":"p2564"},"title":{"type":"object","name":"Title","id":"p2556","attributes":{"text_color":"black","text_font_size":"12pt"}},"renderers":[{"type":"object","name":"TileRenderer","id":"p2586","attributes":{"level":"underlay","tile_source":{"type":"object","name":"WMTSTileSource","id":"p2582","attributes":{"url":"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{Z}/{Y}/{X}.jpg","attribution":"&copy; <a href=\"http://downloads.esri.com/ArcGISOnline/docs/tou_summary.pdf\">Esri</a>, Earthstar Geographics"}}}},{"type":"object","name":"GlyphRenderer","id":"p2599","attributes":{"data_source":{"type":"object","name":"ColumnDataSource","id":"p2590","attributes":{"selected":{"type":"object","name":"Selection","id":"p2591","attributes":{"indices":[],"line_indices":[]}},"selection_policy":{"type":"object","name":"UnionRenderers","id":"p2592"},"data":{"type":"map","entries":[["Longitude (deg)",{"type":"ndarray","array":{"type":"bytes","data":"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"},"shape":[201],"dtype":"float64","order":"little"}],["Latitude (deg)",{"type":"ndarray","array":{"type":"bytes","data":"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"},"shape":[201],"dtype":"float64","order":"little"}],["Longitude_left_parenthesis_deg_right_parenthesis",{"type":"ndarray","array":{"type":"bytes","data":"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"},"shape":[201],"dtype":"float64","order":"little"}],["Latitude_left_parenthesis_deg_right_parenthesis",{"type":"ndarray","array":{"type":"bytes","data":"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"},"shape":[201],"dtype":"float64","order":"little"}],["Epoch",{"type":"ndarray","array":{"type":"bytes","data":"AACgS6yNa0IAAOxorI1rQgDgN4asjWtCAOCDo6yNa0IA4M/ArI1rQgDgG96sjWtCAOBn+6yNa0IA4LMYrY1rQgDg/zWtjWtCAOBLU62Na0IA4JdwrY1rQgDg442tjWtCAOAvq62Na0IA4HvIrY1rQgDgx+WtjWtCAOATA66Na0IA4F8gro1rQgDgqz2ujWtCAOD3Wq6Na0IA4EN4ro1rQgDgj5WujWtCAODbsq6Na0IA4CfQro1rQgDgc+2ujWtCAOC/Cq+Na0IA4Asor41rQgDgV0WvjWtCAOCjYq+Na0IA4O9/r41rQgDgO52vjWtCAOCHuq+Na0IA4NPXr41rQgDgH/WvjWtCAOBrErCNa0IA4LcvsI1rQgDgA02wjWtCAOBParCNa0IA4JuHsI1rQgDg56SwjWtCAOAzwrCNa0IA4H/fsI1rQgDgy/ywjWtCAOAXGrGNa0IA4GM3sY1rQgDgr1SxjWtCAOD7cbGNa0IA4EePsY1rQgDgk6yxjWtCAODfybGNa0IA4CvnsY1rQgDgdwSyjWtCAODDIbKNa0IA4A8/so1rQgDgW1yyjWtCAOCnebKNa0IA4POWso1rQgDgP7SyjWtCAOCL0bKNa0IA4Nfuso1rQgDgIwyzjWtCAOBvKbONa0IA4LtGs41rQgDgB2SzjWtCAOBTgbONa0IA4J+es41rQgDg67uzjWtCAOA32bONa0IA4IP2s41rQgDgzxO0jWtCAOAbMbSNa0IA4GdOtI1rQgDgs2u0jWtCAOD/iLSNa0IA4EumtI1rQgDgl8O0jWtCAODj4LSNa0IA4C/+tI1rQgDgexu1jWtCAODHOLWNa0IA4BNWtY1rQgDgX3O1jWtCAOCrkLWNa0IA4PettY1rQgDgQ8u1jWtCAOCP6LWNa0IA4NsFto1rQgDgJyO2jWtCAOBzQLaNa0IA4L9dto1rQgDgC3u2jWtCAOBXmLaNa0IA4KO1to1rQgDg79K2jWtCAOA78LaNa0IA4IcNt41rQgDg0yq3jWtCAOAfSLeNa0IA4Gtlt41rQgDgt4K3jWtCAOADoLeNa0IA4E+9t41rQgDgm9q3jWtCAODn97eNa0IA4DMVuI1rQgDgfzK4jWtCAODLT7iNa0IA4BdtuI1rQgDgY4q4jWtCAOCvp7iNa0IA4PvEuI1rQgDgR+K4jWtCAOCT/7iNa0IA4N8cuY1rQgDgKzq5jWtCAOB3V7mNa0IA4MN0uY1rQgDgD5K5jWtCAOBbr7mNa0IA4KfMuY1rQgDg8+m5jWtCAOA/B7qNa0IA4Iskuo1rQgDg10G6jWtCAOAjX7qNa0IA4G98uo1rQgDgu5m6jWtCAOAHt7qNa0IA4FPUuo1rQgDgn/G6jWtCAODrDruNa0IA4Dcsu41rQgDgg0m7jWtCAODPZruNa0IA4BuEu41rQgDgZ6G7jWtCAOCzvruNa0IA4P/bu41rQgDgS/m7jWtCAOCXFryNa0IA4OMzvI1rQgDgL1G8jWtCAOB7bryNa0IA4MeLvI1rQgDgE6m8jWtCAOBfxryNa0IA4KvjvI1rQgDg9wC9jWtCAOBDHr2Na0IA4I87vY1rQgDg21i9jWtCAOAndr2Na0IA4HOTvY1rQgDgv7C9jWtCAOALzr2Na0IA4FfrvY1rQgDgowi+jWtCAODvJb6Na0IA4DtDvo1rQgDgh2C+jWtCAODTfb6Na0IA4B+bvo1rQgDga7i+jWtCAOC31b6Na0IA4APzvo1rQgDgTxC/jWtCAOCbLb+Na0IA4OdKv41rQgDgM2i/jWtCAOB/hb+Na0IA4Muiv41rQgDgF8C/jWtCAOBj3b+Na0IA4K/6v41rQgDg+xfAjWtCAOBHNcCNa0IA4JNSwI1rQgDg32/AjWtCAOArjcCNa0IA4HeqwI1rQgDgw8fAjWtCAOAP5cCNa0IA4FsCwY1rQgDgpx/BjWtCAODzPMGNa0IA4D9awY1rQgDgi3fBjWtCAODXlMGNa0IA4COywY1rQgDgb8/BjWtCAOC77MGNa0IA4AcKwo1rQgDgUyfCjWtCAOCfRMKNa0IA4Othwo1rQgDgN3/CjWtCAOCDnMKNa0IA4M+5wo1rQgDgG9fCjWtCAOBn9MKNa0IA4LMRw41rQgDg/y7DjWtC"},"shape":[201],"dtype":"float64","order":"little"}],["Sun_Probe_Earth_angle_left_parenthesis_deg_right_parenthesis",{"type":"ndarray","array":{"type":"bytes","data":"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"},"shape":[201],"dtype":"float64","order":"little"}]]}}},"view":{"type":"object","name":"CDSView","id":"p2600","attributes":{"filter":{"type":"object","name":"AllIndices","id":"p2601"}}},"glyph":{"type":"object","name":"Scatter","id":"p2596","attributes":{"tags":["apply_ranges"],"x":{"type":"field","field":"Longitude (deg)"},"y":{"type":"field","field":"Latitude (deg)"},"size":{"type":"value","value":5.477225575051661},"line_color":{"type":"value","value":"red"},"fill_color":{"type":"value","value":"red"},"hatch_color":{"type":"value","value":"red"}}},"selection_glyph":{"type":"object","name":"Scatter","id":"p2604","attributes":{"tags":["apply_ranges"],"x":{"type":"field","field":"Longitude (deg)"},"y":{"type":"field","field":"Latitude (deg)"},"size":{"type":"value","value":5.477225575051661},"angle":{"type":"value","value":0.0},"line_color":{"type":"value","value":"red"},"line_alpha":{"type":"value","value":1.0},"line_width":{"type":"value","value":1},"line_join":{"type":"value","value":"bevel"},"line_cap":{"type":"value","value":"butt"},"line_dash":{"type":"value","value":[]},"line_dash_offset":{"type":"value","value":0},"fill_color":{"type":"value","value":"red"},"fill_alpha":{"type":"value","value":1.0},"hatch_color":{"type":"value","value":"red"},"hatch_alpha":{"type":"value","value":1.0},"hatch_scale":{"type":"value","value":12.0},"hatch_pattern":{"type":"value","value":null},"hatch_weight":{"type":"value","value":1.0},"marker":{"type":"value","value":"circle"}}},"nonselection_glyph":{"type":"object","name":"Scatter","id":"p2597","attributes":{"tags":["apply_ranges"],"x":{"type":"field","field":"Longitude (deg)"},"y":{"type":"field","field":"Latitude (deg)"},"size":{"type":"value","value":5.477225575051661},"line_color":{"type":"value","value":"red"},"line_alpha":{"type":"value","value":0.1},"fill_color":{"type":"value","value":"red"},"fill_alpha":{"type":"value","value":0.1},"hatch_color":{"type":"value","value":"red"},"hatch_alpha":{"type":"value","value":0.1}}},"muted_glyph":{"type":"object","name":"Scatter","id":"p2598","attributes":{"tags":["apply_ranges"],"x":{"type":"field","field":"Longitude (deg)"},"y":{"type":"field","field":"Latitude (deg)"},"size":{"type":"value","value":5.477225575051661},"line_color":{"type":"value","value":"red"},"line_alpha":{"type":"value","value":0.2},"fill_color":{"type":"value","value":"red"},"fill_alpha":{"type":"value","value":0.2},"hatch_color":{"type":"value","value":"red"},"hatch_alpha":{"type":"value","value":0.2}}}}}],"toolbar":{"type":"object","name":"Toolbar","id":"p2562","attributes":{"tools":[{"type":"object","name":"WheelZoomTool","id":"p2538","attributes":{"renderers":"auto","zoom_on_axis":false}},{"type":"object","name":"BoxZoomTool","id":"p2539","attributes":{"overlay":{"type":"object","name":"BoxAnnotation","id":"p1083","attributes":{"syncable":false,"level":"overlay","visible":false,"left":{"type":"number","value":"nan"},"right":{"type":"number","value":"nan"},"top":{"type":"number","value":"nan"},"bottom":{"type":"number","value":"nan"},"left_units":"canvas","right_units":"canvas","top_units":"canvas","bottom_units":"canvas","line_color":"black","line_alpha":1.0,"line_width":2,"line_dash":[4,4],"fill_color":"lightgrey","fill_alpha":0.5}},"match_aspect":true}},{"type":"object","name":"HoverTool","id":"p2552","attributes":{"tags":["hv_created"],"renderers":[{"id":"p2599"}],"tooltips":[["Longitude (deg)","$x{custom}"],["Latitude (deg)","$y{custom}"],["Epoch","@{Epoch}{%F %T}"],["Sun Probe Earth angle (deg)","@{Sun_Probe_Earth_angle_left_parenthesis_deg_right_parenthesis}"]],"formatters":{"type":"map","entries":[["@{Epoch}","datetime"],["$x",{"type":"object","name":"CustomJSHover","id":"p2602","attributes":{"code":"\n        const projections = Bokeh.require(\"core/util/projections\");\n        const {snap_x, snap_y} = special_vars\n        const coords = projections.wgs84_mercator.invert(snap_x, snap_y)\n        return \"\" + (coords[0]).toFixed(4)\n    "}}],["$y",{"type":"object","name":"CustomJSHover","id":"p2603","attributes":{"code":"\n        const projections = Bokeh.require(\"core/util/projections\");\n        const {snap_x, snap_y} = special_vars\n        const coords = projections.wgs84_mercator.invert(snap_x, snap_y)\n        return \"\" + (coords[1]).toFixed(4)\n    "}}]]}}},{"type":"object","name":"PanTool","id":"p2576"},{"type":"object","name":"ResetTool","id":"p2577"}],"active_drag":{"id":"p2576"}}},"left":[{"type":"object","name":"LinearAxis","id":"p2570","attributes":{"ticker":{"type":"object","name":"MercatorTicker","id":"p2580","attributes":{"mantissas":[1,2,5],"dimension":"lat"}},"formatter":{"type":"object","name":"MercatorTickFormatter","id":"p2581","attributes":{"dimension":"lat"}},"axis_label":"Latitude","major_label_policy":{"type":"object","name":"AllLabels","id":"p2573"}}}],"below":[{"type":"object","name":"LinearAxis","id":"p2565","attributes":{"ticker":{"type":"object","name":"MercatorTicker","id":"p2578","attributes":{"mantissas":[1,2,5],"dimension":"lon"}},"formatter":{"type":"object","name":"MercatorTickFormatter","id":"p2579","attributes":{"dimension":"lon"}},"axis_label":"Longitude","major_label_policy":{"type":"object","name":"AllLabels","id":"p2568"}}}],"center":[{"type":"object","name":"Grid","id":"p2569","attributes":{"axis":{"id":"p2565"},"grid_line_color":null}},{"type":"object","name":"Grid","id":"p2574","attributes":{"dimension":1,"axis":{"id":"p2570"},"grid_line_color":null}}],"frame_width":713,"frame_height":300,"min_border_top":10,"min_border_bottom":10,"min_border_left":10,"min_border_right":10,"output_backend":"webgl","match_aspect":true}},{"type":"object","name":"Spacer","id":"p2606","attributes":{"name":"HSpacer03742","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"p2523"},{"id":"p2521"},{"id":"p2522"}],"margin":0,"sizing_mode":"stretch_width","align":"start"}}]}}],"defs":[{"type":"model","name":"ReactiveHTML1"},{"type":"model","name":"FlexBox1","properties":[{"name":"align_content","kind":"Any","default":"flex-start"},{"name":"align_items","kind":"Any","default":"flex-start"},{"name":"flex_direction","kind":"Any","default":"row"},{"name":"flex_wrap","kind":"Any","default":"wrap"},{"name":"justify_content","kind":"Any","default":"flex-start"}]},{"type":"model","name":"FloatPanel1","properties":[{"name":"config","kind":"Any","default":{"type":"map"}},{"name":"contained","kind":"Any","default":true},{"name":"position","kind":"Any","default":"right-top"},{"name":"offsetx","kind":"Any","default":null},{"name":"offsety","kind":"Any","default":null},{"name":"theme","kind":"Any","default":"primary"},{"name":"status","kind":"Any","default":"normalized"}]},{"type":"model","name":"GridStack1","properties":[{"name":"mode","kind":"Any","default":"warn"},{"name":"ncols","kind":"Any","default":null},{"name":"nrows","kind":"Any","default":null},{"name":"allow_resize","kind":"Any","default":true},{"name":"allow_drag","kind":"Any","default":true},{"name":"state","kind":"Any","default":[]}]},{"type":"model","name":"drag1","properties":[{"name":"slider_width","kind":"Any","default":5},{"name":"slider_color","kind":"Any","default":"black"},{"name":"value","kind":"Any","default":50}]},{"type":"model","name":"click1","properties":[{"name":"terminal_output","kind":"Any","default":""},{"name":"debug_name","kind":"Any","default":""},{"name":"clears","kind":"Any","default":0}]},{"type":"model","name":"copy_to_clipboard1","properties":[{"name":"fill","kind":"Any","default":"none"},{"name":"value","kind":"Any","default":null}]},{"type":"model","name":"FastWrapper1","properties":[{"name":"object","kind":"Any","default":null},{"name":"style","kind":"Any","default":null}]},{"type":"model","name":"NotificationAreaBase1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0}]},{"type":"model","name":"NotificationArea1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"notifications","kind":"Any","default":[]},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0},{"name":"types","kind":"Any","default":[{"type":"map","entries":[["type","warning"],["background","#ffc107"],["icon",{"type":"map","entries":[["className","fas fa-exclamation-triangle"],["tagName","i"],["color","white"]]}]]},{"type":"map","entries":[["type","info"],["background","#007bff"],["icon",{"type":"map","entries":[["className","fas fa-info-circle"],["tagName","i"],["color","white"]]}]]}]}]},{"type":"model","name":"Notification","properties":[{"name":"background","kind":"Any","default":null},{"name":"duration","kind":"Any","default":3000},{"name":"icon","kind":"Any","default":null},{"name":"message","kind":"Any","default":""},{"name":"notification_type","kind":"Any","default":null},{"name":"_destroyed","kind":"Any","default":false}]},{"type":"model","name":"TemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"BootstrapTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"MaterialTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]}]}};
  var render_items = [{"docid":"24340461-f171-489f-80b9-24867c79915b","roots":{"p2520":"b83cf433-199e-4405-83c3-69b1578a0d1d"},"root_ids":["p2520"]}];
  var docs = Object.values(docs_json)
  if (!docs) {
    return
  }
  const py_version = docs[0].version.replace('rc', '-rc.').replace('.dev', '-dev.')
  function embed_document(root) {
    var Bokeh = get_bokeh(root)
    Bokeh.embed.embed_items_notebook(docs_json, render_items);
    for (const render_item of render_items) {
      for (const root_id of render_item.root_ids) {
	const id_el = document.getElementById(root_id)
	if (id_el.children.length && (id_el.children[0].className === 'bk-root')) {
	  const root_el = id_el.children[0]
	  root_el.id = root_el.id + '-rendered'
	}
      }
    }
  }
  function get_bokeh(root) {
    if (root.Bokeh === undefined) {
      return null
    } else if (root.Bokeh.version !== py_version) {
      if (root.Bokeh.versions === undefined || !root.Bokeh.versions.has(py_version)) {
	return null
      }
      return root.Bokeh.versions.get(py_version);
    } else if (root.Bokeh.version === py_version) {
      return root.Bokeh
    }
    return null
  }
  function is_loaded(root) {
    var Bokeh = get_bokeh(root)
    return (Bokeh != null && Bokeh.Panel !== undefined)
  }
  if (is_loaded(root)) {
    embed_document(root);
  } else {
    var attempts = 0;
    var timer = setInterval(function(root) {
      if (is_loaded(root)) {
        clearInterval(timer);
        embed_document(root);
      } else if (document.readyState == "complete") {
        attempts++;
        if (attempts > 200) {
          clearInterval(timer);
	  var Bokeh = get_bokeh(root)
	  if (Bokeh == null || Bokeh.Panel == null) {
            console.warn("Panel: ERROR: Unable to run Panel code because Bokeh or Panel library is missing");
	  } else {
	    console.warn("Panel: WARNING: Attempting to render but not all required libraries could be resolved.")
	    embed_document(root)
	  }
        }
      }
    }, 25, root)
  }
})(window);</script>



## Exercise

The goal of this exercise is to show that the SPE is essentially the Sun elevation angle from the position exactly nadir of the vehicle plus 90 degrees (or so, since the Earth isn't a perfect sphere). It also shows you how to combine the different functionality you've seen with the other tutorials to solve similar problem.

_Note:_ this is the `verify_geometry` Rust test, but rebuilt in Python.

1. For the whole spacecraft trajectory, build the locality exactly nadir of it at each epoch (remember that a `TimeSeries` instance can only be used once, so you'll need to rebuild a new one). For this step, initialize a new `Orbit` instance from the latitude and longitude constructor using the position of the spacecraft in the IAU Earth frame as we did above.
2. At each epoch, grab the state of the Sun as seen from the Earth (both can be in the J2000 frame since the AER computation will transform the states into the correct frames anyway).
3. Call the azimuth, elevtion, and range function of your loaded Almanac, and store the elevation of the Sun as seen from the point exactly nadir of the spacecraft.
4. Plot the elevation data in degrees compared to the SPE angle calculated above.
