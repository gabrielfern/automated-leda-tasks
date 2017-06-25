#!/usr/bin/python3
# Gabriel Fernandes <gabrielfernndss@gmail.com>

import re
import sys
import json
import pprint
import datetime
import requests


"""
Access the server and retrieves
some useful data
"""


URLS = ('http://150.165.85.29:81/cronograma',
        'http://150.165.85.29:81/horaAtual')
turma = '3'


def make_pattern(turma):
    return re.compile('''(?:P[PRF][1-3]|R[01]\d)-0''' + turma
                    + '''\s*<td\s*class="text-xs-center"\s*data-toggle="tooltip"\s*data-placement="right"\s*title='Atividade'''
                    + '''\s*inicia\s*em\s*\d\d/\d\d/2017\s*\d\d:\d\d''')


def valida_requisicao(req):
    try:
        req.raise_for_status()
    except requests.exceptions.HTTPError as http_error:
        print(http_error)
        sys.exit(1)


def make_datetime(datetime_tuple):
    ano = int(datetime_tuple[0][6:10])
    mes = int(datetime_tuple[0][3:5])
    dia = int(datetime_tuple[0][0:2])
    hora = int(datetime_tuple[1][0:2])
    minutos = int(datetime_tuple[1][3:5])
    return datetime.datetime(ano, mes, dia, hora, minutos)


def get_roteiro_today():
    today = get_datetime_atual()
    all_roteiros = get_roteiros()
    for k in all_roteiros:
        if today.date() == all_roteiros[k].date():
            return k
    print('Sem roteiros por hoje...')
    sys.exit(0)


def req_crono():
    req = requests.get(URLS[0])
    valida_requisicao(req)

    all_roteiros = make_pattern(turma).findall(req.text)
    roteiros = []
    dates = []
    horas = []
    for i in range(len(all_roteiros)):
        roteiros.append(all_roteiros[i][:6])
        dates.append(all_roteiros[i][-16:-6])
        horas.append(all_roteiros[i][-1:-6:-1][::-1])
    
    all_roteiros = {a:(b,c) for a, b, c in ((roteiros[i], dates[i], horas[i]) for i in range(len(roteiros)))}
    return all_roteiros


def get_roteiros():
    all_roteiros = req_crono()
    for k in all_roteiros:
        all_roteiros[k] = make_datetime(all_roteiros[k])
    return all_roteiros


def req_date_hora():
    req = requests.get(URLS[1])
    valida_requisicao(req)
    return req.text


def get_datetime_atual():
    return make_datetime((get_date_atual(), get_hora_atual()))


def get_date_atual():
    return req_date_hora()[-19:-9]


def get_hora_atual():
    return req_date_hora()[-8:-3]


def set_up_turma(_turma):
    global turma
    if isinstance(_turma, str):
        turmas = ('1', '2', '3')
        if _turma in turmas:
            turma = _turma
        else:
            raise ValueError('turma precisa ser uma das: (1,2,3)')
    else:
        raise TypeError('turma precisa ser um caractere("str")')


def main():
    global turma
    if len(sys.argv) > 1:
        turma = sys.argv[1]
    pprint.pprint(req_crono())


if __name__ == '__main__':
    main()
