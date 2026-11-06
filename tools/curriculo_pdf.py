#!/usr/bin/env python3
"""Gera o currículo da Karla em PDF a partir de _src/curriculo.py.

    python3 tools/curriculo_pdf.py
    CURRICULO_EMAIL=endereco@dela python3 tools/curriculo_pdf.py pasta-fora-do-repo

Saem duas versões do mesmo texto:
- pública (assets/docs/): a que o site oferece, sem e-mail, que não aparece em nenhuma página, e sem objetivo profissional.
- completa: para ela enviar a quem pedir, com e-mail e objetivo profissional. Só sai com CURRICULO_EMAIL e nunca entra
  no repo, que é público. A cópia em uso fica em 06_OUTPUTS/karla-messias no kit.
"""
import os
import sys
import tempfile
from html import escape as e
from pathlib import Path

from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "_src"))
import curriculo as K  # noqa: E402

FONTES = RAIZ / "assets/fonts"
EMAIL = os.environ.get("CURRICULO_EMAIL", "")

CSS = f"""
@font-face{{font-family:Poppins;src:url({FONTES.as_uri()}/poppins-400.woff2);font-weight:400}}
@font-face{{font-family:Poppins;src:url({FONTES.as_uri()}/poppins-500.woff2);font-weight:500}}
@font-face{{font-family:Playfair;src:url({FONTES.as_uri()}/playfair-500.woff2);font-weight:500}}
@page{{size:A4;margin:12mm 15mm 13mm}}
*{{box-sizing:border-box}}
html{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{margin:0;font:400 8.6pt/1.4 Poppins,Arial,sans-serif;color:#2B1D1F;font-variant-ligatures:none}}
p,ul,h1,h2,h3{{margin:0}}
a{{color:inherit;text-decoration:none}}
header{{padding-bottom:9pt;border-bottom:1.2pt solid #7B1E2D}}
h1{{font:500 18.5pt/1.2 Playfair,Georgia,serif;letter-spacing:.045em;text-transform:uppercase}}
.titulos{{margin-top:3pt;font-weight:500;font-size:8.4pt;letter-spacing:.075em;text-transform:uppercase;color:#7B1E2D}}
.contato{{display:flex;flex-wrap:wrap;gap:0 14pt;margin-top:6pt;font-size:8.6pt;color:#6F5F5C}}
section{{margin-top:10pt}}
section.junto{{break-inside:avoid}}
h2{{font-weight:500;font-size:8.8pt;letter-spacing:.13em;text-transform:uppercase;color:#7B1E2D;padding-bottom:2.5pt;border-bottom:.5pt solid #D9CFC4;break-after:avoid}}
.corpo{{margin-top:5pt}}
.corpo p+p{{margin-top:4pt}}
.nota{{margin-top:4pt;font-size:8pt;color:#6F5F5C}}
.item{{margin-top:5.5pt;break-inside:avoid}}
.item__cab{{display:flex;justify-content:space-between;align-items:baseline;gap:12pt}}
h3{{font-weight:500;font-size:9.1pt;line-height:1.35}}
.periodo{{flex:none;font-weight:500;font-size:8.6pt;color:#6F5F5C}}
.papel{{color:#6F5F5C}}
.item p{{margin-top:2pt}}
.rotulo{{font-weight:500}}
ul{{padding:0;list-style:none}}
li{{position:relative;padding-left:9pt;margin-top:.8pt}}
li::before{{content:"";position:absolute;left:0;top:.56em;width:3pt;height:3pt;border-radius:50%;background:#B08A48}}
.item ul{{margin-top:2.5pt}}
.duas{{columns:2;column-gap:16pt;margin-top:4pt;break-inside:avoid}}
.duas li{{break-inside:avoid}}
.solta{{margin-top:4pt}}
"""


