"""Copy do site Karla Messias, transcrita do briefing que ela mandou (03/11/2026).
Fonte: _src/briefing-ocr.txt. Mudanças só de grafia (crase, ponto final, "Conselhos" -> "Conselho").
"""

NOME = "Karla Messias"
NOME_COMPLETO = "Karla Patrícia Messias Pereira"
LEMA = "Fé • Restauração Emocional • Liderança"
TITULOS = ["Administradora", "Teóloga", "Psicanalista Clínica", "Mentora", "Palestrante", "Apóstola"]
TITULOS_TXT = "Administradora | Teóloga | Psicanalista Clínica | Mentora | Palestrante | Apóstola."

POSICIONAMENTO = ("Uma mulher de fé, conhecimento e liderança, dedicada à restauração de vidas, ao desenvolvimento "
                  "humano, à formação de líderes e à transformação de pessoas e instituições.")

PILARES = [
    ("FÉ E ESPIRITUALIDADE", "Fundamento da identidade, da missão, dos valores cristãos e do chamado ministerial."),
    ("RESTAURAÇÃO EMOCIONAL", "Psicanálise Clínica, cuidado emocional, autoconhecimento e desenvolvimento humano."),
    ("CONHECIMENTO E EDUCAÇÃO", "Teologia, formação, ensino, capacitação e produção de conhecimento."),
    ("LIDERANÇA E PROPÓSITO", "Gestão, empreendedorismo, liderança, mentoria e transformação de pessoas e organizações."),
]

# home, seção 4 (foto que aparece ao passar o mouse)
ATUACAO_HOME = [
    ("Administração e Gestão", "Planejamento, organização e liderança institucional.", "foto-21"),
    ("Teologia", "Ensino bíblico e formação cristã.", "foto-26"),
    ("Psicanálise Clínica", "Escuta clínica, autoconhecimento e compreensão dos processos emocionais.", "foto-13"),
    ("Mentoria", "Desenvolvimento pessoal e liderança.", "foto-16"),
    ("Palestras", "Educação, comportamento, propósito e transformação.", "foto-20"),
]

# landing, seção 3, e página de atuação
ATUACAO = [
    ("Administração e Gestão",
     "Desenvolvimento de competências administrativas, planejamento estratégico, gestão institucional, liderança e organização de projetos.",
     "foto-21"),
    ("Teologia e Formação Ministerial",
     "Ensino bíblico, formação de líderes, discipulado, desenvolvimento ministerial e capacitação missionária.",
     "foto-26"),
    ("Psicanálise Clínica e Desenvolvimento Humano",
     "Atuação voltada ao autoconhecimento, compreensão dos processos emocionais, desenvolvimento pessoal e cuidado com a saúde emocional, respeitando os limites e a finalidade da prática profissional.",
     "foto-13"),
    ("Mentoria e Liderança",
     "Acompanhamento e desenvolvimento de pessoas, líderes, empreendedores e profissionais que desejam ampliar suas competências e sua capacidade de realização.",
     "foto-16"),
    ("Palestras e Conferências",
     "Conteúdos sobre liderança, inteligência emocional, propósito, identidade, desenvolvimento humano, fé e transformação.",
     "foto-20"),
]

TEMAS_HOME = ["Inteligência emocional.", "Liderança e gestão estratégica.", "Desenvolvimento humano.",
              "Identidade e propósito.", "Mulheres e protagonismo.", "Inteligência financeira."]

TEMAS = ["Inteligência Emocional e Desenvolvimento Humano.", "Liderança e Gestão Estratégica.",
         "Identidade, Propósito e Autoconhecimento.", "Inteligência Financeira e Desenvolvimento Pessoal.",
         "Mulheres, Liderança e Protagonismo.", "Fé, Propósito e Superação.",
         "Restauração Emocional e Reconstrução de Identidade.", "Empreendedorismo e Visão Estratégica."]

PUBLICO_PALESTRAS = ["Empresas", "Instituições de ensino", "Igrejas", "Congressos", "Organizações"]

MENTORIAS = ["Mentoria individual.", "Mentoria em grupo.", "Mentoria de mulheres.",
             "Desenvolvimento de liderança.", "Programas de capacitação."]
MENTORIA_AREAS = ["Mentoria de desenvolvimento pessoal.", "Mentoria de liderança.", "Formação de mulheres líderes.",
                  "Desenvolvimento de competências emocionais.", "Capacitação de líderes cristãos.",
                  "Formação ministerial e missionária."]
