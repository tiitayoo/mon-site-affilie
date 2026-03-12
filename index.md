---
layout: default
title: Accueil
---

# Bienvenue sur Mes Comparatifs Produits

Trouvez les meilleurs produits Amazon grâce à nos comparatifs détaillés.

## Tous les articles

<input type="text" id="recherche" placeholder="Rechercher un produit..." style="width:100%; padding:10px; font-size:1em; margin-bottom:15px; border:1px solid #ccc; border-radius:5px; box-sizing:border-box;">

<ul id="liste-articles">
{% for post in site.posts %}
<li><a href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a> — {{ post.date | date: "%d/%m/%Y" }}</li>
{% endfor %}
</ul>

<script>
document.getElementById('recherche').addEventListener('input', function() {
  var terme = this.value.toLowerCase();
  document.querySelectorAll('#liste-articles li').forEach(function(li) {
    li.style.display = li.textContent.toLowerCase().includes(terme) ? '' : 'none';
  });
});
</script>
