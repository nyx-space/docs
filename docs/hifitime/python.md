This is the Python user guide to hifitime.

## Usage

Hifitime is [available on PyPI](https://pypi.org/project/hifitime/). To install it, you can use `pip` or another Python package manager like [poetry](https://python-poetry.org/), [pipenv](https://pipenv.pypa.io/en/latest/), or any other one.

```shell
pip install hifitime
```

To use Epochs, Durations, Timescales, and Timeseries, just import them as needed:

```python
from hifitime import Epoch, Duration, TimeScale, TimeSeries
```

## Examples

Possibly the best way to get started after installing the package is to look at two example scripts:

+ [`basic.py`](https://github.com/nyx-space/hifitime/blob/3.8.6/examples/python/basic.py) shows a typical workflow from initialization of an Epoch from the system's clock to printing it in different time scales

+ [`timescales.py`](https://github.com/nyx-space/hifitime/blob/3.8.6/examples/python/timescales.py) shows how to use hifitime to compute differences between Epochs in different time scales and how to plot these differences with [plotly](https://plotly.com/) [^1]


## Epoch initialization

The default constructor for `Epoch` in Python is from a string.

Just like in the Rust library, this can be an [RFC3339](rust.md#from-a-string-representation-in-rfc3339) representation:

```python
>>> print(Epoch("1994-11-05T13:15:30Z"))
1994-11-05T13:15:30 UTC
```

Where the time delimiter `T` can be replaced by a space ... 

```python
>>> print(Epoch("1994-11-05 13:15:30Z"))
1994-11-05T13:15:30 UTC
```

Where the UTC identifier `Z` can be omitted (defaults to UTC):

```python
>>> print(Epoch("1994-11-05 13:15:30"))
1994-11-05T13:15:30 UTC
```

Or with an offset from UTC:

```python
>>> print(Epoch("1994-11-05 13:15:30-05:00"))
1994-11-05T18:15:30 UTC
>>> 
```

If the format is unknown, it'll throw an error. In the following example, the dashes between the year, month, and day are missing, so hifitime will complain.

```python
>>> print(Epoch("1994 11 05 13:15:30-05:00"))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
Exception: ParseError: UnknownFormat
>>> 
```

### In a specific time scale

The main advantage of hifitime is that it supports several astronomical time scales. So it's also important to be able to initialize a new epoch from a Gregorian date in those time scales.

In this example, all of these epochs actually represent the same UTC date.

```python
>>> epoch_tt = Epoch("2022-09-06T23:25:38.184000000 TT")
>>> epoch_et = Epoch("2022-09-06T23:25:38.182538909 ET")
>>> epoch_tdb = Epoch("2022-09-06T23:25:38.182541259 TDB")
>>> print(f"{epoch_tt}\n{epoch_et}\n{epoch_tdb}")
2022-09-06T23:24:29 UTC
2022-09-06T23:24:29 UTC
2022-09-06T23:24:29 UTC
```

### From the SPICE representation

NAIF SPICE supports Modified Julian Days and Seconds representation past J2000, and so does hifitime.

```python
>>> print(Epoch("SEC 66312032.18493909 TDB"))
2002-02-06T23:59:28.000000257 UTC
>>> print(Epoch("MJD 58985.5 UTC"))
2020-05-16T12:00:00 UTC
>>> print(Epoch("MJD 58985.5 TAI"))
2020-05-16T11:59:23 UTC
>>> 
```

All of the [initializers from Rust](https://docs.rs/hifitime/latest/hifitime/?search=from_) are also exist in Python, but instead of being `from_blahblah` they are called `init_from_blahblah`.

```python
>>> Epoch.init_from_gregorian_utc_hms(1994, 11, 5, 13, 15, 30)
1994-11-05T13:15:30 UTC
>>> Epoch.init_from_gregorian_tai_hms(1994, 11, 5, 13, 15, 30)
1994-11-05T13:15:01 UTC
>>> 
```

## Converting into another time scale

One of the main uses of hifitime is converting between time scales. Hifitime enables you to convert between UTC, TT, TAI, ET, JDE, GPST, and UNIX time scales, represented as centuries, days, hours, minutes, seconds, milliseconds, microseconds, or nanoseconds.

Most of the time, you'll likely need to find the ET or TDB representation

!!! important
    Recall that in Hifitime, ET and TDB are different time scales. In SPICE, ET is actually TDB without the short fluctuations. Hifitime makes sure that its definition of ET exactly matches the SPICE ET (i.e. TDB without fluctuations). For high precision TDB, use the TDB time scale.

```python
>>> leap_day_2000 = Epoch.init_from_gregorian_utc_hms(2000, 2, 29, 14, 57, 29)
>>> leap_day_2000.to_tdb_seconds()
5108313.185384022
>>> leap_day_2000.to_et_seconds()
5108313.185383182
>>> leap_day_2000.to_jde_et_days()
2451604.123995201
>>> 
```

## Converting into another time unit

Hifitime supports leap seconds in the UTC representation. This is supported by allowing for UTC dates that have `60` as the second count.

In the following example, we want the number of centuries past the ET reference for the provided UTC date, that is on the leap second itself:

```python
>>> leap_second_2016 = Epoch("2016-12-31T23:59:60 UTC")
>>> leap_second_2016.to_et_duration().to_unit(Unit.Century)
0.17000686559938963
>>> 

```

So there are 0.1700 ... centuries between the leap second of 01 January 2017 and J2000, because the ET reference is J2000.

But the TAI reference epoch is J1900, so the same call will return the information nearly a whole centuries before:

```python
>>> leap_second_2016.to_tt_duration().to_unit(Unit.Century)
1.1699931763454763

```

You can do this with any of the durations defined in hifitime:

```python
>>> dir(Unit)
['Century', 'Day', 'Hour', 'Microsecond', 'Millisecond', 'Minute', 'Nanosecond', 'Second', ...]
```

## Epoch arithmetics

The arithmetics on Epochs are done in the time scales used at initialization. For example, adding 10 seconds to an epoch defined in the TAI time scale will lead to a different epoch than adding 10 seconds to an epoch defined in the ET time scale (because ET is a dynamical time scale where one second in ET is not the same as one second in TDB).

### Epoch differences

Epoch time differences are supported in Python starting with version `3.6.0` using the method `timedelta`.

```python
e1 = Epoch.system_now()
e3 = e1 + Unit.Day * 1.5998
epoch_delta = e3.timedelta(e1)
assert epoch_delta == Unit.Day * 1 + Unit.Hour * 14 + Unit.Minute * 23 + Unit.Second * 42.720
print(epoch_delta)
```

### Arithmetics in different time scales

Noon UTC after the first leap second is in fact ten seconds _after_ noon TAI. Hence, there are as many TAI seconds since Epoch between UTC Noon and TAI Noon + 10s.

```python
pre_ls_utc = Epoch.init_from_gregorian_utc_at_noon(1971, 12, 31)
pre_ls_tai = pre_ls_utc.in_time_scale(TimeScale.TAI)
```

Before the first leap second, there is no time difference between both epochs (because only IERS announced leap seconds are accounted for by default).

```python
>>> pre_ls_utc
1971-12-31T12:00:00 UTC
>>> pre_ls_tai
1971-12-31T12:00:00 UTC
```

When add 24 hours to either of the them, the UTC initialized epoch will increase the duration by 36 hours in UTC, which will cause a leap second jump. Therefore the difference between both epochs then becomes 10 seconds.

```python
>>> pre_ls_utc + Unit.Day * 1.0
1972-01-01T12:00:00 UTC
>>> pre_ls_tai + Unit.Day * 1.0
1972-01-01T11:59:50 UTC
>>> 
```

## Duration initializations, time units, and frequency units

Time units and frequency units are trivially supported. Hifitime only supports up to nanosecond precision (but guarantees it for 64 millennia), so any duration less than one nanosecond is truncated.

In Python, a Duration can be initialized from a `Unit` multiplied by a number, either an integer or a float.

```python
>>> Unit.Century * 0.7598
27751 days 16 h 40 min 48 s
>>> Unit.Day * 0.7598
18 h 14 min 6 s 720 ms
>>> Unit.Hour * 0.7598
45 min 35 s 280 ms
>>> Unit.Minute * 0.7598
45 s 588 ms
>>> Unit.Second * 0.7598
759 ms 800 μs
>>> Unit.Millisecond * 0.7598
759 μs 800 ns
>>> Unit.Microsecond * 0.7598
759 ns
>>> 
```

## Iterating over epochs with TimeSeries ("linspace" of epochs)

Finally, hifitime provides a `TimeSeries` structure which allows you to evenly iterate between two epochs at a fixed step.

```python
>>> start = Epoch.system_now() - Unit.Day * 1
>>> end = Epoch.system_now()
>>> ts = TimeSeries(start, end, Unit.Hour * 3, True)
>>> ts
TimeSeries [2022-10-17T23:24:21.458805760 UTC : 2022-10-18T23:24:28.418497024 UTC : 3 h]
>>> for epoch in ts:
...     print(f"{epoch}")
... 
2022-10-17T23:24:21.458805760 UTC
2022-10-18T02:24:21.458805760 UTC
2022-10-18T05:24:21.458805760 UTC
2022-10-18T08:24:21.458805760 UTC
2022-10-18T11:24:21.458805760 UTC
2022-10-18T14:24:21.458805760 UTC
2022-10-18T17:24:21.458805760 UTC
2022-10-18T20:24:21.458805760 UTC
2022-10-18T23:24:21.458805760 UTC
>>> 
```

!!! important
    Iterating over a time series will *consume* it, i.e., it can only be used once!

```python
# Continued from above
2022-10-18T20:24:21.458805760 UTC
2022-10-18T23:24:21.458805760 UTC
>>> for epoch in ts:
...     print(f"{epoch}")
... 
>>> # Nothing is printed because the time series has been fully consumed!
```

If you need to iterate over the same durations several times, you'll need to reinitialize it. Note that a TimeSeries is a lazy structure: each epoch is generated when requested, so the size of a time series object is quite small.

```python
>>> import sys
>>> sys.getsizeof(ts)
120

```

[^1]: This is the script used to generate the plots in the introductory page to hifitime.