# -*- coding: utf-8 -*-

import os
import re


def valida_data(data):
    if data not in (1,2,3,4,5):
        raise ValueError()


def valida_hora(hora):
    if (hora < 0 or hora > 23):
        raise ValueError()


def valida_minuto(minuto):
    if (minuto < 0 or minuto > 59):
        raise ValueError()


def valida_turma(turma):
    if not isinstance(turma, str):
        raise TypeError('Turma precisa ser um caractere("str")')
    turmas = ('1', '2', '3')
    if turma not in turmas:
        raise ValueError('Turma precisa ser uma das: (1,2,3)')


def valida_matricula(matricula):
    if not isinstance(matricula, str):
        raise TypeError('Matrícula precisa ser uma String')
    regex = re.compile('\d{1,9}\Z')
    if not (regex.match(matricula) and len(matricula) == 9):
        raise ValueError('Sua matrícula precisa ter 9 dígitos')


def valida_path(path):
    return False if (not os.path.isdir(path) or path.strip() == '') else True


def valida_nome(nome):
    return False if nome.strip() == '' else True


def valida_turma(turma):
    return True if turma in ('1', '2', '3') else False  


def write_error(mensagem):
    return ('\033[31m' + mensagem + '\033[0;0m')


def write_success(mensagem):
    return ('\33[32m' + mensagem + '\033[0;0m')


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
        raise ValueError('roteiro precisa ter o seguinte formato: R03-02'
        + ' ou PP2-3 por exemplo')