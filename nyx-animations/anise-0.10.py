"""
ANISE 0.10 announcement animation
Dynamic frame ID parsing -> DCM construction

Render:
    manim -pqh anise_dynamic_frame_announcement.py Anise010DynamicFrameAnnouncement

Notes:
- This scene avoids LaTeX so it is easier to render on a clean Manim install.
- It is intentionally storyboard-like: the values are illustrative, while the decoding
  matches ANISE's documented packed dynamic-frame orientation ID format.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from manim import *

# Manim's default coordinate frame is 14.222... x 8 units for 16:9 output.
# These safe bounds leave room for titles, captions, and video-platform cropping.
SAFE_WIDTH = 120.6
SAFE_HEIGHT = 60.5


# -----------------------------------------------------------------------------
# Visual constants
# -----------------------------------------------------------------------------
BG = "#0D1117"
PANEL = "#161B22"
PANEL_2 = "#1F2937"
FG = "#E6EDF3"
MUTED = "#8B949E"
CYAN = "#56D4DD"
BLUE = "#58A6FF"
GREEN = "#7EE787"
YELLOW = "#F2CC60"
ORANGE = "#FFA657"
RED = "#FF7B72"
PURPLE = "#D2A8FF"
GRAY = "#30363D"

FONT = "DejaVu Sans"
MONO = "DejaVu Sans Mono"


@dataclass(frozen=True)
class ByteSpec:
    value: str
    name: str
    meaning: str
    color: str


DYNAMIC_ID_BYTES = [
    ByteSpec("0xA0", "prefix", "ANISE dynamic frame", CYAN),
    ByteSpec("0xE1", "family", "Earth TOD", BLUE),
    ByteSpec("0x03", "primary", "IAU 2006 precession", GREEN),
    ByteSpec("0x03", "secondary", "IAU 2006 / 2000A nutation", ORANGE),
]


class Anise010DynamicFrameAnnouncement(Scene):
    """Announcement animation for ANISE 0.10 dynamic frames."""

    def construct(self) -> None:
        self.camera.background_color = BG

        self.title_card()
        self.standard_id()
        self.dynamic_id_decode()
        self.rotate_call()
        self.dcm_pipeline()
        self.time_scale_conversion()
        self.frozen_and_force_inertial()
        self.end_card()

    # ------------------------------------------------------------------
    # Scene sections
    # ------------------------------------------------------------------
    def title_card(self) -> None:
        self.next_section("title")
        title = Text("ANISE 0.10", font=FONT, font_size=68, weight=BOLD, color=FG)
        subtitle = Text(
            "Dynamic frames encoded directly in orientation IDs",
            font=FONT,
            font_size=31,
            color=MUTED,
        )
        group = VGroup(title, subtitle).arrange(DOWN, buff=0.25)

        marker = self.code_chip("0xA0 FF AA BB", color=CYAN, font_size=34)
        marker.next_to(group, DOWN, buff=0.65)

        self.play(FadeIn(title, shift=0.35 * UP), run_time=0.8)
        self.play(FadeIn(subtitle), FadeIn(marker, shift=0.2 * UP), run_time=0.9)
        self.wait(0.8)
        self.play(FadeOut(group), FadeOut(marker), run_time=0.5)

    def standard_id(self) -> None:
        self.next_section("standard orientation id")
        header = self.section_header("1. The ordinary case")
        frame_box = self.id_card(
            title="orientation_id",
            value="399",
            subtitle="Earth IAU orientation model",
            color=GREEN,
        ).scale(1.08)
        lookup = self.pipeline_box("lookup orientation data", GREEN)
        dcm = self.block_dcm(label="DCM from stored model", highlight=GREEN)

        group = VGroup(frame_box, lookup, dcm).arrange(RIGHT, buff=0.65).move_to(ORIGIN)
        self.fit_to_frame(group, max_width=SAFE_WIDTH, max_height=4.7)
        arrows = VGroup(
            self.arrow_between(frame_box, lookup),
            self.arrow_between(lookup, dcm),
        )

        note = Text(
            "No packed-byte interpretation: the ID directly routes to an orientation model.",
            font=FONT,
            font_size=24,
            color=MUTED,
        ).next_to(group, DOWN, buff=0.45)

        self.play(FadeIn(header), FadeIn(frame_box, shift=0.25 * UP), run_time=0.8)
        self.play(GrowArrow(arrows[0]), FadeIn(lookup), run_time=0.55)
        self.play(GrowArrow(arrows[1]), FadeIn(dcm), run_time=0.7)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(1.0)
        self.play(FadeOut(VGroup(header, group, arrows, note)), run_time=0.55)

    def dynamic_id_decode(self) -> None:
        self.next_section("dynamic id decoding")
        header = self.section_header("2. Dynamic frames start with 0xA0")

        signed = Text(
            "orientation_id = 0xA0E10303  // signed i32: -1595866365",
            font=MONO,
            font_size=28,
            color=FG,
        ).to_edge(UP, buff=1.35)
        self.fit_to_frame(signed, max_width=SAFE_WIDTH)

        bytes_group = VGroup(*[self.byte_cell(spec) for spec in DYNAMIC_ID_BYTES])
        bytes_group.arrange(RIGHT, buff=0.17).scale(1.02).move_to(0.25 * UP)

        equation = Text(
            "0xA0 FF AA BB  →  DynamicFrame::EarthTrueOfDate { precession, nutation }",
            font=MONO,
            font_size=23,
            color=MUTED,
        ).next_to(bytes_group, DOWN, buff=0.45)

        self.play(FadeIn(header), FadeIn(signed, shift=0.2 * UP), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(c, shift=0.3 * UP) for c in bytes_group], lag_ratio=0.12), run_time=1.2)

        prefix_box = SurroundingRectangle(bytes_group[0], color=CYAN, buff=0.08, corner_radius=0.08)
        self.play(Create(prefix_box), run_time=0.35)
        self.play(Indicate(bytes_group[0], color=CYAN, scale_factor=1.05), run_time=0.6)
        self.play(Transform(prefix_box, SurroundingRectangle(bytes_group[1:], color=BLUE, buff=0.08, corner_radius=0.08)), run_time=0.55)
        self.play(FadeIn(equation), run_time=0.55)
        self.wait(0.9)
        self.play(FadeOut(VGroup(header, signed, bytes_group, equation, prefix_box)), run_time=0.55)

    def rotate_call(self) -> None:
        self.next_section("rotate call")
        header = self.section_header("3. The public call stays small")

        code = self.code_panel(
            [
                "let dcm = almanac.rotate(",
                "    from_frame,",
                "    to_frame,",
                "    epoch,",
                ")?;",
            ],
            highlight_lines={0: BLUE, 3: PURPLE},
        ).scale(1.0).move_to(ORIGIN + 0.25 * UP)

        left = self.small_frame_card("from_frame", "EME2000", BLUE)
        right = self.small_frame_card("to_frame", "0xA0E10303", CYAN)
        epoch = self.small_frame_card("epoch", "2032-04-12T08:15:00 TCL", PURPLE)
        params = VGroup(left, right, epoch).arrange(RIGHT, buff=0.35).next_to(code, DOWN, buff=0.55)
        self.fit_to_frame(VGroup(code, params), max_width=SAFE_WIDTH, max_height=5.0)

        pulse = SurroundingRectangle(params, color=PURPLE, buff=0.16, corner_radius=0.12)

        self.play(FadeIn(header), FadeIn(code, shift=0.25 * UP), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(p, shift=0.2 * UP) for p in params], lag_ratio=0.15), run_time=0.8)
        self.play(Create(pulse), run_time=0.35)
        self.play(pulse.animate.set_stroke(opacity=0.0), run_time=0.55)
        self.wait(0.7)
        self.play(FadeOut(VGroup(header, code, params, pulse)), run_time=0.55)

    def dcm_pipeline(self) -> None:
        self.next_section("dcm pipeline")
        header = self.section_header("4. Decode, evaluate, compose")

        stages = VGroup(
            self.pipeline_box("parse orientation_id", CYAN),
            self.pipeline_box("select dynamic model", BLUE),
            self.pipeline_box("evaluate at epoch", PURPLE),
            self.pipeline_box("compose DCM", GREEN),
        ).arrange(RIGHT, buff=0.4).move_to(0.4 * UP)
        arrows = VGroup(*[self.arrow_between(stages[i], stages[i + 1]) for i in range(len(stages) - 1)])

        detail_lines = [
            ("0xA0", "dynamic marker", CYAN),
            ("0xE1", "Earth True Equator, True Equinox of Date", BLUE),
            ("0x03", "IAU 2006 precession-bias", GREEN),
            ("0x03", "IAU 2006 / 2000A-compatible nutation", ORANGE),
        ]
        details = VGroup(*[self.key_value(k, v, c) for k, v, c in detail_lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        details.next_to(stages, DOWN, buff=0.55).align_to(stages, LEFT)

        dcm = self.block_dcm(label="6×6 DCM", highlight=GREEN).next_to(details, RIGHT, buff=1.0)
        self.fit_to_frame(VGroup(stages, arrows, details, dcm), max_width=SAFE_WIDTH, max_height=5.4)

        self.play(FadeIn(header), LaggedStart(*[FadeIn(s, shift=0.2 * UP) for s in stages], lag_ratio=0.1), run_time=1.0)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), run_time=0.6)
        self.play(FadeIn(details, shift=0.25 * UP), run_time=0.75)
        self.play(FadeIn(dcm, scale=0.92), run_time=0.65)
        self.wait(1.0)
        self.play(FadeOut(VGroup(header, stages, arrows, details, dcm)), run_time=0.55)

    def time_scale_conversion(self) -> None:
        self.next_section("time scale conversion")
        header = self.section_header("5. SOFA models need the right time argument")

        card_epoch = self.id_card(
            title="incoming epoch",
            value="2032-04-12T08:15:00 TCL",
            subtitle="lunar coordinate time scale in user code",
            color=PURPLE,
        )
        convert = self.pipeline_box("convert to TT", YELLOW)
        sofa = self.pipeline_box("SOFA precession / nutation", BLUE, width=3.05)
        matrix = self.block_dcm(label="R(TT),  Ṙ(TT)", highlight=BLUE)

        group = VGroup(card_epoch, convert, sofa, matrix).arrange(RIGHT, buff=0.45).move_to(0.15 * UP)
        arrows = VGroup(*[self.arrow_between(group[i], group[i + 1]) for i in range(3)])

        code = self.code_panel(
            [
                "let eval_epoch = frame.frozen_epoch.unwrap_or(epoch);",
                "let tt = eval_epoch.to_time_scale(TimeScale::TT);",
                "let r = sofa_precession_nutation(tt, model);",
            ],
            font_size=22,
            highlight_lines={1: YELLOW, 2: BLUE},
        ).next_to(group, DOWN, buff=0.5)
        self.fit_to_frame(VGroup(group, arrows, code), max_width=SAFE_WIDTH, max_height=5.4)

        self.play(FadeIn(header), FadeIn(card_epoch, shift=0.25 * UP), run_time=0.7)
        self.play(GrowArrow(arrows[0]), FadeIn(convert), run_time=0.45)
        self.play(GrowArrow(arrows[1]), FadeIn(sofa), run_time=0.45)
        self.play(GrowArrow(arrows[2]), FadeIn(matrix), run_time=0.55)
        self.play(FadeIn(code, shift=0.25 * UP), run_time=0.75)
        self.wait(1.0)
        self.play(FadeOut(VGroup(header, group, arrows, code)), run_time=0.55)

    def frozen_and_force_inertial(self) -> None:
        self.next_section("frozen and forced inertial")
        header = self.section_header("6. Frame fields decide whether the DCM evolves")

        live = self.block_dcm(label="dynamic frame", highlight=GREEN).scale(1.08)
        frozen = self.block_dcm(label="frozen_epoch set", highlight=YELLOW).scale(1.08)
        forced = self.block_dcm(label="force_inertial = true", highlight=RED).scale(1.08)
        cards = VGroup(live, frozen, forced).arrange(RIGHT, buff=0.65).move_to(0.1 * UP)

        frozen_note = Text(
            "evaluate dynamic model at frozen_epoch instead of integration epoch",
            font=FONT,
            font_size=22,
            color=YELLOW,
        ).next_to(frozen, DOWN, buff=0.28)
        forced_note = Text(
            "zero the time derivative block: Ṙ = 0",
            font=FONT,
            font_size=22,
            color=RED,
        ).next_to(forced, DOWN, buff=0.28)
        live_note = Text(
            "R and Ṙ evolve with epoch",
            font=FONT,
            font_size=22,
            color=GREEN,
        ).next_to(live, DOWN, buff=0.28)
        self.fit_to_frame(VGroup(cards, frozen_note, forced_note, live_note), max_width=SAFE_WIDTH, max_height=5.4)

        self.play(FadeIn(header), FadeIn(live, shift=0.25 * UP), FadeIn(live_note), run_time=0.75)
        self.play(FadeIn(frozen, shift=0.25 * UP), FadeIn(frozen_note), run_time=0.65)
        self.play(Indicate(frozen, color=YELLOW, scale_factor=1.04), run_time=0.6)
        self.play(FadeIn(forced, shift=0.25 * UP), FadeIn(forced_note), run_time=0.65)
        zero_box = SurroundingRectangle(self.dcm_rdot_cell(forced), color=RED, buff=0.05, corner_radius=0.05)
        self.play(Create(zero_box), run_time=0.35)
        self.play(Indicate(self.dcm_rdot_cell(forced), color=RED, scale_factor=1.15), run_time=0.55)
        self.wait(1.0)
        self.play(FadeOut(VGroup(header, cards, frozen_note, forced_note, live_note, zero_box)), run_time=0.55)

    def end_card(self) -> None:
        self.next_section("end")
        title = Text("ANISE 0.10", font=FONT, font_size=62, weight=BOLD, color=FG)
        subtitle = Text(
            "Static IDs, dynamic frames, one rotation API.",
            font=FONT,
            font_size=31,
            color=MUTED,
        )
        bits = self.code_chip("0xA0 FF AA BB  →  DCM(epoch)", color=CYAN, font_size=34)
        stack = VGroup(title, subtitle, bits).arrange(DOWN, buff=0.32)
        self.play(FadeIn(stack, shift=0.25 * UP), run_time=0.85)
        self.wait(1.3)
        self.play(FadeOut(stack), run_time=0.6)

    # ------------------------------------------------------------------
    # Reusable visual primitives
    # ------------------------------------------------------------------
    def section_header(self, text: str) -> VGroup:
        label = Text(text, font=FONT, font_size=34, weight=BOLD, color=FG)
        line = Line(LEFT, RIGHT, color=GRAY, stroke_width=2).set_width(11.6)
        group = VGroup(label, line).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        group.to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.55)
        return group

    def id_card(self, title: str, value: str, subtitle: str, color: str) -> VGroup:
        rect = RoundedRectangle(
            width=3.25,
            height=1.65,
            corner_radius=0.13,
            stroke_color=color,
            stroke_width=2,
            fill_color=PANEL,
            fill_opacity=0.95,
        )
        t = Text(title, font=FONT, font_size=20, color=MUTED)
        v = Text(value, font=MONO, font_size=34, color=color, weight=BOLD)
        s = Text(subtitle, font=FONT, font_size=18, color=FG)
        stack = VGroup(t, v, s).arrange(DOWN, buff=0.12).move_to(rect.get_center())
        return VGroup(rect, stack)

    def small_frame_card(self, title: str, value: str, color: str) -> VGroup:
        rect = RoundedRectangle(
            width=3.25,
            height=1.0,
            corner_radius=0.11,
            stroke_color=color,
            stroke_width=1.6,
            fill_color=PANEL,
            fill_opacity=0.92,
        )
        t = Text(title, font=FONT, font_size=18, color=MUTED)
        v = Text(value, font=MONO, font_size=21, color=FG)
        stack = VGroup(t, v).arrange(DOWN, buff=0.08).move_to(rect.get_center())
        return VGroup(rect, stack)

    def byte_cell(self, spec: ByteSpec) -> VGroup:
        rect = RoundedRectangle(
            width=2.35,
            height=1.85,
            corner_radius=0.12,
            stroke_color=spec.color,
            stroke_width=2,
            fill_color=PANEL,
            fill_opacity=0.94,
        )
        value = Text(spec.value, font=MONO, font_size=32, color=spec.color, weight=BOLD)
        name = Text(spec.name, font=FONT, font_size=18, color=MUTED)
        meaning = Text(spec.meaning, font=FONT, font_size=16, color=FG, line_spacing=0.9)
        meaning.set_width(2.05)
        stack = VGroup(value, name, meaning).arrange(DOWN, buff=0.12).move_to(rect.get_center())
        return VGroup(rect, stack)

    def pipeline_box(self, text: str, color: str, width: float = 2.55) -> VGroup:
        rect = RoundedRectangle(
            width=width,
            height=0.95,
            corner_radius=0.12,
            stroke_color=color,
            stroke_width=1.8,
            fill_color=PANEL,
            fill_opacity=0.94,
        )
        label = Text(text, font=FONT, font_size=21, color=FG)
        label.set_width(width - 0.35) if label.width > width - 0.35 else None
        label.move_to(rect)
        return VGroup(rect, label)

    def code_panel(
        self,
        lines: list[str],
        font_size: int = 25,
        highlight_lines: dict[int, str] | None = None,
    ) -> VGroup:
        highlight_lines = highlight_lines or {}
        text_lines = VGroup()
        for i, line in enumerate(lines):
            color = highlight_lines.get(i, FG)
            text_lines.add(Text(line, font=MONO, font_size=font_size, color=color))
        text_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        bg = RoundedRectangle(
            width=max(text_lines.width + 0.62, 6.0),
            height=text_lines.height + 0.45,
            corner_radius=0.12,
            stroke_color=GRAY,
            stroke_width=1.2,
            fill_color=PANEL,
            fill_opacity=0.96,
        )
        text_lines.move_to(bg.get_center()).align_to(bg, LEFT).shift(0.31 * RIGHT)
        return VGroup(bg, text_lines)

    def code_chip(self, text: str, color: str, font_size: int = 28) -> VGroup:
        label = Text(text, font=MONO, font_size=font_size, color=color)
        rect = RoundedRectangle(
            width=label.width + 0.62,
            height=label.height + 0.32,
            corner_radius=0.14,
            stroke_color=color,
            stroke_width=1.6,
            fill_color=PANEL,
            fill_opacity=0.95,
        )
        label.move_to(rect)
        return VGroup(rect, label)

    def key_value(self, key: str, value: str, color: str) -> VGroup:
        k = self.code_chip(key, color=color, font_size=20)
        v = Text(value, font=FONT, font_size=22, color=FG)
        arrow = Text("→", font=FONT, font_size=22, color=MUTED)
        row = VGroup(k, arrow, v).arrange(RIGHT, buff=0.18)
        return row

    def fit_to_frame(
        self,
        mob: Mobject,
        max_width: float = SAFE_WIDTH,
        max_height: float = SAFE_HEIGHT,
    ) -> Mobject:
        """Scale a layout down only if it would otherwise exceed the camera frame."""
        scale = min(max_width / mob.width if mob.width else 1.0, max_height / mob.height if mob.height else 1.0, 1.0)
        if scale < 1.0:
            mob.scale(scale)
        return mob

    def dcm_rdot_cell(self, dcm: VGroup) -> Mobject:
        """Return the lower-left R-dot cell in block_dcm()."""
        # block_dcm -> [title, full_grid]
        # full_grid -> [left bracket, grid, right bracket]
        # grid -> [top row, bottom row]
        # bottom row -> [Rdot cell, R cell]
        return dcm[1][1][1][0]

    def arrow_between(self, left: Mobject, right: Mobject, color: str = MUTED) -> Arrow:
        return Arrow(
            start=left.get_right(),
            end=right.get_left(),
            buff=0.12,
            stroke_width=3,
            color=color,
            max_tip_length_to_length_ratio=0.16,
        )

    def block_dcm(self, label: str, highlight: str) -> VGroup:
        """Compact visual stand-in for ANISE's 6x6 DCM.

        The group layout is: [title, grid]. The grid children are cells ordered
        row-major. The bottom-left cell is the Rdot block, useful for highlighting
        force_inertial behavior.
        """
        title = Text(label, font=FONT, font_size=22, color=FG)
        cells = VGroup()
        data = [
            ("R", highlight, 0.24),
            ("0", MUTED, 0.08),
            ("Ṙ", ORANGE, 0.22),
            ("R", highlight, 0.24),
        ]
        for text, color, opacity in data:
            rect = Square(side_length=0.72, stroke_color=color, stroke_width=1.8, fill_color=color, fill_opacity=opacity)
            label_mob = Text(text, font=FONT, font_size=23, color=FG)
            label_mob.move_to(rect)
            cells.add(VGroup(rect, label_mob))
        grid = VGroup(
            VGroup(cells[0], cells[1]).arrange(RIGHT, buff=0.06),
            VGroup(cells[2], cells[3]).arrange(RIGHT, buff=0.06),
        ).arrange(DOWN, buff=0.06)
        bracket_l = Line(UP, DOWN, color=MUTED, stroke_width=2).set_height(grid.height + 0.15).next_to(grid, LEFT, buff=0.08)
        bracket_r = Line(UP, DOWN, color=MUTED, stroke_width=2).set_height(grid.height + 0.15).next_to(grid, RIGHT, buff=0.08)
        full_grid = VGroup(bracket_l, grid, bracket_r)
        group = VGroup(title, full_grid).arrange(DOWN, buff=0.18)
        return group


# Optional: a shorter social-clip version that cuts the standard-ID intro.
class Anise010DynamicFrameShort(Anise010DynamicFrameAnnouncement):
    def construct(self) -> None:
        self.camera.background_color = BG
        self.title_card()
        self.dynamic_id_decode()
        self.rotate_call()
        self.dcm_pipeline()
        self.frozen_and_force_inertial()
        self.end_card()
