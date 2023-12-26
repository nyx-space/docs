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
In the following, $N$ is the total number of estimates. $x_k^k$ and $P_k^k$ are respectively the $k$-th unsmoothed state deviation and unsmoothed covariance. Similarly, $x_{k+1}^l$, $P_{k+1}^l$, and $\phi_{k+1}^l$ are the smoothed state deviation, the covariance  and the associated STM of the previous step: $k+1$-th estimate _knowing_ the previous $l$ estimates (where _knowing_ refers to Bayesian knowledge). We also note $S_k$ as the $k$-th smoothed covariance.

> Loop  
$\quad$ Consider x_N^N (the very last estimate) to be smoothed  
$\quad$ Initialize $l=N-1$  
$\quad$ Set $k$ at each iteration to the number of items in the smoothed estimates  
$\qquad$$S_k = P_k^k {\phi_{k+1}^k}^T {P_{k+1}^k}^{-1}$  
$\quad$ Compute the smoothed state deviation  
$\qquad$ $x_k^l = x_k^k + S_k (x_{k+1}^l - \phi_{k+1}^k\cdot x_k^k)$  
$\quad$ Compute the smoothed covariance  
$\qquad$ $P_k^l = P_k^k + S_k  (P_{k+1}^l - p_{k+1}^k) \cdot S_k^T$  
$\quad$ Store the smoothed estimate as modified clone of that estimate  
$\quad$ Repeat until the end of the smoothing arc

!!! note
    A smoothing process will _increase_ the covariance of the estimates.

!!! tip
    Smoothing is mostly used for calibration of the initial estimate. Nyx only includes sequential filters (no batch filters), which tend to be more precise after the orbit is decently determined. For example, an EKF will perform very well in non-linear regimes. However, an EKF will perform terribly poorly if enabled prior to convergence of the previous measurement arc. Hence, a good initial guess in setting up a single-filter performance analysis is to smooth and iterate a CKF on the beginning of the arc (e.g. 30 minutes or an hour), and if the filter has [converged](./iteration.md#iteration-until-convergence), then switch the OD process to an EKF from that point on.

    Let's look at the example of the `xhat_dev_test_ekf_two_body` test. The initial RSS error is 8.66 km. When in CKF mode with a 30 minute arc with a default iteration configuration, the initial RSS error drops to 7.82 km in position and increases the initial RSS velocity error from zero to 0.0066 km/s. In other words, to better fit the data, the filter changes the initial orbit estimate at the beginning of the arc. This error level is kept through the 30 minute arc: the final RSS error at the end of this arc is 7.159 km. For that same 30 minute arc, if the filter is set to an EKF mode, the error is 22 km at the end of the arc! _However_, if the data arc is one day long, the CKF will perform poorly, and iterating on the solution will not provide useful results. An EKF on that same duration however will ingest all of that data, update the reference trajectory through and end up with a final error on the order of a meter.

    I will eventually write up a primer on orbit determination in operations where I'll talk about multiple filter analysis.

--8<-- "includes/Abbreviations.md"