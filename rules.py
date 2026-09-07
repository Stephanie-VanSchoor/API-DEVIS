# ========================================
# RÈGLES D'EXTRACTION POUR DEVIS
# ========================================

# 1. Règles pour le numéro de devis
NUMERO_REGEX = [
    r'N°\s*[:]?\s*(\d+[-/]?\d*)',
    r'Numéro\s*[:]?\s*(\d+[-/]?\d*)',
    r'DEVIS\s*N°\s*[:]?\s*(\d+[-/]?\d*)',
]

# 2. Règles pour le fournisseur
FOURNISSEUR_REGEX = [
    r'Fournisseur\s*[:]?\s*([^\n,]+)',
    r'De\s*[:]?\s*([^\n,]+)',
    r'Émis par\s*[:]?\s*([^\n,]+)',
]

# 3. Règles pour la date
DATE_REGEX = [
    r'Date\s*[:]?\s*(\d{2}[/-]\d{2}[/-]\d{4})',
    r'Date\s*[:]?\s*(\d{2}[/-]\d{2}[/-]\d{2})',
]

# 4. Règles pour les montants
MONTANT_REGEX = [
    r'Total HT\s*[:]?\s*([0-9,.\s]+)[\s€]',
    r'Total HT\s*[:]?\s*([0-9,.\s]+)€',
    r'Total HT\s*[:]?\s*([0-9,.\s]+)'
]

# 5. Règles pour la TVA
TVA_REGEX = [
    r'TVA\s*\((\d+)\s*%\)',     # (21%)
    r'TVA\s*[:]?\s*([0-9,.]+)\s*%',  # 21%
]

# 6. Règles pour le TTC
TTC_REGEX = [
    r'Total TTC\s*[:]?\s*([0-9,.\s]+)[\s€]',
    r'Total TTC\s*[:]?\s*([0-9,.\s]+)€',
]