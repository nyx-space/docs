ANISE relies on [Hifitime](../../hifitime/index.md) for all of its time and duration computations. This ensures exactly one nanosecond precision in all time-related calculations, crucial for astrodynamics. Conversion between time systems is particularly important in the case of SPICE binary files, as epochs in these files are in Ephemeris Time (ET), a time scale whose tick rate is different than Earth based clocks. 

This integration is particularly significant when compared to the SPICE toolkit, which relies on double-precision floating-point numbers (doubles) for time representations. This approach in SPICE can lead to rounding errors, a limitation not encountered in Hifitime. Hifitime's design exclusively utilizes integers for all time computations, effectively eliminating the risk of rounding errors. 

This distinction becomes particularly evident when dealing with PCK (Planetary Constants Kernel) data. The PCK data, sourced from IAU Reports, includes angle, angle rate, and angle acceleration data, all expressed in terms of days or centuries past the J2000 reference epoch. This is where users might notice notable differences between ANISE and SPICE outputs. The high fidelity of Hifitime's time representation minimizes discrepancies in these transformations, **enabling ANISE to provide more reliable results than SPICE for IAU body fixed rotation**.

For an explanation on time scales and details on Hifitime, please refer to [this page](../../hifitime/index.md).

## Re-exported from ANISE

ANISE re-exports Hifitime as-is for convenience to avoid adding a package to your set up.

=== "Python"

    ``` sh
    from anise.time import *
    ```

=== "Rust"

    ``` sh
    use anise::time::*;
    ```

_Note:_ In Python, you must use the ex-exports instead of the Hifitime classes imported from the `hifitime` package because the Python interpreter does not know that both classes are in fact identical.