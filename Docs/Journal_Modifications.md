# Journal des Modifications -- Shadow of Mana

## Objectif
Suivi precis de toutes les evolutions majeures du projet.

## Entrees

### 17/06/2025 -- Nico -- Creation du projet
- Initialisation SoM sous UE5.6, template Third Person Platforming

### 18/06/2025 -- Nico
- Refactoring pipeline Gameplay de base (Dash, Roll, Jump, Stamina)

### 19-20/06/2025 -- Nico
- Lock-On, Menu Radial, refonte Combo

### 21/06/2025 -- Nico
- Refactorisation BP_ComboManagerComponent (TMap, fenetre dynamique)

### 24/06/2025 -- Nico
- Systeme armes data-driven, Menu Radial data-driven, Combo multi-armes

### 26/06/2025 -- Nico
- BPI_TakeDamage, BP_EnemyBase ReceiveDamage + OnDeath

### 27/06/2025 -- Nico
- BP_AIController_Enemy_Base, PawnSensing, aggro/perte

### 20/07/2025 -- Nico
- Animation Weapon Integration

### 07/05/2026 -- Jalons #1 a #7
- #1 : MCP + Hit Flash joueur (M_Hero HitFlashAmount)
- #2 : Mort du joueur (bIsDead, OnPlayerDeath, LoseAggro)
- #3 : OnStatChanged dispatcher (SetStatValue = unique point)
- #4 : Unification inputs (source unique InputActions/)
- #5 : Iframes dash/roll (bIsInvincible via AnimNotify)
- #6 : UI event-driven (zero polling, OnStatChanged)
- #7 : Hit Flash ennemi partiel + fix GameMode PlayerController

### 11/05/2026 -- Jalon #8 -- Migration UE5.7 + UnrealClaude
- Projet migre UE5.6 -> UE5.7.4
- UnrealClaude v1.4.5 : 28 outils MCP, panel operationnel
- Workflow dual-agent mis en place (Docs/Session_UnrealClaude.md)

### 11/05/2026 -- Jalon #9 -- Audit complet + nettoyage
- Fixes config (DefaultGame.ini, uproject, ProjectName)
- Nettoyage : ThirdPerson/, IA debug, Lvl_Platforming GameMode Override

### 11/05/2026 -- Session design
- Lore : Docs/Lore_ShadowOfMana.md
- Roadmap : Docs/Roadmap_Gameplay.md (6 priorites, 32 jalons)
- Architecture magie : Docs/Architecture/Magic_System.md

### 12/05/2026 -- Jalons J-10 a J-14 -- POC Systeme Magie VALIDE

#### Structure assets (Content/Systems/Magic/)
```
Magic/
├── Core/     : BP_MagicComponent, BP_SpellBase
├── Data/     : E_SpellCategory, E_SpellTarget, E_DeliveryType,
│               FSoM_SpellData, FSoM_DeitySpells, DT_Spells
└── Spells/Lumina/ : BP_Spell_Heal, BP_Spell_Attack, BP_Spell_Buff, BP_Spell_Debuff
```

#### BP_MagicComponent
- Variables : UnlockedSpells (Map<Name,FSoM_DeitySpells>), QuickslotSlots (Array<Name>),
  SpellCooldowns (Map<Name,Float>), bIsCasting (Boolean)
- Dispatcher : OnSpellCast(SpellID : Name)
- Fonctions : UnlockDeity / IsSpellUnlocked / ConsumeMana / CanCast / CastSpell
- Event Tick : decrementation cooldowns
- CastSpell : Switch E_SpellTarget -> SpawnActor -> Execute -> ConsumeMana -> cooldown

#### BP_SpellBase + enfants Lumina -- VALIDES PIE
- Heal, Attack, Buff, Debuff valides

#### FSoM_SpellData -- champs complets
SpellID, SpellName, Deity, Category, ManaCost, CastTime, Cooldown, TargetType,
EffectValues, Duration, AffectedStat, DeliveryType, SpellClass

#### HUD mis a jour
- Switch HUD_OnStatChanged : ajout cases HealthMax, StaminaMax, ManaMax

### 12/05/2026 -- Jalon J-15 -- UI_HUD_Main FINALISE

#### Layout finalise (Content/UI/Widgets/Main/)
- SizeBox_Weapon (64x64) + HUD_Main_VertBox (HP/ST/MP/XP)
- RichTextBlock HP/ST/MP avec UpdateStatText centralisee
- DT_HUD_RichTextStyle assigne sur les 3 RichTextBlocks
- To Text Float, 0 decimales, format "X / Y"

### 12/05/2026 -- Jalon J-13 WIP -- Refonte Radial Menu (fondations)

#### Decisions de design actees
- Radial unifie Armes + Magie, navigation verticale stick = changement categorie
- Curseur fixe a 12h, plateau qui tourne (Cos/Sin positioning)
- Slow-mo a l'ouverture : Time Dilation 0.2 (remplace Set Game Paused)
- 2 niveaux magie : Niveau 1 = Divinite, Niveau 2 = Sort
- Confirmation bouton A/X, Retour bouton B/Circle
- QuickslotBar : 3 slots (Haut/Gauche/Droite gamepad), assignation depuis menu general uniquement
- Slots non selectionnes : grises opacity 60%, selectionne : animation respiration + bordure or

