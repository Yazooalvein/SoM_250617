# Architecture Technique — Système d'Entrée & Contrôles

---

## 📌 Objectif du module

Centraliser la gestion des entrées :
- Enhanced Input (clavier, souris, pad, mobile/touch si besoin)
- Mapping contextuel (jeu, UI, menu radial…)
- Règles de priorisation, exécution en pause, gestion dynamique des contextes

---

## 🧩 Composants principaux

- **InputMappingContexts actifs** : IMC_Default, IMC_Platforming, IMC_Prototype
- **InputActions** : source unique dans `Content/Input/InputActions/`
- **BP_PlatformingCharacter** (consommateur principal des inputs)
- **BP_PlatformingPlayerController** (consommateur secondaire)

---

## 📦 Source unique des InputActions

Toutes les IA sont dans `Content/Input/InputActions/` :

| InputAction | Usage |
|---|---|
| IA_Move | Déplacement |
| IA_Look | Caméra (souris + gamepad) |
| IA_Jump | Saut |
| IA_Dodge | Dash / Roll |
| IA_Sprint | Sprint |
| IA_LockOn | Verrouillage cible |
| IA_Attack_Light | Attaque légère |
| IA_Attack_Heavy | Attaque lourde |
| IA_Block | Parade |
| IA_RadialMenu | Menu radial armes |

---

## 🔁 Pipeline de fonctionnement

1. Initialisation du mapping Enhanced Input au BeginPlay (PlayerController)
2. Attribution dynamique des contextes selon l'état du jeu
3. BP_PlatformingCharacter et BP_PlatformingPlayerController consomment les IA
4. Priorité/contextes gérés par les IMC actifs

---

## 🗺️ Roadmap locale

- [x] Unification des inputs : suppression vestiges template ThirdPerson (10/05/2026)
- [x] Source unique : Content/Input/InputActions/
- [x] Suppression BP_ThirdPersonCharacter, BP_ThirdPersonGameMode, IMC_MouseLook
- [ ] Préparer la compatibilité future mobile/autres devices si besoin

---

## 🔗 Liens & docs associées

- [Journal_Modifications.md]
- [Project_Architecture_Index.md]
- [UI_Architecture.md]
- [RadialMenu_Architecture.md]

---

## 🕒 Historique

- Création : 17/06/2025
- Dernière mise à jour : 10/05/2026

---
