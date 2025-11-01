#!/usr/bin/env node
/**
 * Screenshot capture script - converts terminal output to images using Playwright
 */

const fs = require('fs').promises;
const path = require('path');
const { chromium } = require('playwright');

async function loadCurrentPattern() {
  const patternFile = path.join('outputs', 'current_pattern.json');
  const content = await fs.readFile(patternFile, 'utf-8');
  return JSON.parse(content);
}

async function loadTerminalOutput() {
  const today = new Date().toISOString().split('T')[0];
  const outputFile = path.join('outputs', today, 'terminal_output.txt');
  return await fs.readFile(outputFile, 'utf-8');
}

async function generateHTML(terminalOutput) {
  // Convert ANSI codes to HTML
  // For simplicity, we'll use a pre-formatted approach
  // In production, you'd want to properly parse ANSI codes

  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {
      background: #1e1e1e;
      color: #d4d4d4;
      font-family: 'Courier New', monospace;
      padding: 20px;
      margin: 0;
    }
    pre {
      font-size: 14px;
      line-height: 1.6;
      white-space: pre-wrap;
      word-wrap: break-word;
    }
  </style>
</head>
<body>
  <pre>${escapeHtml(terminalOutput)}</pre>
</body>
</html>
  `;
}

function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

async function captureScreenshot(html, outputPath) {
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 1200, height: 800 }
  });

  await page.setContent(html);
  await page.screenshot({
    path: outputPath,
    fullPage: true
  });

  await browser.close();
}

async function main() {
  try {
    console.log('📸 Capturing terminal screenshots...');

    // Load pattern info
    const pattern = await loadCurrentPattern();
    console.log(`Pattern: ${pattern.name}`);

    // Load terminal output
    const terminalOutput = await loadTerminalOutput();
    console.log('✓ Terminal output loaded');

    // Generate HTML
    const html = generateHTML(terminalOutput);
    console.log('✓ HTML generated');

    // Create output directory
    const today = new Date().toISOString().split('T')[0];
    const screenshotDir = path.join('outputs', today, 'screenshots');
    await fs.mkdir(screenshotDir, { recursive: true });

    // Capture screenshot
    const screenshotPath = path.join(screenshotDir, 'terminal_output.png');
    await captureScreenshot(html, screenshotPath);

    console.log(`✓ Screenshot saved to ${screenshotPath}`);
  } catch (error) {
    console.error('Error capturing screenshots:', error);
    process.exit(1);
  }
}

main();
