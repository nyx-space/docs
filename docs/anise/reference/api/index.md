# API Documentation

ANISE is available as a Rust crate and a Python package. Both share the same high-performance core but provide language-specific interfaces.

## [Rust API](https://docs.rs/anise/latest/anise/)

The Rust API provides the most complete and performant access to ANISE. It includes full type safety for frames and epochs.

- [Almanac](https://docs.rs/anise/latest/anise/struct.Almanac.html)
- [Orbit](https://docs.rs/anise/latest/anise/struct.Orbit.html)
- [Epoch](https://docs.rs/anise/latest/anise/time/index.html)

## Python API

The Python API (`anise-py`) is designed to be familiar to users of `SpiceyPy` and `MONTE`, while offering the performance of Rust.

- [Python Module Overview](python/index.md) (Internal documentation)
- [Examples and Jupyter Notebooks](https://github.com/nyx-space/anise/tree/main/anise-py/examples)
