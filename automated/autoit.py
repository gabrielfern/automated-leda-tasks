#!/usr/bin/python3

import re
import sys
import requests

TURMA = '03'
MATRICULA = '116110409'
PATH = '/home/fernandes/leda-roteiros/'

USAGE = '''Specify the sub-folder to looking for pom.xml
            like this: python3 autoit.py R05 5'''

MATRICULA_PATTERN = re.compile('INSIRA SEU NUMERO DE MATRICULA')
ROTEIRO_PATTERN = re.compile('R0X-0X')
CRONOGRAMA_PATTERN = re.compile("""R[01]\d-03\s*<td\s*class="text-xs-center"\s*data-toggle="tooltip"\s*data-placement="right"\s*title='Atividade\s*inicia\s*em\s*\d\d/\d\d/2017\s*\d\d:\d\d'>\d\d/\d\d""")

URLS = ('http://150.165.85.29:81/cronograma',
        'http://150.165.85.29:81/horaAtual')


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


def connectserver():
    req = requests.get(URLS[0])
    horareq = requests.get(URLS[1])
    allroteiros = CRONOGRAMA_PATTERN.findall(req.text)
    dates = []
    horas = []
    roteirnums = []
    for i in range(len(allroteiros)):
        dates.append(allroteiros[i][-5:len(allroteiros[i])])
    for i in range(len(allroteiros)):
        roteirnums.append(allroteiros[i][:6])
    for i in range(len(allroteiros)):
        horas.append(allroteiros[i][-12:-7])
    
    hora = horareq.text[-8:-3]
    date = horareq.text[-19:-14]
    
    print(roteirnums, '\n')
    print(dates, '\n')
    print(horas, '\n')
    print(date)
    print(hora)


if __name__ == '__main__':
    connectserver()
