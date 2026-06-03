# SaveSystem -- Shadow of Mana
# Derniere mise a jour : 03/06/2026

---

## Statut : VALIDE PIE (03/06/2026)

---

## 1. Lore -- Ce qu'est la Fontaine de Fee

Les Fontaines de Fee sont des vestiges de l'epoque ou l'Arbre Mana etait intact : des points d'ancrage du Mana pur dans le monde physique. Depuis le cataclysme, elles sont presque toutes taries ou corrompues. Celles qui restent actives sont des oasis.

**Justification narrative du mecanisme de save :**
La Fee porte un fragment d'ame (celui de la soeur du heros). Ce fragment est instable, et le voyage l'use. Les Fontaines sont les seuls endroits ou ce fragment peut se stabiliser temporairement -- et ou la Fee "grave" le souvenir du monde autour d'elle (= le point de respawn).

Ce n'est pas le heros qui sauvegarde. C'est la Fee qui se souvient.

Les Fontaines se "reveillent" au fur et a mesure que le Mana se restaure -- coherent avec la progression narrative (liberation des deites, restauration des zones).

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

## 3. Mecanique Fontaine -- Interaction de base (C1)

C1 : declenchement automatique par overlap (pas de prompt). C2 : prompt d'interaction + animation.

| Effet | Detail | Statut C1 |
|---|---|---|
| HP / ST / MP restaures a 100% | Instantane | VALIDE |
| Corruption purgee (cout 0 en C1) | Remise a 0 via PurgeCorruption(0.0) | VALIDE (cout -> SESSION-Economie) |
| Fee regeneree | Reset de ses etats | C2 |
| Ennemis normaux respawn | Immediat a la reprise | C2 |
| Boss / mini-boss | Jamais respawn | -- |
| Point de respawn mis a jour | LastFountainTransform | VALIDE |
| Montee niveau deite disponible | Sauf Corruption >= 100 | C2 |

---

## 4. Systeme Corruption / Essence / Fontaine

### Cout des depenses Essence selon Corruption

| Corruption | Modificateur cout Essence |
|---|---|
| 0 -- 74% | x1.0 (normal) |
| 75 -- 99% | x1.15 (+15%) |
| 100% | Essence inutilisable |

### Cout de purge Corruption a la Fontaine

| Corruption au moment du repos | Cout de purge |
|---|---|
| 0 -- 74% | Gratuit |
| 75 -- 99% | Petit cout en Essence (a calibrer -- SESSION-Economie) |
| 100% | Grand cout en Essence (a calibrer -- SESSION-Economie) |

C1 : purge toujours gratuite (PurgeCorruption(0.0)). Couts -> SESSION-Economie.

### Tension de design

```
Corruption monte vers 100%
  -> Depenses Essence coutent plus cher (x1.15)
  -> Purge a la Fontaine coute de l'Essence
  -> Moins d'Essence disponible car depensee plus vite
  -> Double penalite economique si on attend trop longtemps
```

---

## 5. Essence de Mana -- comportement a la mort

| Scenario de mort | C1 | C2+ |
|---|---|---|
| Mort par environnement | Drop au sol (BP_EssenceDrop) | idem |
| Mort par ennemi | Drop au sol (C1) | Mob porteur |
| Mort par boss / mini-boss | Drop au sol | idem (boss jamais re-tuable) |

- Essence non recuperee avant 2eme mort : perdue definitivement (C2 -- C1 = drop indefini)
- La Fontaine ne redonne pas l'Essence -- uniquement point de respawn

---

## 6. Slots de sauvegarde

- **Multi-parties** : 3 slots, chaque slot = une partie distincte
- **Intra-partie** : slot unique, ecrasement automatique -- souls-like strict
- Nom slot courant : stocke dans GameMode.CurrentSlotName (String, default "Slot_1")

---

## 7. Architecture technique -- VALIDE PIE (03/06/2026)

### Principe -- BPI_Saveable

Chaque systeme est responsable de ses propres donnees de persistance.
Le GameMode ne connait pas les details -- il itere sur l'interface.

```
BPI_Saveable
  SaveData(SaveGame : BP_SaveGame_SoM)   -- ecriture dans le SaveGame
  LoadData(SaveGame : BP_SaveGame_SoM)   -- lecture et reconstruction
```

Systemes qui implementent BPI_Saveable :
| Composant | SaveData ecrit | LoadData reconstruit |
|---|---|---|
| BP_InventoryComponent | DiscoveredWeapons | ForEachLoop AddWeapon |
| BP_ComboManagerComponent | CurrentWeaponID + CurrentWeaponLevel | EquipWeapon(ID, Level) -> InitComboTree |
| BP_MagicComponent | LockedDeities + SpellUsageCounts | SET + UnlockDeity depuis DT_Deities |
| BP_AttributeSet_Base | EssenceValue | SET EssenceValue |
| BP_QuestComponent (C4) | NarrativeFlags | -- |
| BP_ForgeComponent (C3) | WeaponLevels | -- |

