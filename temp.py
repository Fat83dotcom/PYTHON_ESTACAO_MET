from string import Template


def recebe_dados(umidade, pressao, temp1, temp2, temp1max, temp1min,
                 temp2max, temp2min, inicio, fim, data):
    with open('template.html', 'r') as doc:
        template = Template(doc.read())
        corpo_msg = template.safe_substitute(umi=umidade, press=pressao, t1=temp1, t2=temp2,
                                             t1max=temp1max, t1min=temp1min, t2max=temp2max,
                                             t2min=temp2min, ini=inicio, fim=fim, dat=data)
    return corpo_msg
