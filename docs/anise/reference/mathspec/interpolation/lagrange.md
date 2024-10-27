This implementation computes both the Lagrange interpolation polynomial and its derivative at a specified point using Newton's divided difference method. The algorithm efficiently computes both values simultaneously through a single triangular computation scheme.

!!! tip
    Lagrange interpolation is particularly useful for trajectory interpolation when provided distinct states with their first order derivative, e.g., position and velocity. It is less commonly used in ephemeris interpolation than the [Hermite interpolation](./hermite.md).

## Foundation

For $n$ points $(x_i, y_i)$, the Lagrange interpolation polynomial $L(x)$ can be expressed using divided differences. The algorithm computes both:

$$ L(x) = \sum_{i=0}^{n-1} y_i \prod_{j=0,j\neq i}^{n-1} \frac{x - x_j}{x_i - x_j} $$

and its derivative:

$$ L'(x) = \sum_{i=0}^{n-1} y_i \sum_{k=0,k\neq i}^{n-1} \frac{1}{x_i - x_k} \prod_{j=0,j\neq i,k}^{n-1} \frac{x - x_j}{x_i - x_j} $$

## Algorithm

[Source code documentation](https://docs.rs/anise/latest/anise/math/interpolation/fn.lagrange_eval.html)

### Initialization

- Input: Points $(x_i, y_i)$ and evaluation point $x$
- Two working arrays:
    - `work`: stores function values
    - `dwork`: stores derivative values

### Divided Difference Table Construction

For each level $j = 1 \to n-1$:

For each index $i = 0 \to n-j-1$:

1. Compute coefficients:

    $$ x_i, x_{i+j} \text{ (interval endpoints)} $$

    $$ \text{denom} = x_i - x_{i+j} $$

2. Update function value:

    $$ \text{work}_i = \frac{(x - x_{i+j})\text{work}_i + (x_i - x)\text{work}_{i+1}}{\text{denom}} $$

3. Update derivative:

    $$ \text{deriv} = \frac{\text{work}_i - \text{work}_{i+1}}{\text{denom}} $$

    $$ \text{dwork}_i = \frac{(x - x_{i+j})\text{dwork}_i + (x_i - x)\text{dwork}_{i+1}}{\text{denom}} + \text{deriv} $$

## Output

Returns tuple $(f, f')$ where:

- $f = L(x)$: interpolated function value
- $f' = L'(x)$: interpolated derivative

## Error Handling

The implementation includes checks for:

- Array length consistency
- Non-empty input arrays
- Division by zero (minimum spacing of $\epsilon \approx 2.22 \times 10^{-16}$)

## Complexity

The algorithm achieves:

- Time complexity: $\mathcal{O}(n^2)$
- Space complexity: $\mathcal{O}(n)$

This implementation is particularly efficient as it computes both the interpolated value and its derivative in a single pass through the divided difference table, avoiding redundant calculations.