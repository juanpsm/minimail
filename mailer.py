import json
import smtplib, ssl

def send(post_data):
    # Convertimos los datos a dict
    data = json.loads(post_data)
    
    port = 1025
    smtp_server = "localhost"
    
    print('Creando servidor..')
    server = smtplib.SMTP(smtp_server,port)
    
    receiver_email = data['json_payload']["envelope"]["to"][0]
    sender_email = data['json_payload']["envelope"]["from"]
    msg = data['json_payload']["data"]
    # Mandar Email
    try:
        print(f"OK.\nEnviar mail de {sender_email} a {receiver_email}.")
        print(f"\nMensaje:\n{'*'*30}\n{msg}\n{'*'*30}\n")
        server.sendmail(sender_email, receiver_email, msg)
        print(f"OK.\nRevisa el servidor!!")
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()

if __name__ == "__main__":
    # Prueba para cargar un json
    with open('mail.json') as json_file:
        data = json.load(json_file)
    print('data:\n', data, '\ntipo: ',type(data))
    data = {'json_payload': data}
    st = json.dumps(data)
    print('string:\n', st, '\ntipo: ',type(st))
    send(st)

