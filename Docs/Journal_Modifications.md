# 📝 Journal des Modifications — Shadow of Mana (ARPG Blueprint Only / UE5.6+)

---

## Objectif

Assurer un **suivi précis et transparent** de toutes les évolutions majeures, correctifs, refactors et ajouts au projet, en cohérence avec le versionning Git.

---

## 🔖 Format recommandé pour chaque entrée

- **Date**
- **Auteur**
- **Résumé clair de la modification**
- **Fichiers / systèmes impactés**
- **Lien commit (optionnel, si remote Git)**

---

## ✅ Entrées

---

### Création du projet & documentation initiale

- **17/06/2025** — [Ton nom]
    - **Initialisation du projet Shadow of Mana (ARPG) sous UE5.6, base template Third Person Plateforming**
    - Création et structuration des documents de base :
        - Présentation_Générale_du_Projet.md
        - Project_Architecture_Index.md
        - Journal_Modifications_ARPG.md
        - Dossier `/Architecture` et squelettes par module
        - Structure_Dossier_Content.md
        - Dossier `/Dev/Sandbox` pour les prototypes

---

### 18/06/2025 — [Ton nom]
- Refactoring complet du pipeline “Gameplay de base” du personnage :  
    - Segmentation du code entre Dash, Roll, Jump, Flags, Stamina.
    - Ajout de “BasicGameplay_Architecture.md” pour centraliser tout ce qui concerne le mouvement, les consommations de stamina, les flags anti-spam, et les feedbacks VFX (jump trail, etc.).
    - Mise à jour de Stats_Architecture.md (ajout des coûts action, pipeline d’init, enrichissement du switch SetStatValue).
    - Mise à jour de HUD_Architecture.md (ordre d’appel initialisation/ref, bindings supplémentaires si besoin).
    - Nettoyage du doc Combat pour le réserver à l’attaque/lock-on/IA.
- Convention : tout ajout d’action principale ou stat associée doit être documenté dans le doc “Gameplay de base”.

---
### 19-20/06/2025

- Import complet du système Lock-On, refactorisation et ajouts :
    - Détection continue à chaque switch de cible.
    - Clamp vertical du pitch caméra (min/max).
    - TODO : Ajout du système d’unlock auto hors rayon.
- Menu Radial importé et refactorisé :
    - Structure dynamique (n slots), gestion rotation/alignement, orientation icônes (anti-spin TODO).
    - TODO : Ajout struct config, dispatcher sélection, logique de désactivation réutilisable pour d’autres menus.
- Import et refonte complète du système de Combo :
    - Passage ComboStepArray -> ComboStepMap (accès direct, suppression des boucles sur input).
    - Nouvelle fonction centralisée HandleAttack, PlayAttackMontage dédiée.
    - Mise en place du pattern “accès direct + gestion StepID/NextStepID”.
    - Factorisation GetOwningMesh dans le composant.
    - Ajout prints pour debug complet du flow.
    - Ancienne logique par Custom Event/ForEach en cours de suppression.
    - TODO : Finaliser la gestion NextStepID lors du notify de fin d’animation (layer “notify” à debugger).
    - TODO : Nettoyage final des anciens Events.
    - DEBUG EN COURS (cf. doc Combo System Architecture pour détail).

- Mise à jour des architectures techniques Combo/Lock-On/UI.

---
### 21/06/2025

- Refactorisation complète du système de ComboManagerComponent (BP_ComboManagerComponent) :
    - Passage d’un système en array/loop à une map (TMap<Name, FComboStep>) pour la gestion des étapes de combos, factorisation et clarté améliorée.
    - Liaison dynamique avec Datatable_FCombo.
    - Ajout de la gestion dynamique de la fenêtre de combo avec timer, basé sur la durée réelle de l’Anim Montage (“Get Play Length”).
    - Ajout du bool “IsInComboWindow” et clean des timers à chaque coup.
    - Liaison propre avec l’input (Reset Combo, gestion “CanAttack” sur Started/Completed).
    - Système désormais prêt à accueillir la gestion multi-armes ultérieure (TODO structuré dans la doc).
    - Debug et journalisation des étapes internes, validation du flux BP.
    - TODO : Gestion multi-armes, fenêtrage par sections, DataTable unifiée ou multiple à trancher plus tard.

