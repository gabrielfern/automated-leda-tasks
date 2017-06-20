import re, requests

URLS = (http://150.165.85.29:81/cronograma,
        http://150.165.85.29:81/horaAtual)

CRONOGRAMA_PATTERN = re.compile("""R[01]\d-03\s*<td\s*class="text-xs-center"\s*data-toggle="tooltip"\s*data-placement="right"\s*title='Atividade\s*inicia\s*em\s*\d\d/\d\d/2017\s*\d\d:\d\d'>\d\d/\d\d""")

req = requests.get(CRONOGRAMA_PATTERN)

req.raise_for_
