"""Script pour récupérer et afficher le token JWT d'un Service Principal pour Azure PostgreSQL."""

from __future__ import annotations

import json
import base64
from datetime import datetime
from azure.identity import DefaultAzureCredential


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
            
            # Informations principales
            if 'aud' in payload:
                print(f"Audience (aud):        {payload['aud']}")
            if 'iss' in payload:
                print(f"Issuer (iss):          {payload['iss']}")
            if 'appid' in payload:
                print(f"Application ID:        {payload['appid']}")
            if 'oid' in payload:
                print(f"Object ID:             {payload['oid']}")
            if 'tid' in payload:
                print(f"Tenant ID:             {payload['tid']}")
            
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
            
            print("-" * 80)
            
            # Afficher le payload complet en JSON
            print("\n📄 Payload complet (JSON):")
            print(json.dumps(payload, indent=2))
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération du token: {e}")
        raise


if __name__ == "__main__":
    main()

