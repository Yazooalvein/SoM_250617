# Architecture Technique — Menu Radial

---

## 📌 Objectif du module

Décrire l’architecture du système de menu radial :
- Navigation dynamique (armes, objets, sorts…)
- Interaction manette/clavier, menu circulaire évolutif
- Intégration avec le Stat System, l’UI, le PlayerController, l’IMC

---

## 🧩 Composants principaux

- **WBP_RadialMenu** (UserWidget principal)
- **WBP_RadialSlot** (widget slot individuel)
- **BP_PlayerController** (contrôle de l’affichage, input, relais UI)
- **Canvas_RadialMenu** (container principal du menu)
- **Struct actuelle** : Array de textures (SlotIcons)
- **Struct à prévoir** : `FRadialMenuSlotData` (voir TODO)
- **Input Mapping Context (IMC_ARPG_Main)** (actions : ouverture/fermeture, rotation, sélection)

---

## 📦 Variables, Fonctions & Structures clés

### **Variables principales (extraites de la dernière version BP)**
- `bIsRadialMenuOpen` (bool) : État du menu
- `CurrentSelectedIndex` (int) : Index du slot sélectionné
- `RadialSlots` (Array) : Références slots UI
- `SlotIcons` (Array<Texture2D>) : Icônes associées aux slots (structure à enrichir)
- `RadialMenuWidgetRef` (WBP_RadialMenu) : Référence courante du widget radial

### **Fonctions principales**
- `OpenRadialMenu()`
- `CloseRadialMenu()`
- `ToggleRadialMenu()`
- `InitializeRadialMenu()`
- `GenerateRadialSlots()`
- `UpdateSelectedIndex(int)`
- `RotateRadialMenu(int)`
- `SelectCurrentSlot()`
- `ResetRadialMenu()`

---

## 🔁 Pipeline de fonctionnement

1. **Ouverture via input dédié**
   - Création du widget, ajout au viewport, passage en mode pause, gestion du focus input.
2. **Génération dynamique des slots**
   - À partir de `SlotIcons` (ou futur `FRadialMenuSlotData`), création des widgets slots et placement radial dynamique via RenderTranslation.
3. **Navigation et rotation**
   - Input IMC : gauche/droite (pad/stick), rotation du menu autour du curseur principal.
   - Mise à jour de l’index sélectionné, feedback visuel sur le slot actif.
4. **Sélection d’un slot**
   - Validation de la sélection (action contextuelle, changement d’arme, usage d’objet, etc.)
   - Relais au Controller ou au système d’action associé.
5. **Fermeture**
   - Remove from Parent du widget, reset des variables, sortie du mode pause, retour au contrôle du personnage.

---

## 🗺️ Roadmap locale / TODO

- [ ] **Remplacer l’array de textures par une struct dédiée `FRadialMenuSlotData`**
  - Gérer icône, nom, état, quantité, cooldown… par slot pour un système data-driven extensible.
- [ ] **Implémenter un dispatcher/événement Blueprint**
  - Pour permettre au widget de notifier le controller d’une sélection/fermeture, sans couplage direct (meilleure modularité).
- [ ] **Ajouter la logique de désactivation/lock de slot**
  - Pour désactiver certains slots selon le contexte (cooldown, indisponibilité, restriction gameplay).
- [ ] (Bonus) **Prévoir un fallback visuel/texte pour slot vide**
  - Message, icon placeholder ou désactivation visuelle.

---

## 🔗 Liens & docs associées

- [UI_Architecture.md]
- [Journal_Modifications_ARPG.md]
- [Project_Architecture_Index.md]
- [LockOn_Architecture.md] (interaction avec le menu radial possible à terme)
- [IMC_ARPG_Main] (mappings d’input)

---

## 🕒 Historique

- Création : 17/06/2025
- Mise à jour : 19/06/2025 (import Shadow of Mana + axes d’amélioration)

---
