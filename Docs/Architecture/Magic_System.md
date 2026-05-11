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
- Régénération passive lente (plus lente que la Stamina)
- Pas de regen en combat ? (à définir lors du POC)

---

## Accès aux sorts — deux systèmes

### 1. Radial Magie (accès complet)

Navigation hiérarchique en deux niveaux :

**Niveau 1 — Roue des éléments**
- Affiche les déités débloquées uniquement (le radial se remplit au fil de l'aventure)
- Au départ : 1 seule entrée (Lumina). A la fin : 8-9 entrées.
- Déclenchement : bouton dédié (à définir, différent du radial armes)
- Effet monde : **slow-mo 0.15x** pendant la navigation (SetGlobalTimeDilation)
  - Le danger reste présent mais atténué
  - Permet la réflexion sans être une vraie pause

**Niveau 2 — Roue des sorts de l'élément**
- S'ouvre après sélection d'un élément au niveau 1
- 4 à 5 sorts par déité : Attaque / Buff / Débuff / Soin / Ultime (débloqué plus tard)
- Lancement : **au relâchement** de la sélection niveau 2
- Retour au niveau 1 : bouton annuler (sans lancer de sort)
- Fermeture : temps réel reprend immédiatement

**Avantage du radial vs quickslots :** accès à l'intégralité de l'arsenal, toutes déités confondues. Contrepartie : navigation en 2 étapes.

---

### 2. Quickslots (accès rapide)

- **4 emplacements** assignables librement par le joueur
- Tous éléments confondus — le joueur choisit ses 4 sorts prioritaires
- Configuration **hors combat uniquement** via menu dédié
- Déclenchement : mini roue à 4 entrées (bouton dédié, différent du radial magie)
- Temps : **temps réel** — pas de slow-mo, réflexes purs
- Lancement : sélection = lancement immédiat

**Différence de rôle :** les quickslots sont pour les sorts qu'on utilise le plus souvent dans la situation actuelle. On les reconfigure selon les ennemis à venir (préparation avant un boss, par exemple).

**Mécanique de préparation :** avant un boss fort au feu, on assigne un sort d'eau en quickslot. C'est une décision tactique hors combat.

---

## Ciblage des sorts

| Catégorie | Cible |
|-----------|-------|
| Attaque | Cible lockée en priorité, sinon ennemi le plus proche |
| Débuff | Cible lockée en priorité, sinon ennemi le plus proche |
| Soin | Héros uniquement (extensible aux compagnons PNJ — module futur) |
| Buff | Héros uniquement (extensible aux compagnons PNJ — module futur) |
| Ultime | Selon le sort (à définir au cas par cas) |

Le système de lock-on existant (`BP_PlatformingPlayerController`) est réutilisé directement pour la notion de cible lockée.

---

## Déblocage progressif

Chaque déité se débloque via sa rencontre narrative (représentant humain ou esprit) :

| Ordre | Déité | Moment narratif | Magie débloquée |
|-------|-------|-----------------|-----------------|
| 1 | Lumina | Début — Lumina rejoint le groupe | Soin, attaque lumière |
| 2 | Luna | Acte 1 — Luna confirmée comme représentante | Buff, attaque lune |
| 3 | Sylphide | Acte 2 — Résolution conflit pays du vent | Vent, débuff |
| 4 | Gnome | Acte 2 — Colosse rejoint | Terre, défense |
| 5 | Salamandre | Acte 2 — Forgeron/Loup | Feu, attaque |
| 6 | Ombre | Acte 3 — Révélation sur le héros | Ombre, attaque critique |
| 7 | Athanor | Acte 3 — Forge complète | Forge, buff arme |
| 8 | Dryade | Acte 3 — Oracle (avant sa mort) | Nature, soin zone |
| 9 | Ondine | Acte 4 — Résolution sœur | Eau, sort ultime |

Le radial magie reflète visuellement cette progression — les entrées apparaissent au fil du jeu.

---

## Architecture technique Blueprint

### Composants et classes

```
BP_MagicComponent (ActorComponent sur BP_PlatformingCharacter)
├── Variables
│   ├── UnlockedSpells : Map<Name, Array<SpellID>>  // par déité
│   ├── QuickslotSlots[4] : Array<SpellID>
│   └── SpellCooldowns : Map<SpellID, Float>
├── Fonctions
│   ├── CastSpell(SpellID, Target)
│   ├── CanCast(SpellID) : Bool          // Mana suffisant + pas en cooldown
│   ├── ConsumeMana(Amount)              // via SetStatValue
│   ├── IsSpellUnlocked(SpellID) : Bool
│   └── UnlockDeity(DeityName)
└── Dispatchers
    └── OnSpellCast(SpellID)             // pour VFX, corruption, UI

DT_Spells (DataTable — struct FSoM_SpellData)
├── SpellID (Name)
├── SpellName (Text)
├── Element / Deity (Name)              // Lumina, Luna, Sylphide...
├── Category (Enum)                     // Attaque, Buff, Debuff, Soin, Ultime
├── ManaCost (Float)
├── Cooldown (Float)
├── TargetType (Enum)                   // Enemy, Self, Area
├── Damage / EffectValue (Float)
├── Duration (Float)                    // pour buffs/debuffs
├── AnimMontage (SoftObjectRef)
└── VFX (SoftObjectRef)

BP_SpellBase (Actor — classe mère)
├── Execute(Caster, Target)
├── ApplyEffect()
└── BP enfants :
    ├── BP_Spell_Attack      // projectile ou AoE
    ├── BP_Spell_Heal        // soin instantané ou HOT
    ├── BP_Spell_Buff        // stat temporaire positive
    ├── BP_Spell_Debuff      // stat temporaire négative sur ennemi
    └── BP_Spell_Ultimate    // à définir au cas par cas
```

### UI

```
UI_RadialMagic
├── Niveau 1 : roue des éléments (entrées = déités débloquées)
└── Niveau 2 : roue des sorts (entrées = sorts de la déité choisie)

UI_QuickslotBar
├── 4 emplacements affichés en permanence sur le HUD
├── Icône du sort + indicateur de cooldown
└── Indicateur de Mana insuffisant (grisé)

UI_MagicConfig (menu hors combat)
└── Drag & drop des sorts vers les 4 quickslots
```

### Slow-mo

```
// Ouverture radial magie
SetGlobalTimeDilation(0.15)

// Fermeture radial magie (lancement ou annulation)
SetGlobalTimeDilation(1.0)
```

---

## POC — Jalons d'implémentation

Voir `Docs/Roadmap_Gameplay.md` sections J-10 à J-14 pour le détail.

**Périmètre du POC (J-14) :**
- 1 déité : Lumina (4 sorts : attaque lumière, soin, buff défense, débuff ennemi)
- Radial magie fonctionnel (2 niveaux, slow-mo)
- Quickslots fonctionnels (4 emplacements, temps réel)
- Ciblage basique (lock-on existant + héros pour soin/buff)
- Mana consommé et régénéré, HUD mis à jour

**Ce qui n'est PAS dans le POC :**
- Corruption magique (module séparé, J-24 à J-26)
- Sorts des compagnons PNJ
- Configuration drag & drop des quickslots (simplifié : assignation directe)
- Sorts ultimes

---

## Questions ouvertes

- La Mana régénère-t-elle en combat ou uniquement hors combat ?
- Les sorts ont-ils une animation qui interrompt le mouvement du héros (cast time) ?
- Les quickslots ont-ils un cooldown partagé (global) ou indépendant par slot ?
- Les buffs s'appliquent-ils aussi aux compagnons PNJ dès le POC ou plus tard ?

---

## Historique

- Création : 11/05/2026
- Dernière mise à jour : 11/05/2026
