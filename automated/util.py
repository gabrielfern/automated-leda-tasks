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
