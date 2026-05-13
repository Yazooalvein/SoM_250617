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
- Roadmap : Docs/Roadmap_Gameplay.md
- Architecture magie : Docs/Architecture/Magic_System.md

### 12/05/2026 -- Jalons J-10 a J-14 -- POC Systeme Magie VALIDE

#### Structure assets (Content/Systems/Magic/)
- BP_MagicComponent, BP_SpellBase
- E_SpellCategory, E_SpellTarget, E_DeliveryType, FSoM_SpellData, FSoM_DeitySpells, DT_Spells
- BP_Spell_Heal, BP_Spell_Attack, BP_Spell_Buff, BP_Spell_Debuff (Lumina) -- VALIDES PIE

#### BP_MagicComponent
- UnlockedSpells, QuickslotSlots, SpellCooldowns, bIsCasting
- CastSpell : Switch E_SpellTarget -> SpawnActor -> Execute -> ConsumeMana -> cooldown

### 12/05/2026 -- Jalon J-15 -- UI_HUD_Main FINALISE
- SizeBox_Weapon (64x64) + HUD_Main_VertBox (HP/ST/MP/XP)
- RichTextBlock HP/ST/MP + UpdateStatText + DT_HUD_RichTextStyle

### 12-13/05/2026 -- Jalon J-13 COMPLET -- Radial Menu + Quickslot

#### Radial Menu (UI_Radial_Main) -- VALIDE PIE
- Navigation par cran (stick G/D), lerp fluide, wrap correct
- UpdateCenterInfo : textes centre depuis SlotDataList[SelectedIndex]
- Fix surbrillance 12h a l'ouverture + drift (RadialContainer 0.01x0.01)
- Fix sens rotation : inversion signe accumulation TargetRotation
- Centrage : RadialRadius = 330, SizeBox padding left = -50
- Image_Cursor masquee (a faire plus tard)

#### PopulateWeaponSlots -- pont temporaire armes VALIDE PIE
- DiscoveredWeapons (Array<FName>) -> GetDataTableRow(DT_Weapons) -> FSoM_RadialSlotData
- Remplace les 4 slots hardcodes dans Event Construct

#### SwitchCategory -- VALIDE PIE
- Toggle CurrentCategory Weapons <-> Magic
- Reset SelectedIndex/TargetRotation/CurrentRotation = 0 au switch
- IA_UI_RadialMenu_ChangeCat -> Handle dans PC avec IsValid guard

#### ValidateSelectedWeapon -- VALIDE PIE
- Migre depuis UI_RadialMenu vers UI_Radial_Main
- SlotDataList[SelectedIndex].SlotID -> EquipWeapon -> CloseRadialMenu
- IA_validate_radial_selection avec IsValid guard dans PC

#### Cancel -- VALIDE PIE
- IA_UI_Radial_Cancel -> IsValid(RadialMainRef) -> CloseRadialMenu
- Note : a terme migrer vers IMC_UI dedie (dette)

#### Quickslot POC -- VALIDE PIE
- 3 variables dans PC : QuickslotUp/Left/Right (FName, SpellID)
- IA_Quickslot_Up/Left/Right -> CastSpell via MagicComponent
- Mapping clavier : & (1) / e accent (2) / guillemet (3)
- Mapping gamepad prevu : fleches ↑ ← →  (fleche ↓ = switch page futur)

#### Session design actee (13/05/2026)
- Mapping PS5 complet acte (voir Docs/Architecture/UI_GlobalMenu.md)
- Quickslot : 3 slots, multi-pages via fleche bas, choix strategique (4 sorts / 3 slots)
- Roadmap reorganisee par dependances + sessions creatives (J-MAP / J-ART / J-MUS)
- Lock-On : dette confirmee (J-lock entre J-13 et J-15)
- Arc : munitions illimitees ACTE

#### Dettes techniques J-13
- ⚠️ Radial : surbrillance devrait pointer l'arme equipee a l'ouverture (pas slot 0) -- J-15+
- ⚠️ Categorie Magic : comportement a definir (affiche "TODO" pour l'instant)
- ⚠️ UI_RadialMenu (ancien) present mais deconnecte -- a nettoyer J-A
- ⚠️ WeaponDataTest dans BP_PlatformingCharacter : variable debug a supprimer J-A
- ⚠️ IMC_UI dedie a creer pour les inputs menus -- J-C

---

## Rappel
Pour la roadmap detaillee : voir Docs/Roadmap_Gameplay.md
Pour le design UI/HUD/Menu : voir Docs/Architecture/UI_GlobalMenu.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 13/05/2026
