# State noise compensation
Also called the process noise, the SNC artificially inflates the covariance of the filter such that the filter does not overly trust its own estimate (which can lead to filter divergence). This computation relies on a Taylor series approximation of the filter time integral. As such, all SNC are initialized with a "disable time" which will ignore the state noise compensation if the difference between the previous and next time updates is greater than that provided value. Proper selection of this disable time must be fine-tined to each application, and two minutes is usually a good initial guess.

Nyx supports a time-based series of SNCs such that, depending on the epoch of the filter, a specific SNC is used.

## Filter affects
The SNC only affects the computation of the propagated covariance in the filter. Let $Q$ be the process noise selected for this specific propagation of the covariance. The size of this square matrix is the same as the velocity components of the estimated state (i.e. usually 3 for spacecraft navigation). Let $\Delta t$ be the number of seconds between the epoch of the previous estimate and the upcoming filter epoch.

We start build the $\Gamma$ matrix as follows (assuming this is an SNC of size 3x3, but the code scales to any velocity size multiple of 3). [^1]

\begin{equation}
\Gamma = \begin{bmatrix}
    \frac {\Delta t^2}{2} & 0 & 0 \\
    0 & \frac {\Delta t^2}{2} & 0 \\
    0 & 0 & \frac {\Delta t^2}{2} \\
    \Delta t & 0 & 0 \\
    0 & \Delta t & 0 \\
    0 & 0 & \Delta t \\
\end{bmatrix}
\end{equation}

Then, we apply this SNC to the previously computed $\bar P$:

$$\bar P_i = \bar P_i + \Gamma Q \Gamma^T $$

## Kinds of SNC
Nyx supports two kinds of process noises. For now, the SNC is always computed in the same reference frame as the filter integration frame.

### Static diagonal
The SNC is defined as follows

$$Q = diag(q_i)$$

### Exponentially decaying diagonal
This can be used to prevent the filter from converging too quickly. It is computed as follows, where $\Delta t$ corresponds to the difference between the current filter epoch and the epoch at the start of the filter in seconds, and $\lambda_i$ corresponds to the $i$-th decay constant specified at the initialization of the SNC.

$$Q = diag(q_i\times\exp(-\lambda_i \Delta t))$$

[^1]: Many thanks to Sai Chikine for identifying and fixing the scaling of the computation of the SNC for larger estimated state sizes.

--8<-- "includes/Abbreviations.md"