#!/usr/bin/python
# Gabriel Fernandes <gabrielfernndss@gmail.com>


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
Algumas funcoes de
utilidade na automatizacao
"""


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
    regex = re.compile('\d{1,9}\Z')
    if not regex.match(matricula):
        raise ValueError('matricula precisa ser do tipo xxxxxxxxx, onde x eh um digito(1-9)')


def valida_path(path):
    if not isinstance(path, str):
        raise TypeError('path precisa ser passado como uma "str"')
    if not os.path.isdir(path):
        raise TypeError('insira um caminho("path") de diretorio valido')


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
    valida_path(path)

    try:
        os.unlink(os.path.join(path, 'personalinfo.json'))
        return 'configuracoes resetadas com sucesso'
    except FileNotFoundError:
        return 'configuracao ainda nao feita'


def main():
    args = sys.argv
    try:
        write_pom(args[1], args[2], args[3])
    except IndexError:
        print('''Uso: passar caminho ate a pasta em que se encontra o pom.xml,
            matricula e roteiro na qual deseja-se preencher automaticamento no pom
            Exemplo: python3 autoit.py /home/fernandes/leda-roteiros 111110234 R03-03''')
        sys.exit(1)


if __name__ == '__main__':
    main()
