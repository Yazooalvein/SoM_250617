# Journal des Modifications -- Shadow of Mana

## Objectif
Suivi precis de toutes les evolutions majeures du projet.

## Entrees

### 04/06/2026 -- SYS-StatSystem -- EN COURS (WIP)

#### Decisions architecture
- Option B retenue : refacto complet BP_AttributeSet_Base -- TMap<Name, Float> x3 + GetStatValue + SetStatValue guards
- StatMinValues + StatMaxValues : deux Maps supplementaires peuplees par InitStats, lues par SetStatValue Default
- InitStats(StatDataTable : DataTable) : parametre passe par HC, pas stocke dans AttributeSet
- SetStatValue Default : pas de Switch residuel -- FClamp via StatMinValues/StatMaxValues
- ConsumeStamina / HandleStaminaRegen / StartStaminaRegen : migrer vers GetStatValue (prochaine session)
- Variables natives conservees comme cache synchronise pour lecteurs UI externes (dette C2)
- BP_CorruptionComponent : OwnerAttributeSet supprimee, variables locales dans chaque fonction

#### Realise cette session
- DT_StatList : 3 rows ajoutees (EssenceValue, Corruption, TenaciteEtat)
- BP_CorruptionComponent : OwnerAttributeSet supprimee -> variables locales dans InitCorruption, TrackDeityUsage, PurgeCorruption
- BP_AttributeSet_Base : variables StatValues, StatMinValues, StatMaxValues (TMap<Name, Float>) ajoutees
- BP_AttributeSet_Base : InitStats() complete -- GetDataTableRowNames -> ForEach -> GetDataTableRow -> BreakStruct -> Map_Add x3
- BP_AttributeSet_Base : GetStatValue(Name)->double complete (Pure) -- Map_Find -> Branch(Found) -> Return / DebugPrint
- BP_AttributeSet_Base : SetStatValue -- 3 guards complets (EssenceValue, Corruption, HealthMax) + Default (MinValues/MaxValues/FClamp)
- Bug HealthMax fixe : FMin.B = GET HealthCurrent (etait non connecte -> clamp vers 0)

#### Reste a faire (prochaine session)
- Brancher CallDelegate OnStatChanged sur les 6 Map_Add.then de SetStatValue
- Migrer ConsumeStamina vers GetStatValue("StaminaCurrent") / GetStatValue("StaminaMax")
- Migrer HandleStaminaRegen vers GetStatValue (StaminaCurrent, StaminaMax, StaminaRegenRate, StaminaRegenInterval)
- Migrer StartStaminaRegen vers GetStatValue (StaminaCurrent, StaminaMax)
- Adapter HC.InitAttributesFromDatatable : Construct BP_AttributeSet_Base -> InitStats(StatsDataTable) -> SetStatValue Current=Max
- BP_SoM_GameMode : ajouter SetStatValue("StaminaCurrent", StaminaMax) dans WriteSaveAndApplyFountainEffects
- BP_CorruptionComponent : supprimer pre-clamp redondant (0,100) dans TrackDeityUsage
- Validation PIE complete
- Mettre a jour snapshot Docs/Blueprints/BP_AttributeSet_Base.md post-jalon

#### Notes techniques
- search_nodes UnrealClaude : utiliser "Set Stat Value" avec espaces (pas "SetStatValue")
- Variables locales MinValue/MaxValue dans SetStatValue pour stocker resultats Map_Find
- FClamp Default path no-max : pin Max = 340282299999999994960115009090224128000 (MAX_FLT accepte par UE5)
- Git : push doc avant push BP -> conflit LFS -> resolution : git checkout origin/main -- Docs/ + commit + push --force-with-lease

---

### 03/06/2026 -- SYS-SaveGame -- VALIDE PIE

#### Architecture save -- BPI_Saveable + BP_SaveGame_SoM
- BPI_Saveable : interface SaveData(SaveGame) + LoadData(SaveGame) dans Content/Systems/Save/
- BP_SaveGame_SoM : conteneur de donnees pur, extends SaveGame -- pas de logique
- Decision archi cle : sauvegarder LockedDeities (delta) plutot que UnlockedSpells (Map complexe) -- reconstruction depuis DT_Deities au load via UnlockDeity() -- robuste aux modifs DataTable
- BPI_Saveable implemente sur 4 composants : BP_InventoryComponent, BP_ComboManagerComponent, BP_MagicComponent, BP_AttributeSet_Base
- HP/ST/MP non sauvegardes -- restaures a max directement au load

#### BP_MagicComponent -- LoadData
- SET LockedDeities + SpellUsageCounts -> GetDataTableRowNames(DT_Deities) -> ForEachLoop -> si NOT IN LockedDeities -> UnlockDeity(RowName)
- Reconstruction propre de UnlockedSpells depuis DT_Deities

#### BP_SoM_GameMode -- OnFountainRest
- Variables : CurrentSaveGame (BP_SaveGame_SoM), CurrentSlotName (String, Slot_1)
- CollectSaveData(FountainID) : CreateSaveGameObject -> metas + ActivatedFountains -> GetComponentsByInterface(BPI_Saveable) -> ForEachLoop -> K2Node_Message SaveData
- CollectFountainTransform(FountainID) : GetAllActorsOfClass(BP_Fountain_Actor)[0] -> GetTransform -> SET LastFountainTransform (C1 = index 0, filtre par ID -> C2)
- WriteSaveAndApplyFountainEffects() : SaveGameToSlot -> SetStatValue HP/ST/MP=Max -> PurgeCorruption(0.0)
- OnFountainRest = 3 calls en sequence -- GameMode ne connait pas les details des composants

