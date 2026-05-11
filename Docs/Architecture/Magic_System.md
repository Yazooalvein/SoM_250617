# Architecture — Système de Magie

Document de référence pour l'implémentation du système de magie de Shadow of Mana.
A lire avant toute implémentation Blueprint liée à la magie.

---

## Vision design

La magie est un système **indépendant du combat physique** — deux ressources séparées (Stamina / Mana), deux roues distinctes, deux philosophies d'accès. Elle peut sauver une situation désespérée mais ne remplace pas un cac maîtrisé. Utiliser trop de magie a des conséquences (voir Corruption Magique, module futur).

---

## Ressource : Mana

- Jauge indépendante de la Stamina — les deux coexistent sans interaction
- Nommage stats : `ManaCurrent` / `ManaMax` (convention sans espace, CamelCase)
- Modification uniquement via `SetStatValue("ManaCurrent", valeur)` — jamais de SET direct
- Notification via `OnStatChanged` existant — le HUD se met à jour automatiquement
- **Pas de régénération de base** — le Mana est une ressource à gérer comme des munitions
- La regen Mana est un bonus apporté uniquement par : buff actif, potion, équipement dédié
- Conséquence design : utiliser de la magie est un vrai choix, pas un spam — les items/stuffs qui donnent de la regen ont de la valeur

---

## Cast time

Les sorts sont divisés en deux catégories selon leur puissance et utilité :

| Type | Cast time | Exemples |
|------|-----------|---------|
| **Instantané** | Aucun — lancement immédiat | Soin d'urgence, buff rapide, débuff simple |
| **Avec cast time** | Animation de cast + fenêtre de vulnérabilité | Attaque puissante, sort de zone, ultime |

Le cast time est défini dans `DT_Spells` via le champ `CastTime (Float)` :
- `0.0` = instantané
- `> 0.0` = durée du cast en secondes

Pendant un cast time :
- Le héros joue une animation de cast (AnimMontage dédié)
- Le héros est **vulnérable** — pas d'iframes, peut être interrompu si touché (à valider lors du POC)
- Le mouvement est **bloqué** pendant la durée du cast
- Un sort interrompu ne consomme pas de Mana

---

## Accès aux sorts — deux systèmes

### 1. Radial Magie (accès complet)

Navigation hiérarchique en deux niveaux :

