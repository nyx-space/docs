# State Transition Matrix computation

Nyx uses dual number theory (i.e. automatic differentiation) to compute all state transition matrices (or Jacobian matrices) to machine precision without relying on finite differencing or error-prone manual derivations. All of the computations are handled by the [hyperdual](https://gitlab.com/chrisrabotin/hyperdual) Rust package, which I co-authored.

The following is an extract of the AAS-19-716 conference paper called _Application of Dual Number Theory to Statistical Orbital Determination_, by C. Rabotin [^1].

First, the mathematical notions of dual numbers and hyper-dual spaces is recalled, along with their error-free auto-differentiation properties. Subsequently, hyper-dual spaces are elegantly applied to statistical orbital determination problems, both for the computation of linearized dynamics, and for the sensitivity matrix of a Kalman filter. Further, a comparison of the execution speeds of the same statistical orbital determination problem using the hyper-dual space formulation and the traditional manual derivation formulation is provided.

Please refer to [Dual Numbers](../appendix/dual_numbers.md) for a primer on dual number theory.

## Applying hyper-dual space to statistical orbital determination using Kalman filtering
### The state transition matrix
The state transition matrix (STM, $\boldsymbol \Phi$) is a linearization procedure of a dynamical system. In the field of astrodynamics, it is an approximation of the dynamics over a short period of time. In the case of statistical orbital determination, the STM is computed around a reference point of an orbit and propagated forward in time until the next propagation time step or until the next spacecraft observation. The STM is computed via the partials matrix $\boldsymbol A$ of the state $\boldsymbol X$ at a time $t$, as shown earlier.

\begin{equation}
\label{grad_stm}
\boldsymbol A(t) = \frac{d \boldsymbol X(t)}{d\boldsymbol X_0}
\end{equation}

If one only estimates the spacecraft state, then the partials matrix corresponds to the gradient of the orbital dynamics applied to the spacecraft. The state $\boldsymbol X$ of a spacecraft may be defined as the vector of its position and velocity in a Cartesian frame. The equation below shows the relation between the partials matrix and the STM, where $t$ and $t_0$ correspond to two different times such that $t>t_0$.

\begin{equation}
\label{stm_def}
\frac{d {\boldsymbol \Phi}(t, t_0)}{dt} = \boldsymbol A(t)\boldsymbol \Phi(t, t_0)
\end{equation}

The $\boldsymbol A$ matrix contains the partial derivatives of the accelerations ($a_x,~a_y,~a_z$) with respect to each of the components of the position of the spacecraft, cf. the next equation.

\begin{equation}
\label{tb_partials}
\boldsymbol A = \begin{bmatrix}
    0 & 0 & 0 & 1 & 0 & 0 \\
    0 & 0 & 0 & 0 & 1 & 0 \\
    0 & 0 & 0 & 0 & 0 & 1 \\
    \frac{\partial a_x}{\partial x} & \frac{\partial a_y}{\partial x} & \frac{\partial a_z}{\partial x} & 0 & 0 & 0 \\
    \frac{\partial a_x}{\partial y} & \frac{\partial a_y}{\partial y} & \frac{\partial a_z}{\partial y} & 0 & 0 & 0 \\
    \frac{\partial a_x}{\partial z} & \frac{\partial a_y}{\partial z} & \frac{\partial a_z}{\partial z} & 0 & 0 & 0 \\
\end{bmatrix}
\end{equation}

In the case of two-body dynamics, the $\boldsymbol A$ matrix is relatively simple to compute. Deriving this partials matrix for higher fidelity dynamics or for a larger state is more complicated. In practice, this may lead orbital estimation software to ignore part of these dynamics. Navigators may then account for smaller perturbations by inflating the covariance matrix with stochastic noise.

Dual numbers, however, provide the partials matrix as part of the computation of the equations of motion (EOM) themselves, as long as these EOMs describe the movement of all of the state variables to be estimated. In practice, this requires defining a hyper-dual space whose size is equal to the number of variables in the state to be estimated. For example, if estimating the Cartesian state a spacecraft and a maneuver magnitude at a reference point during an orbital determination arc, building a seven-dimensional dual space will return the result of the EOMs and the partials matrix computed at that point. An open source example of the building of such hyper-dual space has been implemented as a test case in \textit{dual\_num}, a thorough dual number library in a programming language called Rust.


[^1]: That's me. `\o/`

--8<-- "includes/Abbreviations.md"