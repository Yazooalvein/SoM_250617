# Architecture — Système de Magie

Document de référence pour l'implémentation du système de magie de Shadow of Mana.
A lire avant toute implémentation Blueprint liée à la magie.

---

## Vision design

La magie est un système **indépendant du combat physique** — deux ressources séparées (Stamina / Mana), deux roues distinctes, deux philosophies d'accès. Elle peut sauver une situation désespérée mais ne remplace pas un cac maîtrisé. Utiliser trop de magie a des conséquences (voir Corruption Magique, module futur).

**Standardisation des sorts** : chaque déité dispose exactement de 4 sorts :
- 1 Attaque
- 1 Heal
- 1 Buff
- 1 Debuff

Cette règle est fixe pour toutes les déités. Les ultimes sont un système séparé débloqué plus tard.

---

## Ressource : Mana

- Jauge indépendante de la Stamina
- Nommage : `ManaCurrent` / `ManaMax`
- Modification uniquement via `SetStatValue("ManaCurrent", valeur)` — jamais de SET direct
- **Pas de régénération de base** — ressource à gérer comme des munitions
- La regen Mana vient uniquement de : buff actif, potion, équipement dédié

---

## Cast time

| Type | Cast time | Exemples |
|------|-----------|---------| 
| **Instantané** | CastTime = 0.0 | Soin d'urgence, buff rapide, débuff simple |
| **Avec cast time** | CastTime > 0.0 | Attaque puissante, sort de zone |

Pendant un cast time : héros vulnérable, mouvement bloqué, sort interrompable (sans consommer Mana).

---

## Accès aux sorts — deux systèmes

### 1. Radial Magie (accès complet)

Navigation hiérarchique en deux niveaux :

**Niveau 1 — Roue des éléments**
- Affiche les déités débloquées uniquement
- Déclenchement : bouton dédié (différent du radial armes)
- Effet monde : **slow-mo 0.15x** (SetGlobalTimeDilation)

**Niveau 2 — Roue des sorts de l'élément**
- 4 sorts par déité : Attaque / Buff / Débuff / Heal
- Lancement au relâchement de la sélection
- Retour niveau 1 : bouton annuler

### 2. Quickslots (accès rapide)

- 4 emplacements assignables librement
- Configuration hors combat uniquement
- Déclenchement : mini roue à 4 entrées, temps réel (pas de slow-mo)
- Cooldowns indépendants par slot

---

## Ciblage des sorts

| Catégorie | Cible |
|-----------|-------|
| Attaque | Cible lockée en priorité, sinon ennemi le plus proche |
| Débuff | Cible lockée en priorité, sinon ennemi le plus proche |
| Heal | Héros uniquement (extensible aux PNJ compagnons — module futur) |
| Buff | Héros uniquement (extensible aux PNJ compagnons — module futur) |

---

## Hiérarchie des classes Blueprint

```
BP_SpellBase (Actor — classe mère)
├── Variables : Caster, Target, SpellData
├── Execute() : ApplyEffect -> Destroy Actor
├── ApplyEffect() : vide, overridée par les enfants
│
├── BP_Spell_Heal
│   └── Toujours identique : HealthCurrent + EffectValues via SetStatValue
│
├── BP_Spell_Buff
│   └── Toujours identique : AffectedStat + EffectValues, Timer -> RestoreStats
│       La stat modifiée est définie par AffectedStat dans DT_Spells
│
├── BP_Spell_Attack (classe mère des attaques)
│   ├── BP_Spell_Attack_Direct    ← dégâts instantanés (implémenté)
│   ├── BP_Spell_Attack_Projectile ← projectile qui voyage (futur)
│   └── BP_Spell_Attack_AOE       ← zone de dégâts (futur)
│
└── BP_Spell_Debuff (classe mère des debuffs)
    ├── BP_Spell_Debuff_Direct    ← debuff instantané (implémenté)
    └── BP_Spell_Debuff_AOE       ← debuff de zone (futur)
```

**Principe :** Heal et Buff sont toujours identiques entre déités (seuls les paramètres changent).
Attack et Debuff peuvent avoir des sous-classes selon le mode de livraison (Direct, Projectile, AOE).

---

## Structure FSoM_SpellData (DataTable)

```
FSoM_SpellData
├── SpellID (Name)
├── SpellName (Text)
├── Deity (Name)                  // Lumina, Luna, Sylphide...
├── Category (E_SpellCategory)    // Attack, Buff, Debuff, Heal, Ultime
├── ManaCost (Float)
├── CastTime (Float)              // 0.0 = instantané
├── Cooldown (Float)
├── TargetType (E_SpellTarget)    // Enemy, Self, Area
├── EffectValues (Float)          // dégâts, soin, valeur du buff/debuff
├── Duration (Float)              // pour buffs/debuffs
├── AffectedStat (Name)           // stat modifiée par Buff/Debuff (ex: "HealthMax", "MoveSpeed")
├── DeliveryType (E_DeliveryType) // Direct, Projectile, AOE (futur enum)
└── SpellClass (BP_SpellBase)     // classe Blueprint à spawner
```

