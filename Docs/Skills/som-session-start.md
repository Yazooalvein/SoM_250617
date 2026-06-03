---
name: som-session-start
description: >
  Protocole obligatoire de demarrage de session pour le projet Shadow of Mana (SoM).
  Declencheur IMMEDIAT des que Nico dit "on travaille sur SoM", "lis le CLAUDE.md",
  "reprends le projet SoM", ou toute formulation equivalente indiquant le debut d'une
  session de travail sur ce projet. Ce skill definit exactement quels fichiers lire,
  dans quel ordre, et quel resume produire. Ne jamais demarrer une session SoM sans
  avoir suivi ce protocole.
---

# SoM -- Protocole de demarrage de session

## Etape 1 -- Lecture obligatoire des fichiers de contexte

Lire dans cet ordre exact via `github:get_file_contents` (owner: Yazooalvein, repo: SoM_250617, branch: main) :

1. `CLAUDE.md` -- contexte global, architecture, jalons, regles critiques
2. `Docs/Journal_Modifications.md` -- historique des sessions, derniers changements

Ces deux lectures sont **non negociables**. Ne jamais supposer que le contexte en memoire
est suffisant -- toujours lire les fichiers frais depuis GitHub.

## Etape 2 -- Resume structure a produire

Apres lecture, produire un resume court et actionnable :

```
## Etat du projet SoM -- [date du journal]

**Dernier jalon complete :** [jalon + date + statut PIE]
**Dettes actives (C1 prioritaires) :** [liste courte]
**Prochain jalon recommande :** [jalon suivant selon CLAUDE.md]

---
Pret. Que fait-on aujourd'hui ?
```

Rester court. Pas de recapitulatif exhaustif -- Nico connait le projet.

## Etape 3 -- Verification des regles critiques

Avant toute action, avoir en tete ces regles (issues de CLAUDE.md) :

- **Ne jamais committer sans confirmation explicite de Nico.**
- **Toujours recuperer le SHA avant d'ecrire** (`get_file_contents` du fichier cible).
- **L'agent UnrealClaude** = discovery/audit uniquement. Jamais `blueprint_modify` ni `execute_script`.

## Etape 4 -- Si Nico annonce un nouveau jalon technique

Si la session va demarrer un nouveau jalon de CODE (pas design pur), declencher
immediatement le skill **`som-jalon-design`** AVANT de proposer du code.

Signes qu'un jalon technique demarre :
- "on attaque [NomJalon]"
- "on fait [NomJalon]"
- "prochaine etape c'est [NomJalon]"
- "go" apres un recapitulatif de session qui annonce un jalon

Signes qu'on est en session design (pas besoin de som-jalon-design) :
- "on reflechit a...", "session design", "on parle de..."

## Rappel des fichiers a maintenir en fin de session

Voir le skill `som-commit-protocol` pour le protocole complet.
Fichiers concernes : `CLAUDE.md`, `Docs/Journal_Modifications.md`,
`Docs/Architecture/Decisions.md`, `Docs/Architecture/[Systeme].md` selon ce qui a change,
`Docs/Project_Architecture_Index.md` si un jalon change de statut.
