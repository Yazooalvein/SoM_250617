# CLAUDE.md -- Shadow of Mana / Contexte IA

Ce fichier est lu par Claude au debut de chaque session pour retrouver le contexte du projet rapidement.
Il est lu aussi bien par Claude.ai (via GitHub MCP) que par l'agent UnrealClaude dans l'editeur UE5.7.

---

## Projet

- **Nom** : Shadow of Mana (SoM)
- **Genre** : ARPG Blueprint Only, inspire Secret of Mana + Dark Souls
- **Developpeur** : Nico (GitHub : Yazooalvein)
- **Repo** : https://github.com/Yazooalvein/SoM_250617
- **Moteur** : Unreal Engine 5.7.4

---

## Setup technique actuel Claude <> Projet

- **UnrealClaude v1.4.5** (plugin dans Plugins/UnrealClaude/)
  - Authentification via `claude auth login` (compte Anthropic Pro -- pas d'API key separee)
  - MCP bridge Node.js port 3000 (auto-start au lancement editeur)
  - 28 outils MCP natifs : Blueprint, AnimBlueprint, Enhanced Input, Material, Actor, Level, Asset...
  - Panel : Tools -> Claude Assistant dans l'editeur UE5.7
- **GitHub MCP** : node.exe --use-system-ca + NODE_TLS_REJECT_UNAUTHORIZED=0
- **Claude** : plan Pro, memoire activee

---

## Convention de nommage des jalons

```
Cycles = milestones jouables (C1, C2, C3, C4)
Jalons = prefixe thematique + nom court

Prefixes :
  COMBAT-   : mecaniques de combat (armes, lock-on, combo, inputs, camera)
  MAGIC-    : systeme magie (sorts, deites, radial magie, arbre talents)
  SYS-      : systemes transversaux (save, corruption, essence, statuseffects)
  ENEMY-    : ennemis (base, types, boss, IA)
  MAP-      : niveaux et zones
  HUD-      : interface joueur
  ANIM-     : animations
  DESIGN-   : sessions de design pur (pas de code)
  ART-      : sessions art (modeles, textures)
  MUS-      : sessions musique
  SESSION-  : sessions de design narratif/lore
  NAR-      : systemes narratifs (dialogue, quete, compagnons)
  FORGE-    : systeme de forge et equipement
  AUDIO-    : son et musique en jeu
  UI-       : menus et interfaces hors HUD
  QA-       : tests et qualite
  BUILD-    : builds distribuables
```

---

## Workflow dual-agent

### Roles
**Claude.ai** : chef de projet, planification, decisions archi, mise a jour docs via GitHub MCP
**Agent UnrealClaude** : discovery/audit Blueprint uniquement (pas de modif/creation), logue dans Session_UnrealClaude.md

### Regles
1. Nico pushe toujours en premier, Claude.ai committe la doc ensuite
2. L'agent UE logue ses actions dans Docs/Session_UnrealClaude.md en temps reel
3. Claude.ai lit Session_UnrealClaude.md en debut de session

---

## Documentation du projet -- structure et maintenance

### Fichiers a lire en debut de session
- `CLAUDE.md` (ce fichier)
- `Docs/Journal_Modifications.md`

### Fichiers a maintenir apres chaque session

| Fichier | Quand le mettre a jour |
|---|---|
| `CLAUDE.md` | A chaque session |
| `Docs/Journal_Modifications.md` | A chaque session |
| `Docs/Roadmap_Gameplay.md` | Quand un jalon change |
| `Docs/Architecture/Decisions.md` | A chaque decision importante |
| `Docs/Architecture/Stats_Progression.md` | Quand les stats changent |
| `Docs/Architecture/Combat_StatusEffects.md` | Quand effets statut ou Corruption changent |
| `Docs/Architecture/Economy_Drops.md` | Quand economie ou drops changent |
| `Docs/Architecture/Weapons_Progression.md` | Quand progression armes change |
| `Docs/Architecture/SaveSystem.md` | Quand le systeme de save evolue |
| `Docs/Architecture/Input_Architecture.md` | Quand les inputs changent |
| `Docs/Architecture/RadialMenu_Architecture.md` | Quand le radial evolue |
| `Docs/Lore_ShadowOfMana.md` | Quand le lore ou le cast change |
| `Docs/Project_Architecture_Index.md` | Quand un nouveau fichier doc est cree |
| `Docs/Blueprints/INDEX.md` | Quand un snapshot BP est cree ou mis a jour |
| `Docs/Blueprints/[BP].md` | Apres chaque jalon modifiant ce Blueprint |

---

## Blueprint Snapshot Layer -- PROTOCOLE PERMANENT

### Pourquoi
Claude n'a pas acces aux fichiers binaires Blueprint. Sans snapshots textuels, il travaille
a l'aveugle et peut proposer une architecture incompatible avec l'existant.
Ce layer garantit que Claude a toujours une vision exacte de l'etat reel du projet.

### Structure
```
Docs/
  Blueprints/
    INDEX.md
    BP_AttributeSet_Base.md
    BP_SoM_HeroCharacter.md
    BP_SoM_PlayerController.md
    BP_ComboManagerComponent.md
    BP_MagicComponent.md
    BP_InventoryComponent.md
    BP_CorruptionComponent.md
    BP_EssenceDrop.md
    BP_SoM_GameMode.md
    UI_HUD_Main.md
    UI_Radial_Main.md
  DataTables/
    DT_StatList.md
    DT_Weapons.md
    DT_Combo_Sword.md
    DT_Deities.md
    DT_Spells.md
  Structs/
    StatStruct.md
    FSoM_SpellData.md
```

### Format d'un fichier snapshot
Chaque fichier `Docs/Blueprints/[BP].md` contient :
- Role, Path UE5
- Variables : Nom | Type | Categorie | Notes
- Fonctions : Nom | Inputs | Outputs | Notes
- Dependances : qui appelle ce BP, qui il appelle
- Dettes actives liees a ce BP
- Date et jalon du dernier snapshot

### Quand mettre a jour
- **Fin de chaque jalon** qui modifie un BP -> mettre a jour le fichier snapshot correspondant
- **Pas a chaque commit** -- granularite = jalon
- **Nouveau BP cree** -> creer son snapshot avant la fin de la session
- **INDEX.md** -> mis a jour en meme temps que chaque snapshot

### Qui fait quoi
- **Agent UnrealClaude** : produit les donnees brutes (blueprint_query T3D)
- **Claude.ai** : formate les snapshots en Markdown et committe
- **Nico** : ne touche pas a ces fichiers manuellement

### Regle de lecture en debut de jalon
Avant de concevoir quoi que ce soit sur un BP, Claude lit son snapshot dans `Docs/Blueprints/`.
Si le snapshot est absent ou date de plus d'un jalon, demander un audit agent avant de continuer.

### Commit message pour les snapshots
```
doc: Blueprints/[BP].md - snapshot [NomJalon]
```

---

## Instructions pour l'agent UnrealClaude

### Ligne de contexte OBLIGATOIRE
```
CONTEXTE : Tu es l'assistant UnrealClaude lance dans UE5.7 depuis "Tools => Claude Assistant", tu as acces a 28 MCP Tools.
```

### Regles agent
- blueprint_query UNIQUEMENT. Jamais blueprint_modify, jamais execute_script.
- JAMAIS creer d'assets AnimGraph via MCP (add_state produit des shells corrompus)
- Agent = discovery/audit uniquement. Ouvrir une NOUVELLE session a chaque fois.

### Conventions architecture (IMPERATIVES)
- `SetStatValue(StatName, Value)` = UNIQUE point de modification des stats
- `GetStatValue(StatName)` = UNIQUE point de lecture des stats (Option B)
- `OnStatChanged` = dispatcher de notification
- `BP_SoM_GameMode` : Player Controller Class = BP_SoM_PlayerController
- Hit Flash ennemi : ABANDONNE
- Inputs : source unique Content/Input/InputActions/

---

## Architecture cle

### Personnage
- `BP_SoM_HeroCharacter` (Blueprint Only)
- Stats via `BP_AttributeSet_Base` (ref : `AttributeSetRef`)
- `bIsDead` + `IsDead()`, `bIsInvincible`, `OnPlayerDeath`, `OnStatChanged`
- `bRadialUnlocked` (bool, default=false)
- `BP_CombatLockOnComponent`, `MagicComponent`, `BP_ComboManagerComponent`, `BP_InventoryComponent`, `BP_CorruptionComponent` sur le Character
- HC.ChoosenWeapon SUPPRIME -- source unique : ComboManager.CurrentWeaponID (29/05/2026)
- DiscoveredWeapons SUPPRIME de HC -- migre vers BP_InventoryComponent (29/05/2026)

### Composants HC -- philosophie de factorisation
- HC = coordinateur leger, ne stocke pas d'etat metier
- BP_CombatLockOnComponent : tout l'etat lock-on
- BP_MagicComponent : tout l'etat magie
- BP_ComboManagerComponent : arme courante + niveau arme + etat combo
- BP_InventoryComponent : armes decouvertes (Content/Systems/Inventory/)
- BP_CorruptionComponent : tracking deites, purge, faiblesse 75 (Content/Systems/Corruption/)

### BP_InventoryComponent -- VALIDE PIE (29/05/2026)
- Variables : DiscoveredWeapons (Array<Name>)
- Fonctions : AddWeapon(WeaponID : Name), GetWeapons() -> Array<Name>
- Valeurs par defaut renseignees en Details panel instance HC (dette -> BeginPlay a terme)
- Radial lit GetWeapons() pour peupler les slots armes

### BP_CorruptionComponent -- VALIDE PIE (31/05/2026) -- MIS A JOUR SYS-StatSystem
- Variables : DeityUsageMap (TMap<Name, int32>)
- Fonctions : InitCorruption, TrackDeityUsage(DeityName), GetWeakDeity()->Name, PurgeCorruption(CostAmount)
- TrackDeityUsage : incremente DeityUsageMap + Corruption +5.0 par sort via SetStatValue
- PurgeCorruption : SetStatValue(Corruption, 0) + Map_Clear(DeityUsageMap)
- GetWeakDeity : retourne la deite la plus utilisee depuis la derniere purge
- GOTCHA : NE PAS stocker AttributeSetRef en variable -- recup dynamiquement GetOwner->Cast

### BP_EssenceDrop -- VALIDE PIE (02/06/2026)
- Composants : SphereComponent (root, OverlapAllDynamic), StaticMesh (NoCollision), PointLight
- Variables : EssenceValue (Int64), bCanBePickedUp (Bool, default false)
- BeginPlay : Delay(1.5s) -> SET bCanBePickedUp = true
- ActorBeginOverlap : Branch(bCanBePickedUp) -> Cast HC -> AttributeSetRef -> GetStatValue(EssenceValue) + valeur drop -> SetStatValue(EssenceValue) -> DestroyActor
- Gotcha : StaticMesh NoCollision obligatoire + bCanBePickedUp obligatoire

### Save System -- VALIDE PIE (03/06/2026)
- BPI_Saveable : interface SaveData(SaveGame) + LoadData(SaveGame) -- Content/Systems/Save/
- BP_SaveGame_SoM : conteneur pur, extends SaveGame
- BPI_Saveable sur : BP_InventoryComponent, BP_ComboManagerComponent, BP_MagicComponent, BP_AttributeSet_Base
- HP/ST/MP non persistees -- restaurees a max au load via GetStatValue(Max)
- Voir Docs/Architecture/SaveSystem.md

### Flux mort / respawn -- VALIDE PIE (03/06/2026)
- HC : bIsDead=true -> DisableInput -> PlayAnimMontage(AM_Death) -> Delay(0.2s) -> Call OnPlayerDeath
- PC BeginPlay : Cast HC -> SET PlayerCharacterRef -> Bind OnPlayerDeath -> OnHeroDied
- OnHeroDied : SpawnActor(BP_EssenceDrop) -> EssenceValue -> SetStatValue(EssenceValue, 0) -> CameraFade(noir) -> Delay(1.5s) -> SetStatValue(HP/ST/MP = GetStatValue(Max)) -> SET bIsDead=false -> IsValid(SaveGame) ? Fontaine : PlayerStart -> CameraFade(retour) -> EnableInput

### Stats heros -- SYS-StatSystem VALIDE PIE (04/06/2026)
- BP_AttributeSet_Base : TMap<Name, double> StatValues + StatMinValues + StatMaxValues
- Variables natives : HealthMax, StaminaMax, ManaMax UNIQUEMENT (cache synchronise par guards SetStatValue)
- HealthCurrent, StaminaCurrent, ManaCurrent : dans StatValues UNIQUEMENT -- pas de variable native
- GetStatValue(Name) -> double (Pure) : lecteur universel -- Map_Find + debug si absent
- SetStatValue : guards EssenceValue + Corruption + HealthMax + Default (FClamp via Maps) + 6 CallDelegate
- ConsumeStamina / HandleStaminaRegen / StartStaminaRegen : passent par GetStatValue + SetStatValue
- UI_HUD_Main : RefreshAllStats + InitHUD(AttributeSetRef) -- tout passe par GetStatValue
- Validation PIE complete : stats + HUD + fontaine + mort/respawn/essence + magie + attaques
- Voir Docs/Blueprints/BP_AttributeSet_Base.md
- Voir Docs/Architecture/Stats_Progression.md

### Corruption Magique -- VALIDE PIE (31/05/2026)
- Phase 1 plafond 50 (bCorruptionUnlocked=false) / Phase 2 plafond 100 (bCorruptionUnlocked=true)
- Logique metier dans BP_CorruptionComponent
- Voir Docs/Architecture/Combat_StatusEffects.md

### Hero 3D
- ABP actif : ABP_Manny_Platforming (pas ABP_Unarmed)
- Mesh : Meshy_AI_Crimson_Scarf_Adventu_0513214252_texture
- Rotation Rate Z = -1

### Camera -- VALIDE PIE (17/05/2026)
- SpringArm : 350, Z 60, Lag 8 -- IA_Look dans PC -- UpdateLockOnRotation V2

### Lock-On -- VALIDE PIE (15/05/2026)
- BP_CombatLockOnComponent sur Character -- SwitchCooldown source unique

### Combat -- VALIDE PIE (29/05/2026)
- BP_ComboManagerComponent : TMap<Name, FComboStep>, InitComboTree, HandleAttack, EquipWeapon
- CanAttack : source unique ComboManager

### Armes -- VALIDE PIE (31/05/2026)
- DT_Combo_Sword : Start -> Light1 -> Light2 + Heavy1
- ComboManager.CurrentWeaponID = source unique arme equipee
- HC.EquipWeapon = spawn physique + InventoryComponent.AddWeapon + ComboManager.EquipWeapon

### Magie -- VALIDE PIE (27/05/2026)
- BP_MagicComponent : CastSpell, IsDeityAccessible, LockDeity, UnlockDeity, IncrementSpellUsage, LevelUpSpell
- ConsumeMana : GetStatValue(ManaCurrent) - cout -> SetStatValue(ManaCurrent)
- Deite C1 : Lumina

### UI / HUD -- VALIDE PIE (04/06/2026)
- UI_HUD_Main : event-driven, HP/ST/MP/Essence/Corruption VALIDE PIE
- RefreshAllStats : recalcule tous les pourcentages via GetStatValue
- InitHUD(AttributeSetRef) : SET HUD.AttributeSetRef -> RefreshAllStats -> UpdateStatText
- UpdateStatText : GetStatValue pour les 6 stats texte (Current/Max x3) + EssenceValue
- HUD_OnStatChanged -> RefreshAllStats (switch supprime)
- CorruptionPercent : GetStatValue("Corruption") / 100
- EssenceValue : GetStatValue -> Conv_DoubleToString

### Inputs -- VALIDE PIE (23/05/2026)
- IMC_Gameplay, IMC_Radial, IMC_Menu, IMC_Dialogue, IMC_Cutscene

---

## Jalons completes

- [x] Jalons fondateurs (#1-#9, J-10 a J-15, J-RadialMenu, J-Cleanup) -- historique
- [x] COMBAT-LockOn, COMBAT-Camera, COMBAT-LockMove, COMBAT-ComboFix (15-18/05/2026)
- [x] COMBAT-InputsUI VALIDE PIE (23/05/2026)
- [x] MAGIC-RadialMagie, MAGIC-ProgressionDesign, MAGIC-DataLayer (25/05/2026)
- [x] MAGIC-UnlockSystem, COMBAT-CleanupDettes (27/05/2026)
- [x] DESIGN-StatsProgression, DESIGN-StatusEffects, DESIGN-Corruption, DESIGN-Economy (28/05/2026)
- [x] COMBAT-WeaponArchitecture COMPLET VALIDE PIE (29/05/2026)
- [x] DESIGN-WeaponProgression (30/05/2026)
- [x] HUD-Core VALIDE PIE (31/05/2026)
- [x] DESIGN-SaveDesign (31/05/2026)
- [x] COMBAT-SwordMoveset CLOS VALIDE PIE (31/05/2026)
- [x] SYS-CorruptionSystem VALIDE PIE (31/05/2026)
- [x] SYS-EssenceMana VALIDE PIE (02/06/2026)
- [x] SYS-SaveGame VALIDE PIE (03/06/2026)
- [x] INFRA-BlueprintSnapshotLayer (04/06/2026)
- [x] **SYS-StatSystem VALIDE PIE (04/06/2026)**

## Jalon en cours

Aucun -- prochain jalon a definir.

## Dettes techniques

- **Roll en lock-on** -> ANIM-Pass1 (C1)
- **Rename ABP_Manny_Platforming -> ABP_Hero** -> ANIM-Pass1 (C1)
- **WeaponClass hardcode BP_Enemy_Sword01** -> ENEMY-Types (C2)
- **Retopo hero 246K -> 10-15K** -> ART-Hero
- **Radial curseur position initiale a l'ouverture** -> UI-RadialRefacto (C2)
- **Stats ennemis BP_Enemy_Base** -> ENEMY-Base (C1)
- **BP_StatusEffectComponent** -> SYS-StatusEffects (C2)
- **DiscoveredWeapons par defaut via Details panel HC** -> migrer vers BeginPlay (C2)
- **HUD Designer : TextBlock_Essence et CorruptionBar hors Overlay/SizeBox standard** -> UI-HUDPolish (C4)
- **Calibrage couts purge Corruption** -> SESSION-Economie
- **NextStepID et AnimToPlay dans ComboManager** : variables non utilisees -> nettoyage futur
- **ANIM-DeathMontage** -> ANIM-Pass1 (C2)
- **Mob porteur Essence** -> C2
- **SetStatValue HP/ST/MP dans OnHeroDied ET dans AttributeSet.LoadData** -- doublon a nettoyer
- **CollectFountainTransform prend index 0** -- filtrage par FountainID -> C2
- **DiscoveredWeapons par defaut via Details panel HC** -> migrer vers BeginPlay (C2)

## Prochains jalons C1 (dans l'ordre recommande)

1. **MAGIC-TreeModule** : arbre talents Lumina
2. **ENEMY-Base** : stats sur BP_Enemy_Base
3. **ENEMY-Boss1** : 1 boss, 1-2 patterns
4. **MAP-C1Level** : couloir -> mobs -> fontaine -> arene boss
5. **ANIM-Pass1** : rename ABP, roll en lock-on

## Sessions design a planifier

- **SESSION-Noms** : tous les personnages
- **SESSION-LoreDeites** : rituels par deite, cout Essence
- **SESSION-ZonesA1** : structure zones, Fontaines
- **SESSION-Economie** : calibrage PO/Essence, prix marchands, couts purge

---

## Notes techniques importantes

- SetStatValue = UNIQUE point de modification stats
- GetStatValue(Name) -> double (Pure) = UNIQUE point de lecture stats (Option B -- depuis SYS-StatSystem)
- Variables natives BP_AttributeSet_Base : HealthMax, StaminaMax, ManaMax UNIQUEMENT
- HealthCurrent/StaminaCurrent/ManaCurrent vivent UNIQUEMENT dans StatValues (TMap) -- pas de variable native
- Guard HealthMax dans SetStatValue : Value -> SET HealthMax natif DIRECTEMENT, sans FMin ni GetStatValue(HealthCurrent)
- GOTCHA CRITIQUE : FMin(Value, GetStatValue("HealthCurrent")) dans guard HealthMax -> HealthMax = 0 si HealthCurrent absente de la Map au moment du ForEach
- InitHUD doit recevoir AttributeSetRef en parametre et SET HUD.AttributeSetRef AVANT RefreshAllStats
- HUD_OnStatChanged simplifie : appel direct RefreshAllStats (plus de Switch)
- EssenceValue dans UpdateStatText : Conv_DoubleToString (pas Conv_Int64ToString)
- CorruptionPercent = GetStatValue("Corruption") / 100 (ProgressBar attend 0..1)
- ABP_Manny_Platforming = ABP du HERO (pas ABP_Unarmed)
- SwitchCooldown = dans BP_CombatLockOnComponent UNIQUEMENT
- T3D export = meilleur outil d'audit Blueprint
- search_nodes UnrealClaude : utiliser espaces ("Set Stat Value" pas "SetStatValue")
- add_state MCP AnimGraph = shell corrompu -> creer manuellement
- IA_Look dans PC (pas HeroCharacter)
- LevelMin = 0 dans DT_Combo
- HandleAttack sans parametre ChoosenWeapon
- HC.ChoosenWeapon SUPPRIME -- source unique ComboManager.CurrentWeaponID
- PopulateWeaponSlots lit InventoryComponent.GetWeapons()
- TenaciteEtat heros : base 25, Float dans StatValues
- UnlockDeity : "Set Members in FSoM_DeitySpells" NON "Make FSoM_DeitySpells"
- UnlockDeity Map_Contains : TRUE = deja present -> return
- IsDeityAccessible = Contains(UnlockedSpells) AND NOT Contains(LockedDeities)
- DT_Deities BaseSpells : [0=Attack, 1=Heal, 2=Buff, 3=Debuff]
- Athanor = Salamandre
- Corruption faiblesse 75 = deite la plus utilisee DEPUIS LA DERNIERE PURGE
- BP_CorruptionComponent : NE PAS stocker AttributeSetRef en variable -- recup dynamiquement GetOwner->Cast
- BP_EssenceDrop : StaticMesh NoCollision + bCanBePickedUp Delay 1.5s
- BP_FountainComponent : GetComponentByClass Target = self (la Fontaine, pas le HC)
- BPI_Saveable : GetComponentsByInterface + K2Node_Message = appel interface sans Cast explicite
- LockedDeities sauvegarde (delta) / UnlockedSpells reconstruit depuis DT_Deities au load
- Git : si conflit LFS -> git checkout origin/main -- Docs/ + commit + push --force-with-lease

---

## Comment demarrer une session

### Session claude.ai
1. Nico dit : "on travaille sur SoM"
2. Lire CLAUDE.md + Journal_Modifications.md
3. Si la session touche un BP specifique : lire son snapshot dans Docs/Blueprints/
4. Resume etat actuel + proposition suite

### Session UnrealClaude
1. Tools -> Claude Assistant -> NOUVELLE session
2. "CONTEXTE : Tu es l'assistant UnrealClaude lance dans UE5.7 depuis 'Tools => Claude Assistant', tu as acces a 28 MCP Tools."
3. DISCOVERY UNIQUEMENT

---

*Derniere mise a jour : 04/06/2026*
