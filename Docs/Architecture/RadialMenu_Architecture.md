# Architecture Technique -- Menu Radial

---

## Objectif du module

Systeme de menu radial unifie (Armes + Magie) :
- Navigation circulaire dynamique, plateau tournant, curseur fixe a 12h
- Slow-mo a l'ouverture (Time Dilation 0.2)
- Armes : 1 radial
- Magie : 2 niveaux (Ecole/Deity -> Sort/Spell)
- Data-driven via FSoM_RadialSlotData (generique, non lie a DT_Weapons)
- Support gamepad (stick G/D = rotation, ChangeCat = switch categorie, A = confirmer, B = retour)

---

## ETAT ACTUEL (25/05/2026) -- VALIDE PIE

### Radial Armes -- VALIDE PIE
- PopulateWeaponSlots : lit DiscoveredWeapons -> lookup DT_Weapons -> FSoM_RadialSlotData
- SwitchCategory : toggle Weapons <-> Deity
- ValidateSelectedWeapon : EquipWeapon(SlotID) -> CloseRadial
- Dette : SelectedIndex remis a 0 a chaque ouverture -> doit retourner sur ChoosenWeapon (C1-CleanupDettes)

### Radial Magie -- VALIDE PIE (C1-RadialMagie complete 25/05/2026)
- N1 (Deity) : PopulateMagicSchools -- loop UnlockedSpells -> slots par ecole
- N2 (Spell) : PopulateMagicSpells(SchoolID) -- loop SpellIDs de la deity selectionnee
- ValidateRadial (fonction dediee sur PC) : route selon CurrentCategory
  - Weapons -> ValidateSelectedWeapon
  - Deity -> capture TempSchoolID -> SET CurrentCategory=Spell -> resets -> PopulateMagicSpells(TempSchoolID)
  - Spell -> capture TempSpellID -> CastSpell(TempSpellID) -> CloseRadial
- SwitchCategory 3 branches : Weapons->Deity, Deity->Weapons, Spell->Deity
- Cancel B : Spell->Deity (PopulateMagicSchools) / Deity->CloseRadial
- Rotation slots fonctionnelle en Weapons, Deity et Spell

### Dettes restantes (non bloquantes)
- Text_Category : "MAGIE" en N1, "MAGIE - [NomEcole]" en N2 (pas implemente)
- Icones deites/sorts : placeholder null -> ART-MagicIcons
- SelectedIndex radial : retour sur ChoosenWeapon -> C1-CleanupDettes

### Ancienne architecture -- DECONNECTEE
- UI_RadialMenu + UI_RadialSlot_OLD : presents mais deconnectes depuis 12/05/2026
- A supprimer une fois C1-RadialMagie valide (maintenant fait)

---

## Composants principaux

- `ERadialMode` (enum) : Weapons / Deity / Spell (NewEnumerator0 / NewEnumerator1 / NewEnumerator2)
- `FSoM_RadialSlotData` (struct) : SlotID, DisplayName, Description, Icon, Category, StatA/B/C
- `UI_RadialSlot` (widget 80x80) : slot generique avec SetSelected + SetSlotData
- `UI_Radial_Main` (widget principal) : generation Cos/Sin, navigation, categories
- `BP_SoM_PlayerController` : Open/Close + Time Dilation + ValidateRadial

---

## Assets et chemins

```
Content/UI/Widgets/RadialMenu/
├── ERadialMode.uasset                <- 3 valeurs : Weapons / Deity / Spell
├── FSoM_RadialSlotData.uasset
├── UI_RadialSlot.uasset              <- slot generique
├── UI_RadialSlot_OLD.uasset          <- ancien slot (deconnecte, a supprimer)
├── UI_RadialMenu.uasset              <- ancien radial (deconnecte, a supprimer)
└── UI_Radial_Main.uasset             <- radial principal actif

Content/Systems/Magic/Data/
├── FSoM_DeitySpells.uasset           <- struct { SpellIDs: Array<Name> }
Content/Systems/Magic/Core/
├── BP_MagicComponent.uasset          <- UnlockedSpells, UnlockDeity, CastSpell
```

---

## SwitchCategory -- logique finale (25/05/2026)

```
Entry
  |
  v
Branch (CurrentCategory == Weapons)
  |
  |-- TRUE -> SET CurrentCategory = Deity
  |           PopulateMagicSchools
  |           SET SelectedIndex=0 / TargetRotation=0 / CurrentRotation=0
  |
  |-- FALSE -> Branch (CurrentCategory == Deity)
                |
                |-- TRUE  -> SET CurrentCategory = Weapons
                |            PopulateWeaponSlots
                |            SET SelectedIndex=0 / TargetRotation=0 / CurrentRotation=0
                |
                |-- FALSE (Spell) -> SET CurrentCategory = Deity
                                     PopulateMagicSchools
                                     SET SelectedIndex=0 / TargetRotation=0 / CurrentRotation=0
```

---

## ValidateRadial -- logique finale (25/05/2026)

