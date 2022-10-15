'''
Este modulo faz a leitura do email, senha e destinatários de um arquivo externo, que deve estar na
mesma pasta que o executável Python
'''
modelo = '''Seu email: xxxxx@xxxxx.com
Sua senha: 123456789
Destinatarios aqui!
'''


def meu_email():
    with open('EMAIL_USER_DATA.txt', 'r') as file:
        file.seek(0)
        email_user = [i[11:-1] for e, i in enumerate(file.readlines()) if e == 0 and i != '\n']
        return email_user


def minha_senha():
    with open('EMAIL_USER_DATA.txt', 'r') as file:
        file.seek(0)
        senha_user = [i[11:-1] for e, i in enumerate(file.readlines()) if e == 1 and i != '\n']
        return senha_user


def my_recipients():
    with open('EMAIL_USER_DATA.txt', 'r') as file:
        file.seek(0)
        emails = [i for e, i in enumerate(file.readlines()) if e >= 2 and i != '\n']
        return emails


def define_arquivo():
    with open('EMAIL_USER_DATA.txt', 'w') as file:
        file.write(modelo)


if __name__ == '__main__':
    pass
    # print(''.join(meu_email()))
    # print(''.join(minha_senha()))
    # print(''.join(my_recipients()))
