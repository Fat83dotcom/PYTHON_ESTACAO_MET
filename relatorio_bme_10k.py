import matplotlib.pyplot as plt
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
from confidentials import meu_email, minha_senha, my_recipients
import time


class Periodo:

    def data_inicio(self, dia=str, mes=str, ano=str, hora=str, minuto=str, segundo=str):
        data_ini = f'{dia} {mes} {ano} {hora}:{minuto}'
        return data_ini

    def data_termino(self, dia=str, mes=str, ano=str, hora=str, minuto=str, segundo=str):
        data_ter = f'{dia} {mes} {ano} {hora}:{minuto}'
        return data_ter


def entry_inicio():
    meses_ano = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    retorno = Periodo()
    entrada = False
    while not entrada:
        print('Preencha os campos com a data de início da busca.')
        print(f'Para os meses digite desta maneira: {meses_ano}.')
        dia = ''
        while not dia:
            dia = input('Digite o dia(DD): ')
            if dia.isnumeric() and len(dia) == 2 and 0 < int(dia) <= 31:
                break
            else:
                print('Digite somente dois números entre 1 e 31.')
                dia = ''
                continue
        mes = ''
        while not mes:
            mes = input('Digite o mês(MMM): ').title()
            if mes.isalpha() and len(mes) == 3 or len(mes) == 4:
                for mes1 in meses_ano:
                    if mes1 == mes:
                        break
                else:
                    print('O que você digitou não corresponde a um mes do ano.')
                    mes = ''
            else:
                print('Digite somente 3 letras conforme a lista acima.')
                mes = ''
                continue

        ano = ''
        while not ano:
            data_ano = date.today().year
            ano = input('Digite o ano(AAAA): ')
            if ano.isnumeric() and len(ano) == 4:
                if 2010 <= int(ano) <= data_ano:
                    break
                else:
                    print(f'Digite um ano entre 2010 e {data_ano}')
                    ano = ''
                    continue
            else:
                print('Digite somente 4 números.')
                ano = ''
                continue
        hora = ''
        while not hora:
            hora = input('Digite a hora(HH): ')
            if hora.isnumeric() and len(hora) == 2 and 0 <= int(hora) <= 23:
                break
            else:
                print('Digite somente 2 números entre 00 e 23.')
                hora = ''
                continue
        minuto = ''
        while not minuto:
            minuto = input('Digite os minutos(MM): ')
            if minuto.isnumeric() and len(minuto) == 2 and 0 <= int(minuto) <= 59:
                break
            else:
                print('Digite somente 2 números entre 00 e 59.')
                minuto = ''
                continue
        return retorno.data_inicio(dia, mes, ano, hora, minuto)


def entry_termino():
    meses_ano = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    retorno = Periodo()
    entrada = False
    while not entrada:
        print('Preencha os campos com a data de término da busca.')
        print(f'Para os meses digite desta maneira: {meses_ano}.')
        dia = ''
        while not dia:
            dia = input('Digite o dia(DD): ')
            if dia.isnumeric() and len(dia) == 2 and 0 < int(dia) <= 31:
                break
            else:
                print('Digite somente dois números entre 1 e 31.')
                dia = ''
                continue
        mes = ''
        while not mes:
            mes = input('Digite o mês(MMM): ').title()
            if mes.isalpha() and len(mes) == 3 or len(mes) == 4:
                for mes1 in meses_ano:
                    if mes1 == mes:
                        break
                else:
                    print('O que você digitou não corresponde a um mes do ano.')
                    mes = ''
            else:
                print('Digite somente 3 letras conforme a lista acima.')
                mes = ''
                continue

        ano = ''
        while not ano:
            data_ano = date.today().year
            ano = input('Digite o ano(AAAA): ')
            if ano.isnumeric() and len(ano) == 4:
                if 2010 <= int(ano) <= data_ano:
                    break
                else:
                    print(f'Digite um ano entre 2010 e {data_ano}')
                    ano = ''
                    continue
            else:
                print('Digite somente 4 números.')
                ano = ''
                continue
        hora = ''
        while not hora:
            hora = input('Digite a hora(HH): ')
            if hora.isnumeric() and len(hora) == 2 and 0 <= int(hora) <= 23:
                break
            else:
                print('Digite somente 2 números entre 00 e 23.')
                hora = ''
                continue
        minuto = ''
        while not minuto:
            minuto = input('Digite os minutos(MM): ')
            if minuto.isnumeric() and len(minuto) == 2 and 0 <= int(minuto) <= 59:
                break
            else:
                print('Digite somente 2 números entre 00 e 59.')
                minuto = ''
                continue
        return retorno.data_termino(dia, mes, ano, hora, minuto)


