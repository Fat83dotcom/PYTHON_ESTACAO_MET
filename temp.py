from string import Template


def recebe_dados(umidade, pressao, temp1, temp2, data):
    with open('template.html', 'r') as doc:
        template = Template(doc.read())
        corpo_msg = template.safe_substitute(umi=umidade, press=pressao, t1=temp1, t2=temp2, dat=data)
    return corpo_msg
