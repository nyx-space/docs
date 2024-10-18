ANISE is a modern rewrite of the NAIF SPICE toolkit, with many additional features. ANISE provides a toolkit for **A**ttitude, **N**avigation, **I**nstrument, **S**pacecraft, and **E**phemeris computations.

Answer questions like _what will be the elevation of the Moon from a ground station on 21 Dec 2033_, or _will visible-light cameras on my spacecraft be able to image a given location in 3 orbital periods_.

[Github :material-github:](https://github.com/nyx-space/anise){ .md-button } [User survey :material-file-question:](https://7ug5imdtt8v.typeform.com/to/qYDB14Hj){ .md-button }

## Installation

=== "Python"

    ``` sh
    pip install anise
    ```

=== "Rust"

    ``` sh
    cargo add anise
    ```

## Documentation

This documentation aims to follow the [_Diataxis_ method](https://www.diataxis.fr/).

+ [Tutorials](./tutorials/index.md)
+ [Explanation](./explanation/index.md)

Lots more documentation is needed, and don't hesitate to request some by [creating an issue on Github](https://github.com/nyx-space/anise/issues/new?assignees=&labels=Documentation&projects=&template=documentation.md&title=).

## Validation

Refer to the explanation on [validation](./explanation/validation.md).

## Resources / Assets

For convenience, Nyx Space provides a few important SPICE files on a public bucket:

+ [de440s.bsp](http://public-data.nyxspace.com/anise/de440s.bsp): JPL's latest ephemeris dataset from 1900 until 20250
+ [de440.bsp](http://public-data.nyxspace.com/anise/de440.bsp): JPL's latest long-term ephemeris dataset
+ [pck08.pca](http://public-data.nyxspace.com/anise/v0.4/pck08.pca): planetary constants ANISE (`pca`) kernel, built from the JPL gravitational data [gm_de431.tpc](http://public-data.nyxspace.com/anise/gm_de431.tpc) and JPL's plantary constants file [pck00008.tpc](http://public-data.nyxspace.com/anise/pck00008.tpc)
+ [pck11.pca](http://public-data.nyxspace.com/anise/v0.4/pck11.pca): planetary constants ANISE (`pca`) kernel, built from the JPL gravitational data [gm_de431.tpc](http://public-data.nyxspace.com/anise/gm_de431.tpc) and JPL's plantary constants file [pck00011.tpc](http://public-data.nyxspace.com/anise/pck00011.tpc)
+ [moon_fk.epa](http://public-data.nyxspace.com/anise/v0.4/moon_fk.epa): Euler Parameter ANISE (`epa`) kernel, built from the JPL Moon Frame Kernel `moon_080317.txt`

You may load any of these using the `load()` shortcut that will determine the file type upon loading, e.g. `let almanac = Almanac::new("pck08.pca").unwrap();` or in Python `almanac = Almanac("pck08.pca")`. To automatically download remote assets, from the Nyx Cloud or elsewhere, use the MetaAlmanac: `almanac = MetaAlmanac("ci_config.dhall").process()` in Python.

## Contributing

Contributions to ANISE are welcome! Whether it's in the form of feature requests, bug reports, code contributions, or documentation improvements, every bit of help is greatly appreciated.

## License

ANISE is distributed under the Mozilla Public License 2.0 (MPL-2.0), offering a balanced approach to open-source by allowing the use of source code within both open and proprietary software. MPL-2.0 requires that modifications to the covered code be released under the same license, thus ensuring improvements remain open-source. However, it allows the combining of the covered software with proprietary parts, providing flexibility for both academic and commercial integrations.

For more details, please see the [full text of the license](https://github.com/nyx-space/anise/blob/master/LICENSE) or read [a summary by Github](https://choosealicense.com/licenses/mpl-2.0/).

## Acknowledgements

ANISE is heavily inspired by the NAIF SPICE toolkit and its excellent documentation. Huge thanks to Grégoire Henry from the Royal Observtory of Belgium and Chris De Calverie from GAMA Space for their continued support of this work.