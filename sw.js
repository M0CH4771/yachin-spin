// ヤチンスピン：オフラインでも起動できるようにするキャッシュ
// ゲーム本体（index.html）はネットを優先して、更新がすぐ届くようにする。画像は一度読んだらキャッシュを使う
const VERSION = 'v6';
const CORE = ['./', 'index.html', 'manifest.webmanifest', 'favicon.png', 'icons/icon-192.png', 'icons/icon-512.png', 'bg/festival.jpg'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open('core-' + VERSION).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => !k.endsWith(VERSION)).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== 'GET') return;
  const font = /fonts\.(googleapis|gstatic)\.com$/.test(url.hostname);
  if (url.origin !== location.origin && !font) return;            // ランキングのサーバーなどは素通し
  if (req.mode === 'navigate' || url.pathname.endsWith('/index.html') || url.pathname.endsWith('/')) {
    e.respondWith(fetch(req).then(r => { const copy = r.clone(); caches.open('core-' + VERSION).then(c => c.put('index.html', copy)); return r; })
      .catch(() => caches.match('index.html')));
    return;
  }
  e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(r => {
    if (r.ok || r.type === 'opaque') { const copy = r.clone(); caches.open('assets-' + VERSION).then(c => c.put(req, copy)); }
    return r;
  })));
});
