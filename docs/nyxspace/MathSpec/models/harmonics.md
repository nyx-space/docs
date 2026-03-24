# Spherical harmonics

Gravity field computations in Nyx use their spherical harmonics representation by means of the _Pines equations_. The algorithm is an adaptation of the NASA GMAT implementation, and validated against GMAT. The _Pines_ implementation requires rotation of the inertial state into the body fixed frame of the object for which the spherical harmonics are enabled.

To enable spherical harmonics, one must ensure to load either the low or high fidelity body frame frames for the objects of interest. Note that Nyx supports enabling several gravity fields at once, which is useful when propagating some cislunar halo orbits.

For the Earth, Nyx provides several models: JGM2, JGM3, and EGM2008 from GRACE. These can be used with any Earth body fixed frame, either ITRF93 or IAU Earth.
For the Moon, Nyx provides the JGGRX GRAIL model: be sure to configure the model to use the Moon Principal Axes frame.

Nyx supports the SHADR (_Spherical Harmonic ASCII Model_) and COF formats natively, optionally gunzipped to save on disk space. SHADR (extension `.sha`) can be found directly on the [NASA Planetary Data Service website](https://pds-geosciences.wustl.edu/dataserv/gravity_models.htm).

Nyx Space also hosts a few common SHADR gravity fields:

- <http://public-data.nyxspace.com/nyx/models/JGM3.cof.gz>
- <http://public-data.nyxspace.com/nyx/models/EGM2008_to2190_TideFree.gz>
- <http://public-data.nyxspace.com/nyx/models/Lunar_gggrx_1200a_sha.tab.gz>
- <http://public-data.nyxspace.com/nyx/models/Luna_jggrx_1500e_sha.tab.gz>


--8<-- "includes/Abbreviations.md"
