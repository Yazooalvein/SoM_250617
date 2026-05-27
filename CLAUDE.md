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
  - Facturation : incluse dans forfait Pro claude.ai (verifiable via `claude auth status`)
- **GitHub MCP** : node.exe --use-system-ca + NODE_TLS_REJECT_UNAUTHORIZED=0
- **Claude** : plan Pro, memoire activee

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
- `CLAUDE.md` (ce fichier) : contexte global, architecture cle, jalons, notes techniques
- `Docs/Journal_Modifications.md` : historique des sessions, derniers changements

### Fichiers a maintenir apres chaque session
Claude.ai est responsable de la coherence de toute la documentation.
Apres chaque decision, implementation ou changement de cap, mettre a jour :

| Fichier | Quand le mettre a jour |
|---|---|
| `CLAUDE.md` | A chaque session : jalons, dettes, notes techniques, ordre jalons |
| `Docs/Journal_Modifications.md` | A chaque session : entree datee avec ce qui a ete fait |
| `Docs/Roadmap_Gameplay.md` | Quand un jalon change de statut ou qu'un nouveau jalon est cree |
| `Docs/Architecture/Decisions.md` | A chaque decision importante (abandon, choix archi, gotcha) |
| `Docs/Architecture/[Systeme].md` | Quand l'architecture d'un systeme change |
| `Docs/Architecture/Input_Architecture.md` | Quand les inputs ou IMC changent |
| `Docs/Architecture/RadialMenu_Architecture.md` | Quand le radial menu evolue |
| `Docs/Project_Architecture_Index.md` | Quand un nouveau fichier doc est cree |

### Fichier decisions -- IMPORTANT
`Docs/Architecture/Decisions.md` centralise toutes les decisions architecturales importantes :
abandon de features, choix de source de verite, changements d'approche, gotchas identifes.
Objectif : retrouver en 30 secondes POURQUOI une chose a ete faite, sans fouiller le journal.
Toute decision non triviale doit y etre loguee avec : contexte, decision, raison, consequences.

### Regle generale
La documentation doit rester coherente avec le code. Si quelque chose change dans le projet,
la doc change dans la meme session. Une doc perimee est pire qu'une doc inexistante.

---

## Instructions pour l'agent UnrealClaude

### Ligne de contexte OBLIGATOIRE dans chaque prompt
```
CONTEXTE : Tu es l'assistant UnrealClaude lance dans UE5.7 depuis "Tools => Claude Assistant", tu as acces a 28 MCP Tools.
```
Sans cette ligne, l'agent se croit dans Claude Code CLI et n'utilise pas ses outils MCP.

### Regles agent
- blueprint_query UNIQUEMENT. Jamais blueprint_modify, jamais execute_script.
- JAMAIS creer d'assets AnimGraph via MCP (add_state produit des shells corrompus)
- Toute creation d'etat AnimGraph = manuelle dans l'editeur
- Agent = discovery/audit uniquement. Pas de creation, pas de modification.
- Ouvrir une NOUVELLE session a chaque fois (pas continuer une ancienne)

### Logging obligatoire
Format dans Docs/Session_UnrealClaude.md :
```
### [DATE] -- [NOM DU BLUEPRINT / ASSET]
**Action** : ce qui a ete fait
**Pourquoi** : raison ou contexte
**Points d'attention** : gotchas, dependances
```

### Conventions architecture (IMPERATIVES)
- `SetStatValue(StatName, Value)` = UNIQUE point de modification des stats
- `OnStatChanged` = dispatcher de notification
- `BP_SoM_GameMode` : Player Controller Class = BP_SoM_PlayerController
- Hit Flash ennemi : ABANDONNE -- screen shake + animation suffisent (voir Decisions.md)
- Inputs : source unique Content/Input/InputActions/
- IMC_Gameplay : inputs gameplay (ex IMC_Prototype renomme -- C1-InputsUI COMPLET)

---

## Architecture cle

