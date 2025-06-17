# Architecture Technique — Menu Radial

---

## 📌 Objectif du module

Décrire l’architecture du système de menu radial :  
- Navigation dynamique (armes, objets, sorts…)
- Interaction au pad/clavier, menu circulaire évolutif
- Intégration avec le Stat System, l’UI, et le PlayerController

---

## 🧩 Composants principaux

- UI_RadialMenu (UserWidget principal)
- UI_RadialSlot (slot individuel)
- BP_PlayerController (création, affichage, input menu radial)
- Struct FSlotData (pour data-driven icons/labels)
- Data/Assets d’icônes (textures)

---

## 📦 Variables, Fonctions & Structures clés

> **Basé sur l’itération précédente du projet (ancienne doc Radial Menu).  
> Méthodes, variables, pipelines de placement/rotation, gestion input et logiques UI seront récupérés et adaptés ici.**

---

## 🔁 Pipeline de fonctionnement

1. Ouverture/fermeture via input dédié (clavier/pad)
2. Génération dynamique des slots à partir d’une array de data/struct
3. Positionnement radial automatisé, gestion du curseur
4. Binding et feedback visuel en temps réel
5. Synchro avec pause/focus Game vs UI

---

## 🗺️ Roadmap locale

- [ ] Refactor UI_RadialMenu & UI_RadialSlot selon le nouveau template
- [ ] Adapter la logique d’input Enhanced Input (pad/keyboard)
- [ ] Réintégrer la data-driven structure via FSlotData

---

## 🔗 Liens & docs associées

- [UI_Architecture.md]
- [Journal_Modifications.md]
- [Project_Architecture_Index.md]
- [Stats_Architecture.md]
- [Combat_Architecture.md]

---

## 🕒 Historique

- Création : 17/06/2025
- Dernière mise à jour : [JJ/MM/AAAA]

---
