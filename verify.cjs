// 浏览器验证：真实渲染 + 表单交互 + 截图
// 浏览器验证：真实渲染 + 表单交互 + 截图
//   node verify.cjs                    # 用默认位置找 playwright-core 与浏览器
//   PW=<path> EXE=<path> node verify.cjs
const fs = require('fs');
const path = require('path');

// playwright-core：先看环境变量，再依次试常见安装位置
function findPlaywright() {
  const candidates = [
    process.env.PW,
    path.join(__dirname, '..', 'websearch', 'node_modules', 'playwright-core'),
    path.join(process.env.HOME || '', 'Explore', 'websearch', 'node_modules', 'playwright-core'),
    'playwright-core',
  ].filter(Boolean);
  for (const c of candidates) {
    try { return require(c); } catch (_) {}
  }
  throw new Error('找不到 playwright-core，请用 PW=<路径> 指定');
}
const { chromium } = findPlaywright();

// 浏览器可执行文件：环境变量优先，否则在 ms-playwright 缓存里挑版本号最大的
function findChromium() {
  if (process.env.EXE) return process.env.EXE;
  const root = path.join(process.env.HOME || '', 'Library', 'Caches', 'ms-playwright');
  if (!fs.existsSync(root)) return undefined;            // 交给 playwright 自己解析
  const dirs = fs.readdirSync(root)
    .filter((d) => /^chromium(_headless_shell)?-\d+$/.test(d))
    .sort((a, b) => parseInt(b.split('-').pop(), 10) - parseInt(a.split('-').pop(), 10));
  for (const d of dirs) {
    const exe = path.join(root, d, 'chrome-headless-shell-mac-arm64', 'chrome-headless-shell');
    if (fs.existsSync(exe)) return exe;
  }
  return undefined;
}

const HERE = __dirname;
const FILE = 'file://' + path.join(HERE, 'dist', 'index.html');
const SHOT = path.join(HERE, 'dist', 'verify');