def lista(itens, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f"<ul{c}>" + "".join(f"<li>{e(x)}</li>" for x in itens) + "</ul>"


def item(d):
    periodo = f'<span class="periodo">{e(d["periodo"])}</span>' if d.get("periodo") else ""
    texto = f'<p>{e(d["texto"])}</p>' if d.get("texto") else ""
    rotulo = f'<p class="rotulo">{e(d["rotulo"])}</p>' if d.get("rotulo") else ""
    return (f'<div class="item"><div class="item__cab"><h3>{e(d["org"])}</h3>{periodo}</div>'
            f'<p class="papel">{e(d["papel"])}</p>{texto}{rotulo}{lista(d["itens"])}</div>')


def secao(titulo, miolo, junto=False):
    return f'<section{" class=junto" if junto else ""}><h2>{e(titulo)}</h2>{miolo}</section>'


def documento(publico):
    contato = [f"<span>{e(K.LOCAL)}</span>",
               f'<a href="tel:+55{"".join(c for c in K.TELEFONE if c.isdigit())}">{e(K.TELEFONE)}</a>']
    if not publico:
        contato.append(f'<a href="mailto:{EMAIL}">{e(EMAIL)}</a>')
    contato.append(f'<a href="https://{K.SITE}">{e(K.SITE)}</a>')
    partes = [
        secao("Perfil profissional", '<div class="corpo">' + "".join(f"<p>{e(p)}</p>" for p in K.PERFIL) + "</div>"),
        secao("Principais competências", lista(K.COMPETENCIAS, "duas")),
        secao("Experiência profissional", f'<p class="nota">{e(K.NOTA_EXPERIENCIA)}</p>' + "".join(item(d) for d in K.EXPERIENCIA)),
        secao("Empreendedorismo e liderança empresarial", item(K.PLANCENTER)),
        secao("Consultoria e atuação institucional", item(K.CONSULTORIA) + item(K.TERCEIRO_SETOR)),
        secao("Experiências profissionais complementares", "".join(item(d) for d in K.COMPLEMENTARES)),
        secao("Formação acadêmica e qualificações", lista(K.FORMACAO, "solta"), True),
        secao("Conhecimentos técnicos e sistemas", f'<div class="corpo"><p>{e(K.SISTEMAS_TEXTO)}</p></div>' +
              lista([", ".join(K.SISTEMAS[:-1]), K.SISTEMAS[-1]], "solta"), True),
        secao("Capacitações e aperfeiçoamento profissional", lista(K.CAPACITACOES, "duas"), True),
        secao("Diferenciais profissionais", lista(K.DIFERENCIAIS, "solta"), True),
    ]
    if not publico:
        partes.append(secao("Objetivo profissional", f'<div class="corpo"><p>{e(K.OBJETIVO)}</p></div>', True))
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Currículo de {e(K.NOME)}</title><style>{CSS}</style></head><body>
<header><h1>{e(K.NOME)}</h1><p class="titulos">{e(K.TITULOS)}</p><div class="contato">{"".join(contato)}</div></header>
{"".join(partes)}</body></html>"""


RODAPE = f"""<div style="width:100%;padding:0 15mm;display:flex;justify-content:space-between;font:7pt Arial,sans-serif;color:#6F5F5C">
<span>{e(K.NOME)}</span><span>Página <span class="pageNumber"></span> de <span class="totalPages"></span></span></div>"""


def gerar(pagina, destino, publico):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as t:
        t.write(documento(publico))
    pagina.goto(Path(t.name).as_uri())
    pagina.evaluate("document.fonts.ready")
    destino.parent.mkdir(parents=True, exist_ok=True)
    pagina.pdf(path=str(destino), format="A4", prefer_css_page_size=True, print_background=True, tagged=True, outline=True,
               display_header_footer=True, header_template="<span></span>", footer_template=RODAPE)
    Path(t.name).unlink()
    w = PdfWriter(clone_from=str(destino))
    w.add_metadata({"/Title": f"Currículo de {K.NOME}", "/Author": K.NOME, "/Subject": K.TITULOS})
    w.write(str(destino))
    print(f"  {destino}: {len(PdfReader(str(destino)).pages)} páginas, {destino.stat().st_size / 1024:.0f} KB")


def main():
    with sync_playwright() as p:
        # o Chromium do próprio Playwright, nunca o Chrome do dia a dia; aceita a versão que já estiver baixada
        cache = sorted((Path.home() / "Library/Caches/ms-playwright").glob("chromium_headless_shell-*/*/chrome-headless-shell"))
        nav = p.chromium.launch(executable_path=str(cache[-1])) if cache else p.chromium.launch()
        pagina = nav.new_page()
        if EMAIL and len(sys.argv) > 1:
            gerar(pagina, Path(sys.argv[1]) / "Curriculo-Karla-Messias.pdf", publico=False)
        else:
            print("  versão completa não gerada: ela pede CURRICULO_EMAIL e uma pasta fora do repo")
        gerar(pagina, RAIZ / "assets/docs/curriculo-karla-messias.pdf", publico=True)
        nav.close()


if __name__ == "__main__":
    main()
