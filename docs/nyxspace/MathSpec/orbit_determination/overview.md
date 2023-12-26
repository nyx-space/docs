# Navigation
Spacecraft navigation / orbit determination is a first-class feature of Nyx. The provided implementations should allow you to setup most navigation scenarios. Advanced usage of Nyx enables developers to add new kinds of navigation systems, such as the Cislunar Autonomous Positioning System (CAPS) presented in the Showcase section of this website.

+ [Kalman filter](./kalman.md)
+ [State noise compensation](./snc.md)
+ [Smoothing](./smoothing.md)
+ [Iteration](./iteration.md)
+ [Measurement generation](./measurements.md)

??? check "Validation"
    To run all of the OD test cases, clone the Nyx repo and execute the following command:
    ```
    RUST_LOG=info cargo test od_ --release
    ```
!!! note
    Nyx uses a state replacement model for orbit determination: the STM is recomputed at each step and copied into the filter for appropriate estimate of the arc between two subsequent measurements.

--8<-- "includes/Abbreviations.md"