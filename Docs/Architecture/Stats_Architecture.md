# Architecture Technique — Stat System

---

## 📌 Objectif du module

Centraliser toute la logique liée à la gestion des statistiques du jeu :
- Santé, mana, stamina, XP, progression, etc.
- Initialisation, modification, synchronisation avec l’UI et le gameplay
- Pipeline extensible et “future proof” (GAS-friendly mais full BP)

---

## 🧩 Composants principaux

- **BP_AttributeSet_Base** (Blueprint d’Object, dossier `/Content/Systems/Stats/`)
- **Datatable_StatList** (DataTable avec struct `StatStruct`)
- **Enums** :
    - `EElementType` : None, Athanor, Dryade, Gnome, Lumina, Luna, Ombre, Ondine, Sylphide
    - `EStatType` : Principal, Elem, Second, Progression, Temp
- **BP_PlayerCharacter** (possède une variable `AttributeSetRef`)
- **EventDispatchers** (prévu pour notification UI, debug, etc.)
- **Widgets liés** (HUD, debug...)

---

## 📦 Variables, Fonctions & Structures clés

### Struct `StatStruct` (DataTable)
| Champ         | Type            | Description                        |
|---------------|-----------------|------------------------------------|
| StatID        | Name            | Identifiant unique                 |
| DisplayName   | Text            | Nom affiché en UI/localisation     |
| Description   | Text            | Description détaillée              |
| Type          | EStatType       | Principal, Elem, etc.              |
| Element       | EElementType    | None, Athanor, etc.                |
| BaseValue     | Float           | Valeur de base                     |
| MinValue      | Float           | Borne min                          |
| MaxValue      | Float           | Borne max                          |
| IsModifiable  | Bool            | Peut être modifiée en jeu ?        |
| Icone         | Texture2D       | Icône UI                           |
| GameplayTag   | GameplayTag     | Pour extension GAS/filtres         |

### Variables BP_AttributeSet_Base (exemples actuels)

- **Santé** :
    - HealthMax (Float)
    - HealthCurrent (Float)
- **Stamina** :
    - StaminaMax (Float)
    - StaminaCurrent (Float)
    - StaminaRegenRate (Float)
    - StaminaRegenDelay (Float)
    - StaminaRegenInterval (Float)
    - StaminaCostJump (Float)
    - StaminaCostDash (Float)
    - bIsStaminaRegenerating (Bool)
- **Mana** :
    - ManaMax (Float)
    - ManaCurrent (Float)
- **Élémentaire / Progression** :
    - AffinityAthanor (Float)
    - ResistanceOmbre (Float)
    - WeaponLevel (Float)
- (Ajouter toutes les stats présentes dans la DataTable !)

### Fonctions/Macros principales

- **SetStatValue** (StatName [Name], Value [Float])  
    - Switch sur StatName, set la variable correspondante
- **ApplyStatChange** (optionnel, wrapper pour modif/delta)
- **ConsumeStamina** (logique consommation stamina)
- **StartStaminaRegen / HandleStaminaRegen** (gestion timer, clamp, reset flag)
- **DebugPrintVar** (macro : VarName, VarValue, Prefix, IsCritical)
- Toute initialisation doit assigner la valeur “Current” à la valeur “Max” correspondante (pour Health, Stamina, Mana…) après le loop DataTable.

---

## 🔁 Pipeline de fonctionnement

1. **Initialisation au lancement** :
    - PlayerCharacter instancie BP_AttributeSet_Base (Construct Object from Class)
    - Loop sur la DataTable pour chaque StatID → SetStatValue(StatID, BaseValue)
    - Stocke la référence dans `AttributeSetRef`
2. **Modification de stat** :
    - Toute modif passe par SetStatValue ou ApplyStatChange
    - Ajout (optionnel) d’Event Dispatcher pour notifier la UI ou autres systèmes
3. **Liaison avec l’UI/HUD** :
    - Sur création du widget HUD, passer `AttributeSetRef` en “Expose on Spawn”
    - Les bindings UI accèdent dynamiquement aux valeurs (Get_HealthBar_Percent, etc.)
    - Les fonctions de binding vérifient la validité (`IsValid`), divisent par Max (check > 0), sinon retournent 0

---

## 🗺️ Roadmap locale

- [x] Création du BP_AttributeSet_Base (structure variables + fonctions principales)
- [x] Import de la DataTable avec struct et enums
- [x] Pipeline d’initialisation/consommation/regen stamina fonctionnel
- [x] Macro DebugPrintVar utilisée partout
- [ ] Ajouter EventDispatcher “OnStatChanged” pour automatiser la notif UI (optionnel/à venir)
- [ ] Préparer duplicata/extension pour ennemis/boss/compagnons si besoin

---

## 🔗 Liens & docs associées

- [Journal_Modifications.md]
- [Project_Architecture_Index.md]
- [Présentation_Générale_du_Projet.md]
- [UI_Architecture.md]
- [HUD_Architecture.md]

---

## 💡 Bonnes pratiques

- Ajouter toute nouvelle stat dans la DataTable **et** dans le BP + Switch
- Grouper et nommer toutes les variables par type/stat (ex : HealthMax, HealthCurrent)
- Documenter chaque variable et fonction (tooltip)
- Isoler la logique métier dans le BP, l’UI ne fait que lire/afficher
- Centraliser le debug, utiliser la macro
- DataTable = source unique de vérité

---

## 🕒 Historique

- Création : 17/06/2025
- Dernière mise à jour : 19/06/2025

---
