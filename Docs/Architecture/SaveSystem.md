# SaveSystem -- Shadow of Mana
# Derniere mise a jour : 31/05/2026

---

## Statut : DESIGN VALIDE (31/05/2026)

---

## 1. Lore -- Ce qu'est la Fontaine de Fee

Les Fontaines de Fee sont des vestiges de l'epoque ou l'Arbre Mana etait intact : des points d'ancrage du Mana pur dans le monde physique. Depuis le cataclysme, elles sont presque toutes taries ou corrompues. Celles qui restent actives sont des oasis.

**Justification narrative du mecanisme de save :**
La Fee porte un fragment d'ame (celui de la soeur du heros). Ce fragment est instable, et le voyage l'use. Les Fontaines sont les seuls endroits ou ce fragment peut se stabiliser temporairement -- et ou la Fee "grave" le souvenir du monde autour d'elle (= le point de respawn).

Ce n'est pas le heros qui sauvegarde. C'est la Fee qui se souvient.

Les Fontaines se "reveillent" au fur et a mesure que le Mana se restaure -- cohérent avec la progression narrative (liberation des deites, restauration des zones).

---

## 2. Declencheurs de sauvegarde

| Declencheur | Type de save | Respawn point |
|---|---|---|
| Interaction Fontaine | Save complete | Oui -- mis a jour |
| Fontaine contextuelle (post-boss, entree zone) | Save complete | Oui -- mis a jour |
| Jalon narratif specifique | Save progression uniquement | Non -- respawn = derniere Fontaine |

