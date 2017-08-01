[![PyPI](https://img.shields.io/badge/pypi-1.1.0-blue.svg)](https://pypi.python.org/pypi/automated)
[![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)](https://pypi.python.org/pypi/automated)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/gabrielfern/automated-leda-tasks/master/LICENSE)

# Automatizador de tarefas leda

  # Para que serve

    Evitar a repeticao constante dos mesmos passos a cada roteiro,
    simplificando todos os processos incluindo a primeira submissao,
    resumindo-se a um unico comando, possibilitando agendamento junto
    ao sistema operacional para automatizar por completo sem necessidade
    fisica de estar junto a um computador

  # Funcoes principais

    - Download de roteiro em versao zip
    - Unzip e alocacao em pasta pre configurada
    - Escreve no pom.xml as informacoes necessarias
    - Realiza compilacao com maven (com skip de testes)

  # Dependencias

    - python (em versoes 2.x ou 3.x)
    - mvn (maven versao linha de comando)
    - pip (gerenciador de pacotes python, recomendavel)
    - requests (biblioteca externa de python, pip instala automaticamente)
    - sistema linux/mac (interacao com interface de comando baseada em bash)

  # Para instalar

    pip install --user automated

  # Para rodar

    python -m automated

  # Para ajuda

    python -m automated help
