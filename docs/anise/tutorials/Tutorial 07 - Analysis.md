# Tutorial 07 - Analysis Module

This tutorial covers the new analysis module introduced in ANISE version 0.8.0. We will explore:
1.  **Report Building:** Creating complex scalar reports, generating data, and visualizing it with Polars and Plotly.
2.  **Event Finding:** Finding discrete events like apoapsis, periapsis, and eclipse entry/exit.
3.  **Event Arc Finding:** Detecting continuous events (arcs) like eclipses and sunset periods.
4.  **Ground Contact Finders:** Using `LocationDhallSet` to define ground stations and finding visibility/communication arcs.


```python
import polars as pl
import plotly.express as px
from anise import (
    Almanac,
    Aberration,
    LocationDhallSet,
    LocationDhallSetEntry,
    LocationDataSet,
)
from anise.astro import Location, TerrainMask, FrameUid, Frame
from anise.analysis import Event, Condition
import anise.analysis as analysis
from anise.time import Duration, Epoch, TimeSeries, Unit
from anise.constants import Frames, Orientations

# Load the Almanac with necessary kernels
almanac = (
    Almanac("../../data/de440s.bsp")
    .load("../../data/pck08.pca")
    .load("../../data/lro.bsp")
)
almanac.describe(spk=True)
```

    === SPK #0: `../../data/lro.bsp` ===
    ┌───────────────┬────────────────┬────────────┬───────────────────────────────────┬───────────────────────────────────┬──────────┬──────────────────────┐
    │ Name          │ Target         │ Center     │ Start epoch                       │ End epoch                         │ Duration │ Interpolation kind   │
    ├───────────────┼────────────────┼────────────┼───────────────────────────────────┼───────────────────────────────────┼──────────┼──────────────────────┤
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2023-12-15T00:01:09.183418531 TDB │ 2023-12-16T00:01:09.183445764 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2023-12-16T00:01:09.183445766 TDB │ 2023-12-17T00:01:09.183473001 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2023-12-17T00:01:09.183473003 TDB │ 2023-12-18T00:01:09.183500753 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2023-12-18T00:01:09.183500755 TDB │ 2023-12-19T00:01:09.183528378 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2023-12-19T00:01:09.183528380 TDB │ 2023-12-20T00:01:09.183556262 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2023-12-20T00:01:09.183556264 TDB │ 2023-12-21T00:01:09.183584149 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2023-12-21T00:01:09.183584151 TDB │ 2023-12-22T00:01:09.183612293 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2023-12-22T00:01:09.183612295 TDB │ 2023-12-23T00:01:09.183640567 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2023-12-23T00:01:09.183640569 TDB │ 2023-12-24T00:01:09.183668972 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2023-12-24T00:01:09.183668974 TDB │ 2023-12-25T00:01:09.183697379 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2023-12-25T00:01:09.183697381 TDB │ 2023-12-26T00:01:09.183725917 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2023-12-26T00:01:09.183725919 TDB │ 2023-12-27T00:01:09.183754585 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2023-12-27T00:01:09.183754587 TDB │ 2023-12-28T00:01:09.183783255 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2023-12-28T00:01:09.183783257 TDB │ 2023-12-29T00:01:09.183812055 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2023-12-29T00:01:09.183812057 TDB │ 2023-12-30T00:01:09.183840858 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2023-12-30T00:01:09.183840860 TDB │ 2023-12-31T00:01:09.183869791 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2023-12-31T00:01:09.183869793 TDB │ 2024-01-01T00:01:09.183898599 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-01T00:01:09.183898601 TDB │ 2024-01-02T00:01:09.183927664 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-02T00:01:09.183927666 TDB │ 2024-01-03T00:01:09.183956604 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-03T00:01:09.183956606 TDB │ 2024-01-04T00:01:09.183985547 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-04T00:01:09.183985549 TDB │ 2024-01-05T00:01:09.184014491 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-05T00:01:09.184014493 TDB │ 2024-01-06T00:01:09.184043565 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-06T00:01:09.184043567 TDB │ 2024-01-07T00:01:09.184072515 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-07T00:01:09.184072517 TDB │ 2024-01-08T00:01:09.184101466 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-08T00:01:09.184101468 TDB │ 2024-01-09T00:01:09.184130420 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-09T00:01:09.184130422 TDB │ 2024-01-10T00:01:09.184159376 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-10T00:01:09.184159378 TDB │ 2024-01-11T00:01:09.184188206 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-11T00:01:09.184188208 TDB │ 2024-01-12T00:01:09.184216912 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-12T00:01:09.184216914 TDB │ 2024-01-13T00:01:09.184245618 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-13T00:01:09.184245620 TDB │ 2024-01-14T00:01:09.184274327 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-14T00:01:09.184274329 TDB │ 2024-01-15T00:01:09.184302911 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-15T00:01:09.184302913 TDB │ 2024-01-16T00:01:09.184331240 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-16T00:01:09.184331242 TDB │ 2024-01-17T00:01:09.184359700 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-17T00:01:09.184359702 TDB │ 2024-01-18T00:01:09.184387905 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-18T00:01:09.184387907 TDB │ 2024-01-19T00:01:09.184415986 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-19T00:01:09.184415988 TDB │ 2024-01-20T00:01:09.184443940 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-20T00:01:09.184443942 TDB │ 2024-01-21T00:01:09.184471769 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-21T00:01:09.184471771 TDB │ 2024-01-22T00:01:09.184499470 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-22T00:01:09.184499472 TDB │ 2024-01-23T00:01:09.184527175 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-23T00:01:09.184527177 TDB │ 2024-01-24T00:01:09.184554497 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-24T00:01:09.184554499 TDB │ 2024-01-25T00:01:09.184581694 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-25T00:01:09.184581696 TDB │ 2024-01-26T00:01:09.184608766 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-26T00:01:09.184608768 TDB │ 2024-01-27T00:01:09.184635583 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-27T00:01:09.184635585 TDB │ 2024-01-28T00:01:09.184662273 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-28T00:01:09.184662275 TDB │ 2024-01-29T00:01:09.184688710 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-29T00:01:09.184688712 TDB │ 2024-01-30T00:01:09.184714892 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 ��� 2024-01-30T00:01:09.184714894 TDB │ 2024-01-31T00:01:09.184740949 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-01-31T00:01:09.184740951 TDB │ 2024-02-01T00:01:09.184766751 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-01T00:01:09.184766753 TDB │ 2024-02-02T00:01:09.184792172 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-02T00:01:09.184792174 TDB │ 2024-02-03T00:01:09.184817595 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-03T00:01:09.184817597 TDB │ 2024-02-04T00:01:09.184842507 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-04T00:01:09.184842509 TDB │ 2024-02-05T00:01:09.184867292 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-05T00:01:09.184867294 TDB │ 2024-02-06T00:01:09.184891825 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-06T00:01:09.184891827 TDB │ 2024-02-07T00:01:09.184916102 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-07T00:01:09.184916104 TDB │ 2024-02-08T00:01:09.184939997 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-08T00:01:09.184939999 TDB │ 2024-02-09T00:01:09.184963766 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-09T00:01:09.184963768 TDB │ 2024-02-10T00:01:09.184987025 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-10T00:01:09.184987027 TDB │ 2024-02-11T00:01:09.185010157 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-11T00:01:09.185010159 TDB │ 2024-02-12T00:01:09.185032906 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-12T00:01:09.185032908 TDB │ 2024-02-13T00:01:09.185055402 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-13T00:01:09.185055404 TDB │ 2024-02-14T00:01:09.185077515 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-14T00:01:09.185077517 TDB │ 2024-02-15T00:01:09.185099245 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-15T00:01:09.185099247 TDB │ 2024-02-16T00:01:09.185120850 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-16T00:01:09.185120852 TDB │ 2024-02-17T00:01:09.185141943 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-17T00:01:09.185141945 TDB │ 2024-02-18T00:01:09.185162653 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-18T00:01:09.185162655 TDB │ 2024-02-19T00:01:09.185182982 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-19T00:01:09.185182984 TDB │ 2024-02-20T00:01:09.185203056 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-20T00:01:09.185203058 TDB │ 2024-02-21T00:01:09.185222746 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-21T00:01:09.185222748 TDB │ 2024-02-22T00:01:09.185241926 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-22T00:01:09.185241928 TDB │ 2024-02-23T00:01:09.185260851 TDB │ 1 day    �� Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-23T00:01:09.185260853 TDB │ 2024-02-24T00:01:09.185279522 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-24T00:01:09.185279524 TDB │ 2024-02-25T00:01:09.185297554 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-25T00:01:09.185297556 TDB │ 2024-02-26T00:01:09.185315331 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-26T00:01:09.185315333 TDB │ 2024-02-27T00:01:09.185332596 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-27T00:01:09.185332598 TDB │ 2024-02-28T00:01:09.185349607 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-28T00:01:09.185349609 TDB │ 2024-02-29T00:01:09.185366107 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-02-29T00:01:09.185366109 TDB │ 2024-03-01T00:01:09.185382224 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-03-01T00:01:09.185382226 TDB │ 2024-03-02T00:01:09.185397958 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-03-02T00:01:09.185397960 TDB │ 2024-03-03T00:01:09.185413181 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-03-03T00:01:09.185413183 TDB │ 2024-03-04T00:01:09.185428021 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-03-04T00:01:09.185428023 TDB │ 2024-03-05T00:01:09.185442478 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-03-05T00:01:09.185442480 TDB │ 2024-03-06T00:01:09.185456422 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-03-06T00:01:09.185456424 TDB │ 2024-03-07T00:01:09.185469985 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-03-07T00:01:09.185469987 TDB │ 2024-03-08T00:01:09.185482908 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-03-08T00:01:09.185482910 TDB │ 2024-03-09T00:01:09.185495575 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-03-09T00:01:09.185495577 TDB │ 2024-03-10T00:01:09.185507731 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-03-10T00:01:09.185507733 TDB │ 2024-03-11T00:01:09.185519632 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-03-11T00:01:09.185519634 TDB │ 2024-03-12T00:01:09.185530765 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-03-12T00:01:09.185530767 TDB │ 2024-03-13T00:01:09.185541515 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-03-13T00:01:09.185541517 TDB │ 2024-03-14T00:01:09.185551881 TDB │ 1 day    │ Hermite Unequal Step │
    │ SPK_STATES_13 │ body -85 J2000 │ Moon J2000 │ 2024-03-14T00:01:09.185551883 TDB │ 2024-03-15T00:01:09.185561735 TDB │ 1 day    │ Hermite Unequal Step │
    └───────────────┴────────────────┴────────────┴───────────────────────────────────┴───────────────────────────────────┴──────────┴────���─────────────────┘
    === SPK #1: `../../data/de440s.bsp` ===
    ┌────────────────┬─────────────────────────────┬───────────────────────────────┬───────────────────────────────────┬───────────────────────────────────┬─────────────┬────────────────────┐
    │ Name           │ Target                      │ Center                        │ Start epoch                       │ End epoch                         │ Duration    │ Interpolation kind │
    ├────────────────┼───────────────────────────��─┼───────────────────────────────┼───────────────────────────────────┼───────────────────────────────────┼─────────────┼────────────────────┤
    │ DE-0440LE-0440 │ Mercury Barycenter J2000    │ Solar System Barycenter J2000 │ 1849-12-26T00:00:00.000046619 TDB │ 2150-01-21T23:59:59.999955184 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Venus Barycenter J2000      │ Solar System Barycenter J2000 │ 1849-12-26T00:00:00.000046619 TDB │ 2150-01-21T23:59:59.999955184 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Earth-Moon Barycenter J2000 │ Solar System Barycenter J2000 │ 1849-12-26T00:00:00.000046619 TDB │ 2150-01-21T23:59:59.999955184 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Mars Barycenter J2000       │ Solar System Barycenter J2000 │ 1849-12-26T00:00:00.000046619 TDB │ 2150-01-21T23:59:59.999955184 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Jupiter Barycenter J2000    │ Solar System Barycenter J2000 │ 1849-12-26T00:00:00.000046619 TDB │ 2150-01-21T23:59:59.999955184 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Saturn Barycenter J2000     │ Solar System Barycenter J2000 │ 1849-12-26T00:00:00.000046619 TDB │ 2150-01-21T23:59:59.999955184 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Uranus Barycenter J2000     │ Solar System Barycenter J2000 │ 1849-12-26T00:00:00.000046619 TDB │ 2150-01-21T23:59:59.999955184 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Neptune Barycenter J2000    │ Solar System Barycenter J2000 │ 1849-12-26T00:00:00.000046619 TDB │ 2150-01-21T23:59:59.999955184 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Pluto Barycenter J2000      │ Solar System Barycenter J2000 │ 1849-12-26T00:00:00.000046619 TDB │ 2150-01-21T23:59:59.999955184 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Sun J2000                   │ Solar System Barycenter J2000 │ 1849-12-26T00:00:00.000046619 TDB │ 2150-01-21T23:59:59.999955184 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Moon J2000                  │ Earth-Moon Barycenter J2000   │ 1849-12-26T00:00:00.000046619 TDB │ 2150-01-21T23:59:59.999955184 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Earth J2000                 │ Earth-Moon Barycenter J2000   │ 1849-12-26T00:00:00.000046619 TDB │ 2150-01-21T23:59:59.999955184 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Mercury J2000               │ Mercury Barycenter J2000      │ 1849-12-26T00:00:00.000046619 TDB │ 2150-01-21T23:59:59.999955184 TDB │ 109600 days │ Chebyshev Triplet  │
    │ DE-0440LE-0440 │ Venus J2000                 │ Venus Barycenter J2000        │ 1849-12-26T00:00:00.000046619 TDB │ 2150-01-21T23:59:59.999955184 TDB │ 109600 days │ Chebyshev Triplet  │
    └────────────────┴─────────────────────────────┴───────────────────────────────┴───────────────────────────────────┴───────────────────────────────────┴─────────────┴────────────────────┘


