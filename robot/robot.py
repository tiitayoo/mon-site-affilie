import json
import os
import sys
from datetime import date
import generator
import publisher

# Fix encodage Windows
sys.stdout.reconfigure(encoding='utf-8')

FICHIER_SUJETS = "sujets.txt"
FICHIER_TRAITES = "sujets_traites.json"

def charger_sujets_traites():
    if os.path.exists(FICHIER_TRAITES):
        with open(FICHIER_TRAITES, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def sauvegarder_sujet_traite(sujet, url):
    traites = charger_sujets_traites()
    traites.append({"sujet": sujet, "date": date.today().isoformat(), "url": url})
    with open(FICHIER_TRAITES, 'w', encoding='utf-8') as f:
        json.dump(traites, f, ensure_ascii=False, indent=2)

def prochain_sujet():
    with open(FICHIER_SUJETS, 'r', encoding='utf-8') as f:
        tous = [l.strip() for l in f if l.strip()]
    traites = [t["sujet"] for t in charger_sujets_traites()]
    restants = [s for s in tous if s not in traites]
    return restants[0] if restants else None

def main():
    print("=== Robot Site Affilie ===")
    sujet = prochain_sujet()

    if not sujet:
        print("Tous les sujets ont ete traites !")
        print("Ajoute de nouveaux sujets dans sujets.txt")
        return

    print(f"\nSujet : {sujet}")

    article = generator.generer_article(sujet)
    url = publisher.publier_article(article)

    if url:
        sauvegarder_sujet_traite(sujet, url)
        print(f"\nArticle publie avec succes !")
        print(f"URL : {url}")
        print(f"(Le site se met a jour en 1-2 minutes)")
    else:
        print("\nEchec de la publication")

if __name__ == "__main__":
    main()
