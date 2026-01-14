Covariances are matrices of expected values, e.g., the square of standard deviations, and are therefore positive semi-definite (PSD) matrices.
In the case of the CCSDS OEM files, they represent the uncertainty of a Cartesian position and velocity, in either an inertial frame or an orbit-local frame like the [RIC frame](/nyxspace/MathSpec/celestial/coord_systems/#ric-frame).

## Foundation

ANISE 0.9.0 introduced covariance interpolation using a **Log-Euclidean Riemannian Interpolation** method, which might be novel in the astrodynamics community. Unlike standard linear element-wise interpolation, this approach
respects the geometric manifold of Symmetric Positive Definite (SPD) matrices. This guarantees:

1. **Positive Definiteness:** The interpolated covariance matrix is always mathematically valid (all eigenvalues are strictly positive)

2. **Volume Preservation:** It prevents the artificial "swelling" (determinant increase) of uncertainty that occurs when linearly interpolating between two valid matrices. The interpolation follows the "geodesic" (shortest path) on the curved surface of covariance matrices.


## Algorithm

_Note:_ While covariances only need to be PSD, this method only works for positive definite matrices, i.e. none of the eigenvalues of the matrix may be zero due to the use of the natural logarithm.

1. Find the nearest covariance before and after the requested epoch, storing the epochs $t_0$ and $t_1$ of the nearest records whose covariance is respectively $P_0$ and $P_1$
2. **Frame rotation:** Rotate each of these covariances into the desired frame (e.g. if the user wants the interpolated matrix in the RIC frame, rotate both covariances into the RIC frame before proceeding as they are _stable_ points of the interpolation)
3. For each matrix $P \in \{P_0, P_1\}$ :
    1. Perform the Eigendecomposition of the matrix, building a matrix with the eigenvectors and a diagonal matrix of the associated eigenvalues:

        $$ P = Q \Lambda Q^T $$

    1. Ensure all eigenvalues are positive
    1. Compute the matrix natural logarithm of diagonal matrix, which is simply the natural log of each diagonal element:

        $$ \Lambda ' = \text{diag}(\ln(\lambda_i)) $$

    1. Reconstruct the matrix logarithm by mapping the diagonal log-eigenvalues back using the original eigenvectors:

        $$ \ln(P) = Q \Lambda ' Q^T $$

4. **Interpolate:** Linearly interpolate in the natural logarithm domain after computing the blending factor for the requested epoch:

    $$ \ln(P_k) = (1 - \alpha) \ln(P_0) + \alpha \ln(P_1) $$

5. **Map to Manifold:** Compute the exponential of the interpolated matrix:

    1. Perform Spectral Decomposition on the result from Step 4:

        $$ \ln(P_k) = Q_k \Lambda_k' Q_k^T $$

    2. Exponentiate the diagonal eigenvalues:

        $$ \Lambda_k = \text{diag}(\exp(\lambda_{k,i}')) $$

    3. Reconstruct the final covariance:

        $$ P_k = Q_k \Lambda_k Q_k^T $$


## Scalar example

Let $P(0) = \sigma^2_0 = 1$ and $P(1) = \sigma^2_1 = 100$.

With a basic linear interpolation, we would find the half-way covariance to be:

$$ P(0.5) = \frac{\sigma^2_0 + \sigma^2_1}{2} = 50.5 $$

Which leads to a variance of:

$$ \sigma_{0.5} = \sqrt{50.5} \simeq 7.10 $$

At the halfway mark, the standard deviation should not be 70% of the final standard deviation.
Since uncertainty grows geometrically, the halfway point should be between 1 and 10.

**In other words, the uncertainty swells artificially, creating a larger volume than physically warranted.**

Let's compute the same covariance with the Log-Euclidean interpolation method.

$$ P(0.5) = \exp(0.5 \ln(1) + 0.5 \ln(100)) = 10 $$

Which leads to a standard deviation of $\sigma_{0.5} \simeq 3.16$.

When considering that a covariance represents a volume, we note that the Log-Euclidean method interpolates the volume log-linearly, preventing the artificial volume inflation seen in linear interpolation.
