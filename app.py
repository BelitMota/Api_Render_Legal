import os
import sqlite3

from flask import Flask, request, jsonify
from flask_cors import CORS


# ============================================================
# CRIAÇÃO DA APLICAÇÃO FLASK
# ============================================================
#
# Aqui criamos a aplicação principal do Flask.
#
# A variável "app" representa o nosso servidor web/API.
# É por meio dela que registramos as rotas, como:
#
#   GET /produtos
#   POST /produtos
#   PUT /produtos/1
#   DELETE /produtos/1
#
# No Render, normalmente usamos o comando:
#
#   gunicorn app:app
#
# Nesse comando:
# - o primeiro "app" é o nome do arquivo: app.py
# - o segundo "app" é esta variável abaixo: app = Flask(__name__)
#
app = Flask(__name__)


# ============================================================
# CORS
# ============================================================
#
# CORS significa Cross-Origin Resource Sharing.
#
# Ele é importante quando uma aplicação frontend, por exemplo um app Flutter Web,
# uma página HTML ou outro sistema, tenta consumir esta API a partir de outro
# endereço/origem.
#
# Para testes com Thunder Client ou Postman, o CORS geralmente não faz diferença.
# Porém, como este projeto pode ser usado depois com frontend, deixamos habilitado.
#
CORS(app)


# ============================================================
# CAMINHO DO BANCO SQLITE
# ============================================================
#
# Este projeto usa SQLite porque é simples para aula.
#
# O SQLite salva os dados em um arquivo local.
# Neste caso, o arquivo será chamado:
#
#   produtos.db
#
# Ele será criado na mesma pasta deste arquivo app.py.
#
# Observação importante sobre Render Free:
#
# No plano gratuito do Render, o arquivo SQLite pode funcionar para demonstração,
# mas não deve ser tratado como armazenamento permanente.
#
# Em caso de redeploy, reinicialização ou recriação do ambiente, os dados podem
# ser perdidos.
#
# Para uma aplicação real, o ideal seria usar um banco externo, como PostgreSQL.
#
DATABASE = os.path.join(os.path.dirname(__file__), "produtos.db")


