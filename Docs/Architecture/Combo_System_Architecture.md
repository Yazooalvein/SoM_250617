# Architecture Technique — Système de Combo (DEBUG EN COURS)

---

## 📌 Objectif du module

Décrire l’architecture actuelle, les couches (“layers”) effectives, le workflow, les points de debug, et la feuille de route du système de combo, tel qu’implémenté dans la refactorisation du 20 et 21 juin 2025.

---

## 🧩 Composants principaux

- **BP_ComboManagerComponent** : composant Blueprint attaché au personnage, responsable de toute la logique combo/data.
- **FComboStep** : struct clé, chargée via DataTable (ComboDataTable).
- **ComboStepMap** : Map (Name → FComboStep) pour un accès direct à chaque étape.
- **BP_PlatformingCharacter** : relai input → ComboManagerComponent.
- **IMC_ARPG_Main** : gestion des actions “LightAttack”, “HeavyAttack” etc.
- **AnimMontage** : asset d’animation d’attaque, section utilisée selon la combo.

---

## 📦 Variables, Fonctions & Layers clés

### **Variables**
- `ComboStepMap` : Map<Name, FComboStep>
- `CurrentStepID` : Name (étape courante du combo)
- `CanAttack` : booléen de contrôle
- `Debug` : prints actifs sur chaque layer

### **Fonctions principales**
- `InitComboTree()` : création de la Map à partir de la DataTable selon arme & niveau (appelée au BeginPlay).
- `HandleAttack(InputType)` : pipeline central, traite chaque input et transition combo.
- `PlayAttackMontage(StepID)` : joue l’animation de la step courante (utilise la fonction utilitaire GetOwningMesh).
- `GetOwningMesh()` : accède à l’AnimInstance du mesh du personnage pour le montage.
- `ResetCombo()` : retour à l’état initial (step = Start, etc.).

---

## 🔁 Pipeline de fonctionnement (layers en place)

1. **Initialisation**
    - Au BeginPlay, `InitComboTree` lit la DataTable, filtre par arme/niveau, et construit la Map `ComboStepMap`.
    - Le CurrentStepID est positionné sur “Start”.

2. **Input**
    - Les actions “LightAttack” / “HeavyAttack” appellent la fonction unique `HandleAttack` avec l’enum en paramètre.
    - (Plus de custom events “Attack” en ForEach.)

3. **Logique HandleAttack**
    - Vérification du CanAttack.
    - Recherche instantanée du step courant via la Map.
    - Transition possible vers le NextStepID (selon input et NextSteps du FComboStep).
    - Mise à jour de l’état, appel à `PlayAttackMontage` pour lancer l’anim.
    - Si transition impossible : ResetCombo.

4. **Animation**
    - `PlayAttackMontage` récupère l’AnimMontage et la section depuis la struct, et joue le montage sur le mesh via AnimInstance.
    - TODO : brancher l’ouverture de la fenêtre de combo et la gestion des inputs via notify d’animation.

5. **Gestion du Reset**
    - ResetCombo appelé en cas d’erreur/fin de chaîne ou après montage (via notify).
    - TODO : affiner la gestion CanAttack & window.

---

## 🚧 Layers en cours de debug

- **Gestion du notify** (réouverture de CanAttack, validation de la transition sur input pendant la “combo window”, etc.).
- **Gestion des erreurs StepID/NextStepID** (prints à chaque branche pour vérifier les flux).
- **Suppression définitive de l’ancien Event Attack / ForEach** (nettoyage en cours).
- **Sécurisation du pipeline pour l’extension future** (multi-armes, combos contextuels).

---

## 🗺️ TODO / Roadmap

- [ ] Finaliser la gestion de la fenêtre combo via notify d’animation (input accepté uniquement pendant la window).
- [ ] Nettoyer totalement la logique d’input ancienne.
- [ ] Documenter tous les edge cases (erreur data, mauvais StepID, etc.).
- [ ] Factoriser la logique pour autres personnages ou IA.
- [ ] Prévoir le branchement UI/feedbacks FX/SFX.

---

## 🕒 Historique journalier

- **20/06/2025** :  
    - Début refactorisation complète du système combo (import, suppression progressive des ForEach).
    - Création de ComboStepMap, HandleAttack, début PlayAttackMontage.
    - Centralisation de la logique input.
    - Début debug (prints sur chaque branch critique).

- **21/06/2025** :  
    - Finalisation de la migration DataTable → Map.
    - Ajout fonction GetOwningMesh pour réutilisation propre dans le composant.
    - Séparation stricte logique progression/exécution animation.
    - Début intégration de la gestion via notify d’animation.
    - Ajout du tag “DEBUG EN COURS” (logs/prints actifs).
    - TODO/cleaning précisé dans la feuille de route.
