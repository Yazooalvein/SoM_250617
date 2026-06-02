# Skills Claude — Shadow of Mana

Ce fichier recense les skills Claude actifs pour le projet SoM,
ainsi que les skills recommandes a creer pour ameliorer le workflow.

Les skills sont des fichiers SKILL.md stockes dans `/mnt/skills/user/`
sur l'environnement Claude. Ils sont charges automatiquement quand
Claude detecte un declencheur correspondant dans la conversation.

---

## Skills existants

### `som-session-start`
**Declencheur :** "on travaille sur SoM", "lis le CLAUDE.md", "reprends le projet SoM"
**Role :** Protocole de demarrage de session. Definit quels fichiers lire (CLAUDE.md + Journal), dans quel ordre, et quel resume produire. Garantit que chaque session repart d'un contexte complet et coherent.
**Fichier :** `/mnt/skills/user/som-session-start/SKILL.md`

### `som-commit-protocol`
**Declencheur :** "mets a jour la doc", "committe", "note ca dans le journal", "pousse ca"
**Role :** Protocole de commit GitHub. Definit l'ordre exact des operations (git push Nico d'abord, SHA frais, puis ecriture), le format des entrees de journal, et la checklist de fin de session. Previent les conflits et les SHA perimes.
**Fichier :** `/mnt/skills/user/som-commit-protocol/SKILL.md`

---

## Skills recommandes a creer

### `som-new-system` ⭐ PRIORITE 1
**Declencheur :** "on cree un nouveau systeme", "nouveau jalon SYS-", "nouveau composant"
**Role :** Template de demarrage pour tout nouveau systeme transversal (SYS-*, nouveau Component, nouvelle variable dans AttributeSet). Force a repondre aux questions d'architecture avant de coder :
- Ou vit la donnee ? (AttributeSet, Component, GameMode, PC ?)
- Qui la modifie ? (SetStatValue uniquement ?)
- Qui l'ecoute ? (OnStatChanged, dispatcher ?)
- Quel est le cas d'erreur silencieux le plus probable ? (fils exec manquants, ordre BeginPlay, overlap instantane...)
- Quelle dette est acceptee en C1 vs C2 ?
**Valeur :** Aurait evite le bug `EssenceValue` (fils exec manquants dans SetStatValue) et le bug `bCanBePickedUp` (overlap instantane au spawn) cette session.

### `som-pie-validation` ⭐ PRIORITE 2
**Declencheur :** "on teste en PIE", "valide PIE", "test PIE avant de committer"
**Role :** Checklist de validation PIE standardisee avant de clore un jalon. Structure en 3 niveaux :
- **Cas nominal** : le chemin heureux fonctionne
- **Cas limite** : valeurs a 0, valeurs max, sequence rapide (double-clic, mort instantanee...)
- **Cas d'erreur** : que se passe-t-il si une ref est None ? si on meurt pendant un Delay ?
**Valeur :** Evite de decouvrir des bugs en session suivante sur des jalons "valides". Chaque SYS- a ses propres cas limites documentes.

### `som-blueprint-audit` ⭐ PRIORITE 3
**Declencheur :** "audit du BP", "analyse ce blueprint", "qu'est-ce qui se passe dans X"
**Role :** Prompt standardise pour demander un audit T3D a UnrealClaude. Format de sortie normalise :
- Variables declarees (nom, type, default, instance editable ?)
- Fonctions exposees (signature, pure ou non ?)
- Flux exec principaux (de l'event jusqu'au dead end)
- Fils morts ou disconnectes
- Erreurs detectees (nodes rouges, pins orphelins)
**Valeur :** Aujourd'hui on formule l'audit differemment a chaque fois. Un format standardise = resultats comparables et plus faciles a lire.

### `som-debt-tracker` PRIORITE 4
**Declencheur :** "on reporte ca", "c'est une dette", "on fait ca en C2"
**Role :** Protocole de decision pour les dettes techniques. Force a classifier chaque dette avant de la reporter :
- **Bloquant C1** : empeche la boucle de jeu de fonctionner -> traiter maintenant
- **Bloquant PIE** : crash ou comportement incorrect visible -> traiter avant le commit
- **Dette standard** : comportement sous-optimal mais fonctionnel -> reporter avec jalon cible
- **Dette cosmetique** : polish, nommage, refacto -> C4 ou jamais
Et genere automatiquement la ligne de dette au bon format pour CLAUDE.md.
**Valeur :** Evite les discussions "on fait maintenant ou on reporte ?" en imposant des criteres objectifs.

---

## Notes

- Les skills sont crees et edites via l'outil `memory_user_edits` ou directement dans `/mnt/skills/user/`
- Un skill mal decrit ne se declenche pas -- la description doit contenir les phrases exactes que Nico utilise
- Ordre de creation recommande : `som-new-system` -> `som-pie-validation` -> `som-blueprint-audit` -> `som-debt-tracker`

---

*Derniere mise a jour : 02/06/2026*