**Note :** `AffectedStat` et `DeliveryType` à ajouter dans FSoM_SpellData lors de la prochaine session.
`DeliveryType` nécessite la création de l'enum `E_DeliveryType`.

---

## Sorts par déité — grille standardisée

| Déité | Attaque | Heal | Buff | Debuff |
|-------|---------|------|------|--------|
| Lumina | Rayon de lumière (Direct) | Soin de Lumina | Bouclier (HealthMax+) | Aveuglement (Speed-) |
| Luna | Rayon de lune (?) | Baume lunaire (?) | Buff lune (?) | Debuff lune (?) |
| Sylphide | Rafale de vent (?) | ? | Vitesse (MoveSpeed+) | ? |
| Gnome | Impact de pierre (?) | ? | Défense (?) | ? |
| Salamandre | Flamme (Direct/Projectile) | ? | Ardeur (?) | Brûlure (?) |
| Ombre | Attaque critique (?) | ? | ? | ? |
| Athanor | Forge (?) | ? | Buff arme (?) | ? |
| Dryade | Nature (AOE?) | Soin de zone | ? | ? |
| Ondine | Eau (?) | ? | ? | ? |

Les `?` seront définis au fur et à mesure du développement narratif.

---

## Déblocage progressif

| Ordre | Déité | Moment narratif |
|-------|-------|-----------------|
| 1 | Lumina | Début — Lumina rejoint le groupe |
| 2 | Luna | Acte 1 — Luna confirmée |
| 3 | Sylphide | Acte 2 — Résolution pays du vent |
| 4 | Gnome | Acte 2 — Colosse rejoint |
| 5 | Salamandre | Acte 2 — Forgeron/Loup |
| 6 | Ombre | Acte 3 — Révélation héros |
| 7 | Athanor | Acte 3 — Forge complète |
| 8 | Dryade | Acte 3 — Oracle (avant mort) |
| 9 | Ondine | Acte 4 — Résolution sœur |

---

## Architecture BP_MagicComponent

```
BP_MagicComponent (ActorComponent)
├── Variables
│   ├── UnlockedSpells : Map<Name, FSoM_DeitySpells>  // DeityName -> SpellIDs
│   ├── QuickslotSlots : Array<Name> (4 slots)
│   ├── SpellCooldowns : Map<Name, Float>
│   └── bIsCasting : Boolean
├── Fonctions
│   ├── CastSpell(SpellID)       // CanCast -> DT lookup -> Spawn -> Execute -> ConsumeMana
│   ├── CanCast(SpellID) : Bool  // Pure : NOT bIsCasting AND cooldown<=0 AND mana>=cost
│   ├── ConsumeMana(Amount)      // SetStatValue("ManaCurrent")
│   ├── UnlockDeity(DeityName)   // Map Add DeityName -> SpellIDs
│   └── IsSpellUnlocked(SpellID) : Bool  // Pure
└── Dispatcher : OnSpellCast(SpellID)
```

**Note FSoM_DeitySpells :** struct helper `{SpellIDs: Array<Name>}` pour contourner la limite
Blueprint Map<Name, Array<Name>>. Accès : `UnlockedSpells[DeityName].SpellIDs`.

---

## UI (à implémenter — J-13)

```
UI_RadialMagic
├── Niveau 1 : roue des éléments (déités débloquées)
└── Niveau 2 : roue des sorts (4 sorts de la déité)

UI_QuickslotBar (HUD permanent)
├── 4 emplacements + cooldown par slot + grisé si mana insuffisant

UI_MagicConfig (hors combat)
└── Assignation sorts -> quickslots
```

Slow-mo : `SetGlobalTimeDilation(0.15)` à l'ouverture, `1.0` à la fermeture.

---

## Ce qui reste à faire

- [ ] Ajouter `AffectedStat (Name)` dans FSoM_SpellData
- [ ] Créer enum `E_DeliveryType` (Direct, Projectile, AOE)
- [ ] Ajouter `DeliveryType` dans FSoM_SpellData
- [ ] Refactorer BP_Spell_Buff pour lire AffectedStat depuis SpellData (au lieu de hardcoder HealthMax)
- [ ] Refactorer BP_Spell_Debuff pour lire AffectedStat depuis SpellData
- [ ] UI_RadialMagic + UI_QuickslotBar (J-13)
- [ ] Binding input -> CastSpell (J-13)
- [ ] Test gameplay en PIE (validation POC)
- [ ] Créer BP_Spell_Attack_Projectile et BP_Spell_Attack_AOE quand nécessaire

---

## Historique

- Création : 11/05/2026
- Mise à jour : 12/05/2026 — POC logique complet, hiérarchie sorts standardisée, AffectedStat ajouté
