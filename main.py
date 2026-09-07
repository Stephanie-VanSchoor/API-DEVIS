# ========================================
# TEMPLATE API DEVIS - CODE COMPLET
# 100% gratuit - Facile à personnaliser
# ========================================

from fastapi import FastAPI
import re
import os
from dotenv import load_dotenv
from rules import *

# ========================================
# 1. CHARGER LES VARIABLES D'ENVIRONNEMENT
# ========================================

load_dotenv()

API_NAME = os.getenv("API_NAME", "API Devis")
API_VERSION = os.getenv("API_VERSION", "1.0.0")
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", 8000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# ========================================
# 2. CRÉER L'API
# ========================================

app = FastAPI(
    title=API_NAME,
    description="Extrait les données des devis - Template personnalisable",
    version=API_VERSION,
    debug=DEBUG
)


# ========================================
# 3. FONCTIONS D'EXTRACTION
# ========================================

def extraire_champ(texte: str, regex_list: list, default: str = "Non trouvé"):
    """Extrait un champ en utilisant une liste de motifs"""
    for motif in regex_list:
        match = re.search(motif, texte, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return default


def extraire_montant(texte: str, regex_list: list) -> float:
    """Extrait un montant et le convertit en nombre"""
    for motif in regex_list:
        match = re.search(motif, texte, re.IGNORECASE)
        if match:
            valeur = match.group(1).replace(' ', '').replace(',', '.').strip()
            try:
                return float(valeur)
            except:
                pass
    return 0.0


# ========================================
# 4. ENDPOINTS DE L'API
# ========================================

@app.get("/")
def accueil():
    """Page d'accueil - Informations sur l'API"""
    return {
        "message": f"📄 {API_NAME}",
        "version": API_VERSION,
        "description": "Extrait les données des devis",
        "endpoints": [
            "/exemple - Voir un exemple de devis",
            "/extraire - Extraire les données d'un devis",
            "/docs - Documentation interactive"
        ]
    }


@app.get("/exemple")
def obtenir_exemple():
    """Retourne un exemple de devis à tester"""
    return {
        "exemple": """
DEVIS N° 2025-0789
Fournisseur : Menuiserie Martin SPRL
Adresse : Rue des Artisans 12, 5000 Namur
Date : 15/09/2025

Détails :
- Porte en chêne massif : 450,00€
- Poignée en laiton : 35,00€
- Installation : 150,00€

Total HT : 635,00€
TVA (21%) : 133,35€
Total TTC : 768,35€

Délai de livraison : 5 jours
"""
    }


@app.post("/extraire")
async def extraire(texte: str):
    """
    Extrait les données d'un devis avec les règles personnalisables

    Args:
        texte (str): Le texte complet du devis

    Returns:
        dict: Les données extraites et vérifiées
    """

    # Nettoyer le texte
    texte = texte.replace('\\n', '\n')

    # Extraire les données
    donnees = {
        "numero": extraire_champ(texte, NUMERO_REGEX),
        "fournisseur": extraire_champ(texte, FOURNISSEUR_REGEX),
        "date": extraire_champ(texte, DATE_REGEX),
        "total_ht": extraire_montant(texte, MONTANT_REGEX),
        "tva": extraire_montant(texte, TVA_REGEX),
        "total_ttc": extraire_montant(texte, TTC_REGEX)
    }

    # Vérifier les calculs
    total_ht = donnees["total_ht"]
    tva = donnees["tva"]
    total_ttc = donnees["total_ttc"]

    verification = {
        "erreurs": [],
        "avertissements": []
    }

    if total_ht > 0 and tva > 0:
        total_calcule = round(total_ht * (1 + tva / 100), 2)
        if abs(total_ttc - total_calcule) > 0.01:
            verification["erreurs"].append(
                f"Erreur : TTC ({total_ttc}€) ≠ calcul ({total_calcule}€)"
            )

    if tva > 0 and tva not in [6, 12, 21]:
        verification["avertissements"].append(
            f"TVA {tva}% : vérifier (Belgique : 6%, 12%, 21%)"
        )

    # Construire la réponse
    reponse = {
        "statut": "succès",
        "donnees": donnees,
        "verification": verification
    }

    if verification["erreurs"] or verification["avertissements"]:
        reponse["statut"] = "attention"
        reponse["action_recommandee"] = "Vérification manuelle conseillée"
    else:
        reponse["fiabilite"] = "✅ Données fiables - Prêt à l'emploi"

    return reponse


# ========================================
# 5. LANCER L'API
# ========================================

if __name__ == "__main__":
    import uvicorn

    print("=" * 50)
    print(f"🚀 Lancement de {API_NAME} v{API_VERSION}")
    print(f"📡 Adresse : http://{API_HOST}:{API_PORT}")
    print(f"📖 Documentation : http://{API_HOST}:{API_PORT}/docs")
    print("=" * 50)

    uvicorn.run(
        app,
        host=API_HOST,
        port=API_PORT
    )