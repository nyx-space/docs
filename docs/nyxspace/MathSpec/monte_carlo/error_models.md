# Error modeling
The whole purpose of Monte Carlo analyses is to support appropriate modeling of errors in the design of the mission. Several models are available by default in Nyx, but you may provide your own or request integration of new models by opening an issue or emailing Chris Rabotin.

## Delta-V
### Pointing error

Oftentimes, one needs account for pointing errors in 3-DOF mission design. Nyx provides the `dv_pointing_error` method for computing pointing errors.

Let $\mathbf{v}$ be the velocity vector of the orbit and $\mathbf{\Delta v}$ be the $\Delta v$ vector in the same frame which should be applied to the spacecraft.

Start by computing the angle between those vector as

$$ \alpha = \cos^{-1}\left( \frac{\mathbf v \cdot \mathbf{\Delta v}}{||\mathbf v || ||\mathbf{\Delta v}||} \right)$$

Generate a new angle as the pointing error $3\sigma$ value using a Normal distribution centered on the current angle:

$$ \alpha' \sim \mathcal{N}\left(\alpha, \frac \sigma 3\right) $$

Return the modified $\Delta v$ vector as follows such that its magnitude is the same as before but its pointing is off by the provided $3 \sigma$ value:

$$ \mathbf{\Delta v'} = ||\mathbf{\Delta v}||\cos(\alpha)~\mathbf v $$

### Execution error
Execution errors include both magnitude and pointing errors, whose $3 \sigma$ values may differ.

The algorithm starts by applying the [pointing error](#pointing-error) as defined above. Then, it generates a new magnitude for the $\Delta v$ using a Normal distribution centered on the current magnitude and whose standard deviation is one third of the provided $3\sigma$ magnitude error:

$$ \Delta v' \sim \mathcal{N}\left(\Delta v, \frac \sigma 3\right) $$

Finally, return the execution and pointing error vector as follows where $\mathbf {\Delta v}$ is the velocity change vector with pointing errors:

$$ \mathbf {\Delta v'} = \Delta v' || \mathbf {\Delta v} || $$


## Random unit vector

The `unit_vector_from_seed` function generates a unit vector in 3D space following the [Sphere Point Picking method](https://mathworld.wolfram.com/SpherePointPicking.html).[^1]

It uses a Uniform distribution between 0 and 1 inclusive to generate both the $u$ and $v$ parameters.

$$u \sim \mathcal{U}(0,1) \quad\quad v \sim \mathcal{U}(0,1)$$

Generate the angles on the sphere as:

$$\theta = 2\pi u \quad\quad \phi = \cos^{-1}\left( 2v-1 \right)$$

And return the random vector $\mathbf v$:

\begin{equation}
\mathbf v = \begin{bmatrix}
    \cos\theta ~ \sin\phi \\
    \sin\theta ~ \sin\phi \\
    \cos\phi
\end{bmatrix}
\end{equation}

[^1]: Weisstein, Eric W. "Sphere Point Picking." From MathWorld

--8<-- "includes/Abbreviations.md"