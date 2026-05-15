# Architecture Technique — Gameplay de base (Dash, Roll, Jump, Mouvement)

---

## 📌 Objectif du module

Centraliser toute la logique "core gameplay" du personnage joueur :
- Dash / Roll contextuel (air/sol)
- Jump / Multi-jump / Wall jump
- Gestion d'endurance (stamina) pour chaque action
- Systèmes de flags anti-spam et contrôle de flow
- VFX et feedbacks (Jump trail, etc.)
- Liaison Stat System & HUD

---

## 🧩 Composants principaux

- **BP_SoM_HeroCharacter** (logique movement, input, flags)
- **BP_AttributeSet_Base** (centralisation stamina, coût actions)
- **AnimMontages** (Dash, Roll, Jump…)
- **VFX** : Trail_L, Trail_R (niagara ou autres)
- **UI_HUD_Main** (jauges/bindings)
- **Enhanced Input** : IA_Dodge, IA_Jump…

---

## 📦 Variables & Flags clés

| Nom            | Type       | Description                         |
|----------------|------------|-------------------------------------|
| HasDashed      | Bool       | Anti-spam dash                      |
| HasRolled      | Bool       | Anti-spam roll                      |
| IsDashing      | Bool       | Actuellement en dash                |
| IsRolling      | Bool       | Actuellement en roll                |
| DashMontage    | AnimMontage| Anim dash (root motion)             |
| RollMontage    | AnimMontage| Anim roll (root motion)             |
| StaminaCostDash| Float      | Endurance consommée par dash        |
| StaminaCostJump| Float      | Endurance consommée par saut        |
| ...            | ...        | ...                                 |

---

## 🔁 Pipeline de fonctionnement

### **Initialisation** :
1. Event BeginPlay → Init color des jump trails → Init Attributes from DataTable (crée AttributeSetRef, init Max/Current) → Add_Main_HUD (passe la ref à l'UI).

### **Input Dash/Roll (IA_Dodge)** :
1. Trigger input (Enhanced Input IA_Dodge)
2. Si StaminaCurrent ≥ StaminaCostDash, autorise action, sinon ignore
3. Si IsFalling : dash (air), sinon roll (sol)
4. Flag anti-spam (`HasDashed`/`HasRolled`)
5. Consommation stamina (à l'input, *TODO polish* : placer sur action effective)
6. Montage Play, reset velocity/gravity, active VFX, puis reset flag à la fin via AnimNotify

### **Input Jump** :
1. Trigger input (IA_Jump)
2. Vérif flag IsRolling, stop si true
3. Vérif stamina
4. Consommation stamina, TryMultiJump

---

## 💡 Bonnes pratiques

- Toujours valider toutes les conditions avant de consommer l'endurance
- Reset des flags anti-spam par AnimNotify à la fin du montage
- Séparer clairement Dash et Roll dans les graphes, garder chaque bloc commenté
- Activation/désactivation des VFX dans le flow de chaque action (et reset si besoin)
- Lier tout coût d'action à une variable dédiée dans le Stat System

---

## 🗺️ Roadmap locale

- [x] Implémenter le pipeline input dash/roll/jump clean
- [x] Pipeline d'init ultra lisible (BeginPlay)
- [ ] Optimiser la consommation de stamina pour la placer au moment effectif de l'action
- [ ] Étendre pour wall jump, double jump, ou autres mécaniques selon besoin

---

## 🔗 Liens & docs associées

- [Stats_Architecture.md]
- [HUD_Architecture.md]
- [Combat_Architecture.md] (renvoi pour la partie "attacks/lock-on")
- [UI_Architecture.md]

---

## 🕒 Historique

- Création : 18/06/2025
- Dernière mise à jour : 18/06/2025
- Nommage mis à jour : 15/05/2026 (J-Renommage)

---
