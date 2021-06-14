# Filter iteration
Nyx supports iterations by smoothing the estimates first and then iterating on the measurements.

The algorithm is straight-forward:

1. Smooth all estimates, or until the end of the smoothing arc (cf. [smoothing](/MathSpec/navigation/smoothing/)).
2. Process all of the measurements sequentially forward in time via the [measurement update](https://nyxspace.com/MathSpec/navigation/kalman/#measurement-update) call of the OD Process.

## Iteration until convergence

This allows iterating the filter until one of the following conditions are met:

1. The averaged RMS of the residuals is less than some threshold (defaults to `1e-3`); or
1. The difference between the best averaged RMS of the residuals of one iteration and that of the latest averaged RMS normalized by the best average RMS is less than some threshold (defaults to `1e-4`); or
1. The maximum number of iterations until the above convergence criteria is met (defaults to `15`); or
1. The average RMS of the residuals increases after each iterations until a maximum number of iterations (defaults to `3`).

Whether to use the prefit or the postfit (cf. [nomenclature](/MathSpec/navigation/kalman/#nomenclature)) is defined in configuration of the iteration function call. By default, Nyx will use the postfit residuals.

!!! info "Average root mean square of postfit residual"
    It is defined as follows, where $\hat{z_i}$ is the postfit $i$-th residual normalized by the measurement noise $R_i$ at that epoch:

    $$ \text{RMS} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} \mathbb{\hat{z_i}}\cdot \mathbb{\hat{z_i}} }$$

    We normalize the postfits for the dot product to be unitless (otherwise it would be a mix of units if the measurements have different units).

!!! warning
    In practice, an EKF does not need iteration, only a CKF _might_ benefit from one.

--8<-- "includes/Abbreviations.md"