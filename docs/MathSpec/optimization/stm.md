# State Transition Matrix computation

Nyx uses dual number theory (i.e. automatic differentiation) to compute all state transition matrices (or Jacobian matrices) to machine precision without relying on finite differencing or error-prone manual derivations. All of the computations are handled by the [hyperdual](https://gitlab.com/chrisrabotin/hyperdual) Rust package, which I co-authored.

The following is an extract of the AAS-19-716 conference paper called _Application of Dual Number Theory to Statistical Orbital Determination_, by C. Rabotin [^1].

First, the mathematical notions of dual numbers and hyper-dual spaces is recalled, along with their error-free auto-differentiation properties. Subsequently, hyper-dual spaces are elegantly applied to statistical orbital determination problems, both for the computation of linearized dynamics, and for the sensitivity matrix of a Kalman filter. Further, a comparison of the execution speeds of the same statistical orbital determination problem using the hyper-dual space formulation and the traditional manual derivation formulation is provided.

## Dual numbers and hyper-dual space
### Dual number theory
Dual numbers are a type of complex numbers. The ubiquitous set of complex numbers, $\mathbb{C}$, may be defined as follows, where $i$ is the imaginary number:

\begin{equation} \mathbb{C}=\mathbb{R}[i]=\{z=a+bi~|~(a,b)\in\mathbb{R}^2,i^2=-1\} \end{equation}

Similarly, we may define the set of dual numbers as follows, where $\epsilon$ is the dual number:

$$\begin{equation} \mathbb{D}=\mathbb{R}[\epsilon]=\{z=a+b\epsilon~|~(a,b)\in\mathbb{R}^2,\epsilon^2=0 \text{~and~} \epsilon \neq 0\} \end{equation}$$

Moreover, for $z=a+b\epsilon$ where $z\in\mathbb{D},~(a,b)\in\mathbb{R}$, let us define the $real$ and $dual$ parts of a dual number such as

\begin{equation}
  \begin{cases}
    real(z) = a\\
    dual(z) = b
  \end{cases}
\end{equation}

An auto-differentiation property emerges from the addition of this nilpotent element, as is obvious from a Taylor series expansion. Evidently, this result is only valid for values of $a$ where the function is differentiable.

\begin{equation}
\begin{aligned}
f:\mathbb{D}\rightarrow\mathbb{D}~, (a,b)\in\mathbb{R}^2 &\\
f(a+b\varepsilon)
&=\sum_{n=0}^{\infty} {\frac{f^{(n)} (a)b^n \varepsilon^n}{n!}} \\
&= f(a)+b\frac{df(a)}{da}\varepsilon \\
&
\begin{cases}
    real(f(a+b\epsilon)) = f(a)\\
    dual(f(a+b\epsilon)) = b\frac{df(a)}{da}
  \end{cases}
\end{aligned}
\end{equation}

By choosing $b=1$, the first derivative comes out for free by simply evaluating the function $f$.

### Hyper-dual spaces
We can further extend the dual numbers to a hyper-dual space. Let us define a hyper-dual space of size 2 as follows, where $\epsilon_j$ is the $j$-th dual number:

\begin{equation} \mathbb{D}^2=\mathbb{R}[\epsilon_x, \epsilon_y]=\{z=a+b\epsilon_x+c\epsilon_y+d\epsilon_x\epsilon_y~|~(a,b,c,d)\in\mathbb{R}^4,\epsilon_\gamma^2=0,~\epsilon_\gamma \neq 0,~\gamma\in\{x,y\},~\epsilon_x\epsilon_y \neq 0\} \end{equation}

This mathematical tool enables auto-differentiation of multi-variate functions as follows, where $dual_\gamma$ corresponds to the $\gamma$-th dual number, i.e. the number associated with $\epsilon_\gamma$.

\begin{equation}
\label{dnintro}
\begin{aligned}
f:\mathbb{D}^2\rightarrow\mathbb{D}^2,~(x,y)\in\mathbb{R}^2 &\\
& 
\begin{cases}
    real(f(x+\epsilon_x,~y+\epsilon_y)) = f(x,y)\\
    dual_x(f(x+\epsilon_x,~y+\epsilon_y)) = \frac{\partial}{\partial x}f(x,y) \\
    dual_y(f(x+\epsilon_x,~y+\epsilon_y)) = \frac{\partial}{\partial y}f(x,y) \\
  \end{cases}
\end{aligned}
\end{equation}

### Example
Let us detail a computation example of a smooth multivariate polynomial function defined over all reals.

\begin{equation}
\begin{aligned}
f:\mathbb{R}\rightarrow\mathbb{R},~(x,y)\in\mathbb{R}^2 &\\
& f(x,y) = 2x^3-0.2y^2+x\\
& \frac{\partial}{\partial x} f(x,y) = 6x^2+1\\
& \frac{\partial}{\partial y} f(x,y) = -0.4y\\
\end{aligned}
\end{equation}

Let us extend the definition of this function to $\mathbb{D}^2$.

\begin{equation}
\begin{aligned}
g:\mathbb{D}\rightarrow\mathbb{D},~(x,y)\in\mathbb{R}^2 &\\
& g(x+\epsilon_x,~y+\epsilon_y) = 2(x+\epsilon_x)^3-0.2(y+\epsilon_y)^2+(x+\epsilon_x)
\end{aligned}
\end{equation}

Trivially,

\begin{equation}
\begin{aligned}
(x+\epsilon_x)^2 &= x^2 + 2x\epsilon_x\\
(x+\epsilon_x)^3 &= x^3 + 3x^2\epsilon_x
\end{aligned}
\end{equation}

Hence, $g$ may be written as follows:

\begin{equation}
\begin{aligned}
g(x+\epsilon_x,~y+\epsilon_y) &= 2(x+\epsilon_x)^3-0.2(y+\epsilon_y)^2+(x+\epsilon_x) \\
&= 2(x^3+3x^2\epsilon_x)-0.2(y^2+2y\epsilon_y)+(x+\epsilon_x) \\
&= (2x^3-0.2y^2+x)+(6x^2+1)\epsilon_x-0.4y\epsilon_y\\
\end{aligned}
\end{equation}

As expected, the $dual_x$ part of $g$ corresponds to the partial of $f$ with respect to $x$, the $dual_y$ part of $g$ corresponds to the partial of $f$ with respect to $y$, and the $real$ part of the $g$ corresponds to $f$.

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