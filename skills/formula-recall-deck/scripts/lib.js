// Reusable pptxgenjs component library for exam-review decks.
// Works for any subject: point FORMULA_MANIFEST/DIAGRAM_MANIFEST at that job's
// formula_manifest.json / diagram_manifest.json (produced by gen_formulas.py / gen_diagrams.py)
// and call the slide-builder functions below from your deckN.js files.
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

// Manifest of LaTeX-rendered formula PNGs produced by gen_formulas.py: id -> {file, ar}
const FORMULA_MANIFEST = JSON.parse(fs.readFileSync(path.join(__dirname, "formula_manifest.json"), "utf-8"));
function mathImg(id) {
  const m = FORMULA_MANIFEST[id];
  if (!m) throw new Error(`No rendered formula found for id "${id}" — run gen_formulas.py first`);
  return m;
}

// Manifest of matplotlib-rendered relationship-diagram PNGs from gen_diagrams.py: id -> {file, ar}
const DIAGRAM_MANIFEST = JSON.parse(fs.readFileSync(path.join(__dirname, "diagram_manifest.json"), "utf-8"));
function diagImg(id) {
  const m = DIAGRAM_MANIFEST[id];
  if (!m) throw new Error(`No rendered diagram found for id "${id}" — run gen_diagrams.py first`);
  return m;
}

// ---- Palette: "Structural Steel" — neutral, professional, reused across all subjects by
// default (see SKILL.md). Only change these if the user explicitly asks for a different theme. ----
const C = {
  navy: "1B2A41",     // primary — deep navy
  steel: "4C6B8A",    // secondary — steel blue-grey
  ice: "DCE6F0",      // light tint of steel for backgrounds/cards
  accent: "E8734A",   // sharp accent — warm orange
  white: "FFFFFF",
  ink: "1B2A41",
  sub: "5C7A99",
  cardBg: "F4F6F9",
  trapBg: "2A3F5A",
  // extra tints used by flowMapSlide's colored branch boxes — a small fixed palette the
  // caller picks from via each node's `tint` field ('blue'|'green'|'pink'|'gray')
  mintBg: "DFF0E4", mintFg: "1F7A4D",
  pinkBg: "FBE1DE", pinkFg: "C0392B",
  success: "1E8449",
};

// Decks are typically mostly CJK (Chinese/Japanese/Korean) text. Cambria/Calibri are Latin-only
// fonts whose LibreOffice metric-compatible substitutes (Caladea/Carlito) have broken bold-CJK
// glyph advances that visually overlap adjacent characters into garbage glyphs on render or PDF
// export. Use fonts with full, correct CJK coverage instead — safe both for headless QA renders
// and for the user's own Windows/Office CJK font-linking on open. See references/pitfalls.md.
const FONT_HEAD = "Noto Serif CJK TC";
const FONT_BODY = "Noto Sans CJK TC";

function newPres(author) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.3 x 7.5
  pres.author = author || "考前總複習";
  return pres;
}

function bgSlide(pres, color) {
  const s = pres.addSlide();
  s.background = { color };
  return s;
}

// Title slide: dark navy background, big title, subtitle, kicker.
// footer defaults to a generic "exam review" line — pass your own to match the subject/exam name.
function titleSlide(pres, { kicker, title, subtitle, tag, footer }) {
  const s = bgSlide(pres, C.navy);
  s.addShape("rect", { x: 0, y: 0, w: 13.33, h: 7.5, fill: { color: C.navy } });
  // subtle accent circle motif top-right
  s.addShape("ellipse", { x: 11.3, y: -1.3, w: 3.2, h: 3.2, fill: { color: C.steel, transparency: 60 }, line: { type: "none" } });
  s.addShape("ellipse", { x: 12.1, y: -0.5, w: 1.6, h: 1.6, fill: { color: C.accent, transparency: 20 }, line: { type: "none" } });

  s.addText(kicker, {
    x: 0.7, y: 1.1, w: 10, h: 0.5, fontFace: FONT_BODY, fontSize: 15, color: C.ice,
    charSpacing: 2, bold: true, margin: 0,
  });
  s.addText(title, {
    x: 0.7, y: 1.6, w: 11.3, h: 2.4, fontFace: FONT_HEAD, fontSize: 42, color: C.white,
    bold: true, margin: 0, valign: "top",
  });
  s.addText(subtitle, {
    x: 0.7, y: 4.05, w: 10.8, h: 0.8, fontFace: FONT_BODY, fontSize: 17, color: C.ice,
    margin: 0,
  });
  if (tag) {
    s.addShape("roundRect", { x: 0.7, y: 5.05, w: tag.length * 0.16 + 0.6, h: 0.5, rectRadius: 0.08, fill: { color: C.accent }, line: { type: "none" } });
    s.addText(tag, { x: 0.7, y: 5.05, w: tag.length * 0.16 + 0.6, h: 0.5, fontFace: FONT_BODY, fontSize: 13, bold: true, color: C.white, align: "center", valign: "middle", margin: 0 });
  }
  s.addText(footer || "考前總複習｜原理與公式", {
    x: 0.7, y: 6.9, w: 10, h: 0.4, fontFace: FONT_BODY, fontSize: 11, color: C.steel, margin: 0,
  });
  return s;
}

