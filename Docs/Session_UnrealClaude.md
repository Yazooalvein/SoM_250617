# Session_UnrealClaude.md -- Log des actions de l'agent UE

Ce fichier est maintenu par l'agent UnrealClaude et par Nico en temps reel pendant les sessions dans l'editeur.
Il est lu par Claude.ai en debut de session pour rester au courant de tout ce qui a ete fait dans UE.

## Format d'entree

```
### [DATE] -- [NOM DU BLUEPRINT / ASSET]
**Action** : ce qui a ete fait
**Pourquoi** : raison ou contexte
**Points d'attention** : gotchas, dependances, ce qui pourrait casser
```

## Instructions pour l'agent UnrealClaude

- Logue TOUTE modification significative ici, meme les petites
- Sois precis sur les noms de Blueprint, variables, nodes
- Note les decisions prises et pourquoi (pas juste le "quoi" mais le "pourquoi")
- Si quelque chose ne fonctionne pas comme prevu, logue-le aussi
- Claude.ai lit ce fichier : il doit pouvoir comprendre sans avoir ete present
- TOUJOURS utiliser blueprint_modify et blueprint_query — ne jamais utiliser execute_script (risque de crash)

---

## DEMANDE D'AUDIT -- 08/06/2026 -- COMBAT-LockOnRefacto (A TRAITER EN PRIORITE)

**Contexte** : Le jalon COMBAT-LockOnRefacto est en cours de debugging PIE. Deux problemes bloquants :
1. Le lock-on ne s'active pas (AvailableTargets reste vide apres DetectAvailableTargets)
2. Infinite loop detectee dans DeactivateLockOn

**Demande** : Exporter en T3D (blueprint_query) les graphes suivants et noter TOUT noeud avec ErrorType != 0 :

### 1. BP_CombatLockOnComponent -- fonction ActivateLockOn (graphe complet)
- Chemin : /Game/Systems/LockOn/BP_CombatLockOnComponent
- But : verifier le flux apres SelectInitialTarget -- est-ce que bisLockOnActive est bien SET a true ? Y a-t-il un guard qui coupe avant ?

### 2. BP_CombatLockOnComponent -- fonction SelectInitialTarget (graphe complet)
- But : verifier que CurrentTarget est bien SET et que OnLockOnActivated est bien appele

### 3. BP_CombatLockOnComponent -- fonction DetectAvailableTargets -- FOCUS sur le noeud Message IsDeadOrDestroyed
- But : Sur le noeud K2Node_Message "IsDeadOrDestroyed", verifier la valeur exacte de bDefaultValueIsIgnored sur le pin "self". Si True = bug confirme, le noeud ignore la cible.
- Note : ce noeud a deja ete relie directement a ArrayElement mais garde ErrorType=1 ("must have a valid target"). Un delete + recreate from scratch est peut-etre necessaire.

### 4. BP_Enemy_Base -- implementation de IsDeadOrDestroyed (interface BPI_Lockable)
- But : verifier que l'implementation retourne bien (bIsDead OR IsActorBeingDestroyed) et qu'il n'y a pas de logique inversee ou de noeud mort

### 5. BP_Enemy_Base -- custom event OnSelfLocked (graphe complet apres le Cast BP_SoM_HeroCharacter)
- But : verifier que GetComponentByClass(BP_CombatLockOnComponent) est bien appele sur AsBP_SoM_HeroCharacter (le hero) et PAS sur autre chose

**Format de reponse souhaite** : T3D brut pour chaque graphe + note sur les ErrorType trouves

---

## Historique des sessions

---

### 30/05/2026 -- AUDIT C1-HUDCore -- UI_HUD_Main + BP_AttributeSet_Base + BP_SoM_HeroCharacter

**Action** : Discovery uniquement (blueprint_query). Audit ciblé pour préparer le jalon C1-HUDCore (jauges Stamina, Mana, Essence, Corruption).
Assets inspectés : UI_HUD_Main, BP_AttributeSet_Base, BP_SoM_HeroCharacter.

---

#### 1. UI_HUD_Main -- État complet

**Chemin** : `/Game/UI/Widgets/Main/UI_HUD_Main`
**Classe** : WidgetBlueprint
**Total nodes** : 86 (EventGraph: 30 nodes, 4 events ; 5 fonctions dont 3 Function Bindings ProgressBar)

**Variables (5) :**

| Nom | Type | Catégorie | Rôle |
|-----|------|-----------|------|
| `PlayerCharacterRef` | (type non résolu) | UI\|Debug | Référence debug au personnage |
| `AttributeSetRef` | BP_AttributeSet_Base_C* | Default | Reçu via Exposed on Spawn à la création du widget |
| `HealthPercent` | double | Default | Valeur courante jauge Santé (0-1) |
| `StaminaPercent` | double | Default | Valeur courante jauge Stamina (0-1) |
| `ManaPercent` | double | Default | Valeur courante jauge Mana (0-1) |

