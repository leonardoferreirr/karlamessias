#!/usr/bin/env python3
"""Monta o site da Karla Messias: institucional (home de 12 seções + páginas internas),
landing em /landingpage e a ponte /obrigado para o WhatsApp.

    python3 build.py

A copy mora em _src/conteudo.py, transcrita do briefing dela. O CSS (assets/css/site.css)
vai minificado para dentro do <head>; o site.js leva o hash do conteúdo no nome.
Cada página sai como <rota>.html na raiz (a Vercel serve /sobre-karla com cleanUrls).
"""
import hashlib, json, re, sys
from datetime import date
from html import escape as e
from pathlib import Path

RAIZ = Path(__file__).parent
sys.path.insert(0, str(RAIZ / "_src"))
import conteudo as C  # noqa: E402

DOMINIO = "https://www.karlamessias.com"
INDEXAR = False            # True depois da aprovação dela
WHATSAPP = "5561993973723"  # +55 61 99397-3723, o mesmo dos slides da Plancenter
INSTAGRAM = "https://www.instagram.com/princesakarlamessias/"
IG_USER = "@princesakarlamessias"

# fotos (assets/img/fotos/foto-NN-1400.webp e -800.webp)
FOTO_HERO = "foto-19"
LOGOS_COM_FUNDO = {"rede-aguias-intercessao"}  # recortar mutilava a arte: vai com o fundo creme original
# cor de cada card, puxada da própria marca (c1 = centro, c2 = borda, tx = texto). Claros levam texto escuro.
CORES = {
    "instituto-ancora": ("#EEF8F1", "#BFE2CB", "#16392A"),        # verde claro (o azul e o verde da logo aparecem)
    "plancenter": ("#2457B0", "#0A1D45", "#F3EDE2"),              # azul
    "sisadica": ("#CFA552", "#4E350E", "#FFF7E6"),                # ouro
    "adica-brasao": ("#F1C24A", "#8E5E0B", "#FFF8E8"),            # amarelo
    "commadica": ("#93203A", "#2C0610", "#F6F0E6"),               # bordô
    "conselho-reconstruide": ("#3B3936", "#060606", "#F1E9DA"),   # preto
    "princesas-virtuosas": ("#FCE6F2", "#E3B5D8", "#4A1846"),     # rosa e lilás
    "the-dive": ("#1E93BC", "#052B44", "#EAF7FB"),                # azul do mar
    "visao-de-aguia": ("#22407A", "#060E22", "#F2EBDD"),          # azul-marinho
    "rede-aguias-intercessao": ("#F7EDD9", "#D8BF92", "#3B2412"), # creme e dourado (a arte vai com o fundo)
    "deus-sara-as-nacoes": ("#6E2E96", "#1E0A33", "#F6EEFF"),     # roxo
    "sacerdocio-real": ("#BC2232", "#3D060F", "#FFF1EC"),         # vermelho
    "devocional-palavra-do-rei": ("#3A2A12", "#0B0805", "#F5E7C6"),
}
CLAROS = {"instituto-ancora", "princesas-virtuosas", "rede-aguias-intercessao"}

# eventos e artigos: quando existirem, entram aqui e as áreas se montam sozinhas
EVENTOS = []   # {"dia":"14","mes":"DEZ","titulo":"","local":"","texto":"","link":""}
POSTS = []     # {"cat":"","titulo":"","resumo":"","foto":"foto-26","link":""}

CSS = RAIZ / "assets/css/site.css"
JS = RAIZ / "assets/js/site.js"

# ------------------------------------------------------------------ ícones
SETA = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5"/></svg>'
ZAP = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.4.8 3.2.6a2.8 2.8 0 0 0 1.8-1.3 2.3 2.3 0 0 0 .2-1.3c-.1-.1-.3-.2-.6-.3z"/></svg>')
INSTA = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8" fill="currentColor"/></svg>')
ORN = ('<svg class="orn" viewBox="0 0 72 12" fill="none" aria-hidden="true"><path d="M0 6h28M44 6h28" stroke="currentColor"/>'
       '<rect x="32" y="2" width="8" height="8" transform="rotate(45 36 6)" stroke="currentColor"/></svg>')
ESQ = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M10 3L5 8l5 5" stroke="currentColor" stroke-width="1.5"/></svg>'
DIR = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M6 3l5 5-5 5" stroke="currentColor" stroke-width="1.5"/></svg>'


def zap_link(msg):
    from urllib.parse import quote
    return f"https://wa.me/{WHATSAPP}?text={quote(msg)}"


# ------------------------------------------------------------------ peças
def foto(nome, alt, sizes="(max-width:900px) 92vw, 46vw", cls="", lazy=True, w=1400, h=2100):
    p = RAIZ / f"assets/img/fotos/{nome}-1400.webp"
    if p.exists():
        try:
            from PIL import Image
            with Image.open(p) as im:
                w, h = im.size
        except Exception:
            pass
    else:
        print(f"  ! foto faltando: {nome}-1400.webp")
    lz = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    return (f'<img src="/assets/img/fotos/{nome}-1400.webp" srcset="/assets/img/fotos/{nome}-800.webp 800w, '
            f'/assets/img/fotos/{nome}-1400.webp {w}w" sizes="{sizes}" alt="{e(alt)}" width="{w}" height="{h}"{lz} decoding="async"{cls}>')


def logo(nome, alt, lazy=True):
    p = RAIZ / f"assets/img/logos/{nome}.webp"
    w, h = 640, 640
    if p.exists():
        try:
            from PIL import Image
            with Image.open(p) as im:
                w, h = im.size
        except Exception:
            pass
    else:
        print(f"  ! logo faltando: {nome}.webp")
    p2 = RAIZ / f"assets/img/logos/{nome}@2x.webp"
    srcset = f' srcset="/assets/img/logos/{nome}.webp 1x, /assets/img/logos/{nome}@2x.webp 2x"' if p2.exists() else ""
    lz = ' loading="lazy"' if lazy else ""
    return f'<img src="/assets/img/logos/{nome}.webp"{srcset} alt="{e(alt)}" width="{w}" height="{h}"{lz} decoding="async">'


def btn(txt, href, tipo="pri", seta=True, extra=""):
    return f'<a class="btn btn--{tipo}" href="{href}"{extra}>{e(txt)}{" " + SETA if seta else ""}</a>'


def link(txt, href):
    return f'<a class="link" href="{href}">{e(txt)} {SETA}</a>'


def estilo_cor(logo_nome):
    c1, c2, tx = CORES.get(logo_nome, ("#4a1520", "#2E0B12", "#F6F0E6"))
    return f' style="--c1:{c1};--c2:{c2};--tx:{tx}"'


def card(logo_nome, nome, papel, texto, href, fora=False):
    fundo = " card__logo--fundo" if logo_nome in LOGOS_COM_FUNDO else ""
    claro = " card--claro" if logo_nome in CLAROS else ""
    alvo = ' target="_blank" rel="noopener"' if fora else ""
    return (f'<article class="card{claro}"{estilo_cor(logo_nome)}><div class="card__logo{fundo}">{logo(logo_nome, nome)}</div>'
            f'<div class="card__txt"><h3>{e(nome)}</h3><span class="card__papel">{e(papel.upper())}</span>'
            f'<div class="card__mais"><div><p>{e(texto)}</p><span class="card__ir">CONHECER {SETA}</span></div></div></div>'
            f'<a href="{href}"{alvo} aria-label="{e(nome)}"></a></article>')


def fila(titulo, cards, clara=False):
    cls = " fila--clara" if clara else ""
    return (f'<div class="fila{cls}" data-fila><div class="fila__topo"><h3 class="fila__titulo">{e(titulo)}</h3>'
            f'<div class="fila__setas"><button type="button" data-ant aria-label="Anteriores">{ESQ}</button>'
            f'<button type="button" data-prox aria-label="Próximos">{DIR}</button></div></div>'
            f'<div class="fila__trilho">{"".join(cards)}</div></div>')


def card_plancenter():
    P = C.PLANCENTER
    return card("plancenter", P["nome"], P["papel"], P["texto"], P["url"], fora=True)


def bloco_plancenter():
    P = C.PLANCENTER
    return (f'<div class="ancora ancora--plan rv"><div class="ancora__logo plan__logo">{logo("plancenter", "Plancenter, Consultoria & Projetos")}</div>'
            f'<div><h2>{e(P["frase"])}</h2><p>{e(P["texto"])}</p>'
            f'{btn("Conheça a Plancenter", P["url"], "pri", True, " target=_blank rel=noopener")}</div></div>')


