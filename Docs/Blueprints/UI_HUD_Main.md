# UI_HUD_Main -- Snapshot

**Path UE5 :** `/Game/UI/Widgets/Main/UI_HUD_Main`
**Parent :** UserWidget
**Noeuds totaux :** 88
**Dernier snapshot :** 05/06/2026 -- Audit global

---

## Variables

| Nom | Type | Notes |
|---|---|---|
| AttributeSetRef | BP_AttributeSet_Base_C* | SET par InitHUD avant RefreshAllStats |
| PlayerCharacterRef | (type vide) | ⚠️ vestige debug -- a supprimer UI-HUDPolish C4 |
| HealthPercent | double | Calcule par RefreshAllStats |
| StaminaPercent | double | |
| ManaPercent | double | |
| EssenceValue | double | Conv_DoubleToString pour affichage |
| CorruptionPercent | double | GetStatValue("Corruption") / 100 |

## Fonctions

| Nom | Inputs | Outputs | Notes |
|---|---|---|---|
| InitHUD | AttributeSetRef:BP_AttributeSet_Base_C* | -- | SET ref -> RefreshAllStats -> UpdateStatText |
| RefreshAllStats | -- | -- | Recalcule tous % via GetStatValue |
| UpdateStatText | -- | -- | Textes Current/Max x3 + EssenceValue |
| UpdateEssenceText | -- | -- | |
| Get_HealthBar_Percent | -- | float | Binding ProgressBar |
| Get_StaminaBar_Percent | -- | float | |
| Get_ManaBar_Percent | -- | float | |
| Get_CorruptionBar_Percent | -- | double | |

**EventGraph :** 4 events dont HUD_OnStatChanged -> RefreshAllStats (switch supprime)

## Dependances

**Appelle :** BP_AttributeSet_Base.GetStatValue
**Cree par :** BP_SoM_HeroCharacter.Add_Main_HUD

## Notes techniques

- InitHUD DOIT SET HUD.AttributeSetRef AVANT RefreshAllStats -- sinon AttributeSetRef null
- EssenceValue : Conv_DoubleToString (pas Conv_Int64ToString)
- CorruptionPercent = GetStatValue("Corruption") / 100 (ProgressBar attend 0..1)
- HUD_OnStatChanged -> appel direct RefreshAllStats (plus de Switch)
