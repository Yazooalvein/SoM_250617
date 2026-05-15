# Architecture Technique — Stat System

---

## 📌 Objectif du module

Centraliser toute la logique liée à la gestion des statistiques du jeu :
- Santé, mana, stamina, XP, progression, etc.
- Initialisation, modification, synchronisation avec l'UI et le gameplay
- Pipeline extensible et "future proof" (GAS-friendly mais full BP)

---

## 🧩 Composants principaux

- **BP_AttributeSet_Base** (Blueprint d'Object, dossier `/Content/Systems/Stats/`)
- **DT_StatList** (DataTable avec struct `StatStruct`)
- **Enums** :
    - `EElementType` : None, Athanor, Dryade, Gnome, Lumina, Luna, Ombre, Ondine, Sylphide
    - `EStatType` : Principal, Elem, Second, Progression, Temp
- **BP_SoM_HeroCharacter** (possède une variable `AttributeSetRef`)
- **OnStatChanged** (Event Dispatcher, notifie tous les abonnés)
- **Widgets liés** (UI_HUD_Main)

---

## 📦 Variables, Fonctions & Structures clés

### Struct `StatStruct` (DataTable)
| Champ         | Type            | Description                        |
|---------------|-----------------|-------------------------------------|
| StatID        | Name            | Identifiant unique                  |
| DisplayName   | Text            | Nom affiché en UI/localisation      |
| Description   | Text            | Description détaillée               |
| Type          | EStatType       | Principal, Elem, etc.               |
| Element       | EElementType    | None, Athanor, etc.                 |
| BaseValue     | Float           | Valeur de base                      |
| MinValue      | Float           | Borne min                           |
| MaxValue      | Float           | Borne max                           |
| IsModifiable  | Bool            | Peut être modifiée en jeu ?         |
| Icone         | Texture2D       | Icône UI                            |
| GameplayTag   | GameplayTag     | Pour extension GAS/filtres          |

### Convention de nommage des stats (sans espace, CamelCase)

| Nom dans Switch | Variable BP |
|---|---|
| HealthCurrent | HealthCurrent |
| HealthMax | HealthMax |
| StaminaCurrent | StaminaCurrent |
| StaminaMax | StaminaMax |
| ManaCurrent | ManaCurrent |
| ManaMax | ManaMax |
| StaminaCostJump | StaminaCostJump |
| StaminaCostDash | StaminaCostDash |
| StaminaRegenRate | StaminaRegenRate |
| StaminaRegenDelay | StaminaRegenDelay |
| StaminaRegenInterval | StaminaRegenInterval |

> ⚠️ Les noms doivent être identiques entre le Switch de SetStatValue, les appels depuis le gameplay, et le Switch du HUD. Aucun espace.

### Fonctions/Macros principales

- **SetStatValue** (StatName [Name], Value [Float])
    - Switch sur StatName → SET la variable correspondante → Call OnStatChanged(StatName, NewValue)
    - **Point d'entrée unique pour toute modification de stat**
- **ConsumeStamina** (Amount [Float])
    - Clamp(StaminaCurrent - Amount, 0, StaminaMax) → SetStatValue("StaminaCurrent")
    - Puis Clear Timer + SET bIsStaminaRegenerating = false + Set Timer StartStaminaRegen
- **StartStaminaRegen / HandleStaminaRegen**
    - HandleStaminaRegen : SetStatValue("StaminaCurrent", Clamp(Current + Rate * Interval, 0, Max))
- **OnStatChanged** (Event Dispatcher)
    - Paramètres : StatName [Name], NewValue [Float]
    - Appelé automatiquement par SetStatValue apres chaque modification
- **DebugPrintVar** (macro : VarName, VarValue, Prefix, IsCritical)

---

## 🔁 Pipeline de fonctionnement

1. **Initialisation au lancement** :
    - BP_SoM_HeroCharacter instancie BP_AttributeSet_Base (Construct Object from Class)
    - Loop sur la DataTable → SetStatValue(StatID, BaseValue) pour chaque Max
    - Apres Completed : SetStatValue("HealthCurrent", HealthMax) + Stamina + Mana
    - Stocke la reference dans `AttributeSetRef`
    - Cree UI_HUD_Main avec AttributeSetRef en Expose on Spawn → Add to Viewport → InitHUD

2. **Modification de stat** :
    - Toute modif passe obligatoirement par SetStatValue
    - SetStatValue SET la variable ET appelle OnStatChanged
    - Exemples : ReceiveDamage → SetStatValue("HealthCurrent"), ConsumeStamina → SetStatValue("StaminaCurrent")

3. **Notification des abonnes** :
    - OnStatChanged est un Event Dispatcher bindable par n'importe quel systeme
    - UI_HUD_Main se bind dans son Event Construct
    - Extensible : ennemis, boss, effets de seuil peuvent aussi se binder

4. **Sauvegarde (futur)** :
    - Les valeurs Current ne sont pas dans la DataTable (valeurs de reference statiques)
    - Prevoir un SaveGame Object dedie pour snapshot/restore des Current via SetStatValue

---

## 🗺️ Roadmap locale

- [x] Creation du BP_AttributeSet_Base (structure variables + fonctions principales)
- [x] Import de la DataTable avec struct et enums
- [x] Pipeline d'initialisation/consommation/regen stamina fonctionnel
- [x] Macro DebugPrintVar utilisee partout
- [x] OnStatChanged Event Dispatcher operationnel (10/05/2026)
- [x] SetStatValue = unique point de modification, toutes les fonctions migreees
- [x] Convention nommage unifiee sans espace
- [ ] Systeme SaveGame pour sauvegarde/restauration des Current
- [ ] Dupliquer/etendre pour ennemis/boss/compagnons si besoin

---

## 🔗 Liens & docs associees

- [Journal_Modifications.md]
- [Project_Architecture_Index.md]
- [Présentation_Générale_du_Projet.md]
- [UI_Architecture.md]
- [HUD_Architecture.md]

---

## 💡 Bonnes pratiques

- Toute nouvelle stat : ajouter dans la DataTable ET dans le BP + Switch de SetStatValue
- Nommage sans espace, CamelCase, identique partout
- SetStatValue = seul point d'entree, jamais de SET direct sur les variables
- DataTable = source unique de verite pour les valeurs Max/Reference
- Les valeurs Current s'initialisent = Max apres la boucle DataTable
- Documenter chaque variable et fonction (tooltip)

---

## 🕒 Historique

- Création : 17/06/2025
- Dernière mise à jour : 10/05/2026
- Nommage mis à jour : 15/05/2026 (J-Renommage)

---
