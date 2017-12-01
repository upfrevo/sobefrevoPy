import smtplib
 
# Credenciais
remetente    = 'sobefrevo@gmail.com'
senha        = 'watsonfrevo2017'
 
# Informações da mensagem
destinatario = 'jpataide@gmail.com'

def envia_email(assunto, mensagem):     
    # Preparando a mensagem
    msg = '\r\n'.join([
      'From: %s' % remetente,
      'To: %s' % destinatario,
      'Subject: %s' % assunto,
      '',
      '%s' % mensagem
      ])
     
    # Enviando o email
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(remetente,senha)
    server.sendmail(remetente, destinatario, msg)
    server.quit()

    
