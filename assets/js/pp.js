/* Palestine+ — behaviour. Every plus is a button; every button lays one more line. */
(() => {
  const d = document, root = d.documentElement;
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ------------------------------------------------ loader «Laying the line», first page of the session.
     <head> has already decided (js-load) before the first paint; this only runs it. */
  const ldr = d.querySelector('.ldr');
  if (ldr && root.classList.contains('js-load')) {
    requestAnimationFrame(() => ldr.classList.add('go'));
    setTimeout(() => ldr.classList.add('open'), 1760);
    setTimeout(() => { ldr.remove(); root.classList.remove('js-load'); }, 2700);
    try { sessionStorage.setItem('pp-laid', '1'); } catch (e) {}
  } else if (ldr) ldr.remove();

  /* ------------------------------------------------ page to page: close on a line, open along it */
  const nav = d.querySelector('.nav-ldr');
  const settle = () => { root.classList.remove('pp-arrive', 'pp-open'); };
  if (root.classList.contains('pp-arrive')) {
    /* two frames so the closed state is painted before it opens */
    requestAnimationFrame(() => requestAnimationFrame(() => root.classList.add('pp-open')));
    setTimeout(settle, 750);
  }
  const page = (u) => /(\.html|\/)$/.test(u.pathname);
  d.addEventListener('click', (e) => {
    const a = e.target.closest('a[href]');
    if (!a || !nav || still || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    if ((a.target && a.target !== '_self') || a.hasAttribute('download')) return;
    const u = new URL(a.href, location.href);
    if (u.origin !== location.origin || !page(u)) return;
    if (u.pathname === location.pathname && u.search === location.search) return;   /* same page, maybe a #hash */
    e.preventDefault();
    try { sessionStorage.setItem('pp-nav', '1'); } catch (er) {}
    nav.classList.add('leave');
    setTimeout(() => { location.href = u.href; }, 340);
    setTimeout(() => nav.classList.add('wait'), 900);
  });
  /* back/forward from the page cache: never come back to a closed page */
  addEventListener('pageshow', (e) => {
    if (!e.persisted) return;
    nav && nav.classList.remove('leave', 'wait');
    settle();
    try { sessionStorage.removeItem('pp-nav'); } catch (er) {}
  });

  /* ------------------------------------------------ masthead shrinks once the page moves */
  const mast = d.querySelector('.mast');
  if (mast) {
    const s = d.createElement('div');
    s.style.cssText = 'position:absolute;top:0;height:1px;width:1px';
    mast.before(s);
    new IntersectionObserver(([e]) => mast.classList.toggle('stuck', !e.isIntersecting)).observe(s);
  }

  /* ------------------------------------------------ every [data-lay] button opens one more layer */
  const toggle = (b, open) => {
    const v = open ?? b.getAttribute('aria-expanded') !== 'true';
    b.setAttribute('aria-expanded', String(v));
    const p = d.getElementById(b.getAttribute('aria-controls'));
    if (p) p.inert = !v;
  };
  d.querySelectorAll('[data-lay]').forEach((b) => {
    const p = d.getElementById(b.getAttribute('aria-controls'));
    if (p && b.getAttribute('aria-expanded') !== 'true') p.inert = true;
    b.addEventListener('click', () => toggle(b));
  });
  d.querySelectorAll('[data-all]').forEach((b) => {
    const box = b.closest('[data-stack]');
    b.addEventListener('click', () => {
      const bs = [...box.querySelectorAll('[data-lay]')];
      const open = bs.some((x) => x.getAttribute('aria-expanded') !== 'true');
      /* lay them one after another, top to bottom, the way the eye goes down */
      bs.forEach((x, i) => setTimeout(() => toggle(x, open), still ? 0 : i * 110));
      b.textContent = open ? 'Fold the layers' : 'Open every layer';
    });
  });

  /* ------------------------------------------------ lines laid in on scroll */
  const rv = d.querySelectorAll('.rv');
  if (!still && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver((es) => es.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    }), { rootMargin: '0px 0px -8% 0px' });
    rv.forEach((el) => io.observe(el));
  } else rv.forEach((el) => el.classList.add('in'));

  /* ------------------------------------------------ +Numbers: figures count up, ticks fill */
  const counters = d.querySelectorAll('[data-count]');
  const fmt = new Intl.NumberFormat('en-GB');
  const run = (el) => {
    const to = parseFloat(el.dataset.count), dec = (el.dataset.count.split('.')[1] || '').length;
    if (still || !isFinite(to)) return;
    const t0 = performance.now(), dur = 1300;
    const step = (t) => {
      const k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 4);
      el.firstChild.nodeValue = dec ? (to * e).toFixed(dec) : fmt.format(Math.round(to * e));
      if (k < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  if (counters.length && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver((es) => es.forEach((e) => {
      if (!e.isIntersecting) return;
      run(e.target);
      const tick = e.target.closest('li')?.querySelector('.tick i');
      if (tick) tick.style.setProperty('--k', tick.dataset.k || 1);
      io.unobserve(e.target);
    }), { threshold: .6 });
    counters.forEach((el) => io.observe(el));
  }
  d.querySelectorAll('.tick i').forEach((t) => { if (still) t.style.setProperty('--k', t.dataset.k || 1); });

  /* ------------------------------------------------ story: the depth gauge follows the reader down */
  const gauge = d.querySelectorAll('.gauge a[href^="#"]');
  if (gauge.length) {
    const map = new Map([...gauge].map((a) => [d.getElementById(a.getAttribute('href').slice(1)), a]));
    const io = new IntersectionObserver((es) => {
      es.forEach((e) => {
        if (!e.isIntersecting) return;
        let past = true;
        gauge.forEach((a) => {
          const cur = map.get(e.target) === a;
          a.setAttribute('aria-current', String(cur));
          if (cur) past = false;
          a.classList.toggle('past', past && !cur);
        });
      });
    }, { rootMargin: '-35% 0px -55% 0px' });
    map.forEach((a, el) => el && io.observe(el));
  }

  /* ------------------------------------------------ copy link */
  d.querySelectorAll('[data-copy]').forEach((b) => b.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(location.href.split('#')[0]); b.textContent = 'Link copied'; }
    catch (e) { b.textContent = 'Copy failed'; }
    setTimeout(() => (b.textContent = 'Copy link'), 1800);
  }));

  /* ------------------------------------------------ prototype forms: they send nothing */
  d.querySelectorAll('form[data-proto]').forEach((f) => f.addEventListener('submit', (ev) => {
    ev.preventDefault();
    const m = f.querySelector('.msg');
    if (m) m.textContent = 'This is a design prototype: nothing was sent and no address was kept.';
  }));

  /* ------------------------------------------------ search over assets/data/search.json */
  const sf = d.querySelector('[data-search]');
  if (sf) {
    const q = sf.querySelector('input'), out = d.querySelector('.results'), chips = d.querySelectorAll('.chips button');
    let all = [], desk = '';
    const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    const hi = (s, w) => w ? esc(s).replace(new RegExp('(' + w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig'), '<mark>$1</mark>') : esc(s);
    const draw = () => {
      const w = q.value.trim().toLowerCase();
      const hits = all.filter((s) => (!desk || s.desk === desk) && (!w || (s.h + ' ' + s.f + ' ' + s.p).toLowerCase().includes(w)));
      out.innerHTML = `<p class="count" role="status">${hits.length} ${hits.length === 1 ? 'story' : 'stories'}${w ? ` for “${esc(q.value.trim())}”` : ''}</p>` +
        (hits.length ? '' : `<p class="empty">No line matches${w ? ` “${esc(q.value.trim())}”` : ''}${desk ? ' on this desk' : ''}. Try a place, such as Jenin, Silwan or Khan Younis${desk ? ', or clear the desk filter' : ''}.</p>`) +
        hits.map((s) => `<article class="row"><div class="meta"><span>${esc(s.dl)}</span><span>${esc(s.d)}</span></div><div><h2 class="h-s"><a href="${s.u}"><span class="hl">${hi(s.h, w)}</span></a></h2><p class="dek">${hi(s.f, w)}</p></div><div class="meta"><span><span class="badge"><span class="pl" aria-hidden="true"><i class="pl-h"></i><i class="pl-v"></i></span>${s.n}</span> ${s.n === 1 ? 'layer' : 'layers'}</span><span>${esc(s.p)}</span></div></article>`).join('');
      const u = new URL(location); w ? u.searchParams.set('q', q.value.trim()) : u.searchParams.delete('q'); history.replaceState(null, '', u);
    };
    fetch(sf.dataset.search).then((r) => r.json()).then((j) => {
      all = j; q.value = new URLSearchParams(location.search).get('q') || ''; draw();
    });
    q.addEventListener('input', draw);
    sf.addEventListener('submit', (e) => { e.preventDefault(); draw(); });
    chips.forEach((c) => c.addEventListener('click', () => {
      desk = c.getAttribute('aria-pressed') === 'true' ? '' : c.dataset.desk;
      chips.forEach((x) => x.setAttribute('aria-pressed', String(x === c && !!desk)));
      draw();
    }));
  }
})();
