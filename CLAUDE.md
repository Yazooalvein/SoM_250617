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

| Fichier | Quand le mettre a jour |
|---|---|
| `CLAUDE.md` | A chaque session : jalons, dettes, notes techniques, ordre jalons |
| `Docs/Journal_Modifications.md` | A chaque session : entree datee avec ce qui a ete fait |
| `Docs/Roadmap_Gameplay.md` | Quand un jalon change de statut ou qu'un nouveau jalon est cree |
| `Docs/Architecture/Decisions.md` | A chaque decision importante (abandon, choix archi, gotcha) |
| `Docs/Architecture/Stats_Progression.md` | Quand les stats ou la progression changent |
| `Docs/Architecture/Combat_StatusEffects.md` | Quand les effets de statut ou la Corruption changent |
| `Docs/Architecture/Economy_Drops.md` | Quand l'economie, les drops ou les consommables changent |
| `Docs/Architecture/Input_Architecture.md` | Quand les inputs ou IMC changent |
| `Docs/Architecture/RadialMenu_Architecture.md` | Quand le radial menu evolue |
| `Docs/Project_Architecture_Index.md` | Quand un nouveau fichier doc est cree |

### Fichier decisions -- IMPORTANT
`Docs/Architecture/Decisions.md` centralise toutes les decisions architecturales importantes.
Objectif : retrouver en 30 secondes POURQUOI une chose a ete faite, sans fouiller le journal.

---

## Instructions pour l'agent UnrealClaude

### Ligne de contexte OBLIGATOIRE dans chaque prompt
```
CONTEXTE : Tu es l'assistant UnrealClaude lance dans UE5.7 depuis "Tools => Claude Assistant", tu as acces a 28 MCP Tools.
```

### Regles agent
- blueprint_query UNIQUEMENT. Jamais blueprint_modify, jamais execute_script.
- JAMAIS creer d'assets AnimGraph via MCP (add_state produit des shells corrompus)
- Agent = discovery/audit uniquement. Ouvrir une NOUVELLE session a chaque fois.

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
- NOTE : ChoosenWeapon (HC) et CurrentWeaponID (ComboManager) sont redondants -- a unifier en C1-WeaponArchitecture

### Stats heros -- DESIGN VALIDE (28/05/2026)
- 7 stats : Vitalite, Attaque, Defense, Magie, Resistance, Endurance, Vitesse
- Stats supplementaires cles BP_AttributeSet_Base : "Level", "EssenceMana", "EssenceManaDropped", "PiecesOr", "ChanceCritique", "Corruption", "ManaMax", "ManaCurrent"
- Progression hybride : niveaux globaux 1-10 (stats auto + 2 points libres) + progression par usage armes/magie
- Essence de Mana : ressource progression (niveaux + deites) -- perdue a la mort, recuperable DS-like
- Pieces d'Or (PO) : ressource economie (marchands) -- jamais perdues
- Formule physique : Max(1, (Attaque * CoeffArme * CoeffCritique) - (Defense * 0.5))
- Formule magique : Max(1, (Magie * CoeffSort * CoeffCritique) - (Resistance * 0.5))
- Elementaire : * (1 - ResistanceElementaire[Element]) -- TMap<EElement, float>, 8 elements / 8 deites
- Critique : 5% de base, x1.5, heros ET ennemis
- Stamina : -10 legere, -20 lourde, -25 esquive, -5/s sprint -- recuperation auto 1s
- ManaMax separee de Magie : base 60, +8/niveau -- pas de regen auto
- Cout sorts : Base + (NiveauSort * Multiplicateur) -- voir Economy_Drops.md
- Equipement : 3 slots (Casque, Armure, Accessoire) -- Defense + Resistance uniquement
- Pas de regen PV auto
- Voir Docs/Architecture/Stats_Progression.md pour spec complete

### Stats ennemis -- DESIGN VALIDE (28/05/2026)
- Systeme simplifie dedie : PV, Attaque, Defense, Resistance, Vitesse, VitesseAttaque, TenaciteEtat
- ResistanceElementaire : TMap<EElement, float> comme le heros
- A ajouter sur BP_Enemy_Base lors de C1-WeaponArchitecture ou C2-EnemyTypes

