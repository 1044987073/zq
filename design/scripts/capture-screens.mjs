/**
 * 从 Vue 设计实现导出 PNG，供拖入即时设计作参考。
 * 用法：在 diy-stall-design 目录 npm run build 后，于 design/scripts 执行：
 *   node capture-screens.mjs
 */
import { chromium } from 'playwright';
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { mkdirSync } from 'fs';

const __dir = dirname(fileURLToPath(import.meta.url));
const outDir = join(__dir, '..', 'screens');
const designRoot = join(__dir, '..', '..', 'diy-stall-design');
const port = 4173;
const base = `http://127.0.0.1:${port}`;

const routes = [
  { name: 'U1-home', path: '/', mobile: true },
  { name: 'U2-catalog', path: '/catalog', mobile: true },
  { name: 'U3-detail', path: '/product/pumpkin-s', mobile: true },
  { name: 'U4-bundles', path: '/bundles', mobile: true },
  { name: 'U5-about', path: '/about', mobile: true },
  { name: 'A1-login', path: '/admin/login', mobile: false },
  { name: 'A2-dashboard', path: '/admin', mobile: false, admin: true },
  { name: 'A3-products', path: '/admin/products', mobile: false, admin: true }
];

mkdirSync(outDir, { recursive: true });

function wait(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

const preview = spawn('npx', ['vite', 'preview', '--port', String(port)], {
  cwd: designRoot,
  stdio: 'ignore',
  shell: true
});

await wait(2500);

const browser = await chromium.launch();
try {
  for (const r of routes) {
    const context = await browser.newContext(
      r.mobile
        ? { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 }
        : { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 }
    );
    const page = await context.newPage();
    if (r.admin) {
      await page.goto(`${base}/admin/login`);
      await page.fill('input[type="password"]', 'demo123');
      await page.click('button[type="submit"]');
      await wait(500);
    }
    await page.goto(`${base}${r.path}`);
    await wait(600);
    await page.screenshot({ path: join(outDir, `${r.name}.png`), fullPage: r.mobile });
    await context.close();
  }
  console.log('Screens saved to', outDir);
} finally {
  await browser.close();
  preview.kill();
}