### Personnage
- `BP_SoM_HeroCharacter` (Blueprint Only, ex BP_PlatformingCharacter)
- Stats via `BP_AttributeSet_Base` (ref : `AttributeSetRef`)
- `bIsDead` (private) + `IsDead()` (public pure)
- `bIsInvincible` (iframes dash/roll, pilote par AnimNotify)
- `OnPlayerDeath` dispatcher, `OnStatChanged` dispatcher
- `bRadialUnlocked` (bool, default=false) : bloque ouverture radial jusqu'a evenement narratif
- `DiscoveredWeapons` (Array<FName>) : source de verite Radial, alimente par EquipWeapon
- `ChoosenWeapon` (FName) : arme courante, sette par EquipWeapon, lu par les inputs attaque
- `BP_CombatLockOnComponent` : sur le CHARACTER (pas le PC)
- `MagicComponent` : BP_MagicComponent sur le Character
- `BP_ComboManagerComponent` : sur le Character

### Hero 3D
- ABP actif : **ABP_Manny_Platforming** (pas ABP_Unarmed qui est pour les ennemis)
- Mesh : Meshy_AI_Crimson_Scarf_Adventu_0513214252_texture (Content/Characters/Players/Hero_Test/)
- Retargeting : Mannequin source -> Hero target (Compatible Skeletons)
- Variables ABP_Manny_Platforming : Character, MovementComponent, Velocity, GroundSpeed,
  ShouldMove, IsFalling, WeaponType, Strafe, Can Strafe, Double/Wall Jump...
- Rotation Rate Z = -1 (pivot instantane hors lock-on)
- Variables LastAxisX, LastAxisY (double) : stockees au Triggered de IA_Move
- 246K triangles LOD0 -> retopo (cible 10-15K) -- ART-Hero
- 6 doigts par main (artefact Meshy) -- ART-Hero

### Camera -- J-Camera COMPLET VALIDE PIE (17/05/2026)

#### SpringArm (BP_SoM_HeroCharacter)
- Target Arm Length : 350, Socket Offset Z : 60
- Camera Lag Speed : 8, Camera Lag Max Distance : 200

#### Screen Shake
- CS_HitReceived + CS_EnemyDeath dans Content/Systems/Camera/
- Appeles depuis ReceiveDamage (HeroCharacter) et KillMeNow (Enemy_Base)

#### IA_Look dans BP_SoM_PlayerController
- Fonction `Aim(Axis X, Axis Y)` dans le PC
- IA_Look RETIRE de BP_SoM_HeroCharacter

#### UpdateLockOnRotation V2
- Variables PC : bPlayerIsLooking (bool), LookIdleTime (float), LookReturnDelay (float, 1.5), LockOnReturnSpeed (float, 3.0)
- Guard supplementaire : Branch(Is Rolling) avant SetControlRotation -> si rolling, exit sans modifier
- Flow : DynamicCast -> Branch(IsRolling) -> Branch(bPlayerIsLooking) -> Branch(LookIdleTime >= LookReturnDelay) -> SetControlRotation

### LockMove COMPLET VALIDE PIE (18/05/2026)

#### Fix Move() en lock-on
- Probleme : en lock-on, deplacement partait vers l'ennemi (Control Rotation = direction ennemi)
- Solution : Branch(bisLockOnActive) dans Move() :
  - Lock-on actif : GetPlayerCameraManager -> GetCameraRotation -> Yaw -> MakeRotator(0,Yaw,0) -> GetForward/RightVector
  - Hors lock-on : comportement original (GetControlRotation)
- ScaleValues : branches sur LastAxisX/LastAxisY (stockees au Triggered de IA_Move)
- Deplacement en lock-on VALIDE PIE

#### Fix rotation de base
- CharacterMovement -> Rotation Rate Z = -1 -> pivot instantane hors lock-on

