# Architecture Technique — Menu Radial

---

## 📌 Objectif du module

Décrire l’architecture du système de menu radial d’armes :
- Navigation circulaire dynamique (armes, objets…)
- Gestion scalable (ajout automatique des slots selon découverte)
- Support clavier/souris & gamepad (IMC/IA)
- Sélection, validation et passage à l’équipement joueur

---

## 🧩 Composants principaux

- **WBP_RadialMenu** (UserWidget principal, logique centrale)
- **WBP_RadialSlot** (widget slot individuel, affichage de l’icône/infos)
- **BP_PlayerController** (création/affichage/fermeture radial, relais input)
- **Struct : FRadialMenuSlotData** (cf. roadmap, version actuelle : RowName, Icon, autres infos si besoin)
- **Arrays dynamiques :**
    - `SlotIcons` (`Array<Texture2D>`) — icônes pour chaque slot
    - `SlotRowNames` (`Array<Name>`) — RowName DataTable de chaque arme
- **Variables :**
    - `CurrentSelectedIndex` (`int`) — index du slot sélectionné
    - `RadialSlots` (`Array<WidgetRef>`) — refs aux widgets slots UI
    - `bIsRadialMenuOpen` (`bool`)

---

## 📦 Variables, Fonctions & Structures clés

- **Struct `FRadialMenuSlotData`** *(roadmap, à généraliser)* :
    - `RowName` (Name)
    - `Icon` (Texture2D)
    - *(option : Nom, Stat, Rareté, Locked, etc.)*

- **Fonctions principales :**
    - `OpenRadialMenu()`
    - `CloseRadialMenu()`
    - `InitializeRadialMenu(Array<Name> DiscoveredWeapons)`
    - `GenerateRadialSlots()`
    - `UpdateSelectedIndex(int)`
    - `ValidateSelectedSlot()`
    - `ResetRadialMenu()`

---

## 🔁 Pipeline de fonctionnement

1. **Ouverture (input dédié)**
    - Le PlayerController crée le widget RadialMenu et lui transmet la liste d’armes débloquées (`DiscoveredWeapons`/`SlotRowNames`), et icons associées.
    - Ajoute au viewport, passe le jeu en pause (si besoin), bascule input en mode UI.

2. **Génération dynamique des slots**
    - Boucle sur les `DiscoveredWeapons` (RowNames)
    - Pour chaque :
        - Lookup DT_Weapons → récupère Icon (et autres infos)
        - Ajoute dans `SlotIcons`/`SlotRowNames`
        - Crée le WBP_RadialSlot associé, le place radialement via RenderTranslation
    - Slots alimentés dans le même ordre que les arrays.

3. **Navigation/Highlight**
    - Input gauche/droite (stick/dpad/souris) met à jour `CurrentSelectedIndex`
    - Highlight dynamique du slot sélectionné
    - Aucune rotation de l’array : l’index fait foi

4. **Sélection/validation**
    - À l’input “Valider” (IMC/IA, universel)
        - Le widget lit : `SlotRowNames[CurrentSelectedIndex]`
        - Relaye ce RowName via le controller au BP_Character (Set ChoosenWeapon / EquipWeapon)
    - Feedback visuel sur la sélection

5. **Fermeture**
    - Suppression du widget, reset des variables, retour input “Game Only”

---

## 🛠️ Patterns & best practices

- **Full data-driven** : les slots sont générés depuis la DataTable, rien n’est hardcodé
- **Seul l’index sélectionné compte** : accès aux arrays toujours via `CurrentSelectedIndex` (jamais d’array tournant)
- **Widget autonome** : arrays de slot locaux (SlotIcons, SlotRowNames), transmis “Expose on Spawn”
- **Synchronisation dynamique** : chaque ouverture recharge la liste d’armes et les icons actuelles
- **Input universel** : tout est géré par IMC/IA (clavier, souris, manette…)
- **Séparation logique :**
    - Le radial gère l’UI/choix
    - Le personnage gère l’équipement effectif

---

## 🗺️ TODO / Roadmap

- [ ] **Généraliser struct `FRadialMenuSlotData`**
    - Ajout d’autres datas (Nom, Stat, FX, locked…)
- [ ] **Implémenter EventDispatcher propre**
    - Pour signaler au Controller/Character la sélection/fermeture (plus modulaire)
- [ ] **Ajouter la logique de “slot verrouillé” ou indispo**
    - (pour slots non débloqués, cooldown, etc)
- [ ] **Fallback slot vide**
    - Gestion visuelle (placeholder, désactivation, etc)
- [ ] **Prévoir extension pour sorts/objets/inventaire**

---

## 🕒 Historique

- Création initiale : 17/06/2025
- MAJ lourde : 24/06/2025 (pipeline data-driven, arrays dynamiques, gestion par index, synchronisation avec DT_Weapons et DiscoveredWeapons, sélection input universelle)
- Dernière mise à jour : [à compléter]

---

## **Fin du doc — relu et validé par [à compléter]**
