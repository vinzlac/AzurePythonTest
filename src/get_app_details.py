"""Script pour récupérer les détails d'une application Azure via son appId en utilisant Microsoft Graph API."""

from __future__ import annotations

import sys
import requests
from azure.identity import DefaultAzureCredential


def get_application_by_appid(appid: str, access_token: str) -> dict | None:
    """Récupère les détails d'une application via Microsoft Graph API."""
    url = f"https://graph.microsoft.com/v1.0/applications?$filter=appId eq '{appid}'"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data.get('value') and len(data['value']) > 0:
            return data['value'][0]
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la requête à Microsoft Graph: {e}")
        return None


def get_service_principal_by_appid(appid: str, access_token: str) -> dict | None:
    """Récupère les détails d'un service principal via Microsoft Graph API."""
    url = f"https://graph.microsoft.com/v1.0/servicePrincipals?$filter=appId eq '{appid}'"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data.get('value') and len(data['value']) > 0:
            return data['value'][0]
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la requête à Microsoft Graph: {e}")
        return None


def display_application_info(app: dict) -> None:
    """Affiche les informations d'une application."""
    print("\n" + "=" * 80)
    print("📱 INFORMATIONS DE L'APPLICATION")
    print("=" * 80)
    print(f"Display Name:          {app.get('displayName', 'N/A')}")
    print(f"Application ID:        {app.get('appId', 'N/A')}")
    print(f"Object ID:             {app.get('id', 'N/A')}")
    print(f"Publisher Domain:      {app.get('publisherDomain', 'N/A')}")
    print(f"Sign-in Audience:      {app.get('signInAudience', 'N/A')}")
    
    if app.get('description'):
        print(f"Description:           {app['description']}")
    
    # Propriétaire(s)
    if app.get('createdDateTime'):
        print(f"Créée le:              {app['createdDateTime']}")
    
    # Identifiers URIs
    if app.get('identifierUris'):
        print(f"Identifier URIs:       {len(app['identifierUris'])} URI(s)")
        for uri in app['identifierUris']:
            print(f"  - {uri}")
    
    # Tags
    if app.get('tags'):
        print(f"Tags:                  {', '.join(app['tags'])}")
    
    print("=" * 80)


def display_service_principal_info(sp: dict) -> None:
    """Affiche les informations d'un service principal."""
    print("\n" + "=" * 80)
    print("🤖 INFORMATIONS DU SERVICE PRINCIPAL")
    print("=" * 80)
    print(f"Display Name:          {sp.get('displayName', 'N/A')}")
    print(f"Application ID:        {sp.get('appId', 'N/A')}")
    print(f"Object ID:             {sp.get('id', 'N/A')}")
    print(f"Service Principal Type: {sp.get('servicePrincipalType', 'N/A')}")
    print(f"Enabled:               {'✅ Oui' if sp.get('accountEnabled') else '❌ Non'}")
    
    if sp.get('homepage'):
        print(f"Homepage:              {sp['homepage']}")
    
    if sp.get('appOwnerOrganizationId'):
        print(f"Owner Org ID:          {sp['appOwnerOrganizationId']}")
    
    # App Roles
    if sp.get('appRoles'):
        print(f"App Roles:             {len(sp['appRoles'])} role(s)")
        for role in sp['appRoles'][:5]:  # Max 5 roles
            print(f"  - {role.get('displayName', 'N/A')}: {role.get('value', 'N/A')}")
        if len(sp['appRoles']) > 5:
            print(f"  ... et {len(sp['appRoles']) - 5} autres roles")
    
    # Tags
    if sp.get('tags'):
        print(f"Tags:                  {', '.join(sp['tags'])}")
    
    # OAuth2 Permission Scopes
    if sp.get('oauth2PermissionScopes'):
        print(f"OAuth2 Scopes:         {len(sp['oauth2PermissionScopes'])} scope(s)")
        for scope in sp['oauth2PermissionScopes'][:5]:  # Max 5 scopes
            print(f"  - {scope.get('value', 'N/A')}: {scope.get('adminConsentDisplayName', 'N/A')}")
        if len(sp['oauth2PermissionScopes']) > 5:
            print(f"  ... et {len(sp['oauth2PermissionScopes']) - 5} autres scopes")
    
    print("=" * 80)


def main() -> None:
    """Point d'entrée principal."""
    # Récupérer l'appId depuis les arguments de ligne de commande
    if len(sys.argv) < 2:
        print("Usage: python get_app_details.py <appId>")
        print("\nExemple:")
        print("  python get_app_details.py 04b07795-8ddb-461a-bbee-02f9e1bf7b46")
        sys.exit(1)
    
    appid = sys.argv[1]
    
    print(f"🔍 Recherche des détails pour l'Application ID: {appid}\n")
    
    # Obtenir un token pour Microsoft Graph
    try:
        credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
        token_result = credential.get_token("https://graph.microsoft.com/.default")
        access_token = token_result.token
        print("✅ Token Microsoft Graph obtenu avec succès!\n")
    except Exception as e:
        print(f"❌ Erreur lors de l'obtention du token Microsoft Graph: {e}")
        print("\nAssurez-vous d'être connecté avec 'az login' et d'avoir les permissions nécessaires.")
        sys.exit(1)
    
    # Rechercher l'application
    print("🔎 Recherche de l'application...")
    app = get_application_by_appid(appid, access_token)
    
    if app:
        display_application_info(app)
    else:
        print("ℹ️  Aucune application trouvée avec cet appId.")
        print("   (Cela peut être normal pour les applications Microsoft natives)")
    
    # Rechercher le service principal
    print("\n🔎 Recherche du service principal...")
    sp = get_service_principal_by_appid(appid, access_token)
    
    if sp:
        display_service_principal_info(sp)
    else:
        print("ℹ️  Aucun service principal trouvé avec cet appId dans ce tenant.")
        print("   (Normal pour les applications externes ou Microsoft natives)")
    
    if not app and not sp:
        print("\n" + "=" * 80)
        print("⚠️  INFORMATION")
        print("=" * 80)
        print("Cet appId pourrait correspondre à:")
        print("  1. Une application Microsoft native (Azure CLI, PowerShell, etc.)")
        print("  2. Une application d'un autre tenant Azure")
        print("  3. Un appId invalide ou supprimé")
        print("\nPour les applications Microsoft connues, consultez:")
        print("  https://learn.microsoft.com/en-us/troubleshoot/azure/active-directory/verify-first-party-apps-sign-in")
        print("=" * 80)


if __name__ == "__main__":
    main()

