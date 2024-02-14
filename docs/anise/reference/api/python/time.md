# Module `anise.time`

    
## Classes

    
### Class `Duration`

>     class Duration(
>         string_repr
>     )

Defines generally usable durations for nanosecond precision valid for 32,768 centuries in either direction, and only on 80 bits / 10 octets.

#### Important conventions

1. The negative durations can be mentally modeled "BC" years. One hours before 01 Jan 0000, it was "-1" years but  365 days and 23h into the current day.
It was decided that the nanoseconds corresponds to the nanoseconds _into_ the current century. In other words,
a duration with centuries = -1 and nanoseconds = 0 is _a greater duration_ (further from zero) than centuries = -1 and nanoseconds = 1.
Duration zero minus one nanosecond returns a century of -1 and a nanosecond set to the number of nanoseconds in one century minus one.
That difference is exactly 1 nanoseconds, where the former duration is "closer to zero" than the latter.
As such, the largest negative duration that can be represented sets the centuries to i16::MAX and its nanoseconds to NANOSECONDS_PER_CENTURY.
2. It was also decided that opposite durations are equal, e.g. -15 minutes == 15 minutes. If the direction of time matters, use the signum function.

    
#### Methods

    
##### Method `abs`

>     def abs(
>         self,
>         /
>     )

Returns the absolute value of this duration

    
##### Method `approx`

>     def approx(
>         self,
>         /
>     )

Rounds this duration to the largest units represented in this duration.

This is useful to provide an approximate human duration. Under the hood, this function uses <code>round</code>,
so the "tipping point" of the rounding is half way to the next increment of the greatest unit.
As shown below, one example is that 35 hours and 59 minutes rounds to 1 day, but 36 hours and 1 minute rounds
to 2 days because 2 days is closer to 36h 1 min than 36h 1 min is to 1 day.
    
##### Method `ceil`

>     def ceil(
>         self,
>         /,
>         duration
>     )

Ceils this duration to the closest provided duration

This simply floors then adds the requested duration
    
##### Method `decompose`

>     def decompose(
>         self,
>         /
>     )

Decomposes a Duration in its sign, days, hours, minutes, seconds, ms, us, ns

    
##### Method `epsilon`

>     def epsilon()

    
##### Method `floor`

>     def floor(
>         self,
>         /,
>         duration
>     )

Floors this duration to the closest duration from the bottom
    
##### Method `init_from_all_parts`

>     def init_from_all_parts(
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

    
##### Method `init_from_max`

>     def init_from_max()

    
##### Method `init_from_min`

>     def init_from_min()

    
##### Method `init_from_parts`

>     def init_from_parts(
>         centuries,
>         nanoseconds
>     )

Create a normalized duration from its parts

    
##### Method `init_from_total_nanoseconds`

>     def init_from_total_nanoseconds(
>         nanos
>     )

    
##### Method `init_from_truncated_nanoseconds`

>     def init_from_truncated_nanoseconds(
>         nanos
>     )

Create a new duration from the truncated nanoseconds (+/- 2927.1 years of duration)

    
##### Method `is_negative`

>     def is_negative(
>         self,
>         /
>     )

Returns whether this is a negative or positive duration.

    
##### Method `max`

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

_Note:_ this uses a pointer to <code>self</code> which will be copied immediately because Python requires a pointer.

    
##### Method `min`

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

_Note:_ this uses a pointer to <code>self</code> which will be copied immediately because Python requires a pointer.

    
##### Method `min_negative`

>     def min_negative()

    
##### Method `min_positive`

>     def min_positive()

    
##### Method `normalize`

>     def normalize(
>         self,
>         /
>     )

    
##### Method `round`

>     def round(
>         self,
>         /,
>         duration
>     )

Rounds this duration to the closest provided duration

This performs both a <code>ceil</code> and <code>floor</code> and returns the value which is the closest to current one.

    
##### Method `signum`

>     def signum(
>         self,
>         /
>     )

Returns the sign of this duration
+ 0 if the number is zero
+ 1 if the number is positive
+ -1 if the number is negative

    
##### Method `to_parts`

>     def to_parts(
>         self,
>         /
>     )

Returns the centuries and nanoseconds of this duration
NOTE: These items are not public to prevent incorrect durations from being created by modifying the values of the structure directly.

    
##### Method `to_seconds`

>     def to_seconds(
>         self,
>         /
>     )

Returns this duration in seconds f64.
For high fidelity comparisons, it is recommended to keep using the Duration structure.

    
##### Method `to_unit`

>     def to_unit(
>         self,
>         /,
>         unit
>     )

    
##### Method `total_nanoseconds`

>     def total_nanoseconds(
>         self,
>         /
>     )

Returns the total nanoseconds in a signed 128 bit integer

    
##### Method `truncated_nanoseconds`

>     def truncated_nanoseconds(
>         self,
>         /
>     )

Returns the truncated nanoseconds in a signed 64 bit integer, if the duration fits.
WARNING: This function will NOT fail and will return the i64::MIN or i64::MAX depending on
the sign of the centuries if the Duration does not fit on aa i64

    
##### Method `try_truncated_nanoseconds`

>     def try_truncated_nanoseconds(
>         self,
>         /
>     )

Returns the truncated nanoseconds in a signed 64 bit integer, if the duration fits.

    
##### Method `zero`

>     def zero()

    
### Class `Epoch`

>     class Epoch(
>         string_repr
>     )

Defines a nanosecond-precision Epoch.

Refer to the appropriate functions for initializing this Epoch from different time scales or representations.

    
#### Methods

    
##### Method `ceil`

>     def ceil(
>         self,
>         /,
>         duration
>     )

Ceils this epoch to the closest provided duration in the TAI time scale
    
##### Method `day_of_year`

>     def day_of_year(
>         self,
>         /
>     )

Returns the number of days since the start of the year.

    
##### Method `duration_in_year`

>     def duration_in_year(
>         self,
>         /
>     )

Returns the duration since the start of the year

    
##### Method `floor`

>     def floor(
>         self,
>         /,
>         duration
>     )

Floors this epoch to the closest provided duration

##### Method `hours`

>     def hours(
>         self,
>         /
>     )

Returns the hours of the Gregorian representation  of this epoch in the time scale it was initialized in.

    
##### Method `in_time_scale`

>     def in_time_scale(
>         self,
>         /,
>         new_time_scale
>     )

Copies this epoch and sets it to the new time scale provided.

    
##### Method `init_from_bdt_days`

>     def init_from_bdt_days(
>         days
>     )

Initialize an Epoch from the number of days since the BeiDou Time Epoch,
defined as January 1st 2006 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).

    
##### Method `init_from_bdt_nanoseconds`

