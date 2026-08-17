/**
 * Configuracao do Puppeteer para o mermaid-cli (mmdc).
 *
 * Motivo da existencia: o puppeteer-core varre os diretorios ascendentes a
 * partir do cwd em busca de config (lilconfig). Nesta maquina, o
 * /c/Users/<usuario>/package.json possui BOM (byte order mark), o que faz o
 * JSON.parse do lilconfig lancar SyntaxError e o mmdc abortar antes de
 * renderizar qualquer diagrama. Com este arquivo na raiz do projeto, a
 * varredura encontra a config aqui e nunca sobe ate o home.
 */
const CHROME = process.env.ORCA_PUPPETEER_CHROME
  || "C:/Program Files/Google/Chrome/Application/chrome.exe";

module.exports = {
  launch: {
    executablePath: CHROME,
    args: ["--no-sandbox", "--disable-dev-shm-usage"],
  },
};
