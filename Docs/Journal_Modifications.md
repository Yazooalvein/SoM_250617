# Journal des Modifications -- Shadow of Mana

## Objectif
Suivi precis de toutes les evolutions majeures du projet.

## Entrees

### 17/06/2025 -- Nico -- Creation du projet
- Initialisation SoM sous UE5.6, template Third Person Platforming
- Creation docs de base

### 18/06/2025 -- Nico
- Refactoring pipeline Gameplay de base (Dash, Roll, Jump, Stamina)

### 19-20/06/2025 -- Nico
- Lock-On, Menu Radial, refonte Combo

### 21/06/2025 -- Nico
- Refactorisation BP_ComboManagerComponent (TMap, fenetre dynamique)

### 24/06/2025 -- Nico
- Systeme armes data-driven, Menu Radial data-driven, Combo multi-armes

### 26/06/2025 -- Nico -- Systeme degats
- BPI_TakeDamage, BP_EnemyBase ReceiveDamage + OnDeath

### 27/06/2025 -- Nico -- IA ennemis
- BP_AIController_Enemy_Base, PawnSensing, aggro/perte

### 20/07/2025 -- Nico -- Animation Weapon Integration

### 07/05/2026 -- Nico + Claude -- Jalon stable #1 -- Setup MCP + Hit Flash joueur
- Pipeline Claude Desktop + MCP unreal-handshake operationnel
- GitHub MCP operationnel (SSL fix, node.exe --use-system-ca)
- M_Hero : HitFlashAmount sur Emissive via Python MCP
- BP_PlatformingCharacter > ReceiveDamage : flash blanc 0.12s

### 07/05/2026 -- Nico + Claude -- Jalon stable #2 -- Mort du joueur
- BP_SoM_GameMode, bIsDead, OnPlayerDeath, LoseAggro

### 07/05/2026 -- Nico + Claude -- Jalon stable #3 -- OnStatChanged
- SetStatValue = unique point de modification
- OnStatChanged = notification event-driven

### 08/05/2026 -- Nico + Claude -- Jalon stable #4 -- Unification inputs
- Source unique Content/Input/InputActions/
- Suppression vestiges ThirdPerson

### 08/05/2026 -- Nico + Claude -- Jalon stable #5 -- Iframes dash/roll
- bIsInvincible via AnimNotify AN_EndDash/AN_EndRoll

### 10/05/2026 -- Nico + Claude -- Jalon stable #6 -- UI event-driven
- Zero polling, push pur via OnStatChanged

### 10/05/2026 -- Nico + Claude -- Jalon #7 -- Hit Flash ennemi + fix GameMode
- M_Mannequin HitFlashAmount (temporaire)
- BP_SoM_GameMode : Player Controller Class = BP_PlatformingPlayerController

### 11/05/2026 -- Nico + Claude -- Jalon stable #8 -- Migration UE5.7 + UnrealClaude
- Projet migre UE5.6 -> UE5.7.4
- UnrealClaude v1.4.5 : 28 outils MCP, panel operationnel

### 11/05/2026 -- Nico + Agent UE -- Jalon #9 -- Audit complet + nettoyage
- Fixes config, nettoyage vestiges ThirdPerson et IA debug
- Fix Lvl_Platforming GameMode Override

### 11/05/2026 -- Nico + Claude -- Session design + roadmap gameplay
- Lore : Docs/Lore_ShadowOfMana.md
- Roadmap : Docs/Roadmap_Gameplay.md (6 priorites, 32 jalons)
- Architecture magie : Docs/Architecture/Magic_System.md

### 12/05/2026 -- Nico + Claude -- Jalons J-10 a J-14 -- POC Systeme Magie COMPLET