**Fontaines contextuelles** : apparaissent dans le monde a des moments cles (salle apres un boss, entree d'une nouvelle zone, apres une cinematique majeure). Pas de save silencieuse abstraite -- toujours via une Fontaine physique dans le niveau.

**Jalons narratifs** : sauvegardent la progression (flags, inventaire, etat monde) mais ne deplacent pas le point de respawn. Evite les incoherences (mourir apres une cinematique et respawner au milieu d'une scene).

---

## 3. Mecanique Fontaine -- Interaction de base

Le joueur approche une Fontaine -> prompt d'interaction -> ecran de transition court -> effets appliques :

| Effet | Detail |
|---|---|
| HP / ST / MP restaures a 100% | Instantane |
| Corruption purgee (cout variable, voir section 4) | Remise a 0 |
| Fee regeneree | Reset de ses etats |
| Ennemis normaux respawn | Immediat a la reprise |
| Boss / mini-boss | Jamais respawn |
| Point de respawn mis a jour | Mort -> retour ici, Essence perdue |
| Montee niveau deite disponible | Sauf Corruption >= 100 |

---

## 4. Systeme Corruption / Essence / Fontaine

### Cout des depenses Essence selon Corruption

Toutes les depenses en Essence (montee niveau deite, achats, rituels...) sont affectees par le niveau de Corruption :

| Corruption | Modificateur cout Essence |
|---|---|
| 0 -- 74% | x1.0 (normal) |
| 75 -- 99% | x1.15 (+15%) |
| 100% | Essence inutilisable |

### Cout de purge Corruption a la Fontaine

| Corruption au moment du repos | Cout de purge |
|---|---|
| 0 -- 74% | Gratuit |
| 75 -- 99% | Petit cout en Essence (a calibrer -- session Economie) |
| 100% | Grand cout en Essence (a calibrer -- session Economie) |

La purge remet toujours la Corruption a 0, quel que soit le cout.

### Montee niveau deite a la Fontaine

| Corruption | Acces montee niveau deite |
|---|---|
| 0 -- 74% | Disponible, cout normal |
| 75 -- 99% | Disponible, cout +15% |
| 100% | Bloque -- la Fee ne peut pas effectuer d'evolution |

### Tension de design

```
Corruption monte vers 100%
  -> Depenses Essence coutent plus cher (x1.15)
  -> Purge a la Fontaine coute de l'Essence
  -> Moins d'Essence disponible car depensee plus vite
  -> Double penalite economique si on attend trop longtemps

Purger souvent (avant 75%) = aller souvent a la Fontaine = ennemis qui respawn
Purger rarement = Corruption haute = penalites economiques cumulees
```

Le calibrage exact des couts de purge sera defini en session Economie/Drops.

---

## 5. Essence de Mana -- comportement a la mort

| Scenario de mort | Comportement Essence |
|---|---|
| Mort par environnement (chute, piege, zone) | Essence tombe au sol a l'endroit de la mort -- objet physique ramassable |
| Mort par ennemi | Le mob qui a porte le coup fatal porte l'Essence -- doit etre tue pour recuperer |
| Mob porteur est un boss / mini-boss | Exception : Essence tombe au sol (boss jamais re-tuable) |

- Si le joueur meurt avant de recuperer son Essence : Essence definitivement perdue
- La Fontaine elle-meme ne redonne pas l'Essence -- elle est uniquement le point de respawn

---

## 6. Slots de sauvegarde

- **Multi-parties** : plusieurs slots disponibles (ex. 3 slots), chaque slot = une partie distincte
- **Intra-partie** : un seul slot actif, ecrasement automatique -- pas de save manuelle multiple
- Souls-like strict a l'interieur d'une partie

---

## 7. Architecture technique -- BP_SaveGame_SoM

### Structure de donnees

```
BP_SaveGame_SoM (extends SaveGame)
|
+-- SaveSlotName : String               -- "Slot_1", "Slot_2", "Slot_3"
+-- SaveVersion : Int                   -- pour migrations futures
+-- LastFountainID : Name               -- ID de la derniere Fontaine activee
+-- LastFountainTransform : Transform   -- position de respawn precise
|
+-- [Stats heros]
|   +-- HealthCurrent : Float
|   +-- StaminaCurrent : Float
|   +-- ManaCurrent : Float
|   +-- EssenceMana : Int64            -- Essence sur le heros (pas celle au sol)
|   +-- Corruption : Float
|   +-- bCorruptionUnlocked : Bool
|   +-- HeroLevel : Int
|
+-- [Inventaire]
|   +-- DiscoveredWeapons : Array<Name>
|   +-- CurrentWeaponID : Name
|   +-- CurrentWeaponLevel : Int
|
+-- [Magie]
|   +-- UnlockedDeities : Array<Name>
|   +-- DeitySpellData : Map<Name, FSoM_DeitySpells>
|   +-- SpellUsageCounters : Map<Name, Int>
|
+-- [Progression monde]
|   +-- ActivatedFountains : Array<Name>
|   +-- CompletedNarrativeFlags : Array<Name>
|   +-- MoralChoiceMade : EChoiceResult
|
+-- [Essence au sol]
    +-- DroppedEssenceAmount : Int64
    +-- DroppedEssenceLocation : Vector
```

### Flux de sauvegarde (interaction Fontaine)

```
Joueur interagit avec Fontaine
  -> GameMode.OnFountainRest(FountainID)
    -> Collecter toutes les donnees (AttributeSet, InventoryComponent, MagicComponent...)
    -> Remplir BP_SaveGame_SoM
    -> SaveGameToSlot("Slot_X", 0)
    -> Broadcast RestoreEffects (HP/ST/MP full + purge Corruption avec cout)
    -> Marquer Fontaine comme activee (ActivatedFountains)
    -> Respawn ennemis normaux de la zone
```

### Flux de chargement (mort / reprise)

```
OnPlayerDeath
  -> Dropper Essence au sol OU marquer mob porteur
  -> LoadGameFromSlot("Slot_X", 0)
  -> Restaurer stats depuis SaveGame
  -> Teleporter heros a LastFountainTransform
  -> Rejouer animation "reveil a la Fontaine"
```

---

## 8. BP_FountainComponent

Actor Component attache a chaque Fontaine BP dans le niveau.

| Variable / Fonction | Detail |
|---|---|
| FountainID : Name | Editable dans l'editeur -- identifiant unique |
| bIsActivated : Bool | Premiere activation = animation speciale + particules differentes |
| OnPlayerInteract() | Appelle GameMode.OnFountainRest(FountainID) |

### Convention de nommage FountainID

```
Fountain_A1_Village          -- Fontaine village du heros
Fountain_A1_Gnome_01         -- Premiere Fontaine territoire Gnome
Fountain_A1_Ombre_Entry      -- Entree Sanctuaire d'Ombre
Fountain_A2_Hub_01           -- Premiere Fontaine Hub
Fountain_A2_PostBoss_General -- Fontaine apres boss General
...
```

---

## 9. Jalon d'implementation

Ce design est la spec pour le jalon **C2-SaveGame**.
La logique Corruption (purge, couts) sera implementee dans **C2-CorruptionSystem**.
La logique Essence complete (collecte, perte, recuperation) sera dans **C3-EssenceMana**.

---

## Historique

- Creation : 31/05/2026 -- session SaveDesign complete
