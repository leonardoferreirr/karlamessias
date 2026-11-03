/* Karla Messias: comportamento do site. Sem dependências. */
(() => {
  const d = document, h = d.documentElement, w = window;
  const rm = w.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const toque = w.matchMedia('(hover: none)').matches;

  /* ---------- menu ---------- */
  const burger = d.querySelector('.burger');
  if (burger) burger.addEventListener('click', () => {
    const abre = !h.classList.contains('menu-open');
    h.classList.toggle('menu-open', abre);
    burger.setAttribute('aria-expanded', abre);
    burger.setAttribute('aria-label', abre ? 'Fechar menu' : 'Abrir menu');
  });
  d.querySelectorAll('.nav a').forEach(a => a.addEventListener('click', () => h.classList.remove('menu-open')));
  const topo = d.querySelector('.top');

  /* ---------- revelações (com reserva: nada fica invisível) ---------- */
  const alvos = [...d.querySelectorAll('.rv, .arco, .faixa, .frase')];
  const mostrar = el => el.classList.add('in');
  if ('IntersectionObserver' in w) {
    const io = new IntersectionObserver(es => es.forEach(en => {
      const corre = en.target.matches('.faixa, .frase');
      if (en.isIntersecting) { mostrar(en.target); if (!corre) io.unobserve(en.target); }
      else if (corre) en.target.classList.remove('in');
    }), { rootMargin: '0px 0px -6% 0px' });
    alvos.forEach(el => io.observe(el));
  } else alvos.forEach(mostrar);
  setTimeout(() => alvos.forEach(el => { if (el.getBoundingClientRect().top < innerHeight) mostrar(el); }), 2500);

  /* ---------- catálogo estilo Netflix ---------- */
  d.querySelectorAll('[data-fila]').forEach(fila => {
    const trilho = fila.querySelector('.fila__trilho');
    const ant = fila.querySelector('[data-ant]'), prox = fila.querySelector('[data-prox]');
    const passo = () => Math.max(trilho.clientWidth * 0.8, 260);
    const estado = () => {
      if (!ant) return;
      ant.disabled = trilho.scrollLeft < 8;
      prox.disabled = trilho.scrollLeft + trilho.clientWidth > trilho.scrollWidth - 8;
    };
    ant && ant.addEventListener('click', () => trilho.scrollBy({ left: -passo(), behavior: rm ? 'auto' : 'smooth' }));
    prox && prox.addEventListener('click', () => trilho.scrollBy({ left: passo(), behavior: rm ? 'auto' : 'smooth' }));
    trilho.addEventListener('scroll', () => requestAnimationFrame(estado), { passive: true });
    w.addEventListener('resize', estado, { passive: true });
    estado();
    /* arrastar com o mouse, como no catálogo da TV */
    let x0 = 0, s0 = 0, arrasta = false, moveu = false;
    trilho.addEventListener('pointerdown', ev => {
      if (ev.pointerType !== 'mouse') return;
      arrasta = true; moveu = false; x0 = ev.clientX; s0 = trilho.scrollLeft;
      trilho.style.scrollSnapType = 'none';
    });
    w.addEventListener('pointermove', ev => {
      if (!arrasta) return;
      const dx = ev.clientX - x0;
      if (Math.abs(dx) > 5) moveu = true;
      trilho.scrollLeft = s0 - dx;
    }, { passive: true });
    w.addEventListener('pointerup', () => {
      if (!arrasta) return;
      arrasta = false; trilho.style.scrollSnapType = '';
    });
    trilho.addEventListener('click', ev => { if (moveu) { ev.preventDefault(); ev.stopPropagation(); moveu = false; } }, true);
  });

  /* ---------- lista de atuação: foto que acompanha o mouse ---------- */
  d.querySelectorAll('[data-lista]').forEach(lista => {
    const olho = lista.parentElement.querySelector('.lista__olho');
    if (!olho || toque || rm) return;
    const img = olho.querySelector('img');
    let x = 0, y = 0, cx = 0, cy = 0, anda = false;
    const passo = () => {
      cx += (x - cx) * 0.18; cy += (y - cy) * 0.18;
      olho.style.transform = `translate3d(${cx}px,${cy}px,0) translate(-50%,-50%) scale(${olho.classList.contains('on') ? 1 : .9})`;
      if (Math.abs(x - cx) > .5 || Math.abs(y - cy) > .5) requestAnimationFrame(passo); else anda = false;
    };
    lista.querySelectorAll('.lista__item').forEach(it => {
      it.addEventListener('mouseenter', () => { img.src = it.dataset.foto; olho.classList.add('on'); });
      it.addEventListener('mouseleave', () => olho.classList.remove('on'));
    });
    lista.addEventListener('mousemove', ev => {
      x = ev.clientX + 140; y = ev.clientY;
      if (!anda) { anda = true; requestAnimationFrame(passo); }
    });
  });

  /* ---------- fotos de fundo: rolam mais devagar que a página (paralaxe leve) ---------- */
  const fundos = [...d.querySelectorAll('[data-paralaxe] img')];
  if (fundos.length && !rm && w.matchMedia('(min-width:901px)').matches) {
    let pp = false;
    const mover = () => {
      pp = false;
      fundos.forEach(img => {
        const r = img.parentElement.parentElement.getBoundingClientRect();
        if (r.bottom < 0 || r.top > innerHeight) return;
        img.style.transform = `scale(1.08) translate3d(0,${(r.top * -0.12).toFixed(1)}px,0)`;
      });
    };
    w.addEventListener('scroll', () => { if (!pp) { pp = true; requestAnimationFrame(mover); } }, { passive: true });
    mover();
  }

  /* ---------- foto do topo: leve profundidade com o mouse ---------- */
  const arco = d.querySelector('.arco__foto img');
  if (arco && !toque && !rm) {
    let pend = false, mx = 0, my = 0;
    w.addEventListener('pointermove', ev => {
      mx = ev.clientX / innerWidth - .5; my = ev.clientY / innerHeight - .5;
      if (pend) return; pend = true;
      requestAnimationFrame(() => { pend = false; arco.style.transform = `scale(1.06) translate3d(${(-mx * 10).toFixed(1)}px,${(-my * 10).toFixed(1)}px,0)`; });
    }, { passive: true });
  }

  /* ---------- sombra do cabeçalho ---------- */
  let pend = false;
  w.addEventListener('scroll', () => {
    if (pend) return; pend = true;
    requestAnimationFrame(() => { pend = false; topo && topo.classList.toggle('solid', w.scrollY > 10); });
  }, { passive: true });

  /* ---------- assunto vindo do link (ex.: /contato?assunto=parcerias) ---------- */
  const mapa = { parcerias: 'Convites e parcerias', ancora: 'Instituto Âncora', 'instituto-ancora': 'Instituto Âncora',
    sisadica: 'SISADICA', 'casa-da-alianca': 'Casa da Aliança' };
  const assunto = new URLSearchParams(location.search).get('assunto');
  const sel = d.querySelector('#co-ass');
  if (sel && assunto && mapa[assunto]) sel.value = mapa[assunto];

  /* ---------- formulários: mensagem pronta para o WhatsApp ---------- */
  const t0 = Date.now();
  d.querySelectorAll('form[data-form]').forEach(form => form.addEventListener('submit', ev => {
    ev.preventDefault();
    if (!form.reportValidity()) return;
    const f = new FormData(form);
    if ((f.get('site') || '').toString().trim() || Date.now() - t0 < 2500) return; // robô
    const titulo = form.dataset.form === 'contratacao'
      ? 'Olá! Quero solicitar uma palestra, treinamento ou conferência com Karla Messias.'
      : 'Olá! Vim pelo site da Karla Messias.';
    const linhas = [titulo, ''];
    for (const [k, v] of f.entries()) {
      if (k === 'site' || k === 'aceite') continue;
      const val = v.toString().trim();
      if (!val) continue;
      linhas.push(`${k}: ${k === 'Data prevista' ? val.split('-').reverse().join('/') : val}`);
    }
    try { sessionStorage.setItem('km_msg', linhas.join('\n')); } catch (_) {}
    location.href = `/obrigado?c=${form.dataset.form}`;
  }));
})();
