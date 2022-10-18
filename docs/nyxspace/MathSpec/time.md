# Time management

Space applications require high fidelity time compution, including time systems that ignore the relativistic effects due to the gravity of the Earth (TDB).

All time computation is handled by [hifitime](https://crates.io/crates/hifitime), also written by Chris Rabotin. This library computes all time using lossless fractions with a numerator stored as an unsigned integer on 128 bits and a denominator stored as a 16 bit unsigned integer: conversion into a 64 bit floating point value happens only on request at the end of the time conversion. As such, **hifitime is quite possibly the most precise time computation library in the world.**

[![Build Status](https://api.travis-ci.com/nyx-space/hifitime.svg?branch=master)](https://app.travis-ci.com/nyx-space/hifitime)
[![hifitime on crates.io](https://img.shields.io/crates/v/hifitime.svg)](https://crates.io/crates/hifitime)
[![hifitime on docs.rs](https://docs.rs/hifitime/badge.svg)](https://docs.rs/hifitime/)

??? check "Validation"
    Validation is done using NASA's SPICE toolkit, and specifically the [spiceypy](https://spiceypy.readthedocs.io/) Python wrapper.

    The most challenging validation is the definition of Ephemeris Time, which is very nearly the same as the Dynamic Barycentric Time (TDB).
    These calculations in hifitime are from [ESA's Navipedia](https://gssc.esa.int/navipedia/index.php/Transformations_between_Time_Systems#TDT_-_TDB.2C_TCB).
    
    Hifitime uses a fixed offset for the computation of Ephemeris Time, as is recommended in Navipedia. For TDB however, the offset is based on the centuries since J2000 TT and therefore time varying.
    I believe that SPICE uses TDB for all dates after J2000 TT. Hence, in the following validation, we will be comparing the SPICE ET with the Hifitime TDB.
    
    The following examples are executed as part of the standard test suite (cf. the function called `spice_et_tdb`).
    
    ## Validation case 1
    In SPICE, we chose to convert the UTC date `2012-02-07 11:22:33 UTC` into Ephemeris Time. SPICE responds with `381885819.18493587`.
    Initializing the same UTC date in hifitime and requesting the TDB leads to `381885819.18493646`, which is an error of **596.05 nanoseconds**.
    
    ## Validation case 2
    In SPICE, we chose to convert the UTC date `2002-02-07 00:00:00.000 UTC` into Ephemeris Time. SPICE responds with `66312064.18493876`.
    Initializing the same UTC date in hifitime and requesting the TDB leads to a difference **618.39 nanoseconds**.
    
    ## Validation case 3
    This tests that we can correctly compute TDB time which will have a negative number of days because the UTC input is prior to J2000 TT.
    In SPICE, we chose to convert the UTC date `1996-02-07 11:22:33 UTC` into Ephemeris Time. SPICE responds with `-123035784.81506048`.
    Initializing the same UTC date in hifitime and requesting the TDB leads to a difference **610.94 nanoseconds**.
    
    ## Validation case 4
    In SPICE, we chose to convert the UTC date `2015-02-07 00:00:00.000 UTC` into Ephemeris Time. SPICE responds with `476580220.1849411`.
    Initializing the same UTC date in hifitime and requesting the TDB leads to a difference **596.05 nanoseconds**.
    
    ## Validation case 5
    In SPICE, we chose to convert the TDB Julian Date in days `2452312.500372511` into Ephemeris Time, and initialize a Hifitime Epoch with that result (`66312032.18493909`).
    We then convert that epoch back into **days** of Julian Date TDB and Julian Date ET, both of which lead a difference **below machine precision** on a f64 (the equivalent of a double in C/C++).

## Features
+ Leap seconds
+ Time systems: TAI, UTC, TT, TDB, ET, GPST
+ Time and duration conversions: from nanoseconds to day
+ Time zones: none but GMT, time zones are complicated.
+ Time series: allow creating an iterator between two epochs at a specific step (similar to Numpy's `linspace` but with times and epochs).

## Storage
`Epoch`s are defined as a `Duration` past a reference epoch in TAI. The reference epoch is always J1900. A duration is stored as a fraction of an unsigned 128 bit integer over an unsigned 16 bit integer.

## Time conversions
For sake of clarity, this MathSpec specifies the units used, but some operations _seem_ to operate on different units: the `Duration` structure automatically converts all computations into seconds (represented as a lossless fraction, as described above).

### Dynamical Barycentric Time conversion
This is arguably the most complicated time conversion. Hifitime uses [ESA's Navipedia](https://gssc.esa.int/navipedia/index.php/Transformations_between_Time_Systems#TDT_-_TDB.2C_TCB) formulation. In the following, $C_{J2000_{TT}}$ corresponds to the number of centuries past J2000 TT, $\text{ET}_{s}$ is the ET epoch in seconds, $T_{s_{TT}}$ corresponds to the time in seconds TT, and $T_{s_{TDB}}$ the time in seconds in TDB.

First, compute the $g$ in radians (as 64 bit float), which corresponds to the approximation of the variation of time due to gravity of Earth (somehow).

$$ g = \frac{\pi}{2} \left( 357.528 + 35,999.050 ~  C_{J2000_{TT}} \right) $$

Then, compute the $g'$

$$ g' = g + 0.016,7 ~ \sin(g)$$

Now, compute the TDB duration in seconds:

$$ T_{s_{TDB}} = T_{s_{TT}} - \text{ET}_{s} + 0.001,658 ~ sin(g')$$

### TT
In seconds:

$$ T_{TT} = T_{TAI} + 32.184 $$

### JDE
In days, where $\text{J1900}=15,020$ is the offset in days and $\text{MJD}=2,400,000.5$ is the MJD offset to JDE in days.

$$ T_{JDE} = T_{TT} + (\text{J1900} + \text{MJD}) $$

### ET
In seconds, where $\text{ET'}_{s}=32.184,935$ is the ET offset in seconds compared to TAI.

$$ T_{ET} = T_{TAI} - (\text{ET}_{s} - \text{ET'}_{s}) $$

### GPST
In seconds,

$$ T_{GPST} = T_{TAI} - 19.0$$

--8<-- "includes/Abbreviations.md"