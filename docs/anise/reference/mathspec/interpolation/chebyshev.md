This implementation efficiently evaluates a Chebyshev polynomial and its derivative using Clenshaw's recurrence formula. The algorithm is optimized for numerical stability and computational efficiency.

!!! tip
    Chebyshev interpolation requires building the Chebyshev polynominal coefficients for each spline of each coordinate of a trajectory. Chebyshev interpolations poorly handle accelerations and as such are not suitable for ephemerides with any kind of eccentricity. They are most commonly used in the interpolation of planetary motion.

## Foundation

For Chebyshev polynomials $T_n(x)$ with coefficients $c_n$, the polynomial is:

$$ P(x) = \frac{c_0}{2} + \sum_{n=1}^N c_n T_n(x) $$

where $T_n(x)$ satisfies the recurrence relation:

$$ T_{n+1}(x) = 2xT_n(x) - T_{n-1}(x) $$

## Algorithm

### Initialization

- Input: 
    - Normalized time $x \in [-1,1]$
    - Coefficients $c_n$
    - Spline radius $r_s$
    - Polynomial degree $N$
- Two three-element working arrays:
    - `w`: for function values
    - `dw`: for derivative values

### Clenshaw Recurrence

For $j = N \to 2$:

1. Function value recurrence:

    1. $w_2 = w_1$
    2. $w_1 = w_0$
    3. $w_0 = c_j + 2xw_1 - w_2$
     
1. Derivative recurrence:

    1. $w_2 = w_1$
    2. $w_1 = w_0$
    3. $dw_0 = 2w_1 + 2xdw_1 - dw_2$

### Final Computation

1. Function value:

    $$ f(x) = c_0 + xw_0 - w_1 $$

2. Derivative (scaled by spline radius):

    $$ f'(x) = \frac{w_0 + xdw_0 - dw_1}{r_s} $$

## Error Handling

The implementation checks for:

- Non-zero spline radius
- Availability of coefficients at requested indices
- Valid evaluation epoch

## Complexity

- Time complexity: $\mathcal{O}(N)$
- Space complexity: $\mathcal{O}(1)$ (fixed-size working arrays)

## Key Features

1. **Numerical Stability**: Uses Clenshaw's algorithm instead of direct polynomial evaluation
2. **Memory Efficiency**: Uses fixed-size arrays of length 3
3. **Simultaneous Computation**: Evaluates both polynomial and derivative in a single pass
4. **Scale Handling**: Accounts for spline radius in derivative computation

This implementation is particularly efficient for high-degree polynomials while maintaining numerical stability through the use of Clenshaw recursion.