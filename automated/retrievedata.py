import re
import datetime
import requests

CRONOGRAMA_PATTERN = re.compile("""R[01]\d-03\s*<td\s*class="text-xs-center"\s*data-toggle="tooltip"\s*data-placement="right"\s*title='Atividade\s*inicia\s*em\s*\d\d/\d\d/2017\s*\d\d:\d\d'>\d\d/\d\d""")

URLS = ('http://150.165.85.29:81/cronograma',
        'http://150.165.85.29:81/horaAtual')

def valida_requisicao(req):
    try:
        req.raise_for_status()
    except requests.exceptions.HTTPError as http_error:
        print(http_error)
        sys.exit(1)

def req_hora_date():
    req = requests.get(URLS[1])
    valida_requisicao(req)
    return req.text

def get_datetime_atual():
    date_atual = get_date_atual()
    hora_atual = get_hora_atual()
    ano = int(date_atual[6:10])
    mes = int(date_atual[3:5])
    dia = int(date_atual[0:2])
    hora = int(hora_atual[0:2])
    minutos = int(hora_atual[3:5])
    return datetime.datetime(ano, mes, dia, hora, minutos)


def get_date_atual():
    return req_hora_date()[-19:-9]


def get_hora_atual():
    return req_hora_date()[-8:-3]

def connectserver():
    req = requests.get(URLS[0])
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
    
    print(roteirnums, '\n')
    print(dates, '\n')
    print(horas, '\n')
    print(get_datetime_atual())


if __name__ == '__main__':
    connectserver()
