---
hide:
  - navigation
  - toc
---


# Blazing fast spacecraft navigation {: .tagline}

!!! tip inline "Get started for free"

    Add Nyx to your current Python environment:
    ```sh
    pip install nyx_space
    ```

    Add Nyx to your [Rust :material-language-rust:](https://rust-lang.org) project:
    ```sh
    cargo add nyx_space
    ```

    [**Read the documentation** :material-file-document-multiple-outline:](/nyxspace/showcase/)


    [**Browse the source code** :material-github:](https://github.com/nyx-space/nyx)

    [**Learn about companion projects** :material-compass-rose:](#)


<script src="https://asciinema.org/a/590749.js" id="asciicast-590749" async data-autoplay="false" data-theme="solarized-dark" data-rows="20"></script>

<main class="landing">
    
<section class="grid">
    <article>
        <h2>Empowering flight dynamics engineers</h2>
        <h4>Powerful, open-source tools for mission design and analysis</h4>
        <p>As a flight dynamics engineer, you need to plan maneuvers, analyze spacecraft trajectories, and quickly turn around orbit determination solutions. Most options are proprietary, clunky, expensive, and slow.
        </p>
        <p>
        <span class="emph">Nyx is different.</span>
        <ul>
        <li>Trajectory planning - Targeting and optimization, low thrust or not</li>
        <li>Orbit determination - Gauss Markov noise models, and state-of-the-art autodiff for all orbital dynamics</li>
        <li>Interoperable - uses CCSDS standards and open formats (parquet, yaml)</li>
        <li>Free and open-source - no expensive licenses</li>
        <li>Analysis - plots are finally interactive</li>
        </ul>
        Plotting some residuals (dots dots dots!)
        <img class="blurry-image" src="assets/prefit-resid.png">
        </p>
    </article>
    <article>
        <h2>Built for speed, automation and scalability</h2>
        <h4>Simulate more, faster, from your desktop to the cloud</h4>
        <p>Nyx was built from the ground up to leverage advancements in computer science for space mission design. Our focus on performance, automation, and cloud/HPC-readiness provide insights for any operational scenario.</p>
        <p>
        <span class="emph">Unlock the future.</span>
        <ul>
        <li>Simulate and analyze ten thousand spacecraft in high-fidelity in 90 seconds on a standard desktop</li>
        <li>Automate repetitive tasks like report generation, data processing, and simulations</li>
        <li>Python API for easy integration into your automated pipelines and workflows</li>
        <li>Deploy across architectures from a laptop to the cloud for massive scaling</li>
        </ul>
        </p>
        <p>
        Simulate and analyze ten thousand spacecraft in high-fidelity in 90 seconds on a standard desktop (gravity of Earth, Moon, Sun, and Earth spherical harmonics of 12x12)
        <div class="chart">
            <div class="bar nyx" style="width: 50%">
                <div>Nyx: 90 seconds</div>
            </div>
            <div class="bar gmat" style="width: 85%">
                <div>GMAT: > 1 hour</div>
            </div>
            <div class="bar ansys" style="width: 100%">
                <div>ANSYS STK: > 1 hour + $$$</div>
            </div>
        </div>
        </p>
    </article>
    <article>
        <h2>Reliable, tested and documented</h2>
        <h4>Even the examples from the documentation are tested</h4>
        <p>Nyx provides a robust astrodynamics library tested against real-world scenarios and well documented to support your mission from planning to operations. You can also discuss solutions directly <a href="https://github.com/nyx-space/nyx/discussions">with the community</a>.</p>
        <p>
        <span class="emph">No more obsolete documentation</span>
        <ul>
        <li>Documentation uses the proven Diátaxis method to orient users</li>
        <li>Hundreds of tests validate calculations, methods and outputs</li>
        <li>Approachable syntax and interactive visuals foster understanding</li>
        <li>Lower risk through transparent verification and validation</li>
        </ul>
        <img class="blurry-image" src="assets/pipelines.png">
        </p>
    </article>
</section>
    
</main>

</div>
