from flask import Flask, request, redirect, url_for
import numpy as np

app = Flask(__name__)

# Fonction pour calculer le coefficient de diffusion et l'erreur relative
def calcul_diffusion(x_A, D_AB0, D_BA0, phi_A, phi_B, lambda_A, lambda_B, theta_BA, theta_AB, theta_AA, theta_BB, tau_AB, tau_BA, q_A, q_B):
    x_B = 1 - x_A  
    ln_D_AB0 = np.log(D_AB0)  
    ln_D_BA0 = np.log(D_BA0)  
    first_term = x_B * ln_D_AB0 + x_A * ln_D_BA0
    second_term = 2 * (x_A * np.log(x_A / phi_A) + x_B * np.log(x_B / phi_B))
    third_term = 2 * x_A * x_B * (
        (phi_A / x_A) * (1 - lambda_A / lambda_B) + 
        (phi_B / x_B) * (1 - lambda_B / lambda_A)
    )
    fourth_term = x_B * q_A * (
        (1 - theta_BA**2) * np.log(tau_BA) + 
        (1 - theta_BB**2) * np.log(tau_AB) * tau_AB
    )
    fifth_term = x_A * q_B * (
        (1 - theta_AB**2) * np.log(tau_AB) + 
        (1 - theta_AA**2) * np.log(tau_BA) * tau_BA
    )
    
    ln_D_AB = first_term + second_term + third_term + fourth_term + fifth_term
    D_AB = np.exp(ln_D_AB)
    
    # Valeur expérimentale pour le calcul de l'erreur
    D_exp = 1.33e-5  
    error = abs(D_AB - D_exp) / D_exp * 100  
    
    return D_AB, error

# Page d'accueil
@app.route('/')
def home():
    return """
        <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Calculateur de Diffusion</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; }
                    h1 { text-align: center; margin-top: 50px; }
                    p { text-align: center; font-size: 1.2em; }
                    button { padding: 10px 20px; font-size: 1.2em; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
                    button:hover { background-color: #45a049; }
                    .container { text-align: center; margin-top: 100px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Hello, I am Fatima Mouhieddine</h1>
                    <p>Welcome to the diffusion coefficient application.</p>
                    <a href='/page2'><button>Suivant</button></a>
                </div>
            </body>
        </html>
    """

# Page formulaire
@app.route('/page2', methods=['GET'])
def page2():
    return """
        <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Input Form</title>
                <style>
                    body { font-family: Arial, sans-serif; background-color: #f9f9f9; }
                    h1 { text-align: center; margin-top: 50px; }
                    form { width: 80%; margin: 0 auto; }
                    label, input { font-size: 1em; margin: 10px 0; display: block; width: 100%; }
                    input[type="text"] { padding: 10px; }
                    button { padding: 10px 20px; font-size: 1.2em; background-color: #4CAF50; color: white; border: none; cursor: pointer; margin-top: 20px; }
                    button:hover { background-color: #45a049; }
                </style>
            </head>
            <body>
                <h1>Input the values</h1>
                <form action='/page3' method='post'>
                    <label for='x_A'>Fraction molaire de A (x_A):</label>
                    <input type='text' name='x_A' value='0.25' required><br><br>
                    <label for='D_AB0'>Coefficient de diffusion initial D_AB0:</label>
                    <input type='text' name='D_AB0' value='2.1e-5' required><br><br>
                    <label for='D_BA0'>Coefficient de diffusion initial D_BA0:</label>
                    <input type='text' name='D_BA0' value='2.67e-5' required><br><br>
                    <label for='phi_A'>Phi A (φ_A):</label>
                    <input type='text' name='phi_A' value='0.279' required><br><br>
                    <label for='phi_B'>Phi B (φ_B):</label>
                    <input type='text' name='phi_B' value='0.746' required><br><br>
                    <label for='lambda_A'>Lambda A (λ_A):</label>
                    <input type='text' name='lambda_A' value='1.127' required><br><br>
                    <label for='lambda_B'>Lambda B (λ_B):</label>
                    <input type='text' name='lambda_B' value='0.973' required><br><br>
                    <label for='theta_BA'>Theta BA (θ_BA):</label>
                    <input type='text' name='theta_BA' value='0.612' required><br><br>
                    <label for='theta_AB'>Theta AB (θ_AB):</label>
                    <input type='text' name='theta_AB' value='0.261' required><br><br>
                    <label for='theta_AA'>Theta AA (θ_AA):</label>
                    <input type='text' name='theta_AA' value='0.388' required><br><br>
                    <label for='theta_BB'>Theta BB (θ_BB):</label>
                    <input type='text' name='theta_BB' value='0.739' required><br><br>
                    <label for='tau_AB'>Tau AB (τ_AB):</label>
                    <input type='text' name='tau_AB' value='1.035' required><br><br>
                    <label for='tau_BA'>Tau BA (τ_BA):</label>
                    <input type='text' name='tau_BA' value='0.5373' required><br><br>
                    <label for='q_A'>q_A:</label>
                    <input type='text' name='q_A' value='1.432' required><br><br>
                    <label for='q_B'>q_B:</label>
                    <input type='text' name='q_B' value='1.4' required><br><br>
                    <button type='submit'>Calculate</button>
                </form>
            </body>
        </html>
    """

# Page résultat
@app.route('/page3', methods=['POST'])
def page3():
    try:
        x_A = float(request.form['x_A'].replace(',', '.'))
        D_AB0 = float(request.form['D_AB0'])
        D_BA0 = float(request.form['D_BA0'])
        phi_A = float(request.form['phi_A'])
        phi_B = float(request.form['phi_B'])
        lambda_A = float(request.form['lambda_A'])
        lambda_B = float(request.form['lambda_B'])
        theta_BA = float(request.form['theta_BA'])
        theta_AB = float(request.form['theta_AB'])
        theta_AA = float(request.form['theta_AA'])
        theta_BB = float(request.form['theta_BB'])
        tau_AB = float(request.form['tau_AB'])
        tau_BA = float(request.form['tau_BA'])
        q_A = float(request.form['q_A'])
        q_B = float(request.form['q_B'])

        D_AB, error = calcul_diffusion(x_A, D_AB0, D_BA0, phi_A, phi_B, lambda_A, lambda_B, theta_BA, theta_AB, theta_AA, theta_BB, tau_AB, tau_BA, q_A, q_B)
        
        return f"""
            <html>
                <body>
                    <h1>Here is the result</h1>
                    <p>Le coefficient de diffusion D_AB est : {D_AB:.6e} cm²/s</p>
                    <p>L'erreur relative par rapport à la valeur expérimentale est : {error:.2f} %</p>
                    <a href="/">Return to home</a>
                </body>
            </html>
        """
    except ValueError:
        return """
            <html>
                <body>
                    <h1>Invalid input values. Please enter valid numbers.</h1>
                    <a href="/page2">Back to form</a>
                </body>
            </html>
        """

# Gestion des erreurs pour les routes inexistantes
@app.errorhandler(404)
def page_not_found(e):
    return """
        <html>
            <body>
                <h1>Hello, I am Fatima Mouhieddine,  a PIC12 student</h1>
                <p>Welcome to the diffusion coefficient application.</p>
                <p style='color: red;'>La page demandée n'existe pas. Vous avez été redirigé vers l'accueil.</p>
                <a href='/page2'><button>Suivant</button></a>
            </body>
        </html>
    """, 404

if __name__ == '__main__':
    app.run(debug=True)




