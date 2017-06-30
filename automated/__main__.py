#!/usr/bin/python3
# Gabriel Fernandes <gabrielfernndss@gmail.com>
# os.system('python3 -m pip install --user requests')
# print(os.path.dirname(os.path.abspath(__file__)))

import os
import re
import sys
import json
from . import autoit
from . import retrievedata


"""
Aparentemente funcional,
nao testado na pratica ainda...
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
    with open(os.path.join(HERE, 'personalinfo.json')) as data:
        return json.load(data)


def main():
    try:
        if 'personalinfo.json' not in os.listdir(HERE):
            set_up()
        else:
            data = get_personal_info()
            roteiro = retrievedata.match_roteiro(data['turma'])

            if roteiro:
                retrievedata.get_roteiro_zip(HERE, roteiro, data['turma'])
                autoit.extract_zip(os.path.join(HERE, roteiro), roteiro[0:3])
                autoit.write_pom(os.path.join(HERE, roteiro[0:3]), data['matricula'], roteiro)
                autoit.move_folder(os.path.join(HERE, roteiro[0:3]), data['path'])
                autoit.mvn_commit(os.path.join(data['path'], roteiro[0:3]))

    except KeyboardInterrupt:
        print('\nSaindo...')
        sys.exit(1)


if __name__ == '__main__':
    main()