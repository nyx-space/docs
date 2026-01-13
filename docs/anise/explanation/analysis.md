# Analysis Engine

ANISE includes a powerful **Analysis Engine** designed to answer complex astrodynamics questions declaratively. Instead of writing imperative loops to check conditions at every time step, you define *what* you want to compute, and ANISE figures out *how* to compute it efficiently.

## Core Philosophy

The analysis engine is built on three pillars:

1.  **Declarative Queries**: You describe the state of the system (e.g., "The distance between Earth and Mars") as an expression tree, rather than a sequence of math operations.
2.  **Continuous Resolution**: Unlike simple step-by-step propagation, the engine uses root-finding algorithms (specifically the **Brent solver**) to find exact times of events, such as when a satellite enters an eclipse or crosses a specific altitude.
3.  **Serialization**: All queries can be serialized to **S-expressions** (symbolic expressions). This allows you to define a query in Python, send it to a remote Rust/Python worker, and execute it safely without allowing arbitrary code execution.

## Expression Trees

Everything in the analysis engine is an **Expression**. These expressions can be nested to form complex queries.

-   **`StateSpec`**: Defines the "Context" of an orbital state. Who is the target? Who is the observer? What frame are we in?
    -   *Example*: "LRO (Target) as seen from the Moon (Observer) in the Moon Body-Fixed frame."
-   **`VectorExpr`**: Computes a 3D vector.
    -   *Examples*: `Radius`, `Velocity`, `SunVector`, `OrbitalMomentum`.
-   **`ScalarExpr`**: Computes a single floating-point number.
    -   *Examples*: `Norm` (of a vector), `DotProduct`, `AngleBetween`, `OrbitalElement` (eccentricity, SMA), `ShadowFunction`.
-   **`DcmExpr`**: Defines how to compute a direct cosine matrix, used to correctly align instruments with respect to the orbit frame
    -   *Examples*: `Triad` for an align/clock vector setup, `R1` for a rotation about X

### Example
To compute the **Beta Angle** (angle between the orbit plane and the vector to the Sun), you don't write a function. You build it:

```rust
// In pseudo-code representation of the internal tree
Shape: AngleBetween(
    VectorA: SunVector(Observer),
    VectorB: OrbitalMomentum(Target, Observer)
)
```

## Event Finding (The Superlinear Solver)

One of ANISE's most powerful features is its ability to find **Events**. An Event is defined by a `ScalarExpr` and a `Condition`.

-   **Scalar**: Any continuous values (e.g., "Elevation Angle").
-   **Condition**: A threshold or extrema (e.g., `= 4.57 deg`, `> 5.0 deg`, `Maximum`, `Minimum`).

### The Problem with Steps
If you simply loop through time with a 1-minute step, you might miss short events (like a 30-second eclipse) or get inaccurate start/stop times.

### The ANISE Solution: Brent's Method
ANISE uses an adaptive checking method combined with **Brent's method** for root finding.

1.  **Search**: It scans the time domain using an adapative step scanner inspired from adaptive step Runge Kutta methods
2.  **Bracket**: When it detects that the condition changed (e.g., elevation went from negative to positive), it knows a root (0 crossings) exists in that interval.
3.  **Solve**: It deploys the Brent solver to find the *exact* event when determining the value crossed the threshold.

This allows for **superlinear convergence**, meaning it finds high-precision times with very few function evaluations compared to brute-force searching.

## Reporting

The engine provides three main reporting modes:

1.  **`report_scalars`**: Evaluates a list of expressions at fixed time steps. This is parallelized using `rayon` for maximum speed.
2.  **`report_events`**: Finds discrete instants where a condition happens (e.g., "Apoapsis", "Max Elevation").
3.  **`report_event_arcs`**: Finds durations where a condition holds true (e.g., "Eclipse Duration", "Comm Window").
4.  **`report_visibility_arcs`**: Compute the Azimuth, Elevation, Range, and Range-rate ("AER") for each communication pass from a given location on _any_ celestial object.

## Safety and S-Expressions

Because analysis queries are just data structures (enums), they can be serialized into a lisp-like S-expression format.

```lisp
(Event
  (scalar (AngleBetween (Radius) (SunVector)))
  (condition (LessThan 90.0))
)
```

This is critical for web services or distributed systems. A client can craft a complex query and send it to a server. The server parses the S-expression and executes it. Because the server *only* executes valid ANISE expressions, there is **no risk of arbitrary code injection**, unlike pickling Python objects or sending raw scripts.
