# Session_UnrealClaude.md -- Log des actions de l'agent UE

Ce fichier est maintenu par l'agent UnrealClaude en temps reel pendant ses sessions dans l'editeur.
Il est lu par Claude.ai en debut de session pour rester au courant de tout ce qui a ete fait dans UE.

## Format d'entree

```
### [DATE] -- [NOM DU BLUEPRINT / ASSET]
**Action** : ce qui a ete fait
**Pourquoi** : raison ou contexte
**Points d'attention** : gotchas, dependances, ce qui pourrait casser
```

## ⚠️ Instructions pour l'agent UnrealClaude

- Logue TOUTE modification significative ici, meme les petites
- Sois precis sur les noms de Blueprint, variables, nodes
- Note les decisions prises et pourquoi (pas juste le "quoi" mais le "pourquoi")
- Si quelque chose ne fonctionne pas comme prevu, logue-le aussi
- Claude.ai lit ce fichier : il doit pouvoir comprendre sans avoir ete present

---

## Historique des sessions

### 11/05/2026 -- SESSION POC MAGIE J-10 / J-11 (agent Claude Code)

**Contexte** : Demarrage du POC Magie. Architecture reference : Docs/Architecture/Magic_System.md.
Agent operationnel : Claude Code (pas UnrealClaude plugin -- outils MCP UE non disponibles dans cette session).
Actions effectuees : creation dossier filesystem + plan d'implementation complet pour execution dans l'editeur.

---

#### [J-10] Preparation dossier Content/Systems/Magic/

**Action** : Creation du dossier `Content/Systems/Magic/` (filesystem).
**Pourquoi** : UE5 detecte automatiquement les nouveaux dossiers dans Content/ -- il apparaitra dans le Content Browser au prochain refresh ou ouverture editeur.
**Points d'attention** : Le dossier est vide. Tous les assets (BP_MagicComponent, FSoM_SpellData, DT_Spells, enums) doivent etre crees depuis l'editeur UE. Le format .uasset est binaire -- impossible de les creer depuis le filesystem.

---

#### [J-10] Plan d'implementation BP_MagicComponent -- A EXECUTER DANS L'EDITEUR

**Ce qui doit etre fait dans UE5 :**

**Etape 1 -- Creer les Enums (prerequis pour FSoM_SpellData)**
Dans Content/Systems/Magic/, faire clic droit -> Blueprints -> Enumeration :
- `E_SpellCategory` : valeurs = Attaque, Buff, Debuff, Soin, Ultime
- `E_SpellTarget` : valeurs = Enemy, Self, Area

**Etape 2 -- Creer la Struct FSoM_SpellData (prerequis pour DT_Spells)**
Dans Content/Systems/Magic/, faire clic droit -> Blueprints -> Structure, nommer `FSoM_SpellData` :
- SpellID : Name
- SpellName : Text
- Deity : Name
- Category : E_SpellCategory (enum)
- ManaCost : Float
- CastTime : Float (default 0.0)
- Cooldown : Float
- TargetType : E_SpellTarget (enum)
- EffectValue : Float
- Duration : Float

**Etape 3 -- Creer BP_MagicComponent**
Dans Content/Systems/Magic/, clic droit -> Blueprint Class -> parent = ActorComponent.
Nommer : `BP_MagicComponent`

Variables a ajouter :
| Nom | Type | Default | Details |
|-----|------|---------|---------|
| UnlockedSpells | Map<Name, Array<Name>> | vide | DeityName -> [SpellIDs] |
| QuickslotSlots | Array<Name> (size 4) | ["","","",""] | 4 emplacements quickslot |
| SpellCooldowns | Map<Name, Float> | vide | SpellID -> temps restant |
| bIsCasting | Boolean | false | sort en cours de cast |

Dispatcher a creer :
- `OnSpellCast` avec parametre : SpellID (Name)

Fonctions a creer :
1. **CanCast(SpellID : Name) -> Boolean** (Pure)
   - Get Owner -> Cast to BP_PlatformingCharacter -> GetComponentByClass(BP_AttributeSet_Base) -> Get ManaCurrent
   - Get SpellCooldowns -> Find(SpellID) -> cooldown == 0.0 (ou absent)
   - Return : ManaCurrent >= ManaCost ET cooldown <= 0 ET bIsCasting == false
   - Pour le ManaCost : faire un GetSpellData helper (DT lookup) ou hardcoder temporairement pour le POC

