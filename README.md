# Karla Messias — site institucional e landing

Site estático: home de 12 seções e páginas internas (sobre, atuação, palestras e contratação, mentorias, instituições,
Instituto Âncora, SISADICA, Casa da Aliança, movimentos, conteúdos, agenda, contato, privacidade), landing em
`/landingpage` e ponte `/obrigado` para o WhatsApp.

## Como editar
- Currículo: `_src/curriculo.py` alimenta a página `/curriculo` e o PDF. Mudou o texto: `python3 tools/curriculo_pdf.py` e depois o build.
- Copy: `_src/conteudo.py` (transcrita do briefing da Karla; o texto original está em `_src/briefing-ocr.txt`).
- Montagem, cores dos cards e destinos: `build.py`. Estilo: `assets/css/site.css`. Comportamento: `assets/js/site.js`.
- Eventos e artigos: preencha `EVENTOS` e `POSTS` no `build.py`; as áreas da home e da agenda se montam sozinhas.
- Depois de qualquer mudança: `python3 build.py`. Prévia: `python3 tools/serve.py 4190`.

## Domínio e SEO
- Tudo sai de `DOMINIO` no `build.py` (canonical, og, schema, sitemap, robots e llms.txt).
- `INDEXAR = False` até a Karla aprovar e o domínio (sugestão dela: karlamessias.com.br) estar ligado na Vercel.
  Para trocar: ligar o domínio na Vercel, trocar `DOMINIO`, `INDEXAR = True`, rodar o build e fazer o push.

## Pendências com a cliente
- Confirmar que o WhatsApp profissional é o +55 61 99397-3723.
- Fotos originais do fotógrafo (as atuais vieram pelo WhatsApp, 1024 px).
- Conteúdo das subpáginas que o briefing lista e ainda não tem texto (certificados, missão e valores do
  Instituto, países do SISADICA, declaração de fé da Casa da Aliança etc.).
- Versão em inglês: estrutura pronta, tradução depois da aprovação do texto em português.
- Painel administrativo, e-mail marketing e inscrição em cursos pedem uma segunda fase (CMS/sistema).