HP/ST/MP non persistees -- restaurees a Max au load (inutile de sauvegarder l'etat instantane).

### Decision cle -- LockedDeities vs UnlockedSpells

On sauvegarde **LockedDeities** (Array<Name>, delta = ce qui est bloque) et non UnlockedSpells (Map<Name, FSoM_DeitySpells>).
Au load : GetDataTableRowNames(DT_Deities) -> ForEachLoop -> si NOT IN LockedDeities -> UnlockDeity(RowName).
Raison : robuste aux modifications futures de DT_Deities, pas de desync possible.

### Structure BP_SaveGame_SoM (implementee)

```
BP_SaveGame_SoM (extends SaveGame)
|
+-- [Meta]
|   +-- SaveSlotName : String          -- "Slot_1", "Slot_2", "Slot_3"
|   +-- SaveVersion : Int              -- pour migrations futures
|   +-- LastFountainID : Name          -- ID de la derniere Fontaine activee
|   +-- LastFountainTransform : Transform -- position de respawn precise
|
+-- [Stats heros]
|   +-- EssenceValue : Int64           -- Essence sur le heros (souls-like)
|   +-- HeroLevel : Int                -- (C2 -- pas encore incremente)
|
+-- [Inventaire]
|   +-- DiscoveredWeapons : Array<Name>
|   +-- CurrentWeaponID : Name
|   +-- CurrentWeaponLevel : Int
|
+-- [Magie]
|   +-- LockedDeities : Array<Name>    -- deites bloquees (delta)
|   +-- SpellUsageCounters : Map<Name, Int>
|
+-- [Progression monde]
|   +-- ActivatedFountains : Array<Name>
|   +-- CompletedNarrativeFlags : Array<Name>
|
+-- [Essence au sol]
    +-- DroppedEssenceAmount : Int64
    +-- DroppedEssenceLocation : Vector
```

Note : HealthCurrent/StaminaCurrent/ManaCurrent/Corruption/bCorruptionUnlocked/MoralChoiceMade
preserves dans la struct pour C2/C3 -- non utilises en C1.

### Flux de sauvegarde (interaction Fontaine) -- C1

```
ActorBeginOverlap BP_Fountain_Actor
  -> GetComponentByClass(BP_FountainComponent, Target=self)
  -> OnPlayerInteract()
    -> GetGameMode -> Cast to BP_SoM_GameMode
    -> OnFountainRest(FountainID)
      -> CollectSaveData(FountainID)
           CreateSaveGameObject -> SET CurrentSaveGame
           SET LastFountainID, Array_Add(ActivatedFountains, FountainID)
           SET CurrentSlotName
           Cast HC -> GetComponentsByInterface(BPI_Saveable)
           ForEachLoop -> K2Node_Message SaveData(CurrentSaveGame)
      -> CollectFountainTransform(FountainID)
           GetAllActorsOfClass(BP_Fountain_Actor)[0] -> GetTransform
           SET CurrentSaveGame.LastFountainTransform
           (C1 = index 0, filtrage par FountainID -> C2)
      -> WriteSaveAndApplyFountainEffects()
           SaveGameToSlot(CurrentSaveGame, CurrentSlotName, 0)
           SetStatValue(HP/ST/MP = Max)
           PurgeCorruption(0.0)
```

### Flux de chargement (mort) -- C1

```
OnHeroDied (BP_SoM_PlayerController)
  -> SpawnActor(BP_EssenceDrop) -> SET EssenceValue
  -> SetStatValue(EssenceValue, 0)
  -> CameraFade(0->1, noir)
  -> Delay(1.5s)
  -> SetStatValue(HP/ST/MP = Max), SET bIsDead=false
  -> GetGameMode -> Cast -> GET CurrentSaveGame -> IsValid ?
      TRUE  : GetComponentsByInterface(BPI_Saveable) -> ForEachLoop LoadData
              -> SetActorLocation(BreakTransform(LastFountainTransform).Location)
      FALSE : GetActorOfClass(PlayerStart) -> TeleportTo HC
  -> CameraFade(1->0, retour) -> EnableInput
```

---

## 8. BP_FountainComponent

| Variable / Fonction | Detail |
|---|---|
| FountainID : Name | Editable dans l'editeur -- identifiant unique |
| bIsActivated : Bool | (C2 -- animation speciale premiere activation) |
| OnPlayerInteract() | Cast to BP_SoM_GameMode -> OnFountainRest(FountainID) |

### Gotcha implementation

- `GetComponentByClass` dans BP_Fountain_Actor : **Target = self (la Fontaine)**, pas le HC
- `GetComponentsByInterface` + `K2Node_Message` = appel interface sans Cast explicite -- pattern correct
- Le Cast to BP_FountainComponent apres GetComponentByClass est superflu si la classe est specifiee

### Convention de nommage FountainID

```
Fountain_A1_Village
Fountain_A1_Gnome_01
Fountain_A1_Ombre_Entry
Fountain_A2_Hub_01
Fountain_A2_PostBoss_General
```

---

## 9. Dettes C1 -> C2+

| Dette | Cible |
|---|---|
| CollectFountainTransform prend index 0 (pas filtre par FountainID) | C2 |
| Overlap automatique (pas de prompt d'interaction) | C2 |
| PurgeCorruption gratuite (cout 0) | SESSION-Economie |
| Destruction drop Essence a la 2eme mort | C2 |
| Mob porteur Essence | C2 |
| SetStatValue HP/ST/MP dans OnHeroDied ET AttributeSet.LoadData (doublon) | C2 |
| Animation "reveil a la Fontaine" | C2 |
| Respawn ennemis normaux a la Fontaine | MAP-C1Level |
| HeroLevel non incremente (variable presente, logique absente) | C2 |
| QuestComponent, ForgeComponent (BPI_Saveable a implementer) | C3/C4 |

---

## Historique

- Creation : 31/05/2026 -- session SaveDesign complete (DESIGN VALIDE)
- MAJ 03/06/2026 -- SYS-SaveGame VALIDE PIE : architecture BPI_Saveable implementee, flux complets documentes, dettes C2 listees