def fundo_img(nome, alt="", lazy=True, pos="70% 22%", pos_m="50% 15%"):
    """<picture> de fundo: no desktop a versão larga (preenchimento generativo, -wide), no celular o retrato."""
    larga = RAIZ / f"assets/img/fotos/{nome}-wide-2400.webp"
    lz = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    if larga.exists():
        desk = (f'<source media="(min-width:901px)" srcset="/assets/img/fotos/{nome}-wide-1400.webp 1400w, '
                f'/assets/img/fotos/{nome}-wide-2400.webp 2400w" sizes="100vw">')
    else:
        print(f"  ! sem versão larga ainda: {nome}-wide (usando o retrato no desktop)")
        desk = ""
    return (f'<picture style="--pos:{pos};--pos-m:{pos_m}">{desk}<img src="/assets/img/fotos/{nome}-1400.webp" '
            f'srcset="/assets/img/fotos/{nome}-800.webp 800w, /assets/img/fotos/{nome}-1400.webp 1024w" sizes="100vw" '
            f'alt="{e(alt)}" width="1024" height="1536"{lz} decoding="async"></picture>')


def cards_instituicoes():
    """Instituições e empresas: Âncora e Plancenter viram card junto com as ministeriais."""
    a = next(i for i in C.INSTITUICOES if i["slug"] == "instituto-ancora")
    out = [card("instituto-ancora", "Instituto Âncora", "Presidência", a["texto"], "/instituto-ancora"), card_plancenter()]
    out += [card(l, rot, pap, nome, href) for l, rot, nome, pap, href in C.MINISTERIAL]
    return out


def cards_ministerial():
    return [card(l, rot, pap, nome, href) for l, rot, nome, pap, href in C.MINISTERIAL]


def cards_movimentos(base="/movimentos", sem_conselho=False):
    return [card(l, nome, pap, txt, f"{base}#{i}") for i, l, nome, pap, txt in C.MOVIMENTOS
            if not (sem_conselho and l == "conselho-reconstruide")]


def tags(itens, cols=4, escuro=False, extra=""):
    """Etiquetas em grade de largura igual: `cols` por linha, a última centralizada."""
    li = "".join(f"<li>{e(x.rstrip('.'))}</li>" for x in itens)
    return f'<ul class="tags{" tags--escuro" if escuro else ""}{extra}" style="--cols:{cols}">{li}</ul>'


# instituições na pilha da landing: cor da marca (Casa da Aliança no marsala da casa)
CORES_INST = {"adica-casa-da-alianca": ("#6A1A2C", "#240710", "#F6F0E6")}


def pilha_instituicoes():
    """Cards largos que sobem e empilham na rolagem."""
    out = []
    for n, i in enumerate(C.INSTITUICOES):
        c1, c2, tx = CORES_INST.get(i["logo"]) or CORES.get(i["logo"], ("#4a1520", "#2E0B12", "#F6F0E6"))
        claro = " pcard--claro" if i["logo"] in CLAROS else ""
        out.append(f'<article class="pcard{claro}" style="--c1:{c1};--c2:{c2};--tx:{tx};--i:{n}">'
                   f'<div class="pcard__marca">{logo(i["logo"], i["nome"])}</div>'
                   f'<div class="pcard__cab"><h3>{e(i["nome"])}</h3><p class="pcard__papel">{e(i["papel"])}</p></div>'
                   f'<div class="pcard__txt"><p>{e(i["texto"])}</p>{link("Conheça", "/" + i["slug"])}</div></article>')
    return f'<div class="pilha">{"".join(out)}</div>'


def lista_bloco(titulo, itens, texto="", escuro=False):
    li = "".join(f"<li>{e(x.rstrip('.'))}</li>" for x in itens)
    p = f"<p>{e(texto)}</p>" if texto else ""
    return f'<div class="bloco{" bloco--escuro" if escuro else ""} rv"><h3>{e(titulo)}</h3>{p}<ul>{li}</ul></div>'


def pag_topo(titulo, texto="", trilha=None, ctas=""):
    tr = ""
    if trilha:
        tr = '<nav class="trilha" aria-label="Você está em"><a href="/">Início</a><span>/</span>' + \
             "<span>/</span>".join(f'<a href="{h}">{e(t)}</a>' if h else f"<span>{e(t)}</span>" for t, h in trilha) + "</nav>"
    p = f"<p>{e(texto)}</p>" if texto else ""
    return f'<header class="pag-topo"><div class="wrap">{tr}<h1>{titulo}</h1>{p}{ctas}</div></header>'


def chamada(titulo, texto, botao, href):
    return (f'<section class="sec"><div class="wrap"><div class="chamada rv"><h2>{titulo}</h2><p>{e(texto)}</p>'
            f'<div class="ctas">{btn(botao, href, "ouro")}</div></div></div></section>')


def posts_bloco():
    """Os 3 mais recentes. Sem artigos ainda: as 3 linhas da biblioteca, com o texto dos pilares dela."""
    if POSTS:
        itens = POSTS[:3]
    else:
        itens = [
            {"titulo": "Fé e espiritualidade", "resumo": C.PILARES[0][1], "img": "biblia", "link": "/conteudos"},
            {"titulo": "Restauração emocional", "resumo": C.PILARES[1][1], "img": "devocional", "link": "/conteudos"},
            {"titulo": "Liderança e propósito", "resumo": C.PILARES[3][1], "img": "estudo", "link": "/conteudos"},
        ]
    out = []
    for i, p in enumerate(itens):
        nome = p.get("img", "biblia")
        arq = RAIZ / f"assets/img/conteudos/{nome}-1200.webp"
        if not arq.exists():
            print(f"  ! imagem de conteúdo faltando: {nome}-1200.webp")
        img = (f'<img src="/assets/img/conteudos/{nome}-1200.webp" srcset="/assets/img/conteudos/{nome}-700.webp 700w, '
               f'/assets/img/conteudos/{nome}-1200.webp 1200w" sizes="(max-width:900px) 92vw, 30vw" alt="" width="1200" height="825" loading="lazy" decoding="async">')
        out.append(f'<article class="post rv" data-d="{i}"><div class="foto">{img}</div>'
                   f'<div class="post__txt"><h3>{e(p["titulo"])}</h3><p>{e(p["resumo"])}</p>{link("Acessar", p["link"])}</div></article>')
    return '<div class="grade3">' + "".join(out) + "</div>"


def agenda_bloco(completa=False):
    if EVENTOS:
        out = []
        for ev in EVENTOS:
            out.append(f'<article class="evento rv"><div class="evento__data"><b>{e(ev["dia"])}</b><span>{e(ev["mes"])}</span></div>'
                       f'<div><h3>{e(ev["titulo"])}</h3><p>{e(ev["local"])}. {e(ev["texto"])}</p></div>'
                       f'{btn("Inscrição", ev["link"], "linha", False)}</article>')
        return "".join(out)
    tipos = "".join(f"<li>{e(t.rstrip('.'))}</li>" for t in C.EVENTO_TIPOS)
    return (f'<div class="vazio rv"><h3>Novas datas em breve.</h3>'
            f'<p>A agenda de congressos, seminários, conferências, palestras, cursos, encontros de mulheres e eventos missionários está sendo organizada. Deixe seu contato para receber as datas em primeira mão.</p>'
            f'{"<ul class=tipos>" + tipos + "</ul>" if completa else ""}'
            f'<div class="ctas">{btn("Quero receber a agenda", zap_link("Olá! Quero receber a agenda de eventos da Karla Messias."), "pri", True, " target=_blank rel=noopener")}</div></div>')