def plot_graf(y, inicio, termino, nome):
    x = range(len(y))
    minima = min(y)
    maxima = max(y)
    cont_titulo = f'{nome} mínima: {minima} {nome} -- máxima: {maxima}'
    titulo = f'-> Inicio: {inicio} <-\n->Termino: {termino} <-\nGráfico {nome}: {cont_titulo}'
    plt.title(titulo)
    plt.xlabel('Tempo em segundos.')
    if nome == 'Umidade':
        plt.ylabel('Umidade Relativa do Ar(%).')
    elif nome == 'Pressao':
        plt.ylabel('Pressão em hPa.')
    elif nome == 'Temp Interna':
        plt.ylabel('Temperatura em °C.')
    else:
        plt.ylabel('Temperatura em °C.')
    plt.plot(x, y)
    plt.savefig(f'/home/fernando/Área de trabalho/{nome}.pdf')
    plt.clf()


def data():
    data = time.strftime('%d %b %Y %H:%M:%S', time.localtime())
    return data


def main():
    with open('log_bme280.csv', 'r', encoding='utf-8', newline='') as file:
        file.seek(0)
        lista = [x.split(',') for x in file.readlines()]
        lista0 = [x[0][:-3] for x in lista]
        inicio = entry_inicio()
        termino = entry_termino()
        if inicio in lista0:
            valor1 = inicio
            try:
                valor2 = termino
            except ValueError:
                print('O valor final não foi encontrado.')
                return None
            pos1 = lista0.index(valor1)
            pos2 = lista0.index(valor2)
        else:
            print('O valor inicial não foi encontrado.')
            return None
        try:
            umi = [round(float(x[1]), 2) for x in lista[pos1:pos2]]
            pres = [round(float(x[2]), 2) for x in lista[pos1:pos2]]
            temp1 = [round(float(x[3]), 2) for x in lista[pos1:pos2]]
            temp2 = [round(float(x[4][:-2]), 2) for x in lista[pos1:pos2]]
            plot_graf(umi, inicio, termino, 'Umidade')
            plot_graf(pres, inicio, termino, 'Pressao')
            plot_graf(temp1, inicio, termino, 'Temp Int')
            plot_graf(temp2, inicio, termino, 'Temp Ext')
        except ValueError as er:
            print(f'Erro aos ler os dados, verifique o arquivo fonte se não há dados faltando. {er}')
            return None

        msg = MIMEMultipart()
        msg['from'] = 'Fernando Mendes'
        msg['to'] = ','.join(my_recipients)
        msg['subject'] = f'Relatórios: {data()}'
        corpo = MIMEText(f'Relatórios, {data()}\nPeriodo:\n{inicio}\n{termino}')
        msg.attach(corpo)
        try:

            umidade = '/home/fernando/Área de trabalho/Umidade.pdf'
            pressao = '/home/fernando/Área de trabalho/Pressao.pdf'
            tempint = '/home/fernando/Área de trabalho/Temp Int.pdf'
            tempextr = '/home/fernando/Área de trabalho/Temp Ext.pdf'

            with open(umidade, 'rb') as pdf_umi:
                anexo_U = MIMEApplication(pdf_umi.read(), _subtype='pdf')
                pdf_umi.close()
                anexo_U.add_header('Conteudo', umidade)
                msg.attach(anexo_U)

            with open(pressao, 'rb') as pdf_pre:
                anexo_P = MIMEApplication(pdf_pre.read(), _subtype='pdf')
                pdf_pre.close()
                anexo_P.add_header('Conteudo', pressao)
                msg.attach(anexo_P)

            with open(tempint, 'rb') as pdf_T1:
                anexo_T1 = MIMEApplication(pdf_T1.read(), _subtype='pdf')
                pdf_T1.close()
                anexo_T1.add_header('Conteudo', tempint)
                msg.attach(anexo_T1)

            with open(tempextr, 'rb') as pdf_T2:
                anexo_T2 = MIMEApplication(pdf_T2.read(), _subtype='pdf')
                pdf_umi.close()
                anexo_T2.add_header('Conteudo', tempextr)
                msg.attach(anexo_T2)

            with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(meu_email, minha_senha)
                smtp.send_message(msg)
                print('Email enviado com sucesso.')
        except FileNotFoundError:
            print('Email não enviado.')
            return None

while 1:
    main()
