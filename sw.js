const CACHE = "central-aprovacao-v7-2";
const ASSETS = ["./", "./index.html", "./manifest.webmanifest", "./icons/icon.svg"];

const BOOTSTRAP = `
window.addEventListener('load', () => {
  let tentativas = 0;
  const iniciar = async () => {
    if (typeof window.initSupabase === 'function') {
      try {
        await window.initSupabase();
        if (typeof window.renderConta === 'function') window.renderConta();
      } catch (e) {
        console.error('Falha ao inicializar Supabase:', e);
      }
      return;
    }
    if (tentativas++ < 30) setTimeout(iniciar, 100);
  };
  iniciar();
});
`;

self.addEventListener("install", event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
  );
  self.clients.claim();
});

self.addEventListener("fetch", event => {
  if (event.request.method !== "GET") return;
  const url = new URL(event.request.url);

  if (url.pathname.endsWith("/config.js")) {
    event.respondWith(
      fetch(event.request).then(async response => {
        const text = await response.text();
        return new Response(text + "\n" + BOOTSTRAP, {
          status: response.status,
          statusText: response.statusText,
          headers: {"Content-Type": "application/javascript; charset=utf-8", "Cache-Control": "no-store"}
        });
      })
    );
    return;
  }

  if (event.request.mode === "navigate" || url.pathname.endsWith("/index.html")) {
    event.respondWith(
      fetch(event.request).then(response => {
        const copy = response.clone();
        caches.open(CACHE).then(cache => cache.put(event.request, copy));
        return response;
      }).catch(() => caches.match("./index.html"))
    );
    return;
  }

  event.respondWith(
    caches.match(event.request).then(cached => cached || fetch(event.request).then(response => {
      const copy = response.clone();
      caches.open(CACHE).then(cache => cache.put(event.request, copy));
      return response;
    }))
  );
});
