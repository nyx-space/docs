# Filter iteration
Nyx supports iterations by smoothing the estimates first and then iterating on the measurements. Version 1.1 will support iterating on the measurements [until convergence](https://gitlab.com/nyx-space/nyx/-/issues/168).

The algorithm is straight-forward:

1. Smooth all estimates, or until the end of the smoothing arc (cf. [smoothing](/MathSpec/navigation/smoothing/)).
2. Process all of the measurements sequentially forward in time.