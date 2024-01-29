ANISE is a modern rewrite of the NAIF SPICE toolkit. ANISE provides a toolkit and files for **A**ttitude, **N**avigation, **I**nstrument, **S**pacecraft, and **E**phemeris data.

ANISE is fully validated against SPICE by executing the same instructions in SPICE and in ANISE, and ensuring that the output matches.

Follow the work on [Github](https://github.com/nyx-space/anise) and show your support by adding a star.

Installation of ANISE is trivial:

=== "Python"

    ``` sh
    pip install anise
    ```

=== "Rust"

    ``` sh
    cargo add anise
    ```

## Documentation

This documentation aims to follow the [_Diataxis_ method](https://www.diataxis.fr/). Lots more documentation is needed, and don't hesitate to request some by [creating an issue on Github](https://github.com/nyx-space/anise/issues/new?assignees=&labels=Documentation&projects=&template=documentation.md&title=).

### Tutorials

The latest tutorials in Python are available as [Jupyter notebooks on Github](https://github.com/nyx-space/anise/tree/master/anise-py/notebooks). They are also available in the tutorials section of this website.

## Validation

[![ANISE Validation](https://github.com/nyx-space/anise/actions/workflows/rust.yml/badge.svg)](https://github.com/nyx-space/anise/actions/workflows/rust.yml)

ANISE is validated by running the same queries in ANISE and in SPICE (single threaded) in the _Validation_ step linked above. This workflow validates 101,000 BSP queries in the DE440.BSP file, and 7305 queries each frame in the PCK08 file (every day for 20 years), along with thousands of rotations from Earth high precision BPC file.

**Note:** The PCK data comes from the IAU Reports, which publishes angle, angle rate, and angle acceleration data, expressed in centuries past the J2000 reference epoch.
ANISE uses Hifitime for time conversions. Hifitime's reliance solely on integers for all time computations eliminates the risk of rounding errors. In contrast, SPICE utilizes floating-point values, which introduces rounding errors in calculations like centuries past J2000. Consequently, you might observe a discrepancy of up to 1 millidegree in rotation angles between SPICE and ANISE. However, this difference is a testament to ANISE's superior precision.

## Resources / Assets

For convenience, Nyx Space provides a few important SPICE files on a public bucket:

+ [de440s.bsp](http://public-data.nyxspace.com/anise/de440s.bsp): JPL's latest ephemeris dataset from 1900 until 20250
+ [de440.bsp](http://public-data.nyxspace.com/anise/de440.bsp): JPL's latest long-term ephemeris dataset
+ [pck08.pca](http://public-data.nyxspace.com/anise/v0.3/pck08.pca): planetary constants ANISE (`pca`) kernel, built from the JPL gravitational data [gm_de431.tpc](http://public-data.nyxspace.com/anise/gm_de431.tpc) and JPL's plantary constants file [pck00008.tpc](http://public-data.nyxspace.com/anise/pck00008.tpc)
+ [pck11.pca](http://public-data.nyxspace.com/anise/v0.3/pck11.pca): planetary constants ANISE (`pca`) kernel, built from the JPL gravitational data [gm_de431.tpc](http://public-data.nyxspace.com/anise/gm_de431.tpc) and JPL's plantary constants file [pck00011.tpc](http://public-data.nyxspace.com/anise/pck00011.tpc)
+ [moon_fk.epa](http://public-data.nyxspace.com/anise/v0.3/moon_fk.epa): Euler Parameter ANISE (`epa`) kernel, built from the JPL Moon Frame Kernel `moon_080317.txt`

You may load any of these using the `load()` shortcut that will determine the file type upon loading, e.g. `let almanac = Almanac::new("pck08.pca").unwrap();` or in Python `almanac = Almanac("pck08.pca")`. To automatically download remote assets, from the Nyx Cloud or elsewhere, use the MetaAlmanac: `almanac = MetaAlmanac("ci_config.dhall").process()` in Python.

## Contributing

Contributions to ANISE are welcome! Whether it's in the form of feature requests, bug reports, code contributions, or documentation improvements, every bit of help is greatly appreciated.

## License

ANISE is distributed under the Mozilla Public License 2.0 (MPL-2.0), offering a balanced approach to open-source by allowing the use of source code within both open and proprietary software. MPL-2.0 requires that modifications to the covered code be released under the same license, thus ensuring improvements remain open-source. However, it allows the combining of the covered software with proprietary parts, providing flexibility for both academic and commercial integrations.

For more details, please see the [full text of the license](https://github.com/nyx-space/anise/blob/master/LICENSE) or read [a summary by Github](https://choosealicense.com/licenses/mpl-2.0/).

## Acknowledgements

ANISE is heavily inspired by the NAIF SPICE toolkit and its excellent documentation.