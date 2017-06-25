#!/usr/bin/python3
# Gabriel Fernandes <gabrielfernndss@gmail.com>
# os.system('python3 -m pip install --user requests')
import os
import re
import sys
import json
from . import autoit


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
        
        data['turma'] = input('Digite sua turma(1, 2 ou 3): ')
        if data['turma'] not in (1,2,3):
            print('Sua turma precisa ser 1, 2 ou 3')
            continue
        
        matricula_regex = re.compile(r'\d{9}')
        data['matricula'] = input('Numero de matricula: ')
        if matricula_regex.match(data['matricula']) == None:
            print('Sua matricula precisa ter 9 digitos')
            continue
        
        data['path'] = input('Caminho completo ate sua pasta com roteiros: ')
        if data['path'].strip() == '':
            print('Voce precisa especificar um caminho para sua pasta')
            continue
        validado = True
        break
    
    if validado:
        with open('personalinfo.json', 'w') as arq:
            json.dump(data, arq)


def main():
    try:
        with open('personalinfo.json') as arq:
            data_dict = json.load(arq)
            autoit.main(data_dict['path'],
                        data_dict['turma'],
                        data_dict['matricula'],)
            
    except FileNotFoundError:
        set_up()


if __name__ == '__main__':
    main()