def form_contratacao():
    temas = "".join(f"<option>{e(t.rstrip('.'))}</option>" for t in C.TEMAS) + "<option>Outro tema</option>"
    tipos = "".join(f"<option>{t}</option>" for t in ["Palestra", "Treinamento", "Conferência", "Congresso", "Seminário", "Evento corporativo", "Evento em igreja", "Outro"])
    return f'''<form class="form rv" data-form="contratacao" novalidate>
  <div class="campo"><label for="ct-nome">Nome completo</label><input id="ct-nome" name="Nome" autocomplete="name" required></div>
  <div class="campo"><label for="ct-inst">Empresa ou instituição</label><input id="ct-inst" name="Empresa ou instituição" autocomplete="organization" required></div>
  <div class="campo"><label for="ct-mail">E-mail</label><input id="ct-mail" name="E-mail" type="email" autocomplete="email" required></div>
  <div class="campo"><label for="ct-tel">Telefone/WhatsApp</label><input id="ct-tel" name="Telefone/WhatsApp" type="tel" inputmode="tel" autocomplete="tel" required></div>
  <div class="campo"><label for="ct-cid">Cidade e estado</label><input id="ct-cid" name="Cidade e estado" autocomplete="address-level2" required></div>
  <div class="campo"><label for="ct-tipo">Tipo de evento</label><select id="ct-tipo" name="Tipo de evento" required><option value="" disabled selected>Escolha</option>{tipos}</select></div>
  <div class="campo"><label for="ct-tema">Tema de interesse</label><select id="ct-tema" name="Tema de interesse" required><option value="" disabled selected>Escolha</option>{temas}</select></div>
  <div class="campo"><label for="ct-data">Data prevista</label><input id="ct-data" name="Data prevista" type="date"></div>
  <div class="campo campo--cheio"><label for="ct-msg">Mensagem</label><textarea id="ct-msg" name="Mensagem" rows="3"></textarea></div>
  <div class="form__mel" aria-hidden="true"><label>Não preencha<input name="site" tabindex="-1" autocomplete="off"></label></div>
  <label class="aceite"><input type="checkbox" name="aceite" required> Concordo com o tratamento dos meus dados para responder a esta solicitação, conforme a LGPD e a <a href="/privacidade">Política de Privacidade</a>.</label>
  <button class="btn btn--pri" type="submit">ENVIAR SOLICITAÇÃO</button>
</form>'''


def form_contato(assunto=""):
    ops = ["Convites e parcerias", "Palestras e conferências", "Mentorias e cursos", "Instituto Âncora", "SISADICA",
           "Casa da Aliança", "Ministérios e movimentos", "Imprensa", "Outro"]
    opts = "".join(f'<option{" selected" if o == assunto else ""}>{o}</option>' for o in ops)
    sel0 = "" if assunto else " selected"
    return f'''<form class="form rv" data-form="contato" novalidate>
  <div class="campo"><label for="co-nome">Nome</label><input id="co-nome" name="Nome" autocomplete="name" required></div>
  <div class="campo"><label for="co-mail">E-mail</label><input id="co-mail" name="E-mail" type="email" autocomplete="email" required></div>
  <div class="campo"><label for="co-tel">Telefone</label><input id="co-tel" name="Telefone" type="tel" inputmode="tel" autocomplete="tel" required></div>
  <div class="campo"><label for="co-ass">Assunto</label><select id="co-ass" name="Assunto" required><option value="" disabled{sel0}>Escolha</option>{opts}</select></div>
  <div class="campo campo--cheio"><label for="co-msg">Mensagem</label><textarea id="co-msg" name="Mensagem" rows="4" required></textarea></div>
  <div class="form__mel" aria-hidden="true"><label>Não preencha<input name="site" tabindex="-1" autocomplete="off"></label></div>
  <label class="aceite"><input type="checkbox" name="aceite" required> Concordo com o tratamento dos meus dados para responder a este contato, conforme a LGPD e a <a href="/privacidade">Política de Privacidade</a>.</label>
  <button class="btn btn--pri" type="submit">ENVIAR MENSAGEM</button>
</form>'''


def contatos_diretos():
    return (f'<div class="contatos"><a href="{zap_link("Olá! Vim pelo site da Karla Messias.")}" target="_blank" rel="noopener">{ZAP} WhatsApp</a>'
            f'<a href="{INSTAGRAM}" target="_blank" rel="noopener">{INSTA} Instagram {IG_USER}</a></div>')


# ------------------------------------------------------------------ casca
MENU = [
    ("Início", "/", []),
    ("Sobre Karla", "/sobre-karla", []),
    ("Atuação Profissional", "/atuacao-profissional", []),
    ("Palestras e Mentorias", "/palestras", [("Palestras e conferências", "/palestras"), ("Contratar uma palestra", "/palestras/contratacao"), ("Mentorias", "/mentorias")]),
    ("Instituições", "/instituicoes", [("Instituto Âncora", "/instituto-ancora"), ("SISADICA", "/sisadica"), ("Casa da Aliança", "/casa-da-alianca")]),
    ("Ministérios e Movimentos", "/movimentos", []),
    ("Cursos e Conteúdos", "/conteudos", [("Cursos e formações", "/mentorias#formacoes"), ("Conteúdos", "/conteudos"), ("Agenda", "/agenda")]),
    ("Contato", "/contato", []),
]


def cabecalho(rota):
    itens = []
    for nome, href, sub in MENU:
        atual = ' aria-current="page"' if href == rota or any(h == rota for _, h in sub) else ""
        if sub:
            s = "".join(f'<a href="{h}">{e(t)}</a>' for t, h in sub)
            itens.append(f'<div class="nav__grupo"><a href="{href}"{atual}>{e(nome)}</a><div class="nav__sub">{s}</div></div>')
        else:
            itens.append(f'<a href="{href}"{atual}>{e(nome)}</a>')
    itens.append('<a class="btn btn--pri nav__cta" href="/contato?assunto=parcerias">CONVITES E PARCERIAS</a>')
    return f'''<header class="top"><div class="wrap top__in">
  <a class="marca" href="/" aria-label="Karla Messias, página inicial"><img src="/assets/img/logos/km-monograma.webp" alt="" width="104" height="104"><span>KARLA MESSIAS</span></a>
  <a class="btn btn--pri top__cta" href="/contato?assunto=parcerias">CONVITES E PARCERIAS</a>
  <button class="burger" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="nav"><span></span><span></span></button>
</div><nav class="nav" id="nav" aria-label="Principal"><div class="wrap nav__in">{"".join(itens)}</div></nav></header>'''


def rodape():
    links = [("Sobre Karla", "/sobre-karla"), ("Atuação profissional", "/atuacao-profissional"), ("Palestras e mentorias", "/palestras"),
             ("Instituto Âncora", "/instituto-ancora"), ("SISADICA", "/sisadica"), ("Casa da Aliança", "/casa-da-alianca"),
             ("Privacidade", "/privacidade"), ("Contato", "/contato")]
    metade = len(links) // 2
    col = lambda ls: "".join(f'<li><a href="{h}">{e(t)}</a></li>' for t, h in ls)
    frase = "".join(f'<span{" class=o" if i % 2 else ""}>{e(t)}</span>' for i, t in enumerate(C.TRIADE * 2))
    return f'''<div class="frase" aria-hidden="true"><div class="frase__t">{frase}{frase}</div></div>
<footer class="rod"><div class="wrap">
  <div class="rod__grid">
    <div><p class="rod__marca">KARLA MESSIAS</p><p class="rod__lema">{e(C.LEMA)}</p><p class="rod__titulos">{e(C.TITULOS_TXT)}</p></div>
    <div><p class="rod__h">LINKS</p><ul>{col(links[:metade])}</ul></div>
    <div><p class="rod__h">&nbsp;</p><ul>{col(links[metade:])}<li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram: {IG_USER}</a></li></ul></div>
  </div>
  <div class="rod__fim"><span>© Karla Messias. Todos os direitos reservados.</span><span>{e(C.LEMA)}</span></div>
</div></footer>
<a class="zap" href="{zap_link("Olá! Vim pelo site da Karla Messias.")}" target="_blank" rel="noopener" aria-label="Falar pelo WhatsApp">{ZAP}</a>'''


NOMES_ROTA = {"/sobre-karla": "Sobre Karla", "/atuacao-profissional": "Atuação profissional", "/palestras": "Palestras",
              "/palestras/contratacao": "Contratar palestra", "/mentorias": "Mentorias", "/instituicoes": "Instituições",
              "/instituto-ancora": "Instituto Âncora", "/sisadica": "SISADICA", "/casa-da-alianca": "Casa da Aliança",
              "/movimentos": "Ministérios e movimentos", "/conteudos": "Conteúdos", "/agenda": "Agenda", "/contato": "Contato",
              "/privacidade": "Privacidade", "/landingpage": "Karla Messias"}


