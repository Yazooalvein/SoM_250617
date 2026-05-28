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
| `Docs/Architecture/Input_Architecture.md` | Quand les inputs changent |
| `Docs/Architecture/RadialMenu_Architecture.md` | Quand le radial evolue |
| `Docs/Lore_ShadowOfMana.md` | Quand le lore ou le cast change |
| `Docs/Project_Architecture_Index.md` | Quand un nouveau fichier doc est cree |

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
- `DiscoveredWeapons` (Array<FName>), `ChoosenWeapon` (FName)
- `BP_CombatLockOnComponent`, `MagicComponent`, `BP_ComboManagerComponent` sur le Character
- NOTE : ChoosenWeapon (HC) et CurrentWeaponID (ComboManager) redondants -- a unifier C1-WeaponArchitecture

### Stats heros -- DESIGN VALIDE (28/05/2026)
- 7 stats : Vitalite, Attaque, Defense, Magie, Resistance, Endurance, Vitesse
- Cles supplementaires BP_AttributeSet_Base : Level, EssenceMana, EssenceManaDropped, PiecesOr, ChanceCritique, Corruption, ManaMax, ManaCurrent
- Progression hybride : niveaux 1-10 (stats auto + 2 pts libres) + usage armes/magie
- Essence de Mana : progression -- perdue a la mort, recuperable DS-like
- Pieces d'Or : economie -- jamais perdues
- Formule physique : Max(1, (Attaque * CoeffArme * CoeffCritique) - (Defense * 0.5))
- Formule magique : Max(1, (Magie * CoeffSort * CoeffCritique) - (Resistance * 0.5))
- Elementaire : * (1 - ResistanceElementaire[Element]) -- 8 elements / 8 deites
- ManaMax separee de Magie : base 60, +8/niveau -- pas de regen auto
- Equipement : 3 slots (Casque, Armure, Accessoire) -- Defense + Resistance uniquement
- Voir Docs/Architecture/Stats_Progression.md

### Stats ennemis -- DESIGN VALIDE (28/05/2026)
- PV, Attaque, Defense, Resistance, Vitesse, VitesseAttaque, TenaciteEtat, ResistanceElementaire
- Voir Docs/Architecture/Stats_Progression.md

### Effets de statut -- DESIGN VALIDE (28/05/2026)
- 8 effets par deite, BP_StatusEffectComponent a creer en C1-SwordMoveset
- Voir Docs/Architecture/Combat_StatusEffects.md

