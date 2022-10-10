![Nyx logo](assets/logo.png){: .center }

<p class="pitch">Nyx is a set of open-source astrodynamics tools to support space missions from its early design phase through flight operations.</p>

<!-- <p class="pitch">Blazing fast high-fidelity astrodynamics for <b class="emph">Monte Carlo</b> analyzes of <b class="emph">constellations</b>, <b class="emph">interplanetary</b> missions, and deep space <b class="emph">orbit determination</b></p> -->

| Nyx Space | ANISE | Hifitime |
| :---: | :---: | :---: | 
| A fully featured astrodynamics toolkit in Rust and Python | A modern rewrite of NASA/NAIF SPICE available in Rust, Python, FORTRAN, and C | An ultra-precise time computation library suitable for microcontrollers |
| [Design Docs](#) | [Purpose](#) | [Design Docs](#) |
| [Mathematical specifications](#) | [Design Docs](#) | [Get started in Python](#) |
| [Get started in Rust](#) | [Get started in Python](#) | [Get started in Rust](#) |


## :material-rocket-launch-outline: Mission Design

<ul>
<li>
    <b class="emph">Designed for Monte Carlo analyzes</b>
    <ul>
        <li>Monte Carlo safely run on all processors without any of the multi-threading risks you'd see in C++ or Python (no data race conditions, no stopping the program before saving data)</li>
        <li>Simulate and analyze ten thousand (10,000 !!) spacecraft in high-fidelity in 90 seconds on a standard desktop (celestial bodies of Earth, Moon, Sun, Earth spherical harmonics of 12x12)</li>
        <li>Analyze trajectories in parallel by generating their ephemerides</li>
    </ul>
</li>
<li>
    <b class="emph">High fidelity models</b>
    <ul>
        <li>Multi-body gravity, solar radiation pressure, and atmospheric drag models</li>
        <li>Spherical harmonic gravity fields: JGM3 and EGM2008 for Earth, JGGRX for the Moon</li>
        <li>Eclipse modeling with multiple concurrent celestial objects</li>
    </ul>
</li>
<li>
    <b class="emph">Maneuver planning</b>
    <ul>
        <li>Differential corrector and multiple shooting for finite burn and low-thrust trajectory optimization</li>
        <li>Guidance laws: Ruggiero, Lyapunov control, or add your own guidance law</li>
        <li>Two-body approximations: Lambert solver, Hohmann transfer</li>
    </ul>
</li>
</ul>

<hr/>

## :material-vector-curve: Orbit Determination

<ul>
<li>
    <b class="emph">Spaceflight Navigation</b>
    <ul>
        <li>Conventional and Extended Kalman filters</li>
        <li>Smoothing and iteration of navigation estimates</li>
        <li>One-way and two-range ranging and Doppler measurements</li>
    </ul>
</li>
<li>
    <b class="emph">State-of-the-art partials computation</b>
    <ul>
        <li>Dual Number theory for STM computation (Rabotin 2019)</li>
        <li>Partials available for multibody dynamics, spherical harmonics</li>
    </ul>
</li>
<li>
    <b class="emph">Automation and workflows</b>
    <ul>
        <li>Leverage computational speed for simulating a OD of off-nominal trajectories</li>
        <li>Cloud-ready library and application enables automation of your workflow</li>
    </ul>
</li>
</ul>

<hr/>

## :material-globe-model: ConOps Analysis

<ul>
<li>
    <b class="emph">Event-based ConOps</b>
    <ul>
        <li>Design concepts of operations by finding specific events in a spacecraft trajectories</li>
        <li>Seek spacecraft and cosmic events in any celestial frame</li>
    </ul>
</li>
<li>
    <b class="emph">State-of-the-art models</b>
    <ul>
        <li>Planetary and solar eclipse, penumbra and visibility computations</li>
        <li>NAIF DE438s planetary ephemeris by NASA</li>
        <li>IAU 2018 body fixed frames (Archinal et al. 2018)</li>
    </ul>
</li>
<li>
    <b class="emph">Orbital state transformation</b>
    <ul>
        <li>Conversion between Cartesian states and Keplerian orbital elements</li>
        <li>Central body and rotation transformations</li>
    </ul>
</li>
</ul>

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