// Section header band slide (light bg) used to introduce a topic map / big idea
function sectionHeader(s, { eyebrow, title }) {
  s.addText(eyebrow, { x: 0.6, y: 0.4, w: 11, h: 0.4, fontFace: FONT_BODY, fontSize: 13, bold: true, color: C.accent, charSpacing: 1.5, margin: 0 });
  s.addText(title, { x: 0.6, y: 0.75, w: 12, h: 0.75, fontFace: FONT_HEAD, fontSize: 28, bold: true, color: C.navy, margin: 0 });
}

// Topic map slide: N cards in a row/grid with icon-circle, title, desc
function topicMapSlide(pres, { eyebrow, title, topics }) {
  const s = bgSlide(pres, C.white);
  sectionHeader(s, { eyebrow, title });
  const n = topics.length;
  const cols = n <= 2 ? n : (n === 3 ? 3 : (n === 4 ? 2 : 3));
  const rows = Math.ceil(n / cols);
  const marginX = 0.6, marginTop = 1.85, gap = 0.35;
  const cw = (13.33 - marginX * 2 - gap * (cols - 1)) / cols;
  const chAvail = 7.5 - marginTop - 0.5;
  const ch = (chAvail - gap * (rows - 1)) / rows;
  topics.forEach((t, i) => {
    const col = i % cols, row = Math.floor(i / cols);
    const x = marginX + col * (cw + gap);
    const y = marginTop + row * (ch + gap);
    s.addShape("roundRect", { x, y, w: cw, h: ch, rectRadius: 0.09, fill: { color: C.cardBg }, line: { type: "none" }, shadow: { type: "outer", color: "1B2A41", opacity: 0.18, blur: 6, offset: 2, angle: 90 } });
    s.addShape("ellipse", { x: x + 0.28, y: y + 0.28, w: 0.5, h: 0.5, fill: { color: C.navy }, line: { type: "none" } });
    s.addText(String(i + 1), { x: x + 0.28, y: y + 0.28, w: 0.5, h: 0.5, align: "center", valign: "middle", fontFace: FONT_HEAD, bold: true, fontSize: 18, color: C.white, margin: 0 });
    s.addText(t.title, { x: x + 0.3, y: y + 0.95, w: cw - 0.6, h: 0.5, fontFace: FONT_HEAD, bold: true, fontSize: 16, color: C.navy, margin: 0 });
    s.addText(t.desc, { x: x + 0.3, y: y + 1.4, w: cw - 0.6, h: ch - 1.6, fontFace: FONT_BODY, fontSize: 12.5, color: C.sub, margin: 0, valign: "top", lineSpacingMultiple: 1.15 });
  });
  return s;
}

// Formula card slide: title + description, then one or more formula blocks with note.
// formulas: [{ label?, math: "<id in formula_manifest.json>" }]  (or { label, expr } for a plain
// text fallback if you genuinely can't render an image, though math/LaTeX is strongly preferred)
function formulaSlide(pres, { eyebrow, title, note, formulas }) {
  const s = bgSlide(pres, C.white);
  sectionHeader(s, { eyebrow, title });
  const top = 1.85;
  const n = formulas.length;
  const gap = 0.28;
  const availH = 7.5 - top - (note ? 1.05 : 0.5);
  const fh = (availH - gap * (n - 1)) / n;
  formulas.forEach((f, i) => {
    const y = top + i * (fh + gap);
    s.addShape("roundRect", { x: 0.6, y, w: 12.1, h: fh, rectRadius: 0.08, fill: { color: C.ice }, line: { type: "none" } });
    s.addShape("rect", { x: 0.6, y, w: 0.09, h: fh, fill: { color: C.accent }, line: { type: "none" } });
    if (f.label) {
      s.addText(f.label, { x: 0.95, y: y + 0.08, w: 3.0, h: fh - 0.16, fontFace: FONT_BODY, bold: true, fontSize: 13, color: C.steel, valign: "top", margin: 0 });
    }
    const xStart = f.label ? 3.9 : 0.95;
    const availW = f.label ? 8.5 : 11.4;
    const availHImg = fh - 0.34;
    if (f.math) {
      const m = mathImg(f.math);
      let h = availHImg, w = h * m.ar;
      if (w > availW) { w = availW; h = w / m.ar; }
      const ix = xStart + (availW - w) / 2;
      const iy = y + (fh - h) / 2;
      s.addImage({ path: m.file, x: ix, y: iy, w, h });
    } else {
      s.addText(f.expr, {
        x: xStart, y, w: availW, h: fh, align: "left", valign: "middle",
        fontFace: "Cambria Math", fontSize: f.size || 20, bold: true, color: C.navy, margin: 0,
      });
    }
  });
  if (note) {
    s.addText(note, { x: 0.6, y: 7.5 - 0.95, w: 12.1, h: 0.85, fontFace: FONT_BODY, italic: true, fontSize: 12, color: C.sub, margin: 0, valign: "top" });
  }
  return s;
}

