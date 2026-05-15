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
- Mapping gamepad prevu : fleches haut gauche droite (bas = switch page futur)

#### Session design actee (13/05/2026)
- Mapping PS5 complet acte (voir Docs/Architecture/UI_GlobalMenu.md)
- Quickslot : 3 slots, multi-pages via fleche bas, choix strategique (4 sorts / 3 slots)
- Roadmap reorganisee par dependances + sessions creatives (J-MAP / J-ART / J-MUS)
- Lock-On : dette confirmee (J-lock entre J-13 et J-15)
- Arc : munitions illimitees ACTE

---

### 14/05/2026 -- Session creative J-MUS (exploration workflow)

#### Workflow MP3 -> MIDI -> transformation explore
- Basic Pitch (Spotify) : conversion MP3 -> MIDI validee, gratuit, navigateur
- AIVA.ai : teste pour transformation MIDI -> orchestration sombre -- resultats insuffisants
- Workflow retenu pour J-MUS futur :
  - Humming / fredonnement -> Suno (gratuit, 50 credits/jour)
  - Suno Covers : transformation style avec preservation melodique
  - Suno Remix : iterations plus sombre / autre instru par slider
  - Export MP3 -> import UE5 (Sound Cue / MetaSound)
- Prompt Suno etabli pour le theme overworld sombre (monde devaste, cordes graves, 60 BPM)
- Theme Seiken Densetsu 1 : source protegee, workflow via fredonnement personnel uniquement

---

### 14/05/2026 -- Session creative J-ART -- Hero PLACEHOLDER COMPLET

#### Workflow etabli et teste
- Dessin crayon (Nico)
- Leonardo.ai (cel-shaded, prompt optimise, seed fixe)
- Gemini (vues dos + profil + T-Pose mains ouvertes)
- Meshy 5 (image-to-3D, single image T-Pose)
- Texture Meshy (PBR depuis image reference Leonardo)
- AccuRIG (rig humanoid, meilleur que Mixamo)
- Export FBX T-Pose
- Import UE5.7 (Content/Characters/Players/Hero_Test/)
- IK Rig + RTG (Mannequin source -> Hero target)
- M_Hero_Body (material PBR + HitFlash)
- BP_PlatformingCharacter assigne -- VALIDE PIE

#### Design hero valide -- palette finale ACTEE
- Cheveux : brun fonce spiky asymetrique
- Echarpe : rouge cramoisi
- Armure : gris anthracite
- Veste : bleu nuit
- Pantalon : marron sombre
- Bottes + gants : noir
- Lanieres croisees en X : marron cuir
- Medaillon Mana : centre poitrine
- Pas d'arme sur le modele (switch armes = assets separes)

#### Assets crees -- Content/Characters/Players/Hero_Test/
- Skeletal Mesh : Meshy_AI_Crimson_Scarf_Adventu_0513214252_texture
- M_Hero_Body : material PBR propre (Diffuse + Normal + Roughness + Metallic + HitFlashAmount)
- Material_001 : Material Instance parent M_Hero_Body
- Textures : Material_001_Diffuse, Material_001_Normal + textures Meshy PBR
- Physics Asset : genere automatiquement
- Skeleton AccuRIG : IK propres (ik_foot, ik_hand, pelvis, spine x5)
- IKRig_Hero_Test : chaines auto-generees (Root, Spine, Neck, Head, bras, jambes, doigts)
- RTG_Hero_To_Mannequin : Mannequin source -> Hero AccuRIG target -- VALIDE

#### Retargeting -- VALIDE PIE
- Sens correct : Mannequin source, Hero target
- Toutes animations existantes jouent sur le hero : AM_Dash, AM_Roll, AM_Death, AM_Light/Heavy_Sword...
- Compatible Skeletons : hero compatible avec base_rigged_Skeleton
- ABP_Manny reutilise directement sans export animations

#### Sockets recrees sur skeleton hero
- HandGrip_R sur os hand_r -- placement a affiner
- HandGrip_L sur os hand_l -- placement a affiner

