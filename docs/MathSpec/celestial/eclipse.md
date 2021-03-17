# Eclipse
The eclipse computation in Nyx is an original method I could not found in the literature (but it might be similar to the dual-cone method).[^1] But, it matches GMAT with very good accuracy. The line of sight computation is from Vallado 4th edition.

In summary, we compute the intersection of the circles formed from the apparent radii of the light source and the eclipsing body.

An eclipse state is represented in Nyx as an enum whose accepted values are `Visibilis`, `Umbra`, and `Penumbra(f64)`, where the floating point value in the `Penumbra` variant corresponds to the percentage of visibility: closer to one means that spacecraft sees the light source almost in total visibility, and closer to zero means that the spacecraft barely sees the light source.

!!! note
    This method is applicable to any light source and any eclipsing body which is a geoid. However, it _assumes_ that the geoid is spherical, so this will return an incorrect value for celestial bodies that aren't nearly spherical.

## Nomenclature
+ $\mathbf{r_E}$: radius vector of the spacecraft to the eclipsing body
+ $\mathbf{r_L}$: radius vector of the light source to the spacecraft
+ $R_E$: equatorial radius of the eclipsing body
+ $R_L$: equatorial radius of the light source
+ $r_E'$: apparent radius of the eclipsing body
+ $r_L'$: apparent radius of the light source
+ $d'$: apparent separation of the centers of the circles formed by the aforementioned apparent radii

![eclipse geometry](/assets/figures/eclipse.png)

<span class="center" style="text-align:center"><b>Figure 1</b>: eclipse computation geometry</span>

!!! note
    The celestial objects are considered spherical here allowing the angle formed from the equatorial radius to the spacecraft to objected vector to be a right angle. That is why the apparent angle is computed using the sine.

## Derivation
The `eclipse_state` function requires an observer orbit, a light source (as a `Frame`), and an eclipsing body (also as a `Frame`).

Start by computing the radii vectors $\mathbf{r_E}$ and $\mathbf{r_L}$ by converting the observer orbit into those frames (and negating the vector of $\mathbf{r_L}$).

Compute the apparent radii as follows:

$$ r_L' = \sin^{-1} \frac {R_L} {||\mathbf{r_L}||}$$

$$ r_E' = \sin^{-1} \frac {R_E} {||\mathbf{r_E}||}$$

??? note "Note on $\sin^{-1}$"
    If the spacecraft is "flying" inside either the eclipsing body or the light source, then the equatorial radius of the celestial object will be larger than the distance of the spaceraft to said celestial body. Hence, the $\sin^{-1}$ call would fail (and return NaN): Nyx will _not_ fail on this case on purpose. In this case, we set the apparent radii to equatorial radius of that celestial body.

Compute the apparent separation of both circles, as per [Weisstein, Eric W. "Circle-Circle Intersection." From MathWorld--A Wolfram Web Resource](https://mathworld.wolfram.com/Circle-CircleIntersection.html).

$$ d' = \cos^{-1} \left( - \frac {\mathbf{r_L}\cdot \mathbf{r_E}} { ||\mathbf{r_L}|| ||\mathbf{r_E}|| } \right)$$

Then, apply the circle-circle intersection computation, as referred just above.

If $d' - r_L' < r_E'$, the closest point of the apparent radius of the light source is further away than the furthest point of the apparent radius of eclipsing body, therefore the light source is fully shining on the spacercraft. The function returns `Visibilis`.

If $r_E' > d' + r_L'$, the light source is fully hidden by the eclipsing body, so we're in total eclipse. The function returns `Umbra`.

If $r_L' - r_E' \geq d'$ _or_ $d' \geq r_L' + r_E'$, the spacecraft is in an annular eclipse. Therefore, the function returns `Penumbra` where the percentage of penumbra is computed as follows

$$ P = 1.0 - \frac {(r_E')^2} {(r_L')^2}$$

_Else_, comes the complicated part because the spacecraft is in the penumbra and we want to computate the penumbra percentage. We're just using the circle-circle intersection method from Wolfram above.

Start by computing the distance of the chord connecting the cusps of the lens created by the overlapping circles. Now would be a good time to open the Wolfram link to follow along with their figures.

$$ d_1 = \frac {(d')^2 - (r_L')^2 + (r_E')^2} {2d'}$$

$$ d_2 = \frac {(d')^2 + (r_L')^2 - (r_E')^2} {2d'}$$

Then, compute the shadow area for both circles using $(r_E', d_1)$ and $(r_L', d_2)$ as parameters to the following function.

$$\mathcal{A}(r, d) = r^2 \cos^{-1}\left(\frac{d}{r}\right) - d\sqrt{r^2-d^2}$$

And the total shadow area:

$$\mathcal{A}_T = \mathcal{A}(r_E', d_1) + \mathcal{A}(r_L', d_2)$$

Since we assume the light source and the eclipsing body to be spherical, their projections are perfect circles. So we can compute the penumbra percentage as follows, where $\mathcal{A}^*$ is the nominal circle area of the light source if there were no eclipsing body.

$$\mathcal{A}^* = \pi (r_L')^2$$

$$ P = \frac {\mathcal{A}^* - \mathcal{A}_T} {\mathcal{A}^*} $$

!!! note
    At the start of the algorithm, if the equatorial radius of the light source (not the eclipsing body), then the position of the light source is computed and the line of sight function is called instead, with the light source as an observed orbit structure.


## Special case: line of sight
The `line_of_sight` function expects an `observer`, an `observed` orbit, and an eclipsing body (as a `Frame`).

We start by converting the observed and observer states to the same frame as the eclipsing body, respectively $\mathbf{r_1}$ and $\mathbf{r_2}$.

Define the following dot products:

$$ r_1^2 = \mathbf{r_1}\cdot \mathbf{r_1}$$

$$ r_2^2 = \mathbf{r_2}\cdot \mathbf{r_2}$$

$$ r_{12} = \mathbf{r_1}\cdot \mathbf{r_2}$$

Compute $\tau$ as follows:

$$ \tau = \frac {r_1^2 - r_{12}} {r_1^2+r_2^2-2r_{12}}$$

Check the LOS boolean conditions, where $R_\circ$ is the equatorial radius of the eclipsing body:

$$ \mathcal{L}_0 := \tau \not\in [0;1] $$

$$ \mathcal{L}_1 := (1-\tau) r_1^2 + r_{12} \tau > R_\circ^2$$

If $\mathcal{L}_0 \vee \mathcal{L}_1$, the eclipsing body is _not_ in the way of both observers.

!!! note
    This is the Algorithm 35 of Vallado, 4th edition, page 308.

??? check "Validation"
    The most crucial validation of the penumbral calculation is in the SRP modeling. You may find the validation cases [here](/MathSpec/models/srp/).

    Nyx has two line of slight verification cases (to check for boundary cases). You may run these with `RUST_BACKTRACE=1 cargo test --release -- los_ --nocapture`. These test cases were initial designed to confirm the modeling for CAPS.

    Nyx also has two basic verification scenarios where the number of eclipse state changes is count for a LEO and a GEO spacecraft and verified against some expected data.

[^1]: Surprisingly I could not find many references on how to compute this.

--8<-- "includes/Abbreviations.md"