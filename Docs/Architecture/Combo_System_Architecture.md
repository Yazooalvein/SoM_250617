# Architecture Technique — Système de Combos

---

## 📌 Objectif du module

Décrire l'architecture du système de combos du projet :
- Gestion multi-armes, évolutive, scalable
- DataTables de combos par type d'arme
- Déblocage et variation des combos selon niveau d'arme
- Lien dynamique avec le système d'armes (WeaponID, Level)
- Pipeline d'exécution et de progression des chaînes de combos

---

## 🧩 Composants principaux

- **DT_Combo_<Type>** (DataTables combos par type d'arme, ex : DT_Combo_Sword, DT_Combo_Axe…)
- **FComboStep** (struct combo : StepID, NextStepID, Anim, LevelMin, FX…)
- **BP_ComboManagerComponent** (composant principal de gestion des combos, attaché au personnage)
- **BP_SoM_HeroCharacter** (transmet WeaponID/Level à l'init combo)
- **Variables clés** : ComboStepMap, CurrentComboStep, CurrentComboWindow, bComboActive…

---

## 📦 Structures & Variables clés

### **FComboStep**
- `StepID` (Name) : identifiant du step combo
- `NextStepID` (Array<Name>) : step(s) suivants possibles
- `WeaponID` (Name) : correspondance DataTable armes (RowName)
- `LevelMin` (int) : niveau minimum d'arme requis pour débloquer ce combo
- `AnimMontage` (AnimMontage) : animation associée
- `FX/SFX` (option) : FX à déclencher à ce step
- *(option : InputType, DamageMultiplier, etc.)*

### **Variables principales**
- **ComboStepMap** (TMap<Name, FComboStep>) : accès direct step par ID
- **CurrentComboStepID** (Name) : step en cours
- **CurrentComboWindow** (TimerHandle) : fenêtre de combo active
- **bComboActive** (bool) : combo en cours

---

## 🔁 Pipeline de fonctionnement

### **1. Initialisation**
- À la validation d'une arme dans le radial, le BP_ComboManager :
    - Récupère WeaponID & Level de l'arme équipée
    - Charge la DataTable combo correspondant au type d'arme
    - Boucle sur la DT :
        - Pour chaque step, si WeaponID et LevelMin sont valides, ajoute à ComboStepMap (clé = StepID)
    - Reset les variables de progression (CurrentComboStepID, bComboActive…)

### **2. Exécution du combo**
- À chaque input d'attaque :
    - Vérifie la validité du combo (fenêtre active, anti-repeat)
    - Récupère le FComboStep via ComboStepMap[CurrentComboStepID]
    - Joue l'animation (AnimMontage)
    - Lance les FX/SFX associés (via struct ou DT)
    - Ouvre la fenêtre combo (durée = Get Play Length de l'anim)
    - À l'input suivant :
        - Vérifie si StepID existe dans NextStepID[]
        - Passe à l'étape suivante ou reset

### **3. Progression/Déblocage**
- Seuls les combos dont LevelMin <= niveau de l'arme sont actifs
- Ajout d'un nouveau combo = ajout d'une ligne dans la DT correspondante

### **4. Reset / anti-repeat**
- Le système reset la progression si la fenêtre combo est dépassée
- Bloque le spam input (anti-repeat sur Started/Completed)

---

## 🛠️ Bonnes pratiques & patterns utilisés

- **Accès ultra-rapide via TMap** (vs DataTable lookup à chaque input)
- **DataTables distinctes par type d'arme** (extensible, évolutif)
- **Struct évolutive** : FComboStep peut être enrichie (input, FX, damage, etc.)
- **Décorrélation totale des combos/armes : pipeline scalable multi-type**
- **Modularité : ajout/suppression/modif de combo sans toucher au BP**

---

## 🗺️ TODO / Roadmap

- [ ] Ajouter un fallback "combo parent" pour les niveaux sans combo spécifique
- [ ] Factoriser l'ajout de FX/SFX/camera shake par step via DataTable
- [ ] Gérer les conditions avancées (state machine, buff/debuff, contextuel…)
- [ ] Ajout d'un système d'UI pour afficher la progression combo (debug/player)
- [ ] Prévoir compatibilité futurs types d'input spéciaux (ex : sorts, projectiles)

---

## 🕒 Historique

- Création : 19/06/2025
- MAJ lourde : 24/06/2025 (support multi-armes data-driven, niveau, TMap, pipeline radial, fix anti-repeat, combos évolutifs)
- Nommage mis à jour : 15/05/2026 (J-Renommage)

---

## **Fin du doc — relu et validé par [à compléter]**
