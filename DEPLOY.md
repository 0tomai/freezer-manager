# Déploiement sur PythonAnywhere (gratuit)

## Étape 1 — Créer le compte

1. Va sur **pythonanywhere.com** → **Pricing & signup** → choisis **Beginner (Free)**
2. Choisis un username (ex: `moncongelo`) — ce sera ton URL : `moncongelo.pythonanywhere.com`
3. Valide l'email

---

## Étape 2 — Cloner le repo depuis PythonAnywhere

Dans PythonAnywhere, ouvre un terminal Bash :
**Dashboard → Consoles → Bash**

```bash
git clone https://github.com/0tomai/freezer-manager.git
cd freezer-manager/freezer-api
```

---

## Étape 3 — Créer le virtualenv et installer les dépendances

```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Étape 4 — Configurer les variables d'environnement

```bash
cp .env.example .env
nano .env
```

Modifie les valeurs :
```
FLASK_ENV=production
SECRET_KEY=une-longue-chaine-aleatoire-ici
JWT_SECRET_KEY=une-autre-chaine-aleatoire
SHARED_PIN=ton-pin-a-toi
```

Pour générer des clés aléatoires :
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## Étape 5 — Créer l'application web

1. Va dans **Web** → **Add a new web app**
2. Clique **Next** (domaine gratuit `username.pythonanywhere.com`)
3. Choisis **Manual configuration**
4. Choisis **Python 3.10**
5. Clique **Next**

---

## Étape 6 — Configurer le fichier WSGI

Dans la page **Web**, clique sur le lien vers le fichier WSGI
(quelque chose comme `/var/www/username_pythonanywhere_com_wsgi.py`).

**Efface tout le contenu** et remplace par :

```python
import sys
import os

# Chemin vers ton projet
path = '/home/TON_USERNAME/freezer-manager/freezer-api'
if path not in sys.path:
    sys.path.insert(0, path)

# Charger les variables d'environnement depuis .env
from dotenv import load_dotenv
load_dotenv(os.path.join(path, '.env'))

from app import create_app
application = create_app('production')
```

> Remplace `TON_USERNAME` par ton vrai username PythonAnywhere.

---

## Étape 7 — Configurer le virtualenv

Toujours dans la page **Web**, section **Virtualenv** :

```
/home/TON_USERNAME/freezer-manager/freezer-api/venv
```

---

## Étape 8 — Recharger l'app

Clique le bouton vert **Reload** en haut de la page Web.

Ton app est accessible sur : `https://TON_USERNAME.pythonanywhere.com`

---

## Mettre à jour après un changement de code

Depuis la console Bash PythonAnywhere :
```bash
cd ~/freezer-manager
git pull
```

Puis clique **Reload** dans l'onglet Web.

Si tu as modifié le frontend localement :
```bash
# Sur ta machine locale
bash build.sh
git add freezer-api/frontend_dist
git commit -m "update frontend"
git push

# Puis sur PythonAnywhere
git pull
# + Reload
```