## 1. Report Building

We can define complex scalar expressions and generate reports over a time series. This is useful for analyzing orbital elements, geometric conditions, and custom calculations.


```python
target_frame = analysis.FrameSpec.Loaded(Frame(-85, Orientations.J2000))
observer_frame = analysis.FrameSpec.Loaded(Frames.MOON_J2000)

state = analysis.StateSpec(
    target_frame=target_frame,
    observer_frame=observer_frame,
    ab_corr=None,
)

# Define a VNC (Velocity-Normal-Co-normal) Frame
vnc = analysis.OrthogonalFrame.XY(
    x=analysis.VectorExpr.Unit(analysis.VectorExpr.Velocity(state)),
    y=analysis.VectorExpr.Unit(analysis.VectorExpr.OrbitalMomentum(state)),
)

sun_state = analysis.StateSpec(
    target_frame=target_frame,
    observer_frame=analysis.FrameSpec.Loaded(Frames.SUN_J2000),
    ab_corr=Aberration("LT"),
)

# Project the Earth->Sun vector onto the VNC frame
proj = analysis.VectorExpr.Project(
    v=analysis.VectorExpr.Negate(
        analysis.VectorExpr.Unit(analysis.VectorExpr.Radius(sun_state))
    ),
    frame=vnc,
    plane=analysis.Plane.XY,
)

# Custom Local Solar Time (LST) Calculation using fundamental expressions
earth_sun = analysis.StateSpec(
    target_frame=analysis.FrameSpec.Loaded(Frames.SUN_J2000),
    observer_frame=observer_frame,
    ab_corr=Aberration("LT"),
)
u = analysis.VectorExpr.Unit(
    analysis.VectorExpr.CrossProduct(
        a=analysis.VectorExpr.Unit(analysis.VectorExpr.Radius(earth_sun)),
        b=analysis.VectorExpr.Unit(analysis.VectorExpr.OrbitalMomentum(state)),
    )
)
v = analysis.VectorExpr.CrossProduct(
    a=analysis.VectorExpr.Unit(analysis.VectorExpr.OrbitalMomentum(state)), b=u
)
r = analysis.VectorExpr.Radius(state)
sin_theta = analysis.ScalarExpr.DotProduct(a=v, b=r)
cos_theta = analysis.ScalarExpr.DotProduct(a=u, b=r)
theta = analysis.ScalarExpr.Atan2(y=sin_theta, x=cos_theta)
lst_prod = analysis.ScalarExpr.Mul(
    a=analysis.ScalarExpr.Mul(a=theta, b=analysis.ScalarExpr.Constant(1.0 / 180.0)),
    b=analysis.ScalarExpr.Constant(12.0),
)
lst_add = analysis.ScalarExpr.Add(a=lst_prod, b=analysis.ScalarExpr.Constant(6.0))
lst = analysis.ScalarExpr.Modulo(v=lst_add, m=analysis.ScalarExpr.Constant(24.0))

# Define scalars to report
scalars = [
    analysis.ScalarExpr.Element(analysis.OrbitalElement.SemiMajorAxis),
    analysis.ScalarExpr.Element(analysis.OrbitalElement.Eccentricity),
    analysis.ScalarExpr.SolarEclipsePercentage(eclipsing_frame=Frames.VENUS_J2000),
    analysis.ScalarExpr.VectorX(proj),
    analysis.ScalarExpr.VectorY(proj),
    analysis.ScalarExpr.VectorZ(proj),
    analysis.ScalarExpr.LocalSolarTime(),
    lst,
]

# Set aliases for readable columns
scalars_with_aliases = [(s, None) for s in scalars]
scalars_with_aliases[3] = (scalars_with_aliases[3][0], "proj VNC X")
scalars_with_aliases[4] = (scalars_with_aliases[4][0], "proj VNC Y")
scalars_with_aliases[5] = (scalars_with_aliases[5][0], "proj VNC Z")
scalars_with_aliases[7] = (scalars_with_aliases[7][0], "Custom LST (h)")

report = analysis.ReportScalars(scalars_with_aliases, state)
```

