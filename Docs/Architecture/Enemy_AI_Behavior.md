# Architecture Technique — IA des Ennemis

---

## 🎯 Objectif

Documenter la logique complète du comportement IA des ennemis basiques dans le projet ARPG. Cette logique est intégrée dans le contrôleur IA, sans usage de Behavior Tree pour l’instant, afin de rester simple, lisible et modulaire.

---

## 🧠 Composants principaux

### 🎮 `BP_EnemyBase` (Pawn)
- Composant `PawnSensing_Enemy` (vision)
- Propriétés d’interaction (`bIsDead`, `bIsValid`, `bCanBeLocked`)
- Événement `OnSeePawn` → déclenche un `RegisterTarget()` dans son AIController

### 📦 `BP_AIController_Enemy_Base`
- Contrôleur de base pour tous les ennemis
- Centralise toute la logique de comportement

---

## 🧩 Variables du contrôleur

| Nom | Type | Description |
|------|------|-------------|
| `CurrentTarget` | Actor | Référence de la cible actuelle |
| `bHasAggro` | Booléen | Indique si l’ennemi est en poursuite |
| `HomeLocation` | Vector | Position d’origine (spawn) |
| `ControlledEnemy` | BP_EnemyBase | Référence au pawn contrôlé |
| `AggroRadius` | Float | Distance max pour conserver l’aggro |
| `AttackRadius` | Float | Distance à laquelle l’ennemi s’arrête pour attaquer |
| `LoseAggroRadius` | Float | Distance max avant perte d’intérêt |
| `LoseAggroDelay` | Float | Délai avant désengagement si cible perdue |
| `LoseAggroTimerHandle` | TimerHandle | Timer de désengagement |

---

## 🔄 Cycle de comportement (`EvaluateAIBehavior`)

Appelé via `SetTimerByFunctionName("EvaluateAIBehavior", 0.2s)` dans `OnPossess`

### ▶️ Logique principale :
```plaintext
Si bHasAggro :
  → Si CurrentTarget non valide → lancer LoseAggro (immédiat)
  → Sinon :
      → Si Distance > LoseAggroRadius → Stop + LoseAggro (via Delay)
      → Si Distance > AttackRadius → MoveToActor(CurrentTarget)
      → Sinon → StopMovement (proche du joueur)
Sinon :
  → MoveToLocation(HomeLocation)
```

Le Delay (0.6s) avant `LoseAggro` empêche les pertes d'aggro trop brutales lors de franchissements rapides.

---

## 🔁 Détails des fonctions spécifiques

### 🔹 `RegisterTarget(Actor NewTarget)`
- Appelée depuis `OnSeePawn` (ennemi)
- Set `CurrentTarget`, `bHasAggro = true`
- Clear `LoseAggroTimerHandle`

### 🔹 `LoseAggro()`
- Set `bHasAggro = false`
- Set `CurrentTarget = None`
- `MoveToLocation(HomeLocation)`

---

## 🧠 Système de perception (`PawnSensing`)

- `PawnSensing_Enemy` détecte un `PlayerCharacter`
- L’événement `OnSeePawn` déclenche la fonction `RegisterTarget()` du contrôleur
- `Sensing Interval` ≤ 0.3 recommandé

---

## ✅ Comportement actuel en jeu

| Situation | Réaction |
|----------|----------|
| Joueur dans champ de vision | Poursuite via MoveToActor |
| Joueur s’éloigne trop | L’ennemi s’arrête + timer de désengagement |
| Perte d’aggro | Retour automatique au point de spawn |
| Re-détection | Reprise immédiate de la poursuite |

---

## 🔧 Extensions prévues

- Attaque (animation + montage si dans `AttackRadius`)
- Gestion d'un `bCanAttack`
- Ajout d’un état de `Stagger` / interruption
- Coopération / Alerte à d’autres ennemis
- Passage à `Behavior Tree` + `Blackboard` pour gestion avancée

---

## 🔗 Liens associés

- [AI_Architecture.md] (vue d’ensemble de l’IA)
- [Combat_Architecture.md]
- [HUD_Architecture.md]

---

## 🕒 Historique
- Création : 27/06/2025
- Dernière mise à jour : 27/06/2025

---
