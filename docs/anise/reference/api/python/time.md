Module _anise.time
==================

Classes
-------

`Duration(string_repr)`
:   Defines generally usable durations for nanosecond precision valid for 32,768 centuries in either direction, and only on 80 bits / 10 octets.
    
    **Important conventions:**
    1. The negative durations can be mentally modeled "BC" years. One hours before 01 Jan 0000, it was "-1" years but  365 days and 23h into the current day.
    It was decided that the nanoseconds corresponds to the nanoseconds _into_ the current century. In other words,
    a duration with centuries = -1 and nanoseconds = 0 is _a greater duration_ (further from zero) than centuries = -1 and nanoseconds = 1.
    Duration zero minus one nanosecond returns a century of -1 and a nanosecond set to the number of nanoseconds in one century minus one.
    That difference is exactly 1 nanoseconds, where the former duration is "closer to zero" than the latter.
    As such, the largest negative duration that can be represented sets the centuries to i16::MAX and its nanoseconds to NANOSECONDS_PER_CENTURY.
    2. It was also decided that opposite durations are equal, e.g. -15 minutes == 15 minutes. If the direction of time matters, use the signum function.

    ### Methods

    `abs(self, /)`
    :   Returns the absolute value of this duration

    `approx(self, /)`
    :   Rounds this duration to the largest units represented in this duration.
        
        This is useful to provide an approximate human duration. Under the hood, this function uses `round`,
        so the "tipping point" of the rounding is half way to the next increment of the greatest unit.
        As shown below, one example is that 35 hours and 59 minutes rounds to 1 day, but 36 hours and 1 minute rounds
        to 2 days because 2 days is closer to 36h 1 min than 36h 1 min is to 1 day.
        
        # Example
        
        ```
        use hifitime::{Duration, TimeUnits};
        
        assert_eq!((2.hours() + 3.minutes()).approx(), 2.hours());
        assert_eq!((24.hours() + 3.minutes()).approx(), 1.days());
        assert_eq!((35.hours() + 59.minutes()).approx(), 1.days());
        assert_eq!((36.hours() + 1.minutes()).approx(), 2.days());
        assert_eq!((47.hours() + 3.minutes()).approx(), 2.days());
        assert_eq!((49.hours() + 3.minutes()).approx(), 2.days());
        ```

    `ceil(self, /, duration)`
    :   Ceils this duration to the closest provided duration
        
        This simply floors then adds the requested duration
        
        # Example
        ```
        use hifitime::{Duration, TimeUnits};
        
        let two_hours_three_min = 2.hours() + 3.minutes();
        assert_eq!(two_hours_three_min.ceil(1.hours()), 3.hours());
        assert_eq!(two_hours_three_min.ceil(30.minutes()), 2.hours() + 30.minutes());
        assert_eq!(two_hours_three_min.ceil(4.hours()), 4.hours());
        assert_eq!(two_hours_three_min.ceil(1.seconds()), two_hours_three_min + 1.seconds());
        assert_eq!(two_hours_three_min.ceil(1.hours() + 5.minutes()), 2.hours() + 10.minutes());
        ```

    `decompose(self, /)`
    :   Decomposes a Duration in its sign, days, hours, minutes, seconds, ms, us, ns

    `epsilon()`
    :

    `floor(self, /, duration)`
    :   Floors this duration to the closest duration from the bottom
        
        # Example
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

    `init_from_all_parts(sign, days, hours, minutes, seconds, milliseconds, microseconds, nanoseconds)`
    :   Creates a new duration from its parts

    `init_from_max()`
    :

    `init_from_min()`
    :

    `init_from_parts(centuries, nanoseconds)`
    :   Create a normalized duration from its parts

    `init_from_total_nanoseconds(nanos)`
    :

    `init_from_truncated_nanoseconds(nanos)`
    :   Create a new duration from the truncated nanoseconds (+/- 2927.1 years of duration)

    `is_negative(self, /)`
    :   Returns whether this is a negative or positive duration.

    `max(self, /, other)`
    :   Returns the maximum of the two durations.
        
        ```
        use hifitime::TimeUnits;
        
        let d0 = 20.seconds();
        let d1 = 21.seconds();
        
        assert_eq!(d1, d1.max(d0));
        assert_eq!(d1, d0.max(d1));
        ```
        
        _Note:_ this uses a pointer to `self` which will be copied immediately because Python requires a pointer.

    `min(self, /, other)`
    :   Returns the minimum of the two durations.
        
        ```
        use hifitime::TimeUnits;
        
        let d0 = 20.seconds();
        let d1 = 21.seconds();
        
        assert_eq!(d0, d1.min(d0));
        assert_eq!(d0, d0.min(d1));
        ```
        
        _Note:_ this uses a pointer to `self` which will be copied immediately because Python requires a pointer.

    `min_negative()`
    :

    `min_positive()`
    :

    `normalize(self, /)`
    :

    `round(self, /, duration)`
    :   Rounds this duration to the closest provided duration
        
        This performs both a `ceil` and `floor` and returns the value which is the closest to current one.
        # Example
        ```
        use hifitime::{Duration, TimeUnits};
        
        let two_hours_three_min = 2.hours() + 3.minutes();
        assert_eq!(two_hours_three_min.round(1.hours()), 2.hours());
        assert_eq!(two_hours_three_min.round(30.minutes()), 2.hours());
        assert_eq!(two_hours_three_min.round(4.hours()), 4.hours());
        assert_eq!(two_hours_three_min.round(1.seconds()), two_hours_three_min);
        assert_eq!(two_hours_three_min.round(1.hours() + 5.minutes()), 2.hours() + 10.minutes());
        ```

    `signum(self, /)`
    :   Returns the sign of this duration
        + 0 if the number is zero
        + 1 if the number is positive
        + -1 if the number is negative

    `to_parts(self, /)`
    :   Returns the centuries and nanoseconds of this duration
        NOTE: These items are not public to prevent incorrect durations from being created by modifying the values of the structure directly.

    `to_seconds(self, /)`
    :   Returns this duration in seconds f64.
        For high fidelity comparisons, it is recommended to keep using the Duration structure.

    `to_unit(self, /, unit)`
    :

    `total_nanoseconds(self, /)`
    :   Returns the total nanoseconds in a signed 128 bit integer

    `truncated_nanoseconds(self, /)`
    :   Returns the truncated nanoseconds in a signed 64 bit integer, if the duration fits.
        WARNING: This function will NOT fail and will return the i64::MIN or i64::MAX depending on
        the sign of the centuries if the Duration does not fit on aa i64

    `try_truncated_nanoseconds(self, /)`
    :   Returns the truncated nanoseconds in a signed 64 bit integer, if the duration fits.

    `zero()`
    :