Fonction dediee sur BP_SoM_PlayerController (pas dans l'EventGraph).
Variables locales : TempSchoolID (FName), TempSpellID (FName).

```
Branch (CurrentCategory == Weapons)
  TRUE  -> ValidateSelectedWeapon
  FALSE -> Branch (CurrentCategory == Deity)
    TRUE  -> TempSchoolID = SlotDataList[SelectedIndex].SlotID
             SET CurrentCategory = Spell
             SET SelectedIndex = 0
             SET TargetRotation = 0
             SET CurrentRotation = 0
             PopulateMagicSpells(TempSchoolID)
    FALSE (Spell) -> TempSpellID = SlotDataList[SelectedIndex].SlotID
                     CastSpell(TempSpellID)
                     CloseRadial
```

IMPORTANT : ne pas utiliser CurrentMagicSchool pour distinguer N1/N2 --
PopulateMagicSpells commence par SET CurrentMagicSchool="None", la rendant inutilisable
comme discriminant. Utiliser CurrentCategory a la place.

---

## Architecture UnlockedSpells / UnlockDeity (25/05/2026)

Bug resolu : Make FSoM_DeitySpells a bDefaultValueIsIgnored=True sur le pin SpellIDs,
ce qui fait qu'UE5 ignore la valeur connectee.

Solution : noeud "Set Members in FSoM_DeitySpells" a la place.

```
UnlockDeity(DeityName)
  Branch (Map_Contains(UnlockedSpells, DeityName))
    TRUE  -> return (deja present)
    FALSE -> Set Members in FSoM_DeitySpells :
               StructRef = GET TempDeitySpells  (variable simple FSoM_DeitySpells, PAS un Array)
               SpellIDs  = GET TempSpellsIDs    (Array<FName> avec 4 elements par defaut)
             StructOut -> Map_Add(UnlockedSpells, Key=DeityName, Value=StructOut)
```

TempDeitySpells : variable membre de BP_MagicComponent, type FSoM_DeitySpells SIMPLE.
TempSpellsIDs : variable membre Array<FName>, Default = [Lumina_Attack, Lumina_Heal, Lumina_Buff, Lumina_Debuff].

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

## UI_Radial_Main -- variables cles

- `CurrentCategory` (ERadialMode) : Weapons / Deity / Spell
- `CurrentMagicSchool` (FName) : ecole selectionnee en N1 ("None" par defaut)
- `MagicComponentRef` (BP_MagicComponent) : injectee depuis OpenRadial(PC)
- `SelectedIndex` (Integer) : index slot selectionne
- `SlotWidgets` (Array<UI_RadialSlot>)
- `SlotDataList` (Array<FSoM_RadialSlotData>)
- `RadialRadius` (Float, 150)
- `CurrentRotation` (Float) : rotation courante interpolee
- `TargetRotation` (Float) : rotation cible
- `InterpSpeed` (Float, 8) : vitesse interpolation

---

## BP_SoM_PlayerController -- Open/Close

### OpenRadialMenu
```
Create UI_Radial_Main -> SET RadialMainRef
SET MagicComponentRef (via PlayerCharacterRef -> MagicComponent)
Add to Viewport (ZOrder 99)
Set Global Time Dilation (0.2)
Set Input Mode Game And UI
Remove IMC_Gameplay -> Add IMC_Radial (priority 1)
```

### CloseRadialMenu
```
Remove from Parent (RadialMainRef)
Set Global Time Dilation (1.0)
Set Input Mode Game Only
SET RadialMainRef = null
Remove IMC_Radial -> Add IMC_Gameplay (priority 0)
```

---

## Input map

| Input | Action |
|-------|--------|
| Hold IA_UI_Radial_Open | Ouvre radial + slow-mo |
| Stick G/D | IA_UI_Radial_Rotate : rotation plateau (selection) |
| IA_UI_Radial_ChangeCat | Switch categorie |
| IA_UI_Radial_Validate (A/X) | ValidateRadial : equiper arme / entrer N2 / caster sort |
| IA_UI_Radial_Cancel (B/Circle) | Spell->Deity / Deity->fermer |
| Release IA_UI_Radial_Open | Ferme + restore Time Dilation |

---

## Roadmap locale

- [x] ERadialMode + FSoM_RadialSlotData
- [x] UI_RadialSlot (SetSelected + SetSlotData)
- [x] UI_Radial_Main GenerateSlots (Cos/Sin)
- [x] OpenRadialMenu slow-mo + CloseRadialMenu restore
- [x] Navigation stick G/D (UpdateSelection + rotation plateau lerp)
- [x] UpdateCenterInfo (Text_ItemName + Text_Description)
- [x] SwitchCategory 3 branches (Weapons/Deity/Spell)
- [x] PopulateWeaponSlots valide PIE
- [x] ValidateSelectedWeapon valide PIE
- [x] C1-InputsUI : switch IMC open/close VALIDE PIE
- [x] C1-RadialMagie : MagicComponentRef injected a l'ouverture
- [x] C1-RadialMagie : PopulateMagicSchools (loop UnlockedSpells)
- [x] C1-RadialMagie : PopulateMagicSpells(SchoolID) -- 4 sorts Lumina
- [x] C1-RadialMagie : ValidateRadial (fonction PC, variables locales TempSchoolID/TempSpellID)
- [x] C1-RadialMagie : CastSpell(SpellID) -> CloseRadial
- [x] C1-RadialMagie : Cancel Spell->Deity / Deity->CloseRadial
- [x] C1-RadialMagie : Rotation slots Weapons + Deity + Spell
- [x] Fix bDefaultValueIsIgnored : Set Members in FSoM_DeitySpells
- [ ] Text_Category : "MAGIE" / "MAGIE - [NomEcole]" (dette mineure)
- [ ] Icones deites/sorts : ART-MagicIcons
- [ ] C1-CleanupDettes : SelectedIndex = index ChoosenWeapon a l'ouverture
- [ ] Supprimer UI_RadialMenu et UI_RadialSlot_OLD

---

## Historique

- Creation : 17/06/2025
- Refonte complete J-13 : 12/05/2026
- Nommage mis a jour : 15/05/2026
- MAJ architecture Magie + analyse SwitchCategory T3D : 21/05/2026
- MAJ decisions C1-RadialMagie actees : 23/05/2026
- MAJ C1-RadialMagie VALIDE PIE : 25/05/2026 -- architecture finale ValidateRadial, UnlockDeity, ERadialMode 3 valeurs
