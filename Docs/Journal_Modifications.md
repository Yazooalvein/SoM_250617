# Journal des Modifications -- Shadow of Mana

## Objectif
Suivi precis de toutes les evolutions majeures du projet.

## Entrees

### 25/05/2026 -- Data layer deites + sortie mode dummy magie -- VALIDE PIE

#### Nouveaux assets data layer
- E_SpellTier (enum) : Base / TreeActive / TreeEvolution / Ultime
- E_NodeType (enum) : Active / Passive / Ultime
- FSoM_TalentNode (struct) : NodeID, DeityID, NodeType, SpellID, PassiveStat, PassiveValue, PointCost, Prerequisites
- FSoM_DeityData (struct) : DeityID, DeityName, Icon, UnlockOrder, BaseSpells
- FSoM_SpellData : SpellTier (E_SpellTier) + ReplacesSpellID (Name) ajoutes
- DT_Deities : row Lumina (UnlockOrder=1, BaseSpells=[Lumina_Attack, Lumina_Heal, Lumina_Buff, Lumina_Debuff], Icon placeholder)
- DT_TalentNodes : cree vide, pret pour C1-MagicTreeModule
- Convention BaseSpells : ordre fixe [0=Attack, 1=Heal, 2=Buff, 3=Debuff] pour toutes les deites

#### BP_MagicComponent -- UnlockDeity refactore
- Avant : TempSpellsIDs hardcode en default value -> mode dummy
- Apres : GetDataTableRow(DT_Deities, DeityName) -> BaseSpells -> Set Members in FSoM_DeitySpells
- TempSpellsIDs supprime
- Bug resolu : logique Map_Contains inversee (TRUE=deja present->return, FALSE=absent->debloquer)

#### UI_Radial_Main -- PopulateMagicSchools refactore
- Avant : Conv_NameToText(Map Key) -> DisplayName, Icon null
- Apres : GetDataTableRow(DT_Deities, Map Key) -> DeityData.DeityName + DeityData.Icon -> MakeStruct
- Icone deite reelle affichee dans le radial N1

#### Tests valides PIE
- Radial N1 (Deity) : icone Lumina affichee, DeityName = "Lumina"
- Radial N2 (Spell) : 4 sorts Lumina accessibles, CastSpell fonctionnel

#### Dettes
- Stub BeginPlay Lumina : toujours present, a retirer quand C1-MagicUnlockSystem opere en jeu

#### Etat final
Sortie du mode dummy magie. Data layer deites complet et data-driven. Prochain jalon : C1-MagicUnlockSystem.

---

### 25/05/2026 -- Session design + outils IA

#### C1-MagicProgressionDesign -- DESIGN VALIDE
- Boucle de progression arretee : usage sorts -> montee niveau -> points talent -> arbre de talent
- Structure par deite : 2-4 sorts de base immediats, arbre = 3-4 actifs + 2-3 passifs + 1 ulti
- Points insuffisants pour completer l'arbre -> choix force -> builds differents
- Evolution d'un sort de base : remplace le sort (pas de coexistence)
- Sorts supplementaires d'arbre : s'ajoutent au pool radial/quickslots
- Deites : aucun cout de switch, pas d'equipement, apparition immediate au deblocage
- Coherence avec niveaux armes : a calibrer selon duree de vie jeu
- Magic_System.md mis a jour : section Progression Magique ajoutee, BP_MagicComponent etendu
  (SpellUsageCounts, SpellLevels, TalentPoints, IncrementSpellUsage, LevelUpSpell, AddTalentPoint,
  UnlockTreeNode, OnSpellLevelUp), FSoM_SpellData : SpellTier + ReplacesSpellID ajoutes

#### Points ouverts (-> C1-MagicUnlockSystem)
- Seuils de montee en niveau (nb utilisations) : a calibrer
- Nombre exact de noeuds par arbre : depend duree de vie jeu
- Condition deblocage ulti : bout d'arbre par defaut, evolution possible
- Conditions deblocage deites : a definir (narratif / quete / zone)
- Ratio points max vs noeuds totaux : a calibrer

#### Skills SoM crees (outils IA)
- `Skills/som-session-start/SKILL.md` : protocole lecture CLAUDE.md + Journal en debut de session
- `Skills/som-commit-protocol/SKILL.md` : protocole SHA, confirmation, format journal, checklist
- Installes localement via Settings -> Customize -> Skills sur claude.ai

#### Etat final
C1-MagicProgressionDesign VALIDE. Prochain jalon : C1-MagicUnlockSystem.

---

### 23/05/2026 -- C1-InputsUI COMPLET -- VALIDE PIE

#### IMC crees
- IMC_Gameplay (ex IMC_Prototype renomme) : charge au ReceivePossessed dans BP_SoM_HeroCharacter
- IMC_Radial : 4 IA navigation radial
- IMC_Menu, IMC_Dialogue, IMC_Cutscene : stubs vides