#### Roll en lock-on -- DETTE -> C1-AnimationsPass1
- Probleme : roll en lock-on part toujours vers l'ennemi
- Cause racine : Root Motion en World Space + UseControllerRotationYaw=true force
  le character a regarder l'ennemi chaque frame, annulant SetActorRotation
- Solution propre : LaunchCharacter dans direction stick+camera + animation visuelle sans Root Motion
  (architecture DS/KH) -- A traiter en C1-AnimationsPass1
- En attendant : roll hors lock-on fonctionne correctement

### Lock-On -- COMPLET VALIDE PIE (15/05/2026)
- `BP_CombatLockOnComponent` : sur le Character
  - bisLockOnActive, CurrentTarget, AvailableTargets, LockOnRange, SwitchCooldown
  - OnLockOnActivated / OnLockOnDeactivated (dispatchers custom)
  - **SwitchCooldown** : source de verite UNIQUE pour le cooldown de switch cible
    (LockOnSwitchCooldown du PC est redondant -> a supprimer dans C1-CleanupDettes)
- `BP_SoM_HeroCharacter` bindings (au BeginPlay) :
  - OnLockOnActivated_Handler : bOrientRotationToMovement=false + UseControllerRotationYaw=true
  - OnLockOnDeactivated_Handler : bOrientRotationToMovement=true + UseControllerRotationYaw=false
- Strafe VALIDE PIE : BS_Unarmed_Strafe (Forward x Strafe [-1,1]), animations placeholder

### Ennemis
- `BP_Enemy_Base` : bCanBeLocked, bIsDead, OnDeath, bIsLocked, bIsAttacking, bHasAlreadyHit
  - WeaponClass (hardcode BP_Enemy_Sword01 -- a generaliser C2-EnemyMesh)
  - Implements BPI_TakeDamage
  - Variables stats : MaxHealth, CurrentHealth, AttackRadius
  - Hit Flash ennemi : ABANDONNE (voir Decisions.md)
- `BP_Enemy_TestBed` : enfant de BP_Enemy_Base
  - MaxHealth, CurrentHealth, AttackRadius exposes Instance Editable en map
  - Utilise BP_AIController_Enemy_Base + BT_Enemy_Base (pas de BT dedie)
  - Place dans Lvl_TestBed pour tests
- `BP_AIController_Enemy_Base` : Behavior Tree + PawnSensing
- ABP_Unarmed : pour les ENNEMIS SANS ARME (pas le hero)

### TestBed -- COMPLET VALIDE PIE (18/05/2026)
- Map : `Content/Maps/Lvl_TestBed`
  - Sol BSP checker 4000x4000, obstacles BSP + cubes StaticMesh, plateforme sureleve
  - NavMeshBoundsVolume couvrant toute la zone
  - Lighting Movable (DirectionalLight + SkyLight + SkyAtmosphere) -- zero bake
  - GameMode Override : BP_SoM_GameMode
- `BP_Enemy_TestBed` : stats configurables en map sans ouvrir le BP
- SFX placeholder dans Content/Audio/SFX/Combat/ :
  - Hit joueur recu, attaque ennemi, roll hero
  - Branchement direct Play Sound at Location (pas de SoundCue)
- `BP_Debug_UnlockDeity` : dans Content/Systems/Magic/Debug/
  - Overlap -> UnlockDeity("Lumina") + SET bRadialUnlocked=true
  - Simule l'evenement narratif de debut de jeu

### Combat -- ComboFix VALIDE PIE (18/05/2026)
- `BP_ComboManagerComponent` : architecture TMap<Name, FComboStep> -- a conserver
  - `CurrentWeaponID` (Name) + `CurrentWeaponLevel` (int) : source de verite combo
  - `InitComboTree(WeaponID, WeaponLevel)` : charge ComboStepMap depuis DT_Combo de l'arme
  - `HandleAttack(AttackType)` : plus de parametre ChoosenWeapon (lit CurrentWeaponID en interne)
  - `CanAttack` (bool) : gere uniquement par le ComboManager