#### Lecons apprises workflow
- T-Pose mains ouvertes + bras ecartes OBLIGATOIRE
- Meshy single image > composite multi-vues en plan gratuit
- Meshy 5 : 6 doigts par main (artefact connu, a corriger en J-ART final)
- AccuRIG > Mixamo pour rig stylise
- RTG : toujours Mannequin SOURCE, hero TARGET (pas l'inverse !)
- Auto Create Retarget Chains > creation manuelle
- Compatible Skeletons = solution simple pour reutiliser ABP sans export animations
- FBXLegacyPhongSurface = parent par defaut a remplacer par M_Hero_Body

#### Dettes J-ART restantes (session dediee)
- 6 doigts -> 5 dans Blender
- Poly count : ~246K triangles LOD0 -> retopo (cible 10-15K)
- LODs (LOD1 : ~50K, LOD2 : ~15K)
- Placement sockets HandGrip_R/L a affiner
- Armes comme assets separes (Sword_01, 2HSword_01 en priorite)

---

### 14/05/2026 -- J-Nettoyage COMPLET

#### Suppressions effectuees

**BP_PlatformingCharacter**
- Variable `WeaponDataTest` (FWeaponData) supprimee -- vestige debug prototypage J-13

**BP_PlatformingPlayerController**
- Variables `RadialMenuRef` (UI_RadialMenu_C), `SlotRowNames`, `SlotIcons` supprimees
- Fonctions nettoyees : OpenRadialMenu, CloseRadialMenu, ToggleRadialMenu, ValidateSelectedWeapon
  - Ancien wiring vers UI_RadialMenu retire
  - Logique combo/armes dans EventGraph retiree (sera refaite en J-15/16/17)
- Guard RadialMainRef (IsValid) desormais seul point d'entree radial

**Assets supprimes**
- `UI_RadialMenu` (Content/UI/Widgets/RadialMenu/) -- ancien widget radial remplace par UI_Radial_Main
- `UI_RadialSlot_old` (Content/UI/Widgets/RadialMenu/Slots/) -- ancienne version du slot
- `BP_PlatformingGameMode` -- remplace par BP_SoM_GameMode, aucune reference entrante
- `BP_test_IA` -- vestige debug IA, aucune reference utile

**Reorganisation dossier Enemies**
- Creation : Content/Characters/Enemies/Animations/
- Deplacement : AM_Enemy_Light_Sword_1, AN_Enemy_DisableCollision, AN_Enemy_EnableCollision -> Animations/
- Deplacement : SKM_Enemy_Sword_01 + Skeleton -> Model/
- Deplacement : BP_Enemy_Sword01 -> Blueprints/
- BP_enemyTest conserve (reference par Lvl_ThirdPerson, sera repris en J-EnemyArt)

**EWeaponType**
- NewEnumerator6 absent -- enum deja propre (Sword, HSword, Axe, HAxe, Dagger, Bow)

---

### 14/05/2026 -- Session design -- Roadmap globale refondee

#### Roadmap completement refaite (Docs/Roadmap_Gameplay.md)
- Ancienne roadmap : ~20 jalons, centree gameplay technique
- Nouvelle roadmap : ~50 jalons, 8 couches couvrant le projet complet
- Ajouts majeurs : J-TestBed, J-Camera, J-EnemyArt/AI/Types, J-Boss1
- J-MAP-1/2/3, J-Flammy, J-Transition (monde et navigation)
- J-Dialogue, J-Tuto, J-Deites, J-Corruption, J-ChoixMoral (narratif)
- J-Hub1/2/3, J-Compagnons1/2/3, J-Quetes, J-Lore, J-SoeurReveal
- J-Forge1/2, J-Equipement, J-Talent (forge et progression)
- J-SFX1/2/3, J-MUS-1/2/3, J-AudioMix (audio)
- J-MenuPrincipal/Options/Pause, J-DeathScreen, J-LoadingScreen, J-HUD-Polish, J-Loc (UI/UX)
- J-Debug, J-Acte1Test, J-Perf1/2, J-Crash, J-Build1/2 (qualite et build)

#### Decisions design actees
- Localisation : FR (principale) + EN des le debut -- StringTable obligatoire, pas de hardcode
- Tutoriel : hints contextuels minimalistes, premiers instants uniquement, desactivables
- Vibration : standard uniquement, pas de haptique DualSense avance
- Distribution : non decidee (Steam / itch.io / perso)
- Death screen : respawn sanctuaire (DS) ou checkpoint (Seiken/KH) -- point ouvert

#### Ordre de dependances revise
```
J-lock (Lock-On complet + Strafe animations)
  -> J-Camera
    -> J-TestBed (zone + mob + SFX)
      -> J-15/16/17...
```
Raison : le strafe et le lock sont la matiere necessaire avant de calibrer camera et mob de test

#### Lecons apprises -- workflow agent UnrealClaude
- Ligne contexte obligatoire : "CONTEXTE : Tu es l'assistant UnrealClaude lance dans UE5.7..."
- Agent UE = discovery/audit uniquement -- JAMAIS de creation d'assets AnimGraph via MCP
- add_state MCP produit des shells incomplets dans les State Machines -> noeud corrompu garanti
- Toute creation d'etat AnimGraph = manuelle dans l'editeur
- Facturation : authentification via claude.ai Pro (forfait mensuel), pas d'API key separee
- Le cout affiche ($x.xx) dans le panel = estimation indicative, pas une vraie facturation

---

### 14/05/2026 -- Preparation J-lock -- Audit animations

#### Audit ABP_Unarmed (resultat)
- `Strafe` (double) : calcule chaque frame via DotProduct(Normalize(Velocity), GetActorRightVector)
- `Can Strafe` (bool) : NOT bOrientRotationToMovement -- toggle automatique correct
- `BS_Unarmed_Strafe` : cree manuellement (Content/Characters/Mannequins/Anims/Unarmed/)
  - Axes : Forward [-1,1] x Strafe [-1,1]
  - Points : MM_Idle(0,0), Jog_Fwd(1,0), Jog_Bwd(-1,0), Jog_Right(0,1), Jog_Left(0,-1)
- Etat `LockedOn_Strafe` cree dans State Machine Locomotion d'ABP_Unarmed
  - ⚠️ Strafe non fonctionnel -- calcul Can Strafe au BeginPlay uniquement (pas Update Animation)
  - ⚠️ A reprendre dans J-lock manuellement sans agent

#### Ce qui manque pour J-lock (a faire manuellement)
1. Calcul `Can Strafe` dans **Update Animation** (pas BeginPlay) -- critique
2. `bOrientRotationToMovement = false` dans OnLockOnActivated (BP_PlatformingCharacter)
3. `Use Controller Rotation Yaw = true` dans OnLockOnActivated
4. Audit complet BP_CombatLockOnComponent avant de decider refonte ou conservation
5. Fix detection nouvelles cibles, z-order indicateur, barres HP ennemis

#### Lecon apprise -- PrintVar/PrintString
- Ne jamais supprimer un PrintString sans verifier que les pins d'execution sont rebranches
- Un lien d'execution coupe casse silencieusement toute la chaine sans erreur BP visible

---

## Rappel
Pour la roadmap detaillee : voir Docs/Roadmap_Gameplay.md
Pour le design UI/HUD/Menu : voir Docs/Architecture/UI_GlobalMenu.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 14/05/2026
