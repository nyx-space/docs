# Smoothing estimates

!!! bug
    The SNC is not accounted for in the smoothing process.

## Smoothing arc
For smoothing, Nyx requires the definition of a smoothing arc. This decides which measurements are part of the current OD arc, i.e. tells the smoother when to stop consuming the previous estimates.

Four types of arcs are supported:

1. All estimates computed by the filter;
1. All estimates coming from a measurement update, i.e. as soon as a "prediction" estimate is encountered (as opposed to a "measurement update"), stop consuming the estimates into the smoother;
1. All estimates whose epoch is after a provided datetime;
1. All estimates until the gap between estimates is greater than a specific duration.

## Smoothing algorithm
In the following, $N$ is the total number of estimates. $x_k^k$ and $p_k^k$ are respectively the $k$-th unsmoothed state deviation and unsmoothed covariance. Similarly, $x_{k+1}^l$, $p_{k+1}^l$, and $\phi_{k+1}^l$ are the smoothed state deviation, the covariance  and the associated STM of the previous step ($k+1$-th estimate knowing the previous $l$ estimates). We also note $s_k$ as the $k$-th smoothed estimate.

> Loop  
$\quad$ Initialize $l=N-1$ and $k=l-1$  
$\qquad$$s_k = p_k^k {\phi_{k+1}^k}^T {p_{k+1}^k}^{-1}$  
$\quad$ Compute the smoothed state deviation  
$\qquad$ $x_k^l = x_k^k + s_k (x_{k+1}^l - \phi_{k+1}^k\cdot x_k^k)$  
$\quad$ Compute the smoothed covariance  
$\qquad$ $p_k^l = p_k^k + s_k  (p_{k+1}^l - p_{k+1}^k) * s_k^T$  
$\quad$ Store the smoothed estimate as modified clone of that estimate  
$\quad$ Repeat until the end of the smoothing arc

--8<-- "includes/Abbreviations.md"