### Effets de statut -- DESIGN VALIDE (28/05/2026)
- 8 effets signatures un par deite (Eblouissement, Sommeil, Malediction, Desequilibre, Alourdi, Brulure, Gele, Empoisonne)
- Heros ET ennemis peuvent subir les effets
- BP_StatusEffectComponent a creer en C1-SwordMoveset
- Voir Docs/Architecture/Combat_StatusEffects.md pour spec complete

### Corruption Magique -- DESIGN VALIDE (28/05/2026)
- Phase 1 (debut jeu) : plafond 50, effets limites (aura + resistances)
- Phase 2 (apres revelation Hero/Ombre) : plafond 100, faiblesse = deite la plus utilisee au franchissement 75, effet statut = meme deite a 100
- Bonus Essence ennemis : x1.0 / x1.15 / x1.35 / x1.60 / x1.60 (plafond)
- Purge Fontaine : si >=75 fee epuisee (pas de montee deite) ; si 100 fee gronde
- Voir Docs/Architecture/Combat_StatusEffects.md pour spec complete

### Economie & Drops -- DESIGN VALIDE (28/05/2026)
- Double monnaie : Essence (perdue a la mort) + PO (stable)
- Drops ennemis : Essence + PO toujours, consommables + materiaux + coffres Seiken en aleatoire
- Consommables style Seiken : Bonbon/Noix/Miel/Plante/Herbe/Essence Purifiee/Repas -- 9 unites max par type
- Materiaux forge : 3 tiers (Graine/Cristal/Essence Cristallisee) -- non lies aux elements
- Forge narrative : upgrade N+1 debloque par jalon narratif + materiaux requis
- Respawn : ennemis normaux oui, boss jamais
- Sauvegarde : tout sauf Essence non depensee
- Voir Docs/Architecture/Economy_Drops.md pour spec complete

### Hero 3D
- ABP actif : **ABP_Manny_Platforming** (pas ABP_Unarmed qui est pour les ennemis)
- Mesh : Meshy_AI_Crimson_Scarf_Adventu_0513214252_texture (Content/Characters/Players/Hero_Test/)
- Retargeting : Mannequin source -> Hero target (Compatible Skeletons)
- Rotation Rate Z = -1 (pivot instantane hors lock-on)
- Variables LastAxisX, LastAxisY (double) : stockees au Triggered de IA_Move
- 246K triangles LOD0 -> retopo (cible 10-15K) -- ART-Hero

### Camera -- J-Camera COMPLET VALIDE PIE (17/05/2026)
- SpringArm : Target Arm Length 350, Socket Offset Z 60, Camera Lag Speed 8
- CS_HitReceived + CS_EnemyDeath dans Content/Systems/Camera/
- IA_Look dans PC -- UpdateLockOnRotation V2 (conditionnel, guard IsRolling)

### LockMove COMPLET VALIDE PIE (18/05/2026)
- Move() en lock-on : GetPlayerCameraManager -> GetCameraRotation (pas GetControlRotation)
- Rotation Rate Z = -1 hors lock-on

### Lock-On -- COMPLET VALIDE PIE (15/05/2026)
- BP_CombatLockOnComponent sur le Character
- SwitchCooldown = source de verite UNIQUE dans le Component
- Strafe VALIDE PIE : BS_Unarmed_Strafe (Forward x Strafe [-1,1])

### Ennemis
- `BP_Enemy_Base` : bCanBeLocked, bIsDead, OnDeath, bIsLocked, bIsAttacking, bHasAlreadyHit
  - WeaponClass hardcode BP_Enemy_Sword01 -- a generaliser C2-EnemyMesh
  - Stats a ajouter : Attaque, Defense, Resistance, Vitesse, VitesseAttaque, TenaciteEtat, ResistanceElementaire
