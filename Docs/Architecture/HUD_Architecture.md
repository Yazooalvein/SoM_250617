# Architecture Technique -- HUD Principal

---

## Objectif du module

Definir la structure et les regles du HUD principal en jeu :
- Jauges principales (vie, stamina, mana) avec texte Current/Max
- XP, icone arme active
- Pipeline event-driven via OnStatChanged (zero polling)

---

## Composants principaux

- `UI_HUD_Main` (widget Blueprint central) -- FINALISE 12/05/2026
- `BP_PlatformingCharacter` (cree le widget, passe AttributeSetRef, appelle InitHUD)
- `BP_AttributeSet_Base` (dispatche OnStatChanged a chaque changement de stat)
- `DT_HUD_RichTextStyle` (DataTable styles texte pour RichTextBlocks)

---

## Layout UI_HUD_Main (finalise)

```
Canvas Panel
└── HUD_Anchor (bas-gauche, pos 20/-20, size 400x150, alignment 0/1)
    ⚠️ Size To Content DOIT etre DECOCHE
    └── Horizontal Box
        ├── SizeBox_Weapon (64x64, Auto, V-Center, padding Right 8)
        │   └── Image_Weapon (Fill/Fill)
        └── HUD_Main_VertBox (Fill 1.0)
            ├── Overlay_HP (Fill 1.0)
            │   ├── SizeBox > HealthBar (Fill/Fill, rouge, binding Get_HealthBar_Percent)
            │   └── RichTextBlock_HP (Center/Center, Is Variable)
            ├── Overlay_ST (Fill 1.0)
            │   ├── SizeBox > StaminaBar (Fill/Fill, vert)
            │   └── RichTextBlock_ST (Center/Center, Is Variable)
            ├── Overlay_MP (Fill 1.0)
            │   ├── SizeBox > ManaBar (Fill/Fill, bleu)
            │   └── RichTextBlock_MP (Center/Center, Is Variable)
            └── XP (Auto, padding Top 8, violet, Is Variable)
```

---

## Variables, Fonctions & Bindings cles

### Variables locales (Float, default 1.0)
- `HealthPercent`, `StaminaPercent`, `ManaPercent`

### Fonctions de binding (pure)
- `Get_HealthBar_Percent` -> return HealthPercent
- `Get_StaminaBar_Percent` -> return StaminaPercent
- `Get_ManaBar_Percent` -> return ManaPercent

### Fonction UpdateStatText(Current Float, Max Float, Target RichTextBlock)
- Pipeline : To Text (Float, 0 decimales) -> To String -> Append " / " -> To Text String -> Set Text
- Centralisee, appelee depuis HUD_OnStatChanged ET InitHUD
- Supprime les decimales (Max/Min Fractional Digits = 0 sur To Text Float)

### Custom Event HUD_OnStatChanged(StatName Name, NewValue Float)
- Switch on Name :
  - HealthCurrent  -> SET HealthPercent  = NewValue / HealthMax + UpdateStatText(HP)
  - StaminaCurrent -> SET StaminaPercent = NewValue / StaminaMax + UpdateStatText(ST)
  - ManaCurrent    -> SET ManaPercent    = NewValue / ManaMax + UpdateStatText(MP)
  - HealthMax      -> SET HealthPercent  = HealthCurrent / NewValue (barre reactit aux Max)
  - StaminaMax     -> SET StaminaPercent = StaminaCurrent / NewValue
  - ManaMax        -> SET ManaPercent    = ManaCurrent / NewValue

### Fonction InitHUD
- Appelee depuis BP_PlatformingCharacter apres Add to Viewport
- Init les 3 *Percent + appelle UpdateStatText pour les 3 RichTextBlocks
- Garantit affichage correct des la premiere frame

### Event Construct
- Bind HUD_OnStatChanged sur AttributeSetRef.OnStatChanged

---

## DT_HUD_RichTextStyle

- Chemin : Content/UI/Widgets/Main/DT_HUD_RichTextStyle
- Row structure : RichTextStyleRow
- Row "Default" : font de base, taille readable
- Assigne sur les 3 RichTextBlocks via Text Style Set
- ⚠️ RichTextBlock sans DT assigne n'affiche rien (contrairement a TextBlock)
- Base extensible : futures rows pour styles par stat (HP rouge, MP bleu) ou divinite

---

## Pipeline d'integration

1. BeginPlay (BP_PlatformingCharacter) :
   - InitAttributesFromDatatable -> stats initialisees via SetStatValue
   - Add_Main_HUD : Create Widget (AttributeSetRef Expose on Spawn) -> Add to Viewport -> InitHUD

2. Event Construct (widget) :
   - Bind HUD_OnStatChanged sur AttributeSetRef.OnStatChanged

3. Mise a jour en jeu :
   - SetStatValue -> OnStatChanged -> HUD_OnStatChanged -> SET *Percent + UpdateStatText
   - Zero acces direct a AttributeSetRef apres l'init

---

## Points d'attention techniques

- SizeBox obligatoire autour de chaque ProgressBar (sinon Desired Size force hauteur excessive)
- Size To Content sur HUD_Anchor doit etre DECOCHE
- RichTextBlock necessite DataTable assignee dans Text Style Set
- To Text (Float) : Max/Min Fractional Digits = 0 pour format entier
- Alignement RichTextBlock dans Overlay : Horizontal Center + Vertical Center
- Alignement HealthBar dans Overlay : Fill/Fill

---

## Roadmap locale

- [x] Widget HUD avec jauges Health/Stamina/Mana
- [x] AttributeSetRef passe en Expose on Spawn
- [x] Migration polling -> event-driven via OnStatChanged
- [x] InitHUD pour initialisation correcte au lancement
- [x] RichTextBlock Current/Max avec UpdateStatText centralisee
- [x] DT_HUD_RichTextStyle + font de base
- [x] HUD reactif aux changements de Max (HealthMax, StaminaMax, ManaMax)
- [ ] Image_Weapon : assigner texture depuis arme equipee
- [ ] XP : binding sur XPCurrent/XPMax
- [ ] Buffs/Debuffs actifs : icones en overlay
- [ ] UI_QuickslotBar : 3 slots sorts rapides (J-13)

---

## Liens

- Stats_Architecture.md
- UI_Architecture.md
- Journal_Modifications.md

---

## Historique

- Creation : 17/06/2025
- Migration event-driven : 10/05/2026
- Finalisation layout + RichTextBlock + UpdateStatText : 12/05/2026
- Derniere mise a jour : 12/05/2026
