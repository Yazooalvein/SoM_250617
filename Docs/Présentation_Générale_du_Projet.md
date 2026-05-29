# Shadow of Mana — ARPG Blueprint Only (UE 5.7.4)

---

## 🎮 Présentation Générale

**Shadow of Mana** est un Action-RPG 3D développé sous **Unreal Engine 5.7.4** (template Third Person — Plateforming), 100% **Blueprint Only**.

Le projet est une lettre d'amour aux classiques du genre : **Secret of Mana** (Seiken Densetsu 2 & 3), **Trials of Mana**, **Vision of Mana** pour l'univers et le cast, et **Dark Souls** pour la philosophie de combat — exigeant, lisible, chaque action a un coût.

---

## 🎮 General Overview *(EN)*

**Shadow of Mana** is a 3D Action-RPG built with **Unreal Engine 5.7.4** (Third Person Platforming template), 100% **Blueprint Only**.

The project is a love letter to genre classics: **Secret of Mana** (Seiken Densetsu 2 & 3), **Trials of Mana**, and **Vision of Mana** for the world and cast, and **Dark Souls** for the combat philosophy — demanding, readable, every action has a cost.

---

## 🌌 Histoire (pitch sans spoilers)

L'**Arbre Mana** a été détruit lors d'une Grande Guerre magique. Le monde en porte les cicatrices : zones corrompues, faune et flore altérées, équilibres élémentaires brisés. Les **esprits élémentaires** — les Déités — survivent, affaiblis, cherchant leurs représentants humains.

Le héros, ancien soldat, est entraîné malgré lui dans une quête qui le dépasse. Accompagné d'un groupe de compagnons aux origines et aux races variées, il devra parcourir un monde en ruine, renouer les liens entre les Déités et leurs représentants, et faire face à une vérité bien plus sombre que prévu sur les origines du cataclysme.

Le jeu se déroule sur **4 actes**. Chaque région libérée se transforme visuellement. Chaque choix narratif a des conséquences durables.

---

## 🌌 Story (spoiler-free pitch) *(EN)*

The **Mana Tree** was destroyed in a great magical war. The world bears its scars: corrupted regions, altered flora and fauna, shattered elemental balance. The **elemental spirits** — the Deities — survive, weakened, seeking their human vessels.

A former soldier is reluctantly drawn into a quest far beyond his understanding. Alongside a group of companions from diverse races and origins, he must cross a ruined world, restore the bonds between the Deities and their representatives, and confront a truth far darker than expected about the origins of the cataclysm.

The game unfolds across **4 acts**. Every region freed transforms visually. Every narrative choice has lasting consequences.

---

## 👥 Cast (aperçu)

Un groupe de personnages aux races distinctes — Humain, Humaine Céleste, Beastman Félin, Nains, DragonFolk, Beastman Loup, Sproutling — chacun lié à une Déité élémentaire parmi les huit que compte le monde de Mana.

Huit Déités : **Lumina, Luna, Ombre, Sylphide, Gnome, Salamandre, Ondine, Dryade.**

---

## 👥 Cast (overview) *(EN)*

A group of characters from distinct races — Human, Celestial Human, Feline Beastman, Dwarves, DragonFolk, Wolf Beastman, Sproutling — each bound to one of the eight elemental Deities of the Mana world.

Eight Deities: **Lumina, Luna, Ombre, Sylphide, Gnome, Salamandre, Ondine, Dryade.**

---

## ⚙️ Systèmes clés

**Combat**
- Système de combos par arme (TMap de steps, progression par niveau)
- Lock-on, esquive, stamina — philosophie Dark Souls
- Radial menu en slow-motion pour changer d'arme ou lancer un sort

**Magie**
- 8 écoles élémentaires, déblocage progressif lié à la narration
- Arbre de progression par déité
- Système de **Corruption Magique** : utiliser la magie corrompt le héros — risque/récompense

**Armes**
- Plusieurs types (Épée, Greatsword, Arc, Lance, Hache...)
- Évolution par étapes via la forge — matériaux + jalons narratifs requis
- Inspiré du système d'armes Seiken : chaque arme a son moveset propre

**Progression**
- Système de stats hybride : montée de niveau globale + progression par usage (armes, magie)
- Double monnaie : Essence de Mana (perdue à la mort, récupérable) + Pièces d'Or (permanentes)
- Équipement 3 slots, consommables Seiken

**Hub & Monde**
- Ville centrale qui se reconstruit progressivement au fil des avancées narratives
- PNJs rencontrés en route reviennent peupler la ville
- Fontaines de Fée : mécanisme de repos (inspiré des feux Dark Souls), intégré au lore

---

## ⚙️ Core Systems *(EN)*

**Combat**
- Per-weapon combo system (step TMap, level-based progression)
- Lock-on, dodge, stamina — Dark Souls philosophy
- Slow-motion radial menu to switch weapons or cast spells mid-fight

**Magic**
- 8 elemental schools, progressively unlocked through the narrative
- Per-deity talent tree
- **Magic Corruption** system: using magic corrupts the hero — risk/reward mechanic

**Weapons**
- Multiple types (Sword, Greatsword, Bow, Lance, Axe...)
- Staged evolution through the forge — materials + narrative milestones required
- Inspired by the Seiken weapon system: each weapon has its own moveset

