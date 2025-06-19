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
- Dernière mise à jour : [19/06/2025]

---