// Flow diagram slide: vertical/branching steps as connected boxes (simple linear flow).
// Prefer flowchartSlide below for anything with a real decision branch — this is only for
// a purely sequential list of steps (e.g. an answer-writing SOP for an essay question).
function flowSlide(pres, { eyebrow, title, steps, note }) {
  const s = bgSlide(pres, C.white);
  sectionHeader(s, { eyebrow, title });
  const top = 1.8;
  const n = steps.length;
  const gap = 0.18;
  const bh = (7.5 - top - 0.5 - gap * (n - 1)) / n;
  const bx = 0.9, bw = 10.8;
  steps.forEach((step, i) => {
    const y = top + i * (bh + gap);
    const isDecision = step.type === "decision";
    s.addShape(isDecision ? "roundRect" : "roundRect", {
      x: bx, y, w: bw, h: bh, rectRadius: 0.08,
      fill: { color: isDecision ? C.navy : (i === n - 1 ? C.accent : C.cardBg) },
      line: { type: "none" },
    });
    s.addText(step.text, {
      x: bx + 0.25, y, w: bw - 0.5, h: bh, valign: "middle", align: "left",
      fontFace: FONT_BODY, fontSize: 13.5, bold: isDecision || i === n - 1,
      color: isDecision || i === n - 1 ? C.white : C.navy, margin: 0, lineSpacingMultiple: 1.05,
    });
    // step number badge
    s.addShape("ellipse", { x: bx - 0.42, y: y + bh / 2 - 0.19, w: 0.38, h: 0.38, fill: { color: C.steel }, line: { type: "none" } });
    s.addText(String(i + 1), { x: bx - 0.42, y: y + bh / 2 - 0.19, w: 0.38, h: 0.38, align: "center", valign: "middle", fontFace: FONT_HEAD, bold: true, fontSize: 13, color: C.white, margin: 0 });
    if (i < n - 1) {
      s.addShape("line", { x: bx + bw / 2, y: y + bh, w: 0, h: gap, line: { color: C.steel, width: 1.5, endArrowType: "triangle" } });
    }
  });
  if (note) {
    s.addText(note, { x: bx, y: 7.5 - 0.42, w: bw, h: 0.4, fontFace: FONT_BODY, italic: true, fontSize: 11, color: C.sub, margin: 0 });
  }
  return s;
}

// True branching flowchart slide: sequence of stages rendered top-to-bottom.
// stages: array of —
//   { type: 'step',   text, emphasis? }                         single full-width process box
//   { type: 'decision', question, branches:[{label, text}, ...] } diamond + fan-out branch boxes + fan-in merge
//   { type: 'parallel', header?, branches:[{label?, text}, ...] } fan-out boxes (no diamond) + fan-in merge — for "compute N things, take min/max" patterns
//   { type: 'result', text }                                     final highlighted box (accent fill)
//
// Height budget matters: this slide has ~5.3in of vertical room. A step is ~0.56in, a decision
// diamond + branches is ~1.9in. More than ~3-4 stages (or 2 decisions) will overflow — split into
// multiple flowchartSlide calls instead of cramming everything onto one (see references/pitfalls.md).
function flowchartSlide(pres, { eyebrow, title, stages, note }) {
  const s = bgSlide(pres, C.white);
  sectionHeader(s, { eyebrow, title });
  const bx = 0.9, bw = 10.8;
  const cx = bx + bw / 2;
  const stepH = 0.56, gapV = 0.16;
  const diamondW = 3.6, diamondH = 0.85;
  const branchGap = 0.28;

  let y = 1.78;
  const bottomLimit = 7.5 - (note ? 0.85 : 0.35);

  const arrow = (x1, y1, x2, y2) => {
    s.addShape("line", { x: x1, y: y1, w: x2 - x1, h: y2 - y1, line: { color: C.steel, width: 1.4, endArrowType: "triangle" } });
  };

  stages.forEach((stage, si) => {
    const isLast = si === stages.length - 1;

    if (stage.type === "step" || stage.type === "result") {
      const h = stepH * (stage.lines || 1);
      const fill = stage.type === "result" ? C.accent : (stage.emphasis ? C.navy : C.cardBg);
      const color = stage.type === "result" || stage.emphasis ? C.white : C.navy;
      s.addShape("roundRect", { x: bx, y, w: bw, h, rectRadius: 0.08, fill: { color: fill }, line: { type: "none" } });
      s.addText(stage.text, {
        x: bx + 0.3, y, w: bw - 0.6, h, valign: "middle", align: "left",
        fontFace: FONT_BODY, fontSize: 13.5, bold: stage.type === "result" || stage.emphasis, color, margin: 0, lineSpacingMultiple: 1.05,
      });
      y += h;
      if (!isLast) { arrow(cx, y, cx, y + gapV); y += gapV; }

    } else if (stage.type === "decision" || stage.type === "parallel") {
      const isDecision = stage.type === "decision";
      let branchTopY;
      if (isDecision) {
        s.addShape("diamond", { x: cx - diamondW / 2, y, w: diamondW, h: diamondH, fill: { color: C.navy }, line: { type: "none" } });
        s.addText(stage.question, {
          x: cx - diamondW / 2 + 0.15, y: y + 0.06, w: diamondW - 0.3, h: diamondH - 0.12,
          align: "center", valign: "middle", fontFace: FONT_BODY, bold: true, fontSize: 13, color: C.white, margin: 0, lineSpacingMultiple: 1.0,
        });
        branchTopY = y + diamondH + 0.32;
      } else {
        if (stage.header) {
          s.addText(stage.header, { x: bx, y, w: bw, h: 0.32, align: "center", fontFace: FONT_BODY, italic: true, bold: true, fontSize: 12, color: C.steel, margin: 0 });
          y += 0.32;
        }
        branchTopY = y + 0.22;
      }

      const branches = stage.branches;
      const N = branches.length;
      const totalGap = branchGap * (N - 1);
      const bwBranch = (bw - totalGap) / N;
      const branchLines = Math.max(...branches.map(b => (b.text.match(/\n/g) || []).length + 1));
      const branchH = 0.5 + 0.34 * branchLines;

      branches.forEach((br, i) => {
        const bxi = bx + i * (bwBranch + branchGap);
        const bcx = bxi + bwBranch / 2;
        const fromX = isDecision ? cx : cx;
        const fromY = isDecision ? y + diamondH : y;
        // connector (diagonal fan-out)
        arrow(fromX, fromY, bcx, branchTopY);
        // branch condition label near the connector midpoint
        if (br.label) {
          const lx = (fromX + bcx) / 2, ly = (fromY + branchTopY) / 2;
          s.addShape("rect", { x: lx - 0.55, y: ly - 0.14, w: 1.1, h: 0.28, fill: { color: C.white }, line: { type: "none" } });
          s.addText(br.label, { x: lx - 0.55, y: ly - 0.14, w: 1.1, h: 0.28, align: "center", valign: "middle", fontFace: FONT_BODY, bold: true, fontSize: 11, color: C.accent, margin: 0 });
        }
        s.addShape("roundRect", { x: bxi, y: branchTopY, w: bwBranch, h: branchH, rectRadius: 0.07, fill: { color: C.ice }, line: { type: "none" } });
        s.addText(br.text, {
          x: bxi + 0.14, y: branchTopY, w: bwBranch - 0.28, h: branchH, align: "left", valign: "middle",
          fontFace: FONT_BODY, fontSize: 11.5, bold: true, color: C.navy, margin: 0, lineSpacingMultiple: 1.05,
        });
      });

      const branchBottomY = branchTopY + branchH;
      y = branchBottomY + 0.28;
      if (!isLast) {
        branches.forEach((br, i) => {
          const bxi = bx + i * (bwBranch + branchGap);
          const bcx = bxi + bwBranch / 2;
          arrow(bcx, branchBottomY, cx, y);
        });
      }
    }
  });

  if (note) {
    s.addText(note, { x: bx, y: bottomLimit + 0.02, w: bw, h: 7.5 - bottomLimit - 0.1, fontFace: FONT_BODY, italic: true, fontSize: 11, color: C.sub, margin: 0, valign: "top" });
  }
  return s;
}

