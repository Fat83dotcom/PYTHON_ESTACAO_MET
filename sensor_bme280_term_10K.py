from tqdm import tqdm
import os
import serial
import time
import csv
import matplotlib.pyplot as plt
from threading import Thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
from confidentials import meu_email, minha_senha, my_recipients, define_arquivo
from statistics import mean
from string import Template

if os.path.isfile('EMAIL_USER_DATA.txt'):
    print('Arquivo "EMAIL_USER_DATA.txt" já existe.')
else:
    define_arquivo()
    print('Arquivo "EMAIL_USER_DATA.txt" foi criado, por favor, configure antes de continuar. Digite enter para continuar...')
    input()

set_porta = '/dev/ttyACM0'

path = os.path.dirname(os.path.realpath(__file__))

while set_porta:
    try:
        arduino = serial.Serial(set_porta, 115200, timeout=1)
        arduino.reset_input_buffer()
        break
    except serial.serialutil.SerialException:
        set_porta = input('Digite a porta serial em que o Arduino está conectado: ')
print(f'O Arduino está na porta: {set_porta}')


class EmailThread(Thread):
    def __init__(self, inicio, umi, press, t1, t2, t1max,
                 t1min, t2max, t2min, umimax, umimini,
                 pressmax, pressmini, ini, fim, path):
        super().__init__()
        self.inicio = inicio
        self.path = path
        self.umi = umi
        self.press = press
        self.t1 = t1
        self.t2 = t2
        self.t1max = t1max
        self.t1min = t1min
        self.t2max = t2max
        self.t2min = t2min
        self.umimax = umimax
        self.umimini = umimini
        self.pressmax = pressmax
        self.pressmini = pressmini
        self.ini = ini
        self.fim = fim

    def run(self):
        msg = MIMEMultipart()
        msg['from'] = 'Fernando Mendes'
        msg['to'] = ','.join(my_recipients())
        msg['subject'] = f'Monitoramento Estação Metereologica Fat83dotcom {data()}'
        corpo = MIMEText(recebe_dados(self.umi, self.press, self.t1, self.t2,
                         self.t1max, self.t1min, self.t2max, self.t2min,
                         self.umimax, self.umimini, self.pressmax, self.pressmini,
                         self.ini, self.fim, data()), 'html')
        msg.attach(corpo)
        try:
            umidade = f'{self.path}/Umidade{self.inicio}.pdf'
            pressao = f'{self.path}/Pressao{self.inicio}.pdf'
            tmp1 = f'{self.path}/Temperatura_Interna{self.inicio}.pdf'
            temp2 = f'{self.path}/Temperatura_Externa{self.inicio}.pdf'
            # log = '/home/fernando/PYTHON_PIPENV_ESTACAO_METEREO/log_bme280.csv'

            with open(umidade, 'rb') as pdf_U:
                anexo_U = MIMEApplication(pdf_U.read(), _subtype='pdf')
                pdf_U.close()
                anexo_U.add_header('Conteudo', umidade)
                msg.attach(anexo_U)

            with open(pressao, 'rb') as pdf_P:
                anexo_P = MIMEApplication(pdf_P.read(), _subtype='pdf')
                pdf_P.close()
                anexo_P.add_header('Conteudo', pressao)
                msg.attach(anexo_P)

            with open(tmp1, 'rb') as pdf_T1:
                anexo_T1 = MIMEApplication(pdf_T1.read(), _subtype='pdf')
                pdf_T1.close()
                anexo_T1.add_header('Conteudo', tmp1)
                msg.attach(anexo_T1)

            with open(temp2, 'rb') as pdf_T2:
                anexo_T2 = MIMEApplication(pdf_T2.read(), _subtype='pdf')
                pdf_T2.close()
                anexo_T2.add_header('Conteudo', temp2)
                msg.attach(anexo_T2)

            # with open(log, 'rb') as csv_file:
            #     anexo_csv = MIMEApplication(csv_file.read(), _subtype='csv')
            #     csv_file.close()
            #     anexo_csv.add_header('Conteudo', log)
            #     msg.attach(anexo_csv)

            with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(''.join(meu_email()), ''.join(minha_senha()))
                smtp.send_message(msg)
                # print('Email enviado com sucesso.')
        except FileNotFoundError:
            # print('Email não enviado.')
            pass

        os.remove(f'{self.path}/Umidade{self.inicio}.pdf')
        os.remove(f'{self.path}/Pressao{self.inicio}.pdf')
        os.remove(f'{self.path}/Temperatura_Interna{self.inicio}.pdf')
        os.remove(f'{self.path}/Temperatura_Externa{self.inicio}.pdf')


