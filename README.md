# TP 1 — DevOps : de l'application au déploiement

**EMSI** — Prof. BAKKALI YEDRI OTHMAN
Mini-projet : **API REST → Git → tests → Docker → CI** (Workflow complet)

## 1. Prérequis (Windows)

| Outil   | Version installée | Commande            |
| ------- | ----------------- | ------------------- |
| Python  | 3.12.4            | `python --version`  |
| Git     | 2.x               | `git --version`     |
| Docker  | 29.8.1            | `docker --version`  |

> Sur cette machine Git n'était pas dans le `PATH` ; il a été appelé via
> `C:\Program Files\Git\cmd\git.exe`.

## 2. Arborescence du projet

```
devops-tp1/
├── app/main.py            # API Flask
├── tests/test_main.py     # Tests pytest
├── requirements.txt
├── Dockerfile
├── .gitignore
├── .github/workflows/ci.yml
└── captures/              # captures d'écran des étapes
```

## 3. API Flask (`app/main.py`)

`GET /` → `{"application":"DevOps TP1","status":"running"}`
`GET /hello/<name>` → `{"message":"Bonjour <name> !"}`

## 4. Tests (`pytest -v`)

```
tests/test_main.py::test_home PASSED
tests/test_main.py::test_hello PASSED
2 passed
```

## 5. Git

```
git init
git add .
git commit -m "Initialisation DevOps"
git log --oneline   ->  e0d3362 Initialisation DevOps
```

## 6. Docker

```
docker build -t devops-tp1:1.0 .
docker run --name devops-tp1 -p 5000:5000 devops-tp1:1.0
```

Vérification : `http://127.0.0.1:5000/` renvoie bien le JSON attendu (conteneur `Up`,
port `0.0.0.0:5000->5000/tcp`).

## 7. CI GitHub Actions (`.github/workflows/ci.yml`)

À chaque `push` / `pull_request` : checkout, setup Python 3.12, `pip install -r
requirements.txt`, puis `pytest -v`.

## 7bis. Publication de l'image (Docker Hub)

L'image est publiée sous **`poee55/devops-tp1`** :

```bash
docker login -u poee55
docker tag devops-tp1:1.0 poee55/devops-tp1:1.0
docker tag devops-tp1:1.0 poee55/devops-tp1:latest
docker push poee55/devops-tp1:1.0
docker push poee55/devops-tp1:latest
```

Récupération sur n'importe quelle machine (déploiement délocalisé) :

```bash
docker pull poee55/devops-tp1:latest
docker run --rm -p 5000:5000 poee55/devops-tp1:latest
```

- Dépôt de code : https://github.com/eibaRRR/devops-tp1
- Image : https://hub.docker.com/r/poee55/devops-tp1

## 8. Réponses aux questions

**Pourquoi tester avant le build ?**
Pour détecter au plus tôt les régressions avant de produire une image déployable.
Un test qui échoue doit arrêter la chaîne : inutile (et risqué) de construire et
publier une image non validée. Cela réduit le coût d'un bug (corrigé côté code, pas
en production).

**Quel est le rôle de Docker ?**
Docker empaquette l'application **et ses dépendances** dans une image immuable, ce qui
garantit le même environnement d'exécution sur la machine de dev, le serveur et la CI
(« ça marche chez moi » devient reproductible). Il isole aussi les processus et permet
de distribuer/tester l'app de façon identique partout.

**Que se passe-t-il si un test échoue ?**
`pytest` retourne un code de sortie non nul. En CI, le job est marqué **failed**, le
pipeline s'arrête (les étapes suivantes comme le build/push de l'image ne sont pas
exécutées) et la PR/push est signalée. Le code fautif ne doit pas être déployé.

**Quelle différence entre CI et déploiement ?**
La **CI** (Intégration Continue) vérifie automatiquement chaque changement : installation
des dépendances, tests, parfois build de l'image. Le **déploiement** est l'étape suivante
qui met la version validée en production (ou en préprod) : publication de l'image dans un
registry, mise à jour du serveur, redéploiement des conteneurs. La CI valide, le
déploiement met en service.

## 9. Chaîne DevOps couverte

**Code → Test → Git → Docker → CI**

## 10. Livrables

- Dépôt Git : `app/`, `tests/`, `Dockerfile`, `.gitignore`, workflow CI, `requirements.txt`.
- Captures : versions des outils, arborescence, `pytest`, `git log`, image et conteneur
  Docker, réponses des endpoints, workflow CI (dossier `captures/`).

### Reproduction complète

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install Flask pytest
python app/main.py            # http://127.0.0.1:5000
pytest -v
git init; git add .; git commit -m "Initialisation DevOps"
docker build -t devops-tp1:1.0 .
docker run --name devops-tp1 -p 5000:5000 devops-tp1:1.0
```