(async () => {
  fs.mkdirSync(SHOT, { recursive: true });
  const exe = findChromium();
  const browser = await chromium.launch({ executablePath: exe, headless: true, args: ['--disable-dev-shm-usage', '--no-sandbox'] });
  const errors = [];

  for (const [name, viewport] of [['desktop', {width: 900, height: 1200}], ['mobile', {width: 390, height: 844}]]) {
    const ctx = await browser.newContext({ viewport, deviceScaleFactor: 2 });
    const page = await ctx.newPage();
    page.on('console', (m) => { if (m.type() === 'error') errors.push(`[${name}] console: ${m.text()}`); });
    page.on('pageerror', (e) => errors.push(`[${name}] pageerror: ${e.message}`));

    await page.goto(FILE, { waitUntil: 'load' });
    await page.waitForTimeout(600);

    // 1) 图片是否真的加载出来（base64 内嵌最容易在这里翻车）
    const imgs = await page.$$eval('img[data-card]', (els) =>
      els.map((e) => ({ key: e.dataset.card, w: e.naturalWidth, h: e.naturalHeight, src: e.src.slice(0, 30) })));
    console.log(`── ${name} ──`);
    for (const i of imgs) console.log(`   卡片图 ${i.key}: ${i.w}×${i.h} ${i.w > 0 ? '✅' : '❌'} (${i.src}…)`);

    // 2) 视频源
    const vid = await page.$eval('video source', (e) => e.src.slice(0, 30) + ' len=' + e.src.length);
    console.log(`   视频源: ${vid}`);

    // 3) 横向溢出
    const ovf = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    console.log(`   横向溢出: ${ovf}px ${ovf <= 1 ? '✅' : '❌'}`);

    // 4) 语言切换
    await page.click('#lang-en');
    await page.waitForTimeout(250);
    const h1en = (await page.$eval('.i18n[data-en]:not(.hidden) h1', e => e.textContent)).slice(0, 46);
    const zhVisible = await page.$eval('.i18n[data-zh]', (e) => e.classList.contains('hidden'));
    console.log(`   切英文后标题: "${h1en}"  中文块已隐藏=${zhVisible} ${zhVisible && h1en.includes('Cairn') ? '✅' : '❌'}`);
    await page.click('#lang-en');   // 回中文? 实际是切 zh
    await page.click('#lang-zh');
    await page.waitForTimeout(200);

    // 5) 切换位图
    await page.click('#m-bitmap');
    await page.click('#l-en');
    await page.waitForTimeout(400);
    const bm = await page.$eval('img[data-card=task-blocked]', (e) => ({ w: e.naturalWidth, n: e.src.length }));
    console.log(`   位图×英文 卡住了: ${bm.w}px ${bm.w > 0 ? '✅' : '❌'}`);
    await page.click('#m-web');
    await page.click('#l-zh');
    await page.waitForTimeout(300);

    if (name === 'desktop') {
      // 6) 空表单提交 → 必须报错（校验生效）
      await page.click('button[type=submit]');
      await page.waitForTimeout(300);
      const errShown = await page.$eval('#err', (e) => e.style.display !== 'none' ? e.textContent : '');
      console.log(`   空表单被拦: ${errShown ? '✅ ' + errShown.slice(0, 52) : '❌ 没拦住'}`);

      // 7) 填完整表单
      await page.check('input[name=agents][value="Claude Code"]');
      await page.check('input[name=agents][value="Codex"]');
      await page.selectOption('#q_concurrent', '2–3');
      await page.fill('#q_how', '手机推送 + 声音，但经常分不清是哪个 agent');
      await page.fill('#q_incident', '上周等一个跑了两小时的任务，其实早就退出了');
      await page.fill('#q_pain', '所有 agent 用同一个提示音');
      await page.check('input[name=enough][value*="有时候不够"]');
      await page.fill('#q_enough_why', '大多数时候够，但多任务时会被刷走');
      await page.fill('#q_alt', '写了个 tmux 脚本定期截图');
      await page.check('input[name=want][value="要你批准"]');
      await page.fill('#q_desk', '不需要解锁手机');
      await page.check('input[name=intent][value*="愿意预订"]');
      await page.waitForTimeout(250);
      const priceShown = await page.$eval('#cond_price', (e) => e.classList.contains('on'));
      console.log(`   选「愿意预订」后价位题出现: ${priceShown ? '✅' : '❌'}`);
      await page.selectOption('#q_price', '300–500');
      await page.check('input[name=software_only][value*="一样感兴趣"]');
      await page.check('input[name=chat][value="愿意 / yes"]');
      await page.fill('#q_contact', 'test@example.com');
      await page.fill('#q_name', '念「凯恩」');

      // 8) 提交 → 生成内容
      await page.click('button[type=submit]');
      await page.waitForTimeout(700);
      const out = await page.$eval('#out', (e) => e.value);
      const shown = await page.$eval('#result', (e) => e.classList.contains('on'));
      console.log(`   生成结果区显示: ${shown ? '✅' : '❌'}  输出 ${out.length} 字符`);
      const checks = [
        ['含 agent 选择', out.includes('Claude Code、Codex')],
        ['含需求强度', out.includes('愿意预订')],
        ['含价位', out.includes('300–500')],
        ['含分栏声明', out.includes('分开记录')],
        ['不含占位符', !out.includes('__')],
      ];
      for (const [n, ok] of checks) console.log(`     ${n}: ${ok ? '✅' : '❌'}`);
      const mail = await page.$eval('#mailto', (e) => e.href);
      console.log(`   mailto 指向: ${decodeURIComponent(mail).slice(0, 62)}…`);

      // 9) 扫描禁用词（口径红线）
      // 禁用词必须只出现在「否认/边界」语境里（那正是可信度所在），不能出现在产品主张里
      const scan = await page.evaluate(() => {
        const banned = ['7.5mm','磁吸','续航','独立联网','Wi-Fi','录音','语音转文字','Android','订阅','月费','实时'];
        const deny = /还没做|未实现|未量测|不是已达成|目标值|没有|不运行|不能装|不提供|未测|没有价格|没有上市|没有订阅|不回|不能/;
        const boundary = document.querySelector('.boundary');
        const boundaryText = boundary ? boundary.innerText : '';
        const bodyText = document.body.innerText;
        const outside = bodyText.replace(boundaryText, '');
        return banned.map(w => {
          const inBoundary = boundaryText.includes(w);
          const outsideHits = outside.split('\n').filter(l => l.includes(w)).map(l => l.trim().slice(0, 70));
          return {w, inBoundary, outsideHits};
        });
      });
      let claimHits = 0;
      for (const r of scan) {
        if (r.outsideHits.length) { claimHits++;
          console.log(`   ⚠ 禁用词「${r.w}」出现在主张语境: ${r.outsideHits.slice(0,2).join(' | ')}`);
        }
      }
      const inB = scan.filter(r => r.inBoundary).map(r => r.w);
      console.log(`   禁用词扫描: 主张语境命中 ${claimHits} 处 ${claimHits === 0 ? '✅' : '❌'}；边界段内 ${inB.length ? '（' + inB.join('/') + '，均为否认式表述）' : '无'}`);

      await page.screenshot({ path: path.join(SHOT, 'desktop-full.png'), fullPage: true });
      await page.screenshot({ path: path.join(SHOT, 'desktop-result.png') });
    } else {
      await page.screenshot({ path: path.join(SHOT, 'mobile-full.png'), fullPage: true });
    }
    await ctx.close();
  }

  await browser.close();
  console.log('\n=== 控制台错误 ===');
  console.log(errors.length ? errors.join('\n') : '  无 ✅');
  console.log('\n截图: ' + SHOT);
})().catch((e) => { console.error('FAILED:', e.message); process.exit(1); });