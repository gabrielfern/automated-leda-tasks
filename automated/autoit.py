#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Gabriel Fernandes <gabrielfernndss@gmail.com>
# Héricles Emanuel <hericles.me@gmail.com>

from crontab import CronTab

import re
import os
import sys
import util
import shutil
import zipfile

py_version = sys.version_info.major

if py_version == 2:
    import retrievedata
else:
    from . import retrievedata


"""
Algumas funcões de
utilidade na automatizacao
"""


MATRICULA_PATTERN = re.compile('INSIRA SEU NUMERO DE MATRICULA')
ROTEIRO_PATTERN = re.compile('R0.-0.')
DAY = '\n\r[1] - Segunda \n\r[2] - Terca \n\r[3] - Quarta \n\r[4] - Quinta \n\r[5] - Sexta\n\r'
CRON = CronTab(user=True)


def write_error(mensagem):
    print('\033[31m' + mensagem + '\033[0;0m')


def write_success(mensagem):
    print('\33[32m' + mensagem + '\033[0;0m')


def clear_data():
    this = ['python', '-m', 'automated']
    for job in CRON:
        if (str(job).split()[-3:] == this):
            CRON.remove(job)
    CRON.write()


def agendar_submissao():
    print(DAY)

    while True:
        try:
            data = int(input('Escolha o dia da Submissão: '))
            util.valida_data(data)
            break
        except ValueError:
            write_error('Dia precisa ser um valor entre 1 e 5')

    while True:
        try:
            hora = int(input('Escolha a hora da Submissão (Formato 24h): '))
            util.valida_hora(hora)
            break
        except ValueError:
            write_error('Hora precisa ser um valor entre 0 e 23')

    while True:
        try:
            minuto = int(input('Escolha o minuto da Submissão: '))
            util.valida_minuto(minuto)
            break
        except ValueError:
            write_error('Minuto precisa ser um valor entre 0 e 59')

    dias = {'1':'MON', '2': 'TUE', '3': 'WED', '4': 'THU', '5': 'FRI'}
    job  = CRON.new(command='python -m automated')
    job.dow.on(dias[str(data)])
    job.hour.also.on(hora)
    job.minute.also.on(minuto)
    job.enable()
    CRON.write()
    write_success('Submissão agendada com Sucesso')

def write_pom(path, matricula, roteiro):
    util.valida_path(path)
    util.valida_matricula(matricula)
    retrievedata.util.valida_roteiro(roteiro)

    data = None
    with open(path + '/pom.xml', 'r') as pom:
        data = pom.read()
        data = MATRICULA_PATTERN.sub(matricula, data)
        data = ROTEIRO_PATTERN.sub(roteiro, data)

    if data != None:
        with open(path + '/pom.xml', 'w') as pom:
            pom.write(data)


def extract_zip(zip, folder):
    util.valida_path(os.path.dirname(os.path.abspath(zip)))
    util.valida_path(os.path.dirname(os.path.abspath(folder)))

    with zipfile.ZipFile(zip) as zp:
        zp.extractall(folder)


def move_folder(folder, path):
    util.valida_path(folder)
    util.valida_path(path)

    shutil.move(folder, path)


def mvn_commit(path):
    util.valida_path(path)

    os.system('cd %s && mvn install -DskipTests' %path)


def rm_zips(path):
    util.valida_path(path)

    zips = filter(lambda f: f.endswith('.zip'), os.listdir(path))
    zips = list(map(lambda f: os.path.join(path, f), zips))
    return len(list(map(lambda f: os.unlink(f), zips)))


def rm_folders(path):
    util.valida_path(path)

    folders = list(map(lambda f: os.path.join(path, f), os.listdir(path)))
    folders = filter(lambda f: os.path.isdir(f) and not f.endswith('__pycache__'), folders)
    return len(list(map(lambda f: shutil.rmtree(f), folders)))


def reset_config(path):
    clear_data()
    util.valida_path(path)

    try:
        os.unlink(os.path.join(path, 'personalinfo.json'))
        write_success('Configurações resetadas com sucesso')
    except FileNotFoundError:
        write_error('Configuraçao ainda não feita')


def main():
    args = sys.argv
    try:
        write_pom(args[1], args[2], args[3])
    except IndexError:
        print('''Uso: Passar caminho até a pasta em que se encontra o pom.xml,
            matrícula e roteiro na qual deseja-se preencher automaticamente no pom
            Exemplo: python3 autoit.py /home/fernandes/leda-roteiros 111110234 R03-03''')
        sys.exit(1)


if __name__ == '__main__':
    main()
