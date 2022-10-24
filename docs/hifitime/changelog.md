## 3.6.0
+ Galileo System Time and BeiDou Time are now supported, huge thanks to [@gwbres](https://github.com/gwbres) for all that work!
+ Significant speed improvement in the initialization of Epochs from their Gregorian representation, thanks [@conradludgate](https://github.com/conradludgate) for [#160](https://github.com/nyx-space/hifitime/pull/160).
+ Epoch and Duration now have a `min` and `max` function which respectively returns a copy of the epoch/duration that is the smallest or the largest between `self` and `other`, cf. [#164](https://github.com/nyx-space/hifitime/issues/164).
+ [Python] Duration and Epochs now support the operators `>`, `>=`, `<`, `<=`, `==`, and `!=`. Epoch now supports `init_from_gregorian` with a time scape, like in Rust. Epochs can also be subtracted from one another using the `timedelta` function, cf. [#162](https://github.com/nyx-space/hifitime/issues/162).
+ TimeSeries can now be formatted in different time scales, cf. [#163](https://github.com/nyx-space/hifitime/issues/163)

## 3.5.0
+ Epoch now store the time scale that they were defined in: this allows durations to be added in their respective time scales. For example, adding 36 hours to 1971-12-31 at noon when the Epoch is initialized in UTC will lead to a different epoch than adding that same duration to an epoch initialized at the same time in TAI (because the first leap second announced by IERS was on 1972-01-01), cf. the `test_add_durations_over_leap_seconds` test.
+ RFC3339 and ISO8601 fully supported for initialization of an Epoch, including the offset, e.g. `Epoch::from_str("1994-11-05T08:15:30-05:00")`, cf. [#73](https://github.com/nyx-space/hifitime/issues/73).
+ Python package available on PyPI! To build the Python package, you must first install `maturin` and then build with the `python` feature flag. For example, `maturin develop -F python && python` will build the Python package in debug mode and start a new shell where the package can be imported.
+ Fix bug when printing Duration::MIN (or any duration whose centuries are minimizing the number of centuries).
+ TimeSeries can now be formatted
+ Epoch can now be `ceil`-ed, `floor`-ed, and `round`-ed according to the time scale they were initialized in, cf. [#145](https://github.com/nyx-space/hifitime/issues/145).
+ Epoch can now be initialized from Gregorian when specifying the time system: `from_gregorian`, `from_gregorian_hms`, `from_gregorian_at_noon`, `from_gregorian_at_midnight`.
+ Fix bug in Duration when performing operations on durations very close to `Duration::MIN` (i.e. minus thirty-two centuries).
+ Duration parsing now supports multiple units in a string and does not use regular expressions. THis allows it to work with `no-std`.
+ Epoch parsing no longer requires `regex`.
+ Functions are not more idiomatic: all of the `as_*` functions become `to_*` and `in_*` also becomes `to_*`, cf.  [#155](https://github.com/nyx-space/hifitime/issues/155).

## 3.4.0
+ Ephemeris Time and Dynamical Barycentric Time fixed to use the J2000 reference epoch instead of the J1900 reference epoch. This is a **potentially breaking change** if you relied on the previous one century error when converting from/to ET/TDB into/from UTC _and storing the data as a string_. There is **no difference** if the original representation was used.
+ Ephemeris Time now **strictly** matches NAIF SPICE: **the error between SPICE and hifitime is now zero nanoseconds.** after the introduction of the first leap second. Prior to the first leap second, NAIF SPICE claims that there were nine seconds of difference between TAI and UTC: this is different from SOFA. Hifitime instead does not account for leap seconds in prehistoric (pre-1972) computations at all.
+ The [_Standard of Fundamentals of Astronomy_ (SOFA)](https://www.iausofa.org/2021_0512_C.html) leap seconds from 1960 to 1972 are now available with the `leap_seconds() -> Option<f64>` function on an instance of Epoch. **Importantly**, no difference in the behavior of hifitime should be noticed here: the prehistoric leap seconds are ignored in all calculations in hifitime and only provided to meet the SOFA calculations.
+ `Epoch` and `Duration` now have the C memory representation to allow for hifitime to be embedded in C more easily.
+ `Epoch` and `Duration` can now be encoded or decoded as ASN1 DER with the `asn1der` crate feature (disabled by default).

## 3.3.0
+ Formal verification of the normalization operation on `Duration`, which in turn guarantees that `Epoch` operations cannot panic, cf. [#127](https://github.com/nyx-space/hifitime/issues/127)
+ Fix `len` and `size_hint` for `TimeSeries`, cf. [#131](https://github.com/nyx-space/hifitime/issues/131), reported by [@d3v-null](https://github.com/d3v-null), thanks for the find!
+ `Epoch` now implements `Eq` and `Ord`, cf. [#133](https://github.com/nyx-space/hifitime/pull/133), thanks [@mkolopanis](https://github.com/mkolopanis) for the PR!
+ `Epoch` can now be printed in different time systems with format modifiers, cf. [#130](https://github.com/nyx-space/hifitime/issues/130)
+ (minor) `as_utc_duration` in `Epoch` is now public, cf. [#129](https://github.com/nyx-space/hifitime/issues/129)
+ (minor) The whole crate now uses `num-traits` thereby skipping the explicit use of `libm`. Basically, operations on `f64` look like normal Rust again, cf. [#128](https://github.com/nyx-space/hifitime/issues/128)
+ (minor) Move the tests to their own folder to make it obvious that this is thoroughly tested

## 3.2.0
+ Fix no-std implementation by using `libm` for non-core f64 operations
+ Add UNIX timestamp, thanks [@mkolopanis](https://github.com/mkolopanis)
+ Enums now derive `Eq` and some derive `Ord` (where relevant) [#118](https://github.com/nyx-space/hifitime/issues/118)
+ Use const fn where possible and switch to references where possible [#119](https://github.com/nyx-space/hifitime/issues/119)
+ Allow extracting the centuries and nanoseconds of a `Duration` and `Epoch`, respectively with to_parts and to_tai_parts [#122](https://github.com/nyx-space/hifitime/issues/122)
+ Add `ceil`, `floor`, `round` operations to `Epoch` and `Duration`
## 3.1.0
+ Add `#![no_std]` support
+ Add `to_parts` to `Duration` to extract the centuries and nanoseconds of a duration
+ Allow building an `Epoch` from its duration and parts in TAI system
+ Add pure nanosecond (`u64`) constructor and getter for GPST since GPS based clocks will count in nanoseconds
### Possibly breaking change
+ `Errors::ParseError` no longer contains a `String` but an enum `ParsingErrors` instead. This is considered possibly breaking because it would only break code in the cases where a datetime parsing or unit parsing was caught and handled (uncommon). Moreover, the output is still `Display`-able.
## 3.0.0
+ Backend rewritten from TwoFloat to a struct of the centuries in `i16` and nanoseconds in `u64`. Thanks to [@pwnorbitals](https://github.com/pwnorbitals) for proposing the idea in #[107](https://github.com/nyx-space/hifitime/issues/107) and writing the proof of concept. This leads to at least a 2x speed up in most calculations, cf. [this comment](https://github.com/nyx-space/hifitime/pull/107#issuecomment-1040702004).
+ Fix GPS epoch, and addition of a helper functions in `Epoch` by [@cjordan](https://github.com/cjordan)