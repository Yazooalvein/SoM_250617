# 📑 Index d’Architecture Technique — Shadow of Mana (ARPG / UE5.6+)

---

## 📋 Objectif

Documenter la liste exhaustive de tous les systèmes, modules et documents d’architecture du projet.  
Ce fichier sert de **table des matières centrale** pour la documentation technique, et doit être mis à jour à chaque création ou modification de document.

---

## 📁 Documents principaux

| Système / Module           | Document dédié (fichier)                | Statut           |
|----------------------------|-----------------------------------------|------------------|
| Présentation générale      | Présentation_Générale_du_Projet.md      | ✅ À jour        |
| Index architecture (ce doc)| Project_Architecture_Index.md           | ✅ À jour        |
| Journal des modifications  | Journal_Modifications_ARPG.md           | ✅ À jour        |
| Structure Content/         | Structure_Dossier_Content.md            | ✅ À jour        |

---

## 📂 Architecture par module (dossier `/Architecture`)

| Module / Système           | Fichier                                 | Statut               |
|----------------------------|-----------------------------------------|----------------------|
| UI / Interface             | UI_Architecture.md                      | 🕒 À faire / En cours|
| Stat System                | Stats_Architecture.md                   | 🕒 À faire / En cours|
| Combat System              | Combat_Architecture.md                  | 🕒 À jour            |
| Audio                      | Audio_Architecture.md                   | 🕒 À faire / En cours|
| Save System                | SaveSystem_Architecture.md              | 🕒 À faire / En cours|
| Inventory                  | Inventory_Architecture.md               | 🕒 À faire / En cours|
| Quêtes                     | Quest_Architecture.md                   | 🕒 À faire / En cours|
| Dialogue                   | Dialogue_Architecture.md                | 🕒 À faire / En cours|
| Lore                       | Lore_Architecture.md                    | 🕒 À faire / En cours|
| Radial Menu                | RadialMenu_Architecture.md              | ✅ À jour            |
| HUD Principal              | HUD_Architecture.md                     | 🕒 À faire / En cours|
| Input & Controls           | Input_Architecture.md                   | ✅ À jour            |
| Weapons System             | Weapons_System_Architecture.md           | ✅ À jour            |
| Combo System               | Combo_System_Architecture.md             | ✅ À jour            |
| Damage System              | Damage_System_Architecture.md            | ✅ À jour            |
| IA (globale)               | AI_Architecture.md                     | ✅ À jour            |
| IA Ennemis                 | Enemy_AI_Behavior.md                   | ✅ À jour            |
| ... (à compléter selon besoin) | ...                                 | ...                  |

---

## 📦 Règles de mise à jour

- **Tout ajout, modification ou suppression de fichier de documentation doit être répercuté ici.**
- **Le statut de chaque doc** doit refléter l’état réel (À jour / À faire / En cours / Obsolète…)
- **Le nom du fichier** doit être cohérent avec la convention du projet.
- **Lien croisé** possible vers chaque doc via [lien relatif] pour navigation rapide.

---

## 🧭 Historique / changelog

- **Création : 17/06/2025**
- Dernière mise à jour : 27/06/2025

---

- 20/06/2025 : Début refactorisation majeure systèmes Combo/LockOn/RadialMenu.
- 21/06/2025 : Migration Combo en Map, pipeline centralisé, debug en cours. Voir Combo System Architecture.
- 21/06/2025 : Refactorisation majeure du système de combos (modularité, fenêtre dynamique, base multi-armes prête).  
- Validation du menu radial dynamique (UI), lock-on stable.
- 24/06/2025 : Ajout Weapons_System_Architecture.md, MAJ lourde Combo_System_Architecture.md, RadialMenu_Architecture.md, journal, validation pipeline data-driven armes/menu/combo.
- 26/06/2025 : Ajout de `Damage_System_Architecture.md` : architecture complète du système de dégâts par collision, interface et dispatcher de mort.
- 27/06/2025 : Ajout de `AI_Architecture.md` (structure générale IA du projet)  
               et `Enemy_AI_Behavior.md` (logique de base IA ennemis : poursuite, aggro, retour).

---

## 📌 Note

Ce fichier est la **porte d’entrée** de toute la documentation technique.  
En cas de doute ou de réorganisation, il fait foi.

---
