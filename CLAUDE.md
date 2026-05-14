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
  - Claude Code CLI v2.1.138 (`npm install -g @anthropic-ai/claude-code`)
  - Authentification via `claude auth login` (compte Anthropic Pro -- pas d'API key separee)
  - MCP bridge Node.js port 3000 (auto-start au lancement editeur)
  - 28 outils MCP natifs : Blueprint, AnimBlueprint, Enhanced Input, Material, Actor, Level, Asset...
  - Panel : Tools -> Claude Assistant dans l'editeur UE5.7
- **GitHub MCP** : node.exe --use-system-ca + NODE_TLS_REJECT_UNAUTHORIZED=0
  - Token Classic scope `repo` complet
- **Claude** : plan Pro, memoire activee

### Notes installation (pour reference)
- Compilation depuis sources obligatoire (pas de binaires precompiles)
- RunUAT.bat BuildPlugin avec -MaxParallelActions=2 (limite RAM sur cette machine)
- npm install dans Resources/mcp-bridge apres copie dans Plugins/
- Validation : `curl http://localhost:3000/mcp/status`

---

## Workflow dual-agent

Ce projet utilise deux instances Claude complementaires qui ne se voient pas en temps reel.
Ce fichier (CLAUDE.md) est le point de synchronisation central entre les deux.

### Roles

**Claude.ai (chef de projet)**
- Lit le repo via GitHub MCP au debut de chaque session
- Planification, decisions d'architecture, roadmap
- Met a jour Journal_Modifications.md et CLAUDE.md apres chaque jalon
- Lit Session_UnrealClaude.md pour rester au courant de ce que l'agent UE a fait

**Agent UnrealClaude (bras droit dans l'editeur)**
- Modifications Blueprint directes (variables, nodes, connections, materials)
- Queries temps reel sur assets, acteurs, niveaux
- Logue systematiquement ses actions dans Docs/Session_UnrealClaude.md
- Lit CLAUDE.md au demarrage pour connaitre l'architecture et les conventions

### Regles de synchronisation

1. **Nico pushe toujours en premier**, Claude.ai committe la doc ensuite (jamais l'inverse)
2. **L'agent UE logue ses actions** dans Docs/Session_UnrealClaude.md en temps reel
3. **Claude.ai lit Session_UnrealClaude.md** en debut de session pour rattraper ce qui a ete fait dans UE
4. **Apres chaque jalon significatif** : Nico push -> Claude.ai met a jour Journal + CLAUDE.md

### Deroulement type d'une session

```
DEBUT DE SESSION :
1. Nico ouvre claude.ai
2. Nico dit "on travaille sur SoM, lis le CLAUDE.md et le journal"
3. Claude.ai lit CLAUDE.md + Journal_Modifications.md + Session_UnrealClaude.md
4. Claude.ai fait un resume complet et propose la suite

PENDANT LA SESSION :
5. Nico ouvre UE5.7 + panel Claude Assistant
6. Agent UE travaille sur les Blueprints, logue dans Session_UnrealClaude.md
7. Claude.ai reste disponible pour decisions d'archi et questions

FIN DE JALON :
8. Nico : git add . && git commit -m "..." && git push
9. Claude.ai : met a jour Journal_Modifications.md + CLAUDE.md via GitHub MCP
```

---

## Instructions pour l'agent UnrealClaude

**A lire et appliquer des le debut de chaque session dans l'editeur.**

### IMPORTANT -- Ligne de contexte obligatoire dans chaque prompt

Chaque prompt envoye a l'agent UnrealClaude DOIT commencer par cette ligne :

```
CONTEXTE : Tu es l'assistant UnrealClaude lance dans UE5.7 depuis "Tools => Claude Assistant", tu as acces a 28 MCP Tools.
```

**Pourquoi c'est critique** : sans cette ligne, l'agent peut se croire dans Claude Code CLI
(terminal) et ne pas utiliser ses outils MCP natifs (blueprint_query, blueprint_modify, etc.).
Cette ligne lui confirme son contexte d'execution et l'oblige a utiliser les bons outils.

**Exemple de prompt correct** :
```
CONTEXTE : Tu es l'assistant UnrealClaude lance dans UE5.7 depuis "Tools => Claude Assistant", tu as acces a 28 MCP Tools.

Lis CLAUDE.md pour le contexte du projet.
REGLE : blueprint_query et blueprint_modify UNIQUEMENT. Jamais execute_script.

[... suite du prompt ...]
```

### Logging obligatoire

Apres chaque modification significative, tu dois ecrire dans `Docs/Session_UnrealClaude.md`.
Utilise l'outil Write/Edit pour maintenir ce fichier a jour en temps reel.

Format d'entree a respecter :

```
### [DATE] -- [NOM DU BLUEPRINT / ASSET]
**Action** : ce qui a ete fait (ajout variable, nouveau node, connexion, etc.)
**Pourquoi** : raison ou contexte
**Points d'attention** : gotchas, dependances, ce qui pourrait casser
```

### Conventions architecture a respecter (IMPERATIVES)

- `SetStatValue(StatName, Value)` = UNIQUE point de modification des stats. Jamais de SET direct.
- `OnStatChanged` = dispatcher de notification, tous les abonnes (HUD, ennemis) passent par lui
- Nommage stats : sans espace, CamelCase (HealthCurrent, StaminaMax, etc.)
- `BP_SoM_GameMode` : toujours verifier que Player Controller Class = BP_PlatformingPlayerController
- Hit Flash ennemi : utiliser Dynamic Material Instance au BeginPlay, pas Set Scalar on Materials
- Inputs : source unique Content/Input/InputActions/, ne jamais creer de doublons

### Ce que Claude.ai sait et toi non (en temps reel)

Claude.ai a acces a l'historique complet des sessions via GitHub.
Toi tu as acces a l'editeur en temps reel.
Le fichier Session_UnrealClaude.md est le pont entre vous deux.
Maintiens-le scrupuleusement : Claude.ai s'en sert pour etre au courant de tout ce que tu fais.

---

## Conventions de travail

### Git
```
git add .
git commit -m "description courte et coherente"
git push
```
-> Nico pushe d'abord, puis Claude.ai committe le journal via GitHub MCP
-> Claude.ai fournit systematiquement les commandes git + phrase de commit a chaque jalon

### Journal
- Fichier : `Docs/Journal_Modifications.md`
- Claude.ai le met a jour apres chaque jalon via GitHub MCP
- SHA recupere dynamiquement avant chaque commit

### Session UnrealClaude
- Fichier : `Docs/Session_UnrealClaude.md`
- L'agent UE le met a jour en temps reel pendant ses interventions
- Claude.ai le lit en debut de session pour rattraper le contexte

### Documentation architecture
- Toute nouvelle feature -> doc dans `Docs/Architecture/`
- Index : `Docs/Project_Architecture_Index.md`
- UI/HUD/Menu global : `Docs/Architecture/UI_GlobalMenu.md`

---

## Architecture cle (resume)

### Personnage
- `BP_PlatformingCharacter` (Blueprint Only)
- Stats via `BP_AttributeSet_Base` (ref : `AttributeSetRef`)
- `bIsDead` (private) + `IsDead()` (public pure)
- `bIsInvincible` (iframes dash/roll, pilote par AnimNotify AN_EndDash/AN_EndRoll)
- `OnPlayerDeath` dispatcher (sans params)
- `OnStatChanged(StatName, NewValue)` dispatcher dans AttributeSet
- `DiscoveredWeapons` (Array<FName>) : liste des armes debloquees (source de verite dans PC)

### Hero 3D -- DESIGN VALIDE (14/05/2026)
- Design valide via workflow : Dessin -> Leonardo.ai -> Gemini -> Meshy 5 -> AccuRIG -> UE5
- Palette actee : cheveux brun, echarpe rouge, armure gris anthracite, veste bleu nuit, pantalon marron sombre, bottes+gants noirs
- Assets dans : Content/Characters/Players/Hero_Test/
  - Skeletal Mesh : Meshy_AI_Crimson_Scarf_Adventu_0513214252_texture
  - Material Instance + Textures PBR (Diffuse + Normal)
  - Physics Asset + Skeleton avec IK (ik_foot, ik_hand, pelvis, spine x4)
- Retargeting VALIDE PIE : Mannequin source -> Hero target (ABP_Manny reutilise via Compatible Skeletons)
- ⚠️ 246K triangles LOD0 -> retopo necessaire avant prod (cible 10-15K)
- ⚠️ 6 doigts par main (artefact Meshy) -> correction Blender en J-ART final
- Armes : assets SEPARES du mesh hero (switch armes = BP_Weapon_Base, pas skinne)

### Stats
- `SetStatValue(StatName, Value)` = unique point de modification (jamais de SET direct)
- Nommage sans espace : HealthCurrent, HealthMax, StaminaCurrent, StaminaMax, ManaCurrent, ManaMax...
- `OnStatChanged` notifie tous les abonnes (HUD, futurs ennemis/boss)

### GameMode / Controllers
- `BP_SoM_GameMode` (`/Game/Core/`) -- Player Controller Class = BP_PlatformingPlayerController
- `BP_PlatformingPlayerController` : gere Lock-On, Radial Menu, Quickslots, IMC_Prototype
- ⚠️ Toujours verifier Player Controller Class dans BP_SoM_GameMode apres toute refonte

### Ennemis
- `BP_EnemyBase` -> `BP_AIController_Enemy_Base`
- Behavior Tree + Blackboard + PawnSensing
- `LoseAggro()` pour desengagement
- ⚠️ Lock-On : a revoir (J-lock) -- detection nouvelles cibles + UI z-order

### Combat
- `BPI_TakeDamage` + `BP_ComboManagerComponent`
- ReceiveDamage : bIsInvincible? -> IsDead? -> SetStatValue("HealthCurrent") -> HitFlash -> mort?
- Feedback combo : subtil, dans le monde (flash arme, posture) -- PAS d'UI visible (ACTE)
- ⚠️ Logique combo/armes dans PC EventGraph supprimee (J-Nettoyage) -- a refaire en J-15/16/17

### Armes
- `DT_Weapons` : 2 entrees (Sword_01, 2HSword_01), struct FWeaponData
- `BP_Weapon_Base` : spawn data-driven via GetDataTableRowFromName au BeginPlay
- `EquipWeapon(RowName)` dans BP_PlatformingCharacter
- ⚠️ Refonte armes prevue J-15/16/17 (BP_WeaponType_Base par TYPE)
- ⚠️ DiscoveredWeapons : present dans PC (source verite) ET dans Character -- a unifier J-15/16/17

### Mapping Gamepad PS5 (ACTE)
```
X=Saut  Carre=Esquive  Rond=Blocage  Triangle=Radial
L1=Attaque legere  R1=Attaque forte
L2=Action PNJ compagnon 1  R2=Action PNJ compagnon 2
L3=Sprint  R3=Lock-On (axis=changer cible)
Fleche Haut/Gauche/Droite=Quickslots 1/2/3
Fleche Bas=Switch page quickslots
Options=Menu Global  Touchpad=TBD
```

### UI / HUD
- `UI_HUD_Main` : event-driven via OnStatChanged, zero polling -- FINALISE
  - Layout : SizeBox_Weapon (64x64) + HUD_Main_VertBox (HP/ST/MP/XP)
  - UpdateStatText(Current, Max, RichTextBlock) : affiche "X / Y" sans decimales
  - DT_HUD_RichTextStyle : Content/UI/Widgets/Main/
- Design UI complet : voir `Docs/Architecture/UI_GlobalMenu.md`

### Radial Menu -- J-13 COMPLET + J-Nettoyage PROPRE
- Chemin assets : Content/UI/Widgets/RadialMenu/
- Assets actifs : ERadialMode, FSoM_RadialSlotData, UI_Radial_Main, UI_RadialSlot
- Assets supprimes : UI_RadialMenu (ancien), UI_RadialSlot_old
- `ERadialMode` : enum Weapons / Magic
- `FSoM_RadialSlotData` : struct SlotID, DisplayName, Description, Icon, Category, StatA/B/C
- `UI_RadialSlot` : widget 80x80, SetSelected(bool) + SetSlotData(FSoM_RadialSlotData)
- `UI_Radial_Main` : widget radial principal -- VALIDE PIE
  - RadialRadius=330, RadialContainer Size=0.01x0.01 (fix drift)
  - GenerateSlots() : Cos/Sin positioning
  - UpdateCenterInfo() : textes centre depuis SlotDataList[SelectedIndex]
  - UpdateSelection(AxisValue) : cran par cran, accumulation TargetRotation, wrap
  - Event Tick : FInterpTo lerp + SetRenderTransformAngle + contre-rotation icones
  - PopulateWeaponSlots() : DiscoveredWeapons -> DT_Weapons -> FSoM_RadialSlotData
  - SwitchCategory() : toggle Weapons/Magic + reset rotations
  - ValidateSelectedWeapon() : SlotID -> EquipWeapon -> CloseRadialMenu
- `BP_PlatformingPlayerController` :
  - Open/CloseRadialMenu, Handle_Rotate, Handle_ChangeCat
  - IA_validate_radial_selection, IA_UI_Radial_Cancel
  - IsValid(RadialMainRef) guard OBLIGATOIRE avant tout appel radial
  - Ancien systeme UI_RadialMenu entierement supprime (J-Nettoyage)

### Quickslots -- POC VALIDE
- Variables dans PC : QuickslotUp/Left/Right (FName = SpellID)
- IA_Quickslot_Up/Left/Right -> CastSpell(MagicComponent)
- Mapping : Fleches ↑←→ gamepad / &, e accent, guillemet clavier
- Fleche bas = switch page (futur multi-pages)
- ⚠️ HUD quickslot (affichage icones) : a faire (non urgent, polish)

### Inputs (IMC_Prototype)
- Source unique : Content/Input/InputActions/
- ⚠️ Dette : creer IMC_UI dedie pour inputs menus (J-C)

### Magie
- `BP_MagicComponent` : UnlockedSpells, QuickslotSlots, SpellCooldowns, CastSpell
- `BP_SpellBase` + 4 sorts Lumina valides PIE (Heal, Attack, Buff, Debuff)
- `DT_Spells` + structs FSoM_SpellData / FSoM_DeitySpells
- Chemin assets : Content/Systems/Magic/

---

## Jalons completes

- [x] #1 a #9 : MCP, mort, stats, inputs, iframes, UI, hit flash, migration UE5.7, audit
- [x] J-10/11/12 : BP_MagicComponent complet
- [x] J-14 : BP_SpellBase + 4 sorts Lumina valides PIE
- [x] J-15 : UI_HUD_Main finalise
- [x] J-13 : Radial Menu complet + Quickslot POC VALIDE PIE
- [x] J-Nettoyage : Suppression ancien radial, WeaponDataTest, assets obsoletes
- [x] J-ART (partiel) : Design hero valide + mesh 3D importe UE5 + retargeting VALIDE PIE
- [x] J-MUS (exploration) : Workflow MP3->MIDI->Suno explore, prompt theme sombre etabli

## Prochains jalons (ordre de dependances)

1. J-TestBed : Mini zone + mini mob + SFX placeholder (PROCHAIN)
2. J-SFX1 : Sons de base
3. J-lock : Revision Lock-On
4. J-Camera : Camera & Feel
5. J-15/16/17 : Refonte armes + combo
6. J-C : IMC_UI dedie
7. J-F : SaveGame
8. J-18/19 : Arc + Switching
9. J-B/E : Animations + Hit Flash
10. J-EnemyArt/AI/Types : Ennemis complets

Sessions creatives intercalees : J-MAP / J-ART (retargeting + LODs) / J-MUS (theme principal)

---

## Workflows creatifs etablis (sessions J-ART / J-MUS)

### J-ART -- Workflow hero 3D
```
Dessin crayon
  -> Leonardo.ai (modele : Lucid Origin, guidance 8, 1024x1024)
  -> Gemini (vues complementaires : dos, profil, T-Pose)
  -> Meshy 5 (image-to-3D, single image T-Pose, style Cartoon)
  -> Texture Meshy (PBR depuis image reference Leonardo)
  -> AccuRIG (rig humanoid, meilleur que Mixamo pour stylise)
  -> Export FBX T-Pose
  -> Import UE5 (Skeletal Mesh, skeleton None, Use T0 As Ref Pose)
  -> Compatible Skeletons + RTG Mannequin source -> Hero target
```
Points critiques : T-Pose mains ouvertes obligatoire, bras ecartes du corps, pas d'arme sur le mesh

### J-MUS -- Workflow theme musical
```
Reference melodique (fredonnement personnel, pas audio protege)
  -> Suno.ai (gratuit 50 credits/jour, Upload Audio + Covers)
  -> Iterations par Remix (slider style + slider audio fidelity)
  -> Export MP3
  -> UE5 : Sound Cue ou MetaSound source
```
Prompt etabli : dark orchestral, 60 BPM, D minor, cello lead, no brass, sparse, desolate overworld

---

## Notes techniques importantes

- SetStatValue = unique point de modification stats (jamais de SET direct)
- RichTextBlock : necessite DataTable RichTextStyleRow assignee
- ProgressBar : toujours wrapper dans SizeBox
- To Text (Float) : Max/Min Fractional Digits = 0 pour supprimer decimales
- Time Dilation 0.2 ouverture radial, 1.0 fermeture
- Widget "Is Variable" obligatoire pour acceder depuis le graph
- Radial drift fix : RadialContainer Size = 0.01x0.01
- Radial wrap : (SelectedIndex + NbSlots) % NbSlots
- IsValid(RadialMainRef) guard obligatoire avant tout appel radial depuis PC
- EquipWeapon : BeginDeferredActorSpawnFromClass + K2_AttachToComponent HandGrip_R
- RTG retargeting : toujours Mannequin SOURCE, hero TARGET (pas l'inverse !)

---

## Comment demarrer une session claude.ai

1. Nico dit : "on travaille sur Shadow of Mana, lis le CLAUDE.md et le journal"
2. Claude.ai lit ce fichier + `Docs/Journal_Modifications.md` + `Docs/Session_UnrealClaude.md`
3. Claude.ai fait un resume complet et propose la suite logique

## Comment demarrer une session UnrealClaude (dans l'editeur)

1. Ouvrir Tools -> Claude Assistant
2. Ouvrir une NOUVELLE session (bouton New Conversation / icone +)
   ⚠️ Ne jamais continuer une session existante -- les outils MCP peuvent ne pas etre actifs
3. Toujours commencer le prompt par :
   "CONTEXTE : Tu es l'assistant UnrealClaude lance dans UE5.7 depuis 'Tools => Claude Assistant', tu as acces a 28 MCP Tools."
4. Puis ajouter : "Lis le CLAUDE.md du projet et logue tes actions dans Docs/Session_UnrealClaude.md"
5. L'agent lit le contexte, confirme les conventions, et commence a travailler

**Pourquoi la ligne CONTEXTE est obligatoire** : sans elle, l'agent peut se croire dans Claude Code CLI
et ne pas utiliser ses outils MCP natifs. Cette ligne lui confirme son environnement d'execution.

---

*Derniere mise a jour : 14/05/2026*