class ConvertTempo:
    def __init__(self, hora=None, minuto=None, segundo=None):
        self.hora = hora
        self.minuto = minuto
        self.segundo = segundo

    def convert_hr_segundo(self):
        conv_hr_sec = self.hora * 3600
        return conv_hr_sec

    def convert_min_segundo(self):
        conv_min_sec = self.minuto * 60
        return conv_min_sec

    def soma_tempo(self):
        h = self.hora
        m = self.minuto
        s = self.segundo
        soma = ConvertTempo(hora=h, minuto=m, segundo=s)
        soma = soma.convert_hr_segundo() + soma.convert_min_segundo()
        soma += self.segundo
        return soma


def leia_me():
    with open('LEIA_ME.txt', 'w') as file:
        texto = '''
                ***
                Para usar corretamente este programa, você deve observar os seguintes procedimentos:

                -> No arquivo "EMAIL_USER_DATA" é o local onde o usuário irá configurar seu login de
                email, respeitando algumas regras simples que, se não seguidas, podem ocasionar
                funcionamento inesperado, erros ou a quebra do programa.

                AS REGRAS SÃO:

                -> NA PRIMEIRA E SEGUNDA LINHA DO ARQUIVO, NOS CAMPOS "MEU EMAIL" E "MINHA SENHA", APÓS ":" COLOQUE UM (1) ESPAÇO E APENAS UM (1)
                ESPAÇO, E CASO ESSA REGRA NÃO SEJA SEGUIDA, O PROGRAMA NÃO LERÁ CORRETAMENTE OS DADOS E NÃO ENVIARÁ OS EMAILS CORRETAMENTE.

                -> NA TERCEIRA LINHA, INSIRA OS EMAILS DOS DESTINATARIOS, SEPARADOS POR VIRGULAS E SEM QUEBRAS DE LINHA.
                SE HOUVER QUEBRA DE LINHA, O PROGRAMA AINDA ENVIARÁ OS EMAILS MAS OCORRERÁ ERROS E OMISSÕES DE DADOS INDESEJADAS.

                -> SEGUINDO ESSAS REGRAS É ESPERADO QUE OS EMAILS SEJAM ENVIADOS SEM PROBLEMAS E, CASO ACONTEÇA ALGUM
                PROBLEMA, POR FAVOR, ENTRAR EM CONTATO COM O DESENVOLVEDOR EXPLICANDO O PROBLEMA.


                OBRIGADO!!!

                ***
        '''
        file.write(texto)


def recebe_dados(umidade, pressao, temp1, temp2, temp1max, temp1min,
                 temp2max, temp2min, umima, umimi, pressma, pressmi,
                 inicio, fim, data):
    with open('template.html', 'r') as doc:
        template = Template(doc.read())
        corpo_msg = template.safe_substitute(umi=umidade, press=pressao, t1=temp1, t2=temp2,
                                             t1max=temp1max, t1min=temp1min, t2max=temp2max,
                                             t2min=temp2min, umimax=umima, umimini=umimi,
                                             pressmax=pressma, pressmini=pressmi, ini=inicio,
                                             fim=fim, dat=data)
    return corpo_msg


def data():
    data = time.strftime('%d %b %Y %H:%M:%S', time.localtime())
    return data


def maxi(dados):
    return round(max(dados), 2)


def mini(dados):
    return round(min(dados), 2)


def plot_umidade(uy, inicio, path):
    ux = range(len(uy))
    file = f'{path}/Umidade{inicio}.pdf'
    plt.title(f'Gráfico Umidade\n-> Inicio: {inicio} <-|-> Termino: {data()} <-\nMáxima: {maxi(uy)} --- Mínima: {mini(uy)}')
    plt.xlabel('Tempo em segundos.')
    plt.ylabel('Umidade Relativa do Ar %')
    plt.plot(ux, uy)
    plt.savefig(file)
    plt.clf()


def plot_pressao(py, inicio, path):
    px = range(len(py))
    file = f'{path}/Pressao{inicio}.pdf'
    plt.title(f'Gráfico Pressão\n-> Inicio: {inicio} <-|-> Termino: {data()} <-\nMáxima: {maxi(py)} --- Mínima: {mini(py)}')
    plt.xlabel('Tempo em segundos.')
    plt.ylabel('Pressão Atmosferica em hPa')
    plt.plot(px, py)
    plt.savefig(file)
    plt.clf()


def plot_temp1(t1y, inicio, path):
    t1x = range(len(t1y))
    file = f'{path}/Temperatura_Interna{inicio}.pdf'
    plt.title(f'Gráfico Temp Interna\n-> Inicio: {inicio} <-|-> Termino: {data()} <-\nMáxima: {maxi(t1y)} --- Mínima: {mini(t1y)}')
    plt.xlabel('Tempo em segundos.')
    plt.ylabel('Temperatura em °C')
    plt.plot(t1x, t1y)
    plt.savefig(file)
    plt.clf()


