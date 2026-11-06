"""Currículo da Karla Messias: fonte única do PDF (tools/curriculo_pdf.py) e da página /curriculo (build.py).

Texto dela, à risca. Só muda a tipografia: caixa-alta vira estilo e o travessão que separava nome e UF vira vírgula.
O e-mail dela fica fora daqui de propósito: o repo é público e o site não mostra e-mail. Ver tools/curriculo_pdf.py.
"""

NOME = "Karla Patrícia Messias Pereira"
TITULOS = "Administradora | Empresária | Consultora | Gestora Institucional"
LOCAL = "Brasília, DF"
TELEFONE = "(61) 99397-3723"
SITE = "www.karlamessias.com"

PERFIL = [
    "Administradora, empresária e consultora, com experiência multidisciplinar em gestão pública e privada, empreendedorismo, planejamento institucional, assessoria administrativa, elaboração e gerenciamento de projetos, captação de recursos e gestão de convênios.",
    "Possui trajetória profissional junto a órgãos públicos, prefeituras, empresas, associações e entidades do terceiro setor, com atuação em diferentes áreas da administração, gestão organizacional e desenvolvimento institucional.",
    "Experiência em planejamento estratégico e operacional, organização de processos administrativos, acompanhamento orçamentário, gestão de contratos e convênios, elaboração de propostas, articulação institucional e operacionalização de sistemas governamentais.",
    "Como empreendedora, atua na direção e desenvolvimento de iniciativas empresariais e institucionais, reunindo visão sistêmica, capacidade de liderança, comunicação, organização, análise e resolução de problemas.",
]

COMPETENCIAS = [
    "Administração e gestão organizacional",
    "Gestão pública e privada",
    "Empreendedorismo e gestão empresarial",
    "Planejamento estratégico e operacional",
    "Gestão financeira e acompanhamento orçamentário",
    "Consultoria empresarial e institucional",
    "Assessoria administrativa e técnica",
    "Elaboração, análise e gerenciamento de projetos",
    "Captação de recursos públicos e privados",
    "Gestão de contratos, convênios e parcerias",
    "Programas e políticas públicas",
    "Articulação institucional e governamental",
    "Estruturação de associações e entidades sem fins lucrativos",
    "Organização e desenvolvimento de equipes",
    "Planejamento de eventos e capacitações",
    "Comunicação institucional e produção de conteúdo",
]

NOTA_EXPERIENCIA = "Organizada em ordem cronológica decrescente, considerando o período de encerramento dos vínculos."

