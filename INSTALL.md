# Installation du README de profil GitHub

## 1. Créer le dépôt spécial
Sur GitHub : **New repository** → nom **exactement identique à ton username** (ex. `roudayna-kouka/roudayna-kouka`) → **Public** → cocher *Add a README*.
GitHub affiche alors « ✨ special repository » : son README apparaît sur ta page de profil.

## 2. Remplacer les placeholders
Dans `README.md` :
- Username déjà renseigné : `roudayn-kouka`
- `TODO-...-repo` → les vrais liens de tes dépôts de projets
- `linkedin.com/in/TODO` et `TODO-portfolio-url` → ton LinkedIn et ton portfolio

## 3. Pousser les fichiers
```bash
git clone https://github.com/ton-username/ton-username.git
cd ton-username
# copier ici : README.md, assets/, .github/, build_assets.py
git add . && git commit -m "feat: holographic profile README" && git push
```

## 4. Activer le serpent (contribution snake)
- Repo → **Settings → Actions → General → Workflow permissions** → *Read and write permissions* → Save
- Onglet **Actions** → *Generate contribution snake* → **Run workflow**
- Il se régénère ensuite automatiquement toutes les 12 h (branche `output`).

## 5. Modifier le contenu des SVG
Tous les SVG animés (bannière, terminal, cartes projets, titres) sont générés par `build_assets.py`.
Modifie le texte / les couleurs en haut du fichier (palette `ROSE`, `LILAC`, `PLUM`…) puis :
```bash
python3 build_assets.py
```
Pour coller exactement aux couleurs de ton portfolio, remplace les codes hex de la palette par ceux de ton CSS.

## Notes
- Les cartes stats (`github-readme-stats`) utilisent une instance publique : si elles s'affichent parfois vides, c'est une limite de taux temporaire, elles reviennent seules.
- Le projet AWS 3-tier (ECS/RDS/ElastiCache/S3) est affiché sans lien (badge « private »).
