---
name: som-commit-protocol
description: "Protocole obligatoire pour toute ecriture, mise a jour ou commit sur le repo GitHub du projet Shadow of Mana (SoM). Declencher des que Nico dit 'mets a jour la doc', 'committe', 'note ca dans le journal', 'mets a jour CLAUDE.md', ou demande toute modification d'un fichier du repo SoM_250617. Ce skill definit l'ordre exact des operations, le format des entrees de journal, et les verifications a faire avant chaque ecriture. Ne jamais ecrire sur le repo sans avoir suivi ce protocole."
---

# SoM -- Protocole de commit et mise a jour documentaire

## Regle fondamentale

Ne jamais ecrire sur GitHub sans confirmation explicite de Nico dans le chat.
Les confirmations valides sont des formulations comme :
- "mets a jour la doc"
- "committe"
- "note ca dans le journal"
- "pousse ca"

Une discussion sur ce qui *pourrait* etre commite n'est pas une confirmation.

---

## Protocole avant tout `create_or_update_file`

### 1. Donner les commandes pour le push cote dev

Avant toute chose, il faut que Nico puisse faire son push :
```
git add .
git commit -m "[resume light des modifications/jalons atteints depuis le precedent commit]"
git push
```

### 2. Recuperer le SHA courant
Toujours faire un `github:get_file_contents` du fichier cible **juste avant** d'ecrire.
Ne jamais reutiliser un SHA d'une lecture anterieure dans la conversation -- il peut etre perime.

```
owner: Yazooalvein
repo: SoM_250617
branch: main
path: [chemin du fichier cible]
```

Extraire le champ `sha` de la reponse et l'utiliser dans le parametre `sha` de `create_or_update_file`.

### 3. Verifier les modifs locales

Demander a Nico : **"Est-ce que tu as des modifications locales non pushees ?"**

- Si oui -> Nico pushe d'abord, puis Claude ecrit ensuite
- Si non -> proceder

### 4. Effectuer l'ecriture

Utiliser `github:create_or_update_file` ou `github:push_files` (multi-fichiers) avec :
- `sha` : recupere a l'etape 2
- `message` : format conventionnel (voir ci-dessous)
- `branch` : main

---

## Format des messages de commit

```
doc: [fichier] - [description courte]
```

Exemples :
```
doc: Journal_Modifications.md - session 25/05/2026 C1-RadialMagie
doc: CLAUDE.md - jalons et dettes mis a jour
doc: Decisions.md - ajout decision architecture BPI_Saveable
```

---

## Quels fichiers mettre a jour et quand

| Fichier | Mettre a jour si... |
|---|---|
| `CLAUDE.md` | Jalons changent de statut, nouvelle dette, changement archi, note technique importante |
| `Docs/Journal_Modifications.md` | A chaque session productive |
| `Docs/Roadmap_Gameplay.md` | Un jalon change de statut ou un nouveau jalon est cree |
| `Docs/Architecture/Decisions.md` | Une decision importante est prise (abandon, choix archi, gotcha, nouveau pattern) |
| `Docs/Architecture/[Systeme].md` | L'architecture d'un systeme change ou est implementee |
| `Docs/Project_Architecture_Index.md` | Un jalon change de statut ou un nouveau fichier doc est cree |
| `Docs/Session_UnrealClaude.md` | L'agent UnrealClaude a effectue des actions |

**Regle de coherence** : si un jalon est marque complet dans `CLAUDE.md`, il doit aussi
apparaitre dans `Journal_Modifications.md`, `Roadmap_Gameplay.md` et `Project_Architecture_Index.md`.
Les quatre fichiers se mettent a jour dans la meme session.

---

## Format d'une entree de journal

```markdown
### JJ/MM/AAAA -- [Nom du jalon ou description courte]

#### [Sous-systeme ou fonctionnalite] -- [statut : VALIDE PIE / PARTIEL / DESIGN]
- Point factuel 1
- Point factuel 2
- Bug resolu : [description courte + cause + fix]

#### Dettes restantes (si applicable)
- [dette] : [description courte] -> [jalon cible]

#### Etat final
[Une phrase resumant l'etat apres cette session]
```

**Regles de format :**
- Date : `JJ/MM/AAAA` (pas `YYYY-MM-DD`)
- Toujours mettre le statut PIE en titre de section quand applicable
- Bugs resolus : toujours noter cause + fix (precieux pour les sessions futures)
- Pas de prose -- bullet points factuels uniquement
- Nouvelle entree **en haut** de la section Entrees, pas en bas

---

## Mise a jour de CLAUDE.md -- sections concernees

Quand un jalon est complete, mettre a jour **toutes** ces sections dans le meme commit :

1. **Jalons completes** : ajouter `- [x] [Jalon] VALIDE PIE (JJ/MM/AAAA)`
2. **Dettes techniques** : supprimer les dettes resolues, ajouter les nouvelles
3. **Prochains jalons** : reordonner si necessaire, supprimer le jalon termine
4. **Notes techniques importantes** : ajouter toute regle critique decouverte
5. **Architecture cle** : mettre a jour la section du systeme modifie
6. **Ligne `Derniere mise a jour`** : toujours mettre la date du jour en bas du fichier

---

## Checklist de fin de session

Avant de clore une session productive, verifier mentalement :

- [ ] Journal mis a jour avec entree datee
- [ ] CLAUDE.md mis a jour (jalons, dettes, notes techniques)
- [ ] Roadmap mise a jour si un jalon a change de statut
- [ ] Decisions.md mis a jour si une decision importante a ete prise ou un nouveau pattern etabli
- [ ] Fichier `Docs/Architecture/[Systeme].md` concerne mis a jour et coherent avec l'implementation
- [ ] `Project_Architecture_Index.md` reflète le bon statut du jalon complete
- [ ] Pas d'incoherence entre CLAUDE.md, Journal et fichiers d'archi (noms, statuts, dettes)
- [ ] `Derniere mise a jour` dans CLAUDE.md = date du jour
- [ ] Tous les SHA recuperes frais avant chaque ecriture
- [ ] Confirmation explicite de Nico obtenue avant chaque commit

---

## Erreurs frequentes a eviter

| Erreur | Consequence | Prevention |
|---|---|---|
| Reutiliser un SHA ancien | Conflit / echec silencieux | Toujours `get_file_contents` juste avant d'ecrire |
| Committer sans confirmation | Perte de modifs locales de Nico | Attendre formulation explicite |
| Mettre a jour CLAUDE.md sans le Journal | Documentation incoherente | Checklist fin de session |
| Oublier Project_Architecture_Index | Statut jalon desynchronise | Checklist fin de session |
| Fichier d'archi pas mis a jour | Documentation diverge de l'implementation | Checklist fin de session |
| Incoherence CLAUDE.md / Decisions.md | Prochaine session part sur une base fausse | Comparer les sections concernees |
| Date incorrecte dans le journal | Historique faux | Utiliser la date reelle du jour |
| Entree de journal trop vague | Inutilisable en session future | Toujours noter cause + fix des bugs |