**ABSENT : EssencePercent, CorruptionPercent -- À CRÉER pour C1-HUDCore**

**Fonctions (5 + EventGraph) :**

| Nom | Type | Rôle |
|-----|------|------|
| `Get_HealthBar_Percent` | Function Binding | Retourne HealthPercent → binding ProgressBar Santé |
| `Get_StaminaBar_Percent` | Function Binding | Retourne ReturnValue → binding ProgressBar Stamina |
| `Get_ManaBar_Percent` | Function Binding | Retourne ReturnValue → binding ProgressBar Mana |
| `InitHUD` | Function | Appelée par HC.Add_Main_HUD après création widget ; fait le Bind Event to OnStatChanged |
| `UpdateStatText` | Function | Appelée après chaque Set {stat}Percent |

**ABSENT : Get_EssenceBar_Percent, Get_CorruptionBar_Percent -- À CRÉER**

**Architecture EventGraph (flow complet) :**
```
Event Construct
  → Bind Event to OnStatChanged (sur AttributeSetRef)
     → HUD_OnStatChanged (Custom Event, params: StatName: Name, NewValue: double)
        → Switch on Name (StatName) :
            HealthCurrent  → Set HealthPercent  = NewValue / HealthMax  → UpdateStatText
            StaminaCurrent → Set StaminaPercent = NewValue / StaminaMax → UpdateStatText
            ManaCurrent    → Set ManaPercent    = NewValue / ManaMax    → UpdateStatText
            HealthMax      → Set HealthPercent  = HealthCurrent / NewValue → UpdateStatText
            StaminaMax     → Set StaminaPercent = StaminaCurrent / NewValue → UpdateStatText
            ManaMax        → Set ManaPercent    = ManaCurrent / NewValue   → UpdateStatText
            [EssenceMana]  → ABSENT
            [Corruption]   → ABSENT
```

Event Tick : présent mais non connecté (0 exec) → architecture event-driven confirmée, pas de polling.

**Bindings ProgressBar :**
- Pattern validé : Function Binding retourne la variable *Percent
- Les 3 fonctions Get_*_Percent existent et sont câblées → Stamina et Mana sont PRÊTES côté BP
- Manque : widgets ProgressBar dans le Designer UMG pour Stamina/Mana (non auditable via blueprint_query) et les deux bindings Essence/Corruption à créer

---

#### 2. BP_AttributeSet_Base -- État complet

**Chemin** : `/Game/Systems/Stats/BP_AttributeSet_Base`
**Classe** : Blueprint (ActorObject)

**Variables (13) :**

| Nom | Type | Catégorie | Statut C1-HUDCore |
|-----|------|-----------|-------------------|
| `HealthCurrent` | double | Stats\|Health | ✅ présent |
| `HealthMax` | double | Stats\|Health | ✅ présent |
| `StaminaCurrent` | double | Stats\|Stamina | ✅ présent |
| `StaminaMax` | double | Stats\|Stamina | ✅ présent |
| `StaminaRegenRate` | double | Stats\|Stamina | ✅ présent |
| `StaminaCostJump` | double | Stats\|Stamina | ✅ présent |
| `StaminaCostDash` | double | Stats\|Stamina | ✅ présent |
| `StaminaRegenDelay` | double | Stats\|Stamina | ✅ présent |
| `StaminaRegenInterval` | double | Stats\|Stamina | ✅ présent |
| `bIsStaminaRegenerating` | bool | Stats\|Stamina | ✅ présent |
| `ManaCurrent` | double | Stats\|Mana | ✅ présent |
| `ManaMax` | double | Stats\|Mana | ✅ présent |
| `OnStatChanged` | mcdelegate | Default | ✅ dispatcher présent |

**Stats ABSENTES (design CLAUDE.md "clés supplémentaires") -- À AJOUTER :**
- `EssenceMana` ❌ -- nécessaire C1-HUDCore
- `EssenceManaDropped` ❌
- `Corruption` ❌ -- nécessaire C1-HUDCore
- `CorruptionMax` ❌ -- nécessaire (Phase 1 = 50, Phase 2 = 100)
- `Level`, `PiecesOr`, `ChanceCritique`, `TenaciteEtat` ❌ -- jalons ultérieurs

**Fonctions (4) :**

| Nom | Inputs | Rôle |
|-----|--------|------|
| `SetStatValue` | StatName: Name, Value: double | Point unique de modification -- Switch on 11 cases + Call OnStatChanged |
| `ConsumeStamina` | Amount: double | Consommation stamina |
| `StartStaminaRegen` | — | Démarrage regen stamina |
| `HandleStaminaRegen` | — | Logique tick regen |

