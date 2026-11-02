# Outils fondamentaux


Ce dépôt contient deux parties :

 `tp/` : mes solutions des TP1 à TP6 ;
 `projet/` : mon projet personnel, **casser un chiffrement affine** avec des attaques statistiques. Le détail est dans [`projet/README.md`](projet/README.md).

## Lancer le code

Depuis la racine du dépôt :

```bash
python -m pip install -r requirements.txt
python -m tp.test_solutions            # tests des TP
python -m unittest projet.test_projet -v  # tests du projet
python -m projet.main                  # expériences du projet
```

La dernière commande refait les 1 800 essais et régénère le CSV et les graphiques dans `projet/resultats/`.

J’ai utilisé un assistant IA pour : les graphiques (je n’arrivais pas à les exporter en SVG), le fichier main.py, et la rédaction du README. J’ai relu le code, retouché les commentaires et lancé moi-même les tests et les expériences.
