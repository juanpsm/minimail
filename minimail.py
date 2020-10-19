import smtplib, ssl
from getpass import getpass
import cry

HELP = f'''
\t\t\t\tBienvenido a MiniMail™!
\t(v.0.1)
\tEste pequeño programa sirve para enviar un mail desde la consola tutilizando
\tel protocolo SMTP.

\tPara ello cuenta con tres opciones:

\t    - 'debug'    De esta manera se puede testear el envío del email
\t                 utilizando un servidor de prueba que escucha un puerto del
\t                 localhost, recibe los emails y muestra la información.

\t    - 'SSL'      Iniciar una conexión SMTP que es segura desde el principio.

\t    - 'starttls' Iniciar una conexión SMTP no segura que luego se puede cifrar
\t                 usando la función .starttls\n'''

def enviar_mail(opt, msg):
    my_email = "developingwithpython@gmail.com"
    sender_email = my_email
    receiver_email = "juampi56@gmail.com"

    if opt == "debug":
        # run in console
        # python -m smtpd -c DebuggingServer -n localhost:1025
        ask_debug = "\nEn una consola ejecuta el siguiente comando:\n\n"\
                    "\tpython -m smtpd -c DebuggingServer -n localhost:1025\n\n"\
                    "Ingresa 'cancel' para salir o 'continuar' cuando tengas el\n"\
                    "sevidor de pruebas listo\n\n>> "
        choice = input(ask_debug)
        while choice not in ('cancel', 'continuar'):
            choice = input(ask_debug)
        if choice == "cancel":
            return False
        port = 1025
        smtp_server = "localhost"
        print(f"\nCreando servidor SMTP en {smtp_server} puerto {port}")
        server = smtplib.SMTP(smtp_server,port)
        msg += "\n(es solo una prueba)"

    elif opt in ("SSL", "starttls"):
        smtp_server = "smtp.gmail.com"
        msg += "\n(mensaje enviado desde python usando "

        # Create a secure SSL context
        print(f"\nCreando contexto SSL seguro")
        context = ssl.create_default_context()
        print(f"OK.\n")

        # SSL
        if opt == "SSL":
            port = 465
            print(f"\nIniciando conexión SMTP segura en '{smtp_server}', puerto: {port}")
            server = smtplib.SMTP_SSL(smtp_server, port, context=context)
            msg += "SSL)"
        # starttls
        elif opt == "starttls":
            port = 587
            print(f"\nIniciando conexión SMTP NO segura en '{smtp_server}', puerto: {port}")
            server = smtplib.SMTP(smtp_server,port)
            print(f"OK.\nCifrando conexión con starttls")
            server.starttls(context=context)
            msg += "starttls)"
        else:
            print(f"No se reconoce la opción {opt}")
            return False

        print("OK.\n")
        ask_email = "\nPara enviar el mail de veras, necesitas una cuenta de Gmail. También deberás \n"\
                    "configurar el acceso de aplicaciones no seguras en el siguiente enlace:\n"\
                    "\n\thttps://myaccount.google.com/lesssecureapps"\
                    "\n\n(ingresa 'omitir' para usar una cuenta por defecto)\n\n>> "
        logueado = False
        while not logueado:
            email = input(ask_email)
            while not email:
                print("¡Debes ingresar un email!")
                email = input(ask_email)
            if email not in ("omitir", "o", "O"):
                passw = getpass(prompt=f"Ingresa tu password para '{email}':\n\n>> ")
                while not passw:
                    print("¡Debes ingresar un password!")
                    passw = getpass(prompt=f"Ingresa tu password para '{email}':\n\n>> ")
                sender_email = email
                password = passw
            else:
                ask_pwd = f"\nUtilizaremos una creada con el único propósito de probar esta aplicación.\n"\
                        "Ingresa la constraseña que he proporcionado con la entrega:\n\n>> "
                passw = getpass(prompt=ask_pwd)
                while not passw:
                    print("¡Debes ingresar una contraseña!")
                    passw = getpass(prompt=ask_pwd)
                sender_email = my_email
                password = cry.get(passw)

            # Iniciado el servidor, inicio sesión
            print(f"OK.\n\nIniciar sesión como {sender_email}")
            try:
                server.login(sender_email, password)
                logueado = True
            except UnicodeEncodeError:
                print("Contraseña incorrecta :(\nIntentalo nuevamente o de otra manera.\n")
            except smtplib.SMTPAuthenticationError as e:
                print(e)
                print("Error de autenticación :(\nIntentalo nuevamente o de otra manera.\n")
            except Exception as e:
                print(e)
                print("Intentalo nuevamente o de otra manera.\n")
                return False
    print(f"OK.\n\nFROM:  <{sender_email}>\n")
    to = input("¿A quién quieres enviar el mail?\n"\
                f"(Por defecto me lo enviarás a {receiver_email})\n\n>> ")
    if to:
        receiver_email = to
    print(f"TO:  <{receiver_email}>\n")
    # Mandar Email
    print(f"OK.\nEnviar mail a {receiver_email}.")
    print(f"\nMensaje:\n{'*'*30}\n{msg}\n{'*'*30}\n")
    try:
        server.sendmail(sender_email, receiver_email, msg)
        print(f"OK. Message sent! Bye, bye!")
        server.quit()
        return True
    except Exception as e:
        # Print any error messages to stdout
        print(e)
        server.quit()
        return False

if __name__ == "__main__":
    subject = "Subject: "
    continuar = True
    opciones = {'1': 'debug', '2': 'SSL', '3': 'starttls'}
    str_opciones = "\n"
    for key, value in opciones.items():
        str_opciones += f"\t{key}.  {value}\t"
    str_opciones += "\n\n('exit' para cancelar): "


    print(HELP)
    opcion = input(f"Selecciona el metodo:\n\t{str_opciones}\n\n>> ")
    continuar = opcion != 'exit'
    while continuar:
        while opcion not in opciones:
            print(f"'{opcion}' no es una opción válida...")
            opcion = input(str_opciones+"\n\n>> ")
        if opcion == 'exit':
            exit(0)

        print("\nVamos a redactar el mail.")
        msj = input("\nIngresa el asunto :\n\n[Enter] para continuar\n>> ")
        if len(msj) == 0:
            msj = "Asunto por defecto"
            print(f"\nSUBJECT: {msj}")
        subject += f"{msj}\n\n"
        msj = input(f"\nOK.\nIngresa el cuerpo del mensaje:\n\n[Enter] para continuar\n>> ")
        if len(msj) == 0:
            msj = "Cuerpo por defecto"
            print(f"\nDATA: {msj}\nOK.")
        mensaje = subject + msj

        exito = enviar_mail(opciones[opcion], mensaje)
        if not exito:
            print("No se ha podido enviar el mensaje :(")

        print("\n¿Quieres intentarlo de nuevo?")
        opcion = input(f"Metodo:\n{str_opciones}")
        continuar = opcion != 'exit'