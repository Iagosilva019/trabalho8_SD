import requests

BASE_URL = "http://0.0.0.0:5000"

token = None


def login():
    global token

    username = input("Usuário: ")
    password = input("Senha: ")

    response = requests.post(
        f"{BASE_URL}/login",
        json={
            "username": username,
            "password": password
        }
    )

    print(response.json())

    if response.status_code == 200:
        token = response.json()["token"]


def send_message():

    destinatario = input("Destinatário: ")
    mensagem = input("Mensagem: ")

    response = requests.post(
        f"{BASE_URL}/send",
        headers={"Authorization": token},
        json={
            "destinatario": destinatario,
            "mensagem": mensagem
        }
    )

    print(response.json())


def read_messages():

    response = requests.get(
        f"{BASE_URL}/messages",
        headers={"Authorization": token}
    )

    print(response.json())


def admin_messages():

    response = requests.get(
        f"{BASE_URL}/admin/messages",
        headers={"Authorization": token}
    )

    print(response.json())


while True:

    print("\n1 - Login")
    print("2 - Enviar mensagem")
    print("3 - Ler mensagens")
    print("4 - Ver todas mensagens(admin)")
    print("0 - Sair")

    op = input("Opção: ")

    if op == "1":
        login()

    elif op == "2":
        send_message()

    elif op == "3":
        read_messages()

    elif op == "4":
        admin_messages()

    elif op == "0":
        break