// Snake-flow process map slide: a horizontal, wrapping ("boustrophedon") chain of colored
// boxes connected by arrows, reading left-to-right then right-to-left on the next row, ending
// in a highlighted result box (+ optional side callout) and a dark footer checklist bar.
// This is a different visual language from flowchartSlide's vertical decision-diamond tree —
// use flowMapSlide when the point is to show one continuous worked solution path (a sequence
// of concrete computed quantities like "a → c → εt → φ-zone → Mn"), and reserve flowchartSlide
// for genuine multi-way branching logic. The two can coexist in the same deck.
//
// nodes: ordered array read in normal top-to-bottom logical order (the function computes the
// snake/reversal itself). Each entry is either:
//   { text, type }                          single box; type: 'start'|'decision'|'step'
//   { fork: [{text,tint}, {text,tint}] }     two stacked boxes sharing one slot (a fork that
//                                            either merges back into the next single node, or
//                                            — if it falls at a row wrap — continues as one
//                                            flow into the next row). tint: 'blue'|'green'|'pink'|'gray'
//
// result: { text }                          final highlighted (green) box, connected from the
//                                            last node in `nodes` by a vertical arrow
// sideNote: { title, text, color }          optional bordered callout box beside the result
//                                            box (color: 'pink'|'blue'|'gray', default 'pink')
// checklist: { title, items:[{label,detail}] }  optional dark footer bar with inline items
//
// Height/width budget: designed for cols=4-5 and up to 2 rows of nodes (8-10 slots) plus the
// result row and checklist footer. More than 2 rows will overflow — split into two slides
// instead of cramming a longer chain onto one (same principle as flowchartSlide's budget).
function flowMapSlide(pres, { eyebrow, title, subtitle, badge, tag, cols, nodes, result, sideNote, checklist }) {
  const s = bgSlide(pres, C.white);
  cols = cols || 5;

  // ---- header: badge circle + title + subtitle + optional top-right tag ----
  s.addText(eyebrow, { x: 0.55, y: 0.28, w: 8, h: 0.32, fontFace: FONT_BODY, fontSize: 12, bold: true, color: C.accent, charSpacing: 1.5, margin: 0 });
  if (badge) {
    s.addShape("ellipse", { x: 0.55, y: 0.58, w: 0.62, h: 0.62, fill: { color: C.navy }, line: { type: "none" } });
    s.addText(badge, { x: 0.55, y: 0.58, w: 0.62, h: 0.62, align: "center", valign: "middle", fontFace: FONT_HEAD, bold: true, fontSize: 20, color: C.white, margin: 0 });
  }
  const titleX = badge ? 1.35 : 0.55;
  s.addText(title, { x: titleX, y: 0.52, w: 9.2, h: 0.55, fontFace: FONT_HEAD, bold: true, fontSize: 25, color: C.navy, margin: 0 });
  if (subtitle) {
    s.addText(subtitle, { x: titleX, y: 1.05, w: 9.2, h: 0.35, fontFace: FONT_BODY, fontSize: 12.5, color: C.sub, margin: 0 });
  }
  if (tag) {
    s.addText(tag, { x: 10.5, y: 0.55, w: 2.28, h: 0.4, align: "right", fontFace: FONT_BODY, bold: true, fontSize: 13, color: C.steel, margin: 0 });
  }

  // ---- grid geometry ----
  const marginX = 0.55, gapH = 0.28, rowH = 0.92, rowGapV = 0.5;
  const colW = (13.33 - marginX * 2 - gapH * (cols - 1)) / cols;
  const top = 1.62;
  const rows = Math.ceil(nodes.length / cols);

  const TYPE_FILL = { start: C.navy, decision: C.accent, step: C.cardBg };
  const TYPE_TEXT = { start: C.white, decision: C.white, step: C.navy };
  const TINT_FILL = { blue: C.ice, green: C.mintBg, pink: C.pinkBg, gray: C.cardBg };
  const TINT_TEXT = { blue: C.steel, green: C.mintFg, pink: C.pinkFg, gray: C.navy };

  const arrow = (x1, y1, x2, y2) => {
    s.addShape("line", { x: x1, y: y1, w: x2 - x1, h: y2 - y1, line: { color: C.sub, width: 1.5, endArrowType: "triangle" } });
  };

  // position + render each node, tracking anchor points for arrow-drawing
  const anchors = []; // { row, col, x, y, w, h, isFork, topH?, botH? }
  nodes.forEach((node, i) => {
    const row = Math.floor(i / cols);
    const posInRow = i % cols;
    const col = (row % 2 === 0) ? posInRow : (cols - 1 - posInRow);
    const x = marginX + col * (colW + gapH);
    const y = top + row * (rowH + rowGapV);

    if (node.fork) {
      const stackGap = 0.07, miniH = (rowH - stackGap) / 2;
      node.fork.forEach((opt, fi) => {
        const fy = y + fi * (miniH + stackGap);
        const fill = TINT_FILL[opt.tint || "gray"], txt = TINT_TEXT[opt.tint || "gray"];
        s.addShape("roundRect", { x, y: fy, w: colW, h: miniH, rectRadius: 0.06, fill: { color: fill }, line: { type: "none" } });
        s.addText(opt.text, { x: x + 0.12, y: fy, w: colW - 0.24, h: miniH, align: "left", valign: "middle", fontFace: FONT_BODY, bold: true, fontSize: 11, color: txt, margin: 0, lineSpacingMultiple: 1.0 });
      });
      anchors.push({ row, col, x, y, w: colW, h: rowH, isFork: true });
    } else {
      const fill = TYPE_FILL[node.type || "step"], txt = TYPE_TEXT[node.type || "step"];
      s.addShape("roundRect", { x, y, w: colW, h: rowH, rectRadius: 0.07, fill: { color: fill }, line: { type: "none" } });
      s.addText(node.text, { x: x + 0.14, y, w: colW - 0.28, h: rowH, align: "center", valign: "middle", fontFace: FONT_BODY, bold: true, fontSize: 12, color: txt, margin: 0, lineSpacingMultiple: 1.05 });
      anchors.push({ row, col, x, y, w: colW, h: rowH, isFork: false });
    }
  });

  // draw connecting arrows between consecutive nodes
  for (let i = 0; i < anchors.length - 1; i++) {
    const a = anchors[i], b = anchors[i + 1];
    if (a.row === b.row) {
      // same row: horizontal, direction determined by actual x positions
      const goingRight = b.x > a.x;
      const fromSingle = (fromY) => goingRight ? [a.x + a.w, fromY] : [a.x, fromY];
      const toSingle = (toY) => goingRight ? [b.x, toY] : [b.x + b.w, toY];
      if (!a.isFork && !b.isFork) {
        const cy = a.y + a.h / 2;
        const [x1, y1] = fromSingle(cy), [x2, y2] = toSingle(b.y + b.h / 2);
        arrow(x1, y1, x2, y2);
      } else if (a.isFork && !b.isFork) {
        // merge: two lines from each stacked mini-box into the single next box
        const stackGap = 0.07, miniH = (a.h - stackGap) / 2;
        [0, 1].forEach(fi => {
          const fy = a.y + fi * (miniH + stackGap) + miniH / 2;
          const [x1, y1] = fromSingle(fy), [x2, y2] = toSingle(b.y + b.h / 2);
          arrow(x1, y1, x2, y2);
        });
      } else if (!a.isFork && b.isFork) {
        // fork: two lines from the single box into each stacked mini-box
        const stackGap = 0.07, miniH = (b.h - stackGap) / 2;
        [0, 1].forEach(fi => {
          const fy = b.y + fi * (miniH + stackGap) + miniH / 2;
          const [x1, y1] = fromSingle(a.y + a.h / 2), [x2, y2] = toSingle(fy);
          arrow(x1, y1, x2, y2);
        });
      }
    } else {
      // row wrap: single vertical arrow, a and b share the same column by construction
      const cx = a.x + a.w / 2;
      arrow(cx, a.y + a.h, cx, b.y);
    }
  }

  // ---- result box + optional side note, below the last node ----
  let resultBottom = top + rows * rowH + (rows - 1) * rowGapV;
  if (result) {
    const last = anchors[anchors.length - 1];
    const rY = resultBottom + 0.45;
    const rW = last.w, rH = 0.82;
    const cx = last.x + last.w / 2;
    arrow(cx, last.y + last.h, cx, rY);
    s.addShape("roundRect", { x: last.x, y: rY, w: rW, h: rH, rectRadius: 0.08, fill: { color: C.success }, line: { type: "none" } });
    s.addText(result.text, { x: last.x + 0.14, y: rY, w: rW - 0.28, h: rH, align: "center", valign: "middle", fontFace: FONT_HEAD, bold: true, fontSize: 15, color: C.white, margin: 0 });

    if (sideNote) {
      const noteX = last.x + rW + 0.3;
      const noteW = 13.33 - marginX - noteX;
      const tint = sideNote.color || "pink";
      const fill = TINT_FILL[tint], txt = TINT_TEXT[tint];
      const parts = [];
      if (sideNote.title) parts.push({ text: sideNote.title + "　", options: { bold: true, color: txt, fontSize: 12.5 } });
      parts.push({ text: sideNote.text, options: { color: C.navy, fontSize: 11.5 } });
      // Guard: if the result box's column leaves too little horizontal room beside it
      // (this happens whenever the chain's last node lands in one of the rightmost
      // columns — e.g. a short chain that never wraps to a second row), a side-by-side
      // note would get a negative/near-zero width and overflow off the slide edge.
      // Fall back to a full-width banner under the result box instead.
      if (noteW >= 2.3) {
        s.addShape("roundRect", { x: noteX, y: rY, w: noteW, h: rH, rectRadius: 0.08, fill: { color: fill }, line: { color: txt, width: 1.25 } });
        s.addText(parts, { x: noteX + 0.2, y: rY, w: noteW - 0.4, h: rH, valign: "middle", fontFace: FONT_BODY, margin: 0, lineSpacingMultiple: 1.15 });
        resultBottom = rY + rH;
      } else {
        const bannerY = rY + rH + 0.22, bannerH = 0.62, bannerW = 13.33 - marginX * 2;
        s.addShape("roundRect", { x: marginX, y: bannerY, w: bannerW, h: bannerH, rectRadius: 0.08, fill: { color: fill }, line: { color: txt, width: 1.25 } });
        s.addText(parts, { x: marginX + 0.25, y: bannerY, w: bannerW - 0.5, h: bannerH, valign: "middle", fontFace: FONT_BODY, margin: 0, lineSpacingMultiple: 1.1 });
        resultBottom = bannerY + bannerH;
      }
    } else {
      resultBottom = rY + rH;
    }
  }

  // ---- footer checklist bar ----
  if (checklist) {
    const items = checklist.items;
    const n = items.length;
    const barY = 7.5 - 1.0, barH = 0.85, barX = 0.55, barW = 13.33 - barX * 2;
    s.addShape("roundRect", { x: barX, y: barY, w: barW, h: barH, rectRadius: 0.08, fill: { color: C.trapBg }, line: { type: "none" } });
    if (checklist.title) {
      s.addText(checklist.title, { x: barX + 0.25, y: barY + 0.08, w: barW - 0.5, h: 0.3, fontFace: FONT_BODY, bold: true, fontSize: 12.5, color: C.accent, margin: 0 });
    }
    const iw = (barW - 0.5) / n;
    items.forEach((it, i) => {
      const ix = barX + 0.25 + i * iw;
      s.addShape("ellipse", { x: ix, y: barY + 0.48, w: 0.14, h: 0.14, fill: { color: C.accent }, line: { type: "none" } });
      const parts = [
        { text: it.label + "　", options: { bold: true, color: C.white, fontSize: 12 } },
        { text: it.detail || "", options: { color: C.ice, fontSize: 11 } },
      ];
      s.addText(parts, { x: ix + 0.24, y: barY + 0.4, w: iw - 0.35, h: 0.35, valign: "middle", fontFace: FONT_BODY, margin: 0, lineSpacingMultiple: 1.0 });
    });
  }

  return s;
}

