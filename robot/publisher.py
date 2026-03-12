import re
from github import Github
from datetime import date
import config

def slug(titre: str) -> str:
    """Convertit un titre en slug URL."""
    titre = titre.lower()
    titre = re.sub(r'[àâä]', 'a', titre)
    titre = re.sub(r'[éèêë]', 'e', titre)
    titre = re.sub(r'[îï]', 'i', titre)
    titre = re.sub(r'[ôö]', 'o', titre)
    titre = re.sub(r'[ùûü]', 'u', titre)
    titre = re.sub(r'[^a-z0-9\s-]', '', titre)
    titre = re.sub(r'\s+', '-', titre.strip())
    return titre

def publier_article(article: dict) -> str:
    """Publie un article sur GitHub Pages."""
    g = Github(config.GITHUB_TOKEN)
    repo = g.get_user(config.GITHUB_USERNAME).get_repo(config.GITHUB_REPO)

    aujourd_hui = date.today()
    nom_fichier = f"{aujourd_hui.strftime('%Y-%m-%d')}-{slug(article['titre'])}.md"
    chemin = f"{config.POSTS_FOLDER}/{nom_fichier}" if not config.SITE_FOLDER else f"{config.SITE_FOLDER}/{config.POSTS_FOLDER}/{nom_fichier}"

    front_matter = f"""---
layout: post
title: "{article['titre']}"
date: {aujourd_hui.isoformat()}
categories: comparatif
---

"""
    contenu_final = front_matter + article['contenu']

    print(f"  -> Publication : {nom_fichier}")

    try:
        repo.create_file(
            path=chemin,
            message=f"Article: {article['titre']}",
            content=contenu_final,
            branch="main"
        )
        url = f"https://{config.GITHUB_USERNAME}.github.io/{config.GITHUB_REPO}/{aujourd_hui.year}/{aujourd_hui.strftime('%m')}/{aujourd_hui.strftime('%d')}/{slug(article['titre'])}/"
        print(f"  OK ! URL : {url}")
        return url
    except Exception as e:
        print(f"  ✗ Erreur publication : {e}")
        return None