EXPERIENCIA = [
    {"org": "Instituto Âncora", "papel": "Diretora-Presidente", "periodo": "2025–Atual", "itens": [
        "Direção institucional e acompanhamento das atividades administrativas e organizacionais.",
        "Planejamento e desenvolvimento de projetos institucionais, sociais e educacionais.",
        "Articulação de parcerias e iniciativas voltadas ao desenvolvimento humano e social.",
        "Estruturação de programas, projetos e ações de alcance institucional.",
    ]},
    {"org": "Instituto Travessia", "papel": "Diretora de Projetos", "periodo": "2013–2018", "itens": [
        "Direção e acompanhamento de projetos institucionais.",
        "Planejamento, organização e desenvolvimento de iniciativas e ações.",
        "Articulação institucional e acompanhamento das atividades relacionadas aos projetos.",
    ]},
    {"org": "Prefeitura Municipal de São Mateus do Maranhão, MA", "papel": "Assessora Técnica", "periodo": "2017", "itens": [
        "Atuação em assessoria técnica no âmbito da administração municipal.",
        "Apoio às atividades de planejamento e acompanhamento de demandas institucionais.",
    ]},
    {"org": "Associação Tocantinense de Municípios (ATM)", "papel": "Diretora de Projetos", "periodo": "2013", "itens": [
        "Atuação na direção e no desenvolvimento de projetos institucionais.",
        "Acompanhamento de iniciativas e demandas relacionadas à gestão municipal.",
    ]},
    {"org": "Prefeitura Municipal de Avelino Lopes, PI", "papel": "Especialista em Educação", "periodo": "2013", "itens": [
        "Atuação técnica especializada na área educacional.",
        "Apoio às atividades e demandas relacionadas à gestão da educação municipal.",
    ]},
    {"org": "Prefeitura Municipal de Madeiro, PI", "papel": "Secretária Municipal de Educação", "periodo": "07/2011–09/2012", "itens": [
        "Gestão e acompanhamento das atividades da Secretaria Municipal de Educação.",
        "Acompanhamento de programas e sistemas do FNDE e de propostas cadastradas no SIMEC.",
        "Diagnóstico e elaboração do Plano de Ações Articuladas (PAR).",
        "Acompanhamento e regularização de Conselhos Escolares.",
        "Desenvolvimento e acompanhamento de programas como PDDE, PDE e Mais Educação.",
        "Cadastramento e acompanhamento de programas educacionais ofertados pelo FNDE/MEC.",
        "Elaboração e organização de documentos institucionais, regimentos e propostas pedagógicas.",
        "Acompanhamento de propostas e projetos relacionados à educação e a outras áreas de interesse municipal.",
    ]},
    {"org": "Gabinete do Senador Mão Santa", "papel": "Assistente Parlamentar", "periodo": "2010–2011", "itens": [
        "Apoio às atividades parlamentares e administrativas do gabinete.",
        "Organização e acompanhamento de demandas institucionais.",
        "Suporte administrativo e atendimento às demandas relacionadas à atuação parlamentar.",
    ]},
    {"org": "Senado Federal, Terceira Secretaria", "papel": "Assistente Parlamentar", "periodo": "2008–2010", "itens": [
        "Elaboração e organização de ofícios, documentos e planilhas orçamentárias.",
        "Acompanhamento de projetos e demandas junto às comissões.",
        "Apoio à elaboração e ao acompanhamento de emendas parlamentares e projetos vinculados ao Orçamento Geral da União (OGU).",
        "Assessoria a gestores municipais e acompanhamento de demandas de interesse dos municípios.",
        "Operacionalização e acompanhamento de informações em sistemas governamentais.",
    ]},
]

PLANCENTER = {"org": "Plancenter Consultoria & Projetos", "papel": "Fundadora e Empresária | Gestão Executiva e Consultoria", "itens": [
    "Criação, direção e desenvolvimento da empresa, voltada à consultoria, planejamento e desenvolvimento de projetos.",
    "Gestão e organização das atividades empresariais e administrativas.",
    "Consultoria em gestão organizacional, planejamento estratégico e estruturação de negócios.",
    "Desenvolvimento e elaboração de projetos institucionais e empresariais.",
    "Apoio à organização administrativa e ao planejamento de iniciativas e soluções para organizações públicas e privadas.",
]}

ESTADOS = ["Piauí", "Maranhão", "Tocantins", "Goiás", "Pernambuco", "Minas Gerais", "Ceará"]

CONSULTORIA = {
    "org": "Consultoria e Assessoria a Prefeituras e Órgãos Públicos",
    "papel": "Gestão Pública | Projetos | Convênios | Captação de Recursos",
    "texto": "Atuação junto a municípios e órgãos públicos dos estados do Piauí, Maranhão, Tocantins, Goiás, Pernambuco, Minas Gerais e Ceará.",
    "rotulo": "Principais atividades:",
    "itens": [
        "Assessoria técnica e administrativa a gestores e equipes municipais.",
        "Elaboração, cadastramento, acompanhamento e gerenciamento de projetos governamentais.",
        "Assessoria na captação de recursos federais e estaduais.",
        "Acompanhamento de convênios, contratos e instrumentos de repasse.",
        "Orientação sobre programas e sistemas governamentais.",
        "Apoio à elaboração de propostas nas áreas de saúde, educação, assistência social, cultura, esporte, infraestrutura e meio ambiente.",
        "Atuação como GMC, Gerente Municipal de Contratos e Convênios, junto à Caixa Econômica Federal.",
    ],
}

