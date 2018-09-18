[![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)](https://pypi.python.org/pypi/automated)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/gabrielfern/automated-leda-tasks/master/LICENSE)

# Automatizador de tarefas - LEDA

  # Para que serve?

    Evitar a repetição constante dos mesmos passos a cada roteiro,
    simplificando todos os processos, incluindo a primeira submissão,
    resumindo-se a um único comando, possibilitando agendamento junto
    ao sistema operacional para automatizar por completo sem necessidade
    física de estar junto a um computador

  # Funções principais

    - Download de roteiro em versão zip
    - Unzip e alocação em pasta pré configurada
    - Escreve no pom.xml as informações necessárias
    - Realiza compilação com maven (com skip de testes)

  # Dependências

    - python (em versões 2.x ou 3.x)
    - mvn (maven versão linha de comando)
    - sistema linux/mac (interação com interface de comando baseada em bash)
    - pip (gerenciador de pacotes python, instala dependências internas automaticamente)

  # Instalar

    pip install --user automated

    ou (a partir desse repositório clonado)

    python setup.py install --user

  # Executar

    python -m automated

  # Ajuda

    python -m automated help
