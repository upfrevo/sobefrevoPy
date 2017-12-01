import smtplib
 
# Credenciais
remetente    = 'sobefrevo@gmail.com'
senha        = 'watsonfrevo2017'
 
# Informações da mensagem
destinatario = 'sobefrevo@gmail.com'

def envia_email(assunto, mensagem):     
    # Preparando a mensagem
    msg = MIMEMultipart()
    msg['From'] = destinatario
    
    msg['To'] = destinatario
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = assunto

    arquivo_log = "logs/LOG{}.log".format(time.strftime("_%Y_%m_%d"))
    try:
        msg.attach(MIMEText(mensagem))
        with open(arquivo_log, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)
    finally: 
        smtp = smtplib.SMTP('smtp.gmail.com:587')
        smtp.starttls()
        smtp.login(remetente,senha)
        smtp.sendmail(remetente, destinatario, msg.as_string())
        smtp.close()

    