#### Structure des assets (Content/Systems/Magic/)
```
Magic/
├── Core/     : BP_MagicComponent, BP_SpellBase
├── Data/     : E_SpellCategory, E_SpellTarget, FSoM_SpellData, FSoM_DeitySpells, DT_Spells
└── Spells/
    └── Lumina/ : BP_Spell_Heal, BP_Spell_Attack, BP_Spell_Buff, BP_Spell_Debuff
```

#### BP_MagicComponent (J-10/J-11/J-12)
- Variables : UnlockedSpells (Map<Name,FSoM_DeitySpells>), QuickslotSlots (Array<Name>), SpellCooldowns (Map<Name,Float>), bIsCasting (Boolean)
- Dispatcher : OnSpellCast(SpellID : Name)
- UnlockDeity(DeityName) : Map Contains -> Branch -> Make FSoM_DeitySpells -> Map Add
- IsSpellUnlocked(SpellID) -> Boolean Pure : ForEach Values -> Break -> Array Contains
- ConsumeMana(Amount) : GetOwner -> AttributeSetRef -> SetStatValue("ManaCurrent")
- CanCast(SpellID) -> Boolean Pure : NOT bIsCasting AND cooldown<=0 AND mana>=cost
- CastSpell(SpellID) : CanCast -> GetDT -> SpawnActor -> SET Caster/Target/SpellData -> Execute -> ConsumeMana -> ADD cooldown -> OnSpellCast

#### BP_SpellBase + enfants Lumina (J-14)
- BP_SpellBase (Actor) : variables Caster/Target/SpellData, fonctions Execute + ApplyEffect (vide)
- Execute : ApplyEffect -> Destroy Actor
- BP_Spell_Heal : ApplyEffect override -> HealthCurrent + EffectValues via SetStatValue
- BP_Spell_Attack : ApplyEffect override -> BPI_TakeDamage sur Target (EffectValues comme degats)
- BP_Spell_Buff : ApplyEffect override -> HealthMax + EffectValues, Set Timer "RestoreStats", EventGraph RestoreStats restaure HealthMax
- BP_Spell_Debuff : ApplyEffect override -> CharacterMovement MaxWalkSpeed - EffectValues, Set Timer "RestoreSpeed", EventGraph RestoreSpeed restaure speed

#### DT_Spells mis a jour (J-14)
- Champ SpellClass ajoute dans FSoM_SpellData (Class Reference -> BP_SpellBase)
- 4 lignes Lumina pointent vers leurs BP respectifs

#### BP_PlatformingCharacter
- BeginPlay : InitAttributes -> AddMainHUD -> InitComboTree -> UnlockDeity("Lumina")
- Composant MagicComponent ajoute

#### CastSpell -- architecture finale
- Ciblage sorts offensifs : Get Current Lock on Target (BP_CombatLockOnComponent)
- SpellClass lue depuis DT_Spells -> Spawn Actor -> Execute
- ConsumeMana + cooldown mis a jour systematiquement

#### Notes techniques
- FSoM_DeitySpells : struct helper pour contourner limite UE Map<Name, Array<Name>>
- Fonctions Pure incompatibles avec exec pins -> AND en chaine pour CanCast
- execute_script INTERDIT dans UnrealClaude (crash UE) -- agent = yeux uniquement
- Dette : UnlockDeity hardcode Lumina, a rendre data-driven quand multi-deites

#### Roadmap mise a jour
- [x] J-10 : BP_MagicComponent structure
- [x] J-11 : DT_Spells + Enums + Structs
- [x] J-12 : Fonctions BP_MagicComponent
- [x] J-13/J-14 : BP_SpellBase + sorts Lumina + CastSpell -- POC logique COMPLET
- [ ] J-13 UI : UI_RadialMagic (2 niveaux, slow-mo 0.15x) + UI_QuickslotBar + binding input
- [ ] Test gameplay : brancher CastSpell sur une touche et valider en PIE

---

## Rappel
Ce document doit etre mis a jour a chaque modification significative.
Pour la roadmap detaillee : voir Docs/Roadmap_Gameplay.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 12/05/2026