FORMACOES = ["Cursos livres.", "Formação de líderes.", "Formação ministerial.",
             "Cursos de desenvolvimento pessoal.", "Seminários.", "Apostilas e materiais educacionais."]

# home, seção 8: liderança e educação ministerial (logo, rótulo do card, nome, papel, destino)
MINISTERIAL = [
    ("sisadica", "SISADICA", "Sistema ADICA de Ensino Teológico e de Missões.", "Presidência do Conselho Mundial", "/sisadica"),
    ("adica-brasao", "ADICA", "Assembleia de Deus Internacional Casa da Aliança", "Pastora Presidente", "/casa-da-alianca"),
    ("commadica", "COMMADICA", "Conselho Mundial de Ministros e Ministérios ADICA", "Apóstola Presidente e Liderança Espiritual", "/casa-da-alianca#commadica"),
    ("conselho-reconstruide", "RECONSTRUIDE",
     "Conselho Mundial RECONSTRUIDE de Apoio a Projetos Sociais, Educacionais, Humanitários de Saúde e Missões Transcultural",
     "Presidência Mundial", "/movimentos#conselho-mundial-reconstruide"),
]

# ministérios, movimentos e iniciativas: a lista atualizada que ela mandou às 16:26
# (id, logo, nome, papel no card, descrição)
MOVIMENTOS = [
    ("princesas-virtuosas", "princesas-virtuosas", "Princesas Virtuosas", "Ministério de mulheres",
     "Ministério de mulheres cristãs voltado à fé, restauração, capacitação e fortalecimento feminino."),
    ("conselho-mundial-reconstruide", "conselho-reconstruide", "Conselho Mundial RECONSTRUÍDE", "Mobilização missionária",
     "Mobilização missionária com foco em restauração, reconstrução de vidas e cumprimento da missão e apoio à implantação de Igrejas e projetos sociais e humanitários."),
    ("the-dive", "the-dive", "THE DIVE · O MERGULHO", "Restauração integral",
     "Jornada de restauração integral, com abordagem Corpo, Alma e Espírito."),
    ("visao-de-aguia", "visao-de-aguia", "Visão de Águia", "Empreendedores e empresários",
     "Iniciativa direcionada a empreendedores e empresários, com foco em visão estratégica, liderança, desenvolvimento e propósito."),
    ("rede-aguias-de-intercessao", "rede-aguias-intercessao", "Rede Águias de Intercessão", "Intercessão profética",
     "Rede de mobilização e intercessão cristã, dedicada à oração e ao fortalecimento espiritual."),
    ("deus-sara-as-nacoes", "deus-sara-as-nacoes", "Deus Sara as Nações", "Cura e libertação",
     "Movimento de oração e intercessão com perspectiva missionária e compromisso com as nações."),
    ("sacerdocio-real", "sacerdocio-real", "Sacerdócio Real", "Ministério de homens",
     "Iniciativa de formação e fortalecimento da identidade sacerdotal e do serviço cristão."),
]

INSTITUICOES = [
    {
        "slug": "instituto-ancora", "logo": "instituto-ancora", "nome": "Instituto Âncora",
        "papel": "Presidência: Karla Messias.",
        "texto": "Instituição dedicada ao desenvolvimento educacional, humano e social, por meio de projetos, capacitações, programas de formação e iniciativas de transformação comunitária.",
        "frentes": ["História.", "Apresentação institucional.", "Presidência.", "Missão, visão e valores.", "Projetos.",
                    "Programas educacionais.", "Projetos sociais.", "Parcerias.", "Como participar."],
    },
    {
        "slug": "sisadica", "logo": "sisadica", "nome": "SISADICA",
        "sub": "Sistema de Ensino Teológico e de Missões",
        "papel": "Presidência do Conselho Mundial: Karla Messias.",
        "texto": "Sistema dedicado à formação teológica, capacitação ministerial, educação cristã e desenvolvimento missionário.",
        "frentes": ["Apresentação.", "Conselho Mundial.", "Estrutura internacional.", "Formação teológica.", "Escola de Missões.",
                    "Cursos e programas.", "Países e representações.", "Congressos e atividades."],
    },
    {
        "slug": "casa-da-alianca", "logo": "adica-casa-da-alianca", "nome": "Assembleia de Deus Internacional Casa da Aliança",
        "papel": "Pastora Presidente: Apóstola Karla Messias.",
        "texto": "Ministério cristão dedicado à Palavra de Deus, ao discipulado, à intercessão, à formação de líderes e às missões.",
        "frentes": ["História do ministério.", "Presidência Apostólica.", "Declaração de fé.", "Estrutura mundial.",
                    "Coordenações continentais.", "Supervisões nacionais.", "Igrejas locais.", "Ministérios e departamentos."],
    },
]

