#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Gabriel Fernandes <gabrielfernndss@gmail.com>
# Héricles Emanuel <hericles.me@gmail.com>


import re
import os
import sys
import pprint
import datetime

import requests

py_version = sys.version_info.major

if py_version == 2:
    import autoit

else:
    from . import autoit


"""
Acesso ao servidor
"""


URLS = ('http://150.165.85.29:81/cronograma',
        'http://150.165.85.29:81/horaAtual',
        'http://150.165.85.29:81/download')


def make_pattern(turma):
    return re.compile('''(?:P[PRF][1-3]|R(?:0|1(?=[0-7]))\d)-0''' + turma
                    + '''\s*<td\s*class="text-xs-center"\s*data-toggle="tooltip"\s*data-placement="right"\s*title='Atividade'''
                    + '''\s*inicia\s*em\s*\d\d/\d\d/2017\s*\d\d:\d\d''')


def valida_requisicao(req):
    try:
        req.raise_for_status()
    except requests.exceptions.HTTPError as http_error:
        print(http_error)
        sys.exit(1)


def valida_roteiro(roteiro):
    if not isinstance(roteiro, str):
        raise TypeError('roteiro precisa ser uma "str"')
    regex = re.compile('(?:P[PRF][1-3]|R(?:0|1(?=[0-7]))\d)-0[1-3]\Z')
    if not regex.match(roteiro):
        raise ValueError('roteiro precisa ter o seguinte formato: R03-02 ou PP2-3 por exemplo')


def make_datetime(datetime_tuple):
    ano = int(datetime_tuple[0][6:10])
    mes = int(datetime_tuple[0][3:5])
    dia = int(datetime_tuple[0][0:2])
    hora = int(datetime_tuple[1][0:2])
    minutos = int(datetime_tuple[1][3:5])
    return datetime.datetime(ano, mes, dia, hora, minutos)


def get_roteiro_today(turma):
    today = get_datetime_atual()
    all_roteiros = get_roteiros(turma)
    for k in all_roteiros:
        if today.date() == all_roteiros[k].date():
            return k


def match_roteiro(turma):
    today = get_datetime_atual()
    all_roteiros = get_roteiros(turma)
    for k in all_roteiros:
        if today.date() == all_roteiros[k].date() and today.time() >= all_roteiros[k].time():
            return k


def req_crono(turma):
    req = requests.get(URLS[0])
    valida_requisicao(req)
    autoit.valida_turma(turma)

    all_roteiros = make_pattern(turma).findall(req.text)
    roteiros = []
    dates = []
    horas = []
    for i in range(len(all_roteiros)):
        roteiros.append(all_roteiros[i][:6])
        dates.append(all_roteiros[i][-16:-6])
        horas.append(all_roteiros[i][-1:-6:-1][::-1])

    all_roteiros = {str(a):(str(b), str(c)) for a, b, c in ((roteiros[i], dates[i], horas[i]) for i in range(len(roteiros)))}
    return all_roteiros


def get_roteiros(turma):
    all_roteiros = req_crono(turma)
    for k in all_roteiros:
        all_roteiros[k] = make_datetime(all_roteiros[k])
    return all_roteiros


def req_date_hora():
    req = requests.get(URLS[1])
    valida_requisicao(req)
    if py_version == 2:
        return req.text.encode('utf-8')
    else:
        return req.text


def get_datetime_atual():
    return make_datetime((get_date_atual(), get_hora_atual()))


def get_date_atual():
    return req_date_hora()[-19:-9]


def get_hora_atual():
    return req_date_hora()[-8:-3]


def get_roteiro_zip(path, roteiro, matricula):
    valida_roteiro(roteiro)
    autoit.valida_path(path)
    autoit.valida_matricula(matricula)

    data = {'id': roteiro,
            'matricula': matricula}
    req_roteiro = requests.post(URLS[2], data=data)
    valida_requisicao(req_roteiro)
    if req_roteiro.text.startswith('Matrícula'):
        raise ValueError('Matrícula não cadastrada')
    else:
        with open(os.path.join(path, roteiro + '.zip'), 'wb') as zp:
            zp.write(req_roteiro.content)


def main():
    if len(sys.argv) > 1:
        pprint.pprint(req_crono(sys.argv[1]))
    else:
        print('''Você precisa especificar a turma passando como argumento da linha de comando.
            Por exemplo: "python3 retrievedata.py 3" Sendo o argumento referente a uma das 3 turmas''')
        sys.exit(1)


if __name__ == '__main__':
    main()
