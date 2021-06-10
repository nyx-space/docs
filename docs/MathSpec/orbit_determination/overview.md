# Navigation
Spacecraft navigation / orbit determination is a first-class feature of Nyx. The provided implementations should allow you to setup most navigation scenarios. Advanced usage of Nyx enables developers to add new kinds of navigation systems, such as the Cislunar Autonomous Positioning System (CAPS) presented in the Showcase section of this website.

+ [Kalman filter](/MathSpec/navigation/kalman)
+ [State noise compensation](/MathSpec/navigation/snc)
+ [Smoothing](/MathSpec/navigation/smoothing)
+ [Iteration](/MathSpec/navigation/iteration)
+ [Measurement generation](/MathSpec/navigation/measurements)

??? check "Validation"
    To run all of the OD test cases, clone the Nyx repo and execute the following command:
    ```
    RUST_LOG=info cargo test od_ --release
    ```