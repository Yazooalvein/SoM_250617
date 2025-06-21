# Architecture Technique — UI / Interface

---

## 📌 Objectif du module

Décrire l’architecture complète de l’interface utilisateur du projet :  
- HUD principal  
- Widgets contextuels (RadialMenu, Debug, LockOn, Dialogue, etc.)  
- Pipeline de binding avec le Stat System et autres composants gameplay

---

## 🧩 Composants principaux

- Widgets principaux :  
    - UI_HUD_Main  
    - UI_RadialMenu  
    - UI_DebugWidget  
    - UI_LockOnIndicator  
    - UI_InventoryMenu  
    - UI_DialogueBox  
    - (etc.)
- BP_PlayerController (gestion affichage/masquage, input UI/Game)
- BP_AttributeSet_Base (pour pipeline stats → UI)
- EventDispatchers (pour synchro avec gameplay/stat system)

---

## 📦 Variables & Fonctions clés

> **Basé sur l’itération précédente du projet (voir ancienne doc “UI Architecture”).  
> Les méthodes, noms de variables/fonctions, et conventions seront récupérés et adaptés au nouveau template.**

---

## 🔁 Pipeline de fonctionnement

- Création des widgets au BeginPlay ou sur événement
- Passage des références nécessaires via “Expose on Spawn”
- Binding dynamique à la référence (ex : AttributeSetRef)
- Synchro des affichages en temps réel via EventDispatcher ou binding direct

---

## 🗺️ Roadmap locale

- [ ] Réimplémenter chaque widget clé à partir de l’ancienne structure
- [ ] Adapter les méthodes d’affichage/synchro aux nouveaux composants du template UE5.6
- [ ] Refactor des logiques d’input UI/Game pour tirer parti du nouvel Enhanced Input

---

## TODO / Roadmap UI — Menu Radial

- [ ] Remplacer l’array de textures par une struct dédiée pour chaque slot (data-driven, extensible).
- [ ] Implémenter un dispatcher (event) pour la sélection de slot, décorrélé de la logique controller.
- [ ] Ajouter une logique de désactivation/lock de slot (pour cooldown, indisponibilité, etc.), réutilisable pour d’autres menus radiaux.
- [ ] Finaliser la gestion “anti-spin” pour les icônes (correctif à appliquer à chaque update de slot, pas juste à l’initialisation).

---

## 🔗 Liens & docs associées

- [Journal_Modifications.md]
- [Project_Architecture_Index.md]
- [Présentation_Générale_du_Projet.md]
- [Stats_Architecture.md]
- [RadialMenu_Architecture.md]
- [HUD_Architecture.md]

---

## 🕒 Historique

- Création : 17/06/2025
- Dernière mise à jour : [JJ/MM/AAAA]

---
