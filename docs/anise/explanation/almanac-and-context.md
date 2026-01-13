# The Almanac and the Context Pattern

In most legacy astrodynamics toolkits, loading "kernels" (data files) is a global operation. When you load a file, it enters a global memory pool accessible by any function in your program. This "Global State" pattern makes it extremely difficult to write concurrent code or to manage different scenarios in a single application.

## The Almanac as a Container

ANISE replaces the global pool with the `Almanac`. An `Almanac` is a self-contained object that stores:
- Ephemeris data (SPICE SPK)
- Orientation data (SPICE BPC, PCK)
- Planetary data (PCA)
- Spacecraft data (SCA)
- Euler Parameter / Unit quaternion data (EPA)
- Location data (LKA)
- Instrument data (IKA)

```rust
// In ANISE, you manage your own context
let mut almanac = Almanac::default();
almanac.load("de440.bsp")?;
```

Because the `Almanac` is an object, you can have as many as you want. One thread can work with a high-fidelity Earth model stored in `almanac_A`, while another thread performs long-term trajectory analysis using a simplified model in `almanac_B`.

## Immutable Sharing and Cheap Clones

A common concern with moving away from global state is the overhead of passing around a large context object. ANISE solves this through its memory management:

1. **In-Memory storing**: When you load a kernel into an `Almanac`, the data is read once in memory (on the heap), reducing the overhead of maintaining a file handler;
2. **Shared Data**: Internally, the `Almanac` uses reference-counting buffers;
3. **Cheap Clones**: Cloning an `Almanac` does not copy the gigabytes of ephemeris data; it simply creates a new handle to the same underlying memory.

This allows you to pass the `Almanac` into parallel loops (e.g., using `rayon` in Rust) with near-zero overhead.

## The Search Engine

The `Almanac` acts as a search engine for your data. When you ask for the position of Mars relative to Earth, the `Almanac`:
1. Looks up the IDs for Earth and Mars.
2. Traverses the ephemeris tree to find a common ancestor.
3. Chains together the necessary translations from the loaded SPK segments.
4. Returns the result as a high-precision state vector.

By centralizing this logic in a thread-safe object, ANISE provides a clean API that hides the complexity of multi-segment, multi-file lookups.
