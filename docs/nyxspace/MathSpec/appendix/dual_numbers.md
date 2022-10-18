# Dual numbers and hyperdual space
## Dual number theory
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

## Hyperdual spaces
We can further extend the dual numbers to a hyperdual space. Let us define a hyperdual space of size 2 as follows, where $\epsilon_j$ is the $j$-th dual number:

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

## Example
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

## Computation
All hyperdual computations are handled by the [hyperdual](https://crates.io/crates/hyperdual) Rust crate, co-authored by Chris Rabotin.