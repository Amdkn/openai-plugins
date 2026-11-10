# aspace-openai-plugins-adapter

**Adapter clean-room (D12, D-N048 V5) pour `openai/plugins` — référence seule.**

## Ce que c'est

Le dépôt amont `openai/plugins` est un catalogue de 62 plugins Codex
(manifestes `.codex-plugin/plugin.json`, skills Markdown, serveurs MCP
distants) **sans licence** (aucun fichier LICENSE, `license: null` à l'API
GitHub). Le fork `Amdkn/openai-plugins` est donc une **référence seule** :
aucun fichier amont n'est copié, et l'adaptation est écrite de zéro depuis
la spécification publique du format de manifeste (un plugin vit sous
`plugins/<name>/` avec un manifeste `.codex-plugin/plugin.json` requis).

## Surface (couture contrat seule, §1.5)

| Commande | Effet |
|---|---|
| `python3 mock_plugin.py manifest` | Imprime un manifeste minimal valide (JSON, stdout) |
| `python3 mock_plugin.py validate <dir>` | Contrôle de structure de `.codex-plugin/plugin.json` (exit 0/2) |
| `python3 mock_plugin.py env` | Environnement hors-ligne (télémétrie zéro par construction) |
| `python3 smoke_test.py` | Suite de fumée (unittest stdlib, hors-ligne) |

Stdlib Python seule. Aucun appel réseau, aucun identifiant, aucun serveur
MCP de plugin n'est jamais démarré.

## Fichiers

- `contract.json` — contrat de l'adapter (surface, gel, régime D12).
- `mock_plugin.py` — générateur de manifeste minimal + validateur de structure.
- `smoke_test.py` — 8 tests de fumée (contrat, manifeste, validation OK/KO,
  environnement, absence d'import réseau, absence de contenu amont).
- `README.md` — ce fichier.

## Preuve zéro copie (D12)

Aucun des 4 fichiers de l'adapter n'existe parmi les blobs de l'arbre du
gel `d420d13` (comparaison par hash de blob, faite par l'exécutant et
re-vérifiée par le 13e — même méthode que claude-code en V3b). Le compare
gel→HEAD du fork = ahead 1, exactement ces 4 fichiers.

## Repli (D12)

Si la validation clean-room échoue, le repli nommé est la **suppression du
fork** — aucune publication d'une copie.

## Télémétrie

Zéro par construction (voir `openai-plugins-TELEMETRY-AUDIT.md`) : l'adapter
ne fait aucun appel réseau. Les 31 `.mcp.json` du catalogue pointent vers
des API de fournisseurs (OAuth, identifiants de l'utilisateur) — ce sont les
fonctions des plugins, jamais invoquées par l'adapter.

## Gel et licence

- Gel : `d420d13051bffe4543ed39e30fa46b87148e47dd` (main, « Add AWS Core to
  curated marketplace (#410) »).
- Licence : **aucune** (sans LICENSE, `license: null`).
- Propriétaire : cœur Buzz (lane Clara / 12e).
