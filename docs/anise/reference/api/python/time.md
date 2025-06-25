# Module `anise.time` {#anise.time}

    
## Classes

    
### Class `Duration` {#anise.time.Duration}

>     class Duration(
>         string_repr
>     )

Defines generally usable durations for nanosecond precision valid for 32,768 centuries in either direction, and only on 80 bits / 10 octets.

**Important conventions:**
1. The negative durations can be mentally modeled "BC" years. One hours before 01 Jan 0000, it was "-1" years but  365 days and 23h into the current day.
   It was decided that the nanoseconds corresponds to the nanoseconds _into_ the current century. In other words,
   a duration with centuries = -1 and nanoseconds = 0 is _a greater duration_ (further from zero) than centuries = -1 and nanoseconds = 1.
   Duration zero minus one nanosecond returns a century of -1 and a nanosecond set to the number of nanoseconds in one century minus one.
   That difference is exactly 1 nanoseconds, where the former duration is "closer to zero" than the latter.
   As such, the largest negative duration that can be represented sets the centuries to i16::MAX and its nanoseconds to NANOSECONDS_PER_CENTURY.
2. It was also decided that opposite durations are equal, e.g. -15 minutes == 15 minutes. If the direction of time matters, use the signum function.

(Python documentation hints)
:type string_repr: str
:rtype: Duration

    
#### Methods

    
##### Method `EPSILON` {#anise.time.Duration.EPSILON}

>     def EPSILON()

    
##### Method `MAX` {#anise.time.Duration.MAX}

>     def MAX()

    
##### Method `MIN` {#anise.time.Duration.MIN}

>     def MIN()

    
##### Method `MIN_NEGATIVE` {#anise.time.Duration.MIN_NEGATIVE}

>     def MIN_NEGATIVE()

    
##### Method `MIN_POSITIVE` {#anise.time.Duration.MIN_POSITIVE}

>     def MIN_POSITIVE()

    
##### Method `ZERO` {#anise.time.Duration.ZERO}

>     def ZERO()

    
##### Method `abs` {#anise.time.Duration.abs}

>     def abs(
>         self,
>         /
>     )

Returns the absolute value of this duration
:rtype: Duration

    
##### Method `approx` {#anise.time.Duration.approx}

>     def approx(
>         self,
>         /
>     )

Rounds this duration to the largest units represented in this duration.

This is useful to provide an approximate human duration. Under the hood, this function uses <code>round</code>,
so the "tipping point" of the rounding is half way to the next increment of the greatest unit.
As shown below, one example is that 35 hours and 59 minutes rounds to 1 day, but 36 hours and 1 minute rounds
to 2 days because 2 days is closer to 36h 1 min than 36h 1 min is to 1 day.

##### Example

```
use hifitime::{Duration, TimeUnits};

assert_eq!((2.hours() + 3.minutes()).approx(), 2.hours());
assert_eq!((24.hours() + 3.minutes()).approx(), 1.days());
assert_eq!((35.hours() + 59.minutes()).approx(), 1.days());
assert_eq!((36.hours() + 1.minutes()).approx(), 2.days());
assert_eq!((47.hours() + 3.minutes()).approx(), 2.days());
assert_eq!((49.hours() + 3.minutes()).approx(), 2.days());
```

:rtype: Duration

    
##### Method `ceil` {#anise.time.Duration.ceil}

>     def ceil(
>         self,
>         /,
>         duration
>     )

Ceils this duration to the closest provided duration

This simply floors then adds the requested duration

##### Example
```
use hifitime::{Duration, TimeUnits};

let two_hours_three_min = 2.hours() + 3.minutes();
assert_eq!(two_hours_three_min.ceil(1.hours()), 3.hours());
assert_eq!(two_hours_three_min.ceil(30.minutes()), 2.hours() + 30.minutes());
assert_eq!(two_hours_three_min.ceil(4.hours()), 4.hours());
assert_eq!(two_hours_three_min.ceil(1.seconds()), two_hours_three_min + 1.seconds());
assert_eq!(two_hours_three_min.ceil(1.hours() + 5.minutes()), 2.hours() + 10.minutes());
```

:type duration: Duration
:rtype: Duration

    
##### Method `decompose` {#anise.time.Duration.decompose}

>     def decompose(
>         self,
>         /
>     )

Decomposes a Duration in its sign, days, hours, minutes, seconds, ms, us, ns

:rtype: typing.Tuple

    
##### Method `floor` {#anise.time.Duration.floor}

>     def floor(
>         self,
>         /,
>         duration
>     )

Floors this duration to the closest duration from the bottom

##### Example
```
use hifitime::{Duration, TimeUnits};

let two_hours_three_min = 2.hours() + 3.minutes();
assert_eq!(two_hours_three_min.floor(1.hours()), 2.hours());
assert_eq!(two_hours_three_min.floor(30.minutes()), 2.hours());
// This is zero because we floor by a duration longer than the current duration, rounding it down
assert_eq!(two_hours_three_min.floor(4.hours()), 0.hours());
assert_eq!(two_hours_three_min.floor(1.seconds()), two_hours_three_min);
assert_eq!(two_hours_three_min.floor(1.hours() + 1.minutes()), 2.hours() + 2.minutes());
assert_eq!(two_hours_three_min.floor(1.hours() + 5.minutes()), 1.hours() + 5.minutes());
```

:type duration: Duration
:rtype: Duration

    
##### Method `from_all_parts` {#anise.time.Duration.from_all_parts}

>     def from_all_parts(
>         sign,
>         days,
>         hours,
>         minutes,
>         seconds,
>         milliseconds,
>         microseconds,
>         nanoseconds
>     )

Creates a new duration from its parts
:type sign: int
:type days: int
:type hours: int
:type minutes: int
:type seconds: int
:type milliseconds: int
:type microseconds: int
:type nanoseconds: int
:rtype: Duration

    
##### Method `from_parts` {#anise.time.Duration.from_parts}

>     def from_parts(
>         centuries,
>         nanoseconds
>     )

Create a normalized duration from its parts
:type centuries: int
:type nanoseconds: int
:rtype: Duration

    
##### Method `from_total_nanoseconds` {#anise.time.Duration.from_total_nanoseconds}

>     def from_total_nanoseconds(
>         nanos
>     )

Creates a new Duration from its full nanoseconds
:type nanos: int
:rtype: Duration

    
##### Method `is_negative` {#anise.time.Duration.is_negative}

>     def is_negative(
>         self,
>         /
>     )

Returns whether this is a negative or positive duration.
:rtype: bool

    
##### Method `max` {#anise.time.Duration.max}

>     def max(
>         self,
>         /,
>         other
>     )

Returns the maximum of the two durations.

```
use hifitime::TimeUnits;

let d0 = 20.seconds();
let d1 = 21.seconds();

assert_eq!(d1, d1.max(d0));
assert_eq!(d1, d0.max(d1));
```

:type other: Duration
:rtype: Duration

    
##### Method `min` {#anise.time.Duration.min}

>     def min(
>         self,
>         /,
>         other
>     )

Returns the minimum of the two durations.

```
use hifitime::TimeUnits;

let d0 = 20.seconds();
let d1 = 21.seconds();

assert_eq!(d0, d1.min(d0));
assert_eq!(d0, d0.min(d1));
```

:type other: Duration
:rtype: Duration

    
##### Method `round` {#anise.time.Duration.round}

>     def round(
>         self,
>         /,
>         duration
>     )

Rounds this duration to the closest provided duration

This performs both a <code>ceil</code> and <code>floor</code> and returns the value which is the closest to current one.
##### Example
```
use hifitime::{Duration, TimeUnits};

let two_hours_three_min = 2.hours() + 3.minutes();
assert_eq!(two_hours_three_min.round(1.hours()), 2.hours());
assert_eq!(two_hours_three_min.round(30.minutes()), 2.hours());
assert_eq!(two_hours_three_min.round(4.hours()), 4.hours());
assert_eq!(two_hours_three_min.round(1.seconds()), two_hours_three_min);
assert_eq!(two_hours_three_min.round(1.hours() + 5.minutes()), 2.hours() + 10.minutes());
```

:type duration: Duration
:rtype: Duration

    
##### Method `signum` {#anise.time.Duration.signum}

>     def signum(
>         self,
>         /
>     )

Returns the sign of this duration
+ 0 if the number is zero
+ 1 if the number is positive
+ -1 if the number is negative
:rtype: int

    
##### Method `to_parts` {#anise.time.Duration.to_parts}

>     def to_parts(
>         self,
>         /
>     )

Returns the centuries and nanoseconds of this duration
NOTE: These items are not public to prevent incorrect durations from being created by modifying the values of the structure directly.
:rtype: typing.Tuple

    
##### Method `to_seconds` {#anise.time.Duration.to_seconds}

>     def to_seconds(
>         self,
>         /
>     )

Returns this duration in seconds f64.
For high fidelity comparisons, it is recommended to keep using the Duration structure.
:rtype: float

    
##### Method `to_unit` {#anise.time.Duration.to_unit}

>     def to_unit(
>         self,
>         /,
>         unit
>     )

:type unit: Unit
:rtype: float

    
##### Method `total_nanoseconds` {#anise.time.Duration.total_nanoseconds}

>     def total_nanoseconds(
>         self,
>         /
>     )

Returns the total nanoseconds in a signed 128 bit integer
:rtype: int

    
### Class `DurationError` {#anise.time.DurationError}

>     class DurationError(
>         *args,
>         **kwargs
>     )

    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)

    
### Class `Epoch` {#anise.time.Epoch}

>     class Epoch(
>         string_repr
>     )

Defines a nanosecond-precision Epoch.

Refer to the appropriate functions for initializing this Epoch from different time scales or representations.

(Python documentation hints)
:type string_repr: str
:rtype: Epoch

    
#### Instance variables

    
##### Variable `duration` {#anise.time.Epoch.duration}

:rtype: Duration

    
##### Variable `time_scale` {#anise.time.Epoch.time_scale}

:rtype: TimeScale

    
#### Methods

    
##### Method `ceil` {#anise.time.Epoch.ceil}

>     def ceil(
>         self,
>         /,
>         duration
>     )

Ceils this epoch to the closest provided duration in the TAI time scale

