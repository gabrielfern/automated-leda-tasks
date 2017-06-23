import re
import pprint
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


def make_datetime(datetime_tuple):
    ano = int(datetime_tuple[0][6:10])
    mes = int(datetime_tuple[0][3:5])
    dia = int(datetime_tuple[0][0:2])
    hora = int(datetime_tuple[1][0:2])
    minutos = int(datetime_tuple[1][3:5])
    return datetime.datetime(ano, mes, dia, hora, minutos)


def req_crono():
    req = requests.get(URLS[0])
    valida_requisicao(req)

    all_roteiros = CRONOGRAMA_PATTERN.findall(req.text)
    roteiros = []
    dates = []
    horas = []
    for i in range(len(all_roteiros)):
        roteiros.append(all_roteiros[i][:6])
        #dates.append(all_roteiros[i][-5:len(all_roteiros[i])])
        dates.append(all_roteiros[i][-23:-13])
        horas.append(all_roteiros[i][-12:-7])
    
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


def main():
    pprint.pprint(req_crono())


if __name__ == '__main__':
    main()