// Relationship-diagram slide: embeds a matplotlib-rendered explanatory diagram (from
// gen_diagrams.py / diagram_manifest.json) so students can understand the *behavior* behind
// a formula visually, instead of memorizing it by rote. Optional right-hand "觀念解讀" panel
// with bullet insights that connect the picture back to the formula/variables.
function diagramSlide(pres, { eyebrow, title, diagram, insights, note }) {
  const s = bgSlide(pres, C.white);
  sectionHeader(s, { eyebrow, title });
  const top = 1.85;
  const bottom = 7.5 - (note ? 0.85 : 0.35);
  const availH = bottom - top;
  const hasInsights = insights && insights.length;
  const imgAreaW = hasInsights ? 7.55 : 12.1;
  const pad = 0.22;

  s.addShape("roundRect", { x: 0.6, y: top, w: imgAreaW, h: availH, rectRadius: 0.08, fill: { color: C.cardBg }, line: { type: "none" } });

  const m = diagImg(diagram);
  const innerW = imgAreaW - pad * 2, innerH = availH - pad * 2;
  let w = innerW, h = w / m.ar;
  if (h > innerH) { h = innerH; w = h * m.ar; }
  const ix = 0.6 + (imgAreaW - w) / 2;
  const iy = top + (availH - h) / 2;
  s.addImage({ path: m.file, x: ix, y: iy, w, h });

  if (hasInsights) {
    const sideX = 0.6 + imgAreaW + 0.3;
    const sideW = 13.33 - sideX - 0.6;
    s.addShape("roundRect", { x: sideX, y: top, w: sideW, h: availH, rectRadius: 0.08, fill: { color: C.navy }, line: { type: "none" } });
    s.addText("觀念解讀", { x: sideX + 0.28, y: top + 0.22, w: sideW - 0.56, h: 0.4, fontFace: FONT_BODY, bold: true, fontSize: 13, color: C.accent, margin: 0, charSpacing: 1 });
    const bulletText = insights.map((b, bi) => ({
      text: b,
      options: { bullet: { code: "2726", color: C.accent }, breakLine: bi < insights.length - 1, color: C.white, fontSize: 12.5, paraSpaceAfter: 10 },
    }));
    s.addText(bulletText, { x: sideX + 0.28, y: top + 0.68, w: sideW - 0.56, h: availH - 0.9, fontFace: FONT_BODY, valign: "top", margin: 0, lineSpacingMultiple: 1.2 });
  }

  if (note) {
    s.addText(note, { x: 0.6, y: 7.5 - 0.85, w: 12.1, h: 0.75, fontFace: FONT_BODY, italic: true, fontSize: 11.5, color: C.sub, margin: 0, valign: "top" });
  }
  return s;
}