def conectar_banco():
    """
    Cria uma conexão com o banco SQLite.

    Em SQLite, normalmente abrimos uma conexão, executamos os comandos SQL
    necessários e depois fechamos a conexão.

    A linha abaixo:

        conexao.row_factory = sqlite3.Row

    faz com que o resultado das consultas possa ser acessado pelo nome das
    colunas, como:

        linha["nome"]

    Em vez de acessar apenas por posição, como:

        linha[0]
        linha[1]

    Isso deixa o código mais legível para os alunos.
    """

    conexao = sqlite3.connect(DATABASE)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabela():
    """
    Cria a tabela de produtos, caso ela ainda não exista.

    O comando CREATE TABLE IF NOT EXISTS garante que:
    - se a tabela ainda não existir, ela será criada;
    - se a tabela já existir, o comando não causará erro.

    Campos da tabela:

    id:
        Identificador único do produto.
        É gerado automaticamente pelo banco.

    nome:
        Nome do produto.
        Campo obrigatório.

    preco:
        Preço do produto.
        Campo obrigatório.

    imagem:
        Link de uma imagem do produto.
        Campo opcional.

    usuario:
        Nome ou identificador do usuário dono daquele produto.
        Neste projeto simples, usamos esse campo como filtro didático.
        Assim, cada aluno pode cadastrar produtos usando seu próprio nome.
    """

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            imagem TEXT,
            usuario TEXT NOT NULL
        )
    """)

    conexao.commit() # formaliza a sua inserção, rollback é qnd da algum problema dando um retorno pro estágio anteriror do banco
    conexao.close()


def contar_produtos():
    """
    Conta quantos produtos existem no banco.

    Essa função será usada para decidir se devemos ou não inserir o seed.

    Seed significa "dados iniciais".
    Em projetos didáticos, o seed ajuda porque a API já começa com alguns
    registros prontos para testar as rotas GET.
    """

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM produtos")
    resultado = cursor.fetchone()

    conexao.close()

    return resultado["total"]


def inserir_seed():
    """
    Insere produtos iniciais no banco.

    Para evitar duplicação, só inserimos os produtos de exemplo se a tabela
    estiver vazia.

    Isso é importante porque a aplicação pode ser reiniciada várias vezes.
    Se inseríssemos o seed sempre, cada reinício criaria produtos repetidos.
    """

    total_produtos = contar_produtos()

    if total_produtos > 0:
        return

    produtos_iniciais = [
        (
            "Mouse USB",
            49.90,
            "https://picsum.photos/seed/mouse/300/200",
            "aluno1"
        ),
        (
            "Teclado ABNT2",
            89.90,
            "https://picsum.photos/seed/teclado/300/200",
            "aluno1"
        ),
        (
            "Monitor 24 polegadas",
            799.90,
            "https://picsum.photos/seed/monitor/300/200",
            "aluno2"
        ),
        (
            "Webcam Full HD",
            199.90,
            "https://picsum.photos/seed/webcam/300/200",
            "aluno2"
        ),
        (
            "Notebook",
            3499.90,
            "https://picsum.photos/seed/notebook/300/200",
            "professor"
        )
    ]

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.executemany("""
        INSERT INTO produtos (nome, preco, imagem, usuario)
        VALUES (?, ?, ?, ?)
    """, produtos_iniciais)

    conexao.commit()
    conexao.close()


@app.route("/", methods=["GET"])
def home():
    """
    Rota inicial da API.

    Esta rota serve como uma documentação rápida.
    Ela permite abrir a URL principal da API no navegador e verificar se a
    aplicação está funcionando.

    Exemplo:
        http://127.0.0.1:5000/

    No Render, a URL será parecida com:
        https://nome-do-projeto.onrender.com/
    """

    return jsonify({
        "mensagem": "API de produtos funcionando",
        "observacao": "Projeto simples com Flask, SQLite, CRUD e seed inicial.",
        "endpoints": {
            "listar_todos": "GET /produtos",
            "listar_por_usuario": "GET /produtos?usuario=aluno1",
            "buscar": "GET /produtos/{id}",
            "criar": "POST /produtos",
            "atualizar": "PUT /produtos/{id}",
            "remover": "DELETE /produtos/{id}"
        }
    })


@app.route("/produtos", methods=["GET"])
def listar_produtos():
    """
    Lista os produtos cadastrados.

    Esta rota aceita um parâmetro opcional chamado "usuario".

    Exemplos:

        GET /produtos
        Lista todos os produtos.

        GET /produtos?usuario=aluno1
        Lista apenas os produtos do usuário "aluno1".

    Esse filtro é útil para a aula porque permite que vários alunos usem a mesma
    API e filtrem apenas os seus próprios produtos.
    """

    usuario = request.args.get("usuario")

    conexao = conectar_banco()
    cursor = conexao.cursor()

    if usuario:
        cursor.execute(
            "SELECT * FROM produtos WHERE usuario = ? ORDER BY id DESC",
            (usuario,)
        )
    else:
        cursor.execute("SELECT * FROM produtos ORDER BY id DESC")

    produtos = []

    for linha in cursor.fetchall():
        produtos.append(dict(linha))

    conexao.close()

    return jsonify(produtos)


@app.route("/produtos/<int:id>", methods=["GET"])
def buscar_produto(id):
    """
    Busca um produto específico pelo ID.

    O trecho <int:id> na rota indica que o Flask espera um número inteiro
    naquela posição da URL.

    Exemplo:
        GET /produtos/1

    Se o produto existir, a API retorna seus dados.
    Se não existir, a API retorna erro 404.
    """

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
    produto = cursor.fetchone()

    conexao.close()

    if produto is None:
        return jsonify({"erro": "Produto não encontrado"}), 404

    return jsonify(dict(produto))


@app.route("/produtos", methods=["POST"])
def criar_produto():
    """
    Cria um novo produto.

    Esta rota espera receber um JSON no corpo da requisição.

    Exemplo de JSON:

    {
        "nome": "Cadeira Gamer",
        "preco": 899.90,
        "imagem": "https://picsum.photos/seed/cadeira/300/200",
        "usuario": "aluno1"
    }

    Campos obrigatórios:
    - nome
    - preco
    - usuario

    Campo opcional:
    - imagem
    """

    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "JSON não enviado"}), 400

    nome = dados.get("nome")
    preco = dados.get("preco")
    imagem = dados.get("imagem")
    usuario = dados.get("usuario")

    if not nome or preco is None or not usuario:
        return jsonify({
            "erro": "Campos obrigatórios: nome, preco e usuario"
        }), 400

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO produtos (nome, preco, imagem, usuario)
        VALUES (?, ?, ?, ?)
    """, (nome, preco, imagem, usuario))

    conexao.commit()

    novo_id = cursor.lastrowid

    conexao.close()

    return jsonify({
        "id": novo_id,
        "nome": nome,
        "preco": preco,
        "imagem": imagem,
        "usuario": usuario
    }), 201


