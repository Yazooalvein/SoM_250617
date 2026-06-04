# BP_SoM_PlayerController -- Snapshot

**Dernier snapshot :** 04/06/2026  
**Jalon :** SYS-StatSystem pre-audit  
**Path UE5 :** `Content/Characters/Players/Blueprint/BP_SoM_PlayerController`  
**Type :** PlayerController  
**EventGraph :** 214 nodes

---

## Variables

| Nom | Type | Notes |
|---|---|---|
| PlayerCharacterRef | BP_SoM_HeroCharacter_C* | |
| RadialMainRef | UI_Radial_Main_C* | |
| LockOnIndicatorWidgetRef | UI_LockOnIndicator_C* | |
| bSwitchInProgress | bool | |
| QuickslotUp / Left / Right | FName | |
| bPlayerIsLooking | bool | Camera lock-on |
| LockOnReturnSpeed | double | |

---

## SetStatValue dans EventGraph (zone OnHeroDied)

**IMPORTANT -- Recherche MCP :** `search_nodes("SetStatValue")` retourne 0 resultats. Utiliser `search_nodes("Set Stat Value")` (avec espaces) pour trouver ces nodes.

| StatName | Valeur | Position Y |
|---|---|---|
| "EssenceValue" | **0.0 hardcode** (Value pin non connecte) | ~-4128 |
| "HealthCurrent" | Valeur dynamique (Max) | ~-4080 |
| "StaminaCurrent" | Valeur dynamique (Max) | ~-3968 |
| "ManaCurrent" | Valeur dynamique (Max) | ~-3824 |

**Acces GET AttributeSet :**
- AttributeSetRef via Cast HC (Y~-3760, 2 conn.) -- cible des 4 SetStatValue
- AttributeSetRef (Y~-3712, 6 conn.) -- lecture HealthMax, StaminaMax, ManaMax pour les valeurs Max

---

## Fonctions

| Nom | SetStatValue | Notes |
|---|---|---|
| InitializeSystems | Aucun | Cast HC -> GetComponentByClass(CombatLockOnComponent) -> Bind delegates |
| OnHeroDied | 4 appels (voir ci-dessus) | Event bind depuis BeginPlay |

---

## Anomalies

| Anomalie | Description |
|---|---|
| EssenceValue = 0 hardcode | Value pin non connecte sur le node SetStatValue -- bug silencieux si jamais le pin est connecte a autre chose |
| search_nodes sensible aux espaces | "SetStatValue" -> 0 res. "Set Stat Value" -> resultats. Retenir pour audits futurs. |

---

*Snapshot produit par audit agent UnrealClaude -- session 04/06/2026*
