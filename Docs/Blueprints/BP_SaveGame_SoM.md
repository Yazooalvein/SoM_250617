# BP_SaveGame_SoM -- Snapshot

**Path UE5 :** `/Game/Systems/Save/BP_SaveGame_SoM`
**Parent :** SaveGame
**Noeuds totaux :** 0 (conteneur pur)
**Dernier snapshot :** 05/06/2026 -- Audit global

---

## Variables

| Nom | Type | Notes |
|---|---|---|
| SaveSlotName | FString | |
| SaveVersion | int32 | |
| LastFountainID | FName | |
| LastFountainTransform | Transform | |
| HealthCurrent | double | ⚠️ non persistee en pratique (restauree a Max au load) |
| StaminaCurrent | double | ⚠️ idem |
| ManaCurrent | double | ⚠️ idem |
| EssenceValue | double | Persistee |
| Corruption | double | Persistee |
| bCorruptionUnlocked | bool | Persistee |
| HeroLevel | int32 | |
| DiscoveredWeapons | TArray<FName> | |
| CurrentWeaponID | FName | |
| CurrentWeaponLevel | int32 | |
| LockedDeities | TArray<FName> | Sauvegarde delta (UnlockedSpells reconstruit au load) |
| SpellUsageCounters | TMap<FName,int32> | |
| ActivatedFountains | TArray<FName> | |
| CompletedNarrativeFlags | TArray<FName> | Reserve C3 |
| DroppedEssenceAmount | int64 | |
| DroppedEssenceLocation | Vector | |
| CurrentSaveGame | BP_SaveGame_SoM_C* | ⚠️ auto-reference circulaire potentielle -- a verifier |

## Notes techniques

- HP/ST/MP present dans le conteneur mais non utilisees -- restaurees a Max au load via SetStatValue
- LockedDeities = delta sauvegarde -- UnlockedSpells reconstruit depuis DT_Deities via UnlockDeity() au load
- ActivatedFountains : liste FName des fontaines activees (bIsActivated) -- a utiliser dans UI-FountainMenu
- `CurrentSaveGame` auto-referentielle : variable a investiguer avant tout travail sur le save system