- `BPI_TakeDamage` : interface implementee par Character et Enemy_Base
- ReceiveDamage : bIsInvincible? -> IsDead? -> SetStatValue("HealthCurrent") -> screen shake -> mort?
- Flow equipement : EquipWeapon -> SET ChoosenWeapon -> AddUnique(DiscoveredWeapons) -> InitComboTree
- Flow attaque : IA_Attack -> Branch(CanAttack) -> HandleAttack(AttackType) -> PlayAttackMontage

### Armes
- `BP_Weapon_Base` : WeaponData, OwnerCharacter, bIsEquipped, bCanDealDamage, TouchedActors
- `DT_Weapons` : 2 entrees (Sword_01, 2HSword_01), struct FWeaponData
  - FWeaponData contient : Name, Type, Level, Mesh, Stats, Socket, BP_Weapon, icons, DT_Combo, IdleAnim
- `DT_Combo` par arme : rows avec StepID, InputType, AnimMontage, NextSteps, WeaponID, LevelMin=0
- `LevelMin = 0` sur toutes les rows DT_Combo (niveau de base)

### GameMode / Controllers
- `BP_SoM_GameMode` (`/Game/Core/`) -- Player Controller Class = BP_SoM_PlayerController
- `BP_SoM_PlayerController` :
  - PlayerCharacterRef : SET au OnPossess
  - Lock-On : GetBP_CombatLockOnComponent, UpdateLockOnRotation V2, UpdateLockOnUIIndicator
  - Aim(Axis X, Axis Y) : gestion camera
  - OpenRadial : Branch(bRadialUnlocked) en entree -- FALSE -> Return

### Radial Menu -- COMPLET VALIDE PIE
- `ERadialMode` (enum) : Weapons / Magic
- `CurrentCategory` (ERadialMode) dans UI_Radial_Main : categorie active
- `SwitchCategory(Direction)` : toggle Weapons<->Magic, recharge les slots
  - Switch vers Magic : Branch(UnlockedSpells.Num() > 0) -- bloque si aucune deite
- Radial Magie 2 niveaux : N1 (Deity) -> N2 (Spell) -> CastSpell VALIDE PIE
- Deblocage narratif : bRadialUnlocked (Hero) + UnlockDeity() -- pas de check mecanique DiscoveredWeapons
- Voir Docs/Architecture/RadialMenu_Architecture.md pour details

### Magie -- C1-MagicUnlockSystem VALIDE PIE (27/05/2026)
- `BP_MagicComponent` : UnlockedSpells, LockedDeities, SpellUsageCounts, SpellLevels, TalentPoints,
  QuickslotSlots, SpellCooldowns, CategoryThresholdsConfig
- Fonctions : CastSpell, IsDeityAccessible, LockDeity, UnlockDeity, IncrementSpellUsage, LevelUpSpell, AddTalentPoint
- `BP_SpellBase` + 4 sorts Lumina valides PIE (Heal, Attack, Buff, Debuff)
- Radial 2 niveaux : N1 Deity -> N2 Spell -> CastSpell VALIDE PIE
- Etats deite : Non debloquee (invisible) / Debloquee+lockee (grisee, non castable) / Accessible (normal)
- Progression sorts : usage -> seuil effectif -> LevelUpSpell -> TalentPoints
- Formule seuil : EffectiveThreshold = BaseThreshold / Max(1, 9 - CurrentSpellLevel) -- inspire SoM
- Seuils par categorie (BP_SpellCategoryThresholds) : Attack=150, Heal=100, Buff=50, Debuff=35, Ultime=200
- Data layer deites : DT_Deities (FSoM_DeityData), DT_TalentNodes (FSoM_TalentNode) -- VALIDE PIE
- Convention BaseSpells : [0=Attack, 1=Heal, 2=Buff, 3=Debuff] pour toutes les deites
- Deites (8) : Lumina, Luna, Ombre, Sylphide, Gnome, Salamandre (=Athanor), Ondine, Dryade
- Corruption Magique : compteur sur le heros, effets negatifs progressifs, purge a la Fontaine de Fee
- Dette restante : UsageThreshold dans FSoM_SpellData a supprimer (remplace par BP_SpellCategoryThresholds)