**Progression**
- Hybrid stat system: global level-up + usage-based progression (weapons, magic)
- Dual currency: Mana Essence (lost on death, recoverable) + Gold Pieces (permanent)
- 3 equipment slots, Seiken-style consumables

**Hub & World**
- Central town that rebuilds progressively as the story advances
- NPCs met along the way return to populate the hub
- Fairy Fountains: rest mechanic (inspired by Dark Souls bonfires), woven into the lore

---

## 🗂️ Structure du dossier `Content/` (schéma simplifié)

```
Content/
├── Core/        # BP parents, GameMode, GameInstance, PlayerController
├── Systems/     # Combat, Stats, Inventory, LockOn, Save, Quest, Dialogue, Audio
├── UI/          # Widgets, HUD, RadialMenu, etc.
├── Data/        # DataTables, DataAssets (armes, stats, sorts, drops...)
├── Characters/  # Héros, Ennemis, PNJ (BPs, Meshes, Animations)
├── Audio/       # Cues, Mixes, Musiques, SFX
├── Weapons/     # Blueprints, Data, Meshes
├── Levels/      # Maps, Prototypage
├── Magic/       # FX, sorts, Data
└── Dev/         # Sandbox, prototypes, expérimentations
```

---

## 🗂️ `Content/` Folder Structure (simplified) *(EN)*

```
Content/
├── Core/        # Parent BPs, GameMode, GameInstance, PlayerController
├── Systems/     # Combat, Stats, Inventory, LockOn, Save, Quest, Dialogue, Audio
├── UI/          # Widgets, HUD, RadialMenu, etc.
├── Data/        # DataTables, DataAssets (weapons, stats, spells, drops...)
├── Characters/  # Hero, Enemies, NPCs (BPs, Meshes, Animations)
├── Audio/       # Cues, Mixes, Music, SFX
├── Weapons/     # Blueprints, Data, Meshes
├── Levels/      # Maps, Prototyping
├── Magic/       # FX, spells, Data
└── Dev/         # Sandbox, prototypes, experiments
```

---

## 🛠️ Stack technique

- **Blueprint Only** (aucune classe C++)
- **Unreal Engine 5.7.4** — template Plateforming (Third Person variant)
- **UnrealClaude v1.4.5** : plugin IA intégré à l'éditeur (discovery & audit Blueprint via MCP)
- Versioning : **Git + LFS** pour les assets volumineux
- Documentation centralisée dans `/Docs` et `/Docs/Architecture`
- Journal des modifications et roadmap maintenus à chaque session

---

## 🛠️ Technical Stack *(EN)*

- **Blueprint Only** (no C++ classes)
- **Unreal Engine 5.7.4** — Platforming template (Third Person variant)
- **UnrealClaude v1.4.5**: AI plugin embedded in the editor (Blueprint discovery & audit via MCP)
- Versioning: **Git + LFS** for large assets
- Documentation centralized in `/Docs` and `/Docs/Architecture`
- Change log and roadmap maintained after every session

---

## 📋 Conventions globales

- **Nommage** : `BP_` Blueprints, `UI_` Widgets, `F_`/`E_` Structs/Enums, camelCase variables
- **Architecture** : chaque système a sa fiche dans `Docs/Architecture/`
- **Commits** : format `type(som): description` — référence au module, date
- **Prototypes** : isolés dans `/Dev` pour ne pas polluer la structure principale

---

## 📋 Global Conventions *(EN)*

- **Naming**: `BP_` Blueprints, `UI_` Widgets, `F_`/`E_` Structs/Enums, camelCase variables
- **Architecture**: every system has its own doc in `Docs/Architecture/`
- **Commits**: format `type(som): description` — module reference, date
- **Prototypes**: isolated in `/Dev` to keep the main structure clean

---

## 👤 Crédits

- **Lead Developer** : YazooAlvein
- **Assistant IA architecture & support** : projet initié avec ChatGPT (OpenAI), repris et développé avec Claude (Anthropic)
- **Projet personnel** — prototypage & expérience de développement solo

---

## 👤 Credits *(EN)*

- **Lead Developer**: YazooAlvein
- **AI architecture & support assistant**: project started with ChatGPT (OpenAI), continued and developed with Claude (Anthropic)
- **Personal project** — solo development & prototyping experience

---

## 📁 Documentation

| Document | Contenu |
|----------|---------|
| `CLAUDE.md` | Contexte IA, architecture clé, jalons, règles |
| `Docs/Roadmap_Gameplay.md` | Planification complète par couches |
| `Docs/Journal_Modifications.md` | Historique de toutes les sessions |
| `Docs/Lore_ShadowOfMana.md` | Lore, cast, structure narrative |
| `Docs/Project_Architecture_Index.md` | Index de toute la documentation technique |
| `Docs/Architecture/` | Fiches système détaillées |

---

## 📁 Documentation *(EN)*

| Document | Content |
|----------|---------|
| `CLAUDE.md` | AI context, key architecture, milestones, rules |
| `Docs/Roadmap_Gameplay.md` | Full layered development plan |
| `Docs/Journal_Modifications.md` | Complete session history |
| `Docs/Lore_ShadowOfMana.md` | Lore, cast, narrative structure |
| `Docs/Project_Architecture_Index.md` | Index of all technical documentation |
| `Docs/Architecture/` | Detailed system docs |

---

> Création : 17/06/2025
> Dernière mise à jour : 29/05/2026
