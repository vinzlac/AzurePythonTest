# Azure OpenAI GPT-4o Sample (Python)

Ce dépôt contient un petit script Python qui appelle le service Azure OpenAI (modèle GPT-4o) en utilisant l'authentification Microsoft Entra ID via `DefaultAzureCredential`.

## Prérequis

1. Python 3.9 ou supérieur.
2. Un compte Azure avec un accès au service [Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/).
3. Une ressource Azure OpenAI configurée avec un déploiement du modèle `gpt-4o`.
4. Une authentification Entra ID configurée (par exemple, via `az login`).

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Sur Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## Configuration

Définissez les variables d'environnement suivantes (manuellement ou dans un fichier `.env`).

```bash
export AZURE_OPENAI_ENDPOINT="https://<votre-point-de-termination>.azure.com"
export AZURE_OPENAI_DEPLOYMENT="gpt-4o"
```

Si vous utilisez un fichier `.env`, placez-le à la racine du projet avec le contenu ci-dessus.

Assurez-vous également d'être connecté à Azure via la CLI pour que `DefaultAzureCredential` puisse obtenir un jeton valide :

```bash
az login
```

## Exécution

```bash
python src/main.py
```

Le script enverra un prompt de test en français au modèle GPT-4o et affichera la réponse de l'assistant.

## Ressources

- [Cycle de vie des versions de l'API Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/api-version-lifecycle?tabs=python)
- [Authentification `DefaultAzureCredential`](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme#defaultazurecredential)