- `BP_Enemy_TestBed` : stats Instance Editable, utilise BT_Enemy_Base
- ABP_Unarmed : pour les ENNEMIS SANS ARME (pas le hero)

### TestBed -- COMPLET VALIDE PIE (18/05/2026)
- Map : Content/Maps/Lvl_TestBed -- sol BSP, NavMesh, Lighting Movable, GameMode Override
- BP_Debug_UnlockDeity : Overlap -> UnlockDeity("Lumina") + SET bRadialUnlocked=true

### Combat -- ComboFix VALIDE PIE (18/05/2026)
- BP_ComboManagerComponent : TMap<Name, FComboStep>, CurrentWeaponID, InitComboTree, HandleAttack, CanAttack
- Flow attaque : IA_Attack -> Branch(CanAttack) -> HandleAttack(AttackType) -> PlayAttackMontage
- Flow equipement : EquipWeapon -> SET ChoosenWeapon -> AddUnique(DiscoveredWeapons) -> InitComboTree

### Armes
- FWeaponData : Name, Type, Level, Mesh, Stats, Socket, BP_Weapon, icons, DT_Combo, IdleAnim
- A ajouter en C1-WeaponArchitecture : CoeffArme (float), VitesseAttaque (float)
- VitesseAttaque : multiplicateur PlayRate montage -- Epee1M=1.2, Epee2H=0.75, Arc=1.0, Hache=0.6
- DETTE : ChoosenWeapon (HC) redondant avec CurrentWeaponID (ComboManager) -- C1-WeaponArchitecture

### GameMode / Controllers
- BP_SoM_GameMode : Player Controller Class = BP_SoM_PlayerController
- BP_SoM_PlayerController : PlayerCharacterRef au OnPossess, Lock-On, Aim, OpenRadial

### Radial Menu -- COMPLET VALIDE PIE
- ERadialMode : Weapons / Magic -- SwitchCategory, ValidateRadial
- Radial Magie 2 niveaux : N1 Deity -> N2 Spell -> CastSpell
- Deblocage narratif : bRadialUnlocked (Hero) + UnlockDeity()
- Voir Docs/Architecture/RadialMenu_Architecture.md

### Magie -- C1-MagicUnlockSystem VALIDE PIE (27/05/2026)
- BP_MagicComponent : UnlockedSpells, LockedDeities, SpellUsageCounts, SpellLevels, TalentPoints, ManaMax/Current
- Fonctions : CastSpell, IsDeityAccessible, LockDeity, UnlockDeity, IncrementSpellUsage, LevelUpSpell, AddTalentPoint
- 4 sorts Lumina valides PIE (Heal, Attack, Buff, Debuff)
- Progression sorts : usage -> EffectiveThreshold = BaseThreshold / Max(1, 9-NiveauSort) -> LevelUpSpell
- Seuils categories : Attack=150, Heal=100, Buff=50, Debuff=35, Ultime=200
- Deites (8) : Lumina, Luna, Ombre, Sylphide, Gnome, Salamandre (=Athanor), Ondine, Dryade

### UI / HUD
- UI_HUD_Main : event-driven via OnStatChanged, zero polling -- FINALISE
- A ajouter (C1-WeaponArchitecture) : jauges Stamina, Mana, Essence, PO, Corruption

