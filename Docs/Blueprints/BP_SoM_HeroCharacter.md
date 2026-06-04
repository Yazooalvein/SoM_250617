# BP_SoM_HeroCharacter -- Snapshot

**Dernier snapshot :** 04/06/2026  
**Jalon :** SYS-StatSystem pre-audit  
**Path UE5 :** `Content/Characters/Players/Blueprint/BP_SoM_HeroCharacter`  
**Type :** Character (Blueprint Only)  
**EventGraph :** 287 nodes

---

## Variables pertinentes (stats et refs)

| Nom | Type | Categorie | Notes |
|---|---|---|---|
| AttributeSetRef | BP_AttributeSet_Base_C* | Stats\|Principals | Instance Editable -- cree dans InitAttributesFromDatatable |
| StatsDataTable | DataTable* | Stats\|Principals | Reference vers DT_StatList |
| bIsDead | bool | Default | |
| OnPlayerDeath | mcdelegate | Default | |
| bIsInvincible | bool | Default | |
| bRadialUnlocked | bool | Default | **ATTENTION : trailing space dans le nom de variable** |

---

## Fonctions

| Nom | SetStatValue | Acces GET AttributeSet | Notes |
|---|---|---|---|
| InitAttributesFromDatatable | 4 appels (voir detail) | HealthMax, StaminaMax, ManaMax | Cree aussi l'AttributeSet via Construct Object |
| EquipWeapon | Aucun | Aucun | |
| IsDead | Aucun | Aucun | Retourne bIsDead |
| Add_Main_HUD | Non verifie | Probable (passe AttributeSetRef au widget) | |

---

## Detail InitAttributesFromDatatable

**Construction de l'AttributeSet :** `Construct BP_AttributeSet_Base` (K2Node_GenericCreateObject) -> SET AttributeSetRef. L'objet est cree ici, pas en BeginPlay.

**Appels SetStatValue (4) :**

| # | StatName | Valeur | Dynamique |
|---|---|---|---|
| 1 | StatID (depuis row DT) | BaseValue (depuis row DT) | **OUI** -- ForEach GetDataTableRowNames -> GetDataTableRow -> BreakStatStruct |
| 2 | "HealthCurrent" | GET AttributeSetRef.HealthMax | Non -- initialise HP = MaxHP apres boucle DT |
| 3 | "StaminaCurrent" | GET AttributeSetRef.StaminaMax | Non |
| 4 | "ManaCurrent" | GET AttributeSetRef.ManaMax | Non |

**Note importante :** HC lit deja DT_StatList via GetDataTableRowNames. Apres SYS-StatSystem, InitStats() dans BP_AttributeSet_Base fera ce travail -- InitAttributesFromDatatable devra etre simplifie (appel InitStats() + init Current = Max).

---

## Acces GET AttributeSet dans EventGraph

| Position Y | Variable lue | Usage |
|---|---|---|
| ~4880 | AttributeSetRef | Passage au composant |
| ~4944 | EssenceValue (int64) | Lecture avant spawn BP_EssenceDrop |
| ~-3760 | AttributeSetRef (2 conn.) | Contexte OnHeroDied -- lecture pour drop Essence |

---

## Anomalies

| Anomalie | Description |
|---|---|
| Trailing space sur bRadialUnlocked | Nom de variable avec espace invisible -- risque de bug sur comparaisons de nom |
| InitAttributesFromDatatable cree l'AttributeSet | Apres SYS-StatSystem, InitStats() dans BP_AttributeSet_Base prend le relais pour peupler la TMap -- a refactoriser |

---

*Snapshot produit par audit agent UnrealClaude -- session 04/06/2026*
