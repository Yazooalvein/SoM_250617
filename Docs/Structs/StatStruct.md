# StatStruct -- Snapshot

**Dernier snapshot :** 04/06/2026  
**Jalon :** SYS-StatSystem pre-audit  
**Path UE5 :** `Content/Systems/Stats/StatStruct`  
**Source :** Infere depuis pins K2Node_BreakStruct dans InitAttributesFromDatatable

---

## Champs

| Champ | Type | Usage |
|---|---|---|
| StatID | Name | Cle SetStatValue -- passee directement comme StatName |
| DisplayName | Text | UI |
| Description | Text | UI |
| Type | byte (-> EStatType) | Categorisation (Principal, Elem, Second, Progression, Temp) |
| Element | byte (-> EElementType) | Affinite elementaire |
| BaseValue | double | Valeur initiale passee a SetStatValue dans InitStats() |
| MinValue | double | Clamp minimum -- utilise dans SetStatValue refactorise |
| MaxValue | double | Clamp maximum -- utilise dans SetStatValue refactorise |
| IsModifiable | bool | Reserve pour future logique de lock de stat |
| Icone | Texture2D* | UI |
| GameplayTag | GameplayTag | Reserve pour systeme de tags futur |

---

## Notes pour SYS-StatSystem

- `StatID` = la cle exacte a utiliser pour MAP SET/FIND dans StatValues
- `BaseValue` = valeur initiale dans InitStats()
- `MinValue` / `MaxValue` = bornes du FClamp dans SetStatValue (remplace les guards hardcodes)
- Pour EssenceValue : MinValue=0, MaxValue=0 (pas de max) -> guard special necessaire
- Pour Corruption : MinValue=0, MaxValue=100 mais clamp conditionnel -> guard special (bCorruptionUnlocked)

---

*Snapshot infere depuis nodes -- session 04/06/2026*
