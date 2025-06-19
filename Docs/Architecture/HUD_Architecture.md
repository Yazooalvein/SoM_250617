# Architecture Technique — HUD Principal

---

## 📌 Objectif du module

Définir la structure et les règles du HUD principal en jeu :
- Jauges principales (vie, stamina, mana)
- XP, consommables rapides, affichage de l’arme/sort actif, portrait joueur
- Pipeline de binding synchrone avec le Stat System

---

## 🧩 Composants principaux

- **UI_HUD_Main** (widget Blueprint central)
- **BP_PlayerController** (instancie et ajoute le widget au viewport au BeginPlay, transmet la ref AttributeSetRef via “Expose on Spawn”)
- **BP_AttributeSet_Base** (centralise les valeurs des stats, bindées dynamiquement sur le HUD)
- **DataTable_StatList** (table source des valeurs de stats à l’initialisation)
- Autres widgets contextuels/secondaires si besoin (buff, message, etc.)

---

## 📦 Variables, Fonctions & Bindings clés

### **Variable centrale :**
- **AttributeSetRef** (type : BP_AttributeSet_Base, Expose on Spawn)

### **Fonctions de binding (exemples) :**
- **Get_HealthBar_Percent**
- **Get_StaminaBar_Percent**
- **Get_ManaBar_Percent**
    - Pipeline :  
        - Vérifie `IsValid(AttributeSetRef)`
        - Si Max > 0, retourne Current / Max
        - Sinon retourne 0

### **Autres variables possibles :**
- XP, NextLevelXP, WeaponSlot, QuickItem, etc.

---

## 🔁 Pipeline d’intégration & affichage

1. **Au BeginPlay** (BP_PlayerController ou PlayerCharacter) :
    - Instancie `BP_AttributeSet_Base`
    - Initialise les valeurs via la DataTable
    - Crée le widget `UI_HUD_Main` avec la ref AttributeSetRef en “Expose on Spawn”
    - Ajoute le widget au viewport

2. **Dans le widget** :
    - Les jauges (Health, Stamina, Mana) sont bindées en direct sur AttributeSetRef
    - Tous les bindings UI vérifient la validité de la référence (IsValid)
    - Aucun accès direct au PlayerCharacter

3. **Mise à jour** :
    - Toute modif (dégâts, soin, consommation, régénération…) se reflète instantanément dans le HUD
    - Debug possible via macro DebugPrintVar
    - L’AttributeSet doit être instancié et initialisé (valeurs Max/Current prêtes) **avant** la création du HUD pour garantir l’exactitude des valeurs affichées.
    - Tout ajout de jauge/action (stamina jump, stamina dash…) implique un nouveau binding UI, toujours sur la référence AttributeSetRef.

---

## 💡 Bonnes pratiques

- Passer systématiquement la référence `AttributeSetRef` à la création du widget (Expose on Spawn)
- Les bindings sont toujours “fail safe” : `IsValid` + division par Max > 0
- Aucune variable stat n’est stockée côté widget, uniquement la ref à l’AttributeSet
- L’ajout d’une nouvelle stat nécessite juste un binding UI supplémentaire, sans modif du pipeline
- Commente chaque fonction de binding pour lisibilité

---

## 🗺️ Roadmap locale

- [x] Reprise du widget HUD de l’ancien projet
- [x] Adaptation du binding sur le nouveau système AttributeSetRef
- [ ] Ajout/extension des jauges ou éléments contextuels (buffs, consommables…)
- [ ] Extension UI debug en overlay si besoin

---

## 🔗 Liens & docs associées

- [Stats_Architecture.md]
- [UI_Architecture.md]
- [Journal_Modifications.md]
- [Project_Architecture_Index.md]

---

## 🕒 Historique

- Création : 17/06/2025
- Dernière mise à jour : 18/06/2025

---