TERCEIRO_SETOR = {
    "org": "Associações e Entidades do Terceiro Setor",
    "papel": "Consultoria, Estruturação Institucional e Desenvolvimento de Projetos",
    "itens": [
        "Apoio à organização e estruturação de associações, entidades sem fins lucrativos, cooperativas e organizações sociais.",
        "Elaboração de estatutos, regimentos e documentos organizacionais.",
        "Desenvolvimento de projetos sociais, educacionais e comunitários.",
        "Apoio à captação de recursos e formalização de parcerias.",
        "Organização de capacitações, seminários e eventos institucionais.",
    ],
}

COMPLEMENTARES = [
    {"org": "Prefeitura Municipal de Balsas, MA", "papel": "Diretora de Divisão de Dança e Incentivo ao Folclore", "itens": [
        "Organização, promoção e incentivo a atividades culturais.",
        "Desenvolvimento de ações de valorização da cultura e das manifestações folclóricas.",
    ]},
    {"org": "Jornal O Dia, Balsas/MA", "papel": "Editora-Chefe de Redação | Repórter | Designer", "itens": [
        "Produção jornalística e organização editorial.",
        "Elaboração e edição de matérias.",
        "Desenvolvimento de materiais gráficos e comunicação.",
    ]},
    {"org": "Jornal Rural, São Luís/MA", "papel": "Editora-Chefe | Repórter | Designer", "itens": [
        "Produção e edição de conteúdo jornalístico.",
        "Organização editorial e comunicação.",
        "Desenvolvimento de materiais editoriais.",
    ]},
]

FORMACAO = ["Bacharelado em Administração", "Formação em Psicanálise Clínica", "Curso Técnico em Enfermagem"]

SISTEMAS_TEXTO = "Experiência com sistemas e ferramentas utilizados na gestão pública, acompanhamento de programas, propostas, convênios e recursos governamentais:"
SISTEMAS = ["SICONV", "SIMEC/FNDE", "FNS", "FUNASA", "SIGPC", "SIAFI", "SIGOB", "Sistemas de acompanhamento de propostas e programas governamentais"]

CAPACITACOES = [
    "Licitações e contratos administrativos",
    "Elaboração e gerenciamento de projetos",
    "Captação de recursos",
    "Gestão de convênios e contratos",
    "Cálculos trabalhistas",
    "Finanças pessoais",
    "Plano Local de Habitação de Interesse Social (PLHIS)",
    "Operacionalização de sistemas governamentais",
    "Informática",
    "Web design",
    "Rotinas administrativas",
]
# Na página do site ficam só as ligadas à gestão pública; a lista inteira segue no PDF.
CAPACITACOES_SITE = [c for c in CAPACITACOES if c not in {"Cálculos trabalhistas", "Finanças pessoais", "Informática", "Web design", "Rotinas administrativas"}]

# Bloco da /sobre-karla: os fatos de maior peso, com as palavras do currículo.
DESTAQUES = [
    ("Senado Federal, Terceira Secretaria", "Assistente Parlamentar"),
    ("Prefeitura Municipal de Madeiro, PI", "Secretária Municipal de Educação"),
    ("Plancenter Consultoria & Projetos", "Fundadora e Empresária"),
    ("Consultoria a prefeituras e órgãos públicos", "Piauí, Maranhão, Tocantins, Goiás, Pernambuco, Minas Gerais e Ceará"),
]

DIFERENCIAIS = [
    "Experiência em diferentes estruturas organizacionais e segmentos profissionais.",
    "Conhecimento prático dos processos da Administração Pública e da dinâmica municipal.",
    "Experiência em empreendedorismo, gestão empresarial e desenvolvimento institucional.",
    "Capacidade de planejamento, organização, análise e resolução de problemas.",
    "Experiência na articulação com gestores públicos, equipes técnicas, instituições e organizações sociais.",
    "Capacidade de estruturar projetos e transformar demandas institucionais em propostas organizadas.",
    "Perfil proativo, estratégico, comunicativo e orientado a resultados.",
]

OBJETIVO = "Atuar em organizações públicas ou privadas, instituições, empresas e entidades do terceiro setor, contribuindo com minha experiência em Administração, gestão pública e privada, empreendedorismo, consultoria, planejamento institucional, projetos e desenvolvimento organizacional, agregando conhecimento técnico, capacidade de articulação, liderança e compromisso com resultados."
