from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    html = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Calcul de Factorielle</title>
    </head>
    <body>
        <h1>Calcul de Factorielle</h1>
        <form method="POST">
            <label for="number">Entrez un nombre:</label>
            <input type="text" id="number" name="number" required>
            <button type="submit">Calculer</button>
        </form>
    """

    if request.method == 'POST':
        try:
            x = int(request.form['number'])
            F = 1
            for i in range(1, x + 1):
                F *= i
            result = f"Le factoriel de {x} est : {F}"
        except ValueError:
            result = "Ce n'est pas un nombre valide."

        html += f"<h2>{result}</h2>"

    html += "</body></html>"
    return html

if __name__ == '__main__':
    app.run(debug=True)