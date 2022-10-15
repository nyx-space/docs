![Nyx logo](assets/logo.png){: .center }

<p class="tagline">Analyze, automate, and fly &mdash; as a team</p>

<p class="pitch">Nyx is a platform for astrodynamics tools to support space missions from its early design phase through flight operations.</p>

| Nyx Space | ANISE | Hifitime |
| :---: | :---: | :---: | 
| <big>A fully featured astrodynamics toolkit for mission design and orbit determination</big> | <big>A modern rewrite of NASA SPICE for desktop and embedded systems</big> | <big>An ultra-precise time computation library for safety-critical systems</big> |
| [Design Docs](#) | [Purpose](#) | [Design Docs](/hifitime/design/) |
| [Mathematical specifications](#) | [Design Docs](#) | [Get started in Rust](/hifitime/rust/) |
| [Get started in Rust](#) | [Get started in Python](#) | [Get started in Python](hifitime/python/) |


## :material-rocket-launch-outline: Mission Design

+ **Designed for Monte Carlo analyzes**{ .emph }

    + Monte Carlo safely run on all processors without any of the multi-threading risks you'd see in C++ or Python (no data race conditions, no stopping the program before saving data)
    + Simulate and analyze ten thousand (10,000 !!) spacecraft in high-fidelity in 90 seconds on a standard desktop (celestial bodies of Earth, Moon, Sun, Earth spherical harmonics of 12x12)
    + Analyze trajectories in parallel by generating their ephemerides

+ **High fidelity models**{ .emph }
    
    + Multi-body gravity, solar radiation pressure, and atmospheric drag models
    + Spherical harmonic gravity fields: JGM3 and EGM2008 for Earth, JGGRX for the Moon
    + Eclipse modeling with multiple concurrent celestial objects
    
+ **Maneuver planning**{ .emph }

    + Differential corrector and multiple shooting for finite burn and low-thrust trajectory optimization
    + Guidance laws: Ruggiero, Lyapunov control, or add your own guidance law
    + Two-body approximations: Lambert solver, Hohmann transfer

<hr/>

## :material-vector-curve: Orbit Determination

+ **Spaceflight Navigation**{ .emph }

    + Conventional and Extended Kalman filters
    + Smoothing and iteration of navigation estimates
    + One-way and two-range ranging and Doppler measurements


+ **State-of-the-art partials computation**{ .emph }

    + Dual Number theory for STM computation (Rabotin 2019)
    + Partials available for multibody dynamics, spherical harmonics

+ **Automation and workflows**{ .emph }

    + Leverage computational speed for simulating a OD of off-nominal trajectories
    + Cloud-ready library and application enables automation of your workflow
    

<hr/>

## :material-globe-model: ConOps Analysis

+ **Event-based ConOps**{ .emph }

    + Design concepts of operations by finding specific events in a spacecraft trajectories
    + Seek spacecraft and cosmic events in any celestial frame
    

+ **State-of-the-art models**{ .emph }

    + Planetary and solar eclipse, penumbra and visibility computations
    + NAIF DE438s planetary ephemeris by NASA
    + IAU 2018 body fixed frames (Archinal et al. 2018)

+ **Orbital state transformation**{ .emph }

    + Conversion between Cartesian states and Keplerian orbital elements
    + Central body and rotation transformations


<hr/>

## :material-file-document-outline: Licensing

Nyx itself is licensed in AGPL version 3.0. Learn more about the important terms of this license [here](/license/). ANISE is licensed in Mozilla Public License (MPL). Hifitime is licensed in Apache 2.0

<hr/>

## :material-email-outline: Contact
If some documentation needs clarification, or if you've found a bug, please open a new issue [here](https://gitlab.com/nyx-space/nyx/-/issues/new) (you'll need a free gitlab.com account). Otherwise, you may also create a new issue by emailing the Gitlab project directly by clicking <a href="mailto:incoming+nyx-space-nyx-11893257-issue-@incoming.gitlab.com">here</a>.


For general chatter about astrodynamics, you can join the [#astrodyn](https://app.element.io/#/room/#astrodyn:matrix.org) room on Element.io, a secure and decentralized internet chat platform.

To contact the author of Nyx, Chris Rabotin, email chris.rabotin@pm.me.

!!! quote
    Ce que l'on conçoit bien s'énonce clairement, et les mots pour le dire arrivent aisément.

    <small>Whatever is well conceived is clearly said, and the words to say it flow with ease.</small>

    -- Nicolas Boileau Despréaux

--8<-- "includes/Abbreviations.md"