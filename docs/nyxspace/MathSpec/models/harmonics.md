# Spherical harmonics

Gravity field computations in Nyx use their spherical harmonics representation by means of the _Pines equations_. The algorithm is an adaptation of the NASA GMAT implementation, and validated against GMAT. The _Pines_ implementation requires rotation of the inertial state into the body fixed frame of the object for which the spherical harmonics are enabled.

To enable spherical harmonics, one must ensure to load either the low or high fidelity body frame frames for the objects of interest. Note tht Nyx supports enabling several spherical harmonics at once, e.g. one for the Earth and one for the Moon.

For the Earth, Nyx provides several models: JGM2, JGM3, and EGM2008 from GRACE. These can be used with any Earth body fixed frame, either ITRF93 or IAU Earth.
For the Moon, Nyx provides the JGGRX GRAIL model: be sure to configure the model to use the Moon Principal Axes frame.

--8<-- "includes/Abbreviations.md"