# Architecture Technique — Stat System

---

## 📌 Objectif du module

Centraliser toute la logique liée à la gestion des statistiques du jeu :  
- Santé, mana, stamina, XP, progression, etc.
- Initialisation, modification, synchronisation avec l’UI et le gameplay

---

## 🧩 Composants principaux

- BP_AttributeSet_Base (stat container principal)
- DataTable_StatList (source unique des valeurs de base)
- BP_PlayerCharacter (détient la référence AttributeSetRef)
- EventDispatcher(s) pour notification UI/Debug/Save
- Widgets liés (HUD, debug, etc.)

---

## 📦 Variables, Fonctions & Structures clés

> **Basé sur l’itération précédente du projet (ancienne doc Stat System Architecture).  
> Les signatures de fonctions, noms de variables, structures, conventions seront récupérés/adaptés ici.**

---

## 🔁 Pipeline de fonctionnement

1. Initialisation des stats via DataTable au lancement du jeu
2. Modification des stats via une fonction centrale (`ApplyStatChange`/`SetStatValue`)
3. Notification des changements de stat via EventDispatcher
4. Binding de l’UI par référence unique (AttributeSetRef)

---

## 🗺️ Roadmap locale

- [ ] Récupérer et adapter la structure BP_AttributeSet_Base depuis l’ancien projet
- [ ] Créer DataTable_StatList avec toutes les stats nécessaires
- [ ] Refactor pipeline d’initialisation/consommation/notification pour le nouveau projet
- [ ] Vérifier la compatibilité et la facilité d’ajout de nouvelle stat

---

## 🔗 Liens & docs associées

- [Journal_Modifications.md]
- [Project_Architecture_Index.md]
- [Présentation_Générale_du_Projet.md]
- [UI_Architecture.md]

---

## 🕒 Historique

- Création : 17/06/2025
- Dernière mise à jour : [JJ/MM/AAAA]

---