#### Nouveaux assets (Content/UI/Widgets/RadialMenu/)
- `ERadialMode` : enum Weapons / Magic
- `FSoM_RadialSlotData` : struct SlotID, DisplayName, Description, Icon, Category, StatA/B/C
- `UI_RadialSlot` : widget 80x80
  - Image_Background (noir A=0.7), Image_Icon, Image_SelectionBorder (or, Draw As Border),
    Image_Grayout (noir A=0.5)
  - SetSelected(bool) : toggle SelectionBorder/Grayout visibility
  - SetSlotData(FSoM_RadialSlotData) : SET SlotData + Make Brush from Texture -> Set Brush
  - Variable SlotData stockee
- `UI_Radial_Main` : widget radial principal
  - Overlay fullscreen + SizeBox 400x400 centree
  - Canvas_Radial avec Text_Category, RadialContainer (Is Variable), Image_Cursor, VBox_Center
  - Variables : CurrentCategory, SelectedIndex, SlotWidgets, SlotDataList, RadialRadius(150)
  - GenerateSlots() : Clear -> ForEach SlotDataList -> Create UI_RadialSlot -> SetSlotData ->
    Cos/Sin angle (index*360/len - 90 -> D2R -> Cos*Radius/Sin*Radius) ->
    Add Child to Canvas -> Set Position -> Set Alignment(0.5/0.5) -> ADD SlotWidgets
  - Event Construct : 4 slots test hardcodes -> GenerateSlots -> UpdateCenterInfo
  - VALIDE PIE : 4 slots en cercle affiches, slow-mo fonctionnel
- `UI_RadialSlot_OLD` : ancien widget slot renomme (conserve, non utilise)

### 13/05/2026 -- Jalon J-13 WIP suite -- Navigation radial fonctionnelle

#### UI_Radial_Main -- nouvelles fonctions
- `UpdateCenterInfo` : lit SlotDataList[SelectedIndex] -> SET Text_ItemName/Description/Category
  - Text_Category : ERadialMode -> Enum to String -> To Text
  - 3 RichTextBlocks avec DT_HUD_RichTextStyle assigne
- `UpdateSelection(AxisValue : Float)` : navigation par cran
  - NbSlots = LENGTH(SlotDataList), AnglePerSlot = 360 / NbSlots
  - Branch AxisValue > 0 :
    True  -> SelectedIndex+1, TargetRotation+AnglePerSlot
    False -> SelectedIndex-1, TargetRotation-AnglePerSlot
  - Wrap : (SelectedIndex + NbSlots) % NbSlots
  - ForEach SlotWidgets -> SetSelected(ArrayIndex == SelectedIndex)
  - UpdateCenterInfo
- `Event Tick` : rotation visuelle fluide
  - FInterpTo(CurrentRotation, TargetRotation, DeltaSeconds, InterpSpeed=8.0) -> SET CurrentRotation
  - SetRenderTransformAngle(RadialContainer, CurrentRotation)
  - ForEach SlotWidgets -> SetRenderTransformAngle(slot, CurrentRotation * -1) (contre-rotation icones)

#### BP_PlatformingPlayerController -- fixes
- `OpenRadialMenu` : IsValid(RadialMainRef) guard (evite empilement infini)
  - Set Input Mode Game And UI (WidgetToFocus = RadialMainRef)
- `ValidateSelectedWeapon` : IsValid(RadialMenuRef) guard (stoppe erreurs runtime)
- `Handle_UI_RadialMenu_Rotate` : branche sur RadialMainRef -> UpdateSelection(AxisValue)
- Input IA_UI_RadialMenu_Rotate : Action Value directement en AxisValue (pas de Conv necessaire)

#### Etat navigation
- VALIDE PIE : Q/D (ou stick) = rotation par cran, lerp fluide, wrap correct dans les deux sens
- Text_ItemName change selon slot selectionne
- Icones restent droites pendant rotation plateau

#### Reste a faire J-13
- [ ] Changement categorie stick Haut/Bas (Weapons <-> Magic)
- [ ] Confirmation bouton A + Retour bouton B
- [ ] UI_QuickslotBar : 3 slots HUD
- [ ] Recabler PC sur UI_Radial_Main pour confirmation/retour

#### Roadmap mise a jour
- [x] J-10/J-11/J-12 : BP_MagicComponent complet
- [x] J-14 : BP_SpellBase + 4 sorts Lumina valides PIE
- [x] J-15 : UI_HUD_Main finalise
- [x] J-13 WIP : fondations radial + navigation par cran + lerp fluide VALIDE PIE
- [ ] J-13 suite : categories + confirmation + UI_QuickslotBar
- [ ] Refactorer BP_Spell_Buff/Debuff AffectedStat dynamique (dette)
- [ ] UnlockDeity data-driven depuis DT_Spells (dette)
- [ ] Hit Flash ennemis (vrai mesh + M_Enemy_Base + DMI)
- [ ] SaveGame
- [ ] ComfyUI textures

---

## Rappel
Pour la roadmap detaillee : voir Docs/Roadmap_Gameplay.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 13/05/2026
