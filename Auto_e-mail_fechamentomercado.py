import pandas as pd
import datetime
import yfinance as yf
from matplotlib import pyplot as plt
import mplcyberpunk
import smtplib
from email.message import EmailMessage


ativos = ["^BVSP", "BRL=X"]

hoje = datetime.datetime.now()# data de hoje
um_ano_atras = hoje - datetime.timedelta(days = 365)# delta de um ano atrás

dados_mercado = yf.download(ativos, um_ano_atras, hoje) # base de dados, poderia ser qualquer uma, no caso foi uma gratuita
# argumentos periodo e ativos de interesse

dados_fechamento = dados_mercado['Adj Close'] # pegamos fechamento no mercado ajustado, que é o que interessa
dados_fechamento.columns = ['dolar', 'ibovespa'] # renomear colunas dos ativos, a fim de obter melhor ambiente
dados_fechamento = dados_fechamento.dropna() #tratando dados, retirando linhas brancas

dados_fechamento_mensal = dados_fechamento.resample("M").last() #realojando a tabela em por mes, e fechamento do mes
dados_fechamento_anual = dados_fechamento.resample("Y").last()# o mesmo passo anterior, porém anual

retorno_no_ano = dados_fechamento_anual.pct_change().dropna() #pegando fechamento mensal, a variação percentual e retirando nula linhas nulas
retorno_no_mes = dados_fechamento_mensal.pct_change().dropna()#mesmo passo anterior anual
retorno_no_dia = dados_fechamento.pct_change().dropna()# mesmo passo, porém diario

retorno_dia_dolar = retorno_no_dia.iloc[-1, 0] # pega ultimo elemento do primeiro ativo no dia
retorno_dia_ibovespa = retorno_no_dia.iloc[-1, 1]# pega ultimo elemento do segundo ativo

retorno_mes_dolar = retorno_no_mes.iloc[-1, 0]# pega ultimo elemento do primeiro ativo no mes
retorno_mes_ibovespa = retorno_no_mes.iloc[-1, 1]# pega ultimo elemento do segundo ativo

retorno_ano_dolar = retorno_no_ano.iloc[-1, 0]# pega ultimo elemento do primeiro ativo no ano
retorno_ano_ibovespa = retorno_no_ano.iloc[-1, 1]# pega ultimo elemento do segundo ativo

retorno_dia_dolar = round(retorno_dia_dolar * 100, 2) # reescrevendo para visual mais atrativo
retorno_dia_ibovespa = round(retorno_dia_ibovespa * 100, 2)

retorno_mes_dolar = round(retorno_mes_dolar * 100, 2)
retorno_mes_ibovespa = round(retorno_mes_ibovespa * 100, 2)

retorno_ano_dolar = round(retorno_ano_dolar * 100, 2)
retorno_ano_ibovespa = round(retorno_ano_ibovespa * 100, 2)


#gerando graficos de exemplo
plt.style.use("cyberpunk") #mudando estilo do plot

dados_fechamento.plot(y = 'ibovespa', use_index = True, legend = False)

plt.title("Ibovespa")

plt.savefig('ibovespa.png', dpi = 300)#salvando na pasta



plt.style.use("cyberpunk")

dados_fechamento.plot(y = 'dolar', use_index = True, legend = False)

plt.title("Dolar")

plt.savefig('dolar.png', dpi = 300)


#credenciais do email
import os
from dotenv import load_dotenv
load_dotenv() #objetivo de manter a senha do email privada no codigo
senha = os.environ.get("senha_email")
email = 'seuemail@gmail.com'

msg = EmailMessage()  #criando objeto de emails com assunto, remetente e endereço
msg['Subject'] = "Enviando e-mail com o Python"
msg['From'] = 'seuemail@gmail.com'
msg['To'] = 'seualvo@gmail.com.br'

msg.set_content(f'''Prezado diretor, segue o relatório diário:

Bolsa:

No ano o Ibovespa está tendo uma rentabilidade de {retorno_ano_ibovespa}%, 
enquanto no mês a rentabilidade é de {retorno_mes_ibovespa}%.

No último dia útil, o fechamento do Ibovespa foi de {retorno_dia_ibovespa}%.

Dólar:

No ano o Dólar está tendo uma rentabilidade de {retorno_ano_dolar}%, 
enquanto no mês a rentabilidade é de {retorno_mes_dolar}%.

No último dia útil, o fechamento do Dólar foi de {retorno_dia_dolar}%.


Abs,

''')

# adicionando os anexos, no caso as imagens dos graficos das ações, poderiam ser analises em plot
with open('dolar.png', 'rb') as content_file:
    content = content_file.read()
    msg.add_attachment(content, maintype='application', subtype='png', filename='dolar.png')
    
    
with open('ibovespa.png', 'rb') as content_file:
    content = content_file.read()
    msg.add_attachment(content, maintype='application', subtype='png', filename='ibovespa.png')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp: #enviar email
    
    smtp.login(email, senha)
    smtp.send_message(msg)