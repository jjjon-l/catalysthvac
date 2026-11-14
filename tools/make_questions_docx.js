// Build a fillable Word version of 06-questions-for-derrek.md.
// Usage: node make_questions_docx.js <input.md> <output.docx>
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType,
  ShadingType, BorderStyle, HeadingLevel, AlignmentType, PageOrientation,
  LevelFormat, Footer, PageNumber, TableLayoutType,
} = require("docx");

const [, , inPath, outPath] = process.argv;
const lines = fs.readFileSync(inPath, "utf8").split("\n");

const NAVY = "1B1B5C", RED = "B51C20", FILL = "FFF8D6", BORDER = "C9CDD8", FONT = "Arial";
const PAGE_W = 14400; // landscape letter, 0.5" margins

// Inline markdown: **bold**, escaped underscores, links -> text
function runs(text, base = {}) {
  text = text.replace(/\\_/g, "_").replace(/\[([^\]]+)\]\([^)]+\)/g, "$1");
  const out = [];
  text.split(/(\*\*[^*]+\*\*)/).forEach((part) => {
    if (!part) return;
    const bold = part.startsWith("**") && part.endsWith("**");
    out.push(new TextRun({ text: bold ? part.slice(2, -2) : part, bold: bold || base.bold, color: base.color, size: base.size, font: FONT }));
  });
  return out;
}

const cellBorders = { top: { style: BorderStyle.SINGLE, size: 4, color: BORDER }, bottom: { style: BorderStyle.SINGLE, size: 4, color: BORDER },
  left: { style: BorderStyle.SINGLE, size: 4, color: BORDER }, right: { style: BorderStyle.SINGLE, size: 4, color: BORDER } };

function widthsFor(header) {
  const h = header.map((x) => x.trim().toLowerCase());
  if (h.length === 4 && h[0] === "#" && h[3] === "answer") return [700, 4400, 5200, 4100];
  if (h.length === 2 && h[1] === "recipient") return [6400, 8000];
  if (h.length === 4) return [2400, 4000, 4000, 4000];
  const w = Math.floor(PAGE_W / h.length);
  return h.map((_, i) => (i === h.length - 1 ? PAGE_W - w * (h.length - 1) : w));
}

function table(rows) {
  const header = rows[0];
  const widths = widthsFor(header);
  const answerCol = header.findIndex((c) => /^(answer|recipient)$/i.test(c.trim()));
  const trs = rows.map((cells, ri) => new TableRow({
    tableHeader: ri === 0,
    cantSplit: true,
    children: cells.map((c, ci) => {
      const isHead = ri === 0, isAnswer = !isHead && ci === answerCol;
      return new TableCell({
        width: { size: widths[ci], type: WidthType.DXA },
        borders: cellBorders,
        margins: { top: 100, bottom: 100, left: 120, right: 120 },
        shading: isHead ? { type: ShadingType.CLEAR, fill: NAVY, color: "auto" }
               : isAnswer ? { type: ShadingType.CLEAR, fill: FILL, color: "auto" } : undefined,
        children: [new Paragraph({ children: runs(c.trim(), isHead ? { bold: true, color: "FFFFFF", size: 20 } : { size: 20 }) })],
      });
    }),
  }));
  return new Table({ width: { size: PAGE_W, type: WidthType.DXA }, columnWidths: widths, layout: TableLayoutType.FIXED, rows: trs });
}

const children = [];
let i = 0;
while (i < lines.length) {
  const line = lines[i];
  if (line.trimStart().startsWith("|")) {
    const rows = [];
    while (i < lines.length && lines[i].trimStart().startsWith("|")) {
      const cells = lines[i].trim().replace(/\\\|/g, "\u0000").split("|").slice(1, -1).map((c) => c.replace(/\u0000/g, "|"));
      if (!cells.every((c) => /^\s*-{3,}\s*$/.test(c))) rows.push(cells);
      i++;
    }
    children.push(table(rows));
    children.push(new Paragraph({ spacing: { after: 120 }, children: [] }));
    continue;
  }
  const indent = line.match(/^(\s*)/)[1].length;
  const t = line.trim();
  if (t === "") { i++; continue; }
  if (t === "---") {
    children.push(new Paragraph({ border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: BORDER, space: 1 } }, spacing: { after: 200 }, children: [] }));
  } else if (t.startsWith("# ")) {
    children.push(new Paragraph({ heading: HeadingLevel.TITLE, children: runs(t.slice(2)) }));
  } else if (t.startsWith("## ")) {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: runs(t.slice(3)) }));
  } else if (/^\d+\.\s/.test(t) && indent === 0) {
    children.push(new Paragraph({ numbering: { reference: "nums", level: 0 }, spacing: { after: 80 }, children: runs(t.replace(/^\d+\.\s/, "")) }));
  } else if (t.startsWith("- ")) {
    children.push(new Paragraph({ numbering: { reference: "bullets", level: indent >= 2 ? 1 : 0 }, spacing: { after: 60 }, children: runs(t.slice(2)) }));
  } else {
    children.push(new Paragraph({ spacing: { after: 120 }, indent: indent >= 2 ? { left: 720 } : undefined, children: runs(t) }));
  }
  i++;
}

const doc = new Document({
  creator: "Jonathan Lass",
  title: "Catalyst Website: Questions Before Launch",
  styles: {
    default: { document: { run: { font: FONT, size: 21 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", next: "Normal", run: { font: FONT, size: 40, bold: true, color: NAVY }, paragraph: { spacing: { before: 0, after: 160 }, keepNext: true } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 28, bold: true, color: NAVY },
        paragraph: { spacing: { before: 320, after: 140 }, keepNext: true, outlineLevel: 0, border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: RED, space: 4 } } } },
    ],
  },
  numbering: { config: [
    { reference: "bullets", levels: [
      { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
      { level: 1, format: LevelFormat.BULLET, text: "◦", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1440, hanging: 360 } } } } ] },
    { reference: "nums", levels: [
      { level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } } ] },
  ] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE }, margin: { top: 720, bottom: 720, left: 720, right: 720 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [
      new TextRun({ text: "Catalyst website questions · page ", size: 16, color: "6B7085", font: FONT }),
      new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "6B7085", font: FONT }) ] })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(outPath, buf); console.log("wrote", outPath, buf.length, "bytes"); });
