# Architecture Technique -- Menu Radial

---

## Objectif du module

Systeme de menu radial unifie (Armes + Magie) :
- Navigation circulaire dynamique, plateau tournant, curseur fixe a 12h
- Slow-mo a l'ouverture (Time Dilation 0.2)
- 2 niveaux pour la magie : Divinite -> Sort
- Data-driven via FSoM_RadialSlotData (generique, non lie a DT_Weapons)
- Support gamepad (stick G/D = rotation, stick H/B = categorie, A = confirmer, B = retour)

---

## ETAT ACTUEL (12/05/2026)

### Ancienne architecture (conservee, deconnectee)
L'ancienne logique basee sur UI_RadialMenu + UI_RadialSlot_OLD est toujours presente
dans les fonctions OpenRadialMenu et CloseRadialMenu de BP_SoM_PlayerController,
mais elle est DECONNECTEE de l'exec chain depuis le 12/05/2026.
Elle peut etre supprimee une fois la nouvelle architecture completement validee.
- UI_RadialMenu : Content/UI/Widgets/RadialMenu/UI_RadialMenu (non utilise)
- UI_RadialSlot_OLD : Content/UI/Widgets/RadialMenu/UI_RadialSlot_OLD (non utilise)

### Nouvelle architecture (WIP J-13)
- UI_Radial_Main : VALIDE PIE (4 slots en cercle, slow-mo)
- Navigation, categories, confirmation : EN COURS

---

## Composants principaux

- `ERadialMode` (enum) : Weapons / Magic
- `FSoM_RadialSlotData` (struct) : SlotID, DisplayName, Description, Icon, Category, StatA/B/C
- `UI_RadialSlot` (widget 80x80) : slot generique avec SetSelected + SetSlotData
- `UI_Radial_Main` (widget principal) : generation Cos/Sin, navigation, categories
- `BP_SoM_PlayerController` : Open/Close + Time Dilation

---

## Assets et chemins

```
Content/UI/Widgets/RadialMenu/
├── ERadialMode.uasset
├── FSoM_RadialSlotData.uasset
├── UI_RadialSlot.uasset         <- nouveau slot generique
├── UI_RadialSlot_OLD.uasset     <- ancien slot (conserve, non utilise)
├── UI_RadialMenu.uasset         <- ancien radial (conserve, non utilise)
└── UI_Radial_Main.uasset        <- nouveau radial principal
```

---

## UI_RadialSlot -- detail

### Layout (80x80)
```
SizeBox (80x80)
└── Overlay
    ├── Image_Background   (noir A=0.7)
    ├── Image_Icon         (Is Variable, Texture2D via SetSlotData)
    ├── Image_SelectionBorder (or R=1/G=0.8/B=0, Draw As Border, Hidden par defaut)
    └── Image_Grayout      (noir A=0.5, Visible par defaut)
```

### Fonctions
- `SetSelected(bool bSelected)` :
  - True : SelectionBorder = Visible, Grayout = Hidden
  - False : SelectionBorder = Hidden, Grayout = Visible
- `SetSlotData(FSoM_RadialSlotData)` :
  - SET SlotData (variable locale)
  - Make Brush from Texture (Icon) -> Set Brush (Image_Icon)

### Variables
- `SlotData` (FSoM_RadialSlotData) : donnees du slot stockees

---

## UI_Radial_Main -- detail

### Layout
```
Canvas Panel
└── Overlay (fullscreen)
    ├── Image_Background (noir A=0.6, Fill)
    └── SizeBox (400x400, Center/Center)
        └── Canvas_Radial (Fill/Fill)
            ├── Text_Category   (haut, label "ARMES" / "MAGIE")
            ├── RadialContainer (Is Variable, ancre 0.5/0.5, 10x10, point d'ancrage slots)
            ├── Image_Cursor    (12h, indicateur fixe)
            └── VBox_Center     (centre, nom + description item selectionne)
                ├── Text_ItemName
                └── Text_Description
```

### Variables
- `CurrentCategory` (ERadialMode) : categorie active
- `SelectedIndex` (Integer) : index slot selectionne
- `SlotWidgets` (Array<UI_RadialSlot>) : refs aux slots crees
- `SlotDataList` (Array<FSoM_RadialSlotData>) : donnees des slots
- `RadialRadius` (Float, default 150) : rayon du cercle
- `RadialContainer` (Is Variable) : canvas panel point d'ancrage

