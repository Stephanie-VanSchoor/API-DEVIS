# 📄 API Devis - Template

## Qu'est-ce que c'est ?

Une API qui extrait automatiquement les données des devis :
- Numéro de devis
- Fournisseur
- Date
- Total HT
- TVA
- Total TTC

## Comment l'utiliser ?

1. Envoyer un devis à `/extraire`
2. Recevoir les données structurées

## Exemple

**Envoi :**
L'API est accessible sur : http://localhost:8000
🧪 Tester l'API
Via la documentation interactive

Ouvrez votre navigateur et allez à : http://localhost:8000/docs

    Cliquez sur POST /extraire

    Cliquez sur "Try it out"

    Collez le texte d'un devis

    Cliquez sur "Execute"

Via la ligne de commande (cURL)
bash

curl -X 'POST' \
  'http://localhost:8000/extraire' \
  -H 'Content-Type: application/json' \
  -d '{"texte": "DEVIS N° 2025-0789\nFournisseur : Menuiserie Martin SPRL\nTotal HT : 635,00€\nTVA (21%) : 133,35€\nTotal TTC : 768,35€"}'

🔧 Personnalisation

Les règles d'extraction sont dans le fichier rules.py.

Exemple : Si vos devis utilisent "Montant HT" au lieu de "Total HT", ajoutez cette règle :
python

MONTANT_REGEX = [
    r'Montant HT\s*[:]?\s*([0-9,.\s]+)[\s€]',  # Nouvelle règle
    r'Total HT\s*[:]?\s*([0-9,.\s]+)[\s€]',    # Règle existante
]

💰 Tarifs
Offre	Prix
Mise en place	1 000 € - 2 500 €
Abonnement mensuel	150 € - 400 € / mois
Personnalisation	200 € - 500 €

Tarifs indicatifs, nous contacter pour un devis personnalisé.
🏢 Pourquoi choisir cette solution ?
Avantage	Explication
⏱️ Gain de temps	Économisez 1 à 2 heures par jour
💰 Réduction des erreurs	Plus de saisie manuelle
🔒 Sécurité	Données hébergées localement (option)
📈 Scalable	Adapté aux petites et grandes entreprises