// One-page formula cheat-sheet: dense grid of small cards (label + formula image), for the
// last-glance review right before walking into the exam room. items: [{label, math}]
function cheatSheetSlide(pres, { eyebrow, title, items, cols }) {
  const s = bgSlide(pres, C.white);
  sectionHeader(s, { eyebrow, title });
  const n = items.length;
  cols = cols || 4;
  const rows = Math.ceil(n / cols);
  const marginX = 0.5, marginTop = 1.7, gap = 0.2;
  const cw = (13.33 - marginX * 2 - gap * (cols - 1)) / cols;
  const chAvail = 7.5 - marginTop - 0.35;
  const ch = (chAvail - gap * (rows - 1)) / rows;

  items.forEach((it, i) => {
    const col = i % cols, row = Math.floor(i / cols);
    const x = marginX + col * (cw + gap);
    const y = marginTop + row * (ch + gap);
    s.addShape("roundRect", { x, y, w: cw, h: ch, rectRadius: 0.06, fill: { color: C.cardBg }, line: { type: "none" } });
    s.addShape("rect", { x, y, w: cw, h: 0.055, fill: { color: C.accent }, line: { type: "none" } });
    s.addText(it.label, { x: x + 0.12, y: y + 0.1, w: cw - 0.24, h: 0.32, fontFace: FONT_BODY, bold: true, fontSize: 10.5, color: C.steel, valign: "top", margin: 0 });

    const m = mathImg(it.math);
    const availW = cw - 0.24, availH = ch - 0.5;
    let w = availW, h = w / m.ar;
    if (h > availH) { h = availH; w = h * m.ar; }
    const ix = x + (cw - w) / 2;
    const iy = y + 0.42 + (availH - h) / 2;
    s.addImage({ path: m.file, x: ix, y: iy, w, h });
  });
  return s;
}

