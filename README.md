# Azure Python Test

Ce dépôt contient des scripts Python pour tester l'authentification Azure avec différents services Azure en utilisant Microsoft Entra ID via `DefaultAzureCredential`.

## Scripts disponibles

1. **`src/main.py`** - Appelle le service Azure OpenAI (API Responses)
2. **`src/get_token.py`** - Récupère et affiche le token JWT pour Azure Database for PostgreSQL
3. **`src/get_app_details.py`** - Récupère les détails d'une application Azure via son appId (Microsoft Graph API)

## Prérequis

1. Python 3.9 ou supérieur.
2. Un compte Azure avec une authentification Entra ID configurée (par exemple, via `az login`).
3. Pour `main.py` : Un accès au service [Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/) et une ressource Azure OpenAI configurée.
4. Pour `get_token.py` : Un Service Principal avec les permissions appropriées pour Azure Database for PostgreSQL.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Sur Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## Configuration

Assurez-vous d'être connecté à Azure via la CLI pour que `DefaultAzureCredential` puisse obtenir un jeton valide :

```bash
az login
```

### Configuration pour main.py (Azure OpenAI)

Définissez les variables d'environnement suivantes (manuellement ou dans un fichier `.env`) :

```bash
export AZURE_OPENAI_ENDPOINT="https://<votre-ressource>.openai.azure.com"
export AZURE_OPENAI_DEPLOYMENT="gpt-4.1-nano"  # Remplacez par le nom de votre déploiement
export AZURE_OPENAI_TEST_PROMPT="Optionnel: votre prompt de test personnalisé"
```

Si vous utilisez un fichier `.env`, placez-le à la racine du projet avec le contenu ci-dessus.

## Exécution

### Script 1 : Azure OpenAI (main.py)

```bash
python src/main.py
```

Le script enverra un prompt de test en français (ou celui défini dans `AZURE_OPENAI_TEST_PROMPT`) au modèle et affichera la réponse JSON renvoyée par l'API.

### Script 2 : Récupération du token JWT (get_token.py)

```bash
python src/get_token.py
```

Le script récupérera un token JWT pour Azure Database for PostgreSQL et affichera :
- Le token complet
- Les informations décodées du token (Application ID, dates d'expiration, etc.)
- Le temps restant avant expiration
- Le payload complet au format JSON

### Script 3 : Détails d'une application Azure (get_app_details.py)

```bash
python src/get_app_details.py <appId>
```

**Exemple :**
```bash
# Pour obtenir les détails d'Azure CLI
python src/get_app_details.py 04b07795-8ddb-461a-bbee-02f9e1bf7b46
```

Le script interrogera Microsoft Graph API et affichera :
- Les informations de l'application (display name, publisher, sign-in audience, etc.)
- Les informations du service principal (app roles, OAuth2 scopes, etc.)
- Un message informatif si l'application n'est pas trouvée (applications Microsoft natives)

**Note :** Vous devez avoir les permissions Microsoft Graph appropriées :
- `Application.Read.All` ou `Directory.Read.All`

## Structure du projet

```
AzurePythonTest/
├── .gitignore              # Ignore .venv, __pycache__, .env, etc.
├── README.md               # Ce fichier
├── requirements.txt        # Dépendances Python
└── src/
    ├── main.py            # Script Azure OpenAI
    ├── get_token.py       # Script de récupération de token JWT
    └── get_app_details.py # Script d'interrogation Microsoft Graph
```

## Ressources

### Azure OpenAI
- [Cycle de vie des versions de l'API Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/api-version-lifecycle?tabs=python)
- [Documentation Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/)

### Authentification Azure
- [Authentification `DefaultAzureCredential`](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme#defaultazurecredential)
- [Azure Database for PostgreSQL - Microsoft Entra authentication](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-azure-ad-authentication)

### Microsoft Graph API
- [Microsoft Graph REST API](https://learn.microsoft.com/en-us/graph/api/overview)
- [Application resource type](https://learn.microsoft.com/en-us/graph/api/resources/application)
- [Service Principal resource type](https://learn.microsoft.com/en-us/graph/api/resources/serviceprincipal)
- [Verify first-party Microsoft applications](https://learn.microsoft.com/en-us/troubleshoot/azure/active-directory/verify-first-party-apps-sign-in)

### JWT
- [Introduction to JSON Web Tokens](https://jwt.io/introduction)