**SetStatValue -- Switch on Name (11 cases actuelles) :**
HealthCurrent, HealthMax, StaminaCurrent, StaminaMax, ManaCurrent, ManaMax,
StaminaCostJump, StaminaCostDash, StaminaRegenRate, StaminaRegenDelay, StaminaRegenInterval

**OnStatChanged dispatcher :**
- Appelé à la fin de chaque branche du Switch (11 connexions sur le Call Delegate node)
- Params : StatName (Name), NewValue (double)
- Architecture correcte : tout SET passe par SetStatValue → OnStatChanged notifie les listeners

**EssenceMana et Corruption : 0 node trouvé dans tout le BP** → inexistants, à créer de zéro.

---

#### 3. BP_SoM_HeroCharacter -- Accès AttributeSet + HUD

**Chemin** : `/Game/Characters/Players/Blueprint/BP_SoM_HeroCharacter`

**Accès à BP_AttributeSet_Base :**
- Variable directe `AttributeSetRef` (BP_AttributeSet_Base_C*, catégorie Stats|Principals)
- Set dans `InitAttributesFromDatatable` (construit depuis `StatsDataTable : DataTable*`)
- Utilisée en 5 points : EventGraph (×2 Get), Add_Main_HUD (×1 Get), InitAttributesFromDatatable (×1 Get + ×1 Set)
- **Pas de GetStatValue exposé** -- l'UI accède directement aux variables via la référence

**Fonction Add_Main_HUD (flux complet) :**
```
Add_Main_HUD :
  1. Create Widget UI_HUD_Main (AttributeSetRef passée en pin Exposed on Spawn)
  2. Add to Viewport (ZOrder 0)
  3. Call InitHUD sur le widget (fait le Bind Event to OnStatChanged dans le widget)
```
→ Injection d'AttributeSetRef au moment de la création du widget : pattern propre, pas de Set post-création.

**OnStatChanged dans HC :**
- **AUCUN binding OnStatChanged dans le HC** (0 résultat "Stat Changed" + "OnStatChanged")
- Le HC ne souscrit pas au dispatcher
- Toute la notification HUD passe par : SetStatValue → OnStatChanged → HUD_OnStatChanged (dans le widget)

**Fonctions HC (8) :**
UserConstructionScript, Aim, Move, Add_Main_HUD, InitAttributesFromDatatable, EquipWeapon(RowName), IsDead() → bool, EventGraph (11 events, 287 nodes)

**Note CurrentWeapon :**
HC.CurrentWeapon (BP_Weapon_Base_C*) est présent en variable -- c'est la référence à l'actor arme physique (spawn/attach HandGrip_R), distinct de ComboManager.CurrentWeaponID (source unique identifiant arme). Non concerné par C1-HUDCore.

---

#### 4. Synthèse : ce qui manque pour C1-HUDCore

| Composant | Manque | Action |
|-----------|--------|--------|
| BP_AttributeSet_Base | Variables EssenceMana, Corruption (+ CorruptionMax) | Ajouter variables + cases SetStatValue |
| UI_HUD_Main (BP) | Variables EssencePercent, CorruptionPercent | Ajouter variables |
| UI_HUD_Main (BP) | Fonctions Get_EssenceBar_Percent, Get_CorruptionBar_Percent | Créer (pattern identique aux 3 existantes) |
| UI_HUD_Main (BP) | Cases EssenceMana + Corruption dans Switch HUD_OnStatChanged | Ajouter au Switch |
| UI_HUD_Main (Designer UMG) | ProgressBars Stamina, Mana, Essence, Corruption (+ bindings) | Créer dans le Designer manuellement |

**Stamina et Mana :** variables et Function Bindings déjà présents côté Blueprint. Manque probablement les ProgressBar widgets dans le Designer UMG (non auditable via blueprint_query).

**Questions ouvertes pour C1-HUDCore :**
1. **EssencePercent** : EssenceMana = valeur absolue perdue à la mort. Y a-t-il un EssenceManaMax ? Ou affichage valeur brute (Text) plutôt que ProgressBar ?
2. **CorruptionMax** : stocker dans AttributeSet (variable `CorruptionMax` switchable Phase1=50/Phase2=100) ou coder en dur dans l'UI ?
3. **Stamina/Mana Designer** : vérifier manuellement dans l'éditeur UMG si les ProgressBar existent déjà dans le Designer

---

*Entrée créée le 30/05/2026 -- Agent UnrealClaude (session panel UE5.7, discovery uniquement)*

---

