// mmdc-wrapper.cjs — roda o mermaid-cli com os fixes desta maquina:
//   1. PUPPETEER_EXECUTABLE_PATH -> chrome-headless-shell do playwright;
//   2. cwd de trabalho em pasta TEMPORARIA (o puppeteer faz lilconfig por busca
//      ascendente; o package.json do projeto tem BOM e quebra o JSON.parse).
//   3. -p --puppeteerConfigFile: o wrapper gera a config com executablePath +
//      no-sandbox numa pasta temporaria (sem procurar config global do user).
const { spawnSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const NPM_ROOT = path.join(process.env.APPDATA || '', 'npm');
const MMDC_CLI = path.join(NPM_ROOT, 'node_modules', '@mermaid-js', 'mermaid-cli', 'src', 'cli.js');

function acharChrome() {
  const raiz = path.join(process.env.LOCALAPPDATA || path.join(process.env.USERPROFILE, 'AppData', 'Local'), 'ms-playwright');
  if (!fs.existsSync(raiz)) return null;
  try {
    const versoes = fs.readdirSync(raiz).filter(n => n.startsWith('chromium_headless_shell'));
    versoes.sort();
    for (const v of versoes.reverse()) {
      const exe = path.join(raiz, v, 'chrome-headless-shell-win64', 'chrome-headless-shell.exe');
      if (fs.existsSync(exe)) return exe;
    }
  } catch (e) { /* ignore */ }
  return null;
}

const chrome = acharChrome();
if (chrome) process.env.PUPPETEER_EXECUTABLE_PATH = chrome;

// Monta os argumentos: caminhos relativos viram absolutos (para o mmdc rodar
// com cwd temporario), -p ganha config gerada por nos.
const args = [];
const orig = process.argv.slice(2);
const sentinela = '--puppeteerConfigFile';
for (let i = 0; i < orig.length; i++) {
  const a = orig[i];
  if (a === '-p' || a === '--puppeteerConfigFile' || a === '--puppeteerConfigFile=') {
    if (a.includes('=')) { args.push(a.split('=')[0] + '=__PPCFG__'); }
    else { args.push(sentinela); args.push('__PPCFG__'); i++; }
  } else if (!path.isAbsolute(a) && a.startsWith && !a.startsWith('-')) {
    args.push(path.resolve(process.cwd(), a));
  } else {
    args.push(a);
  }
}

// workdir temporario (sem package.json do projeto) + config puppeteer propria
const work = fs.mkdtempSync(path.join(os.tmpdir(), 'mmdc-work-'));
const cfg = { executablePath: chrome, args: ['--no-sandbox', '--disable-dev-shm-usage'] };
const cfgPath = path.join(work, 'puppeteer.json');
fs.writeFileSync(cfgPath, JSON.stringify(cfg), 'utf8');
const finalArgs = args.map(a => a === '__PPCFG__' ? cfgPath : a);

const r = spawnSync(process.execPath, [MMDC_CLI, ...finalArgs], { stdio: 'inherit', env: process.env, cwd: work });
if (r.status === 0) {
  const outIdx = finalArgs.indexOf('-o');
  if (outIdx >= 0 && finalArgs[outIdx + 1]) {
    const gerado = path.join(work, path.basename(finalArgs[outIdx + 1]));
    if (fs.existsSync(gerado)) fs.copyFileSync(gerado, finalArgs[outIdx + 1]);
  }
}
try { fs.rmSync(work, { recursive: true, force: true }); } catch (e) { /* ignore */ }
process.exit(r.status === null ? 1 : r.status);