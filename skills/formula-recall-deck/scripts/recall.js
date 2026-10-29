// 額外元件：回想卡（Q）、大字標語、分級圖例。沿用 lib.js 的配色與字型。
const { C, FONT_HEAD, FONT_BODY } = require("./lib.js");

const LEVEL = {
  red:    { color: "C0392B", label: "必背", desc: "考卷不會給" },
  orange: { color: "E8734A", label: "會給但別賭", desc: "有沒給的先例" },
  green:  { color: "1E8449", label: "通常會給", desc: "背概念就好" },
};

// 全螢幕深色「回想卡」：只出題，不給答案，給影片一個自然的暫停點
function recallSlide(pres, { index, total, level, topic, question, hint, seconds }) {
  const lv = LEVEL[level] || LEVEL.red;
  const s = pres.addSlide();
  s.background = { color: C.navy };
  s.addShape("ellipse", { x: -1.6, y: 5.2, w: 4.2, h: 4.2, fill: { color: C.steel, transparency: 72 }, line: { type: "none" } });
  s.addShape("ellipse", { x: 11.6, y: -1.5, w: 3.6, h: 3.6, fill: { color: lv.color, transparency: 78 }, line: { type: "none" } });

  s.addText(`回想卡 ${String(index).padStart(2, "0")} / ${String(total).padStart(2, "0")}`, {
    x: 0.75, y: 0.5, w: 5, h: 0.4, fontFace: FONT_BODY, fontSize: 14, bold: true,
    color: C.ice, charSpacing: 2, margin: 0,
  });
  s.addText(topic, {
    x: 7.0, y: 0.5, w: 5.6, h: 0.4, fontFace: FONT_BODY, fontSize: 13, color: C.steel,
    align: "right", margin: 0,
  });

  const pillW = 2.5;
  s.addShape("roundRect", { x: 0.75, y: 1.15, w: pillW, h: 0.5, rectRadius: 0.25, fill: { color: lv.color }, line: { type: "none" } });
  s.addText(`${lv.label}｜${lv.desc}`, {
    x: 0.75, y: 1.15, w: pillW, h: 0.5, fontFace: FONT_BODY, fontSize: 11.5, bold: true,
    color: C.white, align: "center", valign: "middle", margin: 0,
  });

  s.addText(question, {
    x: 0.75, y: 2.05, w: 11.8, h: 2.5, fontFace: FONT_HEAD, fontSize: 38, bold: true,
    color: C.white, margin: 0, valign: "top", lineSpacingMultiple: 1.15,
  });

  if (hint) {
    s.addShape("rect", { x: 0.75, y: 4.75, w: 0.07, h: 0.75, fill: { color: lv.color }, line: { type: "none" } });
    s.addText(hint, {
      x: 1.05, y: 4.75, w: 11.4, h: 0.75, fontFace: FONT_BODY, fontSize: 15, color: C.ice,
      margin: 0, valign: "top", lineSpacingMultiple: 1.1,
    });
  }

  // 倒數圓點
  const n = seconds || 3;
  for (let i = 0; i < n; i++) {
    s.addShape("ellipse", {
      x: 0.75 + i * 0.42, y: 6.35, w: 0.26, h: 0.26,
      fill: { color: i === 0 ? lv.color : "3A4E68" }, line: { type: "none" },
    });
  }
  s.addText(`蓋住下一頁，先在紙上寫出來 — ${n} 秒`, {
    x: 0.75 + n * 0.42 + 0.25, y: 6.25, w: 8, h: 0.45, fontFace: FONT_BODY, fontSize: 13.5,
    color: C.steel, valign: "middle", margin: 0,
  });
  return s;
}