CONTEUDO_CATEGORIAS = ["Fé e espiritualidade.", "Restauração emocional.", "Psicanálise e desenvolvimento humano.",
                       "Liderança e gestão.", "Mulheres e propósito.", "Educação e formação.", "Missões e ministério."]
CONTEUDO_ESPACO = ["Artigos e reflexões.", "Estudos bíblicos.", "Desenvolvimento humano.", "Inteligência emocional.",
                   "Liderança e gestão.", "Vídeos e entrevistas.", "Devocionais.", "Materiais educacionais."]
EVENTO_TIPOS = ["Congressos.", "Seminários.", "Conferências.", "Palestras.", "Cursos.", "Encontros de mulheres.", "Eventos missionários."]

CONTATO_MOTIVOS = ["Solicitação de palestras.", "Convites para eventos.", "Propostas de parcerias.",
                   "Consultorias e treinamentos.", "Informações sobre cursos e mentorias."]

# público -> objetivo (seção 8 do briefing)
PUBLICOS = [
    ("Empresas", "Contratar palestras e treinamentos", "/palestras"),
    ("Mulheres", "Conhecer mentorias e projetos", "/mentorias"),
    ("Líderes", "Acessar conteúdos e formações", "/conteudos"),
    ("Igrejas", "Solicitar convites e cooperação", "/contato"),
    ("Estudantes", "Conhecer cursos e materiais", "/mentorias#formacoes"),
    ("Instituições", "Desenvolver parcerias", "/contato"),
    ("Público geral", "Conhecer a trajetória de Karla", "/sobre-karla"),
]

ENCERRAMENTO = [
    "Não se trata apenas de construir uma história, mas de transformar conhecimento, fé e propósito em instrumentos de impacto.",
    "Karla Messias acredita que pessoas restauradas podem construir novas histórias, líderes preparados podem transformar ambientes e instituições comprometidas podem gerar mudanças duradouras na sociedade.",
]
TRIADE = ["Fé para acreditar.", "Conhecimento para transformar.", "Liderança para impactar."]

BIO = [
    "Karla Patrícia Messias Pereira, conhecida publicamente como Karla Messias, é Administradora, Teóloga, Psicanalista Clínica, Mentora, Palestrante e Apóstola. Sua trajetória reúne experiências nas áreas de gestão, educação, desenvolvimento humano, liderança cristã, aconselhamento e mobilização missionária.",
    "Presidente do Instituto Âncora, Presidente do Conselho Mundial do SISADICA, Sistema de Ensino Teológico e de Missões, e Pastora Presidente da Assembleia de Deus Internacional Casa da Aliança, desenvolve iniciativas que integram conhecimento, fé, liderança e transformação social.",
    "É também idealizadora e líder espiritual dos movimentos Impacto Missionário RECONSTRUÍDE, Princesas Virtuosas e Sacerdócio Real.",
    "Sua atuação é fundamentada na convicção de que o conhecimento amplia possibilidades, a restauração transforma trajetórias e a liderança responsável gera impacto na sociedade.",
]

LIDERANCA_INSTITUCIONAL = [
    ("Instituto Âncora", "Presidente"),
    ("SISADICA, Sistema ADICA de Ensino Teológico e de Missões", "Presidência do Conselho Mundial"),
    ("Assembleia de Deus Internacional Casa da Aliança", "Pastora Presidente"),
    ("COMMADICA, Conselho Mundial de Ministros e Ministérios ADICA", "Apóstola Presidente e Liderança Espiritual"),
    ("Conselho Mundial RECONSTRUIDE", "Presidência Mundial"),
]

# Plancenter: empresa de consultoria da Karla (mandou depois, 03/11 17:12, "esqueci de mencionar")
PLANCENTER = {
    "nome": "Plancenter", "papel": "Consultoria & Projetos",
    "texto": "A Plancenter oferece soluções em planejamento, projetos, gestão, consultoria, branding, mentoria e capacitação.",
    "frase": "Onde suas ideias se transformam em projetos bem-sucedidos.",
    "url": "https://plancenter.vercel.app",
}
