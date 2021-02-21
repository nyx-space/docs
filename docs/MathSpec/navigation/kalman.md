# Kalman filter
The Kalman Filter in Nyx is a sequential filter which can switch between conventional (CKF) and extended filtering (EKF). Both kinds of filters support a _time update_ and _measurement update_ functionality, respectively a "covariance propagation/inflation" step without any new system measurement and a new state estimate and covariance computation provided a measurement of the system.

The only algorithmic difference between a CKF and EKF is that, after a measurement update, the EKF will consider the state estimate as the new reference state of the system. On the contrary, the CKF will only keep track of the state deviation from the reference state and not change the propagator state.

Nyx performs a Joseph update for the covariance[^1]. Nyx does **not** use a UDU factorization for the covariance (cf. [this pull request](https://github.com/dimforge/nalgebra/pull/766) on the linear algebra library used by Nyx and [this issue](https://gitlab.com/chrisrabotin/nyx/-/issues/164) on the repo).

Moreover, Nyx no longer support a square root information filter &mdash; if that is important to your application, reach out as it should not be too difficult to update the pre-1.0 code to the latest version of Nyx.

!!! note
    Please read the [SNC](/MathSpec/navigation/snc/) MathSpec for details on the state noise compensation / process noise.

### Nomenclature
+ $\Phi(t_i,~t_{i+1})$ : state transition matrix from time $t_i$ to time $t_{i+1}$
+ $\mathbf{X}$: the estimated state
+ $\mathbf{X}^*$: the reference state
+ $\mathbf{\bar X}$: the propagated estimated state
+ $\mathbf{\hat X}$: the new estimated state after a measurement update
+ $\mathbf{Y}$: the system measurement vector
+ $y$: the measurement deviation, or prefit residual
+ $z$: the postfit residual
+ $\mathbf{G(\mathbf{X_i})}$: the computed measurement, i.e. the measurement computed from the estimated state
+ $R$: the measurement noise
+ $P$: the covariance matrix
+ $\bar P$: the propagated covariance matrix
+ $K$: the Kalman gain at
+ $\tilde H$: the measurement sensitivity matrix
+ $I_n$: the identity matrix of size _n_
+ $\gamma_i$: whatever the parameter $\gamma$ represents at time $i$

## Time update
The time update (also called prediction step) allows to propagate the filter covariance and state deviation by one linearized step by multiplying the STM with the previously computed state deviation and covariances.

$$\mathbf{\bar X_i} = \Phi(t_i,~t_{i+1}) \mathbf{\bar X_{i-1}}$$

$$\bar P_i = \Phi(t_i,~t_{i+1})P_{i-1}\Phi(t_i,~t_{i+1})^T$$

!!! note
    For an EKF, the state deviation is necessarily zero because we update the reference trajectory at each measurement update.

## Measurement update
The measurement update will compute a new state estimate, its covariance, and its pre-fit and post-fit residuals.

1. Propagate the covariance

    $$\bar P_i = \Phi(t_i,~t_{i+1})P_{i-1}\Phi(t_i,~t_{i+1})^T$$

1. Compute the measurement deviation, or pre-fit residual [^2]:

    $$y_i=\mathbf{Y_i}-G(\mathbf{X_i})$$

1. Compute the measurement sensitivity (using automatic differentiation):

    $$\tilde H_i = \frac{\partial G(\mathbf{X_i})}{\partial \mathbf{X_i}}$$

1. Compute the Kalman gain

    $$K_i = \bar P_i \tilde H_i^T (\tilde H_i \bar P_i \tilde H_i^T+R_i)^{-1}$$

1. Compute the post-fit residual
    1. If in CKF mode, start with a time update of the state, as detailed in the previous section, then:

        $$z_i = y_i - \tilde H_i \mathbf{\bar X_i}$$

    2. If in EKF mode,

        $$z_i = y_i - K_i y_i$$

1. Compute the new state estimate
    1. If in CKF mode,

        $$\mathbf{\hat X_i} = \mathbf{\bar X_i} + K_i z_i$$

    1. If in EKF mode,

        $$\mathbf{\hat X_i} = K_i y_i$$

1. Finally, compute the new covariance (Joseph update) where the size of the identity matrix matches that of the estimated state

    $$P_i = (I_n - K_i \tilde H_i) \bar P_i (I_n - K_i \tilde H_i)^{-1} + K_i R_i K_i^T $$

[^1]: Thanks for Sai Chikine for implementing this formulation.
[^2]: This should really be called the "surprise factor" because it's big it means our estimate state is far off the real state and we should be surprised.

--8<-- "includes/Abbreviations.md"