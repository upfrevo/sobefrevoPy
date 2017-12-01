import smtplib
 
# Credenciais
remetente    = 'sobefrevo@gmail.com'
senha        = 'watsonfrevo2017'
 
# Informações da mensagem
destinatario = 'jpataide@gmail.com'
assunto      = 'Enviando email com python'
texto        = 'Esse email foi enviado usando python! :)'

def envia_email(mensagem):     
    # Preparando a mensagem
    msg = '\r\n'.join([
      'From: %s' % remetente,
      'To: %s' % destinatario,
      'Subject: %s' % assunto,
      '',
      '%s' % texto
      ])
     
    # Enviando o email
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(remetente,senha)
    server.sendmail(remetente, destinatario, msg)
    server.quit()

    
