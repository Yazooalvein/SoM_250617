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

## ETAT ACTUEL (21/05/2026)

### Radial Armes -- VALIDE PIE
- PopulateWeaponSlots : lit DiscoveredWeapons -> lookup DT_Weapons -> FSoM_RadialSlotData
- SwitchCategory branche Weapons : valide PIE
- ValidateSelectedWeapon : EquipWeapon(SlotID) -> CloseRadial
- Bug connu : SelectedIndex remis a 0 a chaque ouverture -> doit retourner sur ChoosenWeapon (C1-RadialMagie)

### Radial Magie -- EN COURS (C1-RadialMagie)
- SwitchCategory branche Magic : stub PrintVar "PASSAGE EN MAGIC" (then deconnecte)
- Architecture 2 niveaux a implementer : ecoles N1 -> sorts N2
- Dependance : C1-InputsUI (IMC_UI dedie) doit etre fait avant

### Ancienne architecture -- DECONNECTEE
- UI_RadialMenu + UI_RadialSlot_OLD : presents mais deconnectes depuis 12/05/2026
- Peuvent etre supprimes une fois C1-RadialMagie valide

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
  |     --> stub MacroInstance PrintVar "PASSAGE EN MAGIC" (then deconnecte -- a implementer)
  |
  |-- FALSE (on est en Magic, on passe en Weapons)
        SET CurrentCategory = NewEnumerator0 (Weapons)
        PopulateWeaponSlots
        SET SelectedIndex = 0  <- a corriger : doit etre index de ChoosenWeapon
        SET TargetRotation = 0
        SET CurrentRotation = 0

  Puis 2e Branch (CurrentCategory == "Weapons" apres le set)
    TRUE  -> appel PopulateWeaponSlots + reset SelectedIndex/Rotations
    FALSE -> stub PrintVar (Magic)
```

Note : la comparaison passe par Conv_ByteToString car ERadialMode est un UserDefinedEnum stocke en byte.

---

## Architecture Radial Magie (cible C1-RadialMagie)

```
Triangle (ouvre/ferme)
  |
  v
UI_Radial_Main
  |
  |-- SwitchCategory -> Weapons : PopulateWeaponSlots (existant)
  |                               SelectedIndex = index de ChoosenWeapon (a corriger)
  |
  └-- SwitchCategory -> Magic
        |
        v
      PopulateMagicSchools (a creer)
        Lit UnlockedSpells depuis BP_MagicComponent
        Groupe par ecole (Lumina, Ondine, Ombre, Athanor, Sylphide, Gnome, Salamandre...)
        Genere slots N1 (une case = une ecole)
        |
        v (selection d'une ecole + confirmer A)
      PopulateMagicSpells(SchoolID) (a creer)
        Lit sorts de l'ecole selectionnee
        Genere slots N2 (Attack, Buff, Debuff, Soin pour cette ecole)
        |
        v (selection d'un sort + confirmer A)
      ValidateSelectedSpell
        -> CastSpell (si acces rapide)
        -> Ou assignation quickslot (si mode assignation)

Retour B : N2 -> N1, N1 -> fermer
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
            ├── Text_Category   (haut : "ARMES" / "MAGIE")
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
- `CurrentMagicSchool` (FName) : ecole selectionnee en N1, vide si N1 pas encore valide

---

## BP_SoM_PlayerController -- Open/Close

### OpenRadialMenu
```
Create UI_Radial_Main -> SET RadialMainRef
Add to Viewport (ZOrder 99)
Set Global Time Dilation (0.2)
Set Input Mode Game And UI
SET Show Mouse Cursor = true
[A faire C1-InputsUI] : Remove IMC_Prototype, Add IMC_UI
```

### CloseRadialMenu
```
Remove from Parent (RadialMainRef)
Set Global Time Dilation (1.0)
Set Input Mode Game Only
SET Show Mouse Cursor = false
SET RadialMainRef = null
[A faire C1-InputsUI] : Remove IMC_UI, Add IMC_Prototype
```

---

## Input map cible

| Input | Action |
|-------|--------|
| Hold IA_RadialMenu | Ouvre radial + slow-mo |
| Stick G/D | Rotation plateau (selection) |
| Stick Haut | Categorie precedente |
| Stick Bas | Categorie suivante |
| Bouton A/X | Confirmer (entrer ecole N1 / caster ou assigner N2) |
| Bouton B/Circle | Retour (N2->N1) / fermer (N1) |
| Release IA_RadialMenu | Ferme + restore Time Dilation |

---

## Design decisions actees

- Curseur fixe a 12h, le plateau tourne (pas le curseur)
- Slow-mo 0.2 (pas de pause complete)
- Armes : 1 radial
- Magie : 2 radiales imbriquees (ecoles -> sorts)
- SelectedIndex doit retourner sur l'arme equipee a l'ouverture (pas 0)
- Feedback visuel : pas de hit flash ennemi (abandonne) -- screen shake suffit
- StatA/B/C generiques : Degats/Portee/Vitesse pour armes, ManaCost/Cooldown/Puissance pour magie

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
- [ ] C1-InputsUI : switch IMC a l'open/close (prerequis)
- [ ] C1-RadialMagie : PopulateMagicSchools + PopulateMagicSpells + ValidateSelectedSpell
- [ ] C1-RadialMagie : fix SelectedIndex = index ChoosenWeapon dans DiscoveredWeapons
- [ ] C1-RadialMagie : navigation retour B (N2->N1)
- [ ] Supprimer ancienne logique UI_RadialMenu une fois C1-RadialMagie valide

---

## Historique

- Creation : 17/06/2025
- Refonte complete J-13 : 12/05/2026
- Nommage mis a jour : 15/05/2026 (J-Renommage)
- MAJ architecture Magie + analyse SwitchCategory T3D : 21/05/2026
