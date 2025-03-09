from flask import Flask, request
import threading

# Première application Flask (pour la factorielle)
app1 = Flask(__name__)

@app1.route('/factorielle', methods=['GET', 'POST'])
def factorielle():
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

# Deuxième application Flask (pour Hello World)
app2 = Flask(__name__)

@app2.route('/')
def hello_world():
    return 'Hello, World!'


# Fonction pour exécuter la première application
def run_app1():
    app1.run(host="0.0.0.0", port=5000, debug=True)

# Fonction pour exécuter la deuxième application
def run_app2():
    app2.run(host="127.0.0.1", port=5001, debug=True)


# Exécution des deux applications dans des threads différents
if __name__ == '__main__':
    thread1 = threading.Thread(target=run_app1)
    thread2 = threading.Thread(target=run_app2)
    
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