2. **ConsumeMana(Amount : Float)**
   - Get Owner -> Cast to BP_PlatformingCharacter -> GetComponentByClass(BP_AttributeSet_Base)
   - AttributeSet -> GetStatValue("ManaCurrent") -> soustraction -> SetStatValue("ManaCurrent", result)
   - Convention : passer par SetStatValue OBLIGATOIRE (jamais SET direct sur la variable)

3. **UnlockDeity(DeityName : Name)**
   - Add ou Find+Modify dans UnlockedSpells : DeityName -> ajouter les SpellIDs de cette deite
   - Pour Lumina : ajouter [Lumina_Heal, Lumina_Attack, Lumina_Buff, Lumina_Debuff]

4. **IsSpellUnlocked(SpellID : Name) -> Boolean** (Pure)
   - Iterate sur toutes les valeurs de UnlockedSpells
   - Chercher si SpellID est present dans l'un des arrays
   - Return true si trouve

**Etape 4 -- Ajouter BP_MagicComponent sur BP_PlatformingCharacter**
Ouvrir BP_PlatformingCharacter -> Components -> Add Component -> BP_MagicComponent
Nommer le component "MagicComponent" (comme AttributeSetRef pour l'AttributeSet)
Sauvegarder BP_PlatformingCharacter.

---

#### [J-11] Plan d'implementation DT_Spells -- A EXECUTER DANS L'EDITEUR

**Etape 5 -- Creer DT_Spells**
Dans Content/Systems/Magic/, clic droit -> Miscellaneous -> Data Table.
Choisir row struct : FSoM_SpellData.
Nommer : `DT_Spells`

Ajouter 4 lignes (Row Name = SpellID) :

| Row Name | SpellName | Deity | Category | ManaCost | CastTime | Cooldown | TargetType | EffectValue | Duration |
|----------|-----------|-------|----------|----------|----------|----------|------------|-------------|----------|
| Lumina_Heal | "Lumiere de Soin" | Lumina | Soin | 15.0 | 0.0 | 3.0 | Self | 30.0 | 0.0 |
| Lumina_Attack | "Trait de Lumiere" | Lumina | Attaque | 20.0 | 1.2 | 5.0 | Enemy | 40.0 | 0.0 |
| Lumina_Buff | "Benediction" | Lumina | Buff | 10.0 | 0.0 | 8.0 | Self | 0.0 | 10.0 |
| Lumina_Debuff | "Marque de Lumiere" | Lumina | Debuff | 15.0 | 0.8 | 6.0 | Enemy | 0.0 | 6.0 |

Notes sur les valeurs :
- Cooldown Lumina_Heal = 3.0 (soin instantane mais pas spammable -- a ajuster lors du POC gameplay)
- EffectValue = 0.0 pour Buff et Debuff (la valeur d'effet sera definie dans BP_Spell_Buff/Debuff)
- SpellName en Text (localisable), Deity en Name (correspondra aux keys de UnlockedSpells)

---

#### [J-10/J-11] BILAN SESSION -- 11/05/2026

**Cree (filesystem) :**
- `Content/Systems/Magic/` dossier ✅

**A creer dans l'editeur UE5 (dans l'ordre) :**
1. `E_SpellCategory` (Enumeration) dans Content/Systems/Magic/
2. `E_SpellTarget` (Enumeration) dans Content/Systems/Magic/
3. `FSoM_SpellData` (Structure) dans Content/Systems/Magic/
4. `BP_MagicComponent` (ActorComponent Blueprint) dans Content/Systems/Magic/
5. Ajout BP_MagicComponent sur BP_PlatformingCharacter (composant "MagicComponent")
6. `DT_Spells` (Data Table, row struct = FSoM_SpellData) dans Content/Systems/Magic/ -- 4 lignes Lumina

**Points d'attention critiques :**
- ConsumeMana DOIT passer par SetStatValue (convention centrale du projet -- jamais SET direct)
- SpellCooldowns doit etre decrement chaque tick si valeur > 0 (ajouter logic dans Tick ou via Timer)
- QuickslotSlots : initialiser avec 4 elements Name vides ("") au BeginPlay pour eviter les out-of-bounds
- UnlockDeity pour Lumina doit etre appelee au debut du jeu (dans GameMode ou au BeginPlay de BP_PlatformingCharacter)

**Dependances avec les jalons suivants (J-12 a J-14) :**
- J-12 : BP_SpellBase + enfants BP_Spell_Heal, BP_Spell_Attack, BP_Spell_Buff, BP_Spell_Debuff
- J-13 : UI_RadialMagic (2 niveaux, slow-mo 0.15x) + UI_QuickslotBar
- J-14 : Integration complete (CastSpell orchestre DT lookup + BP_SpellBase spawn + OnSpellCast)

---

### 11/05/2026 -- SESSION NETTOYAGE PRIORITE 2 (agent Claude Code)

**Action** : Verification des references et suppression des vestiges identifies lors de l'audit.
Methodologie : recherche binaire (Latin1/CP1252) dans tous les .uasset/.umap du projet, plus Config/.ini et .uproject.

---

#### [C3] ThirdPerson vestiges -- verification references

**Verification effectuee** :
- `BP_ThirdPersonCharacter.uasset` : 0 reference externe → SUPPRIME
- `BP_ThirdPersonGameMode.uasset` : 0 reference externe → SUPPRIME
- `ThirdPerson/Lvl_ThirdPerson.umap` : 0 reference externe (doublon de Maps/Lvl_ThirdPerson) → SUPPRIME
- `ThirdPerson/MI_ThirdPersonColWay.uasset` : 0 reference dans Lvl_Platforming (c'est la copie Maps/ qui est referencee) → SUPPRIME
- Dossier `Content/ThirdPerson/` : vide apres suppression → SUPPRIME

**Non supprime -- reference active** :
- `Maps/MI_ThirdPersonColWay.uasset` : reference par `Lvl_Platforming.umap` → CONSERVER
- `Maps/Lvl_ThirdPerson.umap` : map avec ExternalActors (`__ExternalActors__/Maps/Lvl_ThirdPerson/`), statut vestige a confirmer → A INVESTIGUER EN EDITEUR

**Pourquoi** : Nettoyage du dossier ThirdPerson/ residuel du template (jalon #4 n'avait supprime que les BPs dans Players/Blueprint, pas ceux dans ThirdPerson/).
**Points d'attention** : MI_ThirdPersonColWay (Maps/) reste reference dans Lvl_Platforming -- verifier si c'est intentionnel ou vestige du template (coloring waypoint?).

---

#### [C4] BP_PlatformingGameMode -- verification references

**Verification effectuee** :
- `Lvl_Platforming.umap` contient une reference a `BP_PlatformingGameMode` (World Settings override de GameMode)
- `Lvl_Platforming.umap` NE reference PAS `BP_SoM_GameMode` → la map utilise ENCORE l'ancien GameMode !
- `DefaultEngine.ini` : GlobalDefaultGameMode = BP_SoM_GameMode (correct)

**Decision** : NE PAS SUPPRIMER -- la suppression corromprait Lvl_Platforming.umap.
**Fix requis (editeur)** : Ouvrir Lvl_Platforming -> World Settings -> GameMode Override -> vider ou pointer vers BP_SoM_GameMode -> SAVE. Ensuite BP_PlatformingGameMode peut etre supprime proprement via l'editeur.
**Risque actif** : Si Nico ouvre Lvl_Platforming pour tester, les sessions demarrent avec BP_PlatformingGameMode sans BP_PlatformingPlayerController assign correctement.

---

#### [I1] Animations en double -- verification references

**Verification effectuee** :
- `Content/Characters/Players/Animations/AM_Heavy/Light_Sword_*` : reference par `BP_PlatformingCharacter.uasset`
- `Content/Weapons/Animation/AM_Heavy/Light_Sword_*` : reference par `Systems/Combo/DT_Combo_Sword.uasset`, `DT_Combo_2HSword.uasset`, `Datatable_FCombo.uasset`

**Situation** : Les DEUX sets sont actifs et references par des systemes differents.
- BP_PlatformingCharacter utilise Players/Animations/ (versions locales au personnage)
- Les DataTables combo utilisent Weapons/Animation/ (source canonique logique)

**Decision** : AUCUNE SUPPRESSION possible sans editeur. Consolidation requise :
1. Dans l'editeur, ouvrir BP_PlatformingCharacter
2. Rediriger les references AM_ vers Weapons/Animation/
3. Sauvegarder et supprimer les copies Players/Animations/ via l'editeur (avec redirecteurs)

---

#### [I2] IMC -- verification references

**Verification effectuee** :
- `IMC_Default` (Input/ et InputMappings/) : 0 reference dans les binaires .uasset/.umap
- `IMC_Platforming` (Input/) : 0 reference dans les binaires .uasset/.umap
- `IMC_Prototype` (InputMappings/) : reference par `BP_PlatformingCharacter.uasset` ET `BP_PlatformingPlayerController.uasset`
- Config/ : aucune reference IMC dans les .ini

**Situation** : Seul IMC_Prototype est charge par des Blueprints. IMC_Default et IMC_Platforming semblent orphelins dans les assets binaires.
**Decision** : Investigation requise dans l'editeur (Enhanced Input UI, variable defaults) avant toute suppression.
**Points d'attention** : Si IMC_Default et IMC_Platforming sont vraiment inutilises, cela expliquerait pourquoi certaines actions mappees ne fonctionnent que via IMC_Prototype.

---

#### [I5] Input Actions debug -- verification references

**Verification effectuee** :
- `IA_inflictdamage` : reference par `IMC_Prototype.uasset` ET `BP_PlatformingPlayerController.uasset` → CONSERVER
- `IA_KillDummyNow` : reference par `IMC_Prototype.uasset` → CONSERVER
- `IA_TestFloat` : 0 reference externe → SUPPRIME
- `IA_Test_AttachWaepon` : 0 reference externe (la ref dans IA_UI_TestFloat etait fausse) → SUPPRIME
- `IA_UI_TestFloat` : 0 reference externe reelle → SUPPRIME

**Pourquoi** : Ces 3 IA n'ont aucun binding actif et polluent le projet. IA_inflictdamage et IA_KillDummyNow sont bindes dans IMC_Prototype (features de debug volontairement conservees).

---

#### [I4] Reorganisation dossier Enemies

**Decision** : NE PAS FAIRE depuis le filesystem -- deplacement de .uasset briserait les references entre blueprints.
**Fix requis (editeur)** : Dans l'editeur UE5, utiliser le navigateur de contenu pour deplacer les assets (UE cree des redirecteurs automatiquement).
Assets a deplacer vers `Enemies/Blueprints/` : `BP_Enemy_Sword01`, `BP_EnemyWeapon_Sword`, `BP_test_IA`

---

#### BILAN FINAL SESSION -- 11/05/2026

**Suppressions effectuees (filesystem direct -- 0 reference active confirmee) :**
- [C3] `Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset` ✅
- [C3] `Content/ThirdPerson/Blueprints/BP_ThirdPersonGameMode.uasset` ✅
- [C3] `Content/ThirdPerson/Lvl_ThirdPerson.umap` ✅
- [C3] `Content/ThirdPerson/MI_ThirdPersonColWay.uasset` ✅
- [C3] Dossier `Content/ThirdPerson/` (vide) ✅
- [I5] `Content/Input/InputActions/IA_TestFloat.uasset` ✅
- [I5] `Content/Input/InputActions/IA_Test_AttachWaepon.uasset` ✅
- [I5] `Content/Input/InputActions/IA_UI_TestFloat.uasset` ✅

**InputActions restantes (16) -- toutes valides :**
IA_Attack_Heavy, IA_Attack_Light, IA_Block, IA_DebugToggleUI, IA_Dodge,
IA_inflictdamage (debug actif), IA_Jump, IA_KillDummyNow (debug actif),
IA_LockOn, IA_Look, IA_Move, IA_RadialMenu, IA_Sprint, IA_SwitchTarget,
IA_UI_RadialMenu_Rotate, IA_validate_radial_selection

**Actions requises en editeur (ne pas faire depuis filesystem) :**
1. [C4] Lvl_Platforming -> World Settings -> GameMode Override = BP_SoM_GameMode (actuellement pointe encore sur BP_PlatformingGameMode). Apres fix, supprimer BP_PlatformingGameMode via le navigateur de contenu.
2. [I1] BP_PlatformingCharacter : rediriger les references AM_Heavy/Light_Sword_* vers Weapons/Animation/ au lieu de Players/Animations/. Supprimer ensuite les copies Players/Animations/AM_*.
3. [I2] Verifier dans l'editeur si IMC_Default et IMC_Platforming sont actifs (aucune reference trouvee dans les binaires). Si orphelins, supprimer via le navigateur de contenu.
4. [I4] Navigateur de contenu : deplacer BP_Enemy_Sword01, BP_EnemyWeapon_Sword, BP_test_IA vers Enemies/Blueprints/ (UE gere les redirecteurs automatiquement).

---

### 11/05/2026 -- Mise en place du fichier
- Creation du fichier Session_UnrealClaude.md
- Workflow dual-agent mis en place (voir CLAUDE.md section "Workflow dual-agent")
- A partir de maintenant : toutes les actions UE sont loguees ici

---

### 11/05/2026 -- AUDIT COMPLET DU PROJET (agent Claude Code)

**Action** : Audit filesystem complet du projet SoM_250617 apres migration UE5.7 / jalon #8.
Analyse de la structure des assets, configs, plugins et conventions.
Aucune modification Blueprint effectuee -- audit lecture seule.

---

## RAPPORT D'AUDIT -- 11/05/2026

### CRITIQUES (a traiter en priorite)

#### [C1] Plugin GenerativeAISupport -- dossier fantome + config residuelle
- **Symptome** : `Plugins/GenerativeAISupport/` existe mais est VIDE (plugin supprime au jalon #8 mais dossier non nettoye)
- **Config residuelle** : `Config/DefaultGame.ini` contient encore :
  ```
  [/Script/GenerativeAISupportEditor.GenerativeAISupportSettings]
  bAutoStartSocketServer=True
  ```
- **Risque** : UE5 genere des warnings au startup car il cherche le module `GenerativeAISupportEditor` qui n'existe plus. Potentiel crash ou comportement imprévisible du socket server.
- **Fix** : Supprimer `Plugins/GenerativeAISupport/` + nettoyer ces 2 lignes dans `DefaultGame.ini`

#### [C2] UnrealClaude non declare dans .uproject
- **Symptome** : `Plugins/UnrealClaude/` present et compile (v1.4.5), mais le fichier `SoM_250617.uproject` ne le declare pas dans sa liste Plugins
- **Risque** : UE detecte les plugins locaux automatiquement, donc ca fonctionne en pratique. Mais si quelqu'un clone le repo et ouvre le projet, le plugin pourrait ne pas etre active selon la version d'UE. Aussi : le plugin n'apparait pas dans les settings Plugins de l'editeur comme "enabled".
- **Fix** : Ajouter dans `SoM_250617.uproject` : `{"Name": "UnrealClaude", "Enabled": true}`

#### [C3] Vestiges ThirdPerson toujours presents malgre jalon #4
- **Blueprints** :
  - `Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset` -- vestige
  - `Content/ThirdPerson/Blueprints/BP_ThirdPersonGameMode.uasset` -- vestige
- **Maps** :
  - `Content/ThirdPerson/Lvl_ThirdPerson.umap` -- doublon de `Content/Maps/Lvl_ThirdPerson.umap`
- **Materials** :
  - `Content/ThirdPerson/MI_ThirdPersonColWay.uasset` -- vestige
  - `Content/Maps/MI_ThirdPersonColWay.uasset` -- doublon de ce meme materiau
- **Risque** : Ces assets ne sont pas references dans le GameMode actif, mais ils pollutent le projet et peuvent etre accidentellement references. Le jalon #4 a supprime les doublons d'InputActions mais n'a pas nettoye le dossier ThirdPerson/.
- **Fix** : Verifier les references (asset_referencers dans UE), puis supprimer si non references.

#### [C4] BP_PlatformingGameMode -- vestige ou utilise ?
- `Content/Characters/Players/Blueprint/BP_PlatformingGameMode.uasset` existe encore
- Le GameMode actif est `BP_SoM_GameMode` (declare dans DefaultEngine.ini)
- **Risque** : Si BP_PlatformingCharacter ou une map reference encore ce vieux GameMode, les sessions de jeu pourraient demarrer avec le mauvais GameMode (sans BP_PlatformingPlayerController assigned), cassant Lock-On et Radial Menu.
- **Fix** : Verifier via asset_referencers, supprimer si non reference.

---

### IMPORTANTS (a planifier)

#### [I1] Doublons d'animations -- confusion de source
Les montages suivants existent en DOUBLE :
- `Content/Characters/Players/Animations/AM_Heavy_Sword_1.uasset`
  ET `Content/Weapons/Animation/AM_Heavy_Sword_1.uasset`
- `Content/Characters/Players/Animations/AM_Light_Sword_1.uasset`
  ET `Content/Weapons/Animation/AM_Light_Sword_1.uasset`
- `Content/Characters/Players/Animations/AM_Light_Sword_2.uasset`
  ET `Content/Weapons/Animation/AM_Light_Sword_2.uasset`
- **Risque** : Si les deux sont references par des Blueprints differents, une modif sur l'un ne se repercutera pas sur l'autre. Source de bugs silencieux sur les combos.
- **Fix** : Determiner la source canonique (Weapons/Animation/ logiquement), verifier les references, rediriger et supprimer les doublons.

#### [I2] Doublons IMC -- structure incohérente
- `Content/Input/IMC_Default.uasset` (dans Input/ directement)
- `Content/Input/InputMappings/IMC_Default.uasset` (dans sous-dossier)
- `Content/Input/IMC_Platforming.uasset` (dans Input/ directement -- pas dans InputMappings/)
- `Content/Input/InputMappings/IMC_Prototype.uasset` (dans sous-dossier -- pas dans Input/)
- **Etat attendu** (CLAUDE.md) : source unique Content/Input/InputActions/, IMC actifs : IMC_Default, IMC_Platforming, IMC_Prototype
- **Probleme** : IMC_Default existe en 2 exemplaires ; IMC_Platforming et IMC_Prototype sont dans des endroits differents.
- **Fix** : Consolider tous les IMC dans Content/Input/InputMappings/, verifier lequel des 2 IMC_Default est le bon, supprimer les doublons.

#### [I3] ProjectName toujours "Third Person BP Game Template"
- `Config/DefaultGame.ini` : `ProjectName=Third Person BP Game Template`
- **Risque** : Faible (cosmétique), mais peut preter a confusion dans les rapports d'erreur UE et le packaging.
- **Fix** : Changer en `ProjectName=Shadow of Mana`

#### [I4] Structure dossier Enemies incohérente
Assets mixes entre `Content/Characters/Enemies/` et `Content/Characters/Enemies/Blueprints/` :
- **Directement dans Enemies/** : `BP_Enemy_Sword01`, `BP_EnemyWeapon_Sword`, `BP_test_IA`, `SKM_EnemySword_01`, `SKM_EnemySword_01_Skeleton`, `AM_Enemy_Light_Sword_1`
- **Dans Enemies/Blueprints/** : `BP_EnemyBase`, `BP_Enemy_Knight`, `BP_enemyTest`, `BT_Enemy`, `BB_enemy`
- **Convention attendue** (CLAUDE.md) : `BP_EnemyBase` -> `BP_AIController_Enemy_Base`
- **Fix** : Deplacer les BPs de test et assets Enemies dans Blueprints/, nettoyer

#### [I5] Input Actions de debug non nettoyees
Les IA suivantes sont clairement des actions de debug/test qui polluent Content/Input/InputActions/ :
- `IA_inflictdamage` -- debug damage
- `IA_KillDummyNow` -- debug kill
- `IA_Test_AttachWaepon` -- **FAUTE DE FRAPPE** (Waepon au lieu de Weapon) + test
- `IA_TestFloat` -- test
- `IA_UI_TestFloat` -- test
- **Risque** : Ces IA peuvent etre accidentellement bindees. La faute de frappe sur IA_Test_AttachWaepon peut empecher de la retrouver en cherchant "Weapon".
- **Fix** : Verifier si encore bindees dans des IMC ou Blueprints, supprimer si non utilisees.

---

### MINEURS / A SURVEILLER

#### [M1] Deux Animation Blueprints pour le personnage joueur
- `Content/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed.uasset`
- `Content/Characters/Players/Animations/ABP_Manny_Platforming.uasset`
- A verifier : lequel est assigne au Skeletal Mesh de BP_PlatformingCharacter ?
- L'autre est-il un vestige ou en cours de dev ?

#### [M2] Animations pistol/rifle du template -- poids mort
- `Content/Characters/Mannequins/Anims/Pistol/` et `Anims/Rifle/` contiennent ~30 animations
- Ces animations (MM_Pistol_*, MM_Rifle_*) ne sont pas pertinentes pour un ARPG melee/magic
- Poids dans le projet mais pas de risque fonctionnel
- A deplacer dans Dev/SandBox ou supprimer lors d'une session de nettoyage

#### [M3] Input Touch -- pertinence a verifier
- `Content/Input/Touch/` : UI_Thumbstick, UI_TouchSimple, BPI_TouchInterface
- `Content/Input/BPI_TouchInterface_Platforming.uasset`, `UI_TouchInterface_Platforming.uasset`
- Pas pertinent pour un ARPG PC/console. Vestige du template ?

#### [M4] IA_UI_RadialMenu_Rotate -- possible doublon
- `IA_RadialMenu.uasset` ET `IA_UI_RadialMenu_Rotate.uasset` coexistent
- A verifier si les deux sont utilises ou si l'un est un vestige

#### [M5] 3 maps actives -- clarifier le scope
- `Content/Maps/Lvl_Platforming.umap` -- map principale (?)
- `Content/Maps/NewMap.umap` -- map par defaut dans DefaultEngine.ini
- `Content/Maps/Lvl_ThirdPerson.umap` -- vestige ThirdPerson ?
- La map de dev actif devrait etre clairement identifiee. NewMap est un nom generique a renommer.

---

### POSITIF -- Ce qui est bien en place

- Architecture stat (SetStatValue + OnStatChanged) : correctement implementee selon CLAUDE.md
- GameMode et DefaultMap correctement configures dans DefaultEngine.ini
- Source unique InputActions/ : en place (a consolider, voir I2)
- UI event-driven (zero polling) : architecture documentee et en place (jalon #6)
- iframes dash/roll (bIsInvincible) : en place (jalon #5)
- Docs/Architecture/ : bien fourni (14 fichiers d'archi documentes)
- UnrealClaude v1.4.5 : compile et operationnel
- Systeme armes data-driven (DT_Weapons) : en place

---

### PLAN D'ACTION SUGGERE

**Priorite 1 (a faire des la prochaine session)**
1. [C1] Supprimer `Plugins/GenerativeAISupport/` (dossier vide) + nettoyer `DefaultGame.ini`
2. [C2] Ajouter UnrealClaude dans `SoM_250617.uproject`
3. [I3] Renommer ProjectName en "Shadow of Mana" dans `DefaultGame.ini`

**Priorite 2 (session nettoyage)**
4. [C3] Verifier et supprimer vestiges ThirdPerson (Blueprints, maps, materials)
5. [C4] Verifier et supprimer BP_PlatformingGameMode si non reference
6. [I1] Consolider les animations en double
7. [I2] Consolider les IMC dans un seul dossier
8. [I4] Reorganiser la structure dossier Enemies
9. [I5] Nettoyer les IA de debug

**Priorite 3 (quand besoin)**
10. [M1] Clarifier quel ABP est actif
11. [M5] Renommer NewMap + clarifier la map de dev

---

*Audit effectue par l'agent Claude Code (claude-sonnet-4-6) -- lecture seule, aucune modification Blueprint.*
*Le rapport est base sur l'analyse du filesystem et des fichiers de config (les .uasset sont binaires).*
*Pour un audit interne des graphs Blueprint, utiliser les outils MCP blueprint_query dans le panel UnrealClaude.*