##### Example
```
use hifitime::{Epoch, TimeUnits};

let e = Epoch::from_gregorian_tai_hms(2022, 5, 20, 17, 57, 43);
assert_eq!(
    e.ceil(1.hours()),
    Epoch::from_gregorian_tai_hms(2022, 5, 20, 18, 0, 0)
);

// 45 minutes is a multiple of 3 minutes, hence this result
let e = Epoch::from_gregorian_tai(2022, 10, 3, 17, 44, 29, 898032665);
assert_eq!(
    e.ceil(3.minutes()),
    Epoch::from_gregorian_tai_hms(2022, 10, 3, 17, 45, 0)
);
```
:type duration: Duration
:rtype: Epoch

    
##### Method `day_of_year` {#anise.time.Epoch.day_of_year}

>     def day_of_year(
>         self,
>         /
>     )

Returns the number of days since the start of the year.
:rtype: float

    
##### Method `duration_in_year` {#anise.time.Epoch.duration_in_year}

>     def duration_in_year(
>         self,
>         /
>     )

Returns the duration since the start of the year
:rtype: Duration

    
##### Method `floor` {#anise.time.Epoch.floor}

>     def floor(
>         self,
>         /,
>         duration
>     )

Floors this epoch to the closest provided duration

##### Example
```
use hifitime::{Epoch, TimeUnits};

let e = Epoch::from_gregorian_tai_hms(2022, 5, 20, 17, 57, 43);
assert_eq!(
    e.floor(1.hours()),
    Epoch::from_gregorian_tai_hms(2022, 5, 20, 17, 0, 0)
);

let e = Epoch::from_gregorian_tai(2022, 10, 3, 17, 44, 29, 898032665);
assert_eq!(
    e.floor(3.minutes()),
    Epoch::from_gregorian_tai_hms(2022, 10, 3, 17, 42, 0)
);
```
:type duration: Duration
:rtype: Epoch

    
##### Method `from_bdt_days` {#anise.time.Epoch.from_bdt_days}

>     def from_bdt_days(
>         days
>     )

Initialize an Epoch from the number of days since the BeiDou Time Epoch,
defined as January 1st 2006 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
:type days: float
:rtype: Epoch

    
##### Method `from_bdt_nanoseconds` {#anise.time.Epoch.from_bdt_nanoseconds}

>     def from_bdt_nanoseconds(
>         nanoseconds
>     )

Initialize an Epoch from the number of days since the BeiDou Time Epoch,
defined as January 1st 2006 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
This may be useful for time keeping devices that use BDT as a time source.
:type nanoseconds: float
:rtype: Epoch

    
##### Method `from_bdt_seconds` {#anise.time.Epoch.from_bdt_seconds}

>     def from_bdt_seconds(
>         seconds
>     )

Initialize an Epoch from the number of seconds since the BeiDou Time Epoch,
defined as January 1st 2006 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
:type seconds: float
:rtype: Epoch

    
##### Method `from_et_duration` {#anise.time.Epoch.from_et_duration}

>     def from_et_duration(
>         duration_since_j2000
>     )

Initialize an Epoch from the Ephemeris Time duration past 2000 JAN 01 (J2000 reference)
:type duration_since_j2000: Duration
:rtype: Epoch

    
##### Method `from_et_seconds` {#anise.time.Epoch.from_et_seconds}

>     def from_et_seconds(
>         seconds_since_j2000
>     )

Initialize an Epoch from the Ephemeris Time seconds past 2000 JAN 01 (J2000 reference)
:type seconds_since_j2000: float
:rtype: Epoch

    
##### Method `from_gpst_days` {#anise.time.Epoch.from_gpst_days}

>     def from_gpst_days(
>         days
>     )

Initialize an Epoch from the number of days since the GPS Time Epoch,
defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).
:type days: float
:rtype: Epoch

    
##### Method `from_gpst_nanoseconds` {#anise.time.Epoch.from_gpst_nanoseconds}

>     def from_gpst_nanoseconds(
>         nanoseconds
>     )

Initialize an Epoch from the number of nanoseconds since the GPS Time Epoch,
defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).
This may be useful for time keeping devices that use GPS as a time source.
:type nanoseconds: float
:rtype: Epoch

    
##### Method `from_gpst_seconds` {#anise.time.Epoch.from_gpst_seconds}

>     def from_gpst_seconds(
>         seconds
>     )

Initialize an Epoch from the number of seconds since the GPS Time Epoch,
defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).
:type seconds: float
:rtype: Epoch

    
##### Method `from_gregorian` {#anise.time.Epoch.from_gregorian}

>     def from_gregorian(
>         year,
>         month,
>         day,
>         hour,
>         minute,
>         second,
>         nanos,
>         time_scale
>     )

Initialize from the Gregorian parts
:type year: int
:type month: int
:type day: int
:type hour: int
:type minute: int
:type second: int
:type nanos: int
:type time_scale: TimeScale
:rtype: Epoch

    
##### Method `from_gregorian_at_midnight` {#anise.time.Epoch.from_gregorian_at_midnight}

>     def from_gregorian_at_midnight(
>         year,
>         month,
>         day,
>         time_scale
>     )

Initialize from the Gregorian parts, time set to midnight
:type year: int
:type month: int
:type day: int
:type time_scale: TimeScale
:rtype: Epoch

    
##### Method `from_gregorian_at_noon` {#anise.time.Epoch.from_gregorian_at_noon}

>     def from_gregorian_at_noon(
>         year,
>         month,
>         day,
>         time_scale
>     )

Initialize from the Gregorian parts, time set to noon
:type year: int
:type month: int
:type day: int
:type time_scale: TimeScale
:rtype: Epoch

    
##### Method `from_gregorian_utc` {#anise.time.Epoch.from_gregorian_utc}

>     def from_gregorian_utc(
>         year,
>         month,
>         day,
>         hour,
>         minute,
>         second,
>         nanos
>     )

Builds an Epoch from the provided Gregorian date and time in TAI. If invalid date is provided, this function will panic.
Use maybe_from_gregorian_tai if unsure.

:type year: int
:type month: int
:type day: int
:type hour: int
:type minute: int
:type second: int
:type nanos: int
:rtype: Epoch

    
##### Method `from_gst_days` {#anise.time.Epoch.from_gst_days}

>     def from_gst_days(
>         days
>     )

Initialize an Epoch from the number of days since the Galileo Time Epoch,
starting on August 21st 1999 Midnight UT,
(cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
:type days: float
:rtype: Epoch

    
##### Method `from_gst_nanoseconds` {#anise.time.Epoch.from_gst_nanoseconds}

>     def from_gst_nanoseconds(
>         nanoseconds
>     )

Initialize an Epoch from the number of nanoseconds since the Galileo Time Epoch,
starting on August 21st 1999 Midnight UT,
(cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
This may be useful for time keeping devices that use GST as a time source.
:type nanoseconds: float
:rtype: Epoch

    
##### Method `from_gst_seconds` {#anise.time.Epoch.from_gst_seconds}

>     def from_gst_seconds(
>         seconds
>     )

Initialize an Epoch from the number of seconds since the Galileo Time Epoch,
starting on August 21st 1999 Midnight UT,
(cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
:type seconds: float
:rtype: Epoch

    
##### Method `from_jde_et` {#anise.time.Epoch.from_jde_et}

>     def from_jde_et(
>         days
>     )

Initialize from the JDE days
:type days: float
:rtype: Epoch

    
##### Method `from_jde_tai` {#anise.time.Epoch.from_jde_tai}

>     def from_jde_tai(
>         days
>     )

Initialize an Epoch from given JDE in TAI time scale
:type days: float
:rtype: Epoch

    
##### Method `from_jde_tdb` {#anise.time.Epoch.from_jde_tdb}

>     def from_jde_tdb(
>         days
>     )

Initialize from Dynamic Barycentric Time (TDB) (same as SPICE ephemeris time) in JD days
:type days: float
:rtype: Epoch

    
##### Method `from_jde_utc` {#anise.time.Epoch.from_jde_utc}

>     def from_jde_utc(
>         days
>     )

Initialize an Epoch from given JDE in UTC time scale
:type days: float
:rtype: Epoch

    
##### Method `from_mjd_tai` {#anise.time.Epoch.from_mjd_tai}

>     def from_mjd_tai(
>         days
>     )

Initialize an Epoch from given MJD in TAI time scale
:type days: float
:rtype: Epoch

    
##### Method `from_mjd_utc` {#anise.time.Epoch.from_mjd_utc}

>     def from_mjd_utc(
>         days
>     )

Initialize an Epoch from given MJD in UTC time scale
:type days: float
:rtype: Epoch

    
##### Method `from_ptp_duration` {#anise.time.Epoch.from_ptp_duration}

>     def from_ptp_duration(
>         duration
>     )

Initialize an Epoch from the provided IEEE 1588-2008 (PTPv2) duration since TAI midnight 1970 January 01.
PTP uses the TAI timescale but with the Unix Epoch for compatibility with unix systems.

:type duration: Duration
:rtype: Epoch

    
##### Method `from_ptp_nanoseconds` {#anise.time.Epoch.from_ptp_nanoseconds}

>     def from_ptp_nanoseconds(
>         nanoseconds
>     )

Initialize an Epoch from the provided IEEE 1588-2008 (PTPv2) nanoseconds timestamp since TAI midnight 1970 January 01.
PTP uses the TAI timescale but with the Unix Epoch for compatibility with unix systems.

:type nanoseconds: int
:rtype: Epoch

    
##### Method `from_ptp_seconds` {#anise.time.Epoch.from_ptp_seconds}

>     def from_ptp_seconds(
>         seconds
>     )

Initialize an Epoch from the provided IEEE 1588-2008 (PTPv2) second timestamp since TAI midnight 1970 January 01.
PTP uses the TAI timescale but with the Unix Epoch for compatibility with unix systems.

:type seconds: float
:rtype: Epoch

    
##### Method `from_qzsst_days` {#anise.time.Epoch.from_qzsst_days}

>     def from_qzsst_days(
>         days
>     )

Initialize an Epoch from the number of days since the QZSS Time Epoch,
defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).
:type days: float
:rtype: Epoch

    
##### Method `from_qzsst_nanoseconds` {#anise.time.Epoch.from_qzsst_nanoseconds}

>     def from_qzsst_nanoseconds(
>         nanoseconds
>     )

Initialize an Epoch from the number of nanoseconds since the QZSS Time Epoch,
defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).
This may be useful for time keeping devices that use QZSS as a time source.
:type nanoseconds: int
:rtype: Epoch

    
##### Method `from_qzsst_seconds` {#anise.time.Epoch.from_qzsst_seconds}

>     def from_qzsst_seconds(
>         seconds
>     )

Initialize an Epoch from the number of seconds since the QZSS Time Epoch,
defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).
:type seconds: float
:rtype: Epoch

    
##### Method `from_tai_days` {#anise.time.Epoch.from_tai_days}

