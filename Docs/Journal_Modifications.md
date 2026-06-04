# Journal des Modifications -- Shadow of Mana

## Objectif
Suivi precis de toutes les evolutions majeures du projet.

## Entrees

### 04/06/2026 -- SYS-StatSystem (session 2) -- HUD VALIDE PIE

#### HUD HP/ST/MP/Essence -- VALIDE PIE
- Migration Option B complete : tous les lecteurs de stats passent par GetStatValue, plus aucun GET variable native dans les BPs consommateurs
- UI_HUD_Main : RefreshAllStats creee, HUD_OnStatChanged simplifie (switch supprime), InitHUD reçoit AttributeSetRef en input pin et SET HUD.AttributeSetRef avant RefreshAllStats
- UpdateStatText : 6 GET natifs remplaces par GetStatValue (HealthCurrent, HealthMax, StaminaCurrent, StaminaMax, ManaCurrent, ManaMax)
- BP_MagicComponent.ConsumeMana : GET ManaCurrent natif -> GetStatValue("ManaCurrent")
- BP_SoM_PlayerController.OnHeroDied : GET HealthMax/StaminaMax/ManaMax natifs -> GetStatValue
- BP_SoM_GameMode.WriteSaveAndApplyFountainEffects : GET HealthMax/ManaMax natifs -> GetStatValue
- BP_Spell_Heal.ApplyEffect : GET HealthCurrent/HealthMax natifs -> GetStatValue

#### Bug critique resolu : HealthMax = 0 apres InitAttributesFromDatatable
- Cause : guard HealthMax dans SetStatValue contenait FMin(Value, GetStatValue("HealthCurrent")) -- HealthCurrent absent de la Map au moment du ForEach -> GetStatValue retourne 0 -> FMin(100, 0) = 0 -> HealthMax SET a 0
- Fix : suppression du FMin dans le guard HealthMax -- Value connecte directement au SET HealthMax natif sans borne
- Lecon : variables natives Max (HealthMax, StaminaMax, ManaMax) sont les seules a conserver dans BP_AttributeSet_Base -- les Current viennent uniquement de la Map

#### Bug diagnostique : AttributeSetRef null dans UI_HUD_Main
- Cause : InitHUD appelait RefreshAllStats sans avoir SET HUD.AttributeSetRef au prealable
- Fix : ajout input pin AttributeSetRef sur InitHUD + SET en premier noeud avant RefreshAllStats
- Gotcha : le SET doit etre fait dans InitHUD, pas dans le CreateWidget -- le pin Expose ne suffit pas

#### Reste a faire (prochaine session)
- Migrer ConsumeStamina / HandleStaminaRegen / StartStaminaRegen -> GetStatValue
- BP_CorruptionComponent : supprimer pre-clamp redondant (0,100) dans TrackDeityUsage
- Snapshots BP_AttributeSet_Base.md + UI_HUD_Main.md mis a jour

#### Notes techniques
- Variables natives a conserver dans BP_AttributeSet_Base : HealthMax, StaminaMax, ManaMax uniquement -- les Current vivent uniquement dans StatValues (TMap)
- Guard HealthMax dans SetStatValue : Value -> SET HealthMax natif directement, sans FMin ni GetStatValue
- InitHUD doit recevoir AttributeSetRef en parametre et le SET avant tout appel a RefreshAllStats
- Stamina/Mana s'affichaient malgre AttributeSetRef null car OnStatChanged du tick staminaregen creait les entrees Map apres coup -- HealthCurrent n'a pas ce mecanisme
- Option B = migration GetStatValue partout : pas de SET variables natives dans Default path de SetStatValue

---

### 04/06/2026 -- SYS-StatSystem (session 1) -- EN COURS

#### Decisions architecture
- Option B retenue : refacto complet BP_AttributeSet_Base -- TMap<Name, Float> x3 + GetStatValue + SetStatValue guards
- StatMinValues + StatMaxValues : deux Maps supplementaires peuplees par InitStats, lues par SetStatValue Default
- InitStats(StatDataTable : DataTable) : parametre passe par HC, pas stocke dans AttributeSet
- SetStatValue Default : pas de Switch residuel -- FClamp via StatMinValues/StatMaxValues
- Variables natives conservees comme cache synchronise pour lecteurs UI externes (dette C2)
- BP_CorruptionComponent : OwnerAttributeSet supprimee, variables locales dans chaque fonction

#### Realise
- DT_StatList : 3 rows ajoutees (EssenceValue, Corruption, TenaciteEtat)
- BP_CorruptionComponent : OwnerAttributeSet supprimee -> variables locales dans InitCorruption, TrackDeityUsage, PurgeCorruption
- BP_AttributeSet_Base : variables StatValues, StatMinValues, StatMaxValues (TMap<Name, Float>) ajoutees
- BP_AttributeSet_Base : InitStats() complete
- BP_AttributeSet_Base : GetStatValue(Name)->double complete (Pure)
- BP_AttributeSet_Base : SetStatValue -- 3 guards (EssenceValue, Corruption, HealthMax) + Default
- SetStatValue : 6 CallDelegate OnStatChanged branches sur Map_Add.then

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

#### BP_SoM_PlayerController -- OnHeroDied -- respawn Fontaine
- Apres SET bIsDead=false : GetGameMode -> Cast GameMode -> GET CurrentSaveGame -> IsValid
  - TRUE : GetComponentsByInterface(BPI_Saveable) -> ForEachLoop LoadData -> SetActorLocation(LastFountainTransform.Location) -> fade -> EnableInput
  - FALSE (premiere mort) : PlayerStart -> TeleportTo -> fade -> EnableInput

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