### Inputs -- COMPLET VALIDE PIE (23/05/2026)
- IMC_Gameplay, IMC_Radial, IMC_Menu, IMC_Dialogue, IMC_Cutscene
- Voir Docs/Architecture/Input_Architecture.md

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
- [x] J-LockOn COMPLET VALIDE PIE (15/05/2026)
- [x] J-Renommage COMPLET (15/05/2026)
- [x] J-Camera COMPLET VALIDE PIE (17/05/2026)
- [x] J-LockMove COMPLET VALIDE PIE (18/05/2026)
- [x] J-TestBed COMPLET VALIDE PIE (18/05/2026)
- [x] J-ComboFix COMPLET VALIDE PIE (18/05/2026)
- [x] C1-CollisionFix COMPLET VALIDE PIE (18/05/2026)
- [x] C1-HitFeel PARTIEL VALIDE PIE (18/05/2026)
- [x] C1-HitFlashEnemies ABANDONNE (21/05/2026)
- [x] C1-InputsUI COMPLET VALIDE PIE (23/05/2026)
- [x] C1-RadialMagie COMPLET VALIDE PIE (25/05/2026)
- [x] C1-MagicProgressionDesign DESIGN VALIDE (25/05/2026)
- [x] C1-MagicDataLayer VALIDE PIE (25/05/2026)
- [x] DESIGN-MagicProgression VALIDE (26/05/2026)
- [x] C1-MagicUnlockSystem COMPLET VALIDE PIE (27/05/2026)
- [x] RadialUnlock VALIDE PIE (27/05/2026)
- [x] C1-CleanupDettes COMPLET (27/05/2026)
- [x] DESIGN-StatsProgression VALIDE : 7 stats, hybride, Essence, formules, elements, critique, stamina (28/05/2026)
- [x] DESIGN-StatusEffects VALIDE : 8 effets par deite, interactions (28/05/2026)
- [x] DESIGN-Corruption VALIDE : Phase 1/2, lien narratif Ombre, bonus Essence, seuils (28/05/2026)
- [x] DESIGN-Economy VALIDE : double monnaie, drops, consommables Seiken, forge narrative, Mana, equipement (28/05/2026)

## Dettes techniques

- **Roll en lock-on** (C1-AnimationsPass1)
- **Rename ABP_Manny_Platforming -> ABP_Hero** (C1-AnimationsPass1)
- **WeaponClass hardcode BP_Enemy_Sword01** (C2-EnemyMesh)
- **Retopo hero 246K -> 10-15K** (ART-Hero)
- **Radial Armes : SelectedIndex = 0 a l'ouverture** (C1-RadialMagie)
- **Archi armes/combo eclatee** (C1-WeaponArchitecture)
- **Nouvelles stats BP_AttributeSet_Base** (C1-WeaponArchitecture) : Level, EssenceMana, EssenceManaDropped, PiecesOr, ChanceCritique, Corruption, ManaMax, ManaCurrent
- **Stats ennemis enrichies BP_Enemy_Base** (C1-WeaponArchitecture ou C2-EnemyTypes)
- **CoeffArme + VitesseAttaque dans FWeaponData** (C1-WeaponArchitecture)
- **Jauges HUD** (C1-WeaponArchitecture) : Stamina, Mana, Essence, Corruption
- **BP_StatusEffectComponent** (C1-SwordMoveset)
- **Radial dedie objets consommables** (C7-HUDPolish)

## Prochains jalons

1. **C1-WeaponArchitecture + Refacto** : audit armes/combo, source de verite unique, CoeffArme/VitesseAttaque, nouvelles stats, stats ennemis, HUD jauges, doc decisions
2. **C1-SwordMoveset** : moveset epee complet + BP_StatusEffectComponent
3. **SaveDesign** : session design respawn/sauvegarde Fontaine de Fee
4. **Arbre de talents** : C1-MagicTreeModule
5. **C2-SaveGame** : apres SaveDesign validee
6. **C1-BowPOC** : arc
7. **C1-WeaponSwitching** : switching armes en combat
8. **C1-SFXCombat** : sons de base
9. **Lore Deites** : ordre deblocage, cout Essence, structure rituel
10. **Lore Fee** : nom, personnalite, histoire, effet Corruption=100
11. **Session Lore Ombre** : quand debloquer Corruption Phase 2
12. **C1-AnimationsPass1** : strafe + roll sans root motion + rename ABP_Hero

## Sessions design a planifier

- **Session Lore Fee** : nom, personnalite, histoire, lien Ombre/Corruption, effet Corruption=100
- **Session Lore Deites** : ordre deblocage, structure rituel par deite, cout Essence
- **Session Lore Ombre** : moment revelation Hero/Ombre, deblocage Corruption Phase 2
- **Session SaveDesign** : Fontaine de Fee detaillee, respawn, penalites mort
- **Session Economie** : calibrage PO/Essence, prix marchands, taux drops (apres playtest)

