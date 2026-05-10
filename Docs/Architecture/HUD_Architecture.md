# Architecture Technique — HUD Principal

---

## 📌 Objectif du module

Définir la structure et les règles du HUD principal en jeu :
- Jauges principales (vie, stamina, mana)
- XP, consommables rapides, affichage de l'arme/sort actif
- Pipeline event-driven via OnStatChanged (zero polling)

---

## 🧩 Composants principaux

- **UI_HUD_Main** (widget Blueprint central)
- **BP_PlatformingCharacter** (cree le widget, passe AttributeSetRef, appelle InitHUD)
- **BP_AttributeSet_Base** (dispatche OnStatChanged a chaque changement de stat)
- **DataTable_StatList** (table source des valeurs de stats a l'initialisation)

---

## 📦 Variables, Fonctions & Bindings clés

### Variable centrale
- **AttributeSetRef** (type : BP_AttributeSet_Base, Expose on Spawn)

### Variables locales (Float, default 1.0)
- **HealthPercent** — pourcentage vie courante
- **StaminaPercent** — pourcentage stamina courante
- **ManaPercent** — pourcentage mana courante

### Fonctions de binding (pure, retournent la variable locale)
- **Get_HealthBar_Percent** → return HealthPercent
- **Get_StaminaBar_Percent** → return StaminaPercent
- **Get_ManaBar_Percent** → return ManaPercent

### Event Construct
- Bind HUD_OnStatChanged sur AttributeSetRef.OnStatChanged
- (Le Bind suffit : InitHUD initialise les valeurs, pas besoin d'init dans Event Construct)

### Custom Event HUD_OnStatChanged (StatName [Name], NewValue [Float])
- Switch on Name (StatName) :
    - "HealthCurrent"  → SET HealthPercent  = NewValue / AttributeSetRef.HealthMax
    - "StaminaCurrent" → SET StaminaPercent = NewValue / AttributeSetRef.StaminaMax
    - "ManaCurrent"    → SET ManaPercent    = NewValue / AttributeSetRef.ManaMax

### Fonction InitHUD
- Appelee depuis BP_PlatformingCharacter apres Add to Viewport
- SET HealthPercent  = AttributeSetRef.HealthCurrent  / AttributeSetRef.HealthMax
- SET StaminaPercent = AttributeSetRef.StaminaCurrent / AttributeSetRef.StaminaMax
- SET ManaPercent    = AttributeSetRef.ManaCurrent    / AttributeSetRef.ManaMax

---

## 🔁 Pipeline d'intégration & affichage

1. **Au BeginPlay** (BP_PlatformingCharacter) :
    - InitAttributesFromDatatable → stats initialisees via SetStatValue
    - Add_Main_HUD : Create Widget (AttributeSetRef en Expose on Spawn) → Add to Viewport → InitHUD

2. **Dans le widget (Event Construct)** :
    - Bind HUD_OnStatChanged sur AttributeSetRef.OnStatChanged
    - Les Progress Bars lisent les variables locales *Percent (pas de polling)

3. **Mise a jour en jeu** :
    - Toute modification de stat passe par SetStatValue → OnStatChanged fire → HUD_OnStatChanged → SET *Percent → Progress Bar mise a jour automatiquement
    - Zero acces direct a AttributeSetRef apres l'init

---

## 💡 Bonnes pratiques

- Passer AttributeSetRef a la creation du widget (Expose on Spawn)
- InitHUD appelee APRES Add to Viewport pour garantir la validite de AttributeSetRef
- Les Progress Bars ne lisent que les variables locales *Percent, jamais AttributeSetRef directement
- Toute nouvelle jauge : ajouter une variable *Percent + un case dans HUD_OnStatChanged + init dans InitHUD
- Zero polling : jamais de lecture directe dans Get_*Bar_Percent

---

## 🗺️ Roadmap locale

- [x] Widget HUD avec jauges Health/Stamina/Mana
- [x] AttributeSetRef passe en Expose on Spawn
- [x] Migration polling → event-driven via OnStatChanged (10/05/2026)
- [x] InitHUD pour initialisation correcte au lancement
- [ ] Ajout jauges XP, consommables, buffs
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
- Dernière mise à jour : 10/05/2026

---
