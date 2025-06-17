# Architecture Technique — Système d’Entrée & Contrôles

---

## 📌 Objectif du module

Centraliser la gestion des entrées :  
- Enhanced Input (clavier, souris, pad, mobile/touch si besoin)
- Mapping contextuel (jeu, UI, menu radial…)
- Règles de priorisation, exécution en pause, gestion dynamique des contextes

---

## 🧩 Composants principaux

- InputMappingContext(s) (IMC_Gameplay, IMC_UI, IMC_RadialMenu, etc.)
- InputActions (Move, Jump, Attack, Dodge, RadialMenu, Debug, etc.)
- BP_PlayerController (initialisation mapping, switch context)
- Widgets ou UI qui nécessitent des actions spécifiques (menu radial, debug, etc.)

---

## 📦 Variables, Fonctions & Structures clés

> **Basé sur l’itération précédente du projet (ancienne doc Input/Controls Architecture).  
> On récupère la logique de mapping, les conventions de nommage, et la gestion des contextes.**

---

## 🔁 Pipeline de fonctionnement

1. Initialisation du mapping d’entrée au BeginPlay (PlayerController)
2. Attribution dynamique des contextes selon l’état du jeu (gameplay, UI, radial, etc.)
3. Définition des actions de base et contextuelles
4. Gestion de la priorité, des exécutions “en pause”, et des retours de focus (Game Only / Game and UI)

---

## 🗺️ Roadmap locale

- [ ] Adapter la logique Enhanced Input à la structure du nouveau template
- [ ] Uniformiser les conventions de nommage/actions dans tout le projet
- [ ] Préparer la compatibilité future avec le mobile ou d’autres devices si besoin

---

## 🔗 Liens & docs associées

- [Journal_Modifications.md]
- [Project_Architecture_Index.md]
- [UI_Architecture.md]
- [RadialMenu_Architecture.md]

---

## 🕒 Historique

- Création : 17/06/2025
- Dernière mise à jour : [JJ/MM/AAAA]

---