def schema_pagina(rota):
    """BreadcrumbList nas internas; Organization nas páginas de instituição."""
    out = []
    if rota not in ("/", "/obrigado") and rota in NOMES_ROTA:
        itens = [{"@type": "ListItem", "position": 1, "name": "Início", "item": DOMINIO + "/"}]
        if rota == "/palestras/contratacao":
            itens.append({"@type": "ListItem", "position": 2, "name": "Palestras", "item": DOMINIO + "/palestras"})
        itens.append({"@type": "ListItem", "position": len(itens) + 1, "name": NOMES_ROTA[rota], "item": DOMINIO + rota})
        out.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": itens})
    for i in C.INSTITUICOES:
        if rota == "/" + i["slug"]:
            out.append({"@context": "https://schema.org", "@type": "Organization", "name": i["nome"], "description": i["texto"],
                        "url": DOMINIO + rota, "logo": DOMINIO + f'/assets/img/logos/{i["logo"]}.webp',
                        "member": {"@type": "Person", "name": C.NOME, "roleName": i["papel"].split(":")[0]}})
    if rota == "/":
        out.append({"@context": "https://schema.org", "@type": "WebSite", "name": "Karla Messias", "url": DOMINIO + "/", "inLanguage": "pt-BR"})
    return "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False, separators=(",", ":"))}</script>' for o in out)


def schema():
    pessoa = {
        "@context": "https://schema.org", "@type": "Person", "name": C.NOME, "alternateName": C.NOME_COMPLETO,
        "jobTitle": C.TITULOS, "description": C.POSICIONAMENTO, "url": DOMINIO + "/",
        "image": DOMINIO + f"/assets/img/fotos/{FOTO_HERO}-1400.webp", "sameAs": [INSTAGRAM],
        "affiliation": [{"@type": "Organization", "name": "Instituto Âncora"},
                        {"@type": "Organization", "name": "SISADICA, Sistema ADICA de Ensino Teológico e de Missões"},
                        {"@type": "Organization", "name": "Assembleia de Deus Internacional Casa da Aliança"}],
    }
    return f'<script type="application/ld+json">{json.dumps(pessoa, ensure_ascii=False, separators=(",", ":"))}</script>'


