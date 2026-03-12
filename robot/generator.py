from groq import Groq
from datetime import date
import config

client = Groq(api_key=config.GROQ_API_KEY)

PROMPT_TEMPLATE = """
Tu es un rédacteur web spécialisé en comparatifs de produits Amazon.
Écris un article de blog complet en français sur le sujet suivant : {sujet}

L'article doit :
- Avoir un titre accrocheur (commence par # )
- Faire entre 600 et 900 mots
- Présenter 3 à 5 produits avec leurs avantages et inconvénients
- Inclure une section "Notre recommandation" à la fin
- Être rédigé de façon naturelle et utile pour le lecteur
- Utiliser des sous-titres (## ) pour structurer le contenu
- À chaque mention d'un produit spécifique, ajouter [LIEN AMAZON] juste après

Ne mets pas d'introduction générale sur Amazon. Va droit au but.
"""

def generer_article(sujet: str) -> dict:
    """Génère un article complet pour un sujet donné."""
    print(f"  -> Generation : {sujet}")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": PROMPT_TEMPLATE.format(sujet=sujet)}],
        max_tokens=1500
    )

    contenu = response.choices[0].message.content

    lignes = contenu.strip().split('\n')
    titre = lignes[0].replace('# ', '').strip()

    lien_recherche = f"https://www.amazon.fr/s?k={sujet.replace(' ', '+')}&tag={config.AMAZON_TAG}"
    contenu = contenu.replace('[LIEN AMAZON]', f'[→ Voir sur Amazon]({lien_recherche})')

    return {
        "titre": titre,
        "contenu": contenu,
        "sujet": sujet,
        "date": date.today().isoformat()
    }
