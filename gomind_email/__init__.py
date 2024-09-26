"""All utils from gomind robot

Raises:
    RuntimeError: _description_
"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from datetime import datetime
from typing import Literal
from gomind_cli import get_sys_args_as_dict
from dotenv import load_dotenv
import os

load_dotenv()
CLI_ARGUMENTS = get_sys_args_as_dict()

ANO_MIA = CLI_ARGUMENTS.get("competenceYear")
MES_MIA = CLI_ARGUMENTS.get("competenceMonth")

MAIL_PASSWD = os.environ.get("MAIL_PASSWD")

if not MAIL_PASSWD:
    raise Exception("Variável de ambiente MAIL_PASSWD não definida")


try:
    from getmac import get_mac_address as gma  # type: ignore

    mac_address = gma()
except Exception as e:
    raise ImportError("Erro ao importar get_mac_address") from e


def enviar_email(
    msg_mail_to,
    msg_mail_cc="",
    customer_id="",
    result=Literal['start', 'aguarda_analise', 'sucesso', 'erro'],
    RPA="[Robô ainda não identificado]",
):
    try:
        """Corpo do e-mail"""
        if MES_MIA is None or ANO_MIA is None:
            competencia = ''
        else:
            competencia = f"para a competência {MES_MIA}/{ANO_MIA}"
            
        if result == 'start':
            mensagem = {
                "msg": f"""<b>Esta é uma mensagem automática da MIA. 🚀</b></br></br>
                        O {RPA} {competencia}</br>
                        já foi iniciado. Estamos cuidando de tudo por aqui,</br> 
                        e assim que tivermos o resultado, você será o primeiro(a) a saber!</br></br>

                        Fique tranquilo(a), nossa automação está trabalhando para garantir que tudo corra perfeitamente. Até mais!</br></br>""",
                "img": "https://raw.githubusercontent.com/GrupoDomini/Public/a9e6e32a17c4ab0a59561041c547a0f5303f3b26/head_start.png",
                "subject": f"Go Mind | Informativo RPA '{RPA}'- Iniciado"
            }
        elif result == 'aguarda_analise':
            mensagem = {
                "msg": f"""
                        <b>Esta é uma mensagem automática da MIA.</b>🚨</br></br>
                        O {RPA} identificou</br>
                        algumas pendências que precisam ser analisadas por você. 🗂️</br>
                        Para verificar os detalhes e tomar as ações necessárias, acesse o <a style="color: #0D2B5B;" href="https://portalmia.app"><b>Portal Mia</b></a></br>
                """,
                "img": "https://raw.githubusercontent.com/GrupoDomini/Public/a9e6e32a17c4ab0a59561041c547a0f5303f3b26/head_aguarda.png",
                "subject": f"Go Mind | Informativo RPA '{RPA}'- Aguardando Análise"
                }
        elif result == 'sucesso':
            mensagem = {
                'msg':f"""
                    <b>Esta é uma mensagem automática da MIA.</b> 🎉</br></br>
                    Boas notícias! A automação {RPA}</br>
                    {competencia} foi concluída com sucesso. ✅</br>
                    Para mais detalhes, é só acessar o <a style="color: #0D2B5B;" href="https://portalmia.app"><b>Portal Mia</b></a></br>
                    Até a próxima!</br>
                """,
                'img': "https://raw.githubusercontent.com/GrupoDomini/Public/a9e6e32a17c4ab0a59561041c547a0f5303f3b26/head_sucess.png",
                'subject': f"Go Mind | Informativo RPA '{RPA}'- Concluído"
                }
        else:
            mensagem = {
                'msg':f"""
                    <b>Esta é uma mensagem automática da MIA.</b>🚨</br></br>
                    A automação {RPA}</br>
                    {competencia} encontrou um problema e não foi concluída. 😬</br>
                    Sugerimos que você acesse o <a style="color: #0D2B5B;" href="https://portalmia.app"><b>Portal Mia</b></a> para mais detalhes e orientações.</br></br>
                    Conte com a gente para resolver isso! </br></br>
                    
                    <p><em style="font-size: 90%;">Por favor, não responda a este e-mail, pois ele é enviado automaticamente.</em></p>
                """,
                'img': "https://raw.githubusercontent.com/GrupoDomini/Public/refs/heads/main/Cópia%20de%20head%20(1).png",
                'subject': f"Go Mind | Informativo RPA '{RPA}'- Não concluído"
                }
        
        corpo = f"""
            <table style="width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #dddddd;">
                <tr>
                    <td>
                        <!-- Cabeçalho -->
                        <table style="width: 100%; background-color: #ffffff; padding: 5px; font-family: Arial, sans-serif;">
                            <tr>
                                <td style="text-align: center;">
                                    <img src="{mensagem['img']}" alt="Logo da Empresa" style="max-width: 100%;">
                                </td>
                            </tr>
                        <!-- Corpo do E-mail -->
                        <table style="width: 100%; padding: 10px; font-family: Arial, sans-serif; background-color: #ffffff;">

                            <tr>
                                <td td style="padding: 15px 0 30px 0; color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 25px; text-align: center;">
                                    <p>
                                        {mensagem['msg']}
                                    </p>
                                </td>
                            </tr>
                        </table>

                        <!-- Rodapé -->
                        <table style="width: 100%; background-color: #ffffff; padding: -5px; font-family: Arial, sans-serif; text-align: center;">
                            <tr>
                                <td style="text-align: center;">
                                    <a href="https://gomind.com.br">
                                        <img src="https://github.com/GrupoDomini/Public/blob/main/footermail.png?raw=true" alt="Rodapé GoMind" style="max-width: 100%;">
                                    </a>
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
        if result in ['start', 'sucesso', 'aguarda_analise']:
            msg["Subject"] = f'{mensagem["subject"]}'
            msg.attach(MIMEText(corpo, "html"))
        elif result == 'erro':
            msg["Cco"] = "suporte@gomind.com.br"
            msg["Subject"] = f'{mensagem["subject"]}'
            msg.attach(MIMEText(corpo, "html"))


        text = msg.as_string().encode(encoding="latin-1", errors="strict")

        """Protocolo & segurança"""

        # Versão Microsoft
        s = smtplib.SMTP("smtp.office365.com: 587")  # Office365 Server
        password = MAIL_PASSWD

        s.starttls()

        # Envio da mensagem
        s.login(msg["From"], password)
        if result in ['start', 'sucesso', 'aguarda_analise']:
            s.sendmail(msg["From"], msg["To"].split(",") + msg["Cc"].split(","), text)
        elif result == 'erro':
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
            password = MAIL_PASSWD  # token app gerada na conta Google (mia@gomind.com.br)

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