@app.route("/produtos/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    """
    Atualiza um produto existente.

    Esta rota espera receber todos os dados principais do produto.

    Exemplo:
        PUT /produtos/1

    Body JSON:

    {
        "nome": "Mouse Gamer",
        "preco": 129.90,
        "imagem": "https://picsum.photos/seed/mouse-gamer/300/200",
        "usuario": "aluno1"
    }

    Neste projeto simples, o PUT substitui os dados principais do produto.
    """

    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "JSON não enviado"}), 400

    nome = dados.get("nome")
    preco = dados.get("preco")
    imagem = dados.get("imagem")
    usuario = dados.get("usuario")

    if not nome or preco is None or not usuario:
        return jsonify({
            "erro": "Campos obrigatórios: nome, preco e usuario"
        }), 400

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE produtos
        SET nome = ?, preco = ?, imagem = ?, usuario = ?
        WHERE id = ?
    """, (nome, preco, imagem, usuario, id))

    conexao.commit()

    linhas_afetadas = cursor.rowcount

    conexao.close()

    if linhas_afetadas == 0:
        return jsonify({"erro": "Produto não encontrado"}), 404

    return jsonify({
        "id": id,
        "nome": nome,
        "preco": preco,
        "imagem": imagem,
        "usuario": usuario
    })


@app.route("/produtos/<int:id>", methods=["DELETE"])
def remover_produto(id):
    """
    Remove um produto pelo ID.

    Exemplo:
        DELETE /produtos/1

    Se o produto existir, ele será removido.
    Se não existir, a API retornará erro 404.
    """

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))
    conexao.commit()

    linhas_afetadas = cursor.rowcount

    conexao.close()

    if linhas_afetadas == 0:
        return jsonify({"erro": "Produto não encontrado"}), 404

    return jsonify({"mensagem": "Produto removido com sucesso"})


# ============================================================
# INICIALIZAÇÃO DO BANCO
# ============================================================
#
# Quando a aplicação inicia, executamos duas etapas:
#
# 1. criar_tabela()
#    Garante que a tabela produtos exista.
#
# 2. inserir_seed()
#    Insere produtos iniciais, mas somente se a tabela estiver vazia.
#
criar_tabela()
inserir_seed()


if __name__ == "__main__":
    # Este bloco é executado apenas quando rodamos localmente com:
    #
    #   python app.py
    #
    # No Render, quem executa a aplicação é o Gunicorn, usando:
    #
    #   gunicorn app:app
    #
    app.run(debug=True)
