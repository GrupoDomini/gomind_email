"""All utils from gomind robot

Raises:
    RuntimeError: _description_
"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

try:
    from getmac import get_mac_address as gma  # type: ignore

    mac_address = gma()
except Exception as e:
    raise ImportError("Erro ao importar get_mac_address") from e


def enviar_email(
    file_path,
    msg_mail_to,
    msg_mail_cc="",
    result=True,
    RPA="[Robô ainda não identificado]",
):
    try:
        """Corpo do e-mail"""
        sucesso = f"""
        <center>
        <p>Prezados,</p>
        <p><i>Esta é uma mensagem automática da <b>Mia.</b></i></p>
        
        <p>Registramos a conclusão do {RPA} com sucesso! Verifique o resultado do processo em anexo.</p>

        <p>
            <img src="https://raw.githubusercontent.com/GrupoDomini/Public/main/mail_suc.png"></img>
        </p>

        Att, <b>Mia - Go Mind</b><br>
        Departamento de Tecnologia<br>
        <a href='https://www.gomind.com.br' title='Unlimited Growth'>www.gomind.com.br</a>
        </center>
        """

        erro = f"""
        <center>
        <p>Prezados,</p>
        <p><i>Esta é uma mensagem automática da <b>Mia.</b></i></p>
        Registramos erro durante execução do {RPA}.<br>
        <p>Código de Referência: gosppt{mac_address}.</p>
        
        <p>
            <img src="https://raw.githubusercontent.com/GrupoDomini/Public/main/mail_erro.png"></img>
        </p>

        Att, <b>Mia - Go Mind</b><br>
        Departamento de Tecnologia<br>
        <a href='https://www.gomind.com.br' title='Unlimited Growth'>www.gomind.com.br</a>
        </center>
        """

        # Endereços
        msg = MIMEMultipart()
        msg["From"] = "mia@gomind.com.br"
        msg["To"] = msg_mail_to
        msg["Cc"] = msg_mail_cc

        # Assunto da mensagem
        if result:
            msg["Subject"] = "Go Mind | Informativo RPA - Sucesso"
            msg.attach(MIMEText(sucesso, "html"))
        else:
            msg["Cco"] = "suporte@gomind.com.br"
            msg["Subject"] = "Go Mind | Informativo RPA - Erro"
            msg.attach(MIMEText(erro, "html"))

        # Anexo
        if result:
            attachment = open(file_path, "rb")  # Local do arquivo
            anexo = "RPA_resultado.xlsx"  # Nome e extensão do arquivo em anexo

            part = MIMEBase("application", "octet-stream")
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment; filename= %s" % anexo)
            msg.attach(part)
            attachment.close()
        text = msg.as_string().encode(encoding="latin-1", errors="strict")

        """Protocolo & segurança"""
        # Versão Gmail
        # s = smtplib.SMTP('smtp.gmail.com: 587') #Gmail Server
        # password = "pusuxxkylregxdis" #token app gerada na conta Google (john.rpa.domini@gmail.com)

        # Versão Microsoft
        s = smtplib.SMTP("smtp.office365.com: 587")  # Office365 Server
        password = "Xor36280"  # token app gerada na conta Google (mia@gomind.com.br)

        s.starttls()

        # Envio da mensagem
        s.login(msg["From"], password)
        if result:
            s.sendmail(msg["From"], msg["To"].split(",") + msg["Cc"].split(","), text)
        else:
            s.sendmail(
                msg["From"],
                msg["To"].split(",") + msg["Cc"].split(",") + msg["Cco"].split(","),
                text,
            )
        s.quit()

        print("E-mail enviado com sucesso")
    except Exception as e:
        print(e)
        print("Erro ao enviar e-mail")
