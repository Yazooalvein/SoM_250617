# UI_HUD_Main -- Snapshot

**Dernier snapshot :** 04/06/2026  
**Jalon :** SYS-StatSystem pre-audit  
**Path UE5 :** `Content/UI/Widgets/Main/UI_HUD_Main`  
**Type :** UserWidget

---

## Variables

| Nom | Type | Notes |
|---|---|---|
| PlayerCharacterRef | **(type vide)** | **ANOMALIE** -- reference corrompue ou type BP manquant |
| AttributeSetRef | BP_AttributeSet_Base_C* | |
| HealthPercent | double | Cache local normalise |
| StaminaPercent | double | Cache local normalise |
| ManaPercent | double | Cache local normalise |
| EssenceValue | double | Cache local -- stocke NewValue du dispatcher (double) |
| CorruptionPercent | double | Cache local normalise (/100) |

---

## Binding OnStatChanged

Bind dans Event Construct : `Bind Event to OnStatChanged` -> Custom Event `HUD_OnStatChanged(StatName:Name, NewValue:double)`

---

## Switch HUD_OnStatChanged (8 cases)

| Case | Action | Lit AttributeSet nativement |
|---|---|---|
| HealthCurrent | HealthPercent = NewValue / AttributeSetRef.HealthMax | Oui (HealthMax) |
| StaminaCurrent | StaminaPercent = NewValue / AttributeSetRef.StaminaMax | Oui (StaminaMax) |
| ManaCurrent | ManaPercent = NewValue / AttributeSetRef.ManaMax | Oui (ManaMax) |
| HealthMax | HealthPercent = NewValue / AttributeSetRef.HealthMax (NewValue EST le new Max) | Oui |
| StaminaMax | StaminaPercent recalculee | Oui |
| ManaMax | ManaPercent recalculee | Oui |
| EssenceValue | SET self.EssenceValue = NewValue (direct) | Non |
| Corruption | CorruptionPercent = NewValue / 100 | Non |

Apres toutes les cases -> Call UpdateStatText (8 connexions exec entrantes).

---

## UpdateStatText (37 nodes)

Lit directement les variables natives de AttributeSetRef : HealthCurrent, HealthMax, StaminaCurrent, StaminaMax, ManaCurrent, ManaMax, EssenceValue (int64 -> To String).

**UpdateEssenceText :**
```
GET self.EssenceValue (double) -> To Integer64(Float) -> To String -> SetText(TextBlock_Essence)
```
Lit le cache HUD (double), pas directement l'AttributeSet. Meme risque precision double->int64.

---

## Get_CorruptionBar_Percent (Pure)

Retourne `CorruptionPercent` (deja normalise via /100 dans le switch). Correct pour binding ProgressBar.

---

## Anomalies

| Anomalie | Description | Impact |
|---|---|---|
| PlayerCharacterRef type vide | Reference corrompue ou type BP manquant | Pas lie aux stats -- a investiguer |
| UpdateStatText lit variables natives | Acces GET direct sur HealthCurrent/HealthMax/etc. -- bypasse GetStatValue | OK tant que variables natives restent en cache synchronise (SYS-StatSystem) |
| Cache EssenceValue double | self.EssenceValue stocke NewValue (double) puis reconverti en int64 pour affichage | Meme risque precision que BP_EssenceDrop |

---

*Snapshot produit par audit agent UnrealClaude -- session 04/06/2026*
