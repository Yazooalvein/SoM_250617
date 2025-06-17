# Shadow of Mana — ARPG Blueprint Only (UE 5.6+)

---

## 🎮 Présentation Générale

**Shadow of Mana** est un Action-RPG 3D développé sous **Unreal Engine 5.6** (template Third Person — Plateforming), 100% **Blueprint Only**.  
Le projet est inspiré de jeux tels que **Secret of Mana** (Seiken Densetsu) et **Dark Souls**, avec une forte composante action, une structure modulaire, et une architecture documentaire complète.

---

## 🌌 Histoire Macro (Pitch rapide)

Dans un monde fracturé par la destruction de l’Arbre Mana, le héros et ses compagnons cherchent à rétablir l’équilibre des éléments et percer le secret de la grande guerre magique.  
Au fil d’une aventure mêlant action, progression, exploration et narration, le joueur incarne des personnages uniques, chacun lié à un élément et à une histoire singulière.

---

## 🗂️ Structure du dossier `Content/` (schéma simplifié)

Content/
├── Core/ # BP parents, GameMode, GameInstance, PlayerController
├── Systems/ # Combat, Stats, Inventory, LockOn, Save, Quest, Dialogue, Audio
├── UI/ # Widgets, HUD, RadialMenu, Debug, LockOnIndicator, etc.
├── Data/ # DataTables, DataAssets (objets, stats, quêtes, dialogues…)
├── Characters/ # Joueurs, Ennemis, PNJ (BPs, Meshes, Animations)
├── Audio/ # Cues, Mixes, Musiques, SFX, VO
├── Weapons/ # Blueprints, Data, Meshes
├── Levels/ # Maps, Prototypage
├── Magic/ # FX, sorts, Data
├── Dev/ # Sandbox, prototypes, debug, expérimentations

yaml
Copier
Modifier

> **Voir le fichier `Structure_Dossier_Content.md` pour l’arborescence complète et commentée.**

---

## ⚙️ Stack technique

- **Blueprint Only** (aucune classe C++)
- Basé sur le **template Plateforming** UE 5.6 (Third Person variant)
- Systèmes modulaires : Stat System, Combat, Menu Radial, Lock-On, UI, Save, etc.
- Versioning & suivi : **Git** (avec LFS pour les assets volumineux)
- Documentation centralisée dans `/Docs` et `/Architecture`
- Roadmap évolutive et journal des modifications associés à chaque milestone Git

---

## 📋 Règles & conventions globales

- **Nommage Blueprint** : BP_ pour Blueprints, UI_ pour Widgets, F_/E_ pour Structs/Enums, camelCase pour variables
- **Documentation** : chaque système possède sa fiche d’architecture dans `/Architecture`
- **Commits Git** : message structuré, référence au module impacté, date
- **Sandbox/Dev** : tout prototype temporaire est isolé dans `/Dev` pour éviter la pollution du projet

---

## 🚀 Roadmap Macro

- Mise en place du Stat System (out of the box, scalable, modulaire)
- Intégration Combat System (combo, lock-on, esquive, gestion stamina)
- Déploiement du Menu Radial, UI et Debug
- Extension Inventaire, Quêtes, Sauvegarde, Lore, Audio, etc.

---

## 👤 Crédit / Contributeur

- **Développeur principal** : [Ton Nom/Pseudo]
- **Assistant architecture & support** : ChatGPT (OpenAI)
- **Projet privé / prototypage / expérience personnelle**

---

## 📁 Index documentaire

Voir : `Project_Architecture_Index.md` pour la liste exhaustive de la documentation technique.

---

## 📝 Notes complémentaires

- Toutes les docs et schémas sont en français.
- Ce fichier fait foi pour la présentation générale du projet et sert de README principal pour le repo Git.

---
> Création : [17/06/2025]
> Dernière mise à jour : [JJ/MM/AAAA]