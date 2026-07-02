---
hide:
  - navigation
  - toc
---

# Nyx Space: Revolutionizing Flight Dynamics {: .tagline}

<p class="subtagline">Blazing fast open-source tools from mission concept to operations, analysis, and automation</p>

<main class="landing">

<section class="card-container" style="grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));">
    <!-- High Fidelity Mission design (Nyx) -->
    <article class="card" style="flex-direction: column; align-items: flex-start;">
        <div class="card-content">
            <h2 style="margin: 0">Advanced Flight Dynamics</h2>
            <h3 class="text-accent">Complex mission orchestration</h3>
            <ul>
            <li>Access validated gravity model datasets and daily updates to atmospheric and Earth rotation data</li>
            <li>Augmented state estimation and consider covariance, including ground station location, and radio delays and biases</li>
            <li>Target coupled multi-spacecraft trajectories and automating repeated, multi-phase operational conops sequences</li>
            <li>Genetic algorithm global optimization of low thrust constellation orbit raising</li>
            <li><b>100% free license</b> designed for Air-gapped Mission Ops Centers, and continuous integration pipelines</li>
            </ul>
            <a href="https://7ug5imdtt8v.typeform.com/to/BEzJQESl" class="md-button md-button--primary" target="_blank">Learn more</a>
            <a href="https://platform.nyxspace.com" class="md-button">Login</a>
        </div>
    </article>
    <article class="card" style="flex-direction: column; align-items: flex-start;">
        <div class="card-content">
            <h2 style="margin: 0">Orbit Determination</h2>
            <h3 class="text-accent">Scriptable, CI-ready replacement for Ansys ODTK</h3>
            <ul>
            <li>Extended Kalman Filters, with smoothing, and Batch Least Squares Estimators (incl. Levenberg Marquart)</li>
            <li>Access Normalized Innovation Squared (NIS) and Normalized Estimation Error Square (NEES)</li>
            <li>Export whitened residuals, Kalman gains, Filter-Smoother consistency, Uncertainty of orbital elements</li>
            <li>State noise compensation (process noise) available in inertial, RIC, or VNC frames, with maximum inflation duration, or exponentially decaying</li>
            <li>Full OD Monte Carlo simulation suite with multivariate dispersions from covariance</li
            </ul>
            <a href="/nyxspace/showcase/04_lro_od/" class="md-button md-button--primary" target="_blank">Lunar OD demo</a>
        </div>
    </article>
    <article class="card" style="flex-direction: column; align-items: flex-start;">
        <div class="card-content">
            <h2 style="margin: 0">Mission Design &amp; Optimization</h2>
            <h3 class="text-accent">Fidelity of Ansys STK, at several times the speed</h3>
            <ul>
            <li>Third-body effects, solar radiation pressure accounting for tri-axial ellipsoid of the shadow object, drag model (NRLMSISE-00), multi-body solid tides (compatible with gas giants)</li>
            <li>Maneuver targeting and modeling: impulsive, finite high-thrust burns, low-thrust optimization</li>
            <li>Multi-variable differential correctors (<i>targeters</i>) using either Newton Raphson or Broyden's method (<i>Secant</i>)</li>
            <li>Propagation stopping conditions on epoch, duration, orbital element, or any ANISE calculation object (e.g. LST of 0615)</li>
            </ul>
            <a href="/nyxspace/showcase/03_geo_analysis/" class="md-button md-button--primary" target="_blank">GEO low thrust orbit raise</a>
        </div>
    </article>
    <article class="card" style="flex-direction: column; align-items: flex-start;">
        <div class="card-content">
            <h2 style="margin: 0">Monte Carlo &amp; Dispersion Analysis</h2>
            <h3 class="text-accent">3,000 simulation days per minute per CPU core</h3>
            <ul>
            <li>Parallel and thread-safe by design, enabling massive-scale operational-level risk analysis</li>
            <li>Multivariate normal dispersions from covariance, or specific orbital element uncertainty, mapped to Cartesian space with automatic differentiation</li>
            <li><b>Blazing fast speeds</b>, low memory footprint, unmatched by any proprietary toolsuite</li>
            </ul>
            <a href="/nyxspace/showcase/02_jwst_covar_monte_carlo/" class="md-button md-button--primary" target="_blank">James Webb Monte Carlo</a>
        </div>
    </article>
    <!-- ANISE Card -->
    <article class="card" style="flex-direction: column; align-items: flex-start;">
        <div class="card-content">
            <h2 style="margin: 0">ANISE</h2>
            <h3 class="text-accent">Landed Firefly Blue Ghost on the Moon</h3>
            <ul>
            <li>Thread-safe, FSW-ready alternative to legacy SPICE toolkit</li>
            <li>Ephemeris, Orientation, Instrument, Eclipse modeling validated against CSPICE in continuous integration</li>
            <li>Calculations of orbital elements, ground station azimuth, elevation, range, and range-rate data, orbital element uncertainties from covariance, etc.</li>
            <li>Supports NASA SPICE kernels, CCSDS OEM and OPM, and STK .e files</li>
            </ul>
            <a href="/anise/" class="md-button md-button--primary">Learn more</a>
            <a href="/anise/tutorials/" class="md-button">Tutorials</a>
        </div>
    </article>
    <!-- Hifitime Card -->
    <article class="card" style="flex-direction: column; align-items: flex-start;">
        <div class="card-content">
            <h2 style="margin: 0">Hifitime</h2>
            <h3 class="text-accent">Precision Time Management</h3>
            <p>An overflow-safe, high-performance datetime library providing leap-second-correct nanosecond precision across UTC, GPST, and relativistic time-scales. Flight-proven in lunar and deep-space missions, it works on desktop, web assembly, and bare-metal platforms.</p>
            <a href="/hifitime/" class="md-button md-button--primary">Learn more</a>
            <a href="/hifitime/python/" class="md-button">Python Docs</a>
        </div>
    </article>
    <!-- Trusted by Industry Leaders (spans full width) -->
    <article class="card" style="grid-column: 1 / -1; flex-direction: column; text-align: center;">
        <div class="card-content" style="width: 100%; padding-right: 0;">
            <h2 style="margin: 0; text-align: center;">Trusted by Industry Leaders</h2>
            <h3 class="text-accent" style="text-align: center;">See who's already benefiting from our tools</h3>
            <p style="text-align: center; max-width: 800px; margin: 0 auto 1em auto;">Our tools are trusted and actively used by leading companies in the aerospace and technology sectors. Their commitment to using Nyx, Hifitime, and ANISE is a testament to the reliability, efficiency, and advanced capabilities of our software.</p>
            <div class="marquee-container" style="margin-top: 2em;">
                <div class="marquee-content">
                    <div class="marquee-item"><img src="/assets/corps/FireflySpace.png" alt="Firefly Space"></div>
                    <div class="marquee-item"><img src="/assets/corps/K2Space.png" alt="K2 Space"></div>
                    <div class="marquee-item"><img src="/assets/corps/AmazonWebServices.png" alt="Amazon Web Services"></div>
                    <div class="marquee-item"><img src="/assets/corps/CNRS.png" alt="CNRS (Femto-ST)"></div>
                    <div class="marquee-item"><img src="/assets/corps/Astranis.png" alt="Astranis"></div>
                    <div class="marquee-item"><img src="/assets/corps/RocketLab.png" alt="Rocketlab USA"></div>
                    <!-- Duplicate for infinite scroll -->
                    <div class="marquee-item"><img src="/assets/corps/FireflySpace.png" alt="Firefly Space"></div>
                    <div class="marquee-item"><img src="/assets/corps/K2Space.png" alt="K2 Space"></div>
                    <div class="marquee-item"><img src="/assets/corps/AmazonWebServices.png" alt="Amazon Web Services"></div>
                    <div class="marquee-item"><img src="/assets/corps/CNRS.png" alt="CNRS (Femto-ST)"></div>
                    <div class="marquee-item"><img src="/assets/corps/Astranis.png" alt="Astranis"></div>
                    <div class="marquee-item"><img src="/assets/corps/RocketLab.png" alt="Rocketlab USA"></div>
                </div>
            </div> <br />
            <a href="https://7ug5imdtt8v.typeform.com/to/neFvVW3p" class="md-button md-button--primary" target="_blank" style="margin-top: 1em; display: inline-block;">Contact Form</a>
        </div>
    </article>
</section>

</main>