Now we generate the data over a time series and convert it to a Polars DataFrame.


```python
lro_start, lro_stop = almanac.spk_domain(-85)
print(f"LRO valid from {lro_start} to {lro_stop}")
series = TimeSeries(
    lro_stop - Unit.Day * 1.5,
    lro_stop,
    Unit.Minute * 10, # Higher resolution for plotting
    inclusive=True,
)

data = almanac.report_scalars(report, series)

# Convert to Polars DataFrame
rows = []
for epoch_str, val_dict in data.items():
    row = {"Epoch": epoch_str}
    row.update(val_dict)
    rows.append(row)

df = pl.DataFrame(rows)
# Convert Epoch string to datetime for better plotting
df = df.with_columns(pl.col("Epoch").str.to_datetime()).sort("Epoch")
print(df.head())
```

    LRO valid from 2023-12-15T00:01:09.183425793 ET to 2024-03-15T00:01:09.185563263 ET
    shape: (5, 9)
    ┌───────────┬───────────┬───────────┬───────────┬───┬───────────┬───────────┬───────────┬──────────┐
    │ Epoch     ┆ proj VNC  ┆ local     ┆ solar     ┆ … ┆ Custom    ┆ proj VNC  ┆ SemiMajor ┆ proj VNC │
    │ ---       ┆ X         ┆ solar     ┆ eclipse   ┆   ┆ LST (h)   ┆ Y         ┆ Axis (km) ┆ Z        │
    │ datetime[ ┆ ---       ┆ time (h)  ┆ due to    ┆   ┆ ---       ┆ ---       ┆ ---       ┆ ---      │
    │ μs]       ┆ f64       ┆ ---       ┆ Venus     ┆   ┆ f64       ┆ f64       ┆ f64       ┆ f64      │
    │           ┆           ┆ f64       ┆ Bar…      ┆   ┆           ┆           ┆           ┆          │
    │           ┆           ┆           ┆ ---       ┆   ┆           ┆           ┆           ┆          │
    │           ┆           ┆           ┆ f64       ┆   ┆           ┆           ┆           ┆          │
    ╞═══════════╪═══════════╪═══════════╪═══════════╪═══╪═══════════╪═══════════╪═══════════╪══════════╡
    │ 2024-03-1 ┆ -0.382568 ┆ 21.345665 ┆ 0.0       ┆ … ┆ 21.345665 ┆ 0.753565  ┆ 1827.7867 ┆ -0.53235 │
    │ 3 12:01:0 ┆           ┆           ┆           ┆   ┆           ┆           ┆ 98        ┆ 5        │
    │ 9.185563  ┆           ┆           ┆           ┆   ┆           ┆           ┆           ┆          │
    │ 2024-03-1 ┆ -0.055965 ┆ 23.400991 ┆ 0.0       ┆ … ┆ 23.400991 ┆ 0.75363   ┆ 1828.0145 ┆ -0.65309 │
    │ 3 12:11:0 ┆           ┆           ┆           ┆   ┆           ┆           ┆ 17        ┆ 6        │
    │ 9.185563  ┆           ┆           ┆           ┆   ┆           ┆           ┆           ┆          │
    │ 2024-03-1 ┆ 0.287843  ┆ 1.474358  ┆ 0.0       ┆ … ┆ 1.474358  ┆ 0.753692  ┆ 1827.7419 ┆ -0.58883 │
    │ 3 12:21:0 ┆           ┆           ┆           ┆   ┆           ┆           ┆ 3         ┆ 2        │
    │ 9.185563  ┆           ┆           ┆           ┆   ┆           ┆           ┆           ┆          │
    │ 2024-03-1 ┆ 0.550096  ┆ 3.559474  ┆ 0.0       ┆ … ┆ 3.559474  ┆ 0.753795  ┆ 1827.3555 ┆ -0.35611 │
    │ 3 12:31:0 ┆           ┆           ┆           ┆   ┆           ┆           ┆ 14        ┆ 7        │
    │ 9.185563  ┆           ┆           ┆           ┆   ┆           ┆           ┆           ┆          │
    │ 2024-03-1 ┆ 0.654768  ┆ 5.647546  ┆ 0.0       ┆ … ┆ 5.647546  ┆ 0.753964  ┆ 1827.3668 ┆ -0.02131 │
    │ 3 12:41:0 ┆           ┆           ┆           ┆   ┆           ┆           ┆ 86        ┆          │
    │ 9.185563  ┆           ┆           ┆           ┆   ┆           ┆           ┆           ┆          │
    └───────────┴───────────┴───────────┴───────────┴───┴───────────┴───────────┴───────────┴──────────┘


