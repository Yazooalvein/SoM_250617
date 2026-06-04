# BP_SoM_GameMode -- Snapshot

**Dernier snapshot :** 04/06/2026  
**Jalon :** SYS-StatSystem pre-audit  
**Path UE5 :** `Content/Core/BP_SoM_GameMode`  
**Type :** GameMode

---

## Variables

| Nom | Type |
|---|---|
| CurrentSaveGame | BP_SaveGame_SoM_C* |
| CurrentSlotName | FString |

---

## Fonctions

| Nom | SetStatValue | Flow |
|---|---|---|
| OnFountainRest(FountainID) | Aucun direct | Appelle CollectSaveData + CollectFountainTransform + WriteSaveAndApplyFountainEffects |
| CollectSaveData(FountainID) | Aucun | GetComponentsByInterface(BPI_Saveable) -> ForEach -> K2Node_Message(SaveData) |
| CollectFountainTransform(FountainID) | Aucun | GetAllActorsOfClass(BP_Fountain_Actor)[0] -> GetTransform -> SET LastFountainTransform |
| WriteSaveAndApplyFountainEffects | 2 directs + 1 indirect | Voir detail |

---

## Detail WriteSaveAndApplyFountainEffects

**SetStatValue directs (2) :**
- SetStatValue("HealthCurrent", GET AttributeSetRef.HealthMax)
- SetStatValue("ManaCurrent", GET AttributeSetRef.ManaMax)

**SetStatValue indirect (1) :**
- GetComponentByClass(BP_CorruptionComponent) -> PurgeCorruption(0) -> SetStatValue("Corruption", 0) dans CorruptionComponent

**Acces GET AttributeSet :** AttributeSetRef (4 connexions) -- cible des 2 SetStatValue + source HealthMax/ManaMax + source GetComponentByClass.

---

## Anomalies

| Anomalie | Description | Intentionnel ? |
|---|---|---|
| **StaminaCurrent NON restaure a la fontaine** | WriteSaveAndApplyFountainEffects restaure HP et Mana, mais pas Stamina | A confirmer avec Nico |
| CollectFountainTransform prend index 0 | GetAllActorsOfClass[0] -- pas de filtrage par FountainID | Dette connue -> C2 |

---

*Snapshot produit par audit agent UnrealClaude -- session 04/06/2026*