### UI / HUD
- `UI_HUD_Main` : event-driven via OnStatChanged, zero polling -- FINALISE
- `UI_LockOnIndicator` : 1 image LockOnCross, widget statique positionne par PC, ZOrder=10

### Inputs -- etat actuel (C1-InputsUI COMPLET VALIDE PIE 23/05/2026)
- `IMC_Gameplay` (ex IMC_Prototype renomme) : inputs gameplay, charge au ReceivePossessed
- `IMC_Radial` : 4 IA navigation radial, actif pendant ouverture radial
- `IMC_Menu`, `IMC_Dialogue`, `IMC_Cutscene` : stubs vides
- Swap IMC dans PC : OpenRadial (Remove Gameplay + Add Radial) / CloseRadial (inverse)
- Voir Docs/Architecture/Input_Architecture.md pour details

### Mapping Gamepad PS5 (ACTE)
```
X=Saut  Carre=Esquive  Rond=Blocage  Triangle=Radial
L1=Attaque legere  R1=Attaque forte
L3=Sprint  R3=Lock-On (axis=changer cible)
Fleche Haut/Gauche/Droite=Quickslots 1/2/3  Fleche Bas=Switch page
Options=Menu Global
```

---

## Jalons completes

- [x] #1 a #9 : MCP, mort, stats, inputs, iframes, UI, hit flash joueur, migration UE5.7, audit
- [x] J-10 a J-14 : BP_MagicComponent + 4 sorts Lumina valides PIE
- [x] J-15 : UI_HUD_Main finalise
- [x] J-RadialMenu : Radial Menu complet + Quickslot POC VALIDE PIE
- [x] J-Cleanup : Suppression assets obsoletes
- [x] ART-Hero (partiel) : Hero placeholder PIE, workflow etabli
- [x] MUS-Workflow (exploration) : Workflow Suno etabli
- [x] J-LockOn COMPLET : Strafe VALIDE PIE, fix IsLockOnActive, edge cases valides (15/05/2026)
- [x] J-Renommage : Convention de nommage unifiee (15/05/2026)
- [x] J-Camera COMPLET : UpdateLockOnRotation V2, bPlayerIsLooking, screen shake, IA_Look dans PC (17/05/2026)
- [x] J-LockMove COMPLET : Move() en lock-on corrige, Rotation Rate -1, LastAxisX/Y (18/05/2026)
- [x] J-TestBed COMPLET : Lvl_TestBed BSP, BP_Enemy_TestBed, SFX placeholder (18/05/2026)
- [x] J-ComboFix COMPLET : ChoosenWeapon, InitComboTree, LevelMin=0 DT_Combo (18/05/2026)
- [x] C1-CollisionFix COMPLET : capsules Block, weapon collision audit (18/05/2026)
- [x] C1-HitFeel PARTIEL : knockback + screen shake VALIDES PIE, hitstop reporte, gamepad manque (18/05/2026)
- [x] C1-HitFlashEnemies ABANDONNE : Decision 21/05 -- voir Decisions.md
- [x] C1-CleanupDettes PARTIEL : 3/4 faits (21/05/2026) -- reste LockOnSwitchCooldown PC
- [x] C1-InputsUI COMPLET VALIDE PIE : IMC_Gameplay/Radial/Menu/Dialogue/Cutscene, swap IMC, fix rotation radial (23/05/2026)
- [x] C1-RadialMagie COMPLET VALIDE PIE : radial 2 niveaux Deity->Spell, CastSpell, fix bDefaultValueIsIgnored (25/05/2026)
- [x] C1-MagicProgressionDesign DESIGN VALIDE : boucle usage->niveau->points->arbre, structure arbre, gestion deites (25/05/2026)
- [x] C1-MagicDataLayer VALIDE PIE : E_SpellTier, E_NodeType, FSoM_TalentNode, FSoM_DeityData, DT_Deities, DT_TalentNodes, UnlockDeity + PopulateMagicSchools data-driven (25/05/2026)
- [x] DESIGN-MagicProgression : structure 4 paliers quetes deite, Corruption Magique, Fontaine de Fee, fee liee au heros (26/05/2026)
- [x] C1-MagicUnlockSystem COMPLET VALIDE PIE : IsDeityAccessible, LockDeity, IncrementSpellUsage courbe SoM, LevelUpSpell, AddTalentPoint, BP_SpellCategoryThresholds data-driven (27/05/2026)
- [x] RadialUnlock VALIDE PIE : bRadialUnlocked, blocage OpenRadial, blocage SwitchCategory Magic, BP_Debug_UnlockDeity (27/05/2026)