Let's visualize the Custom LST vs Time.


```python
fig = px.line(df, x="Epoch", y="Custom LST (h)", title="Custom Local Solar Time over Time")
fig.show()
```



![png](Tutorial%2007%20-%20Analysis_files/Tutorial%2007%20-%20Analysis_7_0.png)



## 2. Event Finding

We can search for discrete events such as apoapsis, periapsis, or specific geometric conditions.


```python
lro_frame = Frame(-85, 1)  # LRO NAIF ID
lro_state_spec = analysis.StateSpec(
    target_frame=analysis.FrameSpec.Loaded(lro_frame),
    observer_frame=analysis.FrameSpec.Loaded(Frames.MOON_J2000),
    ab_corr=None,
)

apolune = Event.apoapsis()
perilune = Event.periapsis()

start_epoch, end_epoch = almanac.spk_domain(-85)
# Search over a shorter window
search_end = start_epoch + Unit.Day * 2

print(f"Searching events from {start_epoch} to {search_end}")

apo_events = almanac.report_events(lro_state_spec, apolune, start_epoch, search_end)
print(f"Found {len(apo_events)} apoapsis events.")

peri_events = almanac.report_events(lro_state_spec, perilune, start_epoch, search_end)
print(f"Found {len(peri_events)} periapsis events.")

# Print first few events
for i, event in enumerate(apo_events[:3]):
    print(f"Apoapsis {i+1}: {event.orbit.epoch}")
```

    Searching events from 2023-12-15T00:01:09.183425793 ET to 2023-12-17T00:01:09.183425793 ET
    Found 25 apoapsis events.
    Found 24 periapsis events.
    Apoapsis 1: 2023-12-15T00:07:04.599486254 ET
    Apoapsis 2: 2023-12-15T02:05:09.311922236 ET
    Apoapsis 3: 2023-12-15T04:03:14.118872647 ET


