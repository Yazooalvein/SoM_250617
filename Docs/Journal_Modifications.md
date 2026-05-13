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
- Pont temporaire armes : DiscoveredWeapons -> FSoM_RadialSlotData (refacto prevu J-15+)
- Arc : munitions illimitees (ACTE)

#### Nouveaux assets (Content/UI/Widgets/RadialMenu/)
- `ERadialMode` : enum Weapons / Magic
- `FSoM_RadialSlotData` : struct SlotID, DisplayName, Description, Icon, Category, StatA/B/C
- `UI_RadialSlot` : widget 80x80
  - SetSelected(bool) : toggle SelectionBorder/Grayout visibility
  - SetSlotData(FSoM_RadialSlotData) : SET SlotData + Make Brush from Texture -> Set Brush
- `UI_Radial_Main` : widget radial principal -- NAVIGATION VALIDE PIE
  - Variables : CurrentCategory, SelectedIndex, SlotWidgets, SlotDataList
  - RadialRadius = 330, RadialContainer Size = 0.01x0.01 (fix drift)
  - GenerateSlots() : Cos/Sin positioning, slots en cercle
  - UpdateCenterInfo() : SET Text_ItemName/Description/Category
  - UpdateSelection(AxisValue) : navigation par cran, accumulation TargetRotation
  - Event Tick : FInterpTo lerp + SetRenderTransformAngle + contre-rotation icones
  - Event Construct : GenerateSlots + UpdateCenterInfo + SetSelected(slot 0)
- `UI_RadialSlot_OLD` : ancien widget slot renomme (conserve, non utilise)

### 13/05/2026 -- Jalon J-13 WIP suite -- Fixes + Categories + Equipement

#### Fixes rotation et alignement
- Surbrillance a 12h des l'ouverture : ForEach SetSelected dans Event Construct
- Fix drift rotation : RadialContainer Size = 0.01x0.01 (pivot quasi-ponctuel)
- Fix sens rotation : inversion signe accumulation TargetRotation
- Centrage menu : RadialRadius = 330, SizeBox padding left = -50
- Image_Cursor masquee (surbrillance or suffisante, curseur a faire plus tard)

#### PopulateWeaponSlots -- pont temporaire armes VALIDE PIE
- Lit DiscoveredWeapons (Array<FName>) depuis BP_PlatformingCharacter
- GetDataTableRowFromName(DT_Weapons) -> Break FWeaponData -> Make FSoM_RadialSlotData
- SlotID = RowName, DisplayName = To Text(RowName), Icon = FWeaponData.Icons
- Appele depuis Event Construct (remplace les 4 slots hardcodes)

#### SwitchCategory -- changement categorie VALIDE PIE
- Toggle CurrentCategory Weapons <-> Magic
- Branch sur nouvelle categorie -> PopulateWeaponSlots ou Print "Magic TODO"
- Reset SelectedIndex/TargetRotation/CurrentRotation a 0 au switch
- IA_UI_RadialMenu_ChangeCat (Axis1D) dans IMC_Prototype
- Handle dans PC : IsValid(RadialMainRef) -> SwitchCategory(RadialMainRef)

#### ValidateSelectedWeapon -- confirmation equipement VALIDE PIE
- Recree dans UI_Radial_Main (migration depuis UI_RadialMenu)
- SlotDataList[SelectedIndex].SlotID -> EquipWeapon(BP_PlatformingCharacter)
- -> CloseRadialMenu(BP_PlatformingPlayerController)
- IA_validate_radial_selection branchee avec IsValid(RadialMainRef) guard dans PC

#### Dettes techniques identifiees
- ⚠️ Radial armes : au chargement, la surbrillance devrait se placer sur l'arme actuellement equipee
  (pas forcement le slot 0). A implementer lors de la refonte armes J-15+
- ⚠️ Comportement radial Magic a definir quand on travaillera la categorie magie
- ⚠️ UI_RadialMenu (ancien) toujours present mais deconnecte -- a nettoyer post-J-13
- ⚠️ WeaponDataTest dans BP_PlatformingCharacter : variable debug a supprimer post-J-13

#### Reste a faire J-13
- [ ] Retour bouton B (CloseRadialMenu sans equiper)
- [ ] UI_QuickslotBar : 3 slots HUD

---

## Rappel
Pour la roadmap detaillee : voir Docs/Roadmap_Gameplay.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 13/05/2026