## Dettes techniques

- **Roll en lock-on** (C1-AnimationsPass1) -- voir Decisions.md
- **LockOnSwitchCooldown PC** (C1-CleanupDettes) : supprimer, pointer sur Component->SwitchCooldown
- **Rename ABP_Manny_Platforming -> ABP_Hero** (C1-AnimationsPass1)
- **WeaponClass hardcode BP_Enemy_Sword01** (C2-EnemyMesh)
- **Retopo hero 246K -> 10-15K** (ART-Hero)
- **Radial Armes : SelectedIndex = 0 a l'ouverture** (C1-RadialMagie) -- voir Decisions.md
- **UsageThreshold dans FSoM_SpellData** : a supprimer, remplace par BP_SpellCategoryThresholds

## Prochains jalons

1. **C1-CleanupDettes** : supprimer LockOnSwitchCooldown PC + UsageThreshold FSoM_SpellData
2. **Stats/Progression personnage** : caracteristiques, fourchette niveaux, formule degats
3. **C1-WeaponArchitecture** : audit data armes pour forge/talents
4. **Corruption Magique** : compteur, effets progressifs, lien SaveDesign
5. **C1-SwordMoveset** : moveset epee complet
6. **SaveDesign** : session design respawn/sauvegarde Fontaine de Fee
7. **Arbre de talents** : C1-MagicTreeModule -- cablage UnlockTreeNode + UI
8. **C2-SaveGame** : implementation apres spec SaveDesign validee
9. **Economie** : forge, monnaie narrative
10. **C1-BowPOC** : arc
11. **C1-WeaponSwitching** : switching armes en combat
12. **C1-SFXCombat** : sons combat de base
13. **Lore Deites** : ordre deblocage, structure rituel
14. **Lore Fee** : nom, personnalite, histoire
15. **C1-AnimationsPass1** : strafe distincts + roll sans root motion + rename ABP_Hero

## Sessions design a planifier

- **Session Lore Fee** : nom, personnalite, histoire, lien Ombre/Corruption
- **Session Lore Deites** : ordre deblocage, structure rituel par deite, cas Ondine
- **Session SaveDesign** : Fontaine de Fee detaillee, respawn, penalites mort
- **Session Economie** : forge, monnaie narrative, systeme de rattrapage magie
- **Session Stats/Progression personnage** : caracteristiques, fourchette de niveaux, formule degats

---

## Notes techniques importantes