def minificar(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s*\n\s*", "\n", css)
    css = re.sub(r"\s*([{}:;,>])\s*", r"\1", css)
    css = re.sub(r";}", "}", css)
    return re.sub(r"\n+", "", css).replace("../fonts/", "/assets/fonts/").strip()


def hash_de(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()[:10] if p.exists() else "0"


CSS_MIN = ""


def pagina(rota, titulo, desc, corpo, preload="", landing=False, robots=None):
    robots = robots or ("index,follow" if INDEXAR else "noindex,nofollow")
    url = DOMINIO + (rota if rota != "/" else "/")
    topo = landing_topo() if landing else cabecalho(rota)
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#7B1E2D">
<meta property="og:type" content="website"><meta property="og:locale" content="pt_BR"><meta property="og:site_name" content="Karla Messias">
<meta property="og:title" content="{e(titulo)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMINIO}/assets/img/og-image.jpg"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/favicon-v2.png" type="image/png"><link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/poppins-500.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/poppins-300.woff2" as="font" type="font/woff2" crossorigin>
{preload}
<script>document.documentElement.classList.add('js')</script>
<style>{CSS_MIN}</style>
{schema() if rota in ("/", "/sobre-karla", "/landingpage") else ""}{schema_pagina(rota)}
</head>
<body>
{topo}
<main>
{corpo}
</main>
{rodape()}
<script src="/assets/js/site.js?v={hash_de(JS)}" defer></script>
</body>
</html>'''


def landing_topo():
    return f'''<header class="top"><div class="wrap top__in">
  <a class="marca" href="/" aria-label="Karla Messias, site institucional"><img src="/assets/img/logos/km-monograma.webp" alt="" width="104" height="104"><span>KARLA MESSIAS</span></a>
  <a class="btn btn--pri" href="#contato" style="min-height:2.7rem;padding:.5rem 1.2rem;font-size:.8rem">Fale com a equipe</a>
</div></header>'''


def preload_foto(nome):
    """Pré-carrega a foto do topo: a larga no desktop (se já existir) e o retrato no celular."""
    larga = (RAIZ / f"assets/img/fotos/{nome}-wide-2400.webp").exists()
    desk = (f'<link rel="preload" as="image" media="(min-width:901px)" imagesrcset="/assets/img/fotos/{nome}-wide-1400.webp 1400w, '
            f'/assets/img/fotos/{nome}-wide-2400.webp 2400w" imagesizes="100vw" fetchpriority="high">') if larga else \
           f'<link rel="preload" as="image" href="/assets/img/fotos/{nome}-1400.webp" media="(min-width:901px)" fetchpriority="high">'
    return (f'<link rel="preload" as="image" media="(max-width:900px)" imagesrcset="/assets/img/fotos/{nome}-800.webp 800w, '
            f'/assets/img/fotos/{nome}-1400.webp 1024w" imagesizes="100vw" fetchpriority="high">\n' + desk)


# ------------------------------------------------------------------ páginas
def home():
    faixa_itens = "".join(f"<span>{e(t)}</span><i></i>" for t in C.TITULOS)
    pilares = "".join(f'<div class="pilar rv" data-d="{i}"><span class="pilar__n">0{i+1}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>'
                      for i, (t, d) in enumerate(C.PILARES))
    atuacao = "".join(f'<div class="lista__item rv" data-foto="/assets/img/fotos/{f}-800.webp"><span class="lista__n">{i+1:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>'
                      for i, (t, d, f) in enumerate(C.ATUACAO_HOME))
    temas = "".join(f'<li class="rv" data-d="{i % 3}"><span>{i+1:02d}</span>{e(t.rstrip("."))}</li>' for i, t in enumerate(C.TEMAS_HOME))
    corpo = f'''
<section class="capa" id="inicio">
  <div class="capa__bg" data-paralaxe>{fundo_img(FOTO_HERO, "Karla Messias de blazer marsala e vestido creme", lazy=False, pos="75% 50%", pos_m="50% 12%")}</div>
  <div class="wrap"><div class="capa__txt">
    <h1>Fé, conhecimento e liderança <em>para transformar vidas.</em></h1>
    <p>Karla Messias une experiência em gestão, educação, desenvolvimento humano e liderança ministerial em uma trajetória dedicada à transformação de pessoas e instituições.</p>
    <div class="ctas">{btn("Conheça minha história", "/sobre-karla", "ouro")}{btn("Solicite uma palestra", "/palestras/contratacao", "claro", False)}</div>
  </div></div>
</section>
<div class="faixa" aria-hidden="true"><div class="faixa__t">{faixa_itens * 4}</div></div>

<section class="capa capa--clara" id="quem-e">
  <div class="capa__bg" data-paralaxe>{fundo_img("foto-21", "Karla Messias em seu escritório, com livros de liderança e gestão", pos="20% 50%", pos_m="40% 15%")}</div>
  <div class="wrap"><div class="capa__txt rv">
    <h2>Muito além dos títulos. Uma trajetória de propósito.</h2>
    <p>Karla Patrícia Messias Pereira é Administradora, Teóloga, Psicanalista Clínica, Mentora, Palestrante e Apóstola. Sua atuação reúne conhecimento, liderança e compromisso com o desenvolvimento humano, a educação e a transformação espiritual.</p>
    <figure class="citacao"><blockquote>{e(C.POSICIONAMENTO)}</blockquote></figure>
    <div class="ctas" style="margin-top:2rem">{link("Conheça minha biografia", "/sobre-karla")}</div>
  </div></div>
</section>

<section class="sec sec--escuro" id="pilares"><div class="wrap">
  <div class="cab rv"><h2>Os quatro pilares da marca Karla Messias</h2></div>
  <div class="pilares">{pilares}</div>
</div></section>

<section class="sec" id="atuacao"><div class="wrap">
  <div class="cab rv"><h2>Conhecimento aplicado à transformação.</h2></div>
  <div class="lista" data-lista>{atuacao}</div>
  <div class="fim">{link("Conheça todas as áreas de atuação", "/atuacao-profissional")}</div>
</div></section>

<section class="sec sec--branco compacto" id="palestras"><div class="wrap">
  <div class="cab rv"><h2>Ideias que despertam. Conhecimento que transforma.</h2><p>Temas para empresas, instituições de ensino, igrejas, congressos e organizações.</p></div>
  <ol class="temas-grade">{temas}</ol>
  <div class="fim">{btn("Contrate uma palestra", "/palestras/contratacao")}</div>
</div></section>

<section class="fixa" id="mentorias">
  <div class="fixa__bg">{fundo_img("foto-16", "", pos="82% 50%", pos_m="50% 14%")}</div>
  <div class="wrap"><div class="fixa__txt rv">
    <h2>Desenvolvimento começa com conhecimento e direção.</h2>
    <p>Apresentação dos programas de mentoria, cursos, seminários e treinamentos, com acesso às respectivas páginas de inscrição.</p>
    <div class="ctas">{btn("Conheça os programas", "/mentorias", "ouro")}</div>
  </div></div>
</section>

<section class="sec catalogo" id="instituicoes"><div class="wrap">
  <div class="cab rv"><h2>Formar líderes. Fortalecer a Igreja. Preparar para as nações.</h2></div>
  {fila("Instituições e empresas", cards_instituicoes())}
  {fila("Ministérios, movimentos e iniciativas", cards_movimentos(sem_conselho=True))}
  <div class="fim ctas" style="justify-content:center">{btn("Conheça a atuação ministerial", "/instituicoes", "ouro")}{btn("Conheça os movimentos", "/movimentos", "claro", False)}</div>
</div></section>

<section class="sec" id="conteudos"><div class="wrap">
  <div class="cab rv"><h2>Reflexões, conhecimento e formação contínua.</h2></div>
  {posts_bloco()}
  <div class="fim">{btn("Acesse a biblioteca de conteúdos", "/conteudos", "linha")}</div>
</div></section>

<section class="sec sec--creme2" id="agenda"><div class="wrap">
  <div class="cab rv"><h2>Encontros, palestras e experiências de transformação.</h2></div>
  {agenda_bloco()}
  <div class="fim">{btn("Ver agenda completa", "/agenda", "linha")}</div>
</div></section>

<section class="sec" id="contato"><div class="wrap"><div class="chamada rv">
  <h2>Vamos construir novas possibilidades?</h2>
  <p>Para convites, palestras, mentorias, parcerias e projetos institucionais.</p>
  <div class="ctas">{btn("Entre em contato", "/contato", "ouro")}</div>
</div></div></section>'''
    return pagina("/", "Karla Messias | Psicanalista Clínica, Mentora, Palestrante e Líder",
                  "Conheça Karla Messias: Administradora, Teóloga, Psicanalista Clínica, Mentora, Palestrante e Presidente do Instituto Âncora. Fé, restauração emocional e liderança.",
                  corpo, preload_foto(FOTO_HERO))


def sobre():
    bio = "".join(f"<p>{e(p)}</p>" for p in C.BIO)
    pilares = "".join(f'<div class="pilar rv" data-d="{i}"><span class="pilar__n">{"I II III IV".split()[i]}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>'
                      for i, (t, d) in enumerate(C.PILARES))
    papeis = "".join(f"<li><b>{e(n)}</b><span>{e(p)}</span></li>" for n, p in C.LIDERANCA_INSTITUCIONAL)
    galeria = "".join(f'<div class="foto rv">{foto(f, "Karla Messias", "(max-width:900px) 46vw, 23vw")}</div>'
                      for f in ["foto-14", "foto-33", "foto-20", "foto-16", "foto-29", "foto-24", "foto-31", "foto-28"])
    enc = "".join(f"<p>{e(p)}</p>" for p in C.ENCERRAMENTO)
    corpo = f'''{pag_topo("Muito além dos títulos, uma história de propósito, conhecimento e serviço.", "", [("Sobre Karla", None)])}
<section class="sec sec--branco" id="biografia"><div class="wrap par">
  <div class="par__foto moldura rv"><div class="foto foto--alta">{foto("foto-30", "Retrato de Karla Messias", "(max-width:900px) 92vw, 44vw", lazy=False)}</div></div>
  <div class="par__txt rv" data-d="1"><h2>Biografia oficial</h2>{bio}{btn("Solicite uma palestra", "/palestras/contratacao")}</div>
</div></section>
<section class="sec sec--escuro"><div class="wrap">
  <div class="cab rv">{ORN}<h2>{e(C.POSICIONAMENTO)}</h2></div>
  <div class="pilares">{pilares}</div>
</div></section>
<section class="sec" id="lideranca"><div class="wrap">
  <div class="cab rv"><h2>Liderança institucional</h2></div>
  <ul class="papeis rv" style="max-width:56rem;margin-inline:auto">{papeis}</ul>
  <div class="fim">{btn("Conheça as instituições", "/instituicoes", "linha")}</div>
</div></section>
<section class="sec sec--branco" id="galeria"><div class="wrap">
  <div class="cab rv"><h2>Galeria de registros</h2></div>
  <div class="galeria">{galeria}</div>
</div></section>
<section class="sec"><div class="wrap"><div class="texto rv" style="text-align:center">{ORN}{enc}
  <h2 style="margin-top:2rem">{" ".join(e(t) for t in C.TRIADE)}</h2></div></div></section>
{chamada("Vamos construir algo que gere transformação?", "Para palestras, conferências, mentorias, parcerias institucionais e convites ministeriais.", "Entre em contato", "/contato")}'''
    return pagina("/sobre-karla", "Sobre Karla Messias | Biografia oficial",
                  "Karla Patrícia Messias Pereira, a Karla Messias: Administradora, Teóloga, Psicanalista Clínica, Mentora, Palestrante e Apóstola. Biografia e liderança institucional.",
                  corpo, preload_foto("foto-30"))


def atuacao():
    blocos = []
    for i, (t, d, f) in enumerate(C.ATUACAO):
        inv = " par--inv" if i % 2 else ""
        sec = " sec--branco" if i % 2 == 0 else ""
        blocos.append(f'''<section class="sec{sec}"><div class="wrap par{inv}">
  <div class="par__foto moldura rv"><div class="foto foto--larga">{foto(f, t, "(max-width:900px) 92vw, 44vw", lazy=i > 0)}</div></div>
  <div class="par__txt rv" data-d="1"><span class="lista__n">{i+1:02d}</span><h2 style="margin-top:.6rem">{e(t)}</h2><p>{e(d)}</p></div>
</div></section>''')
    blocos.append(f'<section class="sec sec--branco"><div class="wrap">{bloco_plancenter()}</div></section>')
    corpo = (pag_topo("Conhecimento que transforma. Liderança que inspira.", "", [("Atuação Profissional", None)]) + "".join(blocos) +
             chamada("Leve esse conhecimento para a sua instituição.", "Palestras, mentorias, treinamentos e consultorias para empresas, igrejas e organizações.", "Fale com a equipe", "/contato"))
    return pagina("/atuacao-profissional", "Atuação profissional | Karla Messias",
                  "Administração e gestão, teologia e formação ministerial, psicanálise clínica e desenvolvimento humano, mentoria e liderança, palestras e conferências.",
                  corpo)


def palestras():
    temas = "".join(f"<li>{e(t.rstrip('.'))}</li>" for t in C.TEMAS)
    corpo = f'''{pag_topo("Conhecimento que desperta, inspira e transforma.", "Temas para empresas, instituições de ensino, igrejas, congressos e organizações.", [("Palestras e Mentorias", None)], '<div class="ctas">' + btn("Solicitar palestra ou conferência", "/palestras/contratacao") + "</div>")}
<section class="sec sec--branco"><div class="wrap par">
  <div class="par__foto moldura rv"><div class="foto foto--alta">{foto("foto-29", "Karla Messias palestrando", "(max-width:900px) 92vw, 44vw")}</div></div>
  <div class="par__txt rv" data-d="1"><h2>A palestrante</h2>
    <p>Karla Messias é Administradora, Teóloga, Psicanalista Clínica, Mentora, Palestrante e Apóstola. Sua trajetória reúne experiências nas áreas de gestão, educação, desenvolvimento humano, liderança cristã, aconselhamento e mobilização missionária.</p>
    <p>Sua atuação é fundamentada na convicção de que o conhecimento amplia possibilidades, a restauração transforma trajetórias e a liderança responsável gera impacto na sociedade.</p>
    {link("Conheça a biografia completa", "/sobre-karla")}</div>
</div></section>
<section class="sec"><div class="wrap par par--inv">
  <div class="par__foto moldura rv"><div class="foto foto--alta">{foto("foto-14", "Karla Messias com microfone, de blazer marsala", "(max-width:900px) 92vw, 44vw")}</div></div>
  <div class="par__txt rv" data-d="1"><h2>Temas disponíveis</h2><ul class="temas" style="margin-top:1.6rem">{temas}</ul></div>
</div></section>
<section class="sec sec--branco"><div class="wrap blocos">
  {lista_bloco("Formatos", ["Presencial.", "Online."], "Palestras, treinamentos e conferências no local do evento ou transmitidos ao vivo.")}
  {lista_bloco("Público-alvo", C.PUBLICO_PALESTRAS, "", True)}
</div></section>
{chamada("Solicite uma palestra, treinamento ou conferência.", "Conte sobre o seu evento e receba as informações de disponibilidade e investimento.", "Solicitar orçamento", "/palestras/contratacao")}'''
    return pagina("/palestras", "Palestras e conferências | Karla Messias",
                  "Palestras de Karla Messias sobre inteligência emocional, liderança, identidade, propósito, mulheres e protagonismo, fé e superação. Presencial e online.",
                  corpo)


def contratacao():
    corpo = f'''{pag_topo("Solicite uma palestra, treinamento ou conferência.", "", [("Palestras", "/palestras"), ("Contratação", None)])}
<section class="sec"><div class="wrap form-par">
  <div class="form-par__txt rv"><h2>Conte sobre o seu evento.</h2>
    <p>Temas para empresas, instituições de ensino, igrejas, congressos e organizações. A equipe Karla Messias responde com disponibilidade e investimento.</p>
    {contatos_diretos()}</div>
  {form_contratacao()}
</div></section>'''
    return pagina("/palestras/contratacao", "Contratar palestra | Karla Messias",
                  "Solicite uma palestra, treinamento ou conferência com Karla Messias.", corpo)


def mentorias():
    corpo = f'''{pag_topo("Desenvolvendo pessoas para viverem seu potencial.", "Apresentação de programas de mentoria, cursos, treinamentos e capacitações.", [("Mentorias", None)])}
<section class="sec sec--branco"><div class="wrap par">
  <div class="par__foto moldura rv"><div class="foto foto--alta">{foto("foto-16", "Karla Messias de blazer lilás", "(max-width:900px) 92vw, 44vw")}</div></div>
  <div class="par__txt rv" data-d="1"><h2>Mentorias</h2><ul class="temas" style="margin-top:1.6rem">{"".join(f"<li>{e(t.rstrip('.'))}</li>" for t in C.MENTORIAS)}</ul>
    <div class="ctas">{btn("Quero participar", zap_link("Olá! Quero saber sobre as mentorias da Karla Messias."), "pri", True, " target=_blank rel=noopener")}</div></div>
</div></section>
<section class="sec" id="formacoes"><div class="wrap">
  <div class="cab rv"><h2>Cursos e formações</h2></div>
  <div class="blocos">
    {lista_bloco("Áreas", C.MENTORIA_AREAS)}
    {lista_bloco("Academia e formação", C.FORMACOES, "", True)}
  </div>
  <div class="fim">{btn("Conheça as formações disponíveis", zap_link("Olá! Quero conhecer as formações disponíveis da Karla Messias."), "pri", True, " target=_blank rel=noopener")}</div>
</div></section>'''
    return pagina("/mentorias", "Mentorias e formações | Karla Messias",
                  "Mentoria individual, em grupo e de mulheres, desenvolvimento de liderança, cursos livres, seminários e formação ministerial com Karla Messias.", corpo)


def instituicoes():
    blocos = "".join(
        f'<div class="bloco rv"><h3>{e(i["nome"])}</h3><p><b>{e(i["papel"])}</b></p><p>{e(i["texto"])}</p>'
        f'<p style="margin-top:1.4rem">{link("Conheça", "/" + i["slug"])}</p></div>' for i in C.INSTITUICOES)
    cards = [card(i["logo"], i["nome"] if i["slug"] != "casa-da-alianca" else "Casa da Aliança", i["papel"].split(":")[0], i["texto"], "/" + i["slug"]) for i in C.INSTITUICOES]
    cards += [card(l, rot, pap, nome, href) for l, rot, nome, pap, href in C.MINISTERIAL[2:]] + [card_plancenter()]
    corpo = f'''{pag_topo("Projetos e instituições que materializam uma visão.", "", [("Instituições", None)])}
<section class="sec sec--escuro"><div class="wrap">{fila("Instituições e conselhos", cards)}</div></section>
<section class="sec"><div class="wrap">
  <div class="cab rv"><h2>Formar líderes. Fortalecer a Igreja. Preparar para as nações.</h2></div>
  <div class="blocos">{blocos}</div>
</div></section>'''
    return pagina("/instituicoes", "Instituições | Karla Messias",
                  "Instituto Âncora, SISADICA, Assembleia de Deus Internacional Casa da Aliança, COMMADICA e Conselho Mundial RECONSTRUIDE.", corpo)


def inst_pagina(slug):
    i = next(x for x in C.INSTITUICOES if x["slug"] == slug)
    titulo = i["nome"] + (f'<br><span style="font-size:.55em">{e(i["sub"])}</span>' if i.get("sub") else "")
    extra = ""
    if slug == "instituto-ancora":
        extra = (f'<section class="sec sec--branco"><div class="wrap"><div class="ancora rv"><div class="ancora__logo">{logo("instituto-ancora", "Instituto Âncora", False)}</div>'
                 f'<div><h2>Uma âncora de esperança, conhecimento e transformação para as nações.</h2>'
                 f'<p>Karla Messias é Presidente do Instituto Âncora, organização dedicada a iniciativas educacionais, sociais e de desenvolvimento humano.</p>'
                 f'{btn("Como participar", "/contato?assunto=ancora")}</div></div></div></section>')
    if slug == "casa-da-alianca":
        com = C.MINISTERIAL[2]
        extra = (f'<section class="sec" id="commadica"><div class="wrap"><div class="mov rv"><div class="mov__logo">{logo(com[0], com[1])}</div>'
                 f'<div><h2>{e(com[1])}</h2><p><b>{e(com[2])}</b></p><p>{e(com[3])}.</p></div></div></div></section>')
    frentes = lista_bloco("O que reúne", i["frentes"])
    corpo = f'''{pag_topo(titulo, "", [("Instituições", "/instituicoes"), (i["nome"] if len(i["nome"]) < 20 else "Casa da Aliança", None)])}
{extra}
<section class="sec{" sec--branco" if slug != "instituto-ancora" else ""}"><div class="wrap inst">
  <div class="inst__logo rv">{logo(i["logo"], i["nome"], slug == "instituto-ancora")}</div>
  <div class="rv" data-d="1"><h2>{e(i["nome"])}</h2><span class="inst__papel">{e(i["papel"])}</span><p>{e(i["texto"])}</p>
    <div style="margin-top:2rem">{frentes}</div>
    <div class="ctas" style="margin-top:2rem">{btn("Fale com a equipe", "/contato?assunto=" + slug)}</div></div>
</div></section>'''
    nome_curto = {"instituto-ancora": "Instituto Âncora", "sisadica": "SISADICA", "casa-da-alianca": "Casa da Aliança"}[slug]
    return pagina("/" + slug, f"{nome_curto} | Karla Messias", f"{i['nome']}. {i['papel']} {i['texto']}", corpo)


def movimentos():
    itens = []
    for idx, (i, l, nome, pap, txt) in enumerate(C.MOVIMENTOS):
        fundo = " mov__logo--fundo" if l in LOGOS_COM_FUNDO else ""
        itens.append(f'<article class="mov rv" id="{i}"><div class="mov__logo{fundo}"{estilo_cor(l)}>{logo(l, nome, idx > 1)}</div>'
                     f'<div><h2>{e(nome)}</h2><span class="card__papel" style="display:block;margin-top:.5rem;color:var(--dourado);opacity:1">{e(pap.upper())}</span><p>{e(txt)}</p>'
                     f'{link("Quero participar", zap_link("Olá! Quero saber mais sobre " + nome + "."))}</div></article>')
    corpo = f'''{pag_topo("Uma visão que alcança diferentes dimensões da vida.", "Ministérios, movimentos e iniciativas idealizados e liderados por Karla Messias.", [("Ministérios e Movimentos", None)])}
<section class="sec sec--escuro"><div class="wrap">{fila("Ministérios, movimentos e iniciativas", cards_movimentos(""))}</div></section>
<section class="sec"><div class="wrap">{"".join(itens)}</div></section>'''
    return pagina("/movimentos", "Ministérios e movimentos | Karla Messias",
                  "Princesas Virtuosas, Conselho Mundial RECONSTRUÍDE, THE DIVE, Visão de Águia, Rede Águias de Intercessão, Deus Sara as Nações e Sacerdócio Real.", corpo)


def conteudos():
    cats = "".join(f"<li>{e(c.rstrip('.'))}</li>" for c in C.CONTEUDO_CATEGORIAS)
    corpo = f'''{pag_topo("Conhecimento para transformar sua jornada.", "Artigos e reflexões, estudos bíblicos, devocionais, vídeos e entrevistas e materiais educacionais.", [("Conteúdos", None)])}
<section class="sec"><div class="wrap">
  <div class="vazio rv"><h3>A biblioteca de conteúdos está sendo preparada.</h3><p>Em breve, artigos, estudos e materiais organizados por tema. Enquanto isso, acompanhe as reflexões diárias no Instagram.</p>
    <ul class="tipos">{cats}</ul>
    <div class="ctas">{btn("Seguir " + IG_USER, INSTAGRAM, "pri", True, " target=_blank rel=noopener")}</div></div>
</div></section>
<section class="sec sec--escuro"><div class="wrap par">
  <div class="par__foto rv"><div class="mov__logo" style="max-width:24rem;margin-inline:auto">{logo("devocional-palavra-do-rei", "Devocional Palavra do Rei")}</div></div>
  <div class="par__txt rv" data-d="1"><h2>Devocional Palavra do Rei</h2><p>A Palavra do Rei tem autoridade.</p>
    <div class="ctas">{btn("Receber o devocional", zap_link("Olá! Quero receber o Devocional Palavra do Rei."), "ouro", True, " target=_blank rel=noopener")}</div></div>
</div></section>'''
    return pagina("/conteudos", "Conteúdos e publicações | Karla Messias",
                  "Reflexões, estudos bíblicos, devocionais e materiais de Karla Messias sobre fé, restauração emocional, liderança e propósito.", corpo)


def agenda():
    corpo = f'''{pag_topo("Encontros que geram conhecimento e transformação.", "", [("Agenda", None)])}
<section class="sec"><div class="wrap">{agenda_bloco(True)}</div></section>
{chamada("Quer levar Karla Messias ao seu evento?", "Congressos, seminários, conferências, encontros de mulheres e eventos missionários.", "Solicitar participação", "/palestras/contratacao")}'''
    return pagina("/agenda", "Agenda | Karla Messias", "Congressos, seminários, conferências, palestras, cursos, encontros de mulheres e eventos missionários com Karla Messias.", corpo)


def contato():
    motivos = "".join(f"<li>{e(m.rstrip('.'))}</li>" for m in C.CONTATO_MOTIVOS)
    publicos = "".join(f'<a href="{h}"><b>{e(p)}</b><span>{e(o)}</span></a>' for p, o, h in C.PUBLICOS)
    corpo = f'''{pag_topo("Vamos construir algo que gere transformação?", "Para palestras, conferências, mentorias, parcerias institucionais e convites ministeriais.", [("Contato", None)])}
<section class="sec"><div class="wrap form-par">
  <div class="form-par__txt rv"><h2>Fale com a equipe Karla Messias.</h2><ul>{motivos}</ul>{contatos_diretos()}</div>
  {form_contato()}
</div></section>
<section class="sec sec--branco"><div class="wrap">
  <div class="cab rv"><h2>Encontre o caminho certo para você.</h2></div>
  <div class="publico rv">{publicos}</div>
</div></section>'''
    return pagina("/contato", "Contato | Karla Messias", "Convites, palestras, mentorias, parcerias e projetos institucionais com Karla Messias.", corpo)


def privacidade():
    corpo = f'''{pag_topo("Política de Privacidade", "Como os seus dados são tratados neste site, conforme a Lei Geral de Proteção de Dados (LGPD, Lei 13.709/2018).", [("Privacidade", None)])}
<section class="sec"><div class="wrap"><div class="texto">
<h2>Quem cuida dos seus dados</h2><p>Este site é de Karla Patrícia Messias Pereira (Karla Messias), responsável pelo tratamento dos dados enviados por meio dele.</p>
<h2>Que dados recebemos</h2><p>Apenas os que você digita nos formulários de contato e de contratação: nome, empresa ou instituição, e-mail, telefone ou WhatsApp, cidade e estado, dados do evento e a sua mensagem.</p>
<h2>Para que usamos</h2><p>Para responder ao seu contato, enviar informações sobre palestras, mentorias, cursos e eventos que você pediu e organizar convites e parcerias. Não vendemos nem compartilhamos os seus dados com terceiros para fins comerciais.</p>
<h2>Como a mensagem chega até nós</h2><p>Ao enviar um formulário, a sua mensagem é aberta no WhatsApp, já preenchida, para que você a envie à equipe Karla Messias. O WhatsApp tem a sua própria política de privacidade.</p>
<h2>Cookies</h2><p>Este site não usa cookies de publicidade nem de rastreamento. Se ferramentas de medição forem adicionadas no futuro, como o Google Analytics, você será avisado e poderá escolher se aceita.</p>
<h2>Seus direitos</h2><p>Você pode pedir a qualquer momento acesso, correção ou exclusão dos seus dados, e retirar o seu consentimento. Basta escrever para a equipe pelo WhatsApp ou pelo Instagram {IG_USER}.</p>
<h2>Atualização</h2><p>Esta política foi publicada em 04/11/2026 e pode ser atualizada. A versão em vigor é sempre a desta página.</p>
</div></div></section>'''
    return pagina("/privacidade", "Política de Privacidade | Karla Messias", "Política de privacidade e tratamento de dados (LGPD) do site Karla Messias.", corpo)


def landing():
    temas = "".join(f'<li class="rv" data-d="{i % 4}"><span>{i+1:02d}</span>{e(t.rstrip("."))}</li>' for i, t in enumerate(C.TEMAS))
    areas = "".join(f'<div class="lista__item rv" data-foto="/assets/img/fotos/{f}-800.webp"><span class="lista__n">{i+1:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>'
                    for i, (t, d, f) in enumerate(C.ATUACAO))
    bio = "".join(f"<p>{e(p)}</p>" for p in C.BIO)
    faixa_itens = "".join(f"<span>{e(t)}</span><i></i>" for t in C.TITULOS)
    corpo = f'''
<section class="capa">
  <div class="capa__bg" data-paralaxe>{fundo_img(FOTO_HERO, "Karla Messias de blazer marsala e vestido creme", lazy=False, pos="75% 50%", pos_m="50% 12%")}</div>
  <div class="wrap"><div class="capa__txt">
    <h1>Fé, restauração e liderança <em>que transformam vidas.</em></h1>
    <p><b>Administradora, Teóloga, Psicanalista Clínica, Mentora, Palestrante e Líder Ministerial.</b></p>
    <p style="margin-top:.9rem">Uma trajetória dedicada ao desenvolvimento humano, à restauração emocional, à formação de líderes e à expansão de projetos que promovem transformação espiritual, pessoal e social.</p>
    <div class="ctas">{btn("Conheça minha história", "#quem-e", "ouro")}{btn("Contrate uma palestra", "#palestras", "claro", False)}{btn("Conheça meus projetos", "#projetos", "claro", False)}</div>
  </div></div>
</section>
<div class="faixa" aria-hidden="true"><div class="faixa__t">{faixa_itens * 4}</div></div>

<section class="capa capa--clara capa--bio" id="quem-e">
  <div class="capa__bg" data-paralaxe>{fundo_img("foto-21", "Karla Messias em seu escritório", pos="20% 50%", pos_m="40% 15%")}</div>
  <div class="wrap"><div class="capa__txt rv">
    <h2>Muito além dos títulos, uma história de propósito, conhecimento e serviço.</h2>{bio}
    <div class="ctas">{btn("Conheça minha trajetória completa", "/sobre-karla")}</div>
  </div></div>
</section>

<section class="sec" id="areas"><div class="wrap">
  <div class="cab rv"><h2>Conhecimento que transforma. Liderança que inspira.</h2></div>
  <div class="lista" data-lista>{areas}</div>
</div></section>

<section class="sec sec--branco compacto" id="palestras"><div class="wrap">
  <div class="cab rv"><h2>Conhecimento que desperta, inspira e transforma.</h2><p>Temas disponíveis:</p></div>
  <ol class="temas-grade temas-grade--4">{temas}</ol>
  <div class="fim">{btn("Solicitar palestra ou conferência", "/palestras/contratacao")}</div>
</div></section>

<section class="fixa" id="mentorias">
  <div class="fixa__bg">{fundo_img("foto-16", "", pos="82% 50%", pos_m="50% 14%")}</div>
  <div class="wrap"><div class="fixa__txt rv">
    <h2>Desenvolvendo pessoas para viverem seu potencial.</h2>
    <p>Apresentação de programas de mentoria, cursos, treinamentos e capacitações.</p>
    {tags(C.MENTORIA_AREAS, 2, True, " tags--esq")}
    <div class="ctas">{btn("Conheça as formações disponíveis", "/mentorias", "ouro")}</div>
  </div></div>
</section>

<section class="sec catalogo" id="projetos"><div class="wrap">
  <div class="cab rv"><h2>Projetos e instituições que materializam uma visão.</h2></div>
  {fila("Instituições e empresas", cards_instituicoes())}
  {pilha_instituicoes()}
</div></section>

<section class="sec catalogo" id="movimentos" style="padding-top:0"><div class="wrap">
  <div class="cab rv"><h2>Uma visão que alcança diferentes dimensões da vida.</h2></div>
  {fila("Ministérios, movimentos e iniciativas", cards_movimentos(sem_conselho=True))}
</div></section>

<section class="sec" id="conteudos"><div class="wrap">
  <div class="cab rv"><h2>Conhecimento para transformar sua jornada.</h2></div>
  {posts_bloco()}
  {tags(C.CONTEUDO_ESPACO, 4, extra=" rv")}
  <div class="fim">{btn("Acesse os conteúdos", "/conteudos", "linha")}</div>
</div></section>

<section class="sec sec--creme2" id="agenda"><div class="wrap">
  <div class="cab rv"><h2>Encontros que geram conhecimento e transformação.</h2><p>Cada evento terá página própria, programação, local, informações de inscrição e contato.</p></div>
  {tags(C.EVENTO_TIPOS, 4, extra=" rv")}
  <div class="fim">{btn("Ver agenda", "/agenda", "linha")}</div>
</div></section>

<section class="sec" id="contato"><div class="wrap"><div class="chamada rv">
  <h2>Vamos construir algo que gere transformação?</h2>
  <p>Para palestras, conferências, mentorias, parcerias institucionais e convites ministeriais:</p>
  {tags(C.CONTATO_MOTIVOS, 3, True)}
  <div class="ctas">{btn("Fale com a equipe Karla Messias", "/obrigado?c=landing", "ouro")}</div>
</div></div></section>'''
    return pagina("/landingpage", "Karla Messias | Fé, restauração e liderança que transformam vidas",
                  "Karla Messias: Administradora, Teóloga, Psicanalista Clínica, Mentora, Palestrante e Líder Ministerial. Palestras, mentorias, instituições e movimentos.",
                  corpo, preload_foto(FOTO_HERO), landing=True)


def obrigado():
    corpo = f'''<section class="obrigado"><div>
  <img src="/assets/img/logos/km-monograma.webp" alt="Karla Messias" width="104" height="104">
  <h1>Estamos abrindo <span class="ac">a conversa.</span></h1>
  <p>Em instantes você fala com a equipe Karla Messias pelo WhatsApp.</p>
  <div class="gira" aria-hidden="true"></div>
  <div class="ctas"><a class="btn btn--pri" id="vai" href="https://wa.me/{WHATSAPP}">Abrir o WhatsApp {SETA}</a><a class="btn btn--linha" href="/">Voltar ao site</a></div>
</div></section>
<script>
(function(){{
  var W='{WHATSAPP}', msg='Olá! Vim pelo site da Karla Messias.';
  try{{ msg = sessionStorage.getItem('km_msg') || msg; sessionStorage.removeItem('km_msg'); }}catch(e){{}}
  var dest='https://wa.me/'+W+'?text='+encodeURIComponent(msg); document.getElementById('vai').href=dest;
  var c=(new URLSearchParams(location.search).get('c')||'site').replace(/[^a-z0-9_-]/gi,'');
  var t0=Date.now(), partiu=false;
  function vai(){{ if(partiu) return; partiu=true; location.replace(dest); }}
  function talvez(){{ var f=900-(Date.now()-t0); setTimeout(vai, f>0?f:0); }}
  window.dataLayer=window.dataLayer||[]; window.dataLayer.push({{event:'conversao_whatsapp',contexto:c,eventCallback:talvez,eventTimeout:2000}});
  if(!window.google_tag_manager) talvez();
  setTimeout(vai,2600);
}})();
</script>'''
    html = pagina("/obrigado", "Abrindo a conversa | Karla Messias", "Abrindo o WhatsApp da equipe Karla Messias.", corpo, robots="noindex,nofollow")
    # a ponte não leva cabeçalho, rodapé nem o botão flutuante
    html = re.sub(r'<header class="top">.*?</header>', "", html, flags=re.S)
    html = re.sub(r'<div class="frase".*?</a>\n<script', "<script", html, flags=re.S)
    return html


# ------------------------------------------------------------------ saída
def main():
    global CSS_MIN
    CSS_MIN = minificar(CSS.read_text())
    paginas = {
        "index.html": home(), "sobre-karla.html": sobre(), "atuacao-profissional.html": atuacao(),
        "palestras.html": palestras(), "palestras/contratacao.html": contratacao(), "mentorias.html": mentorias(),
        "instituicoes.html": instituicoes(), "instituto-ancora.html": inst_pagina("instituto-ancora"),
        "sisadica.html": inst_pagina("sisadica"), "casa-da-alianca.html": inst_pagina("casa-da-alianca"),
        "movimentos.html": movimentos(), "conteudos.html": conteudos(), "agenda.html": agenda(),
        "contato.html": contato(), "privacidade.html": privacidade(), "landingpage.html": landing(), "obrigado.html": obrigado(),
    }
    for arq, html in paginas.items():
        p = RAIZ / arq
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(html)
        sobra = re.findall(r"\{\{[A-Z_]+\}\}", html)
        print(f"  {arq}: {len(html.encode())/1024:.1f} KB" + (f"  ! {sobra}" if sobra else ""))
    rotas = [a[:-5] for a in paginas if a not in ("obrigado.html",)]
    hoje = date.today().isoformat()
    urls = "".join(f"<url><loc>{DOMINIO}/{'' if r == 'index' else r}</loc><lastmod>{hoje}</lastmod></url>" for r in rotas)
    (RAIZ / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    (RAIZ / "robots.txt").write_text("User-agent: *\n" + ("Allow: /\n" if INDEXAR else "Disallow: /\n") + f"\nSitemap: {DOMINIO}/sitemap.xml\n")
    mov = "\n".join(f"- {n}: {d}" for _, _, n, _, d in C.MOVIMENTOS)
    inst = "\n".join(f"- {i['nome']}: {i['papel']} {i['texto']}" for i in C.INSTITUICOES)
    (RAIZ / "llms.txt").write_text(f"""# Karla Messias

> {C.NOME_COMPLETO}, conhecida como Karla Messias: {", ".join(C.TITULOS[:-1])} e {C.TITULOS[-1]}. {C.POSICIONAMENTO}

## Páginas
- [Início]({DOMINIO}/): apresentação, pilares, atuação, palestras, mentorias, instituições, movimentos, conteúdos, agenda e contato.
- [Sobre Karla]({DOMINIO}/sobre-karla): biografia oficial e liderança institucional.
- [Atuação profissional]({DOMINIO}/atuacao-profissional)
- [Palestras]({DOMINIO}/palestras) e [contratação]({DOMINIO}/palestras/contratacao)
- [Mentorias e formações]({DOMINIO}/mentorias)
- [Instituições]({DOMINIO}/instituicoes): Instituto Âncora, SISADICA e Casa da Aliança.
- [Ministérios e movimentos]({DOMINIO}/movimentos)
- [Contato]({DOMINIO}/contato)

## Instituições
{inst}
- {C.PLANCENTER['nome']} ({C.PLANCENTER['papel']}): {C.PLANCENTER['texto']} {C.PLANCENTER['url']}

## Ministérios, movimentos e iniciativas
{mov}

## Palestras (temas)
""" + "\n".join(f"- {x.rstrip('.')}" for x in C.TEMAS) + f"""

## Contato
WhatsApp: +{WHATSAPP[:2]} {WHATSAPP[2:4]} {WHATSAPP[4:9]}-{WHATSAPP[9:]}
Instagram: {IG_USER}
""")
    print(f"  site.js v={hash_de(JS)}  indexar={INDEXAR}")


if __name__ == "__main__":
    main()