**Avancement : Combo jouable, propre, et entièrement modulable.**

---
### 24/06/2025 — [Ton nom]
- **Refactor & finalisation du système d’armes data-driven :**
    - Structuration complète de la DataTable DT_Weapons (FWeaponData), avec gestion du type, niveau, mesh, icon, socket, BPClass…
    - Ajout de l’array dynamique DiscoveredWeapons (struct FDiscoveredWeapon), centralisation dans BP_Character.
    - Ajout et mise à jour automatique des slots lors de la découverte/évolution d’une arme.
    - Pipeline d’équipement/détachement 100% factorisé, spawn dynamique du BPClass, support offset/rotation à venir.
    - Détachement propre de l’arme précédente.
    - Validation de la synchro Weapons <-> Radial <-> ComboSystem.

- **Menu Radial :**
    - Génération des slots depuis DiscoveredWeapons/DT_Weapons (icônes, RowName, ordre dynamique).
    - Passage à un système data-driven (arrays SlotIcons et SlotRowNames synchronisés à chaque ouverture).
    - Gestion du curseur/highlight central via CurrentSelectedIndex (plus d’array tournant).
    - Sélection de l’arme sur InputAction “Valider”, propagation du RowName au personnage.
    - Compatibilité totale souris/gamepad/clavier via IMC.
    - Ajout des feedbacks visuels sur slot sélectionné, surlignage dynamique.
    - Refonte/MAJ doc RadialMenu_Architecture.md.

- **Combo System :**
    - Pipeline combo multi-armes/multi-niveaux opérationnel (DataTable combo par type).
    - Initialisation du combo tree déplacée sur validation de l’arme (plus à chaque attaque).
    - Map d’accès rapide (TMap) pour StepID/NextStepID, anti-repeat sécurisé.
    - Déblocage dynamique des combos via LevelMin.
    - Synchronisation WeaponID/Level avec le système d’armes (passage automatique lors de l’équipement).
    - MAJ complète de Combo_System_Architecture.md.

- **Bugs/Correctifs :**
    - Correction de l’effacement d’array lors de la boucle d’initialisation des slots radial (usage Add au lieu de Set).
    - Fix combo tree qui se réinitialisait à chaque input attaque (inversion du point d’appel).
    - Correction du sens de certains meshes lors de l’attach (debug offsets/socket, TODO struct DT).
    - Vérification de la robustesse UI/équipement sur permutations rapides.

- **Documentation & Architecture :**
    - Création du doc Weapons_System_Architecture.md (pipeline complet, bonnes pratiques, TODO, historique…).
    - MAJ lourde RadialMenu_Architecture.md (nouvelle struct, arrays dynamiques, gestion input, sélection…).
    - MAJ complète Combo_System_Architecture.md (workflow multi-armes, LevelMin, anti-repeat, synchro WeaponID…).
    - Ajout du jalon dans Journal_Modifications_ARPG.md (présent).

- **TODO / Jalons immédiats :**
    - Ajouter le support offset/rotation par arme dans DT_Weapons et l’appliquer à l’attach.
    - Préparer l’intégration d’un inventaire avancé (pickup, drop, remove…).
    - Implémenter feedbacks VFX/SFX lors de l’équipement et du combo.
    - Sauvegarder/restaurer l’état arme/équipement du joueur.
    - Prévoir le verrouillage/cooldown des slots radial et le fallback “slot vide”.

---


---

### [À compléter à chaque évolution]

- **[JJ/MM/AAAA] — [Auteur]**
    - **Résumé**
    - Fichiers/documents/systèmes concernés
    - [Lien commit optionnel]

---

## 📌 Rappel

Ce document doit être systématiquement mis à jour à chaque modification significative du projet  
(idéalement à chaque push Git ou milestone).

---

## 📜 Historique

- Création : 17/06/2025
- Dernière mise à jour : [21/06/2025]

---
