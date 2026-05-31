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
| `Docs/Architecture/Weapons_Progression.md` | Quand progression armes change |
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
- `BP_CombatLockOnComponent`, `MagicComponent`, `BP_ComboManagerComponent`, `BP_InventoryComponent` sur le Character
- HC.ChoosenWeapon SUPPRIME -- source unique : ComboManager.CurrentWeaponID (29/05/2026)
- DiscoveredWeapons SUPPRIME de HC -- migre vers BP_InventoryComponent (29/05/2026)

### Composants HC -- philosophie de factorisation
- HC = coordinateur leger, ne stocke pas d'etat metier
- BP_CombatLockOnComponent : tout l'etat lock-on
- BP_MagicComponent : tout l'etat magie
- BP_ComboManagerComponent : arme courante + niveau arme + etat combo
- BP_InventoryComponent : armes decouvertes (Content/Systems/Inventory/) -- extensible consommables/craft/equip

### BP_InventoryComponent -- VALIDE PIE (29/05/2026)
- Variables : DiscoveredWeapons (Array<Name>)
- Fonctions : AddWeapon(WeaponID : Name), GetWeapons() -> Array<Name>
- Valeurs par defaut renseignees en Details panel instance HC (dette -> BeginPlay a terme)
- Radial lit GetWeapons() pour peupler les slots armes

### Stats heros -- DESIGN VALIDE (28/05/2026)
- 7 stats : Vitalite, Attaque, Defense, Magie, Resistance, Endurance, Vitesse
- Cles supplementaires BP_AttributeSet_Base : Level, EssenceMana, EssenceManaDropped, PiecesOr, ChanceCritique, Corruption, ManaMax, ManaCurrent, TenaciteEtat
- TenaciteEtat : base 25, impactee par equipement + debuffs + Corruption (a implementer)
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
- 8 effets par deite, BP_StatusEffectComponent a creer (jalon a definir)
- Voir Docs/Architecture/Combat_StatusEffects.md

### Corruption Magique -- DESIGN VALIDE (28/05/2026)
- Phase 1 (debut jeu) : plafond 50 (bCorruptionUnlocked=false dans AttributeSet)
- Phase 2 (apres Sanctuaire d'Ombre) : plafond 100 (bCorruptionUnlocked=true)
- Logique metier complete (tracking deites, purge, faiblesse 75) dans BP_CorruptionComponent (C2-CorruptionSystem)
- Faiblesse a 75 = deite la plus utilisee DEPUIS LA DERNIERE PURGE
- Bonus Essence : x1.0 / x1.15 / x1.35 / x1.60 / x1.60 (plafond)
- Corruption reduit TenaciteEtat heros (calibrage a definir)
- Voir Docs/Architecture/Combat_StatusEffects.md

### Economie & Drops -- DESIGN VALIDE (28/05/2026)
- Double monnaie, consommables Seiken (9 max/type), forge narrative, Mana sans regen
- Menu pause : pause complete (Time Dilation reserve au radial uniquement)
- Touchpad PS5 : reserve a C4
- Voir Docs/Architecture/Economy_Drops.md

### Progression Armes -- DESIGN VALIDE (30/05/2026)
- Usage en combat (nombre d'attaques), formule identique magie (9 - niveau actuel %)
- Niveau 1->2 libre ; Niveau 2->3+ conditionne par forge (XP bloquee avant forge)
- Materiaux : Drop commun x N (Minerai/Bois/etc.) + Drop rare x 1 (Boss/Narratif)
- Arbre par arme : tous les X niveaux (a calibrer) -- choix Combo ou Stat
- ~50% maxables naturellement, reste via quetes annexes haut level (donnent materiaux rares)
- Pas de rattrapage armes (contrairement a la magie)
- Voir Docs/Architecture/Weapons_Progression.md

### Lore & Cast -- DESIGN VALIDE enrichi (29/05/2026)
- Voir Docs/Lore_ShadowOfMana.md pour le detail complet

**Cast (races) :**
- Heros : Humain -- seul impacte physiquement par la Corruption (indices visuels subtils)
- Pretresse (Lumina) : Humaine Celeste (ailes blanches) -- percoit la Corruption sur le heros
- Suivante (Luna) : Beastman Felin -- froide/heros, douce/Garcon Loup -- percoit la Corruption sur le heros
- Forgeron Nain (Salamandre) : Nain -- pere adoptif Garcon Loup -- actif tout au long du jeu
- Colosse (Gnome) : Nain -- ami Garcon Loup -- ne percoit pas la Corruption
- Reine du Vent (Sylphide) : DragonFolk
- Oracle Mana (Dryade) : Sproutling taille humaine -- arrive fin acte 2, meurt debut A4
- Soeur du Heros : Humaine -- fusion incomplete Ondine, devient Deesse Mana fin jeu -- revelee vivante au boss A2
- Garcon Loup : Beastman Loup -- recoit Ondine fin jeu -- ne percoit pas la Corruption
- Fee : fragment ame soeur (insuffle par Ondine) -- nom a trouver avec la soeur ⚠️

**Ordre deites (provisoire) :**
Lumina (A1 debut) -> Luna (A1 debut) -> Gnome (A1 milieu) -> Ombre (A1 milieu post-Gnome) -> Salamandre (A2) -> Sylphide (A2) -> Dryade (A2 fin) -> Ondine (A3)

**Sanctuaire d'Ombre (milieu A1) :**
- Zone obligatoire, Corruption monte anormalement avant d'y entrer
- Boss met heros a 0 PV -- Ombre intervient via Corruption, heros se releve
- Images ambigues d'Ombre (alliee ou menace ?)
- Consequence : Corruption Phase 2 debloquee

**Structure actes (29/05/2026) :**
- A1 : monde brise, equipe, mystere heros/Ombre, Epee Mana brisee + reconnue par heros
- A2 : retour Hub (non reconstruit), liberation zones (deite = changement esthetique + Hub se reconstruit), boss General = choix moral + revelation soeur vivante
- A3 : recherche soeur, verite Grande Guerre, Epee Mana restauree, boss Demon Mana
- A4 : Demon Primordial, Flammy debloque, resolution toutes lignes

**Armes Mana (29/05/2026) :**
- Amenees par la Deesse, trouvees deteriorees en A1, restaurees par etapes (Forgeron + materiaux drop)
- Jalon narratif + materiaux = condition double pour chaque palier d'evolution
- Epee Mana : brisee A1 = reconnaissance heros, evolution par etapes, etat final A3 = condition boss Demon Mana

**⚠️ RAPPEL RECURRENT : noms Soeur et Fee a trouver ensemble (foreshadow)**
**⚠️ Question ouverte : presence General avant boss A2 (Option A ou B) -- en maturation**

### Hero 3D
- ABP actif : ABP_Manny_Platforming (pas ABP_Unarmed)
- Mesh : Meshy_AI_Crimson_Scarf_Adventu_0513214252_texture
- Rotation Rate Z = -1, LastAxisX/LastAxisY doubles sur HeroCharacter

### Camera -- VALIDE PIE (17/05/2026)
- SpringArm : 350, Z 60, Lag 8 -- IA_Look dans PC -- UpdateLockOnRotation V2

### Lock-On -- VALIDE PIE (15/05/2026)
- BP_CombatLockOnComponent sur Character -- SwitchCooldown source unique

### Ennemis
- BP_Enemy_Base : stats a ajouter (C2-EnemyTypes)
- BP_Enemy_TestBed : stats Instance Editable

### Combat -- VALIDE PIE (29/05/2026)
- BP_ComboManagerComponent : TMap<Name, FComboStep>, InitComboTree, HandleAttack, EquipWeapon
- Flow : IA_Attack -> CanAttack -> HandleAttack -> PlayAttackMontage
- CanAttack : source unique ComboManager
- Switch arme en combo = reset combo complet (punition) -- pas de grisage Radial

### Armes -- VALIDE PIE (29/05/2026)
- FWeaponData : CoeffArme + VitesseAttaque present (a utiliser dans formule degats)
- ComboManager.CurrentWeaponID = source unique arme equipee
- ComboManager.EquipWeapon(WeaponID, WeaponLevel) = point d'entree unique equipement arme
  - Flux : SET CurrentWeaponID/Level/StepID/CanAttack -> GetDataTableRow(DT_Weapons) -> InitComboTree(WeaponData)
- HC.EquipWeapon = spawn physique arme + attach HandGrip_R + AddWeapon(InventoryComponent) + appel ComboManager.EquipWeapon
- InitComboTree(WeaponData) = responsabilite unique : Map_Clear + charger ComboStepMap depuis DT_Combo

### Radial Armes -- VALIDE PIE (29/05/2026)
- PopulateWeaponSlots lit InventoryComponent.GetWeapons() (plus HC.DiscoveredWeapons)
- Mecanique : roue tourne sur arme equipee a l'ouverture, curseur fixe en haut (position 0)
- Guard : si CurrentWeaponID == None -> pas de modification rotation
- Dette curseur : position initiale toujours slot 0 -> C?-RadialRefacto (refonte systeme Radial)

### Magie -- VALIDE PIE (27/05/2026)
- BP_MagicComponent : CastSpell, IsDeityAccessible, LockDeity, UnlockDeity, IncrementSpellUsage, LevelUpSpell
- Seuils : Attack=150, Heal=100, Buff=50, Debuff=35, Ultime=200
- Deites (8) : Lumina, Luna, Ombre, Sylphide, Gnome, Salamandre, Ondine, Dryade

### UI / HUD -- VALIDE (31/05/2026)
- UI_HUD_Main : event-driven, finalise
- Architecture : barres HP/ST/MP/Corruption dans HUD_Main_VertBox, compteur Essence separe pres arme
- Variables widget : HealthPercent, StaminaPercent, ManaPercent, EssenceValue, CorruptionPercent
- Switch HUD_OnStatChanged : 8 cases (HealthCurrent, StaminaCurrent, ManaCurrent, HealthMax, StaminaMax, ManaMax, EssenceMana, Corruption)
- Bindings ProgressBar : Get_HealthBar_Percent, Get_StaminaBar_Percent, Get_ManaBar_Percent, Get_CorruptionBar_Percent
- UpdateEssenceText : EssenceValue -> Int64 -> String -> Text -> SetText(TextBlock_Essence)
- bCorruptionUnlocked dans AttributeSet : false=clamp50, true=clamp100
- BP_CorruptionComponent : jalon C2-CorruptionSystem (tracking deites, purge, faiblesse 75)
- C3-EssenceMana : jalon dedie systeme complet (collecte, perte mort, recuperation DS-like)

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
- [x] DESIGN-Lore : cast races, Fee fragment ame soeur, Sanctuaire Ombre, ordre deites (28/05/2026)
- [x] C1-WeaponArchitecture etapes 5-6 VALIDE, etape 7 PARTIELLE (28/05/2026)
- [x] DESIGN-WeaponArchitecture : ComboManager source verite, InventoryComponent, TenaciteEtat, switch combo punition (29/05/2026)
- [x] C1-WeaponArchitecture COMPLET VALIDE PIE (29/05/2026)
- [x] DESIGN-Lore enrichi : structure actes, Armes Mana, Hub reconstruction, Corruption heros (29/05/2026)
- [x] DESIGN-WeaponProgression : progression usage, forge, arbre combo/stat, end-game (30/05/2026)
- [x] C1-HUDCore VALIDE (31/05/2026)

## Dettes techniques

- **Roll en lock-on** (C1-AnimationsPass1)
- **Rename ABP_Manny_Platforming -> ABP_Hero** (C1-AnimationsPass1)
- **WeaponClass hardcode BP_Enemy_Sword01** (C2-EnemyMesh)
- **Retopo hero 246K -> 10-15K** (ART-Hero)
- **Radial curseur position initiale a l'ouverture** (C?-RadialRefacto -- refonte complete systeme Radial)
- **SaveGame : BeginPlay charger arme -> EquipWeapon** (C2-SaveGame)
- **TenaciteEtat : ajouter dans BP_AttributeSet_Base (base 25)** (a placer dans jalon adequat)
- **Stats ennemis BP_Enemy_Base** (C2-EnemyTypes)
- **BP_StatusEffectComponent** (jalon a definir -- lie magie/ennemis)
- **DiscoveredWeapons par defaut via Details panel HC** -> migrer vers BeginPlay (C2-SaveGame)
- **Radial dedie objets consommables** (C7-HUDPolish)
- **HUD Designer : TextBlock_Essence et CorruptionBar hors Overlay/SizeBox standard** (C7-HUDPolish)

## Prochains jalons

1. **SaveDesign** : spec Fontaine de Fee
2. **C2-CorruptionSystem** : BP_CorruptionComponent, tracking deites, purge, faiblesse 75, TenaciteEtat, indices visuels heros
3. **C3-EssenceMana** : systeme complet Essence (collecte, perte a la mort, recuperation DS-like, bonus Corruption)
4. **C1-MagicTreeModule** : arbre de talents magie
5. **C2-SaveGame**
6. **C1-BowPOC**, **C1-WeaponSwitching**, **C1-SFXCombat**
7. **C?-RadialRefacto** : refonte complete systeme Radial (curseur, architecture)
8. **Session Noms personnages** : soeur + fee ensemble ⚠️
9. **Session Lore Deites** : rituels, cout Essence
10. **Session zones acte 1** : structure, Fontaines, enchainement
11. **C1-AnimationsPass1**

## Sessions design a planifier

- **Session Noms** : tous les personnages -- soeur et fee ENSEMBLE ⚠️
- **Session Lore Deites** : rituels par deite, cout Essence, order confirmation
- **Session zones acte 1** : structure zones, Fontaines, conflit Loup/DragonFolk
- **Session zones acte 2** : origine conflit Loup/DragonFolk, structure regions
- **Session SaveDesign** : Fontaine de Fee detaillee
- **Session Forge/Economie** : materiaux par arme, calibrage niveaux arbre

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
- LevelMin = 0 dans DT_Combo
- HandleAttack sans parametre ChoosenWeapon
- HC.CanAttack supprime -- source unique ComboManager.CanAttack
- HC.ChoosenWeapon SUPPRIME -- source unique ComboManager.CurrentWeaponID
- ComboManager.EquipWeapon(WeaponID, WeaponLevel) = point d'entree unique equipement arme
- InitComboTree(WeaponData) = responsabilite unique : charger ComboStepMap (pas de SETs d'etat)
- HC.EquipWeapon = spawn physique + InventoryComponent.AddWeapon + ComboManager.EquipWeapon
- PopulateWeaponSlots lit InventoryComponent.GetWeapons() (pas HC.DiscoveredWeapons)
- BP_InventoryComponent : Actor Component, Content/Systems/Inventory/
- Switch arme en combo = reset combo complet, pas de grisage Radial
- TenaciteEtat heros : base 25, cle supplementaire AttributeSet, impactee par Corruption + debuffs (a implementer)
- UpgradeWeaponLevel : Option A runtime (etape 6 C1-WeaponArchitecture)
- Radial roue tourne sur arme equipee a l'ouverture -- TargetRotation = -(EquippedIndex * AnglePerSlot)
- Guard PopulateWeaponSlots : si CurrentWeaponID == None -> pas de rotation
- Radial curseur position initiale : systeme heterogene -> reporte C?-RadialRefacto
- UnlockDeity : "Set Members in FSoM_DeitySpells" NON "Make FSoM_DeitySpells"
- UnlockDeity Map_Contains : TRUE = deja present -> return
- search_nodes("UnlockDeity") = 0 -> chercher "Unlock Deity" (avec espace)
- IsDeityAccessible = Contains(UnlockedSpells) AND NOT Contains(LockedDeities)
- DT_Deities BaseSpells : [0=Attack, 1=Heal, 2=Buff, 3=Debuff]
- Athanor = Salamandre
- Corruption faiblesse 75 = deite la plus utilisee DEPUIS LA DERNIERE PURGE
- Corruption Phase 1 plafond 50 (bCorruptionUnlocked=false) / Phase 2 plafond 100 (bCorruptionUnlocked=true)
- bCorruptionUnlocked dans AttributeSet = variable simple, logique metier dans C2-CorruptionSystem
- Corruption reduit TenaciteEtat heros (calibrage a definir en session Economie)
- EssenceMana : compteur absolu Int64 (pas de Max), souls-like -- systeme complet dans C3-EssenceMana
- HUD_OnStatChanged Switch : 8 cases -- EssenceMana (SET direct) + Corruption (NewValue/100)
- UpdateEssenceText : Conv_DoubleToInt64 -> Conv_Int64ToString (Int64 = pas d'overflow grandes valeurs)
- Menu pause = pause complete (pas Time Dilation) -- Time Dilation reserve radial uniquement
- Touchpad PS5 : reserve C4
- Fee = fragment ame soeur insuffle par Ondine -- noms Fee ET Soeur a trouver ENSEMBLE ⚠️
- Forge narrative Seiken : upgrade N+1 conditionne par jalon narratif + materiaux
- Armes Mana : jalon narratif + materiaux drop = double condition evolution (empeche tout maxer d'un coup)
- Epee Mana : brisee A1 = reconnaissance heros, evolution par etapes, etat final A3 = condition boss Demon Mana
- Forgeron Nain : actif et utile tout au long du jeu (pas juste A1/A2)
- Liberation deite dans une region = changement esthetique visuel de la zone
- Hub non reconstruit a l'arrivee A2 -- se reconstruit zone par zone, PNJs rencontres en route reviennent
- Heros = seul humanoide impacte physiquement par Corruption -- Pretresse + Suivante le percoivent (sensibilite Mana)
- Flammy : debloque fin A3/A4, acces lieux inaccessibles
- Conflit Loup/DragonFolk : ancien, amplifie par Decheance Mana
- Respawn Fontaine : ennemis normaux oui, boss jamais
- Progression armes : Lvl1->2 libre, Lvl2->3+ forge requise avant XP -- arbre combo/stat tous les X niveaux
- Quetes annexes haut level : donnent materiaux rares manquants (pas forge directe) -- joueur choisit quelle arme maxer
- Pour lore complet : voir Docs/Lore_ShadowOfMana.md
- Pour stats : voir Docs/Architecture/Stats_Progression.md
- Pour effets statut/corruption : voir Docs/Architecture/Combat_StatusEffects.md
- Pour economie/drops : voir Docs/Architecture/Economy_Drops.md
- Pour decisions archi : voir Docs/Architecture/Decisions.md
- Pour progression armes : voir Docs/Architecture/Weapons_Progression.md

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

*Derniere mise a jour : 31/05/2026*
