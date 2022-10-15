from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from email.mime.application import MIMEApplication
import smtplib
from temp import recebe_dados
from confidentials import meu_email, minha_senha, my_recipients


# def elevator():
#     num = [x**2 for x in range(10000)]
#     return num

msg = MIMEMultipart()
msg['from'] = 'Fernando Mendes'
msg['to'] = ','.join(my_recipients())
msg['subject'] = 'testes'
corpo = MIMEText(recebe_dados(3, 5, 7, 7, 77777, 3, 4, 4, 9, 3, 2), 'html')
msg.attach(corpo)

# arquivo = '/home/fernando/Área de Trabalho/TEMP1/Temperatura_Interna21 May 2021 19:20:48.pdf'
# with open(arquivo, 'rb') as pdf:
#     anexo = MIMEApplication(pdf.read(), _subtype='pdf')
#     pdf.close()
#     anexo.add_header('Content', arquivo)
#     msg.attach(anexo)

with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(meu_email, minha_senha)
    smtp.send_message(msg)
    print('Email enviado com sucesso.')
