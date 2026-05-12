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
- Event Tick : decrementation cooldowns (ForEach Keys -> Find -> subtract DeltaSeconds -> Max 0 -> Map Add)
- CastSpell : Switch E_SpellTarget (Self=GetOwner, Enemy=LockOn) -> SpawnActor -> SET Caster/Target/SpellData -> Execute -> ConsumeMana -> cooldown

#### BP_SpellBase + enfants Lumina -- VALIDES PIE ✅
- BP_SpellBase : Execute (ApplyEffect -> chaque enfant gere son propre Destroy Actor)
- BP_Spell_Heal : HealthCurrent + EffectValues, clamp MIN(result, HealthMax) ✅
- BP_Spell_Attack : BPI_TakeDamage sur Target ✅
- BP_Spell_Buff : AffectedStat + EffectValues, Set Timer RestoreStats, anti-cumul (OriginalHealthMax branch) ✅
- BP_Spell_Debuff : MaxWalkSpeed - EffectValues, Set Timer RestoreSpeed, anti-cumul ✅

#### FSoM_SpellData -- champs complets
SpellID, SpellName, Deity, Category, ManaCost, CastTime, Cooldown, TargetType,
EffectValues, Duration, AffectedStat, DeliveryType, SpellClass

#### HUD mis a jour
- Switch HUD_OnStatChanged : ajout cases HealthMax, StaminaMax, ManaMax
- HealthMax change -> HealthPercent = HealthCurrent / NewValue (barre se redimensionne)
- Idem StaminaMax, ManaMax

### 12/05/2026 -- Jalon J-15 -- UI_HUD_Main FINALISE ✅

#### Layout finalise (Content/UI/Widgets/Main/)
```
Canvas Panel
└── HUD_Anchor (bas-gauche, pos 20/-20, size 400/150, alignment 0/1, Size To Content OFF)
    └── Horizontal Box
        ├── SizeBox_Weapon (64x64, Auto, V-Center, padding Right 8)
        │   └── Image_Weapon (Fill/Fill)
        └── HUD_Main_VertBox (Fill 1.0)
            ├── Overlay_HP (Fill 1.0)
            │   ├── SizeBox > HealthBar (Fill/Fill, rouge, Get_HealthBar_Percent)
            │   └── RichTextBlock_HP (Center/Center)
            ├── Overlay_ST (Fill 1.0)
            │   ├── SizeBox > StaminaBar (Fill/Fill, vert)
            │   └── RichTextBlock_ST (Center/Center)
            ├── Overlay_MP (Fill 1.0)
            │   ├── SizeBox > ManaBar (Fill/Fill, bleu)
            │   └── RichTextBlock_MP (Center/Center)
            └── XP (Auto, padding Top 8, violet)
```

#### Fonction UpdateStatText (centralisee)
- Inputs : Current (Float), Max (Float), Target (RichTextBlock ref)
- Pipeline : To Text (Float, 0 decimales) -> To String -> Append " / " -> To Text String -> Set Text
- Appelee depuis HUD_OnStatChanged (cases *Current) ET depuis InitHUD (init au demarrage)

#### DT_HUD_RichTextStyle
- Chemin : Content/UI/Widgets/Main/DT_HUD_RichTextStyle
- Row structure : RichTextStyleRow
- Row "Default" : font configuree, assignee sur les 3 RichTextBlocks
- Base pour futures fonts stylisees par stat ou divinite

#### Points d'attention
- SizeBox autour de chaque ProgressBar obligatoire (sinon Desired Size force hauteur excessive)
- Size To Content sur HUD_Anchor doit etre DECOCHE (sinon ignore Size 400x150)
- RichTextBlock necessite DT assignee pour afficher du texte (contrairement a TextBlock)
- To Text (Float) avec Max/Min Fractional Digits = 0 pour supprimer les decimales

#### Roadmap mise a jour
- [x] J-10/J-11/J-12 : BP_MagicComponent complet
- [x] J-14 : BP_SpellBase + 4 sorts Lumina valides
- [x] AffectedStat + E_DeliveryType ajoutes dans FSoM_SpellData
- [x] HUD reactif aux stats Max
- [x] J-15 : UI_HUD_Main finalise (layout, texte Current/Max, DT_RichTextStyle)
- [ ] J-13 UI : UI_RadialMagic (2 niveaux, slow-mo) + UI_QuickslotBar + binding input
- [ ] Refactorer BP_Spell_Buff/Debuff pour lire AffectedStat dynamiquement (dette)
- [ ] UnlockDeity data-driven depuis DT_Spells (dette)

---

## Rappel
Pour la roadmap detaillee : voir Docs/Roadmap_Gameplay.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 12/05/2026
