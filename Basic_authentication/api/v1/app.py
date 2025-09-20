#!/usr/bin/env python3

"""
Route module for the API
Ce fichier est le point d'entrée principal de l'API Flask.
Il gère :
- L'enregistrement des routes
- L'activation du CORS
- La configuration de l'authentification
- Le filtrage des requêtes avant traitement
- La gestion des erreurs HTTP
"""
from os import getenv                # Pour récupérer les variables d'environnement
from api.v1.views import app_views   # Blueprint contenant les routes de l'API
from flask import Flask, jsonify, abort, request  # Outils Flask pour serveur et requêtes
from flask_cors import (CORS, cross_origin)       # Pour activer le CORS
import os
from api.v1.auth.auth import Auth    # Classe d'authentification générique
from api.v1.auth.basic_auth import BasicAuth  # Authentification basique (user/pass)

# Création de l'application Flask
app = Flask(__name__)

# Enregistrement des routes définies dans le blueprint "app_views"
app.register_blueprint(app_views)

# Activation du CORS sur toutes les routes commençant par /api/v1/
# "origins": "*" signifie que toutes les origines sont autorisées (pratique pour un front séparé)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Variable globale pour stocker l'instance d'authentification
auth = None

# Lecture du type d'authentification depuis une variable d'environnement
AUTH_TYPE = getenv("AUTH_TYPE")

# Choix de l'authentification en fonction de AUTH_TYPE
if AUTH_TYPE == 'basic_auth':
    auth = BasicAuth()  # Authentification avec login/mot de passe via header HTTP
else:
    auth = Auth()       # Authentification basique personnalisée

@app.before_request
def before_request():
    """
    Fonction exécutée AVANT chaque requête reçue.
    Sert à filtrer l'accès aux routes en fonction de l'authentification.
    """
    if auth is None:
        return  # Si aucune authentification n'est configurée, on laisse passer

    # Liste des routes qui ne nécessitent PAS d'authentification
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]

    # Si la route actuelle n'est pas protégée → on continue
    if not auth.require_auth(request.path, excluded_paths):
        return

    # Si aucun header Authorization n'est présent → on renvoie 401 Unauthorized
    if auth.authorization_header(request) is None:
        abort(401)

    # Si le header est présent mais l'utilisateur est invalide → 403 Forbidden
    if auth.current_user(request) is None:
        abort(403)

@app.errorhandler(404)
def not_found(error) -> str:
    """
    Gestion centralisée de l'erreur 404 (Not Found)
    Retourne un JSON clair avec un code HTTP 404
    """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized_error(error):
    """
    Gestion centralisée de l'erreur 401 (Unauthorized)
    Retourne un JSON clair avec un code HTTP 401
    """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden_error(error):
    """
    Gestion centralisée de l'erreur 403 (Forbidden)
    Retourne un JSON clair avec un code HTTP 403
    """
    return jsonify({"error": "Forbidden"}), 403

@app.route('/api/v1/unauthorized', methods=['GET'])
def trigger_unauthorized():
    """
    Route spéciale pour tester une erreur 401 Unauthorized
    Quand on l'appelle, elle déclenche volontairement un abort(401)
    """
    abort(401)

# Lancement de l'application Flask si le script est exécuté directement
if __name__ == "__main__":
    # Lecture de l'hôte et du port depuis les variables d'environnement
    # Valeurs par défaut : 0.0.0.0:5000
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")

    # Démarrage du serveur Flask
    app.run(host=host, port=port)
