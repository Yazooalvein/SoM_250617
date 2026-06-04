# DT_StatList -- Snapshot

**Dernier snapshot :** 04/06/2026  
**Jalon :** SYS-StatSystem pre-audit  
**Path UE5 :** `Content/Systems/Stats/DT_StatList`  
**Structure :** StatStruct  
**Rows listables via MCP :** NON (blueprint_query ne peut pas lister les rows d'une DataTable)

---

## Rows connues (depuis audit visuel precedent)

| RowName | StatID | Type | Element | BaseValue | MinValue | MaxValue |
|---|---|---|---|---|---|---|
| HealthMax | HealthMax | Principal | None | 100.0 | 0.0 | 9999.0 |
| StaminaMax | StaminaMax | Principal | None | 50.0 | 0.0 | 999.0 |
| StaminaRegenInterval | StaminaRegenInterval | Principal | None | 0.1 | 0.0 | 0.0 |
| StaminaCostJump | StaminaCostJump | Principal | None | 5.0 | 1.0 | 20.0 |
| StaminaRegenRate | StaminaRegenRate | Principal | None | 10.0 | 0.0 | 50.0 |
| StaminaRegenDelay | StaminaRegenDelay | Principal | None | 1.0 | 0.0 | 0.0 |
| ManaMax | ManaMax | Principal | None | 999.0 | 0.0 | 999.0 |
| Affinity_Athanor | Resistance_Athanor | Elem | Athanor | 0.0 | 0.0 | 0.0 |
| Res_Ombre | Resistance_Ombre | Elem | Ombre | 0.0 | 0.0 | 0.0 |
| Waepon_lvl | Weapon_Level | Progression | None | 1.0 | 0.0 | 10.0 |
| StaminaCostDash | StaminaCostDash | Principal | None | 10.0 | 0.0 | 50.0 |

**Total : 11 rows**

---

## Rows absentes de DT_StatList (stats dans BP_AttributeSet_Base non listees)

Les stats suivantes existent dans BP_AttributeSet_Base mais N'ONT PAS de row dans DT_StatList :

| Stat manquante | Notes |
|---|---|
| HealthCurrent | Normal -- Current est derive de Max |
| StaminaCurrent | Normal -- Current est derive de Max |
| ManaCurrent | Normal -- Current est derive de Max |
| EssenceValue | A ajouter -- type int64, cas special |
| Corruption | A ajouter -- clamp conditionnel Phase1/Phase2 |
| TenaciteEtat | A ajouter -- base 25, clamp(0,100) |
| bCorruptionUnlocked | Flag bool -- ne va pas dans DT_StatList |
| bIsStaminaRegenerating | Flag bool -- ne va pas dans DT_StatList |

**Action requise avant SYS-StatSystem :** Ajouter EssenceValue, Corruption, TenaciteEtat dans DT_StatList. Confirmer MinValue/MaxValue pour chaque.

---

*Snapshot produit par audit agent UnrealClaude + audit visuel precedent -- session 04/06/2026*
