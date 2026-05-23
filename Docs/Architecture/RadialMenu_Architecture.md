# Architecture Technique -- Menu Radial

---

## Objectif du module

Systeme de menu radial unifie (Armes + Magie) :
- Navigation circulaire dynamique, plateau tournant, curseur fixe a 12h
- Slow-mo a l'ouverture (Time Dilation 0.2)
- Armes : 1 radial
- Magie : 2 niveaux (Ecole -> Sort)
- Data-driven via FSoM_RadialSlotData (generique, non lie a DT_Weapons)
- Support gamepad (stick G/D = rotation, stick H/B = categorie, A = confirmer, B = retour)

---

## ETAT ACTUEL (23/05/2026)

### Radial Armes -- VALIDE PIE
- PopulateWeaponSlots : lit DiscoveredWeapons -> lookup DT_Weapons -> FSoM_RadialSlotData
- SwitchCategory branche Weapons : valide PIE
- ValidateSelectedWeapon : EquipWeapon(SlotID) -> CloseRadial
- Dette : SelectedIndex remis a 0 a chaque ouverture -> doit retourner sur ChoosenWeapon (C1-CleanupDettes)

### Radial Magie -- A IMPLEMENTER (C1-RadialMagie)
- SwitchCategory branche Magic : stub PrintVar "PASSAGE EN MAGIC" (then deconnecte -- a remplacer)
- Decisions actees (23/05/2026) :
  - Validation N2 = CastSpell direct (pas d'assignation quickslot dans le radial)
  - Source ecoles = filtrage UnlockedSpells par Category (pas de variable UnlockedSchools)
  - SelectedIndex arme = dette C1-CleanupDettes

### Ancienne architecture -- DECONNECTEE
- UI_RadialMenu + UI_RadialSlot_OLD : presents mais deconnectes depuis 12/05/2026
- A supprimer une fois C1-RadialMagie valide

---

## Composants principaux

- `ERadialMode` (enum) : Weapons / Magic (NewEnumerator0 / NewEnumerator1)
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
├── UI_RadialSlot.uasset         <- slot generique
├── UI_RadialSlot_OLD.uasset     <- ancien slot (deconnecte, a supprimer apres C1-RadialMagie)
├── UI_RadialMenu.uasset         <- ancien radial (deconnecte, a supprimer apres C1-RadialMagie)
└── UI_Radial_Main.uasset        <- radial principal actif
```

---

## SwitchCategory -- analyse T3D (21/05/2026)

Flow complet de la fonction SwitchCategory(Direction: int) :

```
Entry
  |
  v
Branch (CurrentCategory == "Weapons" via Conv_ByteToString + EqualEqual_StriStri)
  |
  |-- TRUE (on est en Weapons, on passe en Magic)
  |     SET CurrentCategory = NewEnumerator1 (Magic)
  |     --> stub MacroInstance PrintVar "PASSAGE EN MAGIC" (then deconnecte -- a remplacer)
  |
  |-- FALSE (on est en Magic, on passe en Weapons)
        SET CurrentCategory = NewEnumerator0 (Weapons)
        PopulateWeaponSlots
        SET SelectedIndex = 0  <- dette C1-CleanupDettes : doit etre index de ChoosenWeapon
        SET TargetRotation = 0
        SET CurrentRotation = 0

  Puis 2e Branch (CurrentCategory == "Weapons" apres le set)
    TRUE  -> appel PopulateWeaponSlots + reset SelectedIndex/Rotations
    FALSE -> stub PrintVar (Magic)
```

Note : la comparaison passe par Conv_ByteToString car ERadialMode est un UserDefinedEnum stocke en byte.

---

## Architecture Radial Magie (C1-RadialMagie)

```
Triangle (ouvre/ferme)
  |
  v
UI_Radial_Main
  |
  |-- SwitchCategory -> Weapons : PopulateWeaponSlots (existant)
  |                               SelectedIndex = index de ChoosenWeapon (dette C1-CleanupDettes)
  |
  └-- SwitchCategory -> Magic
        |
        v
      PopulateMagicSchools (a creer)
        Acces : BP_SoM_PlayerController -> PlayerCharacterRef -> MagicComponent -> UnlockedSpells
        Loop sur UnlockedSpells -> Extract SpellCategory -> Dedup -> MakeFSoM_RadialSlotData
        Genere slots N1 (une case = une ecole)
        SET CurrentMagicSchool = "" (reset)
        |
        v (selection d'une ecole + confirmer A / IA_UI_Radial_Validate)
      PopulateMagicSpells(SchoolID: FName) (a creer)
        Loop UnlockedSpells -> Filter sur Category == SchoolID -> Genere slots N2
        SET CurrentMagicSchool = SchoolID
        |
        v (selection d'un sort + confirmer A)
      ValidateSelectedSpell (a creer)
        Branch (CurrentMagicSchool == "") -> PopulateMagicSpells (entrer N2)
        Branch (CurrentMagicSchool != "") -> CastSpell(SlotDataList[SelectedIndex].SlotID)
          -> GetPlayerCharacter -> MagicComponent -> CastSpell(SpellID)
          -> CloseRadial

Retour B (IA_UI_Radial_Cancel) :
  Branch (CurrentMagicSchool != "") -> PopulateMagicSchools (retour N1) + SET CurrentMagicSchool = ""
  Branch (CurrentMagicSchool == "") -> CloseRadial
```

### Variables a ajouter dans UI_Radial_Main
- `CurrentMagicSchool` (FName) : "" si en N1 ou en mode Weapons, NomEcole si en N2

### Logique ValidateSelection
L'appui sur A (IA_UI_Radial_Validate) a un comportement different selon le contexte :
- Mode Weapons : ValidateSelectedWeapon (existant)
- Mode Magic + CurrentMagicSchool == "" : entrer N2 via PopulateMagicSpells
- Mode Magic + CurrentMagicSchool != "" : CastSpell + CloseRadial
Il faut donc une fonction centrale ValidateSelection qui route selon ces conditions.

### Acces MagicComponent depuis UI_Radial_Main
UI_Radial_Main -> GetOwningPlayerPawn -> Cast BP_SoM_HeroCharacter -> GET MagicComponent
OU : passer une ref MagicComponentRef dans OpenRadialMenu depuis le PC.
Option recommandee : passer la ref a l'ouverture (plus propre, pas de cast dans le widget).

### Population slots : FSoM_RadialSlotData pour la magie
- SlotID = SpellID (FName, ex : "Lumina_Heal")
- DisplayName = nom affiche (ex : "Soin")
- Icon = icone du sort depuis DT_Spells
- Category = nom de l'ecole (ex : "Lumina")
- StatA = ManaCost, StatB = Cooldown, StatC = Puissance

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
- `SetSelected(bool bSelected)` : SelectionBorder + Grayout
- `SetSlotData(FSoM_RadialSlotData)` : SET SlotData + Make Brush from Texture -> Image_Icon

---

## UI_Radial_Main -- detail

### Layout
```
Canvas Panel
└── Overlay (fullscreen)
    ├── Image_Background (noir A=0.6)
    └── SizeBox (400x400)
        └── Canvas_Radial
            ├── Text_Category   (haut : "ARMES" / "MAGIE" / "MAGIE - Lumina")
            ├── RadialContainer (Is Variable, 10x10, point d'ancrage slots)
            ├── Image_Cursor    (12h, indicateur fixe)
            └── VBox_Center
                ├── Text_ItemName
                └── Text_Description
```

### Variables cles
- `CurrentCategory` (ERadialMode)
- `SelectedIndex` (Integer) : index slot selectionne
- `SlotWidgets` (Array<UI_RadialSlot>)
- `SlotDataList` (Array<FSoM_RadialSlotData>)
- `RadialRadius` (Float, 150)
- `CurrentMagicSchool` (FName) : "" si N1 ou Weapons, NomEcole si N2 -- A AJOUTER

---

## BP_SoM_PlayerController -- Open/Close

### OpenRadialMenu
```
Create UI_Radial_Main -> SET RadialMainRef
Add to Viewport (ZOrder 99)
Set Global Time Dilation (0.2)
Set Input Mode Game And UI
SET Show Mouse Cursor = true
Remove IMC_Gameplay -> Add IMC_Radial (priority 1)  [FAIT C1-InputsUI]
[A faire C1-RadialMagie] : passer MagicComponentRef au widget via fonction Init
```

### CloseRadialMenu
```
Remove from Parent (RadialMainRef)
Set Global Time Dilation (1.0)
Set Input Mode Game Only
SET Show Mouse Cursor = false
SET RadialMainRef = null
Remove IMC_Radial -> Add IMC_Gameplay (priority 0)  [FAIT C1-InputsUI]
```

---

## Input map cible

| Input | Action |
|-------|--------|
| Hold IA_UI_Radial_Open | Ouvre radial + slow-mo |
| Stick G/D | IA_UI_Radial_Rotate : rotation plateau (selection) |
| IA_UI_Radial_ChangeCat | Categorie precedente/suivante |
| IA_UI_Radial_Validate (A/X) | Confirmer (entrer ecole N1 / caster N2 / equiper arme) |
| IA_UI_Radial_Cancel (B/Circle) | Retour (N2->N1) / fermer (N1 ou Weapons) |
| Release IA_UI_Radial_Open | Ferme + restore Time Dilation |

---

## Design decisions actees

- Curseur fixe a 12h, le plateau tourne (pas le curseur)
- Slow-mo 0.2 (pas de pause complete)
- Armes : 1 radial
- Magie : 2 radiales imbriquees (ecoles N1 -> sorts N2)
- Validation N2 = CastSpell direct (pas d'assignation dans le radial)
- Source ecoles = filtrage UnlockedSpells par Category (pas de variable UnlockedSchools separee)
- SelectedIndex arme = dette C1-CleanupDettes (retour sur ChoosenWeapon)
- StatA/B/C : Degats/Portee/Vitesse pour armes, ManaCost/Cooldown/Puissance pour magie

---

## Roadmap locale

- [x] ERadialMode + FSoM_RadialSlotData
- [x] UI_RadialSlot (SetSelected + SetSlotData)
- [x] UI_Radial_Main GenerateSlots (Cos/Sin, VALIDE PIE)
- [x] OpenRadialMenu slow-mo + CloseRadialMenu restore
- [x] Navigation stick G/D (UpdateSelection + rotation plateau lerp)
- [x] UpdateCenterInfo (Text_ItemName + Text_Description)
- [x] SwitchCategory structure (toggle ERadialMode)
- [x] PopulateWeaponSlots valide PIE
- [x] ValidateSelectedWeapon valide PIE
- [x] C1-InputsUI : switch IMC a l'open/close VALIDE PIE
- [ ] C1-RadialMagie : ajouter CurrentMagicSchool dans UI_Radial_Main
- [ ] C1-RadialMagie : PopulateMagicSchools (loop UnlockedSpells -> dedup ecoles)
- [ ] C1-RadialMagie : Cablage branche Magic SwitchCategory
- [ ] C1-RadialMagie : PopulateMagicSpells(SchoolID)
- [ ] C1-RadialMagie : ValidateSelection centralisee (Weapons / Magic N1 / Magic N2)
- [ ] C1-RadialMagie : ValidateSelectedSpell -> CastSpell + CloseRadial
- [ ] C1-RadialMagie : navigation retour B (N2->N1 / N1->fermer)
- [ ] C1-RadialMagie : passer MagicComponentRef a l'ouverture via Init
- [ ] C1-RadialMagie : Text_Category affiche "MAGIE - [NomEcole]" en N2
- [ ] C1-CleanupDettes : SelectedIndex = index ChoosenWeapon dans DiscoveredWeapons
- [ ] Supprimer ancienne logique UI_RadialMenu une fois C1-RadialMagie valide

---

## Historique

- Creation : 17/06/2025
- Refonte complete J-13 : 12/05/2026
- Nommage mis a jour : 15/05/2026 (J-Renommage)
- MAJ architecture Magie + analyse SwitchCategory T3D : 21/05/2026
- MAJ decisions C1-RadialMagie actees : 23/05/2026
