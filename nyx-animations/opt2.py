from manim import *

class DynamicFrameParsing(Scene):
    def construct(self):
        # Step 1: The ID Contrast
        title = Text("ANISE Frame Resolution Decoder").to_edge(UP)
        self.play(Write(title))

        legacy_id = Text("Legacy Frame ID: 399 (Earth IAU)", color=GRAY)
        dynamic_id_str = "0xA0 | 01 | 01 | 018F"
        dynamic_id = Text(f"Dynamic ID: {dynamic_id_str}", color=YELLOW)

        id_group = VGroup(legacy_id, dynamic_id).arrange(DOWN, center=False, aligned_edge=LEFT).move_to(UP * 2)

        self.play(FadeIn(legacy_id))
        self.wait(1)
        self.play(Write(dynamic_id))

        # Break down the dynamic ID
        marker_brace = Brace(dynamic_id[12:16], DOWN)
        marker_text = marker_brace.get_text("Marker")

        flags_brace = Brace(dynamic_id[19:26], DOWN)
        flags_text = flags_brace.get_text("Flags (Inertial/Frozen)")

        body_brace = Brace(dynamic_id[29:], DOWN)
        body_text = body_brace.get_text("Target (399)")

        self.play(
            GrowFromCenter(marker_brace), FadeIn(marker_text),
            GrowFromCenter(flags_brace), FadeIn(flags_text),
            GrowFromCenter(body_brace), FadeIn(body_text)
        )
        self.wait(1)

        # Step 2: The API Call
        self.play(FadeOut(legacy_id), FadeOut(marker_brace), FadeOut(marker_text), FadeOut(flags_brace), FadeOut(flags_text), FadeOut(body_brace), FadeOut(body_text))
        self.play(dynamic_id.animate.scale(0.7).to_corner(UL))

        api_call = Code(
            code_string="almanac.rotate(target=399, observer=ICRF, epoch=tcl_epoch)",
            language="rust",
        ).next_to(dynamic_id, DOWN, aligned_edge=LEFT)

        self.play(FadeIn(api_call))
        self.wait(1)

        # Step 3: Time Scale Conversion (TCL -> TT) for SOFA
        time_conversion = MathTex(
            r"t_{TT} = t_{TCL} + \Delta T_{Relativistic}",
            color=BLUE
        ).next_to(api_call, DOWN, buff=1)

        time_label = Text("SOFA Requirement: Transform to TT", color=BLUE).next_to(time_conversion, UP)

        self.play(FadeIn(time_label), Write(time_conversion))
        self.wait(1)

        # Step 4: The DCM Evaluation
        dcm_math = MathTex(
            r"R(t_{TT})", r"=", r"\text{SOFA}(t_{TT})",

        ).next_to(time_conversion, DOWN, buff=0.5)

        dcm_deriv = MathTex(
            r"\dot{R}(t_{TT})", r"=", r"\frac{d}{dt}\text{SOFA}(t_{TT})",

        ).next_to(dcm_math, DOWN)

        self.play(Write(dcm_math), Write(dcm_deriv))
        self.wait(1)

        # Step 5: Applying the parsed flags

        # Action 1: Force Inertial
        inertial_flag_text = Text("Flag: force_inertial == true", color=RED).to_edge(RIGHT).shift(UP*1)
        self.play(Write(inertial_flag_text))

        # Cross out the derivative and set to 0
        cross = Cross(dcm_deriv[2])
        zero_val = MathTex("0", color=RED).move_to(dcm_deriv[2])

        self.play(Create(cross))
        self.play(Transform(dcm_deriv[2], zero_val), FadeOut(cross))
        self.wait(1)

        # Action 2: Frozen Epoch
        frozen_flag_text = Text("Flag: frozen_epoch == t_0", color=TEAL).next_to(inertial_flag_text, DOWN)
        self.play(Write(frozen_flag_text))

        # Transform t_TT to t_0 in the rotation matrix
        frozen_math = MathTex(
            r"R(t_0)", r"=", r"\text{SOFA}(t_0)",
            color=TEAL
        ).move_to(dcm_math)

        self.play(Transform(dcm_math, frozen_math))
        self.wait(2)