>     def init_from_bdt_nanoseconds(
>         nanoseconds
>     )

Initialize an Epoch from the number of days since the BeiDou Time Epoch,
defined as January 1st 2006 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
This may be useful for time keeping devices that use BDT as a time source.

    
##### Method `init_from_bdt_seconds`

>     def init_from_bdt_seconds(
>         seconds
>     )

Initialize an Epoch from the number of seconds since the BeiDou Time Epoch,
defined as January 1st 2006 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).

    
##### Method `init_from_et_duration`

>     def init_from_et_duration(
>         duration_since_j2000
>     )

Initialize an Epoch from the Ephemeris Time duration past 2000 JAN 01 (J2000 reference)

    
##### Method `init_from_et_seconds`

>     def init_from_et_seconds(
>         seconds_since_j2000
>     )

Initialize an Epoch from the Ephemeris Time seconds past 2000 JAN 01 (J2000 reference)

    
##### Method `init_from_gpst_days`

>     def init_from_gpst_days(
>         days
>     )

Initialize an Epoch from the number of days since the GPS Time Epoch,
defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).

    
##### Method `init_from_gpst_nanoseconds`

>     def init_from_gpst_nanoseconds(
>         nanoseconds
>     )

Initialize an Epoch from the number of nanoseconds since the GPS Time Epoch,
defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).
This may be useful for time keeping devices that use GPS as a time source.

    
##### Method `init_from_gpst_seconds`

>     def init_from_gpst_seconds(
>         seconds
>     )

Initialize an Epoch from the number of seconds since the GPS Time Epoch,
defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).

    
##### Method `init_from_gregorian`

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

    
##### Method `init_from_gregorian_at_midnight`

>     def init_from_gregorian_at_midnight(
>         year,
>         month,
>         day,
>         time_scale
>     )

    
##### Method `init_from_gregorian_at_noon`

>     def init_from_gregorian_at_noon(
>         year,
>         month,
>         day,
>         time_scale
>     )

    
##### Method `init_from_gregorian_tai`

>     def init_from_gregorian_tai(
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

    
##### Method `init_from_gregorian_tai_at_midnight`

>     def init_from_gregorian_tai_at_midnight(
>         year,
>         month,
>         day
>     )

Initialize from the Gregorian date at midnight in TAI.

    
##### Method `init_from_gregorian_tai_at_noon`

>     def init_from_gregorian_tai_at_noon(
>         year,
>         month,
>         day
>     )

Initialize from the Gregorian date at noon in TAI

    
##### Method `init_from_gregorian_tai_hms`

>     def init_from_gregorian_tai_hms(
>         year,
>         month,
>         day,
>         hour,
>         minute,
>         second
>     )

Initialize from the Gregorian date and time (without the nanoseconds) in TAI

    
##### Method `init_from_gregorian_utc`

>     def init_from_gregorian_utc(
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

    
##### Method `init_from_gregorian_utc_at_midnight`

>     def init_from_gregorian_utc_at_midnight(
>         year,
>         month,
>         day
>     )

Initialize from Gregorian date in UTC at midnight

    
##### Method `init_from_gregorian_utc_at_noon`

>     def init_from_gregorian_utc_at_noon(
>         year,
>         month,
>         day
>     )

Initialize from Gregorian date in UTC at noon

    
##### Method `init_from_gregorian_utc_hms`

>     def init_from_gregorian_utc_hms(
>         year,
>         month,
>         day,
>         hour,
>         minute,
>         second
>     )

Initialize from the Gregorian date and time (without the nanoseconds) in UTC

    
##### Method `init_from_gst_days`

>     def init_from_gst_days(
>         days
>     )

Initialize an Epoch from the number of days since the Galileo Time Epoch,
starting on August 21st 1999 Midnight UT,
(cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).

    
##### Method `init_from_gst_nanoseconds`

>     def init_from_gst_nanoseconds(
>         nanoseconds
>     )

Initialize an Epoch from the number of nanoseconds since the Galileo Time Epoch,
starting on August 21st 1999 Midnight UT,
(cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
This may be useful for time keeping devices that use GST as a time source.

    
##### Method `init_from_gst_seconds`

>     def init_from_gst_seconds(
>         seconds
>     )

Initialize an Epoch from the number of seconds since the Galileo Time Epoch,
starting on August 21st 1999 Midnight UT,
(cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).

    
##### Method `init_from_jde_et`

>     def init_from_jde_et(
>         days
>     )

Initialize from the JDE days

    
##### Method `init_from_jde_tai`

>     def init_from_jde_tai(
>         days
>     )

Initialize an Epoch from given JDE in TAI time scale

    
##### Method `init_from_jde_tdb`

>     def init_from_jde_tdb(
>         days
>     )

Initialize from Dynamic Barycentric Time (TDB) (same as SPICE ephemeris time) in JD days

    
##### Method `init_from_jde_utc`

>     def init_from_jde_utc(
>         days
>     )

Initialize an Epoch from given JDE in UTC time scale

    
##### Method `init_from_mjd_tai`

>     def init_from_mjd_tai(
>         days
>     )

Initialize an Epoch from given MJD in TAI time scale

    
##### Method `init_from_mjd_utc`

>     def init_from_mjd_utc(
>         days
>     )

Initialize an Epoch from given MJD in UTC time scale

    
##### Method `init_from_tai_days`

>     def init_from_tai_days(
>         days
>     )

Initialize an Epoch from the provided TAI days since 1900 January 01 at midnight

    
##### Method `init_from_tai_duration`

>     def init_from_tai_duration(
>         duration
>     )

Creates a new Epoch from a Duration as the time difference between this epoch and TAI reference epoch.

    
##### Method `init_from_tai_parts`

>     def init_from_tai_parts(
>         centuries,
>         nanoseconds
>     )

Creates a new Epoch from its centuries and nanosecond since the TAI reference epoch.

    
##### Method `init_from_tai_seconds`

>     def init_from_tai_seconds(
>         seconds
>     )

Initialize an Epoch from the provided TAI seconds since 1900 January 01 at midnight

    
##### Method `init_from_tdb_duration`

>     def init_from_tdb_duration(
>         duration_since_j2000
>     )

Initialize from Dynamic Barycentric Time (TDB) (same as SPICE ephemeris time) whose epoch is 2000 JAN 01 noon TAI.

    
##### Method `init_from_tdb_seconds`

>     def init_from_tdb_seconds(
>         seconds_j2000
>     )

Initialize an Epoch from Dynamic Barycentric Time (TDB) seconds past 2000 JAN 01 midnight (difference than SPICE)
NOTE: This uses the ESA algorithm, which is a notch more complicated than the SPICE algorithm, but more precise.
In fact, SPICE algorithm is precise +/- 30 microseconds for a century whereas ESA algorithm should be exactly correct.

    
##### Method `init_from_tt_duration`

>     def init_from_tt_duration(
>         duration
>     )

Initialize an Epoch from the provided TT seconds (approximated to 32.184s delta from TAI)

    
##### Method `init_from_tt_seconds`

>     def init_from_tt_seconds(
>         seconds
>     )

Initialize an Epoch from the provided TT seconds (approximated to 32.184s delta from TAI)

    
##### Method `init_from_unix_milliseconds`

>     def init_from_unix_milliseconds(
>         milliseconds
>     )

Initialize an Epoch from the provided UNIX millisecond timestamp since UTC midnight 1970 January 01.

    
##### Method `init_from_unix_seconds`

>     def init_from_unix_seconds(
>         seconds
>     )

Initialize an Epoch from the provided UNIX second timestamp since UTC midnight 1970 January 01.

    
##### Method `init_from_utc_days`

>     def init_from_utc_days(
>         days
>     )

Initialize an Epoch from the provided UTC days since 1900 January 01 at midnight

    
##### Method `init_from_utc_seconds`

>     def init_from_utc_seconds(
>         seconds
>     )

Initialize an Epoch from the provided UTC seconds since 1900 January 01 at midnight

    
##### Method `isoformat`

>     def isoformat(
>         self,
>         /
>     )

Equivalent to <code>datetime.isoformat</code>, and truncated to 23 chars, refer to <https://docs.rs/hifitime/latest/hifitime/efmt/format/struct.Format.html> for format options

    
##### Method `leap_seconds`

>     def leap_seconds(
>         self,
>         /,
>         iers_only
>     )

Get the accumulated number of leap seconds up to this Epoch accounting only for the IERS leap seconds and the SOFA scaling from 1960 to 1972, depending on flag.
Returns None if the epoch is before 1960, year at which UTC was defined.

    
##### Method `leap_seconds_iers`

>     def leap_seconds_iers(
>         self,
>         /
>     )

Get the accumulated number of leap seconds up to this Epoch accounting only for the IERS leap seconds.

    
##### Method `leap_seconds_with_file`

>     def leap_seconds_with_file(
>         self,
>         /,
>         iers_only,
>         provider
>     )

Get the accumulated number of leap seconds up to this Epoch from the provided LeapSecondProvider.
Returns None if the epoch is before 1960, year at which UTC was defined.
    
##### Method `max`

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

    
##### Method `maybe_init_from_gregorian`

>     def maybe_init_from_gregorian(
>         year,
>         month,
>         day,
>         hour,
>         minute,
>         second,
>         nanos,
>         time_scale
>     )

Attempts to build an Epoch from the provided Gregorian date and time in the provided time scale.
NOTE: If the time scale is TDB, this function assumes that the SPICE format is used

    
##### Method `maybe_init_from_gregorian_tai`

>     def maybe_init_from_gregorian_tai(
>         year,
>         month,
>         day,
>         hour,
>         minute,
>         second,
>         nanos
>     )

Attempts to build an Epoch from the provided Gregorian date and time in TAI.

    
##### Method `maybe_init_from_gregorian_utc`

>     def maybe_init_from_gregorian_utc(
>         year,
>         month,
>         day,
>         hour,
>         minute,
>         second,
>         nanos
>     )

Attempts to build an Epoch from the provided Gregorian date and time in UTC.

    
##### Method `microseconds`

>     def microseconds(
>         self,
>         /
>     )

Returns the microseconds of the Gregorian representation  of this epoch in the time scale it was initialized in.

    
##### Method `milliseconds`

>     def milliseconds(
>         self,
>         /
>     )

Returns the milliseconds of the Gregorian representation  of this epoch in the time scale it was initialized in.

    
##### Method `min`

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

    
##### Method `minutes`

>     def minutes(
>         self,
>         /
>     )

Returns the minutes of the Gregorian representation  of this epoch in the time scale it was initialized in.

    
##### Method `month_name`

>     def month_name(
>         self,
>         /
>     )

    
##### Method `nanoseconds`

>     def nanoseconds(
>         self,
>         /
>     )

Returns the nanoseconds of the Gregorian representation  of this epoch in the time scale it was initialized in.

    
##### Method `next`

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

    
##### Method `next_weekday_at_midnight`

>     def next_weekday_at_midnight(
>         self,
>         /,
>         weekday
>     )

    
##### Method `next_weekday_at_noon`

>     def next_weekday_at_noon(
>         self,
>         /,
>         weekday
>     )

    
##### Method `previous`

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

    
##### Method `previous_weekday_at_midnight`

>     def previous_weekday_at_midnight(
>         self,
>         /,
>         weekday
>     )

    
##### Method `previous_weekday_at_noon`

>     def previous_weekday_at_noon(
>         self,
>         /,
>         weekday
>     )

    
##### Method `round`

>     def round(
>         self,
>         /,
>         duration
>     )

Rounds this epoch to the closest provided duration in TAI
    
##### Method `seconds`

>     def seconds(
>         self,
>         /
>     )

Returns the seconds of the Gregorian representation  of this epoch in the time scale it was initialized in.

    
##### Method `set`

>     def set(
>         self,
>         /,
>         new_duration
>     )

Makes a copy of self and sets the duration and time scale appropriately given the new duration

    
##### Method `strftime`

>     def strftime(
>         self,
>         /,
>         format_str
>     )

Equivalent to <code>datetime.strftime</code>, refer to <https://docs.rs/hifitime/latest/hifitime/efmt/format/struct.Format.html> for format options

    
##### Method `strptime`

>     def strptime(
>         epoch_str,
>         format_str
>     )

Equivalent to <code>datetime.strptime</code>, refer to <https://docs.rs/hifitime/latest/hifitime/efmt/format/struct.Format.html> for format options

    
##### Method `system_now`

>     def system_now()

    
##### Method `timedelta`

>     def timedelta(
>         self,
>         /,
>         other
>     )

    
##### Method `to_bdt_days`

>     def to_bdt_days(
>         self,
>         /
>     )

Returns days past BDT (BeiDou) Time Epoch, defined as Jan 01 2006 UTC
(cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).

    
##### Method `to_bdt_duration`

>     def to_bdt_duration(
>         self,
>         /
>     )

Returns <code>[Duration](#\_anise.time.Duration "\_anise.time.Duration")</code> past BDT (BeiDou) time Epoch.

    
##### Method `to_bdt_nanoseconds`

>     def to_bdt_nanoseconds(
>         self,
>         /
>     )

Returns nanoseconds past BDT (BeiDou) Time Epoch, defined as Jan 01 2006 UTC
(cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
NOTE: This function will return an error if the centuries past GST time are not zero.

    
##### Method `to_bdt_seconds`

>     def to_bdt_seconds(
>         self,
>         /
>     )

Returns seconds past BDT (BeiDou) Time Epoch

    
##### Method `to_duration`

>     def to_duration(
>         self,
>         /
>     )

Returns this epoch with respect to the time scale this epoch was created in.
This is needed to correctly perform duration conversions in dynamical time scales (e.g. TDB).

###### Examples
1. If an epoch was initialized as Epoch.init_from_..._utc(...) then the duration will be the UTC duration from J1900.
2. If an epoch was initialized as Epoch.init_from_..._tdb(...) then the duration will be the UTC duration from J2000 because the TDB reference epoch is J2000.

    
##### Method `to_duration_in_time_scale`

>     def to_duration_in_time_scale(
>         self,
>         /,
>         time_scale
>     )

Returns this epoch with respect to the provided time scale.
This is needed to correctly perform duration conversions in dynamical time scales (e.g. TDB).

    
##### Method `to_duration_since_j1900`

>     def to_duration_since_j1900(
>         self,
>         /
>     )

Returns this epoch in duration since J1900 in the time scale this epoch was created in.

    
##### Method `to_duration_since_j1900_in_time_scale`

>     def to_duration_since_j1900_in_time_scale(
>         self,
>         /,
>         time_scale
>     )

Returns this epoch in duration since J1900 with respect to the provided time scale.

    
##### Method `to_et_centuries_since_j2000`

>     def to_et_centuries_since_j2000(
>         self,
>         /
>     )

Returns the number of centuries since Ephemeris Time (ET) J2000 (used for Archinal et al. rotations)

    
##### Method `to_et_days_since_j2000`

>     def to_et_days_since_j2000(
>         self,
>         /
>     )

Returns the number of days since Ephemeris Time (ET) J2000 (used for Archinal et al. rotations)

    
##### Method `to_et_duration`

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

    
##### Method `to_et_duration_since_j1900`

>     def to_et_duration_since_j1900(
>         self,
>         /
>     )

Returns the Ephemeris Time in duration past 1900 JAN 01 at noon.
**Only** use this if the subsequent computation expect J1900 seconds.

    
##### Method `to_et_seconds`

>     def to_et_seconds(
>         self,
>         /
>     )

Returns the Ephemeris Time seconds past 2000 JAN 01 midnight, matches NASA/NAIF SPICE.

    
##### Method `to_gpst_days`

>     def to_gpst_days(
>         self,
>         /
>     )

Returns days past GPS Time Epoch, defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).

    
##### Method `to_gpst_duration`

>     def to_gpst_duration(
>         self,
>         /
>     )

Returns <code>[Duration](#\_anise.time.Duration "\_anise.time.Duration")</code> past GPS time Epoch.

    
##### Method `to_gpst_nanoseconds`

>     def to_gpst_nanoseconds(
>         self,
>         /
>     )

Returns nanoseconds past GPS Time Epoch, defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).
NOTE: This function will return an error if the centuries past GPST time are not zero.

    
##### Method `to_gpst_seconds`

>     def to_gpst_seconds(
>         self,
>         /
>     )

Returns seconds past GPS Time Epoch, defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).

    
##### Method `to_gregorian_str`

>     def to_gregorian_str(
>         self,
>         /,
>         time_scale
>     )

Converts the Epoch to Gregorian in the provided time scale and in the ISO8601 format with the time scale appended to the string

    
##### Method `to_gregorian_tai`

>     def to_gregorian_tai(
>         self,
>         /
>     )

Converts the Epoch to the Gregorian TAI equivalent as (year, month, day, hour, minute, second).
WARNING: Nanoseconds are lost in this conversion!

    
##### Method `to_gregorian_tai_str`

>     def to_gregorian_tai_str(
>         self,
>         /
>     )

Converts the Epoch to TAI Gregorian in the ISO8601 format with " TAI" appended to the string

    
##### Method `to_gregorian_utc`

>     def to_gregorian_utc(
>         self,
>         /
>     )

Converts the Epoch to the Gregorian UTC equivalent as (year, month, day, hour, minute, second).
WARNING: Nanoseconds are lost in this conversion!
    
##### Method `to_gregorian_utc_str`

>     def to_gregorian_utc_str(
>         self,
>         /
>     )

Converts the Epoch to UTC Gregorian in the ISO8601 format.

    
##### Method `to_gst_days`

>     def to_gst_days(
>         self,
>         /
>     )

Returns days past GST (Galileo) Time Epoch,
starting on August 21st 1999 Midnight UT
(cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).

    
##### Method `to_gst_duration`

>     def to_gst_duration(
>         self,
>         /
>     )

Returns <code>[Duration](#\_anise.time.Duration "\_anise.time.Duration")</code> past GST (Galileo) time Epoch.

    
##### Method `to_gst_nanoseconds`

>     def to_gst_nanoseconds(
>         self,
>         /
>     )

Returns nanoseconds past GST (Galileo) Time Epoch, starting on August 21st 1999 Midnight UT
(cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
NOTE: This function will return an error if the centuries past GST time are not zero.

    
##### Method `to_gst_seconds`

>     def to_gst_seconds(
>         self,
>         /
>     )

Returns seconds past GST (Galileo) Time Epoch

    
##### Method `to_isoformat`

>     def to_isoformat(
>         self,
>         /
>     )

The standard ISO format of this epoch (six digits of subseconds), refer to <https://docs.rs/hifitime/latest/hifitime/efmt/format/struct.Format.html> for format options

    
##### Method `to_jde_et`

>     def to_jde_et(
>         self,
>         /,
>         unit
>     )

    
##### Method `to_jde_et_days`

>     def to_jde_et_days(
>         self,
>         /
>     )

Returns the Ephemeris Time JDE past epoch

    
##### Method `to_jde_et_duration`

>     def to_jde_et_duration(
>         self,
>         /
>     )

    
##### Method `to_jde_tai`

>     def to_jde_tai(
>         self,
>         /,
>         unit
>     )

Returns the Julian Days from epoch 01 Jan -4713 12:00 (noon) in desired Duration::Unit

    
##### Method `to_jde_tai_days`

>     def to_jde_tai_days(
>         self,
>         /
>     )

Returns the Julian days from epoch 01 Jan -4713, 12:00 (noon)
as explained in "Fundamentals of astrodynamics and applications", Vallado et al.
4th edition, page 182, and on [Wikipedia](https://en.wikipedia.org/wiki/Julian_day).

    
##### Method `to_jde_tai_duration`

>     def to_jde_tai_duration(
>         self,
>         /
>     )

Returns the Julian Days from epoch 01 Jan -4713 12:00 (noon) as a Duration

    
##### Method `to_jde_tai_seconds`

>     def to_jde_tai_seconds(
>         self,
>         /
>     )

Returns the Julian seconds in TAI.

    
##### Method `to_jde_tdb_days`

>     def to_jde_tdb_days(
>         self,
>         /
>     )

Returns the Dynamic Barycentric Time (TDB) (higher fidelity SPICE ephemeris time) whose epoch is 2000 JAN 01 noon TAI (cf. <https://gssc.esa.int/navipedia/index.php/Transformations_between_Time_Systems#TDT_-_TDB.2C_TCB>)

    
##### Method `to_jde_tdb_duration`

>     def to_jde_tdb_duration(
>         self,
>         /
>     )

    
##### Method `to_jde_tt_days`

>     def to_jde_tt_days(
>         self,
>         /
>     )

Returns days past Julian epoch in Terrestrial Time (TT) (previously called Terrestrial Dynamical Time (TDT))

    
##### Method `to_jde_tt_duration`

>     def to_jde_tt_duration(
>         self,
>         /
>     )

    
##### Method `to_jde_utc_days`

>     def to_jde_utc_days(
>         self,
>         /
>     )

Returns the Julian days in UTC.

    
##### Method `to_jde_utc_duration`

>     def to_jde_utc_duration(
>         self,
>         /
>     )

Returns the Julian days in UTC as a <code>[Duration](#\_anise.time.Duration "\_anise.time.Duration")</code>

    
##### Method `to_jde_utc_seconds`

>     def to_jde_utc_seconds(
>         self,
>         /
>     )

Returns the Julian Days in UTC seconds.

    
##### Method `to_mjd_tai`

>     def to_mjd_tai(
>         self,
>         /,
>         unit
>     )

Returns this epoch as a duration in the requested units in MJD TAI

    
##### Method `to_mjd_tai_days`

>     def to_mjd_tai_days(
>         self,
>         /
>     )

<code>as\_mjd\_days</code> creates an Epoch from the provided Modified Julian Date in days as explained
[here](http://tycho.usno.navy.mil/mjd.html). MJD epoch is Modified Julian Day at 17 November 1858 at midnight.

    
##### Method `to_mjd_tai_seconds`

>     def to_mjd_tai_seconds(
>         self,
>         /
>     )

Returns the Modified Julian Date in seconds TAI.

    
##### Method `to_mjd_tt_days`

>     def to_mjd_tt_days(
>         self,
>         /
>     )

Returns days past Modified Julian epoch in Terrestrial Time (TT) (previously called Terrestrial Dynamical Time (TDT))

    
##### Method `to_mjd_tt_duration`

>     def to_mjd_tt_duration(
>         self,
>         /
>     )

    
##### Method `to_mjd_utc`

>     def to_mjd_utc(
>         self,
>         /,
>         unit
>     )

Returns the Modified Julian Date in the provided unit in UTC.

    
##### Method `to_mjd_utc_days`

>     def to_mjd_utc_days(
>         self,
>         /
>     )

Returns the Modified Julian Date in days UTC.

    
##### Method `to_mjd_utc_seconds`

>     def to_mjd_utc_seconds(
>         self,
>         /
>     )

Returns the Modified Julian Date in seconds UTC.

    
##### Method `to_nanoseconds_in_time_scale`

>     def to_nanoseconds_in_time_scale(
>         self,
>         /,
>         time_scale
>     )

Attempts to return the number of nanoseconds since the reference epoch of the provided time scale.
This will return an overflow error if more than one century has past since the reference epoch in the provided time scale.
If this is _not_ an issue, you should use <code>epoch.to\_duration\_in\_time\_scale().to\_parts()</code> to retrieve both the centuries and the nanoseconds
in that century.

    
##### Method `to_rfc3339`

>     def to_rfc3339(
>         self,
>         /
>     )

Returns this epoch in UTC in the RFC3339 format

    
##### Method `to_tai`

>     def to_tai(
>         self,
>         /,
>         unit
>     )

Returns the epoch as a floating point value in the provided unit

    
##### Method `to_tai_days`

>     def to_tai_days(
>         self,
>         /
>     )

Returns the number of days since J1900 in TAI

    
##### Method `to_tai_duration`

>     def to_tai_duration(
>         self,
>         /
>     )

Returns this time in a Duration past J1900 counted in TAI

    
##### Method `to_tai_parts`

>     def to_tai_parts(
>         self,
>         /
>     )

Returns the TAI parts of this duration

    
##### Method `to_tai_seconds`

>     def to_tai_seconds(
>         self,
>         /
>     )

Returns the number of TAI seconds since J1900

    
##### Method `to_tdb_centuries_since_j2000`

>     def to_tdb_centuries_since_j2000(
>         self,
>         /
>     )

Returns the number of centuries since Dynamic Barycentric Time (TDB) J2000 (used for Archinal et al. rotations)

    
##### Method `to_tdb_days_since_j2000`

>     def to_tdb_days_since_j2000(
>         self,
>         /
>     )

Returns the number of days since Dynamic Barycentric Time (TDB) J2000 (used for Archinal et al. rotations)

    
##### Method `to_tdb_duration`

>     def to_tdb_duration(
>         self,
>         /
>     )

Returns the Dynamics Barycentric Time (TDB) as a high precision Duration since J2000

###### Algorithm
Given the embedded sine functions in the equation to compute the difference between TDB and TAI from the number of TDB seconds
past J2000, one cannot solve the revert the operation analytically. Instead, we iterate until the value no longer changes.

1. Assume that the TAI duration is in fact the TDB seconds from J2000.
2. Offset to J2000 because <code>[Epoch](#\_anise.time.Epoch "\_anise.time.Epoch")</code> stores everything in the J1900 but the TDB duration is in J2000.
3. Compute the offset <code>g</code> due to the TDB computation with the current value of the TDB seconds (defined in step 1).
4. Subtract that offset to the latest TDB seconds and store this as a new candidate for the true TDB seconds value.
5. Compute the difference between this candidate and the previous one. If the difference is less than one nanosecond, stop iteration.
6. Set the new candidate as the TDB seconds since J2000 and loop until step 5 breaks the loop, or we've done five iterations.
7. At this stage, we have a good approximation of the TDB seconds since J2000.
8. Reverse the algorithm given that approximation: compute the <code>g</code> offset, compute the difference between TDB and TAI, add the TT offset (32.184 s), and offset by the difference between J1900 and J2000.

    
##### Method `to_tdb_duration_since_j1900`

>     def to_tdb_duration_since_j1900(
>         self,
>         /
>     )

Returns the Dynamics Barycentric Time (TDB) as a high precision Duration with reference epoch of 1900 JAN 01 at noon.
**Only** use this if the subsequent computation expect J1900 seconds.

    
##### Method `to_tdb_seconds`

>     def to_tdb_seconds(
>         self,
>         /
>     )

Returns the Dynamic Barycentric Time (TDB) (higher fidelity SPICE ephemeris time) whose epoch is 2000 JAN 01 noon TAI (cf. <https://gssc.esa.int/navipedia/index.php/Transformations_between_Time_Systems#TDT_-_TDB.2C_TCB>)

    
##### Method `to_time_of_week`

>     def to_time_of_week(
>         self,
>         /
>     )

Converts this epoch into the time of week, represented as a rolling week counter into that time scale
and the number of nanoseconds elapsed in current week (since closest Sunday midnight).
This is usually how GNSS receivers describe a timestamp.

    
##### Method `to_tt_centuries_j2k`

>     def to_tt_centuries_j2k(
>         self,
>         /
>     )

Returns the centuries passed J2000 TT

    
##### Method `to_tt_days`

>     def to_tt_days(
>         self,
>         /
>     )

Returns days past TAI epoch in Terrestrial Time (TT) (previously called Terrestrial Dynamical Time (TDT))

    
##### Method `to_tt_duration`

>     def to_tt_duration(
>         self,
>         /
>     )

Returns <code>[Duration](#\_anise.time.Duration "\_anise.time.Duration")</code> past TAI epoch in Terrestrial Time (TT).

    
##### Method `to_tt_seconds`

>     def to_tt_seconds(
>         self,
>         /
>     )

Returns seconds past TAI epoch in Terrestrial Time (TT) (previously called Terrestrial Dynamical Time (TDT))

    
##### Method `to_tt_since_j2k`

>     def to_tt_since_j2k(
>         self,
>         /
>     )

Returns the duration past J2000 TT

    
##### Method `to_unix`

>     def to_unix(
>         self,
>         /,
>         unit
>     )

Returns the duration since the UNIX epoch in the provided unit.

    
##### Method `to_unix_days`

>     def to_unix_days(
>         self,
>         /
>     )

Returns the number days since the UNIX epoch defined 01 Jan 1970 midnight UTC.

    
##### Method `to_unix_duration`

>     def to_unix_duration(
>         self,
>         /
>     )

Returns the Duration since the UNIX epoch UTC midnight 01 Jan 1970.

    
##### Method `to_unix_milliseconds`

>     def to_unix_milliseconds(
>         self,
>         /
>     )

Returns the number milliseconds since the UNIX epoch defined 01 Jan 1970 midnight UTC.

    
##### Method `to_unix_seconds`

>     def to_unix_seconds(
>         self,
>         /
>     )

Returns the number seconds since the UNIX epoch defined 01 Jan 1970 midnight UTC.

    
##### Method `to_ut1`

>     def to_ut1(
>         self,
>         /,
>         provider
>     )

Returns this time in a Duration past J1900 counted in UT1

    
##### Method `to_ut1_duration`

>     def to_ut1_duration(
>         self,
>         /,
>         provider
>     )

Returns this time in a Duration past J1900 counted in UT1

    
##### Method `to_utc`

>     def to_utc(
>         self,
>         /,
>         unit
>     )

Returns the number of UTC seconds since the TAI epoch

    
##### Method `to_utc_days`

>     def to_utc_days(
>         self,
>         /
>     )

Returns the number of UTC days since the TAI epoch

    
##### Method `to_utc_duration`

>     def to_utc_duration(
>         self,
>         /
>     )

Returns this time in a Duration past J1900 counted in UTC

    
##### Method `to_utc_seconds`

>     def to_utc_seconds(
>         self,
>         /
>     )

Returns the number of UTC seconds since the TAI epoch

    
##### Method `ut1_offset`

>     def ut1_offset(
>         self,
>         /,
>         provider
>     )

Get the accumulated offset between this epoch and UT1, assuming that the provider includes all data.

    
##### Method `weekday`

>     def weekday(
>         self,
>         /
>     )

Returns weekday (uses the TAI representation for this calculation).

    
##### Method `weekday_in_time_scale`

>     def weekday_in_time_scale(
>         self,
>         /,
>         time_scale
>     )

Returns the weekday in provided time scale **ASSUMING** that the reference epoch of that time scale is a Monday.
You _probably_ do not want to use this. You probably either want <code>weekday()</code> or <code>weekday\_utc()</code>.
Several time scales do _not_ have a reference day that's on a Monday, e.g. BDT.

    
##### Method `weekday_utc`

>     def weekday_utc(
>         self,
>         /
>     )

Returns weekday in UTC timescale

    
##### Method `with_hms`

>     def with_hms(
>         self,
>         /,
>         hours,
>         minutes,
>         seconds
>     )

Returns a copy of self where the time is set to the provided hours, minutes, seconds
Invalid number of hours, minutes, and seconds will overflow into their higher unit.
Warning: this does _not_ set the subdivisions of second to zero.

    
##### Method `with_hms_from`

>     def with_hms_from(
>         self,
>         /,
>         other
>     )

Returns a copy of self where the hours, minutes, seconds is set to the time of the provided epoch but the
sub-second parts are kept from the current epoch.

```
use hifitime::prelude::*;

let epoch = Epoch::from_gregorian_utc(2022, 12, 01, 10, 11, 12, 13);
let other_utc = Epoch::from_gregorian_utc(2024, 12, 01, 20, 21, 22, 23);
let other = other_utc.in_time_scale(TimeScale::TDB);

assert_eq!(
    epoch.with_hms_from(other),
    Epoch::from_gregorian_utc(2022, 12, 01, 20, 21, 22, 13)
);
```

    
##### Method `with_hms_strict`

>     def with_hms_strict(
>         self,
>         /,
>         hours,
>         minutes,
>         seconds
>     )

Returns a copy of self where the time is set to the provided hours, minutes, seconds
Invalid number of hours, minutes, and seconds will overflow into their higher unit.
Warning: this will set the subdivisions of seconds to zero.

    
##### Method `with_hms_strict_from`

>     def with_hms_strict_from(
>         self,
>         /,
>         other
>     )

Returns a copy of self where the time is set to the time of the other epoch but the subseconds are set to zero.

```
use hifitime::prelude::*;

let epoch = Epoch::from_gregorian_utc(2022, 12, 01, 10, 11, 12, 13);
let other_utc = Epoch::from_gregorian_utc(2024, 12, 01, 20, 21, 22, 23);
let other = other_utc.in_time_scale(TimeScale::TDB);

assert_eq!(
    epoch.with_hms_strict_from(other),
    Epoch::from_gregorian_utc(2022, 12, 01, 20, 21, 22, 0)
);
```

    
##### Method `with_time_from`

>     def with_time_from(
>         self,
>         /,
>         other
>     )

Returns a copy of self where all of the time components (hours, minutes, seconds, and sub-seconds) are set to the time of the provided epoch.

```
use hifitime::prelude::*;

let epoch = Epoch::from_gregorian_utc(2022, 12, 01, 10, 11, 12, 13);
let other_utc = Epoch::from_gregorian_utc(2024, 12, 01, 20, 21, 22, 23);
// If the other Epoch is in another time scale, it does not matter, it will be converted to the correct time scale.
let other = other_utc.in_time_scale(TimeScale::TDB);

assert_eq!(
    epoch.with_time_from(other),
    Epoch::from_gregorian_utc(2022, 12, 01, 20, 21, 22, 23)
);
```

    
##### Method `year`

>     def year(
>         self,
>         /
>     )

Returns the number of Gregorian years of this epoch in the current time scale.

    
##### Method `year_days_of_year`

>     def year_days_of_year(
>         self,
>         /
>     )

Returns the year and the days in the year so far (days of year).

    
### Class `LatestLeapSeconds`

>     class LatestLeapSeconds

List of leap seconds from <https://www.ietf.org/timezones/data/leap-seconds.list> .
This list corresponds the number of seconds in TAI to the UTC offset and to whether it was an announced leap second or not.
The unannoucned leap seconds come from dat.c in the SOFA library.

    
### Class `LeapSecondsFile`

>     class LeapSecondsFile(
>         path
>     )

A leap second provider that uses an IERS formatted leap seconds file.

    
### Class `TimeScale`

>     class TimeScale(
>         ...
>     )

Enum of the different time systems available

    
#### Class variables

    
##### Variable `BDT`

    
##### Variable `ET`

    
##### Variable `GPST`

    
##### Variable `GST`

    
##### Variable `TAI`

    
##### Variable `TDB`

    
##### Variable `TT`

    
##### Variable `UTC`

    
#### Methods

    
##### Method `uses_leap_seconds`

>     def uses_leap_seconds(
>         self,
>         /
>     )

Returns true if self takes leap seconds into account

    
### Class `TimeSeries`

>     class TimeSeries(
>         start,
>         end,
>         step,
>         inclusive
>     )

An iterator of a sequence of evenly spaced Epochs.

    
### Class `Unit`

>     class Unit(
>         ...
>     )

An Enum to perform time unit conversions.

    
#### Class variables

    
##### Variable `Century`

    
##### Variable `Day`

    
##### Variable `Hour`

    
##### Variable `Microsecond`

    
##### Variable `Millisecond`

    
##### Variable `Minute`

    
##### Variable `Nanosecond`

    
##### Variable `Second`

    
#### Methods

    
##### Method `from_seconds`

>     def from_seconds(
>         self,
>         /
>     )

    
##### Method `in_seconds`

>     def in_seconds(
>         self,
>         /
>     )

    
### Class `Ut1Provider`

>     class Ut1Provider

A structure storing all of the TAI-UT1 data

-----
Generated by *pdoc* 0.10.0 (<https://pdoc3.github.io>).