### Corruption Magique -- DESIGN VALIDE (28/05/2026)
- Phase 1 (debut jeu) : plafond 50
- Phase 2 (apres Sanctuaire d'Ombre) : plafond 100
- Faiblesse a 75 = deite la plus utilisee DEPUIS LA DERNIERE PURGE
- Bonus Essence : x1.0 / x1.15 / x1.35 / x1.60 / x1.60 (plafond)
- Voir Docs/Architecture/Combat_StatusEffects.md

### Economie & Drops -- DESIGN VALIDE (28/05/2026)
- Double monnaie, consommables Seiken (9 max/type), forge narrative, Mana sans regen
- Menu pause : pause complete (Time Dilation reserve au radial uniquement)
- Touchpad PS5 : reserve a C4
- Voir Docs/Architecture/Economy_Drops.md

### Lore & Cast -- DESIGN VALIDE provisoire (28/05/2026)
- Voir Docs/Lore_ShadowOfMana.md pour le detail complet

**Cast (races) :**
- Heros : Humain
- Pretresse (Lumina) : Humaine Celeste (ailes blanches)
- Suivante (Luna) : Beastman Felin -- froide/heros, douce/Garcon Loup
- Forgeron Nain (Salamandre) : Nain -- pere adoptif Garcon Loup
- Colosse (Gnome) : Nain -- ami Garcon Loup
- Reine du Vent (Sylphide) : DragonFolk
- Oracle Mana (Dryade) : Sproutling taille humaine -- arrive fin acte 2
- Soeur du Heros : Humaine -- fusion incomplete Ondine, devient Deesse Mana fin jeu
- Garcon Loup : Beastman Loup -- reçoit Ondine fin jeu
- Fee : fragment ame soeur (insuffle par Ondine) -- nom a trouver avec la soeur ⚠️

**Ordre deites (provisoire) :**
Lumina (A1 debut) -> Luna (A1 debut) -> Gnome (A1 milieu) -> Ombre (A1 milieu post-Gnome) -> Salamandre (A2) -> Sylphide (A2) -> Dryade (A2 fin) -> Ondine (A3)

**Sanctuaire d'Ombre (milieu A1) :**
- Zone obligatoire, Corruption monte anormalement avant d'y entrer
- Boss met heros a 0 PV -- Ombre intervient via Corruption, heros se releve
- Images ambigues d'Ombre (alliee ou menace ?)
- Consequence : Corruption Phase 2 debloquee

**⚠️ RAPPEL RECURRENT : noms Soeur et Fee a trouver ensemble (foreshadow)**

### Hero 3D
- ABP actif : ABP_Manny_Platforming (pas ABP_Unarmed)
- Mesh : Meshy_AI_Crimson_Scarf_Adventu_0513214252_texture
- Rotation Rate Z = -1, LastAxisX/LastAxisY doubles sur HeroCharacter

### Camera -- VALIDE PIE (17/05/2026)
- SpringArm : 350, Z 60, Lag 8 -- IA_Look dans PC -- UpdateLockOnRotation V2

### Lock-On -- VALIDE PIE (15/05/2026)
- BP_CombatLockOnComponent sur Character -- SwitchCooldown source unique

### Ennemis
- BP_Enemy_Base : stats a ajouter (C1-WeaponArchitecture ou C2-EnemyTypes)
- BP_Enemy_TestBed : stats Instance Editable

### Combat -- VALIDE PIE (18/05/2026)
- BP_ComboManagerComponent : TMap<Name, FComboStep>, InitComboTree, HandleAttack
- Flow : IA_Attack -> CanAttack -> HandleAttack -> PlayAttackMontage

### Armes
- FWeaponData : a enrichir CoeffArme + VitesseAttaque (C1-WeaponArchitecture)
- DETTE : ChoosenWeapon (HC) redondant avec CurrentWeaponID (ComboManager)

### Magie -- VALIDE PIE (27/05/2026)
- BP_MagicComponent : CastSpell, IsDeityAccessible, LockDeity, UnlockDeity, IncrementSpellUsage, LevelUpSpell
- Seuils : Attack=150, Heal=100, Buff=50, Debuff=35, Ultime=200
- Deites (8) : Lumina, Luna, Ombre, Sylphide, Gnome, Salamandre, Ondine, Dryade

### UI / HUD
- UI_HUD_Main : event-driven -- FINALISE
- A ajouter (C1-WeaponArchitecture) : jauges Stamina, Mana, Essence, Corruption

### Inputs -- VALIDE PIE (23/05/2026)
- IMC_Gameplay, IMC_Radial, IMC_Menu, IMC_Dialogue, IMC_Cutscene

---

## Jalons completes

- [x] #1 a #9, J-10 a J-15, J-RadialMenu, J-Cleanup, ART-Hero (partiel), MUS-Workflow
- [x] J-LockOn, J-Renommage, J-Camera, J-LockMove, J-TestBed, J-ComboFix (15-18/05/2026)
- [x] C1-CollisionFix, C1-HitFeel (partiel), C1-HitFlashEnemies (abandonne) (18-21/05/2026)
- [x] C1-InputsUI VALIDE PIE (23/05/2026)
- [x] C1-RadialMagie, C1-MagicProgressionDesign, C1-MagicDataLayer (25/05/2026)
- [x] DESIGN-MagicProgression (26/05/2026)
- [x] C1-MagicUnlockSystem, RadialUnlock, C1-CleanupDettes (27/05/2026)
- [x] DESIGN-StatsProgression, DESIGN-StatusEffects, DESIGN-Corruption, DESIGN-Economy (28/05/2026)
- [x] DESIGN-Lore : cast races, Fee fragment ame soeur, Sanctuaire Ombre, ordre deites, conflit Loup/DragonFolk (28/05/2026)

## Dettes techniques

- **Roll en lock-on** (C1-AnimationsPass1)
- **Rename ABP_Manny_Platforming -> ABP_Hero** (C1-AnimationsPass1)
- **WeaponClass hardcode BP_Enemy_Sword01** (C2-EnemyMesh)
- **Retopo hero 246K -> 10-15K** (ART-Hero)
- **Radial Armes : SelectedIndex = 0** (C1-RadialMagie)
- **Archi armes/combo eclatee** (C1-WeaponArchitecture)
- **Nouvelles stats BP_AttributeSet_Base** (C1-WeaponArchitecture)
- **Stats ennemis BP_Enemy_Base** (C1-WeaponArchitecture ou C2-EnemyTypes)
- **CoeffArme + VitesseAttaque FWeaponData** (C1-WeaponArchitecture)
- **Jauges HUD Stamina/Mana/Essence/Corruption** (C1-WeaponArchitecture)
- **BP_StatusEffectComponent** (C1-SwordMoveset)
- **Radial dedie objets consommables** (C7-HUDPolish)

## Prochains jalons

1. **C1-WeaponArchitecture + Refacto**
2. **C1-SwordMoveset** + BP_StatusEffectComponent
3. **SaveDesign** : spec Fontaine de Fee
4. **C1-MagicTreeModule** : arbre de talents
5. **C2-SaveGame**
6. **C1-BowPOC**, **C1-WeaponSwitching**, **C1-SFXCombat**
7. **Session Noms personnages** : soeur + fee ensemble ⚠️
8. **Session Lore Deites** : rituels, cout Essence
9. **Session zones acte 1** : structure, Fontaines, enchaînement
10. **C1-AnimationsPass1**

## Sessions design a planifier

- **Session Noms** : tous les personnages -- soeur et fee ENSEMBLE ⚠️
- **Session Lore Deites** : rituels par deite, cout Essence, order confirmation
- **Session zones acte 1** : structure zones, Fontaines, conflit Loup/DragonFolk
- **Session SaveDesign** : Fontaine de Fee detaillee
- **Session Economie** : calibrage (apres playtest)

---

## Notes techniques importantes

- SetStatValue = unique point de modification stats
- ABP_Manny_Platforming = ABP du HERO (pas ABP_Unarmed)
- SwitchCooldown = dans BP_CombatLockOnComponent UNIQUEMENT
- T3D export = meilleur outil d'audit Blueprint
- add_state MCP AnimGraph = shell corrompu -> creer manuellement
- IA_Look dans PC (pas HeroCharacter)
- Move() lock-on : GetPlayerCameraManager -> GetCameraRotation
- LastAxisX/LastAxisY : doubles sur HeroCharacter, SET au Triggered IA_Move
- InitComboTree(WeaponID, WeaponLevel) : appele par EquipWeapon
- LevelMin = 0 dans DT_Combo
- HandleAttack sans parametre ChoosenWeapon
- UnlockDeity : "Set Members in FSoM_DeitySpells" NON "Make FSoM_DeitySpells"
- UnlockDeity Map_Contains : TRUE = deja present -> return
- search_nodes("UnlockDeity") = 0 -> chercher "Unlock Deity" (avec espace)
- IsDeityAccessible = Contains(UnlockedSpells) AND NOT Contains(LockedDeities)
- DT_Deities BaseSpells : [0=Attack, 1=Heal, 2=Buff, 3=Debuff]
- Athanor = Salamandre
- Corruption faiblesse 75 = deite la plus utilisee DEPUIS LA DERNIERE PURGE
- Corruption Phase 1 plafond 50 / Phase 2 plafond 100 (apres Sanctuaire d'Ombre)
- Menu pause = pause complete (pas Time Dilation) -- Time Dilation reserve radial uniquement
- Touchpad PS5 : reserve C4
- Fee = fragment ame soeur insuffle par Ondine -- noms Fee ET Soeur a trouver ENSEMBLE ⚠️
- Forge narrative Seiken : upgrade N+1 conditionne par jalon narratif + materiaux
- Respawn Fontaine : ennemis normaux oui, boss jamais
- Pour lore complet : voir Docs/Lore_ShadowOfMana.md
- Pour stats : voir Docs/Architecture/Stats_Progression.md
- Pour effets statut/corruption : voir Docs/Architecture/Combat_StatusEffects.md
- Pour economie/drops : voir Docs/Architecture/Economy_Drops.md
- Pour decisions archi : voir Docs/Architecture/Decisions.md

---

## Comment demarrer une session

### Session claude.ai
1. Nico dit : "on travaille sur SoM"
2. Lire CLAUDE.md + Journal_Modifications.md
3. Resume etat actuel + proposition suite

### Session UnrealClaude
1. Tools -> Claude Assistant -> NOUVELLE session
2. "CONTEXTE : Tu es l'assistant UnrealClaude lance dans UE5.7 depuis 'Tools => Claude Assistant', tu as acces a 28 MCP Tools."
3. DISCOVERY UNIQUEMENT

---

*Derniere mise a jour : 28/05/2026*
