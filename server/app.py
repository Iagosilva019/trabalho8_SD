from flask import Flask, request, jsonify
from database import create_tables, connect
from auth import hash_password, generate_token, validate_token
from crypto import encrypt_message, decrypt_message
from datetime import datetime

app = Flask(__name__)

create_tables()


@app.route("/login", methods=["POST"])
def login():

    data = request.json

    username = data["username"]
    password = data["password"]

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT senha_hash,papel FROM usuarios WHERE username=?",
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    if not user:
        return jsonify({"erro": "Usuário não encontrado"}), 401

    if hash_password(password) != user[0]:
        return jsonify({"erro": "Senha inválida"}), 401

    token = generate_token(username, user[1])

    return jsonify({"token": token})


@app.route("/send", methods=["POST"])
def send_message():

    token = request.headers.get("Authorization")

    session = validate_token(token)

    if not session:
        return jsonify({"erro": "Token inválido"}), 401

    data = request.json

    destinatario = data["destinatario"]
    mensagem = data["mensagem"]

    mensagem_cifrada = encrypt_message(mensagem)

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO mensagens(
        remetente,
        destinatario,
        conteudo_cifrado,
        timestamp
        )
        VALUES(?,?,?,?)
        """,
        (
            session["username"],
            destinatario,
            mensagem_cifrada,
            datetime.now().isoformat()
        )
    )

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Enviada com sucesso"})


@app.route("/messages", methods=["GET"])
def read_messages():

    token = request.headers.get("Authorization")

    session = validate_token(token)

    if not session:
        return jsonify({"erro": "Token inválido"}), 401

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT remetente,
        conteudo_cifrado,
        timestamp
        FROM mensagens
        WHERE destinatario=?
        """,
        (session["username"],)
    )

    messages = cursor.fetchall()

    conn.close()

    result = []

    for msg in messages:
        result.append({
            "remetente": msg[0],
            "mensagem": decrypt_message(msg[1]),
            "timestamp": msg[2]
        })

    return jsonify(result)


@app.route("/admin/messages", methods=["GET"])
def admin_messages():

    token = request.headers.get("Authorization")

    session = validate_token(token)

    if not session:
        return jsonify({"erro": "Token inválido"}), 401

    if session["role"] != "admin":
        return jsonify({"erro": "Acesso negado"}), 403

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT remetente,
        destinatario,
        conteudo_cifrado,
        timestamp
        FROM mensagens
        """
    )

    messages = cursor.fetchall()

    conn.close()

    result = []

    for msg in messages:
        result.append({
            "remetente": msg[0],
            "destinatario": msg[1],
            "mensagem": decrypt_message(msg[2]),
            "timestamp": msg[3]
        })

    return jsonify(result)


@app.route("/admin/create-user", methods=["POST"])
def create_user():

    token = request.headers.get("Authorization")

    session = validate_token(token)

    if not session:
        return jsonify({"erro": "Token inválido"}), 401

    if session["role"] != "admin":
        return jsonify({"erro": "Acesso negado"}), 403

    data = request.json

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO usuarios VALUES(?,?,?)",
        (
            data["username"],
            hash_password(data["password"]),
            data["papel"]
        )
    )

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Usuário criado"})


@app.route("/admin/active-users", methods=["GET"])
def active_users():

    token = request.headers.get("Authorization")

    session = validate_token(token)

    if not session:
        return jsonify({"erro": "Token inválido"}), 401

    if session["role"] != "admin":
        return jsonify({"erro": "Acesso negado"}), 403

    return jsonify(list(set(
        value["username"]
        for value in validate_token.__globals__["tokens"].values()
    )))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