>     def from_tai_days(
>         days
>     )

Initialize an Epoch from the provided TAI days since 1900 January 01 at midnight
:type days: float
:rtype: Epoch

    
##### Method `from_tai_duration` {#anise.time.Epoch.from_tai_duration}

>     def from_tai_duration(
>         duration
>     )

Creates a new Epoch from a Duration as the time difference between this epoch and TAI reference epoch.
:type duration: Duration
:rtype: Epoch

    
##### Method `from_tai_parts` {#anise.time.Epoch.from_tai_parts}

>     def from_tai_parts(
>         centuries,
>         nanoseconds
>     )

Creates a new Epoch from its centuries and nanosecond since the TAI reference epoch.
:type centuries: int
:type nanoseconds: int
:rtype: Epoch

    
##### Method `from_tai_seconds` {#anise.time.Epoch.from_tai_seconds}

>     def from_tai_seconds(
>         seconds
>     )

Initialize an Epoch from the provided TAI seconds since 1900 January 01 at midnight
:type seconds: float
:rtype: Epoch

    
##### Method `from_tdb_duration` {#anise.time.Epoch.from_tdb_duration}

>     def from_tdb_duration(
>         duration_since_j2000
>     )

Initialize from Dynamic Barycentric Time (TDB) (same as SPICE ephemeris time) whose epoch is 2000 JAN 01 noon TAI.
 :type duration_since_j2000: Duration
:rtype: Epoch

    
##### Method `from_tdb_seconds` {#anise.time.Epoch.from_tdb_seconds}

>     def from_tdb_seconds(
>         seconds_j2000
>     )

Initialize an Epoch from Dynamic Barycentric Time (TDB) seconds past 2000 JAN 01 midnight (difference than SPICE)
NOTE: This uses the ESA algorithm, which is a notch more complicated than the SPICE algorithm, but more precise.
In fact, SPICE algorithm is precise +/- 30 microseconds for a century whereas ESA algorithm should be exactly correct.
:type seconds_j2000: float
:rtype: Epoch

    
##### Method `from_tt_duration` {#anise.time.Epoch.from_tt_duration}

>     def from_tt_duration(
>         duration
>     )

Initialize an Epoch from the provided TT seconds (approximated to 32.184s delta from TAI)
:type duration: Duration
:rtype: Epoch

    
##### Method `from_tt_seconds` {#anise.time.Epoch.from_tt_seconds}

>     def from_tt_seconds(
>         seconds
>     )

Initialize an Epoch from the provided TT seconds (approximated to 32.184s delta from TAI)
:type seconds: float
:rtype: Epoch

    
##### Method `from_unix_milliseconds` {#anise.time.Epoch.from_unix_milliseconds}

>     def from_unix_milliseconds(
>         milliseconds
>     )

Initialize an Epoch from the provided UNIX millisecond timestamp since UTC midnight 1970 January 01.
:type milliseconds: float
:rtype: Epoch

    
##### Method `from_unix_seconds` {#anise.time.Epoch.from_unix_seconds}

>     def from_unix_seconds(
>         seconds
>     )

Initialize an Epoch from the provided UNIX second timestamp since UTC midnight 1970 January 01.
:type seconds: float
:rtype: Epoch

    
##### Method `from_utc_days` {#anise.time.Epoch.from_utc_days}

>     def from_utc_days(
>         days
>     )

Initialize an Epoch from the provided UTC days since 1900 January 01 at midnight
:type days: float
:rtype: Epoch

    
##### Method `from_utc_seconds` {#anise.time.Epoch.from_utc_seconds}

>     def from_utc_seconds(
>         seconds
>     )

Initialize an Epoch from the provided UTC seconds since 1900 January 01 at midnight
:type seconds: float
:rtype: Epoch

    
##### Method `fromdatetime` {#anise.time.Epoch.fromdatetime}

>     def fromdatetime(
>         dt
>     )

Builds an Epoch in UTC from the provided datetime after timezone correction if any is present.
:type dt: datetime.datetime
:rtype: Epoch

    
##### Method `hours` {#anise.time.Epoch.hours}

>     def hours(
>         self,
>         /
>     )

Returns the hours of the Gregorian representation  of this epoch in the time scale it was initialized in.
:rtype: int

    
##### Method `init_from_bdt_days` {#anise.time.Epoch.init_from_bdt_days}

