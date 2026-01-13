# Why ANISE?

ANISE (Attitude, Navigation, Instrument, Spacecraft, Ephemeris) was born out of a need for a modern, high-performance, and thread-safe toolkit for space mission design and operations. While the NAIF SPICE toolkit has been the industry standard for decades, its architecture was designed for an era of single-threaded, procedural programming.

## Designed for Modern Hardware

Modern computing environments, from high-performance workstations to cloud-based clusters, rely on multi-core processors. Legacy toolkits often struggle in these environments due to:

- **Global State**: SPICE uses a global kernel pool. This means you cannot easily load different sets of kernels for different threads or perform concurrent queries without complex locking mechanisms (mutexes) that severely bottleneck performance.
- **Thread Safety**: Because of its global state and internal cache mechanisms, SPICE is inherently NOT thread-safe.

**ANISE is thread-safe by design.** It eliminates global state by using the `Almanac` as a first-class object. You can create multiple `Almanac` instances, each with its own set of loaded kernels, and share them across threads safely.

## Safety through Rust

By building on Rust, ANISE leverages a powerful type system and ownership model to provide guarantees that other toolkits cannot:

- **Memory Safety**: Rust prevents common bugs like null pointer dereferences, buffer overflows, and data races at compile time.
- **Frame Safety**: ANISE doesn't just treat frames as integer IDs. It understands the relationship between frames. It validates that any transformation (rotation or translation) you request is physically possible before even attempting the math. No more mixing up J2000 and ITRF93 by accident.

## Precision and Performance

ANISE matches SPICE's mathematical precision—and in many cases, exceeds it.

- **Integer-based Time**: By using the `hifitime` library, ANISE avoids the rounding errors inherent in floating-point time representations (used by SPICE). This is particularly critical for high-fidelity planetary rotations where a few microseconds of error can accumulate over years.
- **Limited file system calls**: ANISE uses copies the content of files on the heap on load, allowing it to query large kernel files (like DE440) with zero file system waits, minimal memory overhead and maximum speed.

## Multi-language from the Core

ANISE is an ecosystem. While the core engine is written in Rust for maximum performance, it is designed to be easily accessible from other languages.
- **Rust**: Native performance and type safety.
- **Python**: A pythonic API (`anise-py`) that offers the performance and safety of the Rust core.
- **CLI/GUI**: Tools for quick inspection and visualization that work cross-platform.
- **C++**: While planned, this interface is stalled due to limited resources.
