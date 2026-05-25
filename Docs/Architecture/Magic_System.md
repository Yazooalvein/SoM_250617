# Architecture -- Systeme de Magie

Document de reference pour l'implementation du systeme de magie de Shadow of Mana.
A lire avant toute implementation Blueprint liee a la magie.

---

## Vision design

La magie est un systeme independant du combat physique -- deux ressources separees (Stamina / Mana),
deux roues distinctes, deux philosophies d'acces. Elle peut sauver une situation desesperee
mais ne remplace pas un cac maitrise. Utiliser trop de magie a des consequences
(voir Corruption Magique, module futur).

**Standardisation des sorts** : chaque deite dispose exactement de 4 sorts de base :
- 1 Attaque
- 1 Heal
- 1 Buff
- 1 Debuff

Ces 4 sorts sont disponibles immediatement a l'acces a la deite. Les sorts supplementaires
et evolutions passent par l'arbre de talent (voir section Progression Magique).

---

## ETAT ACTUEL (25/05/2026)

### Data layer deites -- VALIDE PIE

#### Nouveaux enums
- `E_SpellTier` : Base / TreeActive / TreeEvolution / Ultime
- `E_NodeType` : Active / Passive / Ultime

#### Nouvelles structs
- `FSoM_DeityData` : DeityID (Name), DeityName (Text), Icon (Texture2D), UnlockOrder (Int), BaseSpells (Array<Name>)
- `FSoM_TalentNode` : NodeID, DeityID, NodeType (E_NodeType), SpellID, PassiveStat, PassiveValue (Float), PointCost (Int), Prerequisites (Array<Name>)

#### FSoM_SpellData -- champs ajoutes
- SpellTier (E_SpellTier) : Base sur les 4 sorts Lumina existants
- ReplacesSpellID (Name) : vide par defaut, utilise pour les evolutions d'arbre

#### DataTables
- `DT_Deities` : row Lumina (UnlockOrder=1, Icon=placeholder, BaseSpells=[Lumina_Attack, Lumina_Heal, Lumina_Buff, Lumina_Debuff])
- `DT_TalentNodes` : vide, pret pour C1-MagicTreeModule

#### Convention BaseSpells
Ordre fixe pour toutes les deites : [0=Attack, 1=Heal, 2=Buff, 3=Debuff]
Source de verite pour l'ordre d'affichage dans le radial N2.

### BP_MagicComponent -- UnlockDeity refactore -- VALIDE PIE
- Avant : TempSpellsIDs hardcode en default value (mode dummy)
- Apres : GetDataTableRow(DT_Deities, DeityName) -> BreakStruct -> BaseSpells -> Set Members in FSoM_DeitySpells -> Map_Add
- TempSpellsIDs supprime
- GOTCHA : Map_Contains retourne TRUE si deja present -> branch TRUE = return (ne rien faire), FALSE = debloquer
  (logique contre-intuitive -- inverser produit un bug silencieux : UnlockedSpells vide, radial vide)

### UI_Radial_Main -- PopulateMagicSchools refactore -- VALIDE PIE
- Avant : Conv_NameToText(Map Key) -> DisplayName, Icon null
- Apres : GetDataTableRow(DT_Deities, Map Key) -> BreakStruct -> DeityName + Icon -> MakeStruct FSoM_RadialSlotData
- Row Not Found : non connecte = skip silencieux (deite non referencee dans DT ignoree)

### Radial Magie 2 niveaux -- VALIDE PIE
- N1 (Deity) : ecoles debloquees depuis UnlockedSpells, icone reelle affichee
- N2 (Spell) : 4 sorts depuis UnlockedSpells[DeityID].SpellIDs (alimentes par DT_Deities.BaseSpells)
- CastSpell depuis N2 : fonctionne PIE

### Dette C1-MagicUnlockSystem
- Stub BeginPlay Lumina toujours present (UnlockDeity("Lumina") au BeginPlay)
- A retirer quand C1-MagicUnlockSystem gere le deblocage en jeu
- C1-MagicTreeModule : implementation arbre de talent (apres Menu Principal)

---

## Progression Magique (C1-MagicProgressionDesign -- DESIGN VALIDE 25/05/2026)

### Boucle de progression

> **Utilise tes sorts -> ils progressent -> tu gagnes des points -> tu debloques l'arbre -> l'arbre modifie tes sorts**

Pas de grind d'XP generique. Chaque progression est le resultat direct du jeu.

### Montee en niveau des sorts de base

- Chaque sort de base monte en niveau via l'utilisation (comptage du nombre de lancements)
- Seuils de passage de niveau : a calibrer selon la duree de vie cible du jeu
- La montee en niveau ameliore le sort (puissance, effet -- a definir sort par sort)

### Points de talent

- **A chaque montee de niveau d'un sort -> gain d'un point de talent**
- Les points sont depenses dans l'arbre de la deite correspondante
- Le total de points accumulables est volontairement insuffisant pour completer l'arbre entier
  -> choix force -> builds differents -> rejouabilite

### Structure de l'arbre par deite

```
Arbre de talent par deite
├── 3-4 noeuds actifs
│   ├── Sort supplementaire (s'ajoute au pool du radial/quickslots)
│   └── Evolution d'un sort de base (REMPLACE le sort de base -- pas de coexistence)
├── 2-3 noeuds passifs (bonus permanents lies a la deite)
└── 1 ulti (bout d'arbre -- condition alternative possible, a definir)
```

**Coherence avec le systeme armes :** le nombre de niveaux de sorts doit correspondre
aux niveaux d'armes pour une progression globale coherente. Valeurs exactes a calibrer
lors de la definition de la duree de vie du jeu.

### Gestion des deites

- Toutes les deites se debloquent au fil de la progression (narratif ou condition de jeu)
- Aucun cout de switch entre deites
- Pas d'equipement de deite : une deite debloquee est definitivement accessible
- Apparition immediate dans le radial et/ou menu quickslots au deblocage
- Moment narratif/UI de presentation prevu mais non encore defini (non bloquant)

### Points ouverts pour C1-MagicUnlockSystem

| Question | Statut |
|---|---|
| Seuils de montee en niveau (nb utilisations) | A calibrer |
| Nombre exact de noeuds par arbre | Depend duree de vie jeu / coherence niveaux armes |
| Condition deblocage ulti (bout d'arbre ou autre) | A definir |
| Conditions deblocage deites (narratif / quete / zone) | A definir |
| Points max accumulables vs noeuds totaux (ratio) | A calibrer |
| Presentation UI deite debloquee | A definir (non bloquant) |

---

## Ressource : Mana

- Jauge independante de la Stamina
- Nommage : ManaCurrent / ManaMax
- Modification uniquement via SetStatValue("ManaCurrent", valeur) -- jamais de SET direct
- Pas de regeneration de base -- ressource a gerer comme des munitions
- La regen Mana vient uniquement de : buff actif, potion, equipement dedie

---

## Cast time

| Type | Cast time | Exemples |
|------|-----------|----------|
| Instantane | CastTime = 0.0 | Soin d'urgence, buff rapide, debuff simple |
| Avec cast time | CastTime > 0.0 | Attaque puissante, sort de zone |

Pendant un cast time : heros vulnerable, mouvement bloque, sort interrompable (sans consommer Mana).

---

## Acces aux sorts -- deux systemes

### 1. Radial Magie (acces complet)

Navigation hierarchique en deux niveaux :

**Niveau 1 -- Roue des elements (Deity)**
- Affiche les deites debloquees uniquement (filtrage UnlockedSpells)
- Effet monde : slow-mo 0.2x (SetGlobalTimeDilation)

**Niveau 2 -- Roue des sorts (Spell)**
- 4 sorts de base par deite + sorts supplementaires debloques via arbre
- Validation = CastSpell direct + CloseRadial
- Retour niveau 1 : bouton Cancel

### 2. Quickslots (acces rapide)

- 4 emplacements assignables librement (sorts de base ET sorts d'arbre)
- Configuration hors combat uniquement (menu general)
- Declenchement : mini roue a 4 entrees, temps reel (pas de slow-mo)
- Cooldowns independants par slot

---

## Ciblage des sorts

| Categorie | Cible |
|-----------|-------|
| Attaque | Cible lockee en priorite, sinon ennemi le plus proche |
| Debuff | Cible lockee en priorite, sinon ennemi le plus proche |
| Heal | Heros uniquement (extensible aux PNJ compagnons -- module futur) |
| Buff | Heros uniquement (extensible aux PNJ compagnons -- module futur) |

---

## Hierarchie des classes Blueprint

```
BP_SpellBase (Actor -- classe mere)
├── Variables : Caster, Target, SpellData
├── Execute() : ApplyEffect -> Destroy Actor
├── ApplyEffect() : vide, overridee par les enfants
│
├── BP_Spell_Heal
│   └── Toujours identique : HealthCurrent + EffectValues via SetStatValue
│
├── BP_Spell_Buff
│   └── AffectedStat + EffectValues, Timer -> RestoreStats
│
├── BP_Spell_Attack (classe mere des attaques)
│   ├── BP_Spell_Attack_Direct    <- degats instantanes (implemente)
│   ├── BP_Spell_Attack_Projectile <- projectile (futur)
│   └── BP_Spell_Attack_AOE       <- zone de degats (futur)
│
└── BP_Spell_Debuff (classe mere des debuffs)
    ├── BP_Spell_Debuff_Direct    <- debuff instantane (implemente)
    └── BP_Spell_Debuff_AOE       <- debuff de zone (futur)
```

---

## Structure FSoM_SpellData (DataTable)

```
FSoM_SpellData
├── SpellID (Name)
├── SpellName (Text)
├── Deity (Name)                  // Lumina, Luna, Sylphide...
├── Category (E_SpellCategory)    // Attack, Buff, Debuff, Heal, Ultime
├── SpellTier (E_SpellTier)       // Base, TreeActive, TreeEvolution, Ultime
├── ManaCost (Float)
├── CastTime (Float)              // 0.0 = instantane
├── Cooldown (Float)
├── TargetType (E_SpellTarget)    // Enemy, Self, Area
├── EffectValues (Float)          // degats, soin, valeur buff/debuff
├── Duration (Float)              // pour buffs/debuffs
├── AffectedStat (Name)           // stat modifiee (ex: "HealthMax", "MoveSpeed")
├── DeliveryType (E_DeliveryType) // Direct, Projectile, AOE (futur)
├── ReplacesSpellID (Name)        // si TreeEvolution : SpellID du sort de base remplace
└── SpellClass (BP_SpellBase)     // classe Blueprint a spawner
```

---

## Structure FSoM_DeityData (DataTable DT_Deities)

```
FSoM_DeityData
├── DeityID (Name)          -- cle de lookup (ex: "Lumina")
├── DeityName (Text)        -- nom affiche dans le radial N1
├── Icon (Texture2D)        -- icone radial N1
├── UnlockOrder (Int)       -- ordre narratif (1=Lumina, 9=Ondine)
└── BaseSpells (Array<Name>) -- 4 SpellIDs [0=Attack, 1=Heal, 2=Buff, 3=Debuff]
```

## Structure FSoM_TalentNode (DataTable DT_TalentNodes)

```
FSoM_TalentNode
├── NodeID (Name)              -- cle unique (ex: "Lumina_Node_01")
├── DeityID (Name)             -- filtrage par deite
├── NodeType (E_NodeType)      -- Active / Passive / Ulti
├── SpellID (Name)             -- si Active/Ulti : sort debloque (vide si Passive)
├── PassiveStat (Name)         -- si Passive : stat affectee
├── PassiveValue (Float)       -- valeur du bonus passif
├── PointCost (Int)            -- cout en points (defaut 1)
└── Prerequisites (Array<Name>) -- NodeIDs requis avant deblocage
```

---

## Architecture BP_MagicComponent

```
BP_MagicComponent (ActorComponent)
├── Variables
│   ├── UnlockedSpells : Map<Name, FSoM_DeitySpells>  // DeityName -> SpellIDs actifs
│   ├── SpellUsageCounts : Map<Name, Int>              // SpellID -> nb utilisations
│   ├── SpellLevels : Map<Name, Int>                   // SpellID -> niveau actuel
│   ├── TalentPoints : Map<Name, Int>                  // DeityName -> points disponibles
│   ├── TempDeitySpells : FSoM_DeitySpells             // variable helper (SIMPLE, pas Array)
│   ├── QuickslotSlots : Array<Name> (4 slots)
│   ├── SpellCooldowns : Map<Name, Float>
│   └── bIsCasting : Boolean
├── Fonctions
│   ├── CastSpell(SpellID)           // CanCast -> DT lookup -> Spawn -> Execute -> ConsumeMana -> IncrementUsage
│   ├── CanCast(SpellID) : Bool      // Pure : NOT bIsCasting AND cooldown<=0 AND mana>=cost
│   ├── ConsumeMana(Amount)          // SetStatValue("ManaCurrent")
│   ├── IncrementSpellUsage(SpellID) // +1 usage -> check seuil niveau -> LevelUpSpell si atteint
│   ├── LevelUpSpell(SpellID)        // monte niveau + AddTalentPoint(Deity)
│   ├── AddTalentPoint(DeityName)    // +1 dans TalentPoints[DeityName]
│   ├── UnlockTreeNode(NodeID)       // depense point -> active sort/passif dans UnlockedSpells
│   ├── UnlockDeity(DeityName)       // GetDataTableRow(DT_Deities) -> BaseSpells -> Set Members -> Map_Add
│   └── IsSpellUnlocked(SpellID) : Bool
└── Dispatchers
    ├── OnSpellCast(SpellID)
    └── OnSpellLevelUp(SpellID, NewLevel)
```

**Note FSoM_DeitySpells :** struct helper `{SpellIDs: Array<Name>}` pour contourner la limite
Blueprint Map<Name, Array<Name>>.

**Note Set Members :** utiliser "Set Members in FSoM_DeitySpells" et NON "Make FSoM_DeitySpells"
pour alimenter le Map_Add -- le pin SpellIDs de Make a bDefaultValueIsIgnored=True dans UE5.

**Note Map_Contains dans UnlockDeity :** TRUE = deja present -> return sans rien faire.
FALSE = absent -> proceder au deblocage. Logique contre-intuitive, ne pas inverser.

---

## Sorts par deite -- grille standardisee

| Deite | Attaque | Heal | Buff | Debuff |
|-------|---------|------|------|--------|
| Lumina | Rayon de lumiere (Direct) | Soin de Lumina | Bouclier (HealthMax+) | Aveuglement (Speed-) |
| Luna | Rayon de lune (?) | Baume lunaire (?) | Buff lune (?) | Debuff lune (?) |
| Sylphide | Rafale de vent (?) | ? | Vitesse (MoveSpeed+) | ? |
| Gnome | Impact de pierre (?) | ? | Defense (?) | ? |
| Salamandre | Flamme (Direct/Projectile) | ? | Ardeur (?) | Brulure (?) |
| Ombre | Attaque critique (?) | ? | ? | ? |
| Athanor | Forge (?) | ? | Buff arme (?) | ? |
| Dryade | Nature (AOE?) | Soin de zone | ? | ? |
| Ondine | Eau (?) | ? | ? | ? |

---

## Deblocage progressif des deites

| Ordre | Deite | Moment narratif |
|-------|-------|-----------------|
| 1 | Lumina | Debut -- Lumina rejoint le groupe |
| 2 | Luna | Acte 1 -- Luna confirmee |
| 3 | Sylphide | Acte 2 -- Resolution pays du vent |
| 4 | Gnome | Acte 2 -- Colosse rejoint |
| 5 | Salamandre | Acte 2 -- Forgeron/Loup |
| 6 | Ombre | Acte 3 -- Revelation heros |
| 7 | Athanor | Acte 3 -- Forge complete |
| 8 | Dryade | Acte 3 -- Oracle (avant mort) |
| 9 | Ondine | Acte 4 -- Resolution soeur |

---

## Ce qui reste a faire

- [x] BP_MagicComponent : UnlockedSpells + UnlockDeity + CastSpell VALIDE PIE
- [x] Stub BeginPlay Lumina x4 (temporaire)
- [x] Fix bDefaultValueIsIgnored : Set Members in FSoM_DeitySpells
- [x] Radial Magie 2 niveaux VALIDE PIE
- [x] C1-MagicProgressionDesign : spec progression sorts + arbre de talent DESIGN VALIDE
- [x] E_SpellTier + E_NodeType crees
- [x] FSoM_DeityData + FSoM_TalentNode crees
- [x] FSoM_SpellData : SpellTier + ReplacesSpellID ajoutes
- [x] DT_Deities : row Lumina complete (BaseSpells, Icon, UnlockOrder)
- [x] DT_TalentNodes : cree vide
- [x] UnlockDeity : data-driven via DT_Deities (TempSpellsIDs supprime)
- [x] PopulateMagicSchools : DeityName + Icon depuis DT_Deities VALIDE PIE
- [ ] C1-MagicUnlockSystem : UnlockSpell(SchoolID, SpellID) + systeme usage/niveau/points
- [ ] Retirer stub BeginPlay quand UnlockSpell opere en jeu
- [ ] Refactorer BP_Spell_Buff/Debuff pour lire AffectedStat depuis SpellData
- [ ] UI_QuickslotBar (HUD permanent) + UI_MagicConfig (hors combat)
- [ ] Binding input -> Quickslots
- [ ] BP_Spell_Attack_Projectile et BP_Spell_Attack_AOE
- [ ] C1-MagicTreeModule : implementation arbre de talent (apres Menu Principal)

---

## Historique

- Creation : 11/05/2026
- MAJ : 12/05/2026 -- POC logique complet, hierarchie sorts
- MAJ : 25/05/2026 -- C1-RadialMagie VALIDE PIE, architecture UnlockDeity finale,
  fix bDefaultValueIsIgnored, note Set Members obligatoire
- MAJ : 25/05/2026 -- C1-MagicProgressionDesign VALIDE : section Progression Magique ajoutee,
  boucle usage->niveau->points->arbre, structure arbre par deite, variables BP_MagicComponent
  etendues (SpellUsageCounts, SpellLevels, TalentPoints, dispatchers OnSpellLevelUp)
- MAJ : 25/05/2026 -- Data layer deites VALIDE PIE : E_SpellTier, E_NodeType, FSoM_DeityData,
  FSoM_TalentNode, DT_Deities, DT_TalentNodes, UnlockDeity + PopulateMagicSchools data-driven,
  gotcha Map_Contains logique documente