---

## Notes techniques importantes

- SetStatValue = unique point de modification stats
- ABP_Manny_Platforming = ABP du HERO (pas ABP_Unarmed)
- SwitchCooldown = dans BP_CombatLockOnComponent UNIQUEMENT
- T3D export = meilleur outil d'audit Blueprint
- add_state MCP dans AnimGraph = shell corrompu -> toujours creer manuellement
- IA_Look est dans le PC (pas dans HeroCharacter) depuis J-Camera
- Move() en lock-on : GetPlayerCameraManager -> GetCameraRotation (pas GetControlRotation)
- LastAxisX/LastAxisY : variables double sur HeroCharacter, SET au Triggered de IA_Move
- InitComboTree(WeaponID, WeaponLevel) : appele par EquipWeapon
- LevelMin = 0 dans DT_Combo = niveau de base (pas 1)
- HandleAttack n'a plus de parametre ChoosenWeapon
- UnlockDeity : "Set Members in FSoM_DeitySpells" et NON "Make FSoM_DeitySpells"
- UnlockDeity Map_Contains : TRUE = deja present -> return (logique contre-intuitive)
- search_nodes("UnlockDeity") MCP = 0 resultats -> chercher "Unlock Deity" (avec espace)
- IsDeityAccessible = Contains(UnlockedSpells) AND NOT Contains(LockedDeities)
- BP_SpellCategoryThresholds : TMap<E_SpellCategory, int> acces via GetClassDefaults
- DT_Deities BaseSpells : ordre fixe [0=Attack, 1=Heal, 2=Buff, 3=Debuff]
- Athanor = Salamandre : meme deite, deux noms
- ChoosenWeapon (HC) et CurrentWeaponID (ComboManager) redondants -- a unifier C1-WeaponArchitecture
- Essence de Mana = perdue a la mort, recuperable sur place (DS-like) -- double mort = perdue definitivement
- PiecesOr = jamais perdues a la mort
- ManaMax separee de Magie -- pas de regen Mana auto
- Cout sorts : Base + (NiveauSort * Multiplicateur)
- ResistanceElementaire = TMap<EElement, float> -- valeurs negatives = faiblesse
- VitesseAttaque = multiplicateur PlayRate montage dans FWeaponData
- Corruption Phase 1 : plafond 50 ; Phase 2 : plafond 100 apres revelation Hero/Ombre
- Corruption faiblesse a 75 = element de la deite la plus utilisee au franchissement (deterministe)
- Corruption bonus Essence plafonne a x1.60 (seuil 75+)
- BP_StatusEffectComponent : a creer en C1-SwordMoveset sur HC et Enemy_Base
- Forge narrative Seiken : upgrade N+1 conditionne par jalon narratif + materiaux
- Coffres ennemis : gimmick Seiken, drop aleatoire
- Respawn Fontaine : ennemis normaux oui, boss jamais
- Pour stats et progression : voir Docs/Architecture/Stats_Progression.md
- Pour effets de statut et corruption : voir Docs/Architecture/Combat_StatusEffects.md
- Pour economie et drops : voir Docs/Architecture/Economy_Drops.md
- Pour decisions archi : voir Docs/Architecture/Decisions.md
- Pour progression magique : voir Docs/Architecture/Magic_Progression.md
- Pour lore complet : voir Docs/Lore_ShadowOfMana.md

---

## Comment demarrer une session

### Session claude.ai
1. Nico dit : "on travaille sur SoM"
2. Claude.ai lit CLAUDE.md + Journal_Modifications.md via GitHub MCP
3. Resume de l'etat actuel + proposition suite

### Session UnrealClaude (editeur)
1. Tools -> Claude Assistant -> NOUVELLE session
2. "CONTEXTE : Tu es l'assistant UnrealClaude lance dans UE5.7 depuis 'Tools => Claude Assistant', tu as acces a 28 MCP Tools."
3. Agent en mode DISCOVERY UNIQUEMENT

---

*Derniere mise a jour : 28/05/2026*