#### Swap IMC cable dans BP_SoM_PlayerController
- OpenRadial (apres SET bShowMouseCursor=true) :
  GetSubsystemFromPC(Self) -> RemoveMappingContext(IMC_Gameplay) -> AddMappingContext(IMC_Radial, Priority=1)
- CloseRadial (avant RemoveFromParent) :
  GetSubsystemFromPC(Self) -> RemoveMappingContext(IMC_Radial) -> AddMappingContext(IMC_Gameplay, Priority=0)

#### Fix rotation radial
- Bug : rotations multiples et sens incorrect au premier test
- Cause : axe analogique continu sans threshold -> declenchements en rafale
- Fix 1 : ajout trigger Pressed avec threshold 0.5 sur IA_UI_Radial_Rotate
- Fix 2 : ajout Modifier Negate X sur le binding direction gauche (Q / Stick G X-)
  Sans Negate, les deux directions envoient la meme valeur positive -> meme sens

#### Tests valides PIE
- Triangle -> inputs gameplay morts, radial naviguable
- Rotation gauche/droite correcte avec 3 armes
- Rond -> fermeture, inputs gameplay reviennent
- Attaque pendant radial ouvert -> rien
- IA_UI_Radial_Open toujours fonctionnel depuis le gameplay

---

### 23/05/2026 -- Session design -- Architecture IMC complete
- 5 IMC decides (Gameplay/Radial/Menu/Dialogue/Cutscene)
- IMC_Dialogue = SEUL cumulatif, personnage mobile pendant dialogues
- Cinematiques = Level Sequence -> IMC_Cutscene pertinent
- Corrections noms IA (audit T3D), IA_UI_Radial_Rotate identifiee

---

### 21/05/2026 -- Session design & documentation
- C1-HitFlashEnemies ABANDONNE, C1-CleanupDettes 3/4, C1-InputsUI PRIORITAIRE
- Nouveau jalon C1-RadialMagie, Decisions.md cree, regles maintenance doc

---

### 19/05/2026 -- C1-HitFlashEnemies -- ARCHITECTURE COMPLETE
- Architecture DMI faite, blocage M_Mannequin identifie

---

### 18/05/2026 -- C1-HitFeel PARTIEL -- VALIDE PIE
- Knockback + screen shake valides, hitstop reporte, vibration gamepad manque

---

### 18/05/2026 -- C1-CollisionFix COMPLET -- VALIDE PIE
- CapsuleComponent Pawn=Block, weapon collision audit

---

### 18/05/2026 -- J-ComboFix COMPLET -- VALIDE PIE
- ChoosenWeapon, InitComboTree, HandleAttack sans parametre, LevelMin=0

---

### 18/05/2026 -- J-TestBed COMPLET -- VALIDE PIE
- Lvl_TestBed BSP, BP_Enemy_TestBed, SFX placeholder

---

### 18/05/2026 -- J-LockMove COMPLET -- VALIDE PIE
- Move() en lock-on via CameraRotation, Rotation Rate -1, LastAxisX/Y

---

### 17/05/2026 -- J-Camera COMPLET -- VALIDE PIE
- SpringArm regle, IA_Look dans PC, UpdateLockOnRotation V2, Screen Shake valide

---

### 15/05/2026 -- J-Renommage COMPLET
- Convention nommage unifiee, Fix Up Redirectors, VALIDE PIE

---

### 15/05/2026 -- J-lock COMPLET -- VALIDE PIE
- Fix IsLockOnActive, fix dispatcher espace, fix bind PC, UpdateLockOnUIIndicator
- ABP_Manny_Platforming Strafe VALIDE PIE, edge cases valides

---

### 14/05/2026 -- Session design -- Roadmap globale refondee
- ~50 jalons, 8 couches, projet complet de A a Z
- Decisions : FR+EN, tuto minimaliste, vibration standard
- Ordre revise : J-lock -> J-Camera -> J-TestBed -> J-15/16/17

---

### 14/05/2026 -- J-Nettoyage COMPLET
- BP_SoM_HeroCharacter : WeaponDataTest supprimee
- BP_SoM_PlayerController : RadialMenuRef, SlotRowNames, SlotIcons supprimes
- Assets : UI_RadialMenu, UI_RadialSlot_old, BP_PlatformingGameMode, BP_test_IA
- Reorganisation dossier Enemies (Animations/, Model/, Blueprints/)

---

### 14/05/2026 -- Session creative J-ART ; Hero PLACEHOLDER COMPLET
- Workflow valide : Dessin -> Leonardo.ai -> Gemini -> Meshy 5 -> AccuRIG -> UE5.7
- Design palette actee, retargeting VALIDE PIE (ABP_Manny reutilise via Compatible Skeletons)
- Dettes : 6 doigts, retopo 246K -> 10-15K, LODs, sockets HandGrip a affiner

---

### 14/05/2026 -- Session creative J-MUS (exploration workflow)
- Workflow : Fredonnement -> Suno (gratuit 50 credits/jour) -> Export MP3 -> UE5
- Prompt theme overworld sombre etabli (60 BPM, D minor, cello lead)

---

### 12-13/05/2026 -- Jalon J-13 COMPLET -- Radial Menu + Quickslot

#### Radial Menu (UI_Radial_Main) -- VALIDE PIE
- Navigation par cran (stick G/D), lerp fluide, wrap correct
- Fix drift (RadialContainer 0.01x0.01), fix sens rotation
- PopulateWeaponSlots, SwitchCategory, ValidateSelectedWeapon -- VALIDES PIE

#### Quickslot POC -- VALIDE PIE
- 3 variables dans PC : QuickslotUp/Left/Right (FName, SpellID)
- IA_Quickslot_Up/Left/Right -> CastSpell via MagicComponent

---

### 12/05/2026 -- Jalon J-15 -- UI_HUD_Main FINALISE
- SizeBox_Weapon (64x64) + HUD_Main_VertBox (HP/ST/MP/XP)
- RichTextBlock HP/ST/MP + UpdateStatText + DT_HUD_RichTextStyle

### 12/05/2026 -- Jalons J-10 a J-14 -- POC Systeme Magie VALIDE

#### Structure assets (Content/Systems/Magic/)
- BP_MagicComponent, BP_SpellBase
- E_SpellCategory, E_SpellTarget, E_DeliveryType, FSoM_SpellData, FSoM_DeitySpells, DT_Spells
- BP_Spell_Heal, BP_Spell_Attack, BP_Spell_Buff, BP_Spell_Debuff (Lumina) -- VALIDES PIE

#### BP_MagicComponent
- UnlockedSpells, QuickslotSlots, SpellCooldowns, bIsCasting
- CastSpell : Switch E_SpellTarget -> SpawnActor -> Execute -> ConsumeMana -> cooldown

### 11/05/2026 -- Session design
- Lore : Docs/Lore_ShadowOfMana.md
- Roadmap : Docs/Roadmap_Gameplay.md
- Architecture magie : Docs/Architecture/Magic_System.md

### 11/05/2026 -- Jalon #9 -- Audit complet + nettoyage
- Fixes config (DefaultGame.ini, uproject, ProjectName)
- Nettoyage : ThirdPerson/, IA debug, Lvl_Platforming GameMode Override

### 11/05/2026 -- Jalon #8 -- Migration UE5.7 + UnrealClaude
- Projet migre UE5.6 -> UE5.7.4
- UnrealClaude v1.4.5 : 28 outils MCP, panel operationnel
- Workflow dual-agent mis en place (Docs/Session_UnrealClaude.md)

### 07/05/2026 -- Jalons #1 a #7
- #1 : MCP + Hit Flash joueur (M_Hero HitFlashAmount)
- #2 : Mort du joueur (bIsDead, OnPlayerDeath, LoseAggro)
- #3 : OnStatChanged dispatcher (SetStatValue = unique point)
- #4 : Unification inputs (source unique InputActions/)
- #5 : Iframes dash/roll (bIsInvincible via AnimNotify)
- #6 : UI event-driven (zero polling, OnStatChanged)
- #7 : Hit Flash ennemi partiel + fix GameMode PlayerController

### 20/07/2025 -- Nico
- Animation Weapon Integration

### 27/06/2025 -- Nico
- BP_AIController_Enemy_Base, PawnSensing, aggro/perte

### 26/06/2025 -- Nico
- BPI_TakeDamage, BP_Enemy_Base ReceiveDamage + OnDeath

### 24/06/2025 -- Nico
- Systeme armes data-driven, Menu Radial data-driven, Combo multi-armes

### 21/06/2025 -- Nico
- Refactorisation BP_ComboManagerComponent (TMap, fenetre dynamique)

### 19-20/06/2025 -- Nico
- Lock-On, Menu Radial, refonte Combo

### 18/06/2025 -- Nico
- Refactoring pipeline Gameplay de base (Dash, Roll, Jump, Stamina)

### 17/06/2025 -- Nico -- Creation du projet
- Initialisation SoM sous UE5.6, template Third Person Platforming

---

## Rappel
Pour la roadmap detaillee : voir Docs/Roadmap_Gameplay.md
Pour les decisions architecturales : voir Docs/Architecture/Decisions.md
Pour les inputs et IMC : voir Docs/Architecture/Input_Architecture.md
Pour le radial menu : voir Docs/Architecture/RadialMenu_Architecture.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 25/05/2026