// Knowledge cards grid (for concept-only slides / traps): list of {title, bullets[]}
function cardGridSlide(pres, { eyebrow, title, cards, cols }) {
  const s = bgSlide(pres, C.white);
  sectionHeader(s, { eyebrow, title });
  const n = cards.length;
  cols = cols || (n <= 2 ? n : (n === 4 ? 2 : 3));
  const rows = Math.ceil(n / cols);
  const marginX = 0.6, marginTop = 1.85, gap = 0.3;
  const cw = (13.33 - marginX * 2 - gap * (cols - 1)) / cols;
  const chAvail = 7.5 - marginTop - 0.4;
  const ch = (chAvail - gap * (rows - 1)) / rows;
  cards.forEach((c, i) => {
    const col = i % cols, row = Math.floor(i / cols);
    const x = marginX + col * (cw + gap);
    const y = marginTop + row * (ch + gap);
    s.addShape("roundRect", { x, y, w: cw, h: ch, rectRadius: 0.08, fill: { color: C.cardBg }, line: { type: "none" }, shadow: { type: "outer", color: "1B2A41", opacity: 0.15, blur: 5, offset: 2, angle: 90 } });
    s.addText(c.title, { x: x + 0.22, y: y + 0.15, w: cw - 0.44, h: 0.45, fontFace: FONT_HEAD, bold: true, fontSize: 14.5, color: C.navy, margin: 0 });
    const bulletText = c.bullets.map((b, bi) => ({ text: b, options: { bullet: { code: "2726", color: C.accent }, breakLine: bi < c.bullets.length - 1, color: C.ink, fontSize: 11.5, paraSpaceAfter: 4 } }));
    s.addText(bulletText, { x: x + 0.22, y: y + 0.62, w: cw - 0.44, h: ch - 0.8, fontFace: FONT_BODY, valign: "top", margin: 0, lineSpacingMultiple: 1.1 });
  });
  return s;
}

