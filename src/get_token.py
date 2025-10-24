"""Script pour récupérer et afficher le token JWT pour Azure PostgreSQL."""

from __future__ import annotations

import json
import base64
from datetime import datetime
from azure.identity import DefaultAzureCredential

# Applications Azure connues
KNOWN_AZURE_APPS = {
    "04b07795-8ddb-461a-bbee-02f9e1bf7b46": "Azure CLI",
    "1950a258-227b-4e31-a9cf-717495945fc2": "Azure PowerShell",
    "e9f49c6b-5ce5-44c8-925d-015017e9f7ad": "Visual Studio 2022",
    "872cd9fa-d31f-45e0-9eab-6e460a02d1f1": "Visual Studio",
    "0c1307d4-29d6-4389-a11c-5cbe7f65d7fa": "Azure Data Studio",
    "c44b4083-3bb0-49c1-b47d-974e53cbdf3c": "Azure Portal",
    "89bee1f7-5e6e-4d8a-9f3d-ecd601259da7": "Office 365 Management",
}


def decode_jwt_payload(token: str) -> dict:
    """Décode la partie payload d'un token JWT (sans vérification de signature)."""
    try:
        # Un JWT a 3 parties séparées par des points: header.payload.signature
        parts = token.split('.')
        if len(parts) != 3:
            return {}
        
        # Décoder le payload (partie centrale)
        payload = parts[1]
        
        # Ajouter le padding nécessaire pour base64
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding
        
        # Décoder de base64
        decoded_bytes = base64.urlsafe_b64decode(payload)
        decoded_str = decoded_bytes.decode('utf-8')
        
        # Parser le JSON
        return json.loads(decoded_str)
    except Exception as e:
        print(f"Erreur lors du décodage du token: {e}")
        return {}


def format_timestamp(timestamp: int) -> str:
    """Convertit un timestamp Unix en date lisible."""
    try:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return "Invalid timestamp"


def main() -> None:
    """Récupère et affiche le token JWT pour Azure Database for PostgreSQL."""
    print("🔐 Récupération du token JWT pour Azure Database for PostgreSQL...\n")
    
    # Créer le credential
    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
    
    # Scope pour Azure Database for PostgreSQL
    scope = "https://ossrdbms-aad.database.windows.net/.default"
    
    try:
        # Récupérer le token
        token_result = credential.get_token(scope)
        access_token = token_result.token
        
        print("✅ Token récupéré avec succès!\n")
        print("=" * 80)
        print("TOKEN JWT:")
        print("=" * 80)
        print(access_token)
        print("=" * 80)
        print()
        
        # Décoder et afficher les informations du token
        payload = decode_jwt_payload(access_token)
        
        if payload:
            print("📋 Informations du token:")
            print("-" * 80)
            
            # Type d'identité
            if 'idtyp' in payload:
                idtyp = payload['idtyp']
                if idtyp == 'user':
                    print(f"Type d'identité:       👤 Utilisateur (user)")
                elif idtyp == 'app':
                    print(f"Type d'identité:       🤖 Service Principal (app)")
                else:
                    print(f"Type d'identité:       {idtyp}")
                print()
            
            # Informations utilisateur (si c'est un user token)
            if 'upn' in payload:
                print(f"User Principal Name:   {payload['upn']}")
            if 'name' in payload:
                print(f"Nom:                   {payload['name']}")
            if 'unique_name' in payload:
                print(f"Unique Name:           {payload['unique_name']}")
            
            # Informations principales
            if 'aud' in payload:
                print(f"Audience (aud):        {payload['aud']}")
            if 'iss' in payload:
                print(f"Issuer (iss):          {payload['iss']}")
            if 'appid' in payload:
                appid = payload['appid']
                app_name = KNOWN_AZURE_APPS.get(appid, "Application inconnue")
                print(f"Application ID:        {appid}")
                print(f"  └─ Application:      {app_name}")
            if 'oid' in payload:
                print(f"Object ID:             {payload['oid']}")
            if 'tid' in payload:
                print(f"Tenant ID:             {payload['tid']}")
            
            # Scopes et permissions
            if 'scp' in payload:
                scopes = payload['scp']
                print(f"Scopes (scp):          {scopes}")
            if 'roles' in payload:
                roles = payload['roles']
                if isinstance(roles, list):
                    print(f"Roles:                 {', '.join(roles)}")
                else:
                    print(f"Roles:                 {roles}")
            
            # Groupes de sécurité
            if 'groups' in payload:
                groups = payload['groups']
                if isinstance(groups, list):
                    print(f"Groupes de sécurité:   {len(groups)} groupe(s)")
                    for i, group_id in enumerate(groups[:5], 1):  # Afficher max 5 groupes
                        print(f"  {i}. {group_id}")
                    if len(groups) > 5:
                        print(f"  ... et {len(groups) - 5} autres groupes")
            
            print()
            
            # Dates importantes
            if 'iat' in payload:
                print(f"Émis le (iat):         {format_timestamp(payload['iat'])} (timestamp: {payload['iat']})")
            if 'nbf' in payload:
                print(f"Valide à partir (nbf): {format_timestamp(payload['nbf'])} (timestamp: {payload['nbf']})")
            if 'exp' in payload:
                exp_date = format_timestamp(payload['exp'])
                print(f"Expire le (exp):       {exp_date} (timestamp: {payload['exp']})")
                
                # Calculer le temps restant
                now = datetime.now().timestamp()
                remaining = payload['exp'] - now
                if remaining > 0:
                    hours = int(remaining // 3600)
                    minutes = int((remaining % 3600) // 60)
                    print(f"Temps restant:         {hours}h {minutes}m")
                else:
                    print("⚠️  Token EXPIRÉ!")
            
            # Méthodes d'authentification
            if 'amr' in payload:
                amr = payload['amr']
                if isinstance(amr, list):
                    amr_str = ', '.join(amr)
                    print(f"Auth. methods (amr):   {amr_str}")
                    if 'mfa' in amr:
                        print("  ✅ Multi-Factor Authentication activé")
            
            print("-" * 80)
            
            # Afficher le payload complet en JSON
            print("\n📄 Payload complet (JSON):")
            print(json.dumps(payload, indent=2))
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération du token: {e}")
        raise


if __name__ == "__main__":
    main()