## 3. Event Arc Finding

Event arcs represent continuous periods where a condition is met, such as being in eclipse or having the sun set.


```python
sun_has_set = analysis.Event(
    analysis.ScalarExpr.SunAngle(observer_id=-85),
    Condition.LessThan(90.0),
    Unit.Second * 0.5,
    ab_corr=None,
)
eclipse = Event.total_eclipse(Frames.MOON_J2000)

sunset_arcs = almanac.report_event_arcs(lro_state_spec, sun_has_set, start_epoch, search_end)
print(f"Found {len(sunset_arcs)} sunset arcs.")

eclipse_arcs = almanac.report_event_arcs(lro_state_spec, eclipse, start_epoch, search_end)
print(f"Found {len(eclipse_arcs)} eclipse arcs.")

if eclipse_arcs:
    print(f"First eclipse duration: {eclipse_arcs[0].duration()}")
```

    Found 11 sunset arcs.
    Found 25 eclipse arcs.
    First eclipse duration: 39 min 12 s 806 ms 171 μs 252 ns


## 4. Ground Contact Finders

We can simulate ground station visibility by defining locations and masks.


```python
# Define a ground station (DSS65)
mask = [TerrainMask(0.0, 5.0), TerrainMask(35.0, 10.0), TerrainMask(270.0, 3.0)]
dss65 = Location(
    40.427_222,
    4.250_556,
    0.834_939,
    FrameUid(399, 399),
    mask,
    terrain_mask_ignored=True,
)

# Create and save an LKA (Location Kernel Anise) file
entry = LocationDhallSetEntry(dss65, id=1, alias="DSS65")
dhallset = LocationDhallSet([entry])
dataset = dhallset.to_dataset()
lka_path = "tutorial_loc_kernel.lka"
dataset.save_as(lka_path, True)

# Load the LKA into the Almanac
almanac = almanac.load(lka_path)

# Find visibility arcs
horizon = Event.visible_from_location_id(1)

comm_arcs = almanac.report_event_arcs(
    lro_state_spec, horizon, start_epoch, start_epoch + Unit.Day * 1
)
print(f"Found {len(comm_arcs)} Comm arcs (1 day).")

# More detailed visibility report
visibility_arcs = almanac.report_visibility_arcs(
    lro_state_spec, 1, start_epoch, start_epoch + Unit.Day * 1, Unit.Minute * 10, None
)

if visibility_arcs:
    first_pass = visibility_arcs[0]
    print(f"First pass duration: {first_pass.duration()}")
    print(f"Pass location: {first_pass.location_ref}")

    # Access AER (Azimuth, Elevation, Range) data
    print(f"Number of AER data points: {len(first_pass.aer_data)}")
else:
    print("No visibility arcs found.")
```

    [save_as] overwriting tutorial_loc_kernel.lka


    Found 1 Comm arcs (1 day).
    First pass duration: 8 h 56 min 55 s 251 ms 300 μs 749 ns
    Pass location: DSS65 (#1)
    Number of AER data points: 54



```python

```
