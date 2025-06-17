# Architecture Technique — HUD Principal

---

## 📌 Objectif du module

Définir la structure et les règles du HUD principal en jeu :  
- Jauges (vie, stamina, mana), XP, consommables rapides
- Affichage d’armes/sorts actifs, portrait, feedback de stat en temps réel
- Liaison 100% dynamique avec le Stat System

---

## 🧩 Composants principaux

- UI_HUD_Main (widget central)
- BP_PlayerController (instancie/retire le HUD)
- BP_AttributeSet_Base (source unique des stats)
- Widgets contextuels (pour feedback buff/debuff, quick items, etc.)

---

## 📦 Variables, Fonctions & Structures clés

> **Basé sur l’itération précédente du projet (voir ancienne doc HUD/UI).  
> Les conventions, pipelines, noms de variables, fonctions de binding, gestion “Expose on Spawn”, etc., sont récupérés/adaptés ici.**

---

## 🔁 Pipeline de fonctionnement

1. Création dynamique du HUD au BeginPlay via le PlayerController
2. Passage de la référence AttributeSetRef au widget (Expose on Spawn)
3. Binding de toutes les barres et textes UI sur les variables du Stat System
4. Feedback en temps réel via EventDispatcher ou binding direct

---

## 🗺️ Roadmap locale

- [ ] Réintégrer le pipeline d’initialisation HUD du précédent projet
- [ ] Adapter à la structure UI et stat du template UE5.6+
- [ ] Ajouter les modules contextuels (buffs, mini-map, etc.) selon besoin

---

## 🔗 Liens & docs associées

- [Stats_Architecture.md]
- [UI_Architecture.md]
- [Journal_Modifications.md]
- [Project_Architecture_Index.md]

---

## 🕒 Historique

- Création : 17/06/2025
- Dernière mise à jour : [JJ/MM/AAAA]

---
