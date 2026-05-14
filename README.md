# API Simples de Produtos com Flask, SQLite e Seed

Este projeto é uma API REST simples desenvolvida com **Python**, **Flask** e **SQLite**.

A API permite realizar um CRUD de produtos:

- listar produtos;
- buscar produto por ID;
- cadastrar produto;
- atualizar produto;
- remover produto.

O projeto também possui um **seed inicial**, ou seja, alguns produtos são inseridos automaticamente no banco quando a aplicação é executada pela primeira vez.

---

## 1. Objetivo do projeto

O objetivo deste projeto é servir como exemplo didático para uma aula introdutória de backend.

A proposta é mostrar, de maneira simples:

- como criar uma API com Flask;
- como usar rotas HTTP;
- como receber e devolver JSON;
- como salvar dados em SQLite;
- como testar a API com Thunder Client ou Postman;
- como subir uma API simples no Render.

Este projeto evita estruturas mais complexas, como:

- Blueprints;
- autenticação;
- JWT;
- SQLAlchemy;
- migrations;
- arquitetura em múltiplas camadas.

A ideia é que o aluno consiga enxergar todo o funcionamento da API em um único arquivo principal.

---

## 2. Estrutura do projeto

```text
api-produtos/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## 3. Arquivos do projeto

### 3.1. `app.py`

Arquivo principal da aplicação.

Ele contém:

- criação da aplicação Flask;
- configuração do CORS;
- conexão com o banco SQLite;
- criação da tabela `produtos`;
- inserção dos dados iniciais;
- rotas da API;
- execução local da aplicação.

---

### 3.2. `requirements.txt`

Arquivo com as dependências do projeto.

Conteúdo esperado:

```txt
Flask
flask-cors
gunicorn
```

---

### 3.3. `README.md`

Arquivo de documentação do projeto.

---

## 4. Banco de dados

O projeto usa SQLite.

O banco será criado automaticamente em um arquivo chamado:

```text
produtos.db
```

Esse arquivo será criado na mesma pasta do `app.py`.

---

## 5. Tabela `produtos`

A tabela possui os seguintes campos:

```text
id
nome
preco
imagem
usuario
```

### Explicação dos campos

| Campo | Tipo | Explicação |
|---|---|---|
| `id` | INTEGER | Identificador único do produto |
| `nome` | TEXT | Nome do produto |
| `preco` | REAL | Preço do produto |
| `imagem` | TEXT | Link de imagem do produto |
| `usuario` | TEXT | Nome ou identificador do usuário dono do produto |

---

## 6. Seed inicial

Seed significa **dados iniciais**.

Quando a aplicação inicia, ela verifica se a tabela `produtos` está vazia.

Se estiver vazia, alguns produtos são cadastrados automaticamente:

```text
Mouse USB
Teclado ABNT2
Monitor 24 polegadas
Webcam Full HD
Notebook
```

Cada produto também possui um campo `usuario`, por exemplo:

```text
aluno1
aluno2
professor
```

Isso permite testar filtros como:

```text
GET /produtos?usuario=aluno1
```

---

## 7. Instalação local

### 7.1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
cd api-produtos
```

---

### 7.2. Criar ambiente virtual

No Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

No Linux, macOS ou WSL:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 7.3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 7.4. Executar o projeto

```bash
python app.py
```

A API ficará disponível em:

```text
http://127.0.0.1:5000
```

---

## 8. Executando no Render

