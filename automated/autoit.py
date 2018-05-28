#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Gabriel Fernandes <gabrielfernndss@gmail.com>
# Héricles Emanuel <hericles.me@gmail.com>

from crontab import CronTab

import re
import os
import sys
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
            valida_data(data)
            break
        except (TypeError, NameError):
            write_error('Data precisa ser um inteiro')
        except ValueError:
            write_error('Data precisa ser um valor entre 1 e 5')

    while True:
        try:
            hora = int(input('Escolha a hora da Submissão (Formato 24h): '))
            valida_hora(hora)
            break
        except (TypeError, NameError):
            write_error('Hora precisa ser um inteiro')
        except ValueError:
            write_error('Hora precisa ser um valor entre 0 e 24')
    dias = {'1':'MON', '2': 'TUE', '3': 'WED', '4': 'THU', '5': 'FRI'}
    job  = CRON.new(command='python -m automated')
    job.dow.on(dias[str(data)])
    job.hour.also.on(hora)
    job.minute.also.on(1)
    job.enable()
    CRON.write()
    write_success('Submissão agendada com Sucesso')


def valida_data(data):
    if not isinstance(data, int):
        raise TypeError()
    datas = (1,2,3,4,5)
    if data not in datas:
        raise ValueError()


def valida_hora(hora):
    if not isinstance(hora, int):
        raise TypeError()
    if (hora < 0 or hora > 24):
        raise ValueError()


def valida_turma(turma):
    if not isinstance(turma, str):
        raise TypeError('Turma precisa ser um caractere("str")')
    turmas = ('1', '2', '3')
    if turma not in turmas:
        raise ValueError('Turma precisa ser uma das: (1,2,3)')


def valida_matricula(matricula):
    if not isinstance(matricula, str):
        raise TypeError('matricula precisa ser uma "str"')
    regex = re.compile('\d{1,9}\Z')
    if not regex.match(matricula):
        raise ValueError('matricula precisa ser do tipo xxxxxxxxx, onde x eh um digito(1-9)')


def valida_path(path):
    if not isinstance(path, str):
        raise TypeError('Path precisa ser passado como uma "str"')
    if not os.path.isdir(path):
        raise TypeError('Insira um caminho("path") de diretório Válido')


def write_pom(path, matricula, roteiro):
    valida_path(path)
    valida_matricula(matricula)
    retrievedata.valida_roteiro(roteiro)

    data = None
    with open(path + '/pom.xml', 'r') as pom:
        data = pom.read()
        data = MATRICULA_PATTERN.sub(matricula, data)
        data = ROTEIRO_PATTERN.sub(roteiro, data)

    if data != None:
        with open(path + '/pom.xml', 'w') as pom:
            pom.write(data)


def extract_zip(zip, folder):
    valida_path(os.path.dirname(os.path.abspath(zip)))
    valida_path(os.path.dirname(os.path.abspath(folder)))

    with zipfile.ZipFile(zip) as zp:
        zp.extractall(folder)


def move_folder(folder, path):
    valida_path(folder)
    valida_path(path)

    shutil.move(folder, path)


def mvn_commit(path):
    valida_path(path)

    os.system('cd %s && mvn install -DskipTests' %path)


def rm_zips(path):
    valida_path(path)

    zips = filter(lambda f: f.endswith('.zip'), os.listdir(path))
    zips = list(map(lambda f: os.path.join(path, f), zips))
    return len(list(map(lambda f: os.unlink(f), zips)))


def rm_folders(path):
    valida_path(path)

    folders = list(map(lambda f: os.path.join(path, f), os.listdir(path)))
    folders = filter(lambda f: os.path.isdir(f) and not f.endswith('__pycache__'), folders)
    return len(list(map(lambda f: shutil.rmtree(f), folders)))


def reset_config(path):
    clear_data()
    valida_path(path)

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
