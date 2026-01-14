# Analysis API

The Analysis API allows you to query the almanac for data products, events, and contact windows.

## Reporting Scalars

Use `report_scalars` to generate time-series data for analysis or plotting.

### `almanac.report_scalars(report, time_series)`

Expects a `ReportScalars` object containing a list of expressions and a `StateSpec`.

**Parameters:**

- `report`: A `ReportScalars` instance defined with:
    - `state_spec`: The context (Target, Observer, Frame) to evaluate against.
    - `scalars`: A list of `ScalarExpr` items.
- `time_series`: A `hifitime::TimeSeries` defining the start, end, and step.

**Returns:**

A dictionary (or map) where keys are Epochs and values are maps of `{ "Alias": Value }`.

```python
    target_frame = analysis.FrameSpec.Loaded(Frames.EME2000)
    observer_frame = analysis.FrameSpec.Loaded(Frames.MOON_J2000)

    state = analysis.StateSpec(
        target_frame=target_frame,
        observer_frame=observer_frame,
        ab_corr=None,
    )

    # Define all scalars to be calculated
    scalars = [
        analysis.ScalarExpr.Element(analysis.OrbitalElement.SemiMajorAxis),
        analysis.ScalarExpr.Element(analysis.OrbitalElement.Eccentricity),
        analysis.ScalarExpr.Element(analysis.OrbitalElement.Rmag),
        analysis.ScalarExpr.BetaAngle(),
        analysis.ScalarExpr.SolarEclipsePercentage(eclipsing_frame=Frames.VENUS_J2000),
    ]

    # Add optional aliases (Tuple of (Scalar, Alias))
    scalars_with_aliases = [(s, None) for s in scalars]
    
    # Build the final report object
    report = analysis.ReportScalars(scalars_with_aliases, state)

    # Generate the report data
    series = TimeSeries(
        Epoch("2025-01-01 00:00:00 UTC"),
        Epoch("2025-01-02 12:00:00 UTC"),
        Unit.Day * 0.5,
        inclusive=True,
    )
    data = almanac.report_scalars(report, series)
```

## Finding Events

Use `report_events` to find specific instants (points in time).

### `almanac.report_events(state, event, start, end)`

Finds discrete events such as:

- **Orbital Events**: Apoapsis, Periapsis.
- **Min/Max**: Time of maximum elevation, minimum range.
- **Crossings**: Time when altitude crosses 100km.

**Returns:**

A list of `EventDetails` objects, each containing:

- `epoch`: The precise time of the event.
- `value`: The value of the scalar at that time.
- `orbit`: The full spacecraft state at that time.

```python
    # Define an event: Sun Angle < 90.0 degrees (Sunset)
    sun_has_set = analysis.Event(
        analysis.ScalarExpr.SunAngle(observer_id=-85), # LRO ID
        Condition.LessThan(90.0),
        Unit.Second * 0.5,
        ab_corr=None,
    )
    
    # Predefined events are also available
    apolune = Event.apoapsis()
    perilune = Event.periapsis()

    # Find distinct events (points in time)
    apo_events = almanac.report_events(lro_state_spec, apolune, start_epoch, end_epoch)
```

## Finding Intervals (Arcs)

Use `report_event_arcs` to find durations.

### `almanac.report_event_arcs(state, event, start, end)`

Finds time intervals where a condition is continuously true.

- **Visibility**: "When can I see the station?"
- **Battery**: "When am I in sunlight?"
- **Geometry**: "When is the Earth-Sun-Probe angle < 90?"

**Returns:**

A list of `EventArc` objects, each containing:

- `start`: The `EventDetails` of the start (Rising edge).
- `end`: The `EventDetails` of the end (Falling edge).

```python
    eclipse = Event.total_eclipse(Frames.MOON_J2000)

    # Find durations (arcs)
    sunset_arcs = almanac.report_event_arcs(
        lro_state_spec, sun_has_set, start_epoch, end_epoch
    )
    
    eclipse_arcs = almanac.report_event_arcs(
        lro_state_spec, eclipse, start_epoch, start_epoch + period * 3
    )
```

**Returns:**

A list of `EventArc` objects, each containing:

- `start`: The `EventDetails` of the start (Rising edge).
- `end`: The `EventDetails` of the end (Falling edge).

The [`EventArc`](https://docs.rs/anise/latest/anise/analysis/event/struct.EventArc.html#impl-EventArc) provides the following helpers:

- `duration`: the duration of the event, as a hifitime Duration
- `start_epoch`, `end_epoch`: the epochs of the start and end of the event
- `midpoint_epoch`: the half-way point in the event, useful if you need to check for some calculation that happens undoubtedly during the event itself.

