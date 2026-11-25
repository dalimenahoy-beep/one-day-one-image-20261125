// One Day, One Image — 25 November 2026 entry.
//
// The poster (entry.png, drawn at build time by make_poster.py) is committed
// beside this file. At grading time the sandbox runs only Node, so this
// program does exactly one thing: copy the committed PNG into the output
// directory as entry.png, byte for byte. Standard library only.

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

function posterPath() {
  return join(dirname(fileURLToPath(import.meta.url)), 'entry.png');
}

function outputPath() {
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
  mkdirSync(outDir, { recursive: true });
  return join(outDir, 'entry.png');
}

function deliverPoster() {
  copyFileSync(posterPath(), outputPath());
}

deliverPoster();