### 14/05/2026 -- J-NETTOYAGE -- Audit pré-modifications (3 points)

**Action** : Audit de l'état actuel avant nettoyage sur 3 cibles : WeaponDataTest, ancien système radial dans PC, NewEnumerator6 dans EWeaponType.
Source : données Session_UnrealClaude.md du 13/05/2026 (audit binaire confirmé). Session Claude Code CLI, pas panel UnrealClaude.

**Résultats confirmés :**

1. **WeaponDataTest dans BP_PlatformingCharacter**
   - Type : `FWeaponData`
   - Statut : variable debug vestige, non utilisée en production
   - Action prévue : supprimer la variable

2. **Ancien système radial dans BP_PlatformingPlayerController**
   - `RadialMenuRef` (UI_RadialMenu_C) : présente, créée dans OpenRadialMenu
   - `SlotRowNames` (Array\<Name\>) : présente, construite dans OpenRadialMenu
   - `SlotIcons` (Array\<Texture2D\>) : présente, passée à InitializeRadialMenu
   - Fonctions à migrer : OpenRadialMenu, CloseRadialMenu, ToggleRadialMenu, ValidateSelectedWeapon
   - ValidateSelectedWeapon lit encore `RadialMenuRef.SelectedRowName` → doit lire `RadialMainRef.SlotDataList[SelectedIndex].SlotID`
   - `RadialMainRef` (UI_Radial_Main_C) existe dans le WIP — migration à finaliser

3. **NewEnumerator6 dans EWeaponType**
   - 7 enumerateurs (Sword/HSword/Axe/HAxe/Dagger/Bow/NewEnumerator6)
   - NewEnumerator6 : non nommé, vestige probable
   - Action prévue : supprimer ou renommer selon décision Nico

**Points d'attention** :
- Ne pas supprimer WeaponDataTest avant d'avoir confirmé qu'aucun Blueprint n'y fait référence (asset_referencers recommandé)
- Supprimer NewEnumerator6 peut casser AnimBP si Blend Pose by Enum l'utilise — vérifier avant suppression
- Migrer l'ancien radial = modifier OpenRadialMenu + CloseRadialMenu + ValidateSelectedWeapon + supprimer InitializeRadialMenu + RadialMenuRef

**Statut** : ✅ AUDIT VALIDÉ PAR NICO — modifications approuvées

---

### 14/05/2026 -- J-NETTOYAGE -- Plan d'exécution (en attente panel UnrealClaude)

**Action** : Session Claude Code CLI. Audit validé par Nico. Plan d'exécution détaillé établi. Modifications blueprint à exécuter via panel UnrealClaude (outils blueprint_query/blueprint_modify requis).

**Pourquoi** : Claude Code CLI n'a pas accès aux outils MCP blueprint_* — ces outils sont disponibles uniquement dans le panel UnrealClaude de l'éditeur.

**Plan d'exécution validé (ordre 1→2→3) :**

**POINT 1 — BP_PlatformingCharacter : WeaponDataTest**
- asset_referencers sur WeaponDataTest → si 0 référence → supprimer la variable
- Compile + Save

**POINT 2 — BP_PlatformingPlayerController : migration radial (4 fonctions)**
- OpenRadialMenu : remplacer CreateWidget(UI_RadialMenu_C) + InitializeRadialMenu par IsValid(RadialMainRef) → PopulateWeaponSlots() → GenerateSlots()
- CloseRadialMenu : supprimer lecture SelectedRowName sur RadialMenuRef, garder RemoveFromParent + SetInputMode + TimeDilation restore
- ToggleRadialMenu : remplacer IsValid(RadialMenuRef) par IsValid(RadialMainRef)
- ValidateSelectedWeapon : remplacer RadialMenuRef.SelectedRowName par RadialMainRef.SlotDataList[SelectedIndex].SlotID, guard = IsValid(RadialMainRef)
- Supprimer variables : RadialMenuRef (UI_RadialMenu_C), SlotRowNames (Array<Name>), SlotIcons (Array<Texture2D>)
- Compile + Save

**POINT 3 — EWeaponType : NewEnumerator6**
- Ouvrir AnimBP hero → vérifier Blend Pose by Enum → si NewEnumerator6 non connecté → supprimer dans EWeaponType
- Compile + Save

**Points d'attention** :
- IsValid(RadialMainRef) = guard obligatoire sur tous les appels radial (convention projet)
- Si Blend Pose by Enum référence NewEnumerator6, le renommer avant de supprimer

**Statut** : ⏸ EN ATTENTE EXÉCUTION VIA PANEL UNREALCLAUDE

---

*Derniere mise a jour : 08/06/2026 -- Claude.ai (demande audit COMBAT-LockOnRefacto)*
