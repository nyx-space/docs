# Measurement generation
Nyx allows custom implementations of a `MeasurementDevice`, which this MathSpec cannot cover. Therefore, this page focuses on the implementation for `GroundStation`: this is the structure used for the default orbit determination setups which rely on Earth based ground stations.

## Range and range-rate calculation
The embeded ground stations are initialized with a latitude $\phi$, a longitude $\lambda$, a height $h$, an elevation mask, a range noise level and a range-rate noise level.

The position of this ground station is converted into the frame of the spacecraft to generate a measurement between a spacecraft ($r$, for receiver) and a ground station ($t$, for transmitter). In the following, the subscript $r$ corresponds to the radius of that orbital state and $v$ the velocity vector of that state. Further, if a symbol has a frame associated to it, e.g. $^{\text{SEZ}}\mathbf{\rho}$, then it is a vector (the bold font may not that visible).

The range in the IAU Earth fixed frame is then computed:

$$^{\text{IAU Earth}}\mathbf{\rho} = \mathbf{r}_r - \mathbf{t}_r$$

That range vector is then converted in the SEZ frame using the algorithm from Vallado, where $R_i$ corresponds to a rotation by the $i$-th axis:

$$^{\text{SEZ}}\mathbf{\rho} = R_2\left(\frac \pi 2 - \phi\right)~R_3(\lambda)~\cdot~^{\text{IAU Earth}}\mathbf{\rho}$$

The elevation is then computed as follows:

$$ el= \sin^{-1}\left(\frac {^{\text{SEZ}}\mathbf{\rho_z}}{|^{\text{SEZ}}\mathbf{\rho}|}\right) $$

A Gaussian/normal PDF is sampled with the range and range-rate noises to noise-up the true range and range rate computations, respectively noted $\mathcal{N}(\rho)$ and $\mathcal{N}(\dot\rho)$. The range is computed trivially computed:

$$\rho = |^{\text{SEZ}}\mathbf{\rho}| + \mathcal{N}(\rho)$$

And the range-rate is computed as:

$$\dot\rho = ^{\text{SEZ}}\mathbf{\rho} \cdot \frac{(\mathbf{r}_v - \mathbf{t}_v)}{\rho} + \mathcal{N}(\dot\rho)$$

## Measurement sensitivity matrix
In a Kalman filter, the sensitivity matrix, noted $\tilde{H}$, relates the filter covariance, the filter gain, the measurements and the noise of the measurement. Like the state transition matrix, the sensitivity matrix is a partials matrix of size $N\times M$, where $N$ is the size of the measurement and $M$ is the size of the state to be estimated. For example, if the measurement is the range $\rho$ and the range-rate $\dot{\rho}$, and the estimated state is the position $\{x,y,z\}$ and velocity $\{\dot x, \dot y, \dot z\}$, then the sensitivity matrix is written as follows.

\begin{equation}
\label{sensitivity}
\tilde H = \begin{bmatrix}
    \frac{\partial \rho}{\partial x} & \frac{\partial \rho}{\partial y} & \frac{\partial \rho}{\partial z} & \frac{\partial \rho}{\partial \dot x} & \frac{\partial \rho}{\partial \dot y} & \frac{\partial \rho}{\partial \dot z} \\
    \frac{\partial \dot \rho}{\partial x} & \frac{\partial \dot \rho}{\partial y} & \frac{\partial \dot \rho}{\partial z} & \frac{\partial \dot \rho}{\partial \dot x} & \frac{\partial \dot \rho}{\partial \dot y} & \frac{\partial \dot \rho}{\partial \dot z} \\
\end{bmatrix}
\end{equation}

Using the same methodology as previously, it is evident that the sensitivity matrix may be computed by simply defining a hyper-dual space whose size is equal to that of the state to be estimated. The equations which return the range $\rho$ and the range-rate $\dot\rho$ from an input state will then automatically also return the components of the sensitivity matrix.

!!! note
    The ground stations currently do not support light-time corrections or tropospheric attenuations. This will be part of the 1.1.0 release.