// Trap cards slide (dark theme, for high-frequency mistakes / "陷阱")
function trapSlide(pres, { eyebrow, title, traps }) {
  const s = bgSlide(pres, C.navy);
  s.addText(eyebrow, { x: 0.6, y: 0.4, w: 11, h: 0.4, fontFace: FONT_BODY, fontSize: 13, bold: true, color: C.accent, charSpacing: 1.5, margin: 0 });
  s.addText(title, { x: 0.6, y: 0.75, w: 12, h: 0.75, fontFace: FONT_HEAD, fontSize: 28, bold: true, color: C.white, margin: 0 });
  const n = traps.length;
  const cols = n <= 2 ? n : 2;
  const rows = Math.ceil(n / cols);
  const marginX = 0.6, marginTop = 1.85, gap = 0.3;
  const cw = (13.33 - marginX * 2 - gap * (cols - 1)) / cols;
  const chAvail = 7.5 - marginTop - 0.4;
  const ch = (chAvail - gap * (rows - 1)) / rows;
  traps.forEach((t, i) => {
    const col = i % cols, row = Math.floor(i / cols);
    const x = marginX + col * (cw + gap);
    const y = marginTop + row * (ch + gap);
    s.addShape("roundRect", { x, y, w: cw, h: ch, rectRadius: 0.08, fill: { color: C.trapBg }, line: { type: "none" } });
    s.addShape("ellipse", { x: x + 0.22, y: y + 0.2, w: 0.36, h: 0.36, fill: { color: C.accent }, line: { type: "none" } });
    s.addText("!", { x: x + 0.22, y: y + 0.2, w: 0.36, h: 0.36, align: "center", valign: "middle", fontFace: FONT_HEAD, bold: true, fontSize: 16, color: C.white, margin: 0 });
    s.addText(t.title, { x: x + 0.7, y: y + 0.18, w: cw - 0.9, h: 0.5, fontFace: FONT_HEAD, bold: true, fontSize: 13.5, color: C.white, margin: 0, valign: "middle" });
    s.addText(t.desc, { x: x + 0.22, y: y + 0.75, w: cw - 0.44, h: ch - 0.95, fontFace: FONT_BODY, fontSize: 11, color: C.ice, valign: "top", margin: 0, lineSpacingMultiple: 1.15 });
  });
  return s;
}

// Table slide
function tableSlide(pres, { eyebrow, title, header, rows, colW }) {
  const s = bgSlide(pres, C.white);
  sectionHeader(s, { eyebrow, title });
  const tRows = [];
  tRows.push(header.map(h => ({ text: h, options: { bold: true, color: C.white, fill: { color: C.navy }, fontFace: FONT_BODY, fontSize: 13, align: "center", valign: "middle" } })));
  rows.forEach((r, i) => {
    tRows.push(r.map(cell => ({ text: cell, options: { color: C.ink, fill: { color: i % 2 === 0 ? C.cardBg : C.white }, fontFace: FONT_BODY, fontSize: 12, align: "left", valign: "middle" } })));
  });
  s.addTable(tRows, { x: 0.6, y: 1.9, w: 12.1, colW, autoPage: false, border: { type: "solid", color: "D9E1EA", pt: 0.75 }, rowH: 0.55 });
  return s;
}

// Closing / summary slide
function closingSlide(pres, { title, points }) {
  const s = bgSlide(pres, C.navy);
  s.addShape("ellipse", { x: -1.2, y: 5.4, w: 3.4, h: 3.4, fill: { color: C.steel, transparency: 65 }, line: { type: "none" } });
  s.addText("考前總複習｜重點回顧", { x: 0.7, y: 0.9, w: 10, h: 0.5, fontFace: FONT_BODY, fontSize: 14, bold: true, color: C.accent, charSpacing: 1.5, margin: 0 });
  s.addText(title, { x: 0.7, y: 1.35, w: 11.5, h: 0.9, fontFace: FONT_HEAD, fontSize: 30, bold: true, color: C.white, margin: 0 });
  const top = 2.5, gap = 0.22, n = points.length;
  const ih = (7.5 - top - 0.5 - gap * (n - 1)) / n;
  points.forEach((p, i) => {
    const y = top + i * (ih + gap);
    s.addShape("roundRect", { x: 0.7, y, w: 11.9, h: ih, rectRadius: 0.06, fill: { color: "24384F" }, line: { type: "none" } });
    s.addShape("ellipse", { x: 0.95, y: y + ih / 2 - 0.15, w: 0.3, h: 0.3, fill: { color: C.accent }, line: { type: "none" } });
    s.addText(String(i + 1), { x: 0.95, y: y + ih / 2 - 0.15, w: 0.3, h: 0.3, align: "center", valign: "middle", fontFace: FONT_HEAD, bold: true, fontSize: 12, color: C.white, margin: 0 });
    s.addText(p, { x: 1.4, y, w: 11.0, h: ih, valign: "middle", fontFace: FONT_BODY, fontSize: 13.5, color: C.ice, margin: 0, lineSpacingMultiple: 1.1 });
  });
  return s;
}

module.exports = { newPres, titleSlide, topicMapSlide, formulaSlide, flowSlide, flowchartSlide, flowMapSlide, diagramSlide, cheatSheetSlide, cardGridSlide, trapSlide, tableSlide, closingSlide, C, FONT_HEAD, FONT_BODY };
