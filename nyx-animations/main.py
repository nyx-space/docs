

from manim import *
import numpy as np

class FrozenFrameKinematics(ThreeDScene):
    def construct(self):
        # 1. Setup the Camera and ICRF (The Absolute Anchor)
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        icrf_axes = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3])
        icrf_labels = icrf_axes.get_axis_labels(
            Text("X_icrf").scale(0.5),
            Text("Y_icrf").scale(0.5),
            Text("Z_icrf").scale(0.5)
        )
        self.add(icrf_axes, icrf_labels)

        # Title Overlay
        title = Text("ANISE v0.10: Dynamic & Frozen Frames", font_size=36)
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)

        # --- THE NEW ADDITION: SOFA/IAU Telemetry HUD ---
        telemetry_text = (
            "Engine: SOFA\n"
            "Precession-Nutation: IAU 2006A / 2000A\n"
            "Base Frame: ICRS"
        )
        telemetry = Text(telemetry_text, font_size=18, color=LIGHT_GRAY, line_spacing=1.5)
        telemetry.to_corner(DL) # Bottom Left
        self.add_fixed_in_frame_mobjects(telemetry)
        # ------------------------------------------------

        # 2. The Dynamic Frame (Earth True of Date)
        tod_axes = ThreeDAxes(
            x_range=[-2.5, 2.5], y_range=[-2.5, 2.5], z_range=[-2.5, 2.5],
            axis_config={"color": YELLOW}
        )

        time_tracker = ValueTracker(0)

        def update_tod(axes):
            t = time_tracker.get_value()
            precession = t * 0.5
            nutation = np.sin(t * 2) * 0.2

            axes.become(ThreeDAxes(
                x_range=[-2.5, 2.5], y_range=[-2.5, 2.5], z_range=[-2.5, 2.5],
                axis_config={"color": YELLOW}
            ))
            axes.rotate(precession, axis=OUT)
            axes.rotate(nutation, axis=RIGHT)

        tod_axes.add_updater(update_tod)
        self.add(tod_axes)

        tod_label = Text("Evaluating: Earth TOD", color=YELLOW, font_size=24)
        tod_label.to_corner(UR) # Top Right
        self.add_fixed_in_frame_mobjects(tod_label)

        # Let the dynamic frame drift
        self.play(time_tracker.animate.set_value(4), run_time=4, rate_func=linear)

        # 3. The Freeze Event (PR #697)
        frozen_axes = tod_axes.copy()
        frozen_axes.clear_updaters()
        frozen_axes.set_color(BLUE)
        frozen_axes.set_opacity(0.6)

        flash = Flash(ORIGIN, color=WHITE, line_length=1, num_lines=12)
        self.play(FadeIn(frozen_axes), flash, run_time=0.5)

        frozen_label = Text("Instantiated: Explicitly Frozen TOD @ Epoch", color=BLUE, font_size=24)
        frozen_label.next_to(tod_label, DOWN, aligned_edge=RIGHT)
        self.add_fixed_in_frame_mobjects(frozen_label)

        # 4. Divergence
        self.play(time_tracker.animate.set_value(10), run_time=6, rate_func=linear)
        self.wait(2)