>     def init_from_bdt_days(
>         days
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_bdt\_days</code> instead
Initialize an Epoch from the number of days since the BeiDou Time Epoch,
defined as January 1st 2006 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
:type days: float
:rtype: Epoch

    
##### Method `init_from_bdt_nanoseconds` {#anise.time.Epoch.init_from_bdt_nanoseconds}

>     def init_from_bdt_nanoseconds(
>         nanoseconds
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_bdt\_nanoseconds</code> instead
Initialize an Epoch from the number of days since the BeiDou Time Epoch,
defined as January 1st 2006 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
This may be useful for time keeping devices that use BDT as a time source.
:type nanoseconds: float
:rtype: Epoch

    
##### Method `init_from_bdt_seconds` {#anise.time.Epoch.init_from_bdt_seconds}

>     def init_from_bdt_seconds(
>         seconds
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_bdt\_seconds</code> instead
Initialize an Epoch from the number of seconds since the BeiDou Time Epoch,
defined as January 1st 2006 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
:type seconds: float
:rtype: Epoch

    
##### Method `init_from_et_duration` {#anise.time.Epoch.init_from_et_duration}

>     def init_from_et_duration(
>         duration_since_j2000
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_et\_duration</code> instead
Initialize an Epoch from the Ephemeris Time duration past 2000 JAN 01 (J2000 reference)
:type duration_since_j2000: Duration
:rtype: Epoch

    
##### Method `init_from_et_seconds` {#anise.time.Epoch.init_from_et_seconds}

>     def init_from_et_seconds(
>         seconds_since_j2000
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_et\_seconds</code> instead
Initialize an Epoch from the Ephemeris Time seconds past 2000 JAN 01 (J2000 reference)
:type seconds_since_j2000: float
:rtype: Epoch

    
##### Method `init_from_gpst_days` {#anise.time.Epoch.init_from_gpst_days}

>     def init_from_gpst_days(
>         days
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_gpst\_days</code> instead
Initialize an Epoch from the number of days since the GPS Time Epoch,
defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).
:type days: float
:rtype: Epoch

    
##### Method `init_from_gpst_nanoseconds` {#anise.time.Epoch.init_from_gpst_nanoseconds}

>     def init_from_gpst_nanoseconds(
>         nanoseconds
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_gpst\_nanoseconds</code> instead
Initialize an Epoch from the number of nanoseconds since the GPS Time Epoch,
defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).
This may be useful for time keeping devices that use GPS as a time source.
:type nanoseconds: float
:rtype: Epoch

    
##### Method `init_from_gpst_seconds` {#anise.time.Epoch.init_from_gpst_seconds}

>     def init_from_gpst_seconds(
>         seconds
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_gpst\_seconds</code> instead
Initialize an Epoch from the number of seconds since the GPS Time Epoch,
defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).
:type seconds: float
:rtype: Epoch

    
##### Method `init_from_gregorian` {#anise.time.Epoch.init_from_gregorian}

>     def init_from_gregorian(
>         year,
>         month,
>         day,
>         hour,
>         minute,
>         second,
>         nanos,
>         time_scale
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_gregorian</code> instead
Initialize from the Gregorian parts
:type year: int
:type month: int
:type day: int
:type hour: int
:type minute: int
:type second: int
:type nanos: int
:type time_scale: TimeScale
:rtype: Epoch

    
##### Method `init_from_gregorian_at_midnight` {#anise.time.Epoch.init_from_gregorian_at_midnight}

>     def init_from_gregorian_at_midnight(
>         year,
>         month,
>         day,
>         time_scale
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_gregorian\_at\_midnight</code> instead
Initialize from the Gregorian parts, time set to midnight
:type year: int
:type month: int
:type day: int
:type time_scale: TimeScale
:rtype: Epoch

    
##### Method `init_from_gregorian_at_noon` {#anise.time.Epoch.init_from_gregorian_at_noon}

>     def init_from_gregorian_at_noon(
>         year,
>         month,
>         day,
>         time_scale
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_gregorian\_at\_noon</code> instead
Initialize from the Gregorian parts, time set to noon
:type year: int
:type month: int
:type day: int
:type time_scale: TimeScale
:rtype: Epoch

    
##### Method `init_from_gregorian_utc` {#anise.time.Epoch.init_from_gregorian_utc}

>     def init_from_gregorian_utc(
>         year,
>         month,
>         day,
>         hour,
>         minute,
>         second,
>         nanos
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_gregorian\_utc</code> instead
Builds an Epoch from the provided Gregorian date and time in TAI. If invalid date is provided, this function will panic.
Use maybe_from_gregorian_tai if unsure.

:type year: int
:type month: int
:type day: int
:type hour: int
:type minute: int
:type second: int
:type nanos: int
:rtype: Epoch

    
##### Method `init_from_gst_days` {#anise.time.Epoch.init_from_gst_days}

>     def init_from_gst_days(
>         days
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_gst\_days</code> instead
Initialize an Epoch from the number of days since the Galileo Time Epoch,
starting on August 21st 1999 Midnight UT,
(cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
:type days: float
:rtype: Epoch

    
##### Method `init_from_gst_nanoseconds` {#anise.time.Epoch.init_from_gst_nanoseconds}

>     def init_from_gst_nanoseconds(
>         nanoseconds
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_gst\_nanoseconds</code> instead
Initialize an Epoch from the number of nanoseconds since the Galileo Time Epoch,
starting on August 21st 1999 Midnight UT,
(cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
This may be useful for time keeping devices that use GST as a time source.
:type nanoseconds: float
:rtype: Epoch

    
##### Method `init_from_gst_seconds` {#anise.time.Epoch.init_from_gst_seconds}

>     def init_from_gst_seconds(
>         seconds
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_gst\_seconds</code> instead
Initialize an Epoch from the number of seconds since the Galileo Time Epoch,
starting on August 21st 1999 Midnight UT,
(cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
:type seconds: float
:rtype: Epoch

    
##### Method `init_from_jde_et` {#anise.time.Epoch.init_from_jde_et}

>     def init_from_jde_et(
>         days
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_jde\_et</code> instead
Initialize from the JDE days
:type days: float
:rtype: Epoch

    
##### Method `init_from_jde_tai` {#anise.time.Epoch.init_from_jde_tai}

>     def init_from_jde_tai(
>         days
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_jde\_tai</code> instead
Initialize an Epoch from given JDE in TAI time scale
:type days: float
:rtype: Epoch

    
##### Method `init_from_jde_tdb` {#anise.time.Epoch.init_from_jde_tdb}

>     def init_from_jde_tdb(
>         days
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_jde\_tdb</code> instead
Initialize from Dynamic Barycentric Time (TDB) (same as SPICE ephemeris time) in JD days
:type days: float
:rtype: Epoch

    
##### Method `init_from_jde_utc` {#anise.time.Epoch.init_from_jde_utc}

>     def init_from_jde_utc(
>         days
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_jde\_utc</code> instead
Initialize an Epoch from given JDE in UTC time scale
:type days: float
:rtype: Epoch

    
##### Method `init_from_mjd_tai` {#anise.time.Epoch.init_from_mjd_tai}

>     def init_from_mjd_tai(
>         days
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_mjd\_tai</code> instead
Initialize an Epoch from given MJD in TAI time scale
:type days: float
:rtype: Epoch

    
##### Method `init_from_mjd_utc` {#anise.time.Epoch.init_from_mjd_utc}

>     def init_from_mjd_utc(
>         days
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_mjd\_utc</code> instead
Initialize an Epoch from given MJD in UTC time scale
:type days: float
:rtype: Epoch

    
##### Method `init_from_qzsst_days` {#anise.time.Epoch.init_from_qzsst_days}

>     def init_from_qzsst_days(
>         days
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_qzsst\_days</code> instead
Initialize an Epoch from the number of days since the QZSS Time Epoch,
defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).
:type days: float
:rtype: Epoch

    
##### Method `init_from_qzsst_nanoseconds` {#anise.time.Epoch.init_from_qzsst_nanoseconds}

>     def init_from_qzsst_nanoseconds(
>         nanoseconds
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_qzsst\_nanoseconds</code> instead
Initialize an Epoch from the number of nanoseconds since the QZSS Time Epoch,
defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).
This may be useful for time keeping devices that use QZSS as a time source.
:type nanoseconds: int
:rtype: Epoch

    
##### Method `init_from_qzsst_seconds` {#anise.time.Epoch.init_from_qzsst_seconds}

>     def init_from_qzsst_seconds(
>         seconds
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_qzsst\_seconds</code> instead
Initialize an Epoch from the number of seconds since the QZSS Time Epoch,
defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).
:type seconds: float
:rtype: Epoch

    
##### Method `init_from_tai_days` {#anise.time.Epoch.init_from_tai_days}

>     def init_from_tai_days(
>         days
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_tai\_days</code> instead
Initialize an Epoch from the provided TAI days since 1900 January 01 at midnight
:type days: float
:rtype: Epoch

    
##### Method `init_from_tai_duration` {#anise.time.Epoch.init_from_tai_duration}

>     def init_from_tai_duration(
>         duration
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_tai\_duration</code> instead
Creates a new Epoch from a Duration as the time difference between this epoch and TAI reference epoch.
:type duration: Duration
:rtype: Epoch

    
##### Method `init_from_tai_parts` {#anise.time.Epoch.init_from_tai_parts}

>     def init_from_tai_parts(
>         centuries,
>         nanoseconds
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_tai\_parts</code> instead
Creates a new Epoch from its centuries and nanosecond since the TAI reference epoch.
:type centuries: int
:type nanoseconds: int
:rtype: Epoch

    
##### Method `init_from_tai_seconds` {#anise.time.Epoch.init_from_tai_seconds}

>     def init_from_tai_seconds(
>         seconds
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_tai\_seconds</code> instead
Initialize an Epoch from the provided TAI seconds since 1900 January 01 at midnight
:type seconds: float
:rtype: Epoch

    
##### Method `init_from_tdb_duration` {#anise.time.Epoch.init_from_tdb_duration}

>     def init_from_tdb_duration(
>         duration_since_j2000
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_tdb\_duration</code> instead
Initialize from Dynamic Barycentric Time (TDB) (same as SPICE ephemeris time) whose epoch is 2000 JAN 01 noon TAI.
 :type duration_since_j2000: Duration
:rtype: Epoch

    
##### Method `init_from_tdb_seconds` {#anise.time.Epoch.init_from_tdb_seconds}

>     def init_from_tdb_seconds(
>         seconds_j2000
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_tdb\_seconds</code> instead
Initialize an Epoch from Dynamic Barycentric Time (TDB) seconds past 2000 JAN 01 midnight (difference than SPICE)
NOTE: This uses the ESA algorithm, which is a notch more complicated than the SPICE algorithm, but more precise.
In fact, SPICE algorithm is precise +/- 30 microseconds for a century whereas ESA algorithm should be exactly correct.
:type seconds_j2000: float
:rtype: Epoch

    
##### Method `init_from_tt_duration` {#anise.time.Epoch.init_from_tt_duration}

>     def init_from_tt_duration(
>         duration
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_tt\_duration</code> instead
Initialize an Epoch from the provided TT seconds (approximated to 32.184s delta from TAI)
:type duration: Duration
:rtype: Epoch

    
##### Method `init_from_tt_seconds` {#anise.time.Epoch.init_from_tt_seconds}

>     def init_from_tt_seconds(
>         seconds
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_tt\_seconds</code> instead
Initialize an Epoch from the provided TT seconds (approximated to 32.184s delta from TAI)
:type seconds: float
:rtype: Epoch

    
##### Method `init_from_unix_milliseconds` {#anise.time.Epoch.init_from_unix_milliseconds}

>     def init_from_unix_milliseconds(
>         milliseconds
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_unix\_milliseconds</code> instead
Initialize an Epoch from the provided UNIX millisecond timestamp since UTC midnight 1970 January 01.
:type milliseconds: float
:rtype: Epoch

    
##### Method `init_from_unix_seconds` {#anise.time.Epoch.init_from_unix_seconds}

>     def init_from_unix_seconds(
>         seconds
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_unix\_seconds</code> instead
Initialize an Epoch from the provided UNIX second timestamp since UTC midnight 1970 January 01.
:type seconds: float
:rtype: Epoch

    
##### Method `init_from_utc_days` {#anise.time.Epoch.init_from_utc_days}

>     def init_from_utc_days(
>         days
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_utc\_days</code> instead
Initialize an Epoch from the provided UTC days since 1900 January 01 at midnight
:type days: float
:rtype: Epoch

    
##### Method `init_from_utc_seconds` {#anise.time.Epoch.init_from_utc_seconds}

>     def init_from_utc_seconds(
>         seconds
>     )

WARNING: Deprecated since 4.1.1; Use <code>from\_utc\_seconds</code> instead
Initialize an Epoch from the provided UTC seconds since 1900 January 01 at midnight
:type seconds: float
:rtype: Epoch

    
##### Method `isoformat` {#anise.time.Epoch.isoformat}

>     def isoformat(
>         self,
>         /
>     )

Equivalent to <code>datetime.isoformat</code>, and truncated to 23 chars, refer to <https://docs.rs/hifitime/latest/hifitime/efmt/format/struct.Format.html> for format options
:rtype: str

    
##### Method `leap_seconds` {#anise.time.Epoch.leap_seconds}

>     def leap_seconds(
>         self,
>         /,
>         iers_only
>     )

Get the accumulated number of leap seconds up to this Epoch accounting only for the IERS leap seconds and the SOFA scaling from 1960 to 1972, depending on flag.
Returns None if the epoch is before 1960, year at which UTC was defined.

##### Why does this function return an <code>Option</code> when the other returns a value
This is to match the <code>iauDat</code> function of SOFA (src/dat.c). That function will return a warning and give up if the start date is before 1960.
:type iers_only: bool
:rtype: float

    
##### Method `leap_seconds_iers` {#anise.time.Epoch.leap_seconds_iers}

>     def leap_seconds_iers(
>         self,
>         /
>     )

Get the accumulated number of leap seconds up to this Epoch accounting only for the IERS leap seconds.
:rtype: int

    
##### Method `leap_seconds_with_file` {#anise.time.Epoch.leap_seconds_with_file}

>     def leap_seconds_with_file(
>         self,
>         /,
>         iers_only,
>         provider
>     )

Get the accumulated number of leap seconds up to this Epoch from the provided LeapSecondProvider.
Returns None if the epoch is before 1960, year at which UTC was defined.

##### Why does this function return an <code>Option</code> when the other returns a value
This is to match the <code>iauDat</code> function of SOFA (src/dat.c). That function will return a warning and give up if the start date is before 1960.

:type iers_only: bool
:type provider: LeapSecondsFile
:rtype: float

    
##### Method `max` {#anise.time.Epoch.max}

>     def max(
>         self,
>         /,
>         other
>     )

Returns the maximum of the two epochs.

```
use hifitime::Epoch;

let e0 = Epoch::from_gregorian_utc_at_midnight(2022, 10, 20);
let e1 = Epoch::from_gregorian_utc_at_midnight(2022, 10, 21);

assert_eq!(e1, e1.max(e0));
assert_eq!(e1, e0.max(e1));
```

_Note:_ this uses a pointer to <code>self</code> which will be copied immediately because Python requires a pointer.
:type other: Epoch
:rtype: Epoch

    
##### Method `microseconds` {#anise.time.Epoch.microseconds}

>     def microseconds(
>         self,
>         /
>     )

Returns the microseconds of the Gregorian representation  of this epoch in the time scale it was initialized in.
:rtype: int

    
##### Method `milliseconds` {#anise.time.Epoch.milliseconds}

>     def milliseconds(
>         self,
>         /
>     )

Returns the milliseconds of the Gregorian representation  of this epoch in the time scale it was initialized in.
:rtype: int

    
##### Method `min` {#anise.time.Epoch.min}

>     def min(
>         self,
>         /,
>         other
>     )

Returns the minimum of the two epochs.

```
use hifitime::Epoch;

let e0 = Epoch::from_gregorian_utc_at_midnight(2022, 10, 20);
let e1 = Epoch::from_gregorian_utc_at_midnight(2022, 10, 21);

assert_eq!(e0, e1.min(e0));
assert_eq!(e0, e0.min(e1));
```

_Note:_ this uses a pointer to <code>self</code> which will be copied immediately because Python requires a pointer.
:type other: Epoch
:rtype: Epoch

    
##### Method `minutes` {#anise.time.Epoch.minutes}

>     def minutes(
>         self,
>         /
>     )

Returns the minutes of the Gregorian representation  of this epoch in the time scale it was initialized in.
:rtype: int

    
##### Method `month_name` {#anise.time.Epoch.month_name}

>     def month_name(
>         self,
>         /
>     )

:rtype: MonthName

    
##### Method `nanoseconds` {#anise.time.Epoch.nanoseconds}

>     def nanoseconds(
>         self,
>         /
>     )

Returns the nanoseconds of the Gregorian representation  of this epoch in the time scale it was initialized in.
:rtype: int

    
##### Method `next` {#anise.time.Epoch.next}

>     def next(
>         self,
>         /,
>         weekday
>     )

Returns the next weekday.

```
use hifitime::prelude::*;

let epoch = Epoch::from_gregorian_utc_at_midnight(1988, 1, 2);
assert_eq!(epoch.weekday_utc(), Weekday::Saturday);
assert_eq!(epoch.next(Weekday::Sunday), Epoch::from_gregorian_utc_at_midnight(1988, 1, 3));
assert_eq!(epoch.next(Weekday::Monday), Epoch::from_gregorian_utc_at_midnight(1988, 1, 4));
assert_eq!(epoch.next(Weekday::Tuesday), Epoch::from_gregorian_utc_at_midnight(1988, 1, 5));
assert_eq!(epoch.next(Weekday::Wednesday), Epoch::from_gregorian_utc_at_midnight(1988, 1, 6));
assert_eq!(epoch.next(Weekday::Thursday), Epoch::from_gregorian_utc_at_midnight(1988, 1, 7));
assert_eq!(epoch.next(Weekday::Friday), Epoch::from_gregorian_utc_at_midnight(1988, 1, 8));
assert_eq!(epoch.next(Weekday::Saturday), Epoch::from_gregorian_utc_at_midnight(1988, 1, 9));
```
:type weekday: Weekday
:rtype: Epoch

    
##### Method `next_weekday_at_midnight` {#anise.time.Epoch.next_weekday_at_midnight}

>     def next_weekday_at_midnight(
>         self,
>         /,
>         weekday
>     )

:type weekday: Weekday
:rtype: Epoch

    
##### Method `next_weekday_at_noon` {#anise.time.Epoch.next_weekday_at_noon}

>     def next_weekday_at_noon(
>         self,
>         /,
>         weekday
>     )

:type weekday: Weekday
:rtype: Epoch

    
##### Method `precise_timescale_conversion` {#anise.time.Epoch.precise_timescale_conversion}

>     def precise_timescale_conversion(
>         self,
>         /,
>         forward,
>         reference_epoch,
>         polynomial,
>         target
>     )

Converts this [Epoch] into targeted [TimeScale] using provided [Polynomial].

###### Input
- forward: whether this is forward or backward conversion.
  For example, using GPST-UTC [Polynomial]
  - GPST->UTC is the forward conversion
  - UTC->GPST is the backward conversion
- reference_epoch: any reference [Epoch] for the provided [Polynomial].  

While we support any time difference, it should remain short in pratice (a day at most, for precise applications).
- polynomial: that must be valid for this reference [Epoch], used in the equation `a0 + a1*dt + a2*dt² = GPST-UTC` for example.
- target: targetted [TimeScale] we will transition to.

Example:
```
use hifitime::{Epoch, TimeScale, Polynomial, Unit};

// random GPST Epoch for forward conversion to UTC
let t_gpst = Epoch::from_gregorian(2020, 01, 01, 0, 0, 0, 0, TimeScale::GPST);

// Let's say we know the GPST-UTC polynomials for that day,
// They allow precise forward transition from GPST to UTC,
// and precise backward transition from UTC to GPST.
let gpst_utc_polynomials = Polynomial::from_constant_offset_nanoseconds(1.0);

// This is the reference [Epoch] attached to the publication of these polynomials.
// You should use polynomials that remain valid and were provided recently (usually one day at most).
// Example: polynomials were published 1 hour ago.
let gpst_reference = t_gpst - 1.0 * Unit::Hour;

// Forward conversion (to UTC) GPST - a0 + a1 *dt + a2*dt² = UTC
let t_utc = t_gpst.precise_timescale_conversion(true, gpst_reference, gpst_utc_polynomials, TimeScale::UTC)
    .unwrap();

// Verify we did transition to UTC
assert_eq!(t_utc.time_scale, TimeScale::UTC);

// Verify the resulting [Epoch] is the coarse GPST->UTC transition + fine correction
let reversed = t_utc.to_time_scale(TimeScale::GPST) + 1.0 * Unit::Nanosecond;
assert_eq!(reversed, t_gpst);

// Apply the backward transition, from t_utc back to t_gpst.
// The timescale conversion works both ways: (from UTC) GPST = UTC + a0 + a1 *dt + a2*dt²
let backwards = t_utc.precise_timescale_conversion(false, gpst_reference, gpst_utc_polynomials, TimeScale::GPST)
    .unwrap();

assert_eq!(backwards, t_gpst);

// It is important to understand that your reference point does not have to be in the past.
// The only logic that should prevail is to always minimize interpolation gap.
// In other words, if you can access future interpolation information that would minimize the data gap, they should prevail.
// Example: +30' in the future.
let gpst_reference = t_gpst + 30.0 * Unit::Minute;

// Forward conversion (to UTC) but using polynomials that were released 1 hour after t_gpst
let t_utc = t_gpst.precise_timescale_conversion(true, gpst_reference, gpst_utc_polynomials, TimeScale::UTC)
    .unwrap();

// Verifications
assert_eq!(t_utc.time_scale, TimeScale::UTC);

let reversed = t_utc.to_time_scale(TimeScale::GPST) + 1.0 * Unit::Nanosecond;
assert_eq!(reversed, t_gpst);
```
:type forward: bool
:type reference_epoch: Epoch
:type polynomial: Polynomial
:type target: TimeScale
:rtype: Epoch

    
##### Method `previous` {#anise.time.Epoch.previous}

>     def previous(
>         self,
>         /,
>         weekday
>     )

Returns the next weekday.

```
use hifitime::prelude::*;

let epoch = Epoch::from_gregorian_utc_at_midnight(1988, 1, 2);
assert_eq!(epoch.previous(Weekday::Friday), Epoch::from_gregorian_utc_at_midnight(1988, 1, 1));
assert_eq!(epoch.previous(Weekday::Thursday), Epoch::from_gregorian_utc_at_midnight(1987, 12, 31));
assert_eq!(epoch.previous(Weekday::Wednesday), Epoch::from_gregorian_utc_at_midnight(1987, 12, 30));
assert_eq!(epoch.previous(Weekday::Tuesday), Epoch::from_gregorian_utc_at_midnight(1987, 12, 29));
assert_eq!(epoch.previous(Weekday::Monday), Epoch::from_gregorian_utc_at_midnight(1987, 12, 28));
assert_eq!(epoch.previous(Weekday::Sunday), Epoch::from_gregorian_utc_at_midnight(1987, 12, 27));
assert_eq!(epoch.previous(Weekday::Saturday), Epoch::from_gregorian_utc_at_midnight(1987, 12, 26));
```
:type weekday: Weekday
:rtype: Epoch

    
##### Method `previous_weekday_at_midnight` {#anise.time.Epoch.previous_weekday_at_midnight}

>     def previous_weekday_at_midnight(
>         self,
>         /,
>         weekday
>     )

:type weekday: Weekday
:rtype: Epoch

    
##### Method `previous_weekday_at_noon` {#anise.time.Epoch.previous_weekday_at_noon}

>     def previous_weekday_at_noon(
>         self,
>         /,
>         weekday
>     )

:type weekday: Weekday
:rtype: Epoch

    
##### Method `round` {#anise.time.Epoch.round}

>     def round(
>         self,
>         /,
>         duration
>     )

Rounds this epoch to the closest provided duration in TAI

##### Example
```
use hifitime::{Epoch, TimeUnits};

let e = Epoch::from_gregorian_tai_hms(2022, 5, 20, 17, 57, 43);
assert_eq!(
    e.round(1.hours()),
    Epoch::from_gregorian_tai_hms(2022, 5, 20, 18, 0, 0)
);
```
:type duration: Duration
:rtype: Epoch

    
##### Method `seconds` {#anise.time.Epoch.seconds}

>     def seconds(
>         self,
>         /
>     )

Returns the seconds of the Gregorian representation  of this epoch in the time scale it was initialized in.
:rtype: int

    
##### Method `strftime` {#anise.time.Epoch.strftime}

>     def strftime(
>         self,
>         /,
>         format_str
>     )

Formats the epoch according to the given format string. Supports a subset of C89 and hifitime-specific format codes. Refer to <https://docs.rs/hifitime/latest/hifitime/efmt/format/struct.Format.html> for available format options.
:type format_str: str
:rtype: str

    
##### Method `strptime` {#anise.time.Epoch.strptime}

>     def strptime(
>         epoch_str,
>         format_str
>     )

Equivalent to <code>datetime.strptime</code>, refer to <https://docs.rs/hifitime/latest/hifitime/efmt/format/struct.Format.html> for format options
:type epoch_str: str
:type format_str: str
:rtype: Epoch

    
##### Method `system_now` {#anise.time.Epoch.system_now}

>     def system_now()

Returns the computer clock in UTC

:rtype: Epoch

    
##### Method `timedelta` {#anise.time.Epoch.timedelta}

>     def timedelta(
>         self,
>         /,
>         other
>     )

Differences between two epochs
:type other: Duration
:rtype: Duration

    
##### Method `to_bdt_days` {#anise.time.Epoch.to_bdt_days}

>     def to_bdt_days(
>         self,
>         /
>     )

Returns days past BDT (BeiDou) Time Epoch, defined as Jan 01 2006 UTC
(cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
:rtype: float

    
##### Method `to_bdt_duration` {#anise.time.Epoch.to_bdt_duration}

>     def to_bdt_duration(
>         self,
>         /
>     )

Returns <code>[Duration](#anise.time.Duration "anise.time.Duration")</code> past BDT (BeiDou) time Epoch.
:rtype: Duration

    
##### Method `to_bdt_nanoseconds` {#anise.time.Epoch.to_bdt_nanoseconds}

>     def to_bdt_nanoseconds(
>         self,
>         /
>     )

Returns nanoseconds past BDT (BeiDou) Time Epoch, defined as Jan 01 2006 UTC
(cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
NOTE: This function will return an error if the centuries past GST time are not zero.
:rtype: int

    
##### Method `to_bdt_seconds` {#anise.time.Epoch.to_bdt_seconds}

>     def to_bdt_seconds(
>         self,
>         /
>     )

Returns seconds past BDT (BeiDou) Time Epoch
:rtype: float

    
##### Method `to_duration_in_time_scale` {#anise.time.Epoch.to_duration_in_time_scale}

>     def to_duration_in_time_scale(
>         self,
>         /,
>         ts
>     )

Returns this epoch with respect to the provided time scale.
This is needed to correctly perform duration conversions in dynamical time scales (e.g. TDB).
:type ts: TimeScale
:rtype: Duration

    
##### Method `to_et_centuries_since_j2000` {#anise.time.Epoch.to_et_centuries_since_j2000}

>     def to_et_centuries_since_j2000(
>         self,
>         /
>     )

Returns the number of centuries since Ephemeris Time (ET) J2000 (used for Archinal et al. rotations)
:rtype: float

    
##### Method `to_et_days_since_j2000` {#anise.time.Epoch.to_et_days_since_j2000}

>     def to_et_days_since_j2000(
>         self,
>         /
>     )

Returns the number of days since Ephemeris Time (ET) J2000 (used for Archinal et al. rotations)
:rtype: float

    
##### Method `to_et_duration` {#anise.time.Epoch.to_et_duration}

>     def to_et_duration(
>         self,
>         /
>     )

Returns the duration between J2000 and the current epoch as per NAIF SPICE.

##### Warning
The et2utc function of NAIF SPICE will assume that there are 9 leap seconds before 01 JAN 1972,
as this date introduces 10 leap seconds. At the time of writing, this does _not_ seem to be in
line with IERS and the documentation in the leap seconds list.

In order to match SPICE, the as_et_duration() function will manually get rid of that difference.
:rtype: Duration

    
##### Method `to_et_seconds` {#anise.time.Epoch.to_et_seconds}

>     def to_et_seconds(
>         self,
>         /
>     )

Returns the Ephemeris Time seconds past 2000 JAN 01 midnight, matches NASA/NAIF SPICE.
:rtype: float

    
##### Method `to_gpst_days` {#anise.time.Epoch.to_gpst_days}

>     def to_gpst_days(
>         self,
>         /
>     )

Returns days past GPS Time Epoch, defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).
:rtype: float

    
##### Method `to_gpst_duration` {#anise.time.Epoch.to_gpst_duration}

>     def to_gpst_duration(
>         self,
>         /
>     )

Returns <code>[Duration](#anise.time.Duration "anise.time.Duration")</code> past GPS time Epoch.
:rtype: Duration

    
##### Method `to_gpst_nanoseconds` {#anise.time.Epoch.to_gpst_nanoseconds}

>     def to_gpst_nanoseconds(
>         self,
>         /
>     )

Returns nanoseconds past GPS Time Epoch, defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).
NOTE: This function will return an error if the centuries past GPST time are not zero.
:rtype: int

    
##### Method `to_gpst_seconds` {#anise.time.Epoch.to_gpst_seconds}

>     def to_gpst_seconds(
>         self,
>         /
>     )

Returns seconds past GPS Time Epoch, defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).
:rtype: float

    
##### Method `to_gst_days` {#anise.time.Epoch.to_gst_days}

>     def to_gst_days(
>         self,
>         /
>     )

Returns days past GST (Galileo) Time Epoch,
starting on August 21st 1999 Midnight UT
(cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
:rtype: float

    
##### Method `to_gst_duration` {#anise.time.Epoch.to_gst_duration}

>     def to_gst_duration(
>         self,
>         /
>     )

Returns <code>[Duration](#anise.time.Duration "anise.time.Duration")</code> past GST (Galileo) time Epoch.
:rtype: Duration

    
##### Method `to_gst_nanoseconds` {#anise.time.Epoch.to_gst_nanoseconds}

>     def to_gst_nanoseconds(
>         self,
>         /
>     )

Returns nanoseconds past GST (Galileo) Time Epoch, starting on August 21st 1999 Midnight UT
(cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
NOTE: This function will return an error if the centuries past GST time are not zero.
:rtype: int

    
##### Method `to_gst_seconds` {#anise.time.Epoch.to_gst_seconds}

>     def to_gst_seconds(
>         self,
>         /
>     )

Returns seconds past GST (Galileo) Time Epoch
:rtype: float

    
##### Method `to_isoformat` {#anise.time.Epoch.to_isoformat}

>     def to_isoformat(
>         self,
>         /
>     )

The standard ISO format of this epoch (six digits of subseconds) in the _current_ time scale, refer to <https://docs.rs/hifitime/latest/hifitime/efmt/format/struct.Format.html> for format options.
:rtype: str

    
##### Method `to_jde_et` {#anise.time.Epoch.to_jde_et}

>     def to_jde_et(
>         self,
>         /,
>         unit
>     )

:type unit: Unit
:rtype: float

    
##### Method `to_jde_et_days` {#anise.time.Epoch.to_jde_et_days}

>     def to_jde_et_days(
>         self,
>         /
>     )

Returns the Ephemeris Time JDE past epoch
:rtype: float

    
##### Method `to_jde_et_duration` {#anise.time.Epoch.to_jde_et_duration}

>     def to_jde_et_duration(
>         self,
>         /
>     )

:rtype: Duration

    
##### Method `to_jde_tai` {#anise.time.Epoch.to_jde_tai}

>     def to_jde_tai(
>         self,
>         /,
>         unit
>     )

Returns the Julian Days from epoch 01 Jan -4713 12:00 (noon) in desired Duration::Unit
:type unit: Unit
:rtype: float

    
##### Method `to_jde_tai_days` {#anise.time.Epoch.to_jde_tai_days}

>     def to_jde_tai_days(
>         self,
>         /
>     )

Returns the Julian days from epoch 01 Jan -4713, 12:00 (noon)
as explained in "Fundamentals of astrodynamics and applications", Vallado et al.
4th edition, page 182, and on [Wikipedia](https://en.wikipedia.org/wiki/Julian_day).
:rtype: float

    
##### Method `to_jde_tai_duration` {#anise.time.Epoch.to_jde_tai_duration}

>     def to_jde_tai_duration(
>         self,
>         /
>     )

Returns the Julian Days from epoch 01 Jan -4713 12:00 (noon) as a Duration
:rtype: Duration

    
##### Method `to_jde_tai_seconds` {#anise.time.Epoch.to_jde_tai_seconds}

>     def to_jde_tai_seconds(
>         self,
>         /
>     )

Returns the Julian seconds in TAI.
:rtype: float

    
##### Method `to_jde_tdb_days` {#anise.time.Epoch.to_jde_tdb_days}

>     def to_jde_tdb_days(
>         self,
>         /
>     )

Returns the Dynamic Barycentric Time (TDB) (higher fidelity SPICE ephemeris time) whose epoch is 2000 JAN 01 noon TAI (cf. <https://gssc.esa.int/navipedia/index.php/Transformations_between_Time_Systems#TDT_-_TDB.2C_TCB>)
:rtype: float

    
##### Method `to_jde_tdb_duration` {#anise.time.Epoch.to_jde_tdb_duration}

>     def to_jde_tdb_duration(
>         self,
>         /
>     )

:rtype: Duration

    
##### Method `to_jde_tt_days` {#anise.time.Epoch.to_jde_tt_days}

>     def to_jde_tt_days(
>         self,
>         /
>     )

Returns days past Julian epoch in Terrestrial Time (TT) (previously called Terrestrial Dynamical Time (TDT))
:rtype: float

    
##### Method `to_jde_tt_duration` {#anise.time.Epoch.to_jde_tt_duration}

>     def to_jde_tt_duration(
>         self,
>         /
>     )

:rtype: Duration

    
##### Method `to_jde_utc_days` {#anise.time.Epoch.to_jde_utc_days}

>     def to_jde_utc_days(
>         self,
>         /
>     )

Returns the Julian days in UTC.
:rtype: float

    
##### Method `to_jde_utc_duration` {#anise.time.Epoch.to_jde_utc_duration}

>     def to_jde_utc_duration(
>         self,
>         /
>     )

Returns the Julian days in UTC as a <code>[Duration](#anise.time.Duration "anise.time.Duration")</code>
:rtype: Duration

    
##### Method `to_jde_utc_seconds` {#anise.time.Epoch.to_jde_utc_seconds}

>     def to_jde_utc_seconds(
>         self,
>         /
>     )

Returns the Julian Days in UTC seconds.
:rtype: float

    
##### Method `to_mjd_tai` {#anise.time.Epoch.to_mjd_tai}

>     def to_mjd_tai(
>         self,
>         /,
>         unit
>     )

Returns this epoch as a duration in the requested units in MJD TAI
:type unit: Unit
:rtype: float

    
##### Method `to_mjd_tai_days` {#anise.time.Epoch.to_mjd_tai_days}

>     def to_mjd_tai_days(
>         self,
>         /
>     )

<code>as\_mjd\_days</code> creates an Epoch from the provided Modified Julian Date in days as explained
[here](http://tycho.usno.navy.mil/mjd.html). MJD epoch is Modified Julian Day at 17 November 1858 at midnight.
:rtype: float

    
##### Method `to_mjd_tai_seconds` {#anise.time.Epoch.to_mjd_tai_seconds}

>     def to_mjd_tai_seconds(
>         self,
>         /
>     )

Returns the Modified Julian Date in seconds TAI.
:rtype: float

    
##### Method `to_mjd_tt_days` {#anise.time.Epoch.to_mjd_tt_days}

>     def to_mjd_tt_days(
>         self,
>         /
>     )

Returns days past Modified Julian epoch in Terrestrial Time (TT) (previously called Terrestrial Dynamical Time (TDT))
:rtype: float

    
##### Method `to_mjd_tt_duration` {#anise.time.Epoch.to_mjd_tt_duration}

>     def to_mjd_tt_duration(
>         self,
>         /
>     )

:rtype: Duration

    
##### Method `to_mjd_utc` {#anise.time.Epoch.to_mjd_utc}

>     def to_mjd_utc(
>         self,
>         /,
>         unit
>     )

Returns the Modified Julian Date in the provided unit in UTC.
:type unit: Unit
:rtype: float

    
##### Method `to_mjd_utc_days` {#anise.time.Epoch.to_mjd_utc_days}

>     def to_mjd_utc_days(
>         self,
>         /
>     )

Returns the Modified Julian Date in days UTC.
:rtype: float

    
##### Method `to_mjd_utc_seconds` {#anise.time.Epoch.to_mjd_utc_seconds}

>     def to_mjd_utc_seconds(
>         self,
>         /
>     )

Returns the Modified Julian Date in seconds UTC.
:rtype: float

    
##### Method `to_nanoseconds_in_time_scale` {#anise.time.Epoch.to_nanoseconds_in_time_scale}

>     def to_nanoseconds_in_time_scale(
>         self,
>         /,
>         time_scale
>     )

Attempts to return the number of nanoseconds since the reference epoch of the provided time scale.
This will return an overflow error if more than one century has past since the reference epoch in the provided time scale.
If this is _not_ an issue, you should use <code>epoch.to\_duration\_in\_time\_scale().to\_parts()</code> to retrieve both the centuries and the nanoseconds
in that century.

:type time_scale: TimeScale
:rtype: int

    
##### Method `to_qzsst_days` {#anise.time.Epoch.to_qzsst_days}

>     def to_qzsst_days(
>         self,
>         /
>     )

Returns days past QZSS Time Epoch, defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).
:rtype: float

    
##### Method `to_qzsst_duration` {#anise.time.Epoch.to_qzsst_duration}

>     def to_qzsst_duration(
>         self,
>         /
>     )

Returns <code>[Duration](#anise.time.Duration "anise.time.Duration")</code> past QZSS time Epoch.
:rtype: Duration

    
##### Method `to_qzsst_nanoseconds` {#anise.time.Epoch.to_qzsst_nanoseconds}

>     def to_qzsst_nanoseconds(
>         self,
>         /
>     )

Returns nanoseconds past QZSS Time Epoch, defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).
NOTE: This function will return an error if the centuries past QZSST time are not zero.
:rtype: int

    
##### Method `to_qzsst_seconds` {#anise.time.Epoch.to_qzsst_seconds}

>     def to_qzsst_seconds(
>         self,
>         /
>     )

Returns seconds past QZSS Time Epoch, defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).
:rtype: float

    
##### Method `to_rfc3339` {#anise.time.Epoch.to_rfc3339}

>     def to_rfc3339(
>         self,
>         /
>     )

Returns this epoch in UTC in the RFC3339 format
:rtype: str

    
##### Method `to_tai` {#anise.time.Epoch.to_tai}

>     def to_tai(
>         self,
>         /,
>         unit
>     )

Returns the epoch as a floating point value in the provided unit
:type unit: Unit
:rtype: float

    
##### Method `to_tai_days` {#anise.time.Epoch.to_tai_days}

>     def to_tai_days(
>         self,
>         /
>     )

Returns the number of days since J1900 in TAI
:rtype: float

    
##### Method `to_tai_duration` {#anise.time.Epoch.to_tai_duration}

>     def to_tai_duration(
>         self,
>         /
>     )

Returns this time in a Duration past J1900 counted in TAI
:rtype: Duration

    
##### Method `to_tai_parts` {#anise.time.Epoch.to_tai_parts}

>     def to_tai_parts(
>         self,
>         /
>     )

Returns the TAI parts of this duration
:rtype: typing.Tuple

    
##### Method `to_tai_seconds` {#anise.time.Epoch.to_tai_seconds}

>     def to_tai_seconds(
>         self,
>         /
>     )

Returns the number of TAI seconds since J1900
:rtype: float

    
##### Method `to_tdb_centuries_since_j2000` {#anise.time.Epoch.to_tdb_centuries_since_j2000}

>     def to_tdb_centuries_since_j2000(
>         self,
>         /
>     )

Returns the number of centuries since Dynamic Barycentric Time (TDB) J2000 (used for Archinal et al. rotations)
:rtype: float

    
##### Method `to_tdb_days_since_j2000` {#anise.time.Epoch.to_tdb_days_since_j2000}

>     def to_tdb_days_since_j2000(
>         self,
>         /
>     )

Returns the number of days since Dynamic Barycentric Time (TDB) J2000 (used for Archinal et al. rotations)
:rtype: float

    
##### Method `to_tdb_duration` {#anise.time.Epoch.to_tdb_duration}

>     def to_tdb_duration(
>         self,
>         /
>     )

Returns the Dynamics Barycentric Time (TDB) as a high precision Duration since J2000

###### Algorithm
Given the embedded sine functions in the equation to compute the difference between TDB and TAI from the number of TDB seconds
past J2000, one cannot solve the revert the operation analytically. Instead, we iterate until the value no longer changes.

1. Assume that the TAI duration is in fact the TDB seconds from J2000.
2. Offset to J2000 because <code>[Epoch](#anise.time.Epoch "anise.time.Epoch")</code> stores everything in the J1900 but the TDB duration is in J2000.
3. Compute the offset <code>g</code> due to the TDB computation with the current value of the TDB seconds (defined in step 1).
4. Subtract that offset to the latest TDB seconds and store this as a new candidate for the true TDB seconds value.
5. Compute the difference between this candidate and the previous one. If the difference is less than one nanosecond, stop iteration.
6. Set the new candidate as the TDB seconds since J2000 and loop until step 5 breaks the loop, or we've done five iterations.
7. At this stage, we have a good approximation of the TDB seconds since J2000.
8. Reverse the algorithm given that approximation: compute the <code>g</code> offset, compute the difference between TDB and TAI, add the TT offset (32.184 s), and offset by the difference between J1900 and J2000.

:rtype: Duration

    
##### Method `to_tdb_seconds` {#anise.time.Epoch.to_tdb_seconds}

>     def to_tdb_seconds(
>         self,
>         /
>     )

Returns the Dynamic Barycentric Time (TDB) (higher fidelity SPICE ephemeris time) whose epoch is 2000 JAN 01 noon TAI (cf. <https://gssc.esa.int/navipedia/index.php/Transformations_between_Time_Systems#TDT_-_TDB.2C_TCB>)
:rtype: float

    
##### Method `to_time_of_week` {#anise.time.Epoch.to_time_of_week}

>     def to_time_of_week(
>         self,
>         /
>     )

Converts this epoch into the time of week, represented as a rolling week counter into that time scale
and the number of nanoseconds elapsed in current week (since closest Sunday midnight).
This is usually how GNSS receivers describe a timestamp.
:rtype: typing.Tuple[int]

    
##### Method `to_time_scale` {#anise.time.Epoch.to_time_scale}

>     def to_time_scale(
>         self,
>         /,
>         ts
>     )

Converts self to another time scale

As per the [Rust naming convention](https://rust-lang.github.io/api-guidelines/naming.html#ad-hoc-conversions-follow-as_-to_-into_-conventions-c-conv),
this borrows an Epoch and returns an owned Epoch.

:type ts: TimeScale
:rtype: Epoch

    
##### Method `to_tt_centuries_j2k` {#anise.time.Epoch.to_tt_centuries_j2k}

>     def to_tt_centuries_j2k(
>         self,
>         /
>     )

Returns the centuries passed J2000 TT
:rtype: float

    
##### Method `to_tt_days` {#anise.time.Epoch.to_tt_days}

>     def to_tt_days(
>         self,
>         /
>     )

Returns days past TAI epoch in Terrestrial Time (TT) (previously called Terrestrial Dynamical Time (TDT))
:rtype: float

    
##### Method `to_tt_duration` {#anise.time.Epoch.to_tt_duration}

>     def to_tt_duration(
>         self,
>         /
>     )

Returns <code>[Duration](#anise.time.Duration "anise.time.Duration")</code> past TAI epoch in Terrestrial Time (TT).
:rtype: Duration

    
##### Method `to_tt_seconds` {#anise.time.Epoch.to_tt_seconds}

>     def to_tt_seconds(
>         self,
>         /
>     )

Returns seconds past TAI epoch in Terrestrial Time (TT) (previously called Terrestrial Dynamical Time (TDT))
:rtype: float

    
##### Method `to_tt_since_j2k` {#anise.time.Epoch.to_tt_since_j2k}

>     def to_tt_since_j2k(
>         self,
>         /
>     )

Returns the duration past J2000 TT
:rtype: Duration

    
##### Method `to_unix` {#anise.time.Epoch.to_unix}

>     def to_unix(
>         self,
>         /,
>         unit
>     )

Returns the duration since the UNIX epoch in the provided unit.
:type unit: Unit
:rtype: float

    
##### Method `to_unix_days` {#anise.time.Epoch.to_unix_days}

>     def to_unix_days(
>         self,
>         /
>     )

Returns the number days since the UNIX epoch defined 01 Jan 1970 midnight UTC.
:rtype: float

    
##### Method `to_unix_duration` {#anise.time.Epoch.to_unix_duration}

>     def to_unix_duration(
>         self,
>         /
>     )

Returns the Duration since the UNIX epoch UTC midnight 01 Jan 1970.
:rtype: Duration

    
##### Method `to_unix_milliseconds` {#anise.time.Epoch.to_unix_milliseconds}

>     def to_unix_milliseconds(
>         self,
>         /
>     )

Returns the number milliseconds since the UNIX epoch defined 01 Jan 1970 midnight UTC.
:rtype: float

    
##### Method `to_unix_seconds` {#anise.time.Epoch.to_unix_seconds}

>     def to_unix_seconds(
>         self,
>         /
>     )

Returns the number seconds since the UNIX epoch defined 01 Jan 1970 midnight UTC.
:rtype: float

    
##### Method `to_utc` {#anise.time.Epoch.to_utc}

>     def to_utc(
>         self,
>         /,
>         unit
>     )

Returns the number of UTC seconds since the TAI epoch
:type unit: Unit
:rtype: float

    
##### Method `to_utc_days` {#anise.time.Epoch.to_utc_days}

>     def to_utc_days(
>         self,
>         /
>     )

Returns the number of UTC days since the TAI epoch
:rtype: float

    
##### Method `to_utc_duration` {#anise.time.Epoch.to_utc_duration}

>     def to_utc_duration(
>         self,
>         /
>     )

Returns this time in a Duration past J1900 counted in UTC
:rtype: Duration

    
##### Method `to_utc_seconds` {#anise.time.Epoch.to_utc_seconds}

>     def to_utc_seconds(
>         self,
>         /
>     )

Returns the number of UTC seconds since the TAI epoch
:rtype: float

    
##### Method `todatetime` {#anise.time.Epoch.todatetime}

>     def todatetime(
>         self,
>         /
>     )

Returns a Python datetime object from this Epoch (truncating the nanoseconds away)
:rtype: datetime.datetime

    
##### Method `weekday` {#anise.time.Epoch.weekday}

>     def weekday(
>         self,
>         /
>     )

Returns weekday (uses the TAI representation for this calculation).
:rtype: Weekday

    
##### Method `weekday_in_time_scale` {#anise.time.Epoch.weekday_in_time_scale}

>     def weekday_in_time_scale(
>         self,
>         /,
>         time_scale
>     )

Returns the weekday in provided time scale **ASSUMING** that the reference epoch of that time scale is a Monday.
You _probably_ do not want to use this. You probably either want <code>weekday()</code> or <code>weekday\_utc()</code>.
Several time scales do _not_ have a reference day that's on a Monday, e.g. BDT.
:type time_scale: TimeScale
:rtype: Weekday

    
##### Method `weekday_utc` {#anise.time.Epoch.weekday_utc}

>     def weekday_utc(
>         self,
>         /
>     )

Returns weekday in UTC timescale
:rtype: Weekday

    
##### Method `year` {#anise.time.Epoch.year}

>     def year(
>         self,
>         /
>     )

Returns the number of Gregorian years of this epoch in the current time scale.
:rtype: int

    
##### Method `year_days_of_year` {#anise.time.Epoch.year_days_of_year}

>     def year_days_of_year(
>         self,
>         /
>     )

Returns the year and the days in the year so far (days of year).
:rtype: typing.Tuple

    
### Class `HifitimeError` {#anise.time.HifitimeError}

>     class HifitimeError(
>         *args,
>         **kwargs
>     )

    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)

    
### Class `LatestLeapSeconds` {#anise.time.LatestLeapSeconds}

>     class LatestLeapSeconds

List of leap seconds from <https://www.ietf.org/timezones/data/leap-seconds.list>.
This list corresponds the number of seconds in TAI to the UTC offset and to whether it was an announced leap second or not.
The unannoucned leap seconds come from dat.c in the SOFA library.

    
### Class `LeapSecondsFile` {#anise.time.LeapSecondsFile}

>     class LeapSecondsFile(
>         path
>     )

A leap second provider that uses an IERS formatted leap seconds file.

(Python documentation hints)
:type path: str
:rtype: LeapSecondsFile

    
### Class `MonthName` {#anise.time.MonthName}

>     class MonthName(
>         ...
>     )

    
#### Class variables

    
##### Variable `April` {#anise.time.MonthName.April}

    
##### Variable `August` {#anise.time.MonthName.August}

    
##### Variable `December` {#anise.time.MonthName.December}

    
##### Variable `February` {#anise.time.MonthName.February}

    
##### Variable `January` {#anise.time.MonthName.January}

    
##### Variable `July` {#anise.time.MonthName.July}

    
##### Variable `June` {#anise.time.MonthName.June}

    
##### Variable `March` {#anise.time.MonthName.March}

    
##### Variable `May` {#anise.time.MonthName.May}

    
##### Variable `November` {#anise.time.MonthName.November}

    
##### Variable `October` {#anise.time.MonthName.October}

    
##### Variable `September` {#anise.time.MonthName.September}

    
### Class `ParsingError` {#anise.time.ParsingError}

>     class ParsingError(
>         *args,
>         **kwargs
>     )

    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)

    
### Class `Polynomial` {#anise.time.Polynomial}

>     class Polynomial(
>         ...
>     )

Interpolation [Polynomial] used for example in [TimeScale]
maintenance, precise monitoring or conversions.

(Python documentation hints)
:type constant: Duration
:type rate: Duration
:type accel: Duration
:rtype: Polynomial

    
#### Methods

    
##### Method `correction_duration` {#anise.time.Polynomial.correction_duration}

>     def correction_duration(
>         self,
>         /,
>         time_interval
>     )

Calculate the correction (as [Duration] once again) from [Self] and given
the interpolation time interval
:type time_interval: Duration
:rtype: Duration

    
##### Method `from_constant_offset` {#anise.time.Polynomial.from_constant_offset}

>     def from_constant_offset(
>         constant
>     )

Create a [Polynomial] structure that is only made of a static offset
:type constant: Duration
:rtype: Polynomial

    
##### Method `from_constant_offset_nanoseconds` {#anise.time.Polynomial.from_constant_offset_nanoseconds}

>     def from_constant_offset_nanoseconds(
>         nanos
>     )

Create a [Polynomial] structure from a static offset expressed in nanoseconds
:type nanos: float
:rtype: Polynomial

    
##### Method `from_offset_and_rate` {#anise.time.Polynomial.from_offset_and_rate}

>     def from_offset_and_rate(
>         constant,
>         rate
>     )

Create a [Polynomial] structure from both static offset and rate of change:
:type constant: Duration
:type rate: Duration
:rtype: Polynomial

    
##### Method `from_offset_rate_nanoseconds` {#anise.time.Polynomial.from_offset_rate_nanoseconds}

>     def from_offset_rate_nanoseconds(
>         offset_ns,
>         drift_ns_s
>     )

Create a [Polynomial] structure from a static offset and drift, in nanoseconds and nanoseconds.s⁻¹
:type offset_ns: float
:type drift_ns_s: float
:rtype: Polynomial

    
### Class `TimeScale` {#anise.time.TimeScale}

>     class TimeScale(
>         ...
>     )

Enum of the different time systems available

    
#### Class variables

    
##### Variable `BDT` {#anise.time.TimeScale.BDT}

    
##### Variable `ET` {#anise.time.TimeScale.ET}

    
##### Variable `GPST` {#anise.time.TimeScale.GPST}

    
##### Variable `GST` {#anise.time.TimeScale.GST}

    
##### Variable `QZSST` {#anise.time.TimeScale.QZSST}

    
##### Variable `TAI` {#anise.time.TimeScale.TAI}

    
##### Variable `TDB` {#anise.time.TimeScale.TDB}

    
##### Variable `TT` {#anise.time.TimeScale.TT}

    
##### Variable `UTC` {#anise.time.TimeScale.UTC}

    
#### Methods

    
##### Method `uses_leap_seconds` {#anise.time.TimeScale.uses_leap_seconds}

>     def uses_leap_seconds(
>         self,
>         /
>     )

Returns true if self takes leap seconds into account
:rtype: bool

    
### Class `TimeSeries` {#anise.time.TimeSeries}

>     class TimeSeries(
>         start,
>         end,
>         step,
>         inclusive
>     )

An iterator of a sequence of evenly spaced Epochs.

(Python documentation hints)
:type start: Epoch
:type end: Epoch
:type step: Duration
:type inclusive: bool
:rtype: TimeSeries

    
### Class `Unit` {#anise.time.Unit}

>     class Unit(
>         ...
>     )

An Enum to perform time unit conversions.

    
#### Class variables

    
##### Variable `Century` {#anise.time.Unit.Century}

    
##### Variable `Day` {#anise.time.Unit.Day}

    
##### Variable `Hour` {#anise.time.Unit.Hour}

    
##### Variable `Microsecond` {#anise.time.Unit.Microsecond}

    
##### Variable `Millisecond` {#anise.time.Unit.Millisecond}

    
##### Variable `Minute` {#anise.time.Unit.Minute}

    
##### Variable `Nanosecond` {#anise.time.Unit.Nanosecond}

    
##### Variable `Second` {#anise.time.Unit.Second}

    
##### Variable `Week` {#anise.time.Unit.Week}

    
#### Methods

    
##### Method `from_seconds` {#anise.time.Unit.from_seconds}

>     def from_seconds(
>         self,
>         /
>     )

    
##### Method `in_seconds` {#anise.time.Unit.in_seconds}

>     def in_seconds(
>         self,
>         /
>     )

    
### Class `Ut1Provider` {#anise.time.Ut1Provider}

>     class Ut1Provider

A structure storing all of the TAI-UT1 data

    
### Class `Weekday` {#anise.time.Weekday}

>     class Weekday(
>         ...
>     )

    
#### Class variables

    
##### Variable `Friday` {#anise.time.Weekday.Friday}

    
##### Variable `Monday` {#anise.time.Weekday.Monday}

    
##### Variable `Saturday` {#anise.time.Weekday.Saturday}

    
##### Variable `Sunday` {#anise.time.Weekday.Sunday}

    
##### Variable `Thursday` {#anise.time.Weekday.Thursday}

    
##### Variable `Tuesday` {#anise.time.Weekday.Tuesday}

    
##### Variable `Wednesday` {#anise.time.Weekday.Wednesday}

-----
Generated by *pdoc* 0.11.6 (<https://pdoc3.github.io>).
