# from _future_ import print_function
import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import imaplib
import email
from email.header import decode_header

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

email_user = "mariaj.gc95@gmail.com"
email_pass = "Tester1234!"
imap_server = "imap.gmail.com"


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        # Autorizar la aplicación sin abrir el navegador
        creds = authorize_headless()
        # Guardar las credenciales para el próximo uso
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        for label in labels:
            print(label['name'])

    except HttpError as error:
        # TODO(developer) - Handle errors from Gmail API.
        print(f'An error occurred: {error}')


def authorize_headless():
    from google_auth_oauthlib.flow import InstalledAppFlow

    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES,
        authorization_prompt_message='',
        success_message='The authentication flow has completed.',
        open_browser=False
    )
    creds = flow.run_local_server(port=0)

    return creds


def buscar_codigo(correo):
    # Aquí debes implementar la lógica para buscar el código en el contenido del correo.
    # Por ejemplo, puedes buscar un patrón específico en el cuerpo del correo.
    # Si encuentras el código, devuélvelo. De lo contrario, devuelve None.
    # Ejemplo:
    if "Codigo:" in correo:
        codigo = correo.split("Codigo:")[1].strip()
        return codigo
    else:
        return None


while True:
    # Conéctate al servidor IMAP de Gmail
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_user, email_pass)

    # Selecciona la bandeja de entrada
    mail.select("inbox")

    # Busca correos no leídos
    status, message_numbers = mail.search(None, "UNSEEN")

    # Procesa los correos no leídos
    for num in message_numbers[0].split():
        status, msg_data = mail.fetch(num, "(RFC822)")
        raw_email = msg_data[0][1].decode("utf-8")
        msg = email.message_from_string(raw_email)

        # Extrae el asunto del correo
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")

        # Analiza el contenido del correo en busca del código
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode()

                    # Busca el código en el cuerpo del correo
                    codigo = buscar_codigo(body)
                    if codigo:
                        print(f"Se encontró un código en el correo con asunto: {subject}")
                        print(f"Código: {codigo}")

    # Cierra la conexión
    mail.logout()

if __name__ == '_main_':
    main()