// 大字標語（一句話重點）
function bigIdeaSlide(pres, { eyebrow, lines, footnote, accent }) {
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape("rect", { x: 0, y: 0, w: 0.28, h: 7.5, fill: { color: accent || C.accent }, line: { type: "none" } });
  s.addText(eyebrow, {
    x: 0.95, y: 1.0, w: 11, h: 0.5, fontFace: FONT_BODY, fontSize: 14, bold: true,
    color: accent || C.accent, charSpacing: 2, margin: 0,
  });
  const rich = lines.map((l, i) => ({
    text: l.text,
    options: {
      breakLine: i < lines.length - 1,
      color: l.em ? (accent || C.accent) : C.navy,
      bold: true,
      fontSize: l.size || 30,
    },
  }));
  s.addText(rich, {
    x: 0.95, y: 1.75, w: 11.6, h: 4.1, fontFace: FONT_HEAD, valign: "top", margin: 0,
    lineSpacingMultiple: 1.28,
  });
  if (footnote) {
    s.addText(footnote, {
      x: 0.95, y: 6.05, w: 11.6, h: 1.0, fontFace: FONT_BODY, fontSize: 14, color: C.sub,
      margin: 0, valign: "top", lineSpacingMultiple: 1.15,
    });
  }
  return s;
}

// 三色分級圖例（本片的「玩法說明」）
function legendSlide(pres, { title, subtitle, items, howto }) {
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addText("HOW TO USE", { x: 0.6, y: 0.4, w: 11, h: 0.4, fontFace: FONT_BODY, fontSize: 13, bold: true, color: C.accent, charSpacing: 1.5, margin: 0 });
  s.addText(title, { x: 0.6, y: 0.75, w: 12, h: 0.6, fontFace: FONT_HEAD, fontSize: 28, bold: true, color: C.navy, margin: 0 });
  s.addText(subtitle, { x: 0.6, y: 1.42, w: 12, h: 0.45, fontFace: FONT_BODY, fontSize: 14, color: C.sub, margin: 0 });

  const cw = (13.33 - 1.2 - 0.6) / 3;
  items.forEach((it, i) => {
    const lv = LEVEL[it.level];
    const x = 0.6 + i * (cw + 0.3);
    const y = 2.1;
    const h = 2.55;
    s.addShape("roundRect", { x, y, w: cw, h, rectRadius: 0.09, fill: { color: C.cardBg }, line: { type: "none" } });
    s.addShape("rect", { x, y, w: cw, h: 0.12, fill: { color: lv.color }, line: { type: "none" } });
    s.addShape("ellipse", { x: x + 0.3, y: y + 0.42, w: 0.42, h: 0.42, fill: { color: lv.color }, line: { type: "none" } });
    s.addText(it.count, { x: x + 0.85, y: y + 0.36, w: cw - 1.1, h: 0.55, fontFace: FONT_HEAD, fontSize: 26, bold: true, color: lv.color, margin: 0, valign: "middle" });
    s.addText(lv.label, { x: x + 0.3, y: y + 1.0, w: cw - 0.6, h: 0.4, fontFace: FONT_HEAD, fontSize: 17, bold: true, color: C.navy, margin: 0 });
    s.addText(it.desc, { x: x + 0.3, y: y + 1.45, w: cw - 0.6, h: h - 1.6, fontFace: FONT_BODY, fontSize: 12.5, color: C.sub, margin: 0, valign: "top", lineSpacingMultiple: 1.15 });
  });

  s.addShape("roundRect", { x: 0.6, y: 4.95, w: 12.1, h: 2.05, rectRadius: 0.09, fill: { color: C.navy }, line: { type: "none" } });
  s.addText("這支影片怎麼看", { x: 0.95, y: 5.15, w: 5, h: 0.4, fontFace: FONT_BODY, fontSize: 13, bold: true, color: C.accent, charSpacing: 1, margin: 0 });
  const rich = howto.map((t, i) => ({
    text: t,
    options: { bullet: { code: "2726", color: C.accent }, breakLine: i < howto.length - 1, color: C.white, fontSize: 13, paraSpaceAfter: 6 },
  }));
  s.addText(rich, { x: 0.95, y: 5.6, w: 11.4, h: 1.3, fontFace: FONT_BODY, valign: "top", margin: 0, lineSpacingMultiple: 1.15 });
  return s;
}

module.exports = { recallSlide, bigIdeaSlide, legendSlide, LEVEL };
