# shodan-verify

## Introduction

Dans le cas où nous possédons un (ou plusieurs) VPS, il est assez intéressant de savoir si ils sont référencé sur Shodan.
C'est le but du script suivant. Vous lancer le lancer via CLI avec :

* Une query string shodan
* Les IPs de vos VPS qui sont à détecter
* Les nom de domaines de vos VPS

L'exécution est simple, le script effectue une recherche sur Shodan grâce à la librairie python utilisée, et nous recherchons la présence des IPs et noms de domaines de vos VPS dans les résultats de la recherce.

À noter: à aucun moment vos IPs et noms de domaine ne sont envoyé à Shodan, la recherche se fait en local sur votre machine.

## Pré-requis

Installer la librairie de shodan pour Python :

```bash
pip install shodan
```

Un compte Shodan avec une clé d'API.

## Utilisation

Le script propose 3 commandes:
* api-key
* search
* count

### api-key

Pour utiliser shodan il faut renseigner une clé d'API dans le script. Deux possibilités lors d'une recherche:
* La renseigner dans la CLI
* La renseigner dans un fichier pour éviter de la taper à chaque fois dans la CLI

La commande `api-key` permet d'enregistrer une clé d'API dans un fichier afin de l'utiliser par la suite dans les recherches.

Ajouter une clé:
```bash
python3 main.py api-key --key-value jQ4o3X52s0g9FU5xlRy8hFl1DEnTQ6y8
```

Supprimer la clé du fichier:
```bash
python3 main.py api-key --delete
```

Supprimer la clé du fichier et confirmer directement la suppression:
```bash
python3 main.py api-key --delete --confirm
```

### count

La commande `count` retourne seulement le nombre de server trouvé sur Shodan et le compare avec le nombre attendu.

Cette commande peut sembler inutile, pourtant quand vous avez seulement un compte gratuit sur Shodan il n'est pas possible de récupérer tous les résultats pour une recherche. De plus il n'est pas possible d'utiliser les filtres Shodan dans la commande `search` alors que dans la commande count cela est possible. Donc la commande `count` reste très intéressante pour ceux qui ont un compte gratuit, surtout si votre recherche ne retourne habituellement que peux de résultat. (Par exemple pour ma part ma recherche ne retourne que 3 résultats)

Utiliser la commande `count`:

```bash
python3 main.py count -q "rainloop org:\"xiranxinxi\"" -n 1
```

Si le script retourne plus qu'un résultat alors cela va déclencher une alerte (dans la console)

### search

La commande `search` retourn les éléments des serveurs mais avec une limite dans le nombre de résultat. Le problème avec cette commande quand nous possédons qu'un compte gratuit? Pas d'utilisation de filtre, nombre de résultat limité.

```bash
python3 main.py search -q "rainloop org:\"xiranxinxi\"" --ip 120.130.140.150 121.131.141.151 --dns pizza.tonio.fr tata.yoyo.fr
```

La commande suivante va retourner les éléments (ip et dns) qu'elle à trouver dans les résultats
