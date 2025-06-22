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

## ✅ État au 21/06/2025

- Système de combo factorisé : TMap<Name, FComboStep> pour accès direct, scalable et lisible.
- ComboStepMap remplie dynamiquement via DataTable_FCombo au BeginPlay, filtrée par arme et niveau.
- Nouvelle gestion dynamique de la fenêtre de combo :  
    - Utilisation du “Get Play Length” du montage pour définir la durée réelle de la combo window (plus de valeurs codées en dur dans la struct, sauf multiplicateur optionnel).
    - À chaque attaque, timer ResetCombo cleané puis relancé pour empêcher les resets fantômes et garantir une fenêtre dynamique.
    - Variable “IsInComboWindow” gérée dans le flow.
- Gestion propre de l’input (Started/Completed), suppression effective du spam d’attaque, prise en compte du relâchement (anti-repeat).
- Prêt pour extension vers le multi-armes (TODO/feuille de route à compléter).
- Toutes les anciennes boucles/forEach et CustomEvents d’attaque sont obsolètes ou en phase de suppression finale.
- Journalisation/débug à chaque layer validée.

---


---

## 🚧 Layers en cours de debug

- **Gestion du notify** (réouverture de CanAttack, validation de la transition sur input pendant la “combo window”, etc.).
- **Gestion des erreurs StepID/NextStepID** (prints à chaque branche pour vérifier les flux).
- **Suppression définitive de l’ancien Event Attack / ForEach** (nettoyage en cours).
- **Sécurisation du pipeline pour l’extension future** (multi-armes, combos contextuels).

---

## 🗺️ TODO / Roadmap

- [x] Gestion dynamique de la fenêtre combo par timer (lié à la durée réelle du montage d’attaque, scalable par struct).
- [ ] Nettoyer totalement la logique d’input ancienne.
- [ ] Ajouter l’option de multiplicateur de fenêtre combo par coup (facultatif, pour ajustement finesse).
- [ ] Factoriser la logique pour autres personnages ou IA (et extension multi-armes, à trancher : dataTable unique ou multiple).
- [ ] Prévoir le branchement UI/feedbacks FX/SFX.
- [ ] (À venir) Ajout d’une gestion ultra-précise par notify pour l’ouverture/fermeture des fenêtres de combo (optionnel, polish).


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

- **21/06/2025** :
    - Mise en place de la gestion dynamique de la fenêtre de combo par timer, synchronisée avec la durée réelle du montage via “Get Play Length”.
    - Debug et validation du flux combo (anti-repeat, ResetCombo propre).
    - Prêt pour tests multi-armes et extension struct.

