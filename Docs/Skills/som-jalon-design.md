---
name: som-jalon-design
description: >
  Phase de design obligatoire avant tout nouveau jalon technique Shadow of Mana.
  Declencher des que Nico annonce un nouveau jalon de code (ex: "on attaque MAGIC-TreeModule",
  "on fait ENEMY-Base", "prochaine etape c'est MAP-C1Level", "on commence SYS-X").
  NE PAS declencher pour les sessions de design pur (DESIGN-*, SESSION-*).
  Ce skill force une reflexion architecturale complete AVANT de proposer du code.
  Ne jamais sauter cette etape sous peine de produire une dette technique immediate.
---

# SoM -- Protocole de design de jalon technique

## Pourquoi ce protocole existe

Sans reflexion prealable, on produit des solutions qui fonctionnent localement mais
qui ne respectent pas les patterns etablis, ne s'integrent pas avec les systemes futurs,
et creent de la dette. Exemple : OnFountainRest sans BPI_Saveable (session 03/06/2026).

Ce protocole force 4 questions avant tout code.

---

## Etape 1 -- Lire les documents de reference

Via `github:get_file_contents` (owner: Yazooalvein, repo: SoM_250617, branch: main) :

1. `Docs/Architecture/Decisions.md` -- **section PATTERNS ETABLIS en priorite**
2. `Docs/Roadmap_Gameplay.md` -- jalons C2/C3/C4 a ne pas bloquer
3. `CLAUDE.md` -- si pas deja lu en debut de session (architecture cle, dettes actives)

Ces lectures sont non negociables. Les patterns etablis dans Decisions.md sont la
constitution du projet -- tout nouveau systeme doit les respecter.

---

## Etape 2 -- Verification de coherence documentaire

Avant de concevoir quoi que ce soit, verifier que les fichiers existants sont a jour
par rapport a l'etat reel du projet :

- Le fichier `Docs/Architecture/[Systeme].md` correspondant au jalon est-il a jour ?
- `Docs/Project_Architecture_Index.md` reflete-t-il le bon statut des jalons recents ?
- `Docs/Architecture/Decisions.md` contient-il les decisions prises dans les dernieres sessions ?
- Y a-t-il des incoherences entre CLAUDE.md et les fichiers d'archi (noms de variables,
  statuts de jalons, dettes listees) ?

**Signaler toute incoherence a Nico avant de continuer.**
Ne pas laisser la documentation diverger de l'implementation reelle.

---

## Etape 3 -- Fiche de design du jalon

Produire cette fiche et la soumettre a Nico pour validation AVANT tout code :

```
## Design -- [NomJalon]

### Systemes existants impactes
(liste exhaustive -- qui va appeler ce systeme ? qui va etre appele ?)
- [Systeme] : [comment il interagit]

### Systemes futurs concernes (Roadmap C2/C3/C4)
(ce qu'on ne fait PAS maintenant mais qu'on ne doit PAS bloquer)
- [Jalon futur] : [ce dont il aura besoin de ce systeme]

### Patterns etablis applicables
(lesquels de Decisions.md s'appliquent ici ?)
- [Pattern] : [comment il s'applique concretement]

### Perimetre C1 strict
(minimum fonctionnel sans bloquer l'avenir)
- Ce qu'on fait : [...]
- Ce qu'on ne fait PAS et pourquoi : [...]

### Proposition d'architecture
[1-2 options max avec trade-offs explicites]

Option A -- [Nom] :
  + Avantage
  - Inconvenient

Option B -- [Nom] :
  + Avantage
  - Inconvenient

### Recommandation
[Option retenue + justification courte]
```

---

## Etape 4 -- Validation

**Attendre la validation explicite de Nico sur la fiche de design avant de proposer du code.**

Une formulation comme "go", "ca me va", "on part sur ca" est une validation.
Une question ou une remarque n'est pas une validation -- affiner la fiche d'abord.

---

## Regles complementaires

- Si un pattern etabli ne semble pas applicable, le dire explicitement et expliquer
  pourquoi plutot que de l'ignorer silencieusement.
- Si le jalon touche un systeme qui a un fichier `Docs/Architecture/[Systeme].md`,
  proposer de le mettre a jour en fin de session.
- Si une nouvelle decision architecturale importante emerge pendant la conception,
  la noter pour l'ajouter a `Decisions.md` en fin de session.
- Toujours se demander : "si on ajoute [X] en C3, est-ce que ce qu'on construit
  maintenant le rend facile ou difficile ?"
- Si Nico remet en question l'architecture proposee, c'est un signal positif --
  prendre le recul demande et reproposer avant de coder.