### GenerateSlots()
```
Clear Children (RadialContainer)
Clear (SlotWidgets)
ForEach SlotDataList :
  Create UI_RadialSlot Widget
  SET NewSlot = Return Value
  SetSlotData(Array Element)
  AngleDeg = Index * 360 / Length(SlotDataList)
  AdjustedAngle = AngleDeg - 90  <- index 0 a 12h
  AngleRad = DegreesToRadians(AdjustedAngle)
  PosX = Cos(AngleRad) * RadialRadius
  PosY = Sin(AngleRad) * RadialRadius
  Add Child to Canvas (RadialContainer, NewSlot)
    -> Set Position (PosX, PosY)
    -> Set Alignment (0.5, 0.5)
  ADD SlotWidgets (NewSlot)
```

### Event Construct (test)
- 4 slots hardcodes (Sword, 2hSword, Axe, 2hAxe) -> SET SlotDataList -> GenerateSlots

### A implementer (J-13 suite)
- UpdateSelection(int delta) : SelectedIndex +/- 1, SetSelected sur tous les slots
- UpdateCenterInfo() : Text_ItemName + Text_Description depuis SlotData[SelectedIndex]
- Changement categorie (stick Haut/Bas) : CurrentCategory toggle + regenerer SlotDataList
- Confirmation (bouton A) : niveau 1 magie = entrer divinite, niveau 2 = caster
- Retour (bouton B) : niveau 2 -> niveau 1, ou fermer

---

## BP_SoM_PlayerController -- OpenRadialMenu

```
Create UI_Radial_Main -> SET RadialMainRef
Add to Viewport (ZOrder 99)
Set Global Time Dilation (0.2)
Set Input Mode Game And UI (focus = RadialMainRef, PlayerController = Self)
SET Show Mouse Cursor = true

ANCIENNE LOGIQUE DECONNECTEE (toujours presente dans la fonction) :
- Clear SlotRowNames + RadialNumberObject
- ForEach DiscoveredWeapons -> GetDataTableRow DT_Weapons -> Build SlotRowNames/SlotIcons
- Create UI_RadialMenu -> SET RadialMenuRef -> InitializeRadialMenu
- Set Game Paused = true
```

## BP_SoM_PlayerController -- CloseRadialMenu

```
Remove from Parent (RadialMainRef)
Set Global Time Dilation (1.0)
Set Input Mode Game Only (Self)
SET Show Mouse Cursor = false
SET RadialMainRef = null

ANCIENNE LOGIQUE DECONNECTEE (toujours presente dans la fonction) :
- ValidateSelectedWeapon -> GetDataTableRow DT_Weapons -> EquipWeapon
- RemoveFromParent (RadialMenuRef)
- Set Game Paused = false
```

---

## Input map cible

| Input | Action |
|-------|--------|
| Hold IA_RadialMenu | Ouvre radial + slow-mo |
| Stick G/D | Rotation plateau (selection) |
| Stick Haut | Categorie precedente |
| Stick Bas | Categorie suivante |
| Bouton A/X | Confirmer (entrer divinite niv1 / caster niv2) |
| Bouton B/Circle | Retour / fermer |
| Release IA_RadialMenu | Ferme + restore Time Dilation |

---

## Design decisions actees

- Curseur fixe a 12h, le plateau tourne (pas le curseur)
- Slow-mo 0.2 (pas de pause complete) : pression maintenue en combat
- QuickslotBar 3 slots (Haut/Gauche/Droite gamepad) : assignation depuis menu general uniquement
- Slots non selectionnes : opacity 60%, selectionne : animation respiration + bordure or
- Label categorie en haut, info item au centre (nom + description + StatA/B/C)
- StatA/B/C generiques : Degats/Portee/Vitesse pour armes, ManaCost/Cooldown/Puissance pour magie

---

## Roadmap locale

- [x] ERadialMode + FSoM_RadialSlotData
- [x] UI_RadialSlot (SetSelected + SetSlotData)
- [x] UI_Radial_Main GenerateSlots (Cos/Sin, VALIDE PIE)
- [x] OpenRadialMenu slow-mo + CloseRadialMenu Time Dilation restore
- [ ] Navigation stick G/D (UpdateSelection + rotation plateau lerp)
- [ ] UpdateCenterInfo (Text_ItemName + Text_Description)
- [ ] Changement categorie stick Haut/Bas + animation transition
- [ ] Confirmation A / Retour B
- [ ] Alimentation depuis DT_Weapons (Armes) et BP_MagicComponent (Magie)
- [ ] UI_QuickslotBar (3 slots HUD)
- [ ] Supprimer ancienne logique UI_RadialMenu une fois validation complete

---

## Historique

- Creation : 17/06/2025
- Refonte complete J-13 : 12/05/2026
- Nommage mis à jour : 15/05/2026 (J-Renommage)
