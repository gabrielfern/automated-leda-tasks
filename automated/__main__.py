#!/usr/bin/python
# Gabriel Fernandes <gabrielfernndss@gmail.com>


from __future__ import print_function

import os
import re
import sys
import json
import shutil
from pprint import pprint

py_version = sys.version_info.major

if py_version == 2:
    import autoit
    import retrievedata

    input = raw_input

else:
    from . import autoit
    from . import retrievedata


"""
Controla as funcionalidades
principais
"""


HERE = os.path.dirname(os.path.abspath(__file__))


def set_up():
    data = {}
    validado = False
    print('Primeiro uso detectado...')
    print('...comecando configuracao')

    while True:
        data['nome'] = input('Digite seu nome: ')
        if data['nome'].strip == '':
            print('Voce precisa ter um nome')
            continue
        break

    while True:
        data['turma'] = input('Digite sua turma(1, 2 ou 3): ')
        if data['turma'] not in ('1', '2', '3'):
            print('Sua turma precisa ser 1, 2 ou 3')
            continue
        break

    while True:
        matricula_regex = re.compile(r'\d{9}')
        data['matricula'] = input('Numero de matricula: ')
        if matricula_regex.match(data['matricula']) == None:
            print('Sua matricula precisa ter 9 digitos')
            continue
        break

    while True:
        data['path'] = input('Caminho completo ate sua pasta com roteiros: ')
        if data['path'].strip() == '' or not os.path.isdir(data['path']):
            print('Voce precisa especificar um caminho para sua pasta')
            continue
        validado = True
        break

    if validado:
        with open(os.path.join(HERE, 'personalinfo.json'), 'w') as arq:
            json.dump(data, arq, indent=2)
        print('\nConfiguracao efetuada com sucesso!')


def get_personal_info():
    try:
        FileNotFoundError
    except NameError:
        FileNotFoundError = IOError

    try:
        with open(os.path.join(HERE, 'personalinfo.json')) as data:
            if py_version == 2:
                return {a.encode('utf-8'):b.encode('utf-8') for a, b in json.load(data).items()}
            return json.load(data)

    except FileNotFoundError:
        return 'configuracao ainda nao realizada'


def main():
    try:
        if 'personalinfo.json' not in os.listdir(HERE):
            set_up()
            main()
        else:
            if len(sys.argv) > 1:
                command = sys.argv[1]

                if command == 'info':
                    pprint(get_personal_info())
                elif command == 'hora':
                    print(retrievedata.get_hora_atual())
                elif command == 'reset':
                    print(autoit.reset_config(HERE))
                elif command == 'hoje':
                    print(retrievedata.get_roteiro_today(get_personal_info()['turma']))
                elif command == 'cronograma':
                    pprint(retrievedata.req_crono(get_personal_info()['turma']))
                else:
                    print('Como usar',
                                '\n\tsempre que tiver um roteiro para fazer, rode como um modulo python',
                                '\n\te confira na pasta que configurou como a de roteiros',
                                '\n\t(o opcional "-m" para o python significa que voce que rodar como modulo)',
                                '\n\ttambem possivel utilizar sem a etapa de instalacao, para isso',
                                '\n\tclone o repositorio no github e sempre que quiser rodar',
                                '\n\tse dirija ate a pasta automated-leda-tasks e rode como modulo python',
                            '\nInstalar',
                                '\n\tpip install --user automated',
                            '\nRodar',
                                '\n\tpython -m automated',
                                '\n\t(necessario somente essa linha para realizar todo o servico)',
                                '\n\tpython -m automated [opcional]',
                                '\n\t(ou funcionalidades extras com algum opcional)',
                            '\nTambem possivel utilizar de outras aplicacoes',
                                '\n\tfrom automated import [__main__ | autoit | retrievedata]',
                            '\nOpcionais validos via linha de comando',
                                '\n\thelp::          mostra essa mensagem',
                                '\n\thora::          exibe hora segundo o servidor',
                                '\n\thoje::          mostra se existe roteiro para hoje',
                                '\n\tinfo::          exibe informacoes configuradas',
                                '\n\treset::         reseta configuracoes',
                                '\n\tcronograma::    exibe todos os roteiros do periodo'
                        )

            else:
                data = get_personal_info()
                roteiro = retrievedata.match_roteiro(data['turma'])

                if roteiro:
                    print('Roteiro %s disponivel, pegando ele para voce...\n' %s)
                    retrievedata.get_roteiro_zip(HERE, roteiro, data['matricula'])
                    autoit.extract_zip(os.path.join(HERE, roteiro + '.zip'), os.path.join(HERE, roteiro[0:3]))
                    autoit.rm_zips(HERE)
                    autoit.write_pom(os.path.join(HERE, roteiro[0:3]), data['matricula'], roteiro)
                    try:
                        autoit.move_folder(os.path.join(HERE, roteiro[0:3]), data['path'])
                    except shutil.Error as e:
                        autoit.rm_folders(HERE)

                    print('...enviando com o maven...\n')
                    autoit.mvn_commit(os.path.join(data['path'], roteiro[0:3]))
                    print('...trabalho acabado por aqui, roteiro %s' %roteiro,
                            '\nencontra-se em %s' %(data['path'] + roteiro[0:3]))
                else:
                    print('...sem roteiros disponiveis no momento')

    except KeyboardInterrupt:
        print('\nSaindo...')
        sys.exit(1)


if __name__ == '__main__':
    main()
