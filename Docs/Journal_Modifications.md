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

### 12/05/2026 -- Nico + Claude -- Jalons J-10 a J-14 -- POC Systeme Magie VALIDE EN GAMEPLAY

#### Structure des assets (Content/Systems/Magic/)
```
Magic/
├── Core/     : BP_MagicComponent, BP_SpellBase
├── Data/     : E_SpellCategory, E_SpellTarget, FSoM_SpellData, FSoM_DeitySpells, DT_Spells
└── Spells/
    └── Lumina/ : BP_Spell_Heal, BP_Spell_Attack, BP_Spell_Buff, BP_Spell_Debuff
```

#### BP_MagicComponent
- Variables : UnlockedSpells (Map<Name,FSoM_DeitySpells>), QuickslotSlots (Array<Name>), SpellCooldowns (Map<Name,Float>), bIsCasting (Boolean)
- Dispatcher : OnSpellCast(SpellID : Name)
- UnlockDeity / IsSpellUnlocked / ConsumeMana / CanCast / CastSpell
- Event Tick : decrementation cooldowns (ForEach Keys -> Find -> subtract DeltaSeconds -> Max 0.0 -> Map Add)

#### CastSpell -- architecture finale validee
- CanCast -> GetDT -> SpawnActor -> SET Caster (GetOwner cast BP_PlatformingCharacter)
- Switch on E_SpellTarget : Enemy -> GetCurrentLockOnTarget / Self -> GetOwner
- SET Target -> SET SpellData -> Execute -> ConsumeMana -> ADD cooldown -> OnSpellCast

#### BP_SpellBase + enfants Lumina
- BP_SpellBase : Execute (ApplyEffect -> Destroy Actor), ApplyEffect (vide, overridee)
- BP_Spell_Heal : HealthCurrent + EffectValues, clamp a HealthMax via MIN -- VALIDE PIE ✅
- BP_Spell_Attack : BPI_TakeDamage sur Target
- BP_Spell_Buff : HealthMax + EffectValues, Set Timer RestoreStats
- BP_Spell_Debuff : MaxWalkSpeed - EffectValues, Set Timer RestoreSpeed

#### Bugs corriges lors du test gameplay
- Caster non assigne : GetOwner -> Cast BP_PlatformingCharacter manquait dans CastSpell
- Target None pour sorts Self : Switch on E_SpellTarget ajoute (Self = GetOwner, Enemy = LockOn)
- Heal depassait HealthMax : MIN(HealthCurrent + EffectValues, HealthMax) ajoute
- Cooldown ne se decrementait pas : Event Tick vide -> implementé

#### Architecture standardisee (decision design)
- 4 sorts par deite exactement : Attack / Heal / Buff / Debuff
- Hierachie Attack : Direct (actuel) / Projectile / AOE (futurs)
- Hierachie Debuff : Direct (actuel) / AOE (futur)
- AffectedStat (Name) a ajouter dans FSoM_SpellData pour rendre Buff/Debuff generiques
- DeliveryType (E_DeliveryType) a creer et ajouter dans FSoM_SpellData

#### Roadmap mise a jour
- [x] J-10/J-11/J-12 : BP_MagicComponent complet
- [x] J-14 : BP_SpellBase + sorts Lumina + CastSpell
- [x] Test gameplay POC valide (Heal fonctionne, cooldown, mana) ✅
- [ ] Ajouter AffectedStat + E_DeliveryType dans FSoM_SpellData
- [ ] Refactorer BP_Spell_Buff/Debuff pour lire AffectedStat dynamiquement
- [ ] J-13 UI : UI_RadialMagic (2 niveaux, slow-mo) + UI_QuickslotBar + binding input

---

## Rappel
Ce document doit etre mis a jour a chaque modification significative.
Pour la roadmap detaillee : voir Docs/Roadmap_Gameplay.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 12/05/2026
