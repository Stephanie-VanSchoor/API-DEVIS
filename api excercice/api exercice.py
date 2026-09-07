# ========================================
# API DEVIS SANS IA - 100% GRATUITE
# Extrait les données avec des règles simples
# ========================================

from fastapi import FastAPI
import re
from typing import Dict, Any

# Créer l'API
app = FastAPI(
    title="API Devis - Version Économique",
    description="Extrait les données des devis sans IA - 100% gratuit",
    version="1.0.0"
)


# ========================================
# FONCTIONS D'EXTRACTION (SANS IA)
# ========================================

def extraire_numero(texte: str) -> str:
    """Extrait le numéro de devis"""
    motifs = [
        r'N°\s*[:]?\s*(\d+[-/]?\d*)',
        r'Numéro\s*[:]?\s*(\d+[-/]?\d*)',
        r'DEVIS\s*N°\s*[:]?\s*(\d+[-/]?\d*)',
        r'DEVIS\s*[:]?\s*(\d+[-/]?\d*)'
    ]
    for motif in motifs:
        match = re.search(motif, texte, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return "Non trouvé"


def extraire_fournisseur(texte: str) -> str:
    """Extrait le nom du fournisseur"""
    motifs = [
        r'Fournisseur\s*[:]?\s*([^\n]+)',
        r'De\s*[:]?\s*([^\n]+)',
        r'Émis par\s*[:]?\s*([^\n]+)',
        r'Entreprise\s*[:]?\s*([^\n]+)'
    ]
    for motif in motifs:
        match = re.search(motif, texte, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return "Non trouvé"


def extraire_date(texte: str) -> str:
    """Extrait la date du devis"""
    motifs = [
        r'Date\s*[:]?\s*(\d{2}[/-]\d{2}[/-]\d{4})',
        r'Date\s*[:]?\s*(\d{2}[/-]\d{2}[/-]\d{2})',
        r'Le\s*[:]?\s*(\d{2}[/-]\d{2}[/-]\d{4})'
    ]
    for motif in motifs:
        match = re.search(motif, texte, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return "Non trouvé"


def extraire_montant(texte: str, mot_cle: str) -> float:
    """Extrait un montant (HT, TVA, TTC)"""
    motifs = [
        rf'{mot_cle}\s*[:]?\s*([0-9,.\s]+)[\s€]',
        rf'{mot_cle}\s*[:]?\s*([0-9,.\s]+)€',
        rf'{mot_cle}\s*[:]?\s*([0-9,.\s]+)'
    ]
    for motif in motifs:
        match = re.search(motif, texte, re.IGNORECASE)
        if match:
            valeur = match.group(1).replace(' ', '').replace(',', '.').strip()
            try:
                return float(valeur)
            except:
                pass
    return 0.0


def extraire_tva_pourcentage(texte: str) -> float:
    """Extrait le pourcentage de TVA"""
    motifs = [
        r'TVA\s*[:]?\s*([0-9,.]+\s*%)',
        r'TVA\s*[:]?\s*([0-9,.]+\s*%)',
        r'TVA\s*[:]?\s*([0-9,.]+)\s*%'
    ]
    for motif in motifs:
        match = re.search(motif, texte, re.IGNORECASE)
        if match:
            valeur = match.group(1).replace('%', '').replace(',', '.').strip()
            try:
                return float(valeur)
            except:
                pass
    return 0.0


# ========================================
# FONCTION : Vérifier les données
# ========================================

def verifier_donnees(donnees: Dict[str, Any]) -> Dict[str, Any]:
    """Vérifie la cohérence des données"""
    resultat = {
        "erreurs": [],
        "avertissements": [],
        "valide": True
    }

    total_ht = donnees.get("total_ht", 0)
    tva = donnees.get("tva", 0)
    total_ttc = donnees.get("total_ttc", 0)

    # Vérification 1 : TTC = HT + TVA
    if total_ht > 0 and tva > 0:
        total_calcule = round(total_ht * (1 + tva / 100), 2)
        if abs(total_ttc - total_calcule) > 0.01:
            resultat["erreurs"].append(
                f"Le total TTC ({total_ttc}€) ne correspond pas au calcul HT + TVA ({total_calcule}€)"
            )
            resultat["valide"] = False

    # Vérification 2 : TVA belge
    if tva > 0 and tva not in [6, 12, 21]:
        resultat["avertissements"].append(
            f"TVA de {tva}% : vérifier (taux belges : 6%, 12%, 21%)"
        )

    # Vérification 3 : Montants positifs
    if total_ht < 0:
        resultat["erreurs"].append(f"Total HT négatif : {total_ht}€")
        resultat["valide"] = False
    if total_ttc < 0:
        resultat["erreurs"].append(f"Total TTC négatif : {total_ttc}€")
        resultat["valide"] = False

    return resultat


# ========================================
# ENDPOINT 1 : Page d'accueil
# ========================================

@app.get("/")
def accueil():
    return {
        "message": "🚀 API Devis - Version économique (sans IA)",
        "version": "1.0.0",
        "fonctionnalites": [
            "Extraction du numéro de devis",
            "Extraction du fournisseur",
            "Extraction de la date",
            "Extraction des montants (HT, TVA, TTC)",
            "Vérification des calculs",
            "Détection des taux TVA belges"
        ],
        "endpoints": [
            "/docs - Documentation interactive",
            "/exemple - Voir un exemple de devis",
            "/extraire - Extraire les données d'un devis"
        ]
    }


# ========================================
# ENDPOINT 2 : Exemple de devis
# ========================================

@app.get("/exemple")
def obtenir_exemple():
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


# ========================================
# ENDPOINT 3 : Extraire les données (sans IA !)
# ========================================

@app.post("/extraire")
def extraire(texte: str):
    """Extrait les données d'un devis sans utiliser d'IA"""

    # 1. Extraire les données
    donnees = {
        "numero": extraire_numero(texte),
        "fournisseur": extraire_fournisseur(texte),
        "date": extraire_date(texte),
        "total_ht": extraire_montant(texte, "Total HT"),
        "tva": extraire_tva_pourcentage(texte),
        "total_ttc": extraire_montant(texte, "Total TTC")
    }

    # 2. Vérifier les données
    verification = verifier_donnees(donnees)

    # 3. Construire la réponse
    reponse = {
        "statut": "succès",
        "donnees_extraites": donnees,
        "verification": verification
    }

    # 4. Ajouter une indication globale
    if verification["valide"] and not verification["avertissements"]:
        reponse["fiabilite"] = "✅ Données fiables - Peut être utilisé directement"
    elif verification["valide"] and verification["avertissements"]:
        reponse["fiabilite"] = "⚠️ Données valides mais à vérifier (avertissements)"
    else:
        reponse["fiabilite"] = "❌ Données invalides - Vérification manuelle nécessaire"

    return reponse


# ========================================
# LANCER L'API
# ========================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
