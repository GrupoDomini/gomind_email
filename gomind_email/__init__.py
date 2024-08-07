"""All utils from gomind robot

Raises:
    RuntimeError: _description_
"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from datetime import datetime
from typing import Literal


try:
    from getmac import get_mac_address as gma  # type: ignore

    mac_address = gma()
except Exception as e:
    raise ImportError("Erro ao importar get_mac_address") from e


def enviar_email(
    msg_mail_to,
    msg_mail_cc="",
    customer_id="",
    aguarda_analise=False,
    result=Literal['start', 'aguarda_analise', 'sucesso', 'erro'],
    RPA="[Robô ainda não identificado]",
):
    try:
        """Corpo do e-mail"""

        start = f"""
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
                                            Identificamos a inicialização do <b>{RPA}</b> e a execução está em andamento.
                                            <br/>
                                            Retornaremos com o resultado em breve.
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <a href="https://www.gomind.com.br">
                                                <img src="https://github.com/GrupoDomini/Public/blob/main/ASS_MIA.png?raw=true" alt="Go Mind" width="80%" height="auto" style="display: block; margin: auto;" />
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

        msg_aguarda = f"""
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
                                            O <b>{RPA}</b> já coletou os documentos e agora<br/>
                                            aguarda a sua análise para seguir com o processamento!<br/>
                                            Clique <a style="color: #0D2B5B;" href="https://portalmia.app"><b>aqui</b></a> para acessar a plataforma MIA.
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <a href="https://www.gomind.com.br">
                                                <img src="https://github.com/GrupoDomini/Public/blob/main/ASS_MIA.png?raw=true" alt="Go Mind" width="80%" height="auto" style="display: block; margin: auto;" />
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
                                            Registramos a conclusão do <b>{RPA}</b> com sucesso!.
                                            <br/>
                                            Clique <a style="color: #0D2B5B;" href="https://portalmia.app"><b>aqui</b></a> e verifique os resultados
                                            <br/>
                                            <b style="color: #13B2A3;">na plataforma MIA</b>.
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <a href="https://www.gomind.com.br">
                                                <img src="https://github.com/GrupoDomini/Public/blob/main/ASS_MIA.png?raw=true" alt="Go Mind" width="80%" height="auto" style="display: block; margin: auto;" />
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
                                            Registramos erro durante execução do <b>{RPA}</b>.
                                            <br/>
                                            Código de Referência: <b style="color: #13B2A3;">{customer_id}</b>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <a href="https://www.gomind.com.br">
                                                <img src="https://github.com/GrupoDomini/Public/blob/main/ASS_MIA.png?raw=true" alt="Go Mind" width="80%" height="auto" style="display: block; margin: auto;" />
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
        if result == 'sucesso':
            msg["Subject"] = f"Go Mind | Informativo RPA '{RPA}'- Sucesso"
            msg.attach(MIMEText(sucesso, "html"))
        elif result == 'start':
            msg["Subject"] = f"Go Mind | Informativo RPA '{RPA}'- Inicializou"
            msg.attach(MIMEText(start, "html"))
        elif result == 'sucesso' and aguarda_analise == True:
            msg["Subject"] = f"Go Mind | Informativo RPA '{RPA}'- Aguardando Análise"
            msg.attach(MIMEText(msg_aguarda, "html"))
        else:
            msg["Cco"] = "suporte@gomind.com.br"
            msg["Subject"] = f"Go Mind | Informativo RPA '{RPA}'- Erro"
            msg.attach(MIMEText(erro, "html"))


        text = msg.as_string().encode(encoding="latin-1", errors="strict")

        """Protocolo & segurança"""

        # Versão Microsoft
        s = smtplib.SMTP("smtp.office365.com: 587")  # Office365 Server
        password = "Xor36280"  # token app gerada na conta Google (mia@gomind.com.br)

        s.starttls()

        # Envio da mensagem
        s.login(msg["From"], password)
        if result == 'start':
            s.sendmail(msg["From"], msg["To"].split(",") + msg["Cc"].split(","), text)

        elif result == 'sucesso' and aguarda_analise == True:
            s.sendmail(
                msg["From"],
                msg["To"].split(",") + msg["Cc"].split(","),
                text,
            )
        elif result == 'sucesso':
            s.sendmail(
                msg["From"],
                msg["To"].split(",") + msg["Cc"].split(","),
                text,
            )
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

def log_email(
    log,
    msg_mail_to = "suporte@gomind.com.br",
    msg_mail_cc = "suporte@gomind.com.br",
    result=True,
    RPA="[Robô ainda não identificado]",
    ):
    
        date = datetime.now()
        
        try:
            """Corpo do e-mail"""
            sucesso = f"""
            <center>
            <p>Prezados,</p>
            <p><i>Esta é uma mensagem automática da <b>Mia.</b></i></p>
            
            <p>Registro de log do {RPA}.</p>

            <p>{date.strftime("[%Y/%m/%d %H:%M:%S]")} {log}</p>
            <br>

            Att, <b>Mia - Go Mind</b><br>
            Departamento de Tecnologia<br>
            <a href='https://www.gomind.com.br' title='Unlimited Growth'>www.gomind.com.br</a>
            </center>
            """

            # Endereços
            msg     = MIMEMultipart()
            msg["From"] = "mia@gomind.com.br"
            msg["To"] = msg_mail_to
            msg["Cc"] = msg_mail_cc

            # Assunto da mensagem
            if result:
                msg["Subject"] = f"Go Mind | Informativo RPA '{RPA}'- LOG"
                msg.attach(MIMEText(sucesso, "html"))
        
            text = msg.as_string().encode(encoding="latin-1", errors="strict")

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

