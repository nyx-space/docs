This implementation computes the Hermite interpolation of a function given a set of points and their derivatives. The algorithm constructs and evaluates both the interpolated function value and its derivative at a specified point.

!!! tip
    Hermite interpolation is particularly useful for trajectory interpolation when provided distinct states with their first order derivative, e.g., position and velocity.

!!! note
    This algorithm differs from the conventional method found in literature as it prevents ringing (aliasing) at specific abscissas. [This test from the original NASA SPICE](https://github.com/nyx-space/anise/blob/0524a6aaa60cca08856260d445b0c53fa6f5c000/anise/src/math/interpolation/hermite.rs#L218) documentation checks that the implementation is free from this ill-behavior.

## Foundation

Given $n$ points $(x_i, y_i)$ and their derivatives $y'_i$, the Hermite interpolation constructs a polynomial that matches both the function values and derivatives at each point. The interpolation is built using a divided difference table approach.

## Algorithm

[Source code documentation](https://docs.rs/anise/latest/anise/math/interpolation/fn.hermite_eval.html)

### Initialization

- Input: Points $(x_i, y_i)$, derivatives $y'_i$, and evaluation point $x$
- Constraints: $n \leq 32$ points, no duplicate abscissas
- Working array initialized as $2n \times 4n$ matrix

### First Column Construction

The initial column alternates between function values and derivatives:

$$ \text{work}_{2i} = y_i $$

$$ \text{work}_{2i+1} = y'_i $$

### Second Column Computation

For each pair of consecutive points $(i-1, i)$:

1. Compute coefficients:

    1. $c_1 = x_i - x$
    1. $c_2 = x - x_{i-1}$
    1. $\text{denom} = x_i - x_{i-1}$
   
2. Linear interpolation:

    $$ \text{work}_{i-1} = \frac{c_1y_{i-1} + c_2y_i}{\text{denom}} $$

### Higher-Order Differences

For columns $j = 2 \to 2n-1$:

1. Compute divided differences using:

    $$ \text{work}_{i-1} = \frac{(x_{i+j-1} - x)\text{work}_{i-1} + (x - x_i)\text{work}_i}{x_{i+j-1} - x_i} $$
   
2. Derivative updates:

    $$ \text{work}_{i+2n-1} = \frac{c_1\text{work}_{i+2n-1} + c_2\text{work}_{i+2n} + (\text{work}_i - \text{work}_{i-1})}{\text{denom}} $$

## Output

The algorithm returns a tuple $(f, f')$ where:

- $f$ is the interpolated function value at $x$
- $f'$ is the interpolated derivative at $x$

## Error Handling

The implementation includes robust error checking for:

- Array length consistency
- Maximum sample limit (32 points)
- Division by zero (minimum spacing of $\epsilon \approx 2.22 \times 10^{-16}$)

## Complexity

- Time complexity: $\mathcal{O}(n^2)$
- Space complexity: $\mathcal{O}(n^2)$

This algorithm maintains numerical stability through careful handling of divided differences.