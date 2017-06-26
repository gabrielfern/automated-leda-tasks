#!/usr/bin/python3
# Gabriel Fernandes <gabrielfernndss@gmail.com>

import re
import os
import sys
import requests


turma = '3'
matricula = '116110409'
path = '/home/fernandes/leda-roteiros/'

USAGE = '''Specify the folder to looking for pom.xml and the 'roteiro number' 
            like this: python3 autoit.py /path/to/pom/ 5'''

MATRICULA_PATTERN = re.compile('INSIRA SEU NUMERO DE MATRICULA')
ROTEIRO_PATTERN = re.compile('R0.-0.')


def valida_turma(turma):
    if not isinstance(turma, str):
        raise TypeError('turma precisa ser um caractere("str")')
    turmas = ('1', '2', '3')
    if turma not in turmas:
        raise ValueError('turma precisa ser uma das: (1,2,3)')


def valida_matricula(matricula):
    if not isinstance(matricula, str):
        raise TypeError('matricula precisa ser uma "str"')
    regex = re.compile('\d{1,9}')
    if not regex.fullmatch(matricula):
        raise ValueError('matricula precisa ser do tipo xxxxxxxxx, onde x é um digito(1-9)')


def valida_path(path):
    if not isinstance(path, str):
        raise TypeError('insira um caminho("path") de diretorio valido')
    if not os.path.isdir(path):
        raise TypeError('path precisa ser passado como uma "str')


def set_up_turma(_turma):
    global turma
    valida_turma(_turma)
    turma = _turma


def set_up_matricula(_matricula):
    global matricula
    valida_matricula(_matricula)
    matricula = _matricula


def set_up_path(_path):
    global path
    valida_path(_path)
    path = os.path.abspath(_path)


def main():
    if len(sys.argv) < 3:
        print(USAGE)
        sys.exit(1)
    else:
        new_path = path + sys.argv[1]
        roteiro = 'R0' + sys.argv[2] + '-0' + turma

    data = None
    with open(new_path + '/pom.xml', 'r') as pom:

        data = pom.read()
        data = MATRICULA_PATTERN.sub(matricula, data)
        data = ROTEIRO_PATTERN.sub(roteiro, data)

    if data != None:
        with open(new_path + '/pom.xml', 'w') as pom:
            pom.write(data)

    print('...done!')


if __name__ == '__main__':
    main()