**Niveau 1 — Roue des éléments**
- Affiche les déités débloquées uniquement (le radial se remplit au fil de l'aventure)
- Au départ : 1 seule entrée (Lumina). A la fin : 8-9 entrées.
- Déclenchement : bouton dédié (différent du radial armes)
- Effet monde : **slow-mo 0.15x** pendant la navigation (SetGlobalTimeDilation)
  - Le danger reste présent mais atténué
  - Permet la réflexion sans être une vraie pause

**Niveau 2 — Roue des sorts de l'élément**
- S'ouvre après sélection d'un élément au niveau 1
- 4 à 5 sorts par déité : Attaque / Buff / Débuff / Soin / Ultime (débloqué plus tard)
- Lancement : **au relâchement** de la sélection niveau 2
- Retour au niveau 1 : bouton annuler (sans lancer de sort)
- Fermeture radial : temps réel reprend immédiatement (1.0)

**Avantage du radial vs quickslots :** accès à l'intégralité de l'arsenal, toutes déités confondues. Contrepartie : navigation en 2 étapes.

---

### 2. Quickslots (accès rapide)

- **4 emplacements** assignables librement par le joueur
- Tous éléments confondus — le joueur choisit ses 4 sorts prioritaires
- Configuration **hors combat uniquement** via menu dédié
- Déclenchement : mini roue à 4 entrées (bouton dédié, différent du radial magie)
- Temps : **temps réel** — pas de slow-mo, réflexes purs
- Lancement : sélection = lancement immédiat

**Différence de rôle :** les quickslots sont pour les sorts qu'on utilise le plus souvent dans la situation actuelle. On les reconfigure selon les ennemis à venir (préparation avant un boss).

**Mécanique de préparation :** avant un boss fort au feu, on assigne un sort d'eau en quickslot. Décision tactique hors combat.

**Cooldowns quickslots :** indépendants par slot (un slot en cooldown n'affecte pas les autres).

---

## Ciblage des sorts

| Catégorie | Cible |
|-----------|-------|
| Attaque | Cible lockée en priorité, sinon ennemi le plus proche |
| Débuff | Cible lockée en priorité, sinon ennemi le plus proche |
| Soin | Héros uniquement (extensible aux compagnons PNJ — module futur) |
| Buff | Héros uniquement (extensible aux compagnons PNJ — module futur) |
| Ultime | Selon le sort (à définir au cas par cas) |

Le système de lock-on existant (`BP_PlatformingPlayerController`) est réutilisé directement.

---

## Déblocage progressif

Chaque déité se débloque via sa rencontre narrative (représentant humain ou esprit) :

| Ordre | Déité | Moment narratif | Magie débloquée |
|-------|-------|-----------------|-----------------|\
| 1 | Lumina | Début — Lumina rejoint le groupe | Soin, attaque lumière, buff défense, débuff |
| 2 | Luna | Acte 1 — Luna confirmée | Buff, attaque lune |
| 3 | Sylphide | Acte 2 — Résolution pays du vent | Vent, débuff |
| 4 | Gnome | Acte 2 — Colosse rejoint | Terre, défense |
| 5 | Salamandre | Acte 2 — Forgeron/Loup | Feu, attaque |
| 6 | Ombre | Acte 3 — Révélation héros | Ombre, attaque critique |
| 7 | Athanor | Acte 3 — Forge complète | Forge, buff arme |
| 8 | Dryade | Acte 3 — Oracle (avant mort) | Nature, soin zone |
| 9 | Ondine | Acte 4 — Résolution sœur | Eau, sort ultime |

---

## Architecture technique Blueprint

### Composants et classes

```
BP_MagicComponent (ActorComponent sur BP_PlatformingCharacter)
├── Variables
│   ├── UnlockedSpells : Map<Name, Array<Name>>  // DeityName -> [SpellIDs]
│   ├── QuickslotSlots[4] : Array<Name>          // SpellIDs assignés
│   ├── SpellCooldowns : Map<Name, Float>        // SpellID -> temps restant
│   └── bIsCasting : Bool                        // interruptible si hit pendant cast
├── Fonctions
│   ├── CastSpell(SpellID)                       // orchestre tout le flow
│   ├── CanCast(SpellID) : Bool                  // Mana ok + cooldown ok + pas en cast
│   ├── ConsumeMana(Amount)                      // SetStatValue("ManaCurrent")
│   ├── StartCast(SpellID)                       // joue AnimMontage, set bIsCasting
│   ├── CompleteCast(SpellID)                    // applique l'effet, consomme Mana
│   ├── InterruptCast()                          // annule sans consommer Mana
│   ├── IsSpellUnlocked(SpellID) : Bool
│   └── UnlockDeity(DeityName)                  // ajoute les sorts de la déité
└── Dispatchers
    └── OnSpellCast(SpellID)                     // VFX, corruption (futur), UI

DT_Spells (DataTable — struct FSoM_SpellData)
├── SpellID (Name)
├── SpellName (Text)
├── Deity (Name)                    // Lumina, Luna, Sylphide...
├── Category (Enum)                 // Attaque, Buff, Debuff, Soin, Ultime
├── ManaCost (Float)
├── CastTime (Float)                // 0.0 = instantané, >0 = cast time en secondes
├── Cooldown (Float)
├── TargetType (Enum)               // Enemy, Self, Area
├── EffectValue (Float)             // dégats, soin, valeur du buff...
├── Duration (Float)                // pour buffs/debuffs
├── CastMontage (SoftObjectRef)     // animation de cast (peut être None si instantané)
└── VFX (SoftObjectRef)

BP_SpellBase (Actor — classe mère)
├── Execute(Caster, Target)
├── ApplyEffect()
└── BP enfants :
    ├── BP_Spell_Attack      // projectile ou AoE
    ├── BP_Spell_Heal        // soin instantané
    ├── BP_Spell_Buff        // stat temporaire positive sur héros
    ├── BP_Spell_Debuff      // stat temporaire négative sur ennemi
    └── BP_Spell_Ultimate    // à définir au cas par cas
```

### UI

```
UI_RadialMagic
├── Niveau 1 : roue des éléments (entrées = déités débloquées)
└── Niveau 2 : roue des sorts (entrées = sorts de la déité choisie)
    └── Indicateur cast time visible sur chaque sort (icône horloge)

UI_QuickslotBar (affiché en permanence sur le HUD)
├── 4 emplacements avec icône du sort
├── Indicateur de cooldown indépendant par slot
└── Grisé si Mana insuffisant

UI_MagicConfig (menu hors combat)
└── Assignation des sorts aux 4 quickslots
```

### Slow-mo

```
// Ouverture radial magie
SetGlobalTimeDilation(0.15)

// Fermeture radial magie (lancement ou annulation)
SetGlobalTimeDilation(1.0)

// Les quickslots ne modifient pas GlobalTimeDilation
```

---

## POC — Périmètre J-10 à J-14

**Ce qui est dans le POC :**
- BP_MagicComponent avec gestion Mana (sans regen de base)
- DT_Spells avec 4 sorts Lumina (1 attaque avec cast time, 1 soin instantané, 1 buff instantané, 1 débuff avec cast time)
- BP_SpellBase + 4 BP enfants Lumina
- Radial magie 2 niveaux + slow-mo 0.15x
- Quickslots 4 emplacements temps réel
- Ciblage : lock-on existant pour attaque/débuff, héros pour soin/buff
- HUD : jauge Mana event-driven (OnStatChanged existant) + UI_QuickslotBar

**Ce qui n'est PAS dans le POC :**
- Regen Mana (aucune — ajoutée via buff/potion/stuff plus tard)
- Corruption magique (J-24 à J-26)
- Sorts des compagnons PNJ
- Configuration avancée des quickslots (assignation simple pour le POC)
- Sorts ultimes
- Interruption du cast par dégats (à valider gameplay lors du POC)

---

## Questions encore ouvertes

- Le cast time peut-il être interrompu par des dégats reçus ? (probable oui — à tester gameplay)
- Les buffs s'appliquent-ils aussi aux compagnons PNJ dès le POC ou plus tard ? (plus tard)
- Un sort peut-il être annulé volontairement pendant le cast time ?

---

## Historique

- Création : 11/05/2026
- Dernière mise à jour : 11/05/2026 — decisions Mana et cast time tranchées
