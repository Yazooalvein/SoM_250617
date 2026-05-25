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

### BP_MagicComponent -- VALIDE PIE
- UnlockedSpells : TMap<FName, FSoM_DeitySpells> -- alimente au BeginPlay (stub test)
- UnlockDeity(DeityName) : Map_Add via Set Members in FSoM_DeitySpells (fix bDefaultValueIsIgnored)
- CastSpell(SpellID) : lookup DT_Spells -> Spawn -> Execute -> ConsumeMana
- Stub BeginPlay : UnlockDeity("Lumina") avec 4 sorts [Lumina_Attack, Lumina_Heal, Lumina_Buff, Lumina_Debuff]

### Radial Magie 2 niveaux -- VALIDE PIE
- N1 (Deity) : ecoles debloquees depuis UnlockedSpells
- N2 (Spell) : 4 sorts de l'ecole selectionnee
- CastSpell depuis N2 : fonctionne PIE

### Dette C1-MagicUnlockSystem
- Le stub BeginPlay est temporaire
- Implementer UnlockSpell(SchoolID, SpellID) pour un deblocage progressif reel
- Chaque nouvelle ecole (Ondine, Ombre...) = nouveau DT_Spells + UnlockSpell calls
- Planifier apres C1-MagicProgressionDesign

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
├── SpellTier (E_SpellTier)       // Base, TreeActive, Ulti -- a ajouter
├── ManaCost (Float)
├── CastTime (Float)              // 0.0 = instantane
├── Cooldown (Float)
├── TargetType (E_SpellTarget)    // Enemy, Self, Area
├── EffectValues (Float)          // degats, soin, valeur buff/debuff
├── Duration (Float)              // pour buffs/debuffs
├── AffectedStat (Name)           // stat modifiee (ex: "HealthMax", "MoveSpeed")
├── DeliveryType (E_DeliveryType) // Direct, Projectile, AOE (futur)
├── ReplacesSpellID (Name)        // si evolution : SpellID du sort de base remplace
└── SpellClass (BP_SpellBase)     // classe Blueprint a spawner
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
│   ├── TempSpellsIDs : Array<Name>                    // [Attack, Heal, Buff, Debuff] par defaut
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
│   ├── UnlockDeity(DeityName)       // Map_Contains -> FALSE -> Set Members -> Map_Add
│   └── IsSpellUnlocked(SpellID) : Bool
└── Dispatchers
    ├── OnSpellCast(SpellID)
    └── OnSpellLevelUp(SpellID, NewLevel)
```

**Note FSoM_DeitySpells :** struct helper `{SpellIDs: Array<Name>}` pour contourner la limite
Blueprint Map<Name, Array<Name>>.

**Note Set Members :** utiliser "Set Members in FSoM_DeitySpells" et NON "Make FSoM_DeitySpells"
pour alimenter le Map_Add -- le pin SpellIDs de Make a bDefaultValueIsIgnored=True dans UE5.

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
- [ ] C1-MagicUnlockSystem : UnlockSpell(SchoolID, SpellID) + systeme usage/niveau/points
- [ ] Retirer stub BeginPlay quand UnlockSpell opere en jeu
- [ ] Ajouter SpellTier + ReplacesSpellID dans FSoM_SpellData
- [ ] Ajouter DeliveryType (E_DeliveryType) dans FSoM_SpellData
- [ ] Refactorer BP_Spell_Buff/Debuff pour lire AffectedStat depuis SpellData
- [ ] UI_QuickslotBar (HUD permanent) + UI_MagicConfig (hors combat)
- [ ] Binding input -> Quickslots
- [ ] BP_Spell_Attack_Projectile et BP_Spell_Attack_AOE

---

## Historique

- Creation : 11/05/2026
- MAJ : 12/05/2026 -- POC logique complet, hierarchie sorts
- MAJ : 25/05/2026 -- C1-RadialMagie VALIDE PIE, architecture UnlockDeity finale,
  fix bDefaultValueIsIgnored, variables TempDeitySpells/TempSpellsIDs,
  note Set Members obligatoire
- MAJ : 25/05/2026 -- C1-MagicProgressionDesign VALIDE : section Progression Magique ajoutee,
  boucle usage->niveau->points->arbre, structure arbre par deite, variables BP_MagicComponent
  etendues (SpellUsageCounts, SpellLevels, TalentPoints, dispatchers OnSpellLevelUp)
