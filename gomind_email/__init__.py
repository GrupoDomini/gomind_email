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
        <table width="100%" border="0" cellspacing="0" cellpadding="0">
            <tr>
                <td bgcolor="#e8e8e8" style="padding: 10px 0 10px 0;">
                    <table align="center" border="0" cellpadding="0" cellspacing="0" width="700" style="border-collapse: collapse;">
                        
                        <tr>
                            <td bgcolor="#ffffff">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%">

                                    <tr>
                                        <td style="color: #153643; font-family: Arial, sans-serif; font-size: 24px; text-align: center; padding-top: 50px">
                                            <b>Olá! Esta é uma mensagem automática da Mia.</b>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 20px 0 30px 0; color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 25px; text-align: center;">
                                            Registramos erro durante execução do {RPA}.
                                            <br/>
                                            Código de Referência: <b style="color: #13B2A3;">gosppt{mac_address}</b>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <a href="https://www.gomind.com.br">
                                                <img src="https://lh3.googleusercontent.com/drive-viewer/AKGpihbkcMb6Z8W7BZ4cdRBqdb27XK_pvKkARDsJf92QxEyeSAukwEkb0YL_vrSSyZ0yAofPPf3TGcW0fG9eCPcUDpH3PKxt=w1366-h607" alt="Go Mind" width="60%" height="auto" style="display: block; margin: auto;" />
                                            </a>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
        """

        erro = f"""
        <table width="100%" border="0" cellspacing="0" cellpadding="0">
            <tr>
                <td bgcolor="#e8e8e8" style="padding: 10px 0 10px 0;">
                    <table align="center" border="0" cellpadding="0" cellspacing="0" width="700" style="border-collapse: collapse;">
                        
                        <tr>
                            <td bgcolor="#ffffff">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%">

                                    <tr>
                                        <td style="color: #153643; font-family: Arial, sans-serif; font-size: 24px; text-align: center; padding-top: 50px">
                                            <b>Olá! Esta é uma mensagem automática da Mia.</b>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 20px 0 30px 0; color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 25px; text-align: center;">
                                            Registramos erro durante execução do {RPA}.
                                            <br/>
                                            Código de Referência: <b style="color: #13B2A3;">gosppt{mac_address}</b>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <a href="https://www.gomind.com.br">
                                                <img src="https://lh3.googleusercontent.com/u/0/drive-viewer/AKGpihbz7cph3IXX6fWznlmRztsmDSqN-yzr0pgyEaLa6eqGg-jIYmUcd5Tvaz_8LxeX5O3dZ8zcq_Hsw4oH0kml5J3GHTUx=w1366-h607" alt="Go Mind" width="60%" height="auto" style="display: block; margin: auto;" />
                                            </a>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
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