#### BP_Fountain_Actor -- fix overlap
- ActorBeginOverlap -> GetComponentByClass(BP_FountainComponent, Target=self) -> OnPlayerInteract
- Bug resolu : Target du GetComponentByClass branche sur HC au lieu de self -> Accessed None -- fix : Target = self (la Fontaine)
- Cast to BP_FountainComponent superflu -- GetComponentByClass retourne deja le bon type

#### BP_SoM_PlayerController -- OnHeroDied -- respawn Fontaine
- Apres SET bIsDead=false : GetGameMode -> Cast GameMode -> GET CurrentSaveGame -> IsValid
  - TRUE : GetComponentsByInterface(BPI_Saveable) -> ForEachLoop LoadData -> SetActorLocation(LastFountainTransform.Location) -> fade -> EnableInput
  - FALSE (premiere mort) : PlayerStart -> TeleportTo -> fade -> EnableInput
- Dette resolue : Respawn PlayerStart hardcode remplace par LastFountainTransform

#### Dettes ajoutees
- SetStatValue HP/ST/MP dans OnHeroDied ET dans AttributeSet.LoadData -- doublon a nettoyer (non bloquant)
- CollectFountainTransform prend index 0 -- filtrage par FountainID -> C2

#### Etat final
SYS-SaveGame VALIDE PIE. Overlap Fontaine -> save + restauration HP/ST/MP/Corruption. Mort -> drop Essence -> respawn Fontaine (LastFountainTransform). Premiere mort sans save -> respawn PlayerStart.

---

### 02/06/2026 -- SYS-EssenceMana -- VALIDE PIE

#### Etat final
BP_EssenceDrop VALIDE PIE. Mort -> drop Essence + fade -> respawn PlayerStart. Pickup -> restitution Essence + HUD. EssenceValue renomme depuis EssenceMana.

---

### 31/05/2026 -- SYS-CorruptionSystem -- VALIDE PIE

#### Etat final
BP_CorruptionComponent VALIDE PIE. TrackDeityUsage, PurgeCorruption, GetWeakDeity operationnels.

---

### 31/05/2026 -- COMBAT-SwordMoveset -- CLOS VALIDE PIE

#### Etat final
Combo epee fonctionnel (Light x2 + Heavy x1). TenaciteEtat dans AttributeSet (base 25).

---

### 31/05/2026 -- SaveDesign -- DESIGN VALIDE

#### Etat final
DESIGN-SaveDesign VALIDE. Spec dans Docs/Architecture/SaveSystem.md.

---

### 31/05/2026 -- C1-HUDCore -- VALIDE

#### Etat final
C1-HUDCore VALIDE. Architecture event-driven HP/ST/MP/Essence/Corruption operationnelle.

---

### 30/05/2026 -- DESIGN-WeaponProgression -- VALIDE

#### Etat final
Weapons_Progression.md cree et pousse.

---

### 29/05/2026 -- Session design Lore + C1-WeaponArchitecture -- CLOTURE

#### Etat final
WeaponArchitecture clos. Lore actes/Armes Mana/Hub documente.

---

### 28/05/2026 -- Sessions design -- Stats / StatusEffects / Corruption / Economy / Lore

#### Etat final
Sessions design completes. Specs dans fichiers Architecture/ et Lore_ShadowOfMana.md.

---

### 27/05/2026 -- C1-CleanupDettes + MagicUnlockSystem + RadialUnlock -- VALIDE PIE

---

### 25-26/05/2026 -- Data layer deites + Magic_Progression DESIGN

---

### 23/05/2026 -- C1-InputsUI COMPLET -- VALIDE PIE

---

### 18-21/05/2026 -- CollisionFix / HitFeel / ComboFix / TestBed / LockMove

---

### 17/05/2026 -- J-Camera COMPLET -- VALIDE PIE

---

### 15/05/2026 -- J-lock + J-Renommage COMPLET

---

### 14/05/2026 -- Session design Roadmap + J-Nettoyage + ART + MUS

---

### 12-13/05/2026 -- J-13 Radial Menu + J-15 HUD_Main + J-10 a J-14 POC Magie

---

### 11/05/2026 -- Sessions design + jalons #8 et #9

### 07/05/2026 -- Jalons #1 a #7

### 2025 -- Sessions fondatrices (voir historique complet)

---

## Rappel
Pour la roadmap detaillee : voir Docs/Roadmap_Gameplay.md
Pour les decisions architecturales : voir Docs/Architecture/Decisions.md
Pour les stats et progression : voir Docs/Architecture/Stats_Progression.md
Pour les effets de statut et corruption : voir Docs/Architecture/Combat_StatusEffects.md
Pour l'economie et les drops : voir Docs/Architecture/Economy_Drops.md
Pour le lore et la narrative : voir Docs/Lore_ShadowOfMana.md
Pour la progression armes : voir Docs/Architecture/Weapons_Progression.md
Pour le systeme de save : voir Docs/Architecture/SaveSystem.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 04/06/2026
