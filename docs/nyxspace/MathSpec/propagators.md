# Propagators
Nyx provides [several](https://docs.rs/nyx-space/latest/nyx_space/propagators/index.html) implicit [Runga-Kutta methods](https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods#Explicit_Runge%E2%80%93Kutta_methods) for solving ordinary differential equations.

## Default configuration
The default (and recommended) propagator is an adaptive-step Runge Kutta 89 configured as follows:

 + Step size controller (`ErrorCtrl`) is RSS Cartesian Step (GMAT's default)
 + Initial step size: 60.0 seconds
 + Minimum step size: 0.001 seconds
 + Maximum step size: 2700.0 seconds
 + Tolerance: 1e-12
 + Step size attempts: 50

## Error control
The error control is used to determine the time of the next step the propagator should take. It is only used in adaptive step propagators and relies on the error evaluation coefficients of said propagator. This method is used _during_ the computation of the next state to assess whether the step taken was too large.

The error control takes the estimated state error ($\mathbf{\tilde{E}}$), the candidate state vector ($\mathbf{C}$), and the current state ($\mathbf{S}$), does some fancy computation (detailed below), and returns a single floating point number corresponding to the error.

$$ f: (\mathbb{R}^n, \mathbb{R}^n, \mathbb{R}^n) \to \mathbb{R}, \quad n \in \mathbb{N} $$

If that error is larger than the tolerance of the propagator, the candidate state is rejected and a new intermediate step is computed and evaluated. This process repeats itself until either the tolerance is below the tolerance threashold of the propagator instance, or the maximum number of step size attempts is reached. If the maximum attempts is reached, a warning will be printed to the logs and the propagator will continue with this state.

### RSS Step
1. Compute the norm of the difference between the candidate state and the current state

    $$ |\mathbf{C} - \mathbf{S} | $$

1. If that magnitude is greater than $\sqrt{0.1}$, the error is evaluated as

    $$\frac {|\mathbf{C} - \mathbf{S} |} {|\mathbf{\tilde{E}}|}$$

1. Else, the error is simply $|\mathbf{\tilde{E}}|$

### RSS State
1. Compute the half of the sum of the candidate state and the current state

    $$ 0.5 \times |\mathbf{C} + \mathbf{S} | $$

1. If that magnitude is greater than $0.1$, the error is evaluated as

    $$\frac {|\mathbf{C} - \mathbf{S} |} {|\mathbf{\tilde{E}}|}$$

1. Else, the error is simply $|\mathbf{\tilde{E}}|$

### Step size computation
Upon a successful step taken by the propagator, we'll try to increase the step size for the next step. Let $\epsilon$ be the propagator tolerance, $\delta$ be the error of the previous step taken (cf. above), and $m$ be the order of the Runga Kutta method. Further, let $s_i$ be the current step size in seconds and $s_{i+1}$ be the step size computed for the next step.

$$ s_{i+1} = 0.9\times s_i \times \left(\frac{\epsilon}{\delta}\right)^{\frac{1}{m}}$$

If the proposed step $s_{i+1}$ is greater than the maximum step size configured in the propagator, then it is capped to that value.

??? info "Memory allocations"
    1. The propagators requires a single memory allocation on the creation of a `PropInstance`, i.e. on the call `propagator_setup.with(some_state)`. This is used to create the buffer of stages for the intermediate steps. Note that this buffer is reused throughout the integration.
    1. The dynamical model used in the propagator must be in an `Arc` (Atomically Reference Counted), which moves the dynamical model to the heap. This is also done _once_ prior to the call to the propagator.


--8<-- "includes/Abbreviations.md"