def plot_temp2(t2y, inicio, path):
    t2x = range(len(t2y))
    file = f'{path}/Temperatura_Externa{inicio}.pdf'
    plt.title(f'Gráfico Temp Externa\n-> Inicio: {inicio} <-|-> Termino: {data()} <-\nMáxima: {maxi(t2y)} --- Mínima: {mini(t2y)}')
    plt.xlabel('Tempo em segundos.')
    plt.ylabel('Temperatura em °C')
    plt.plot(t2x, t2y)
    plt.savefig(file)
    plt.clf()


def flagEntry():
    opition = ''
    cont = 0
    tentativa = 5
    while opition == '' and cont < tentativa:
        print(f'{cont  + 1}ª tentativa... {tentativa - (cont + 1)} restantes.')
        print('Tempo padrão: 1 Hora.')
        opition = input('Deseja definir a frequencia dos gráficos ?[S/N]: ').upper()
        if opition[0] == 'S':
            call = call_tempo()
            if call:
                print('Em Execução ....')
                return int(call)
            else:
                cont += 1
                opition = ''
                continue
        else:
            print('Tempo padrão definido, 1 hora.')
            flag_entry = 3600
            return flag_entry
    print('O tempo padrão foi definito: 1 hora.')
    flag_entry = 3600
    return flag_entry


def call_tempo():
    print('Intervalo máximo: 6 horas.')
    print('Digite as horas, minutos e segundos para saida de gráficos: ')
    hora = input('Digite o tempo em horas: ')
    minuto = input('Digite o tempo em minutos: ')
    segundo = input('Digite o tempo em segundos: ')
    try:
        if 0 <= int(minuto) < 60 and 0 <= int(segundo) < 60:
            flag_entry = ConvertTempo(int(hora), int(minuto), int(segundo))
            flag_entry = flag_entry.soma_tempo()
            if flag_entry > 21600:
                flag_entry = 21600
                print(f'Tempo definido em {flag_entry} segundos/ {flag_entry/3600} horas.')
                return int(flag_entry)
            else:
                print(f'Tempo definido em {flag_entry} segundos/ {flag_entry/3600} horas.')
                return int(flag_entry)
        else:
            print('Digite os minutos e segundos entre 0 e 59.')
            return None
    except ValueError:
        print('error')
        print('Digite somente numeros.\n')
        return None


def main():
    cont3 = 0
    while 1:
        if cont3 == 0:
            tempo_graf = int(flagEntry())
            print(f'Inicio: --> {data()} <--')
            arduino.reset_input_buffer()
        else:
            print(f'Parcial {cont3} --> {data()} <--')

        inicio = data()

        uy = []
        py = []
        t1y = []
        t2y = []

        d1 = {
            'u': '',
            'p': '',
            '1': '',
            '2': ''
        }

        cont2 = 0
        with tqdm(total=tempo_graf) as barra:
            while cont2 < tempo_graf:
                cont = 0
                while cont < 8:
                    try:
                        dado = str(arduino.readline())
                        dado = dado[2:-5]
                        if dado[0] == 'u':
                            d1['u'] = float(dado[1:].strip())
                        if dado[0] == 'p':
                            d1['p'] = float(dado[1:].strip())
                        if dado[0] == '1':
                            d1['1'] = float(dado[1:].strip())
                        if dado[0] == '2':
                            d1['2'] = float(dado[1:].strip())
                    except (ValueError, IndexError):
                        continue
                    cont += 1
                with open('log_bme280.csv', 'a+', newline='', encoding='utf-8') as log:
                    try:
                        w = csv.writer(log)
                        w.writerow([data(), d1['u'], d1['p'], d1['1'], d1['2']])
                        uy.append(float(d1['u']))
                        py.append(float(d1['p']))
                        t1y.append(float(d1['1']))
                        t2y.append(float(d1['2']))
                        cont2 += 1
                        barra.update(1)
                        time.sleep(0.90)
                    except ValueError:
                        print('error')
                        continue
        plot_umidade(uy, inicio, path)
        plot_pressao(py, inicio, path)
        plot_temp1(t1y, inicio, path)
        plot_temp2(t2y, inicio, path)
        cont3 += 1
        emaail = EmailThread(inicio, round(mean(uy), 2), round(mean(py), 2),
                             round(mean(t1y), 2), round(mean(t2y), 2),
                             maxi(t1y), mini(t1y), maxi(t2y), mini(t2y),
                             maxi(uy), mini(uy), maxi(py), mini(py),
                             inicio, data(), path)
        emaail.start()


while 1:
    leia_me()
    main()