- SetStatValue = unique point de modification stats
- ABP_Manny_Platforming = ABP du HERO (pas ABP_Unarmed)
- UpdateLockOnRotation dans PC = suivi camera vers cible V2 (conditionnel)
- Bind "On Lock on Activated/Deactivated" = dispatchers CUSTOM du Component
- SwitchCooldown = dans BP_CombatLockOnComponent UNIQUEMENT (pas dans PC)
- T3D export (clic droit -> Asset Actions -> Export) = meilleur outil d'audit
- add_state MCP dans AnimGraph = shell corrompu garanti -> toujours creer manuellement
- IA_Look est dans le PC (pas dans HeroCharacter) depuis J-Camera
- Move() en lock-on : utilise GetPlayerCameraManager -> GetCameraRotation (pas GetControlRotation)
- LastAxisX/LastAxisY : variables double sur HeroCharacter, SET au Triggered de IA_Move
- BP_Enemy_TestBed : pas de BT dedie, utilise BT_Enemy_Base via BP_AIController_Enemy_Base
- InitComboTree(WeaponID, WeaponLevel) : appele par EquipWeapon, charge ComboStepMap
- LevelMin = 0 dans DT_Combo = niveau de base (pas 1)
- HandleAttack n'a plus de parametre ChoosenWeapon -- le ComboManager lit CurrentWeaponID en interne
- SwitchCategory : toggle ERadialMode, recharge slots, reset SelectedIndex/TargetRotation/CurrentRotation
- SwitchCategory vers Magic : bloque si UnlockedSpells.Num() == 0
- OpenRadial dans PC : bloque si bRadialUnlocked == false sur HeroCharacter
- bRadialUnlocked = flag narratif UNIQUE pour l'ouverture radial (pas de check mecanique DiscoveredWeapons)
- UnlockDeity : utiliser "Set Members in FSoM_DeitySpells" et NON "Make FSoM_DeitySpells" (bDefaultValueIsIgnored=True sur Make)
- UnlockDeity Map_Contains : TRUE = deja present -> return, FALSE = absent -> debloquer (logique contre-intuitive, source de bug)
- UnlockDeity hardcode dans BeginPlay HeroCharacter : SUPPRIME -- deblocage via evenement narratif uniquement
- search_nodes("UnlockDeity") MCP trouve 0 resultats car le noeud s'appelle "Unlock Deity" (avec espace)
- IsDeityAccessible = Contains(UnlockedSpells) AND NOT Contains(LockedDeities) -- deux conditions independantes
- LockDeity(DeityID) : AddUnique(LockedDeities) -- deite visible dans radial mais non castable
- IncrementSpellUsage -> EffectiveThreshold = BaseThreshold / Max(1, 9-CurrentSpellLevel) -> LevelUpSpell
- BP_SpellCategoryThresholds : TMap<E_SpellCategory, int> keyed par enum, acces via GetClassDefaults
- Seuils categories : Attack=150, Heal=100, Buff=50, Debuff=35, Ultime=200 (Buff/Debuff montent vite)
- DT_Deities BaseSpells : ordre fixe [0=Attack, 1=Heal, 2=Buff, 3=Debuff] pour toutes les deites
- Athanor = Salamandre : meme deite, deux noms selon localisation
- Corruption Magique : compteur dedie sur le heros, effets progressifs par seuil, purge a la Fontaine de Fee
- Fontaine de Fee = feu de camp DS : repos -> purge Corruption + fee restauree + mobs respawn
- Pour les POURQUOI des decisions : voir Docs/Architecture/Decisions.md
- Pour le design progression magique : voir Docs/Architecture/Magic_Progression.md
- Pour le lore complet : voir Docs/Lore_ShadowOfMana.md

---

## Comment demarrer une session

### Session claude.ai
1. Nico dit : "on travaille sur SoM, lis le CLAUDE.md et le journal"
2. Claude.ai lit CLAUDE.md + Journal_Modifications.md via GitHub MCP
3. Claude.ai fait un resume de l'etat actuel et propose la suite

### Session UnrealClaude (editeur)
1. Ouvrir Tools -> Claude Assistant -> NOUVELLE session
2. Commencer par : "CONTEXTE : Tu es l'assistant UnrealClaude lance dans UE5.7 depuis 'Tools => Claude Assistant', tu as acces a 28 MCP Tools."
3. Agent en mode DISCOVERY UNIQUEMENT -- pas de blueprint_modify

---

*Derniere mise a jour : 27/05/2026*
