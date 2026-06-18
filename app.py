from flask import Flask, request
import sqlite3
import pandas as pd

app = Flask(__name__)
@app.route("/teste")
def teste():
    return "<h1>Nova rota funcionando!</h1>"
@app.route("/fluido")
def fluido():

    transmissao = request.args.get("transmissao", "")
    modelo = request.args.get("modelo", "")
    ano = request.args.get("ano", "")
    motor = request.args.get("motor", "")
    conn = sqlite3.connect("oleocambio.db")

    sql = """
    SELECT *
    FROM tb_fluido
    WHERE TRANSMISSAO LIKE ?
    """

    df = pd.read_sql(
        sql,
        conn,
        params=[f"%{transmissao}%"]
    )

    conn.close()

    if len(df) == 0:
        return f"""
    <html>

    <head>
        <title>Fluido não encontrado</title>
    </head>

    <body style="font-family: Arial; background-color:#f4f6f9;">

        <div style="
            width:600px;
            margin:40px auto;
            background:white;
            padding:30px;
            border-radius:10px;
            box-shadow:0px 0px 10px rgba(0,0,0,0.15);
        ">

            <h1>⚠ Fluido não encontrado</h1>

            <p>
                Nenhum fluido foi localizado para a transmissão:
                <b>{transmissao}</b>
            </p>

            <br>

            <a href="/"
               style="
                    padding:12px 20px;
                    background:#0066cc;
                    color:white;
                    text-decoration:none;
                    border-radius:5px;
               ">
               🔎 Nova Consulta
            </a>

        </div>

    </body>

    </html>
    """

    linha = df.iloc[0]

    return f"""
<html>

<head>

<title>Resultado da Consulta</title>

<style>

body {{
    font-family: Arial;
    background-color: #f4f6f9;
}}

.container {{
    width: 600px;
    margin: 40px auto;
    background: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.15);
}}

h1 {{
    color: #003366;
}}

.info {{
    margin-bottom: 15px;
    font-size: 18px;
}}

.botao {{
    display: inline-block;
    padding: 12px 20px;
    background: #0066cc;
    color: white;
    text-decoration: none;
    border-radius: 5px;
}}

</style>

</head>

<body>

<div class="container">

<h1>🚗 Resultado da Consulta</h1>

<div class="info">
<b>Veículo:</b><br>
{modelo}
</div>

<div class="info">
<b>Ano:</b><br>
{ano}
</div>

<div class="info">
<b>Motorização:</b><br>
{motor}
</div>

<hr>

<div class="info">
<b>Transmissão:</b><br>
{linha['TRANSMISSAO']}
</div>

<div class="info">
<b>Fluido Recomendado:</b><br>
{linha['FLUIDO_RECOMENDADO']}
</div>

<div class="info">
<b>Quantidade:</b><br>
{linha['QUANTIDADE']}
</div>

<div class="info">
<b>Código FEBI:</b><br>
{linha['CODIGO_FEBI']}
</div>

<div class="info">
<b>Período de Troca:</b><br>
{linha['PERIODO_TROCA']}
</div>

<br>

<a class="botao" href="/">🔎 Nova Consulta</a>

</div>

</body>

</html>
"""
@app.route("/")
def inicio():

    modelo = request.args.get("modelo", "")

    html = f"""
    <html>
    <head>
        <title>Gutos Car - Consulta de Óleo de Câmbio</title>

        <style>

            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f6f9;
                margin: 0;
            }}

            .container {{
                width: 90%;
                max-width: 1200px;
                margin: 30px auto;
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(0,0,0,0.15);
            }}

            h1 {{
                color: #003366;
            }}

            input {{
                padding: 10px;
                width: 300px;
                font-size: 16px;
            }}

            button {{
                padding: 10px 20px;
                background: #0066cc;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}

            th {{
                background: #003366;
                color: white;
                padding: 10px;
            }}

            td {{
                border: 1px solid #ddd;
                padding: 8px;
            }}

            tr:nth-child(even) {{
                background: #f2f2f2;
            }}

        </style>

    </head>

    <body>

        <div class="container">

            <h1>🚗 Gutos Car Autopeças</h1>

            <h2>Consulta de Óleo de Câmbio</h2>

            <form method="get">

                <input
                    type="text"
                    name="modelo"
                    placeholder="Digite o modelo"
                    value="{modelo}"
                >

                <button type="submit">
                    Consultar
                </button>

            </form>

            <hr>
    """

    if modelo:

        conn = sqlite3.connect("oleocambio.db")

        sql = """
        SELECT *
        FROM tb_aplicacao
        WHERE MODELO LIKE ?
        LIMIT 50
        """

        df = pd.read_sql(
            sql,
            conn,
            params=[f"%{modelo.upper()}%"]
        )

        conn.close()

        if len(df) == 0:

            html += "<p>Nenhum veículo encontrado.</p>"

        else:

            html += "<h3>Resultados</h3>"

            html += """
            <table>
            <tr>
                <th>Modelo</th>
                <th>Ano</th>
                <th>Motorização</th>
                <th>Transmissão</th>
                <th>Ação</th>
            </tr>
            """

            for _, row in df.iterrows():

                transmissao = str(row["MODELO_TRANSMISSAO"]).split(",")[0]

                html += f"""
                <tr>
                    <td>{row['MODELO']}</td>
                    <td>{row['ANO']}</td>
                    <td>{row['MOTORIZACAO']}</td>
                    <td>{row['MODELO_TRANSMISSAO']}</td>
                    <td>
                        <a href="/fluido?transmissao={transmissao}&modelo={row['MODELO']}&ano={row['ANO']}&motor={row['MOTORIZACAO']}">
                            🔍 Consultar Fluido
                        </a>
                    </td>
                </tr>
                """

            html += "</table>"
    html += """
        </div>

    </body>

    </html>
    """

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
