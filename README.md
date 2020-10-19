# minimail
## desafio 2 de la materia Redes 2020

### requerimientos:
 - Python 3
  ```bash
  pip install -r requirements.txt
  ```

### Uso:
#### `minimail.py` 
Pequeño script para enviar mails por consola (instrucciones provistas en el programa)
```bash
python minimail.py
```
#### Gateway:

Para escuchar peticiones HTTP ejecute `httpserver.py` (sin argumentos)
```bash
python httpserver.py
```
Este proceso quedará a la espera de un POST request en el puerto 8080 de localhost.
Para revisar los mails puede ejecute en otra consola el comando:
```bash
python -m smtpd -c DebuggingServer -n localhost:1025
```
Esto creará un servidor SMTP que quedara a la escucha del puerto 1025.
Para enviar requerimiento POST con el json puede utilizar `poster.py`
```bash
python poster.py
```
Ejecutelo y dicho programa cargará el archivo mail.json y lo enviara por POST al puerto 8080.
Al recibirlo `httpserver.py` llama al `mailer.py`, que recibe los datos y los envia por mail
utilizando SMTP.
Para verificarlo revise el servidor que esta corriendo en el puerto 1025.

