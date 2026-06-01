# Sistema de Comunicação Segura entre Processos Distribuídos

## Descrição

Este projeto implementa um sistema distribuído de troca de mensagens entre processos utilizando Python, atendendo aos requisitos de autenticação, criptografia e controle de acesso.

O sistema é composto por:

* **Servidor Central (Flask)**: responsável pela autenticação dos usuários, armazenamento das mensagens e controle de acesso.
* **Cliente**: realiza login, envia mensagens e consulta mensagens recebidas.
* **Banco de Dados SQLite**: armazena usuários e mensagens.
* **Criptografia Fernet**: protege as mensagens durante o armazenamento e transmissão.

---

## Arquitetura

```text
Cliente A
    |
    | HTTP/JSON
    v
+------------------+
| Servidor Flask   |
|                  |
| Autenticação     |
| Controle Acesso  |
| Criptografia     |
+------------------+
    |
    v
SQLite Database
    |
    v
Cliente B
```

---

## Tecnologias Utilizadas

* Python 3
* Flask
* SQLite3
* Cryptography (Fernet)
* Requests
* Hashlib (SHA-256)
* Secrets

---

## Recursos de Segurança Implementados

### 1. Autenticação

* Usuários cadastrados no banco SQLite.
* Senhas armazenadas utilizando hash SHA-256.
* Geração de token de sessão após login.
* Todas as requisições protegidas utilizam token no cabeçalho Authorization.

### 2. Criptografia

* Utilização do algoritmo Fernet da biblioteca Cryptography.
* Todas as mensagens são criptografadas antes de serem armazenadas.
* Apenas o destinatário recebe a mensagem descriptografada.

### 3. Controle de Acesso

#### Usuário comum

* Enviar mensagens.
* Ler apenas suas próprias mensagens.

#### Administrador

* Enviar mensagens.
* Ler suas próprias mensagens.
* Ler mensagens de qualquer usuário.
* Cadastrar novos usuários.
* Visualizar usuários ativos.

---

## Estrutura do Projeto

```text
projeto/
│
├── server/
│   ├── app.py
│   ├── auth.py
│   ├── crypto.py
│   ├── database.py
│   └── key.key
│
├── client/
│   └── client.py
│
├── requirements.txt
└── README.md
```

---

## Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git

cd seu-repositorio
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## Executando o Servidor

Abra um terminal:

```bash
cd server

python app.py
```

Saída esperada:

```text
* Running on http://0.0.0.0:5000
```

O servidor ficará aguardando conexões dos clientes.

---

## Executando o Cliente

Abra outro terminal:

```bash
cd client

python client.py
```

Menu exibido:

```text
1 - Login
2 - Enviar mensagem
3 - Ler mensagens
4 - Ver todas mensagens(admin)
0 - Sair
```

---

## Usuários Padrão

### Administrador

```text
Usuário: admin
Senha: admin123
```

### Usuário João

```text
Usuário: joao
Senha: 123456
```

### Usuário Maria

```text
Usuário: maria
Senha: 654321
```

---

## Fluxo de Demonstração

### 1. Login inválido

Tentar login com senha incorreta.

Exemplo:

```text
Usuário: joao
Senha: 111111
```

Resultado:

```text
401 Unauthorized
```

---

### 2. Login válido

Exemplo:

```text
Usuário: joao
Senha: 123456
```

Resultado:

```text
Token gerado com sucesso.
```

---

### 3. Envio de mensagem

João envia uma mensagem para Maria.

Exemplo:

```text
Destinatário: maria
Mensagem: Olá Maria
```

Resultado:

```text
Mensagem enviada com sucesso.
```

---

### 4. Leitura de mensagens

Maria realiza login e consulta suas mensagens.

Resultado:

```text
Remetente: joao
Mensagem: Olá Maria
```

---

### 5. Tentativa de acesso indevido

João tenta acessar:

```http
GET /admin/messages
```

Resultado:

```text
403 Forbidden
```

---

### 6. Acesso administrativo

Administrador realiza login.

Exemplo:

```text
Usuário: admin
Senha: admin123
```

Acessa:

```http
GET /admin/messages
```

Resultado:

```text
Visualização de todas as mensagens do sistema.
```

---

### 7. Verificação da Criptografia

Abrir o banco SQLite:

```bash
cd server

sqlite3 database.db
```

Consultar mensagens:

```sql
SELECT * FROM mensagens;
```

Exemplo:

```text
1|joao|maria|gAAAAAB...
```

Observe que o conteúdo armazenado está criptografado e não pode ser lido diretamente.

---

## Endpoints Disponíveis

### Login

```http
POST /login
```

---

### Enviar Mensagem

```http
POST /send
```

---

### Ler Mensagens

```http
GET /messages
```

---

### Ver Todas as Mensagens (Admin)

```http
GET /admin/messages
```

---

### Criar Usuário (Admin)

```http
POST /admin/create-user
```

---

### Usuários Ativos (Admin)

```http
GET /admin/active-users
```

---

## Dependências

Conteúdo do arquivo `requirements.txt`:

```text
Flask
cryptography
requests
```

---

## Autor

Trabalho desenvolvido para a disciplina de Sistemas Distribuídos, demonstrando os conceitos de autenticação, criptografia, controle de acesso e comunicação segura entre processos distribuídos.
