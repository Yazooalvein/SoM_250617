# BP_SaveGame_SoM -- Snapshot

**Path UE5 :** `/Game/Systems/Save/BP_SaveGame_SoM`
**Parent :** SaveGame
**Noeuds totaux :** 0 (conteneur pur -- aucune logique)
**Dernier snapshot :** 07/06/2026 -- UI-FountainMenu

---

## Variables

| Nom | Type UE5 reel | Notes |
|---|---|---|
| SaveSlotName | FString | |
| SaveVersion | int32 | |
| LastFountainID | FName | Fontaine de dernier repos |
| LastFountainTransform | Transform | Position spawn apres mort |
| HealthCurrent | double | Presente mais non persistee (restauree a Max au load) |
| StaminaCurrent | double | Presente mais non persistee (restauree a Max au load) |
| ManaCurrent | double | Presente mais non persistee (restauree a Max au load) |
| EssenceValue | **int64** | Persistee -- type int64 (pas double) |
| Corruption | double | Persistee |
| bCorruptionUnlocked | bool | Persistee |
| HeroLevel | int32 | Reserve |
| DiscoveredWeapons | TArray\<FName\> | |
| CurrentWeaponID | FName | |
| CurrentWeaponLevel | int32 | |
| LockedDeities | TArray\<FName\> | Sauvegarde delta -- UnlockedSpells reconstruit depuis DT_Deities au load |
| SpellUsageCounters | **FName** | ⚠️ TYPE INCORRECT -- devrait etre TMap\<FName,int32\>. Probablement vide/inutilise. |
| ActivatedFountains | TArray\<FName\> | Fontaines activees -- ajoute jalon UI-FountainMenu |
| CompletedNarrativeFlags | TArray\<FName\> | Reserve C3 |
| DroppedEssenceAmount | int64 | |
| DroppedEssenceLocation | Vector | |
| CurrentSaveGame | BP_SaveGame_SoM_C* | ⚠️ Auto-reference circulaire -- a investiguer/supprimer |

## Notes techniques

- Conteneur pur : aucun EventGraph, aucune fonction. Les BPs clients (InventoryComponent, etc.) implementent BPI_Saveable.
- HP/ST/MP presentes dans le conteneur mais non utilisees en pratique -- restaurees a Max via SetStatValue au load.
- **SpellUsageCounters** : type FName dans UE5 (pas TMap). Dette de creation -- a corriger avant implementation du systeme de sorts C2.
- **CurrentSaveGame** : auto-reference BP_SaveGame_SoM dans un BP_SaveGame_SoM -- origine inconnue, probablement vestige. Ne pas utiliser.
- EssenceValue : int64 dans le SaveGame, double dans StatValues -- conversion a la serialisation.
- ActivatedFountains : TArray\<FName\> de FountainID -- peuple par BP_FountainComponent.SaveData.
