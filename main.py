from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

lista_produtos = [
    {"id": 1, "nome": "notebook", "preco": 10},
    {"id": 2, "nome": "smartphone", "preco": 20},
    {"id": 3, "nome": "tablet", "preco": 100},
    {"id": 4, "nome": "monitor", "preco": 1000},
]


# Rotas
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Home", header="Pagina Inicial")


@app.route("/produtos")
def listar_produtos():
    produto = request.args.get("search")
    resultSearch = []

    for p in lista_produtos:
        if produto and p["nome"] == produto.lower():
            resultSearch.append(p)

    return render_template(
        "produtos.html",
        title="Produtos",
        header="Lista de Produtos",
        produtos=lista_produtos,
        search=produto,
        resultSearch=resultSearch,
    )


@app.route("/produtos/criar", methods=["GET", "POST"])
def criar_produto():
    if request.method == "POST":
        novo_produto = {
            "id": max([p["id"] for p in lista_produtos], default=0) + 1,
            "nome": request.form["nome"].strip().lower(),
            "preco": float(request.form["preco"]),
        }
        lista_produtos.append(novo_produto)
        return redirect(url_for("listar_produtos"))

    return render_template(
        "criarProduto.html", title="Criar Produto", header="Cadastrar Produto"
    )


@app.route("/produtos/editar/<int:id>", methods=["GET", "POST"])
def editar_produto(id):
    produto = None
    for p in lista_produtos:
        if p["id"] == id:
            produto = p
            break

    if produto is None:
        return render_template("404.html", title="404", header="Não encontrado"), 404

    if request.method == "POST":
        produto["nome"] = request.form["nome"].strip().lower()
        produto["preco"] = float(request.form["preco"])
        return redirect(url_for("listar_produtos"))

    return render_template(
        "editarProduto.html",
        title="Editar Produto",
        header="Editar Produto",
        produto=produto,
    )


@app.route("/produtos/deletar/<int:id>", methods=["POST"])
def deletar_produto(id):
    produto_encontrado = None
    for p in lista_produtos:
        if p["id"] == id:
            produto_encontrado = p
            break

    if produto_encontrado is None:
        return render_template("404.html", title="404", header="Não encontrado"), 404

    lista_produtos.remove(produto_encontrado)
    return redirect(url_for("listar_produtos"))


@app.route("/produtos/<int:produto_id>")
def produto(produto_id):
    return f"Produto: {produto_id}"


if __name__ == "__main__":
    app.run(debug=True)
