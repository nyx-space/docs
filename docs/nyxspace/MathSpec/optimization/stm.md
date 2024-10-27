The State Transition Matrix (STM, $\boldsymbol \Phi$) is a linearization tool for dynamical systems: it is a local approximation of the dynamics of the system.

In the field of astrodynamics, it is an approximation of the forces applied to the spacecraft over a short period of time. The STM is a necessary tool in orbit determination and in the circular restricted three-body problem (CRTBP), and may also be used in trajectory optimization.

For example, in orbit determination, the STM is computed from a propagated spacecraft state. It is considered a reasonable approximation of the forces acting on a spacecraft until the next time step (typically the next tracking measurement) through the time-propagation of the whole matrix.

## System Dynamics

Consider an orbital state $\boldsymbol{X}$ in a Cartesian frame, comprising position $\boldsymbol{r} = [x,y,z]$ and velocity $\boldsymbol{v} = [\dot{x}, \dot{y}, \dot{z}]$:

$$\boldsymbol{X} = \begin{bmatrix} x \\ y \\ z \\ \dot{x} \\ \dot{y} \\ \dot{z} \end{bmatrix}$$

The time derivative $\boldsymbol{\dot{X}}$ represents system dynamics:

$$\boldsymbol{\dot{X}} = F(\boldsymbol{X}, t)$$

For two-body problems, acceleration $\boldsymbol{\dot{v}}$ is $-\frac{\mu}{r^3}\boldsymbol{X}$. More complex dynamics extend $F$ to include additional state components. For example, when enabling [Solar Radiation Pressure (SRP)](../models/srp.md) estimation in Nyx, the state vector is expanded to include the coefficient of reflectivity $C_r$.

### Computation

The STM is computed via the partials matrix (or _Jacobian_) $\boldsymbol A$ of the state $\boldsymbol X$ at a time $t$. A first order Taylor series expansion is used to compute this Jacobian.

$$ \boldsymbol{\dot{X}} = \boldsymbol{\dot{X}^*} + \frac{\partial F (\boldsymbol{X^*})}{\partial \boldsymbol{\dot{X}}} \cdot \left( \boldsymbol{\dot{X}} - \boldsymbol{\dot{X}^*} \right) $$

where $\boldsymbol{X^*}$ is a reference state vector, e.g. the state at $t_0$.

In practice, this Jacobian is the matrix of partial derivatives of the acceleration of the system, forming the $A$ matrix, where $\boldsymbol{a_{x,y,z}}$ is the acceleration in the X, Y, and Z axes:

$$\boldsymbol A = \frac{d \boldsymbol X(t)}{d\boldsymbol X_0} = \begin{bmatrix} 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 \\ \frac{\partial a_x}{\partial x} & \frac{\partial a_y}{\partial x} & \frac{\partial a_z}{\partial x} & 0 & 0 & 0 \\ \frac{\partial a_x}{\partial y} & \frac{\partial a_y}{\partial y} & \frac{\partial a_z}{\partial y} & 0 & 0 & 0 \\ \frac{\partial a_x}{\partial z} & \frac{\partial a_y}{\partial z} & \frac{\partial a_z}{\partial z} & 0 & 0 & 0 \end{bmatrix}$$

## Dual Numbers and Hyper-Dual Spaces

Nyx computes STMs using dual number theory because it avoids manual derivation errors via its error-free auto-differentiation properties. This is implemented via the [hyperdual](https://github.com/christopherrabotin/hyperdual) Rust crate. Refer to the page on [Dual Number theory](../appendix/dual_numbers.md) for a primer on the topic.

### Application in Kalman Filtering and Orbit determination

In statistical orbital determination, the STM is computed around an orbit reference point and propagated forward. The partials matrix $\boldsymbol A(t)$ relates to the STM as:

$$\frac{d {\boldsymbol \Phi}(t, t_0)}{dt} = \boldsymbol A(t)\boldsymbol \Phi(t, t_0)$$

Refer to the [Kalman filtering](../orbit_determination/kalman.md) page for details on how the state transition matrix is used in orbit determination in Nyx.

Dual numbers provide these derivatives directly from equations of motion, enabling efficient computation even in complex systems. For details, refer to the AAS-19-716 conference paper _Application of Dual Number Theory to Statistical Orbital Determination_, Rabotin.

[^1]: For detailed STM discussion, refer to section 1.2.5 and 4.2.1. "Statistical Orbit Determination" by Tapley et al., Elsevier 2004.

--8<-- "includes/Abbreviations.md"