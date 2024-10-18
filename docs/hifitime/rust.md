This user guide focuses on typical usage of hifitime in Rust. You may find the API documentation [here](https://docs.rs/hifitime/).

## Usage

Put this in your `Cargo.toml`:

```toml
[dependencies]
hifitime = "4"
```

Then at the top of each source file, just add the following line:

```rust
use hifitime::prelude::*;
```

### Compile-time features

By default, the `std` feature is enabled. Practically, this enables functions that return a `String` type, like `to_rfc3339()`. It also allows interoperability with the standard library, such as the creation of a UTC epoch from the system time (`Epoch::now()`) and the conversion of a hifitime `Duration` into a (less precise) `std::time::Duration`. This also enables deserializing epochs and duration with the `serde` crate.

!!! important
    The `std` feature is _not_ required for parsing datetimes, even from the RFC3339 format.

Optional features:

+ `ut1`: enables the UT1 time scale, the only true time with respect to the stars
+ `python`: this feature must be enabled to build the Python bindings

## Epoch initialization

### From a string representation in RFC3339

!!! note
    1. All of the following initializations correspond to 05 November 1994 at 13 hours 15 minutes and thirty seconds UTC.
    1. All of the `from_str` initialization may fail, and therefore they return a `Result` type. These examples are also part of the test suite, so we can safely `unwrap` them because we know they won't fail.

Epochs can be initialized from the string representation in RFC3339 ...

```rust
let epoch = Epoch::from_str("1994-11-05T13:15:30Z").unwrap();
```

Where the time delimiter `T` can be replaced by a space ... 

```rust
let epoch = Epoch::from_str("1994-11-05 13:15:30Z").unwrap();
```

Where the UTC identifier `Z` can be omitted (defaults to UTC):

```rust
let epoch = Epoch::from_str("1994-11-05 13:15:30").unwrap();
```

Or with an offset from UTC:

```rust
let epoch = Epoch::from_str("1994-11-05T08:15:30-05:00").unwrap();
```

### From a string in a specific time scale

You may also specify a time scale if the RFC3339 representation should be in another time scale that UTC. Just append the time scale in uppercase to the string.

```rust
let epoch_tt = Epoch::from_str("2022-09-06T23:25:38.184000000 TT").unwrap();
let epoch_et = Epoch::from_str("2022-09-06T23:25:38.182538909 ET").unwrap();
let epoch_tdb = Epoch::from_str("2022-09-06T23:25:38.182541259 TDB").unwrap();
```

!!! important
    The TDB and ET initialization use a Newton Raphson iteration scheme to correctly compute the time offset from TAI. This causes an error of a few nanoseconds when initialized from a string.

### From a string in SPICE format

NAIF SPICE supports Modified Julian Days and Seconds representation past J2000, and so does hifitime.

```rust
let epoch = Epoch::from_str("SEC 66312032.18493909 TDB").unwrap();
```

### From an exact Gregorian date time

Either by specifying every element down to the nanosecond:

```rust
let epoch_utc = Epoch::from_gregorian_utc(1983, 4, 13, 12, 9, 14, 274_000_000);
let epoch_tai = Epoch::from_gregorian_tai(1983, 4, 13, 12, 9, 14, 274_000_000);
```

Or stopping at the seconds:

```rust
let epoch_tai = Epoch::from_gregorian_tai_hms(1983, 4, 13, 12, 9, 14);
```

You may also specify the Gregorian epoch in one of the supported time scales:

```rust
let epoch = Epoch::from_gregorian(2017, 1, 14, 0, 31, 55, 811000000, TimeScale::TT);
```

Also optionally without the nanoseconds:

```rust
assert_eq!(
    Epoch::from_gregorian_hms(1994, 11, 5, 13, 15, 30, TimeScale::TDB),
    Epoch::from_str("1994-11-05T13:15:30Z TDB").unwrap()
);
```

### From a date at noon or midnight

Initializations at [noon](https://docs.rs/hifitime/latest/hifitime/?search=noon) and at [midnight](https://docs.rs/hifitime/latest/hifitime/?search=midnight) are also available.

```rust
let epoch = Epoch::from_gregorian_utc_at_noon(1972, 1, 1);
let epoch = Epoch::from_gregorian_utc_at_midnight(1972, 1, 1);
```

### From an exact number of days or seconds past the reference epoch of the time scale

+ TDB and ET initializations can be done with either the seconds only or the fully qualified `Duration`, respectively with the `from_et_seconds`, `from_tdb_seconds`, `from_et_duration`, and `from_tdb_duration`.
+ Same thing for the TAI and TT time scales.
+ Modified Julian Dates and Julian Dates can also be initialized with their days in UTC or TAI using [these functions](https://docs.rs/hifitime/latest/hifitime/?search=from_mjd).
+ Julian Dates can also be initialized with days past the Julian reference epoch in UTC, TAI, TDB, or ET time scales using [these functions](https://docs.rs/hifitime/latest/hifitime/?search=from_jde).
+ GPS clocks often store the number of ticks in nanoseconds, and hifitime also supports this with the `from_gpst_nanoseconds` function. If you only have the days or seconds, you can use the `from_gpst_days` or `from_gpst_seconds` initialization functions.

All of the initialization functions start with [`from_`](https://docs.rs/hifitime/latest/hifitime/?search=from_).

## Converting into another time scale

One of the main use cases of hifitime is converting between time scales. As of version 4, simply call `to_time_scale` on an epoch with the desired time scale as a parameter. This will return a copy of the original Epoch converted into the time scale of your choice.

## Epoch arithmetics

You can easily check whether an epoch is before or after another one with the `>` and `<` operators.

```rust
// Noon UTC after the first leap second is in fact ten seconds _after_ noon TAI.
// Hence, there are as many TAI seconds since Epoch between UTC Noon and TAI Noon + 10s.
assert!(
    Epoch::from_gregorian_utc_at_noon(1972, 1, 1)
        > Epoch::from_gregorian_tai_at_noon(1972, 1, 1)
);
```

The arithmetics on Epochs are done in the time scales used at initialization. For example, adding 10 seconds to an epoch defined in the TAI time scale will lead to a different epoch than adding 10 seconds to an epoch defined in the ET time scale (because ET is a dynamical time scale where one second in ET is not the same as one second in TDB).

### Epoch differences

Comparing times will lead to a Duration type. Printing that will automatically select which units to print.

```rust
let at_midnight = Epoch::from_gregorian_utc_at_midnight(2020, 11, 2);
let at_noon = Epoch::from_gregorian_utc_at_noon(2020, 11, 2);

assert_eq!(at_noon - at_midnight, 12 * Unit::Hour);
assert_eq!(at_noon - at_midnight, 1 * Unit::Day / 2);
assert_eq!(at_midnight - at_noon, -1.days() / 2);

let delta_time = at_noon - at_midnight;
assert_eq!(format!("{}", delta_time), "12 h".to_string());
```

And we can multiply or divide durations by a scalar...

```rust
// Continued from above
let delta2 = 2 * delta_time;
assert_eq!(format!("{}", delta2), "1 days".to_string());

assert_eq!(format!("{}", delta2 / 2.0), "12 h".to_string());
```

And of course, these comparisons account for differences in time scales    

```rust
let at_midnight_utc = Epoch::from_gregorian_utc_at_midnight(2020, 11, 2);
let at_noon_tai = Epoch::from_gregorian_tai_at_noon(2020, 11, 2);
assert_eq!(format!("{}", at_noon_tai - at_midnight_utc), "11 h 59 min 23 s".to_string());
```

### Arithmetics in different time scales

Noon UTC after the first leap second is in fact ten seconds _after_ noon TAI. Hence, there are as many TAI seconds since Epoch between UTC Noon and TAI Noon + 10s.

```rust
let pre_ls_utc = Epoch::from_gregorian_utc_at_noon(1971, 12, 31);
let pre_ls_tai = pre_ls_utc.to_time_scale(TimeScale::TAI);
```

Before the first leap second, there is no time difference between both epochs (because only IERS announced leap seconds are accounted for by default).

```rust
// Continued from above
assert_eq!(pre_ls_utc - pre_ls_tai, Duration::ZERO);
```

When add 24 hours to either of the them, the UTC initialized epoch will increase the duration by 36 hours in UTC, which will cause a leap second jump. Therefore the difference between both epochs then becomes 10 seconds.

```rust
// Continued from above
assert_eq!(
    (pre_ls_utc + 1 * Unit::Day) - (pre_ls_tai + 1 * Unit::Day),
    10 * Unit::Second
);
```

Of course this works the same way the other way around

```rust
let post_ls_utc = pre_ls_utc + Unit::Day;
let post_ls_tai = pre_ls_tai + Unit::Day;
assert_eq!(
    (post_ls_utc - Unit::Day) - (post_ls_tai - Unit::Day),
    Duration::ZERO
);
```

## Duration initializations, time units, and frequency units

Time units and frequency units are trivially supported. Hifitime only supports up to nanosecond precision (but guarantees it for 64 millennia), so any duration less than one nanosecond is truncated.

### Initialization

A Duration can be initialized from a `i64` integer or an `f64` floating point values by simply suffixing it with one of the following units defined in [TimeUnits](https://docs.rs/hifitime/latest/hifitime/trait.TimeUnits.html):

+ `.centuries()`
+ `.days()`
+ `.hours()`
+ `.minutes()`
+ `.seconds()`
+ `.milliseconds()`
+ `.microseconds()`
+ `.nanoseconds()`

```rust
let d_10s = 10.seconds();
let d_10_5us = 10.5.microseconds();
```

Or by multiplying an `i64` or `f64` with a [`Unit`](https://docs.rs/hifitime/latest/hifitime/enum.Unit.html):

```rust
let d_10s = 10 * Unit::Second;
let d_10_5us = 10.5 * Unit::Microsecond;
```

### End to end example

```rust
// One can compare durations
assert!(10.seconds() > 5.seconds());
assert!(10.days() + 1.nanoseconds() > 10.days());

// Those durations are more precise than floating point since this is integer math in nanoseconds
let d: Duration = 1.0.hours() / 3 - 20.minutes();
assert!(d.abs() < Unit::Nanosecond);
assert_eq!(3 * 20.minutes(), Unit::Hour);

// And also frequencies but note that frequencies are converted to Durations!
// So the duration of that frequency is compared, hence the following:
assert!(10 * Freq::Hertz < 5 * Freq::Hertz);
assert!(4 * Freq::MegaHertz > 5 * Freq::MegaHertz);

// And asserts on the units themselves
assert!(Freq::GigaHertz < Freq::MegaHertz);
assert!(Unit::Second > Unit::Millisecond);
```

## Iterating over epochs with TimeSeries ("linspace" of epochs)

Finally, something which may come in very handy, line spaces between times with a given step.

```rust
let start = Epoch::from_gregorian_utc_at_midnight(2017, 1, 14);
let end = Epoch::from_gregorian_utc_at_noon(2017, 1, 14);
let step = 2 * Unit::Hour;
let time_series = TimeSeries::inclusive(start, end, step);
for epoch in time_series {
    // Will print 2017-01-14 at midnight, 2am, 4am, 6am, 8am, 10am, and noon.
    println!("{}", epoch);
}
```