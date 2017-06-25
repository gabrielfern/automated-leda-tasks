#!/usr/bin/python3
# Gabriel Fernandes <gabrielfernndss@gmail.com>

import re
import sys
import requests


TURMA = '03'
MATRICULA = '116110409'
PATH = '/home/fernandes/leda-roteiros/'

USAGE = '''Specify the folder to looking for pom.xml and the 'roteiro number' 
            like this: python3 autoit.py /path/to/pom/ 5'''

MATRICULA_PATTERN = re.compile('INSIRA SEU NUMERO DE MATRICULA')
ROTEIRO_PATTERN = re.compile('R0.-0.')


def main():
    if len(sys.argv) < 3:
        print(USAGE)
        sys.exit(1)
    else:
        path = PATH + sys.argv[1]
        roteiro = 'R0' + sys.argv[2] + '-' + TURMA 

    data = None
    with open(path + '/pom.xml', 'r') as pom:

        data = pom.read()
        data = MATRICULA_PATTERN.sub(MATRICULA, data)
        data = ROTEIRO_PATTERN.sub(roteiro, data)

    if data != None:
        with open(path + '/pom.xml', 'w') as pom:
            pom.write(data)
        

    print('...done!')


if __name__ == '__main__':
    main()
