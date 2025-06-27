# Architecture Technique — Intelligence Artificielle (IA)

---

## 🎯 Objectif du système IA

Fournir une structure modulaire, évolutive et cohérente pour l’ensemble des entités intelligentes du jeu (ennemis, PNJ, objets interactifs), basée sur Unreal Engine 5.6 (Blueprint Only).

---

## 🧩 Types d'entités IA prévues

### 1. 🧠 **Ennemis**
- Comportement : poursuite, attaque, désengagement, retour au point d'origine
- Dérivent de `BP_EnemyBase` et sont contrôlés par `BP_AIController_Enemy_Base`
- Réagissent à la détection via `PawnSensing`

### 2. 🧍‍♂️ **PNJ (personnages non joueurs)**
- Comportement : interaction avec le joueur, dialogues, réactions simples
- Seront contrôlés par un futur `BP_AIController_NPC_Base`
- Comportement passif et centré sur les événements ou le déclenchement de dialogues

### 3. 🧱 **Objets interactifs intelligents**
- Exemples : coffres verrouillés, pièges, portes animées
- Pas nécessairement des pawns, mais peuvent embarquer une logique de type IA ou s’appuyer sur le système de perception

---

## 🧠 Systèmes communs d’IA

### ▶️ **Contrôleurs IA**
- Tous les pawns IA sont contrôlés par une classe dérivée de `AIController`
- Base commune prévue : `BP_AIController_Base`

### 🔎 **Système de détection (`PawnSensing`)**
- Utilisé dans les ennemis
- Détection visuelle uniquement pour le moment (cone + distance)
- Déclenche `OnSeePawn` → cible stockée via `RegisterTarget()` dans le contrôleur

### 🧭 **Navigation (NavMesh)**
- Tous les déplacements utilisent `MoveToActor` / `MoveToLocation`
- Le NavMesh est requis dans chaque niveau pour permettre les mouvements IA

### 🔁 **État comportemental simplifié**
- `bHasAggro`, `CurrentTarget`, `HomeLocation` : utilisés pour gérer les transitions de comportement
- Timers (`LoseAggroTimerHandle`) permettent de désengager après perte de vue

---

## 🏗️ Convention & bonnes pratiques

- Chaque type d’IA a son propre `AIController` dédié
- L’intelligence est **centralisée dans le contrôleur**, pas dans le pawn
- Toutes les détections sont traitées par événement (`OnSeePawn`) et relayées au contrôleur
- Les comportements doivent être encapsulés dans des fonctions nommées explicitement (`EvaluateAIBehavior`, `LoseAggro`, `RegisterTarget`, etc.)
- Tous les timers sont stockés dans des `TimerHandle` nommés, annulés proprement via `ClearAndInvalidate`
- Le comportement d’un pawn IA ne doit jamais dépendre directement du joueur, mais uniquement de sa cible

---

## 🛣️ Roadmap prévue

- [x] Mise en place IA ennemis de base (sensing + poursuite + retour)
- [ ] Ajout logique d’attaque (montage ou behavior)
- [ ] IA PNJ : architecture base NPC passive (dialogue / réaction / événement)
- [ ] Système de blackboard + behavior tree pour transitions plus propres
- [ ] Système d’esquive / fuite pour IA non-agressive (faune, civils…)

---

## 📎 Liens documentaires associés

- [Enemy_AI_Behavior.md] *(détail du comportement des ennemis)*
- [Combat_Architecture.md]
- [UI_Architecture.md]
- [Journal_Modifications_ARPG.md]

---

## 🕒 Historique

- Création : 27/06/2025
- Dernière mise à jour : 27/06/2025

---
