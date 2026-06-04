# UI_HUD_Main -- Snapshot

**Dernier snapshot :** 04/06/2026  
**Jalon :** SYS-StatSystem VALIDE PIE  
**Path UE5 :** `Content/UI/Widgets/Main/UI_HUD_Main`  
**Type :** UserWidget

---

## Variables

| Nom | Type | MemberGuid | Notes |
|---|---|---|---|
| AttributeSetRef | BP_AttributeSet_Base_C* | 263CFEF741EFFCAD5A6F159E54ECB206 | SET par InitHUD en premier noeud -- jamais null apres init |
| HealthPercent | double | -- | 0..1 pour ProgressBar |
| StaminaPercent | double | -- | 0..1 pour ProgressBar |
| ManaPercent | double | -- | 0..1 pour ProgressBar |
| EssenceValue | double | -- | Cache local -- NewValue du dispatcher |
| CorruptionPercent | double | -- | 0..1 pour ProgressBar (NewValue / 100) |
| RichTextBlock_HP | RichTextBlock | 9FB1E1E74F87B04B1399889DB47B3275 | Widget UMG |
| RichTextBlock_ST | RichTextBlock | 8F6496EE473F238DB56355BDA9BB55B2 | Widget UMG |
| RichTextBlock_MP | RichTextBlock | 6DF4F5E04C2EEEF13570BD80F37ED786 | Widget UMG |
| TextBlock_Essence | RichTextBlock | 49257A7047B9394A35C2A89A6EA8ADEB | Widget UMG |

---

## Fonctions

### InitHUD (input : AttributeSetRef : BP_AttributeSet_Base)
```
FunctionEntry(AttributeSetRef)
  -> SET HUD.AttributeSetRef = AttributeSetRef
  -> RefreshAllStats
  -> UpdateStatText
```
Appele depuis HC.Add_Main_HUD apres CreateWidget. Le pin AttributeSetRef est connecte a HC.AttributeSetRef.

**GOTCHA :** SET HUD.AttributeSetRef doit etre le PREMIER noeud -- RefreshAllStats ne peut pas s'executer avec une ref nulle.

---

### RefreshAllStats
```
GET HUD.AttributeSetRef
  -> SET HealthPercent   = GetStatValue("HealthCurrent") / GetStatValue("HealthMax")
  -> SET StaminaPercent  = GetStatValue("StaminaCurrent") / GetStatValue("StaminaMax")
  -> SET ManaPercent     = GetStatValue("ManaCurrent") / GetStatValue("ManaMax")
  -> SET EssenceValue    = GetStatValue("EssenceValue")
  -> SET CorruptionPercent = GetStatValue("Corruption") / 100
  -> UpdateStatText
```
Aucun GET variable native -- tout passe par GetStatValue.

---

### HUD_OnStatChanged (StatName:Name, NewValue:double)
Custom Event bind sur AttributeSetRef.OnStatChanged dans Event Construct.  
Corps simplifie : appel direct a RefreshAllStats (Switch supprime).
```
HUD_OnStatChanged -> RefreshAllStats
```

---

### UpdateStatText
Ecrit dans les 3 RichTextBlock (HP, ST, MP) et TextBlock_Essence.  
Format : "Current / Max" (Concat_StrStr avec " / " comme separateur).
```
GET AttributeSetRef
  -> GetStatValue("HealthCurrent")  -> Conv_DoubleToText -> Conv_TextToString -> Concat " / " -> Conv_StringToText -> SetText(RichTextBlock_HP)
  -> GetStatValue("HealthMax")      -> Conv_DoubleToText -> Conv_TextToString -> Concat
  -> GetStatValue("StaminaCurrent") -> ...
  -> GetStatValue("StaminaMax")     -> ...
  -> GetStatValue("ManaCurrent")    -> ...
  -> GetStatValue("ManaMax")        -> ...
  -> GetStatValue("EssenceValue")   -> Conv_DoubleToString -> Conv_StringToText -> SetText(TextBlock_Essence)
```
Aucun GET variable native -- tout passe par GetStatValue.

**GOTCHA EssenceValue :** utiliser Conv_DoubleToString (pas Conv_Int64ToString) car GetStatValue retourne double.

---

### Event Construct
```
Bind Event OnStatChanged -> AddDelegate -> RefreshAllStats (refresh initial)
```

---

### Get_CorruptionBar_Percent (Pure)
Retourne `CorruptionPercent` (deja normalise 0..1). Binding ProgressBar.

---

## Dependances

| Direction | Blueprint | Fonction |
|---|---|---|
| Appele par | BP_SoM_HeroCharacter | Add_Main_HUD -> InitHUD |
| Ecoute | BP_AttributeSet_Base | OnStatChanged |
| Lit via | BP_AttributeSet_Base | GetStatValue |

---

## Architecture Option B (post SYS-StatSystem)

Plus aucun GET variable native dans UI_HUD_Main. Toutes les lectures de stats passent par `AttributeSetRef.GetStatValue(StatName)`. Les ProgressBar et RichTextBlocks sont alimentes par RefreshAllStats qui est appele :
- A l'init (InitHUD)
- A chaque OnStatChanged broadcast
- Au Event Construct (refresh initial)

---

*Snapshot mis a jour post-SYS-StatSystem -- 04/06/2026*