`Epoch(string_repr)`
:   Defines a nanosecond-precision Epoch.
    
    Refer to the appropriate functions for initializing this Epoch from different time scales or representations.

    ### Methods

    `ceil(self, /, duration)`
    :   Ceils this epoch to the closest provided duration in the TAI time scale
        
        # Example
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

    `day_of_year(self, /)`
    :   Returns the number of days since the start of the year.

    `duration_in_year(self, /)`
    :   Returns the duration since the start of the year

    `floor(self, /, duration)`
    :   Floors this epoch to the closest provided duration
        
        # Example
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

    `hours(self, /)`
    :   Returns the hours of the Gregorian representation  of this epoch in the time scale it was initialized in.

    `in_time_scale(self, /, new_time_scale)`
    :   Copies this epoch and sets it to the new time scale provided.

    `init_from_bdt_days(days)`
    :   Initialize an Epoch from the number of days since the BeiDou Time Epoch,
        defined as January 1st 2006 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).

    `init_from_bdt_nanoseconds(nanoseconds)`
    :   Initialize an Epoch from the number of days since the BeiDou Time Epoch,
        defined as January 1st 2006 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
        This may be useful for time keeping devices that use BDT as a time source.

    `init_from_bdt_seconds(seconds)`
    :   Initialize an Epoch from the number of seconds since the BeiDou Time Epoch,
        defined as January 1st 2006 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).

    `init_from_et_duration(duration_since_j2000)`
    :   Initialize an Epoch from the Ephemeris Time duration past 2000 JAN 01 (J2000 reference)

    `init_from_et_seconds(seconds_since_j2000)`
    :   Initialize an Epoch from the Ephemeris Time seconds past 2000 JAN 01 (J2000 reference)

    `init_from_gpst_days(days)`
    :   Initialize an Epoch from the number of days since the GPS Time Epoch,
        defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).

    `init_from_gpst_nanoseconds(nanoseconds)`
    :   Initialize an Epoch from the number of nanoseconds since the GPS Time Epoch,
        defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).
        This may be useful for time keeping devices that use GPS as a time source.

    `init_from_gpst_seconds(seconds)`
    :   Initialize an Epoch from the number of seconds since the GPS Time Epoch,
        defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).

    `init_from_gregorian(year, month, day, hour, minute, second, nanos, time_scale)`
    :

    `init_from_gregorian_at_midnight(year, month, day, time_scale)`
    :

    `init_from_gregorian_at_noon(year, month, day, time_scale)`
    :

    `init_from_gregorian_tai(year, month, day, hour, minute, second, nanos)`
    :   Builds an Epoch from the provided Gregorian date and time in TAI. If invalid date is provided, this function will panic.
        Use maybe_from_gregorian_tai if unsure.

    `init_from_gregorian_tai_at_midnight(year, month, day)`
    :   Initialize from the Gregorian date at midnight in TAI.

    `init_from_gregorian_tai_at_noon(year, month, day)`
    :   Initialize from the Gregorian date at noon in TAI

    `init_from_gregorian_tai_hms(year, month, day, hour, minute, second)`
    :   Initialize from the Gregorian date and time (without the nanoseconds) in TAI

    `init_from_gregorian_utc(year, month, day, hour, minute, second, nanos)`
    :   Builds an Epoch from the provided Gregorian date and time in TAI. If invalid date is provided, this function will panic.
        Use maybe_from_gregorian_tai if unsure.

    `init_from_gregorian_utc_at_midnight(year, month, day)`
    :   Initialize from Gregorian date in UTC at midnight

    `init_from_gregorian_utc_at_noon(year, month, day)`
    :   Initialize from Gregorian date in UTC at noon

    `init_from_gregorian_utc_hms(year, month, day, hour, minute, second)`
    :   Initialize from the Gregorian date and time (without the nanoseconds) in UTC

    `init_from_gst_days(days)`
    :   Initialize an Epoch from the number of days since the Galileo Time Epoch,
        starting on August 21st 1999 Midnight UT,
        (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).

    `init_from_gst_nanoseconds(nanoseconds)`
    :   Initialize an Epoch from the number of nanoseconds since the Galileo Time Epoch,
        starting on August 21st 1999 Midnight UT,
        (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
        This may be useful for time keeping devices that use GST as a time source.

    `init_from_gst_seconds(seconds)`
    :   Initialize an Epoch from the number of seconds since the Galileo Time Epoch,
        starting on August 21st 1999 Midnight UT,
        (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).

    `init_from_jde_et(days)`
    :   Initialize from the JDE days

    `init_from_jde_tai(days)`
    :   Initialize an Epoch from given JDE in TAI time scale

    `init_from_jde_tdb(days)`
    :   Initialize from Dynamic Barycentric Time (TDB) (same as SPICE ephemeris time) in JD days

    `init_from_jde_utc(days)`
    :   Initialize an Epoch from given JDE in UTC time scale

    `init_from_mjd_tai(days)`
    :   Initialize an Epoch from given MJD in TAI time scale

    `init_from_mjd_utc(days)`
    :   Initialize an Epoch from given MJD in UTC time scale

    `init_from_tai_days(days)`
    :   Initialize an Epoch from the provided TAI days since 1900 January 01 at midnight

    `init_from_tai_duration(duration)`
    :   Creates a new Epoch from a Duration as the time difference between this epoch and TAI reference epoch.

    `init_from_tai_parts(centuries, nanoseconds)`
    :   Creates a new Epoch from its centuries and nanosecond since the TAI reference epoch.

    `init_from_tai_seconds(seconds)`
    :   Initialize an Epoch from the provided TAI seconds since 1900 January 01 at midnight

    `init_from_tdb_duration(duration_since_j2000)`
    :   Initialize from Dynamic Barycentric Time (TDB) (same as SPICE ephemeris time) whose epoch is 2000 JAN 01 noon TAI.

    `init_from_tdb_seconds(seconds_j2000)`
    :   Initialize an Epoch from Dynamic Barycentric Time (TDB) seconds past 2000 JAN 01 midnight (difference than SPICE)
        NOTE: This uses the ESA algorithm, which is a notch more complicated than the SPICE algorithm, but more precise.
        In fact, SPICE algorithm is precise +/- 30 microseconds for a century whereas ESA algorithm should be exactly correct.

    `init_from_tt_duration(duration)`
    :   Initialize an Epoch from the provided TT seconds (approximated to 32.184s delta from TAI)

    `init_from_tt_seconds(seconds)`
    :   Initialize an Epoch from the provided TT seconds (approximated to 32.184s delta from TAI)

    `init_from_unix_milliseconds(milliseconds)`
    :   Initialize an Epoch from the provided UNIX millisecond timestamp since UTC midnight 1970 January 01.

    `init_from_unix_seconds(seconds)`
    :   Initialize an Epoch from the provided UNIX second timestamp since UTC midnight 1970 January 01.

    `init_from_utc_days(days)`
    :   Initialize an Epoch from the provided UTC days since 1900 January 01 at midnight

    `init_from_utc_seconds(seconds)`
    :   Initialize an Epoch from the provided UTC seconds since 1900 January 01 at midnight

    `isoformat(self, /)`
    :   Equivalent to `datetime.isoformat`, and truncated to 23 chars, refer to <https://docs.rs/hifitime/latest/hifitime/efmt/format/struct.Format.html> for format options

    `leap_seconds(self, /, iers_only)`
    :   Get the accumulated number of leap seconds up to this Epoch accounting only for the IERS leap seconds and the SOFA scaling from 1960 to 1972, depending on flag.
        Returns None if the epoch is before 1960, year at which UTC was defined.
        
        # Why does this function return an `Option` when the other returns a value
        This is to match the `iauDat` function of SOFA (src/dat.c). That function will return a warning and give up if the start date is before 1960.

    `leap_seconds_iers(self, /)`
    :   Get the accumulated number of leap seconds up to this Epoch accounting only for the IERS leap seconds.

    `leap_seconds_with_file(self, /, iers_only, provider)`
    :   Get the accumulated number of leap seconds up to this Epoch from the provided LeapSecondProvider.
        Returns None if the epoch is before 1960, year at which UTC was defined.
        
        # Why does this function return an `Option` when the other returns a value
        This is to match the `iauDat` function of SOFA (src/dat.c). That function will return a warning and give up if the start date is before 1960.

    `max(self, /, other)`
    :   Returns the maximum of the two epochs.
        
        ```
        use hifitime::Epoch;
        
        let e0 = Epoch::from_gregorian_utc_at_midnight(2022, 10, 20);
        let e1 = Epoch::from_gregorian_utc_at_midnight(2022, 10, 21);
        
        assert_eq!(e1, e1.max(e0));
        assert_eq!(e1, e0.max(e1));
        ```
        
        _Note:_ this uses a pointer to `self` which will be copied immediately because Python requires a pointer.

    `maybe_init_from_gregorian(year, month, day, hour, minute, second, nanos, time_scale)`
    :   Attempts to build an Epoch from the provided Gregorian date and time in the provided time scale.
        NOTE: If the time scale is TDB, this function assumes that the SPICE format is used

    `maybe_init_from_gregorian_tai(year, month, day, hour, minute, second, nanos)`
    :   Attempts to build an Epoch from the provided Gregorian date and time in TAI.

    `maybe_init_from_gregorian_utc(year, month, day, hour, minute, second, nanos)`
    :   Attempts to build an Epoch from the provided Gregorian date and time in UTC.

    `microseconds(self, /)`
    :   Returns the microseconds of the Gregorian representation  of this epoch in the time scale it was initialized in.

    `milliseconds(self, /)`
    :   Returns the milliseconds of the Gregorian representation  of this epoch in the time scale it was initialized in.

    `min(self, /, other)`
    :   Returns the minimum of the two epochs.
        
        ```
        use hifitime::Epoch;
        
        let e0 = Epoch::from_gregorian_utc_at_midnight(2022, 10, 20);
        let e1 = Epoch::from_gregorian_utc_at_midnight(2022, 10, 21);
        
        assert_eq!(e0, e1.min(e0));
        assert_eq!(e0, e0.min(e1));
        ```
        
        _Note:_ this uses a pointer to `self` which will be copied immediately because Python requires a pointer.

    `minutes(self, /)`
    :   Returns the minutes of the Gregorian representation  of this epoch in the time scale it was initialized in.

    `month_name(self, /)`
    :

    `nanoseconds(self, /)`
    :   Returns the nanoseconds of the Gregorian representation  of this epoch in the time scale it was initialized in.

    `next(self, /, weekday)`
    :   Returns the next weekday.
        
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

    `next_weekday_at_midnight(self, /, weekday)`
    :

    `next_weekday_at_noon(self, /, weekday)`
    :

    `previous(self, /, weekday)`
    :   Returns the next weekday.
        
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

    `previous_weekday_at_midnight(self, /, weekday)`
    :

    `previous_weekday_at_noon(self, /, weekday)`
    :

    `round(self, /, duration)`
    :   Rounds this epoch to the closest provided duration in TAI
        
        # Example
        ```
        use hifitime::{Epoch, TimeUnits};
        
        let e = Epoch::from_gregorian_tai_hms(2022, 5, 20, 17, 57, 43);
        assert_eq!(
            e.round(1.hours()),
            Epoch::from_gregorian_tai_hms(2022, 5, 20, 18, 0, 0)
        );
        ```

    `seconds(self, /)`
    :   Returns the seconds of the Gregorian representation  of this epoch in the time scale it was initialized in.

    `set(self, /, new_duration)`
    :   Makes a copy of self and sets the duration and time scale appropriately given the new duration

    `strftime(self, /, format_str)`
    :   Equivalent to `datetime.strftime`, refer to <https://docs.rs/hifitime/latest/hifitime/efmt/format/struct.Format.html> for format options

    `strptime(epoch_str, format_str)`
    :   Equivalent to `datetime.strptime`, refer to <https://docs.rs/hifitime/latest/hifitime/efmt/format/struct.Format.html> for format options

    `system_now()`
    :

    `timedelta(self, /, other)`
    :

    `to_bdt_days(self, /)`
    :   Returns days past BDT (BeiDou) Time Epoch, defined as Jan 01 2006 UTC
        (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).

    `to_bdt_duration(self, /)`
    :   Returns `Duration` past BDT (BeiDou) time Epoch.

    `to_bdt_nanoseconds(self, /)`
    :   Returns nanoseconds past BDT (BeiDou) Time Epoch, defined as Jan 01 2006 UTC
        (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
        NOTE: This function will return an error if the centuries past GST time are not zero.

    `to_bdt_seconds(self, /)`
    :   Returns seconds past BDT (BeiDou) Time Epoch

    `to_duration(self, /)`
    :   Returns this epoch with respect to the time scale this epoch was created in.
        This is needed to correctly perform duration conversions in dynamical time scales (e.g. TDB).
        
        # Examples
        1. If an epoch was initialized as Epoch::from_..._utc(...) then the duration will be the UTC duration from J1900.
        2. If an epoch was initialized as Epoch::from_..._tdb(...) then the duration will be the UTC duration from J2000 because the TDB reference epoch is J2000.

    `to_duration_in_time_scale(self, /, time_scale)`
    :   Returns this epoch with respect to the provided time scale.
        This is needed to correctly perform duration conversions in dynamical time scales (e.g. TDB).

    `to_duration_since_j1900(self, /)`
    :   Returns this epoch in duration since J1900 in the time scale this epoch was created in.

    `to_duration_since_j1900_in_time_scale(self, /, time_scale)`
    :   Returns this epoch in duration since J1900 with respect to the provided time scale.

    `to_et_centuries_since_j2000(self, /)`
    :   Returns the number of centuries since Ephemeris Time (ET) J2000 (used for Archinal et al. rotations)

    `to_et_days_since_j2000(self, /)`
    :   Returns the number of days since Ephemeris Time (ET) J2000 (used for Archinal et al. rotations)

    `to_et_duration(self, /)`
    :   Returns the duration between J2000 and the current epoch as per NAIF SPICE.
        
        # Warning
        The et2utc function of NAIF SPICE will assume that there are 9 leap seconds before 01 JAN 1972,
        as this date introduces 10 leap seconds. At the time of writing, this does _not_ seem to be in
        line with IERS and the documentation in the leap seconds list.
        
        In order to match SPICE, the as_et_duration() function will manually get rid of that difference.

    `to_et_duration_since_j1900(self, /)`
    :   Returns the Ephemeris Time in duration past 1900 JAN 01 at noon.
        **Only** use this if the subsequent computation expect J1900 seconds.

    `to_et_seconds(self, /)`
    :   Returns the Ephemeris Time seconds past 2000 JAN 01 midnight, matches NASA/NAIF SPICE.

    `to_gpst_days(self, /)`
    :   Returns days past GPS Time Epoch, defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).

    `to_gpst_duration(self, /)`
    :   Returns `Duration` past GPS time Epoch.

    `to_gpst_nanoseconds(self, /)`
    :   Returns nanoseconds past GPS Time Epoch, defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).
        NOTE: This function will return an error if the centuries past GPST time are not zero.

    `to_gpst_seconds(self, /)`
    :   Returns seconds past GPS Time Epoch, defined as UTC midnight of January 5th to 6th 1980 (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS#GPS_Time_.28GPST.29>).

    `to_gregorian_str(self, /, time_scale)`
    :   Converts the Epoch to Gregorian in the provided time scale and in the ISO8601 format with the time scale appended to the string

    `to_gregorian_tai(self, /)`
    :   Converts the Epoch to the Gregorian TAI equivalent as (year, month, day, hour, minute, second).
        WARNING: Nanoseconds are lost in this conversion!
        
        # Example
        ```
        use hifitime::Epoch;
        let dt = Epoch::from_gregorian_tai_at_midnight(1972, 1, 1);
        let (y, m, d, h, min, s, _) = dt.to_gregorian_tai();
        assert_eq!(y, 1972);
        assert_eq!(m, 1);
        assert_eq!(d, 1);
        assert_eq!(h, 0);
        assert_eq!(min, 0);
        assert_eq!(s, 0);
        ```

    `to_gregorian_tai_str(self, /)`
    :   Converts the Epoch to TAI Gregorian in the ISO8601 format with " TAI" appended to the string

    `to_gregorian_utc(self, /)`
    :   Converts the Epoch to the Gregorian UTC equivalent as (year, month, day, hour, minute, second).
        WARNING: Nanoseconds are lost in this conversion!
        
        # Example
        ```
        use hifitime::Epoch;
        
        let dt = Epoch::from_tai_parts(1, 537582752000000000);
        
        // With the std feature, you may use FromStr as such
        // let dt_str = "2017-01-14T00:31:55 UTC";
        // let dt = Epoch::from_gregorian_str(dt_str).unwrap()
        
        let (y, m, d, h, min, s, _) = dt.as_gregorian_utc();
        assert_eq!(y, 2017);
        assert_eq!(m, 1);
        assert_eq!(d, 14);
        assert_eq!(h, 0);
        assert_eq!(min, 31);
        assert_eq!(s, 55);
        #[cfg(feature = "std")]
        assert_eq!("2017-01-14T00:31:55 UTC", dt.as_gregorian_utc_str().to_owned());
        ```

    `to_gregorian_utc_str(self, /)`
    :   Converts the Epoch to UTC Gregorian in the ISO8601 format.

    `to_gst_days(self, /)`
    :   Returns days past GST (Galileo) Time Epoch,
        starting on August 21st 1999 Midnight UT
        (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).

    `to_gst_duration(self, /)`
    :   Returns `Duration` past GST (Galileo) time Epoch.

    `to_gst_nanoseconds(self, /)`
    :   Returns nanoseconds past GST (Galileo) Time Epoch, starting on August 21st 1999 Midnight UT
        (cf. <https://gssc.esa.int/navipedia/index.php/Time_References_in_GNSS>).
        NOTE: This function will return an error if the centuries past GST time are not zero.

    `to_gst_seconds(self, /)`
    :   Returns seconds past GST (Galileo) Time Epoch

    `to_isoformat(self, /)`
    :   The standard ISO format of this epoch (six digits of subseconds), refer to <https://docs.rs/hifitime/latest/hifitime/efmt/format/struct.Format.html> for format options

    `to_jde_et(self, /, unit)`
    :

    `to_jde_et_days(self, /)`
    :   Returns the Ephemeris Time JDE past epoch

    `to_jde_et_duration(self, /)`
    :

    `to_jde_tai(self, /, unit)`
    :   Returns the Julian Days from epoch 01 Jan -4713 12:00 (noon) in desired Duration::Unit

    `to_jde_tai_days(self, /)`
    :   Returns the Julian days from epoch 01 Jan -4713, 12:00 (noon)
        as explained in "Fundamentals of astrodynamics and applications", Vallado et al.
        4th edition, page 182, and on [Wikipedia](https://en.wikipedia.org/wiki/Julian_day).

    `to_jde_tai_duration(self, /)`
    :   Returns the Julian Days from epoch 01 Jan -4713 12:00 (noon) as a Duration

    `to_jde_tai_seconds(self, /)`
    :   Returns the Julian seconds in TAI.

    `to_jde_tdb_days(self, /)`
    :   Returns the Dynamic Barycentric Time (TDB) (higher fidelity SPICE ephemeris time) whose epoch is 2000 JAN 01 noon TAI (cf. <https://gssc.esa.int/navipedia/index.php/Transformations_between_Time_Systems#TDT_-_TDB.2C_TCB>)

    `to_jde_tdb_duration(self, /)`
    :

    `to_jde_tt_days(self, /)`
    :   Returns days past Julian epoch in Terrestrial Time (TT) (previously called Terrestrial Dynamical Time (TDT))

    `to_jde_tt_duration(self, /)`
    :

    `to_jde_utc_days(self, /)`
    :   Returns the Julian days in UTC.

    `to_jde_utc_duration(self, /)`
    :   Returns the Julian days in UTC as a `Duration`

    `to_jde_utc_seconds(self, /)`
    :   Returns the Julian Days in UTC seconds.

    `to_mjd_tai(self, /, unit)`
    :   Returns this epoch as a duration in the requested units in MJD TAI

    `to_mjd_tai_days(self, /)`
    :   `as_mjd_days` creates an Epoch from the provided Modified Julian Date in days as explained
        [here](http://tycho.usno.navy.mil/mjd.html). MJD epoch is Modified Julian Day at 17 November 1858 at midnight.

    `to_mjd_tai_seconds(self, /)`
    :   Returns the Modified Julian Date in seconds TAI.

    `to_mjd_tt_days(self, /)`
    :   Returns days past Modified Julian epoch in Terrestrial Time (TT) (previously called Terrestrial Dynamical Time (TDT))

    `to_mjd_tt_duration(self, /)`
    :

    `to_mjd_utc(self, /, unit)`
    :   Returns the Modified Julian Date in the provided unit in UTC.

    `to_mjd_utc_days(self, /)`
    :   Returns the Modified Julian Date in days UTC.

    `to_mjd_utc_seconds(self, /)`
    :   Returns the Modified Julian Date in seconds UTC.

    `to_nanoseconds_in_time_scale(self, /, time_scale)`
    :   Attempts to return the number of nanoseconds since the reference epoch of the provided time scale.
        This will return an overflow error if more than one century has past since the reference epoch in the provided time scale.
        If this is _not_ an issue, you should use `epoch.to_duration_in_time_scale().to_parts()` to retrieve both the centuries and the nanoseconds
        in that century.

    `to_rfc3339(self, /)`
    :   Returns this epoch in UTC in the RFC3339 format

    `to_tai(self, /, unit)`
    :   Returns the epoch as a floating point value in the provided unit

    `to_tai_days(self, /)`
    :   Returns the number of days since J1900 in TAI

    `to_tai_duration(self, /)`
    :   Returns this time in a Duration past J1900 counted in TAI

    `to_tai_parts(self, /)`
    :   Returns the TAI parts of this duration

    `to_tai_seconds(self, /)`
    :   Returns the number of TAI seconds since J1900

    `to_tdb_centuries_since_j2000(self, /)`
    :   Returns the number of centuries since Dynamic Barycentric Time (TDB) J2000 (used for Archinal et al. rotations)

    `to_tdb_days_since_j2000(self, /)`
    :   Returns the number of days since Dynamic Barycentric Time (TDB) J2000 (used for Archinal et al. rotations)

    `to_tdb_duration(self, /)`
    :   Returns the Dynamics Barycentric Time (TDB) as a high precision Duration since J2000
        
        ## Algorithm
        Given the embedded sine functions in the equation to compute the difference between TDB and TAI from the number of TDB seconds
        past J2000, one cannot solve the revert the operation analytically. Instead, we iterate until the value no longer changes.
        
        1. Assume that the TAI duration is in fact the TDB seconds from J2000.
        2. Offset to J2000 because `Epoch` stores everything in the J1900 but the TDB duration is in J2000.
        3. Compute the offset `g` due to the TDB computation with the current value of the TDB seconds (defined in step 1).
        4. Subtract that offset to the latest TDB seconds and store this as a new candidate for the true TDB seconds value.
        5. Compute the difference between this candidate and the previous one. If the difference is less than one nanosecond, stop iteration.
        6. Set the new candidate as the TDB seconds since J2000 and loop until step 5 breaks the loop, or we've done five iterations.
        7. At this stage, we have a good approximation of the TDB seconds since J2000.
        8. Reverse the algorithm given that approximation: compute the `g` offset, compute the difference between TDB and TAI, add the TT offset (32.184 s), and offset by the difference between J1900 and J2000.

    `to_tdb_duration_since_j1900(self, /)`
    :   Returns the Dynamics Barycentric Time (TDB) as a high precision Duration with reference epoch of 1900 JAN 01 at noon.
        **Only** use this if the subsequent computation expect J1900 seconds.

    `to_tdb_seconds(self, /)`
    :   Returns the Dynamic Barycentric Time (TDB) (higher fidelity SPICE ephemeris time) whose epoch is 2000 JAN 01 noon TAI (cf. <https://gssc.esa.int/navipedia/index.php/Transformations_between_Time_Systems#TDT_-_TDB.2C_TCB>)

    `to_time_of_week(self, /)`
    :   Converts this epoch into the time of week, represented as a rolling week counter into that time scale
        and the number of nanoseconds elapsed in current week (since closest Sunday midnight).
        This is usually how GNSS receivers describe a timestamp.

    `to_tt_centuries_j2k(self, /)`
    :   Returns the centuries passed J2000 TT

    `to_tt_days(self, /)`
    :   Returns days past TAI epoch in Terrestrial Time (TT) (previously called Terrestrial Dynamical Time (TDT))

    `to_tt_duration(self, /)`
    :   Returns `Duration` past TAI epoch in Terrestrial Time (TT).

    `to_tt_seconds(self, /)`
    :   Returns seconds past TAI epoch in Terrestrial Time (TT) (previously called Terrestrial Dynamical Time (TDT))

    `to_tt_since_j2k(self, /)`
    :   Returns the duration past J2000 TT

    `to_unix(self, /, unit)`
    :   Returns the duration since the UNIX epoch in the provided unit.

    `to_unix_days(self, /)`
    :   Returns the number days since the UNIX epoch defined 01 Jan 1970 midnight UTC.

    `to_unix_duration(self, /)`
    :   Returns the Duration since the UNIX epoch UTC midnight 01 Jan 1970.

    `to_unix_milliseconds(self, /)`
    :   Returns the number milliseconds since the UNIX epoch defined 01 Jan 1970 midnight UTC.

    `to_unix_seconds(self, /)`
    :   Returns the number seconds since the UNIX epoch defined 01 Jan 1970 midnight UTC.

    `to_ut1(self, /, provider)`
    :   Returns this time in a Duration past J1900 counted in UT1

    `to_ut1_duration(self, /, provider)`
    :   Returns this time in a Duration past J1900 counted in UT1

    `to_utc(self, /, unit)`
    :   Returns the number of UTC seconds since the TAI epoch

    `to_utc_days(self, /)`
    :   Returns the number of UTC days since the TAI epoch

    `to_utc_duration(self, /)`
    :   Returns this time in a Duration past J1900 counted in UTC

    `to_utc_seconds(self, /)`
    :   Returns the number of UTC seconds since the TAI epoch

    `ut1_offset(self, /, provider)`
    :   Get the accumulated offset between this epoch and UT1, assuming that the provider includes all data.

    `weekday(self, /)`
    :   Returns weekday (uses the TAI representation for this calculation).

    `weekday_in_time_scale(self, /, time_scale)`
    :   Returns the weekday in provided time scale **ASSUMING** that the reference epoch of that time scale is a Monday.
        You _probably_ do not want to use this. You probably either want `weekday()` or `weekday_utc()`.
        Several time scales do _not_ have a reference day that's on a Monday, e.g. BDT.

    `weekday_utc(self, /)`
    :   Returns weekday in UTC timescale

    `with_hms(self, /, hours, minutes, seconds)`
    :   Returns a copy of self where the time is set to the provided hours, minutes, seconds
        Invalid number of hours, minutes, and seconds will overflow into their higher unit.
        Warning: this does _not_ set the subdivisions of second to zero.

    `with_hms_from(self, /, other)`
    :   Returns a copy of self where the hours, minutes, seconds is set to the time of the provided epoch but the
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

    `with_hms_strict(self, /, hours, minutes, seconds)`
    :   Returns a copy of self where the time is set to the provided hours, minutes, seconds
        Invalid number of hours, minutes, and seconds will overflow into their higher unit.
        Warning: this will set the subdivisions of seconds to zero.

    `with_hms_strict_from(self, /, other)`
    :   Returns a copy of self where the time is set to the time of the other epoch but the subseconds are set to zero.
        
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

    `with_time_from(self, /, other)`
    :   Returns a copy of self where all of the time components (hours, minutes, seconds, and sub-seconds) are set to the time of the provided epoch.
        
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

    `year(self, /)`
    :   Returns the number of Gregorian years of this epoch in the current time scale.

    `year_days_of_year(self, /)`
    :   Returns the year and the days in the year so far (days of year).

`LatestLeapSeconds()`
:   List of leap seconds from https://www.ietf.org/timezones/data/leap-seconds.list .
    This list corresponds the number of seconds in TAI to the UTC offset and to whether it was an announced leap second or not.
    The unannoucned leap seconds come from dat.c in the SOFA library.

`LeapSecondsFile(path)`
:   A leap second provider that uses an IERS formatted leap seconds file.

`TimeScale(...)`
:   Enum of the different time systems available

    ### Class variables

    `BDT`
    :

    `ET`
    :

    `GPST`
    :

    `GST`
    :

    `TAI`
    :

    `TDB`
    :

    `TT`
    :

    `UTC`
    :

    ### Methods

    `uses_leap_seconds(self, /)`
    :   Returns true if self takes leap seconds into account

`TimeSeries(start, end, step, inclusive)`
:   An iterator of a sequence of evenly spaced Epochs.

`Unit(...)`
:   An Enum to perform time unit conversions.

    ### Class variables

    `Century`
    :

    `Day`
    :

    `Hour`
    :

    `Microsecond`
    :

    `Millisecond`
    :

    `Minute`
    :

    `Nanosecond`
    :

    `Second`
    :

    ### Methods

    `from_seconds(self, /)`
    :

    `in_seconds(self, /)`
    :

`Ut1Provider()`
:   A structure storing all of the TAI-UT1 data