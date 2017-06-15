#!/usr/bin/python3

import sys
import re

TURMA = '03'
MATRICULA = '116110409'
PATH = '/home/fernandes/leda-roteiros/'

USAGE = '''Specify the sub-folder to looking for pom.xml
            like this: python3 autoit.py R05 5'''

MATRICULA_PATTERN = re.compile('INSIRA SEU NUMERO DE MATRICULA')
ROTEIRO_PATTERN = re.compile('R0X-0X')

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
