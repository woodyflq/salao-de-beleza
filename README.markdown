# Sistema de Agendamentos de Salão de Beleza

E aí, beleza? Esse aqui é um sistema maneiro feito com Django pra ajudar a gerenciar os agendamentos do seu salão de beleza. Dá pra controlar clientes, serviços, a equipe, os agendamentos e até tirar um relatório dos serviços que foram feitos direitinho.

## O Que Você Vai Precisar
- Python 3.11 ou uma versão mais nova
- Git (pra baixar o código)

## Como Instalar e Rodar na Sua Máquina

### 1. Baixa o Código
Primeiro, clona o repositório pra sua máquina:
```bash
git clone https://github.com/woodyflq/salao-de-beleza.git
cd salao-de-beleza
```
Isso pega tudo que tá no GitHub e joga na sua pasta.

### 2. Cria e Ativa um Ambiente Virtual
Vamos criar um cantinho separado pra instalar as coisas e evitar bagunça:
- No Windows:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- No macOS/Linux:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
Quando der certo, você vai ver `(venv)` no começo do prompt do terminal.

### 3. Instala as Coisas Necessárias
Instala as dependências que tão listadas no `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Configura o Banco de Dados
Deixa o banco de dados pronto com os comandos de migração:
```bash
python manage.py migrate
```
Isso cria as tabelas que o sistema precisa.

### 5. Cria um Superusuário (Se Quiser Entrar no Admin)
Pra mexer no painel de admin, cria um superusuário:
```bash
python manage.py createsuperuser
```
Aí ele vai pedir um nome de usuário, e-mail e senha.

### 6. Liga o Servidor
Roda o servidor pra ver o sistema funcionando:
```bash
python manage.py runserver
```

### 7. Entra no Sistema
- Abre o navegador e vai em `http://127.0.0.1:8000/salon/` pra ver as páginas principais.
- Se quiser mexer no admin, vai em `http://127.0.0.1:8000/admin/` e usa o login do superusuário que você criou.

### 8. Coloca Dados de Exemplo (Opcional)
Se quiser encher o banco com dados fake pra testar, roda esse script:
```bash
python populate_db.py
```
Ele cria clientes, serviços, equipe e agendamentos.

## O Que Esse Sistema Faz
- **Gerencia Clientes**: Vê e controla clientes com paginação e escolhe quantos mostrar por página.
- **Gerencia Serviços**: Adiciona e vê serviços com duração e preço, com paginação.
- **Gerencia Equipe**: Cuida dos membros da equipe com especialidades, também com paginação.
- **Agendamentos**: Faz e acompanha agendamentos (Agendado, Concluído, Cancelado), com paginação.
- **Relatórios**: Mostra serviços concluídos num período (a data final já vem como hoje por padrão).
- **Botão Admin**: Tem um botãozinho na barra de cima pra ir direto pro painel de admin.

## Dicas de Performance
- Tem índices nas colunas mais usadas (`email`, `appointment_time`, `status`) pra ficar mais rápido.
- Usa `select_related` pra não sobrecarregar o banco com muitas consultas.
- A paginação ajuda quando tiver muita coisa pra mostrar.