No Render, as configurações principais são:

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
gunicorn app:app
```

---

## 9. Sobre o comando `gunicorn app:app`

O comando:

```bash
gunicorn app:app
```

significa:

```text
gunicorn arquivo:variavel
```

Neste projeto:

- `app.py` é o arquivo;
- `app = Flask(__name__)` é a variável da aplicação Flask.

Portanto:

```text
app:app
```

significa:

```text
arquivo app.py : variável app
```

Localmente, podemos executar com:

```bash
python app.py
```

No Render, usamos:

```bash
gunicorn app:app
```

---

## 10. Observação sobre SQLite no Render

Este projeto usa SQLite por simplicidade didática.

No plano gratuito do Render, o arquivo SQLite pode não ser persistente.

Isso significa que os dados podem ser perdidos em situações como:

- novo deploy;
- reinício do serviço;
- recriação do ambiente;
- inatividade do serviço gratuito.

Para uma aplicação real, o ideal seria usar um banco persistente externo, como PostgreSQL.

Para esta aula, o SQLite é suficiente porque o foco está em:

- API REST;
- rotas;
- JSON;
- CRUD;
- deploy simples;
- testes com Thunder Client ou Postman.

---

## 11. Endpoints da API

### 11.1. Rota inicial

```text
GET /
```

Retorna uma mensagem de funcionamento da API e uma lista dos endpoints disponíveis.

---

### 11.2. Listar todos os produtos

```text
GET /produtos
```

Exemplo de resposta:

```json
[
  {
    "id": 1,
    "nome": "Mouse USB",
    "preco": 49.9,
    "imagem": "https://picsum.photos/seed/mouse/300/200",
    "usuario": "aluno1"
  }
]
```

---

### 11.3. Listar produtos por usuário

```text
GET /produtos?usuario=aluno1
```

Essa rota retorna apenas os produtos associados ao usuário informado.

---

### 11.4. Buscar produto por ID

```text
GET /produtos/1
```

Se o produto existir, a API retorna os dados do produto.

Se não existir, retorna erro `404`.

---

### 11.5. Criar produto

```text
POST /produtos
```

Body JSON:

```json
{
  "nome": "Cadeira Gamer",
  "preco": 899.90,
  "imagem": "https://picsum.photos/seed/cadeira/300/200",
  "usuario": "aluno1"
}
```

Campos obrigatórios:

```text
nome
preco
usuario
```

Campo opcional:

```text
imagem
```

---

### 11.6. Atualizar produto

```text
PUT /produtos/1
```

Body JSON:

```json
{
  "nome": "Mouse Gamer",
  "preco": 129.90,
  "imagem": "https://picsum.photos/seed/mouse-gamer/300/200",
  "usuario": "aluno1"
}
```

---

### 11.7. Remover produto

```text
DELETE /produtos/1
```

Se o produto existir, ele será removido.

Se não existir, a API retorna erro `404`.

---

## 12. Ordem sugerida para testar no Thunder Client ou Postman

### 12.1. Testar a API

```text
GET /
```

---

### 12.2. Listar produtos iniciais

```text
GET /produtos
```

A resposta já deve trazer os produtos do seed.

---

### 12.3. Filtrar por usuário

```text
GET /produtos?usuario=aluno1
```

---

### 12.4. Buscar um produto

```text
GET /produtos/1
```

---

### 12.5. Criar um produto

```text
POST /produtos
```

Body:

```json
{
  "nome": "Cadeira Gamer",
  "preco": 899.90,
  "imagem": "https://picsum.photos/seed/cadeira/300/200",
  "usuario": "aluno1"
}
```

---

### 12.6. Atualizar o produto criado

```text
PUT /produtos/6
```

Body:

```json
{
  "nome": "Cadeira Gamer Atualizada",
  "preco": 999.90,
  "imagem": "https://picsum.photos/seed/cadeira-atualizada/300/200",
  "usuario": "aluno1"
}
```

Observação: o ID pode variar conforme os registros existentes no banco.

---

### 12.7. Remover um produto

```text
DELETE /produtos/6
```

---

## 13. Exemplos de JSON

### Produto simples

```json
{
  "nome": "Produto Teste",
  "preco": 10.50,
  "imagem": "https://picsum.photos/seed/teste/300/200",
  "usuario": "aluno1"
}
```

### Produto sem imagem

```json
{
  "nome": "Produto Sem Imagem",
  "preco": 25.00,
  "usuario": "aluno2"
}
```

---

## 14. Conceitos abordados

Este projeto permite trabalhar os seguintes conceitos:

- API REST;
- métodos HTTP;
- JSON;
- Flask;
- SQLite;
- seed inicial;
- CRUD;
- parâmetros de URL;
- consulta por ID;
- filtro por usuário;
- status HTTP;
- deploy no Render;
- uso de Gunicorn.

---

## 15. Melhorias possíveis

Este projeto é propositalmente simples.

Em uma aplicação mais completa, poderíamos adicionar:

- autenticação com JWT;
- usuários reais no banco;
- validação mais robusta;
- banco PostgreSQL;
- separação em Blueprints;
- camada de serviço;
- camada de repositório;
- testes automatizados;
- paginação;
- busca por nome;
- tratamento mais detalhado de erros.

Por enquanto, a prioridade é compreender o fluxo básico:

```text
requisição HTTP -> rota Flask -> banco SQLite -> resposta JSON
```
