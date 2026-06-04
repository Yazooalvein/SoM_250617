# Journal des Modifications -- Shadow of Mana

## Objectif
Suivi precis de toutes les evolutions majeures du projet.

## Entrees

### 05/06/2026 -- DESIGN-ReplanificationC1 -- session design

#### Replanification jalons C1
- MAGIC-TreeModule reporte C2 : Lumina 4 sorts suffit pour POC C1, arbre talents = contenu pas mecanique bloquante
- ANIM-Pass1 reporte C2 : dette technique, ABP_Manny_Platforming fonctionnel meme mal nomme
- ENEMY-DropSystem ajoute C1 : mort ennemi -> spawn BP_EssenceDrop + chance objet -- retour tangible indispensable
- UI-FountainMenu ajoute C1 : refacto BP_FountainComponent + mini-menu deux interactions

#### Design Fontaine de Fee -- VALIDE
- Interaction volontaire (pas overlap automatique) -- refacto BP_FountainComponent a prevoir
- bIsActivated=false (1ere fois) : animation + regen HP/ST/MP + save spawn -- pas de menu, pas de respawn
- bIsActivated=true (suivantes) : ouvre UI_FountainMenu
- UI_FountainMenu.Se reposer : regen + save + respawn ennemis zone + PurgeCorruption + restock objets
- UI_FountainMenu.Menu Inventaire : quickslots + upgrade magie/deites + level up hero (Essence)
- Essence = monnaie unique (level + magie + purge) -- tension intentionnelle style DS
- Acces menu gestion : Fontaine uniquement (pas de menu pause global pour ces fonctions)
- Visuel C1 : changement couleur/materiau sur bIsActivated
- Vision ART future : racines arbre Mana poussant a l'activation (Fee), Fee se reposant dans la Fontaine -- note en maturation, session ART-Fontaine a planifier

#### Nouvel ordre jalons C1 restants
1. ENEMY-DropSystem
2. UI-FountainMenu (+ refacto BP_FountainComponent)
3. ENEMY-Base
4. ENEMY-Boss1
5. MAP-C1Level

#### Etat final
Session design pure. Aucun Blueprint modifie. Roadmap, CLAUDE.md et Decisions.md mis a jour.

---

### 04/06/2026 -- SYS-StatSystem -- VALIDE PIE

#### SYS-StatSystem CLOS -- validation PIE complete
- Stats (HP/ST/MP/Essence/Corruption) : affichage HUD correct
- Fontaine : save + restauration HP/ST/MP + PurgeCorruption OK
- Mort/respawn : drop Essence + fade + reset stats + respawn Fontaine/PlayerStart OK
- Magie : ConsumeMana via GetStatValue OK, sorts Lumina operationnels
- Attaques : equip armes + combo Light/Heavy OK

#### Session 2 -- HUD + migration Option B
- Migration Option B complete : tous les lecteurs passent par GetStatValue -- plus aucun GET variable native hors BP_AttributeSet_Base
- UI_HUD_Main : RefreshAllStats creee, HUD_OnStatChanged simplifie (switch supprime -> appel direct RefreshAllStats)
- InitHUD(AttributeSetRef) : SET HUD.AttributeSetRef en premier noeud avant RefreshAllStats
- UpdateStatText : 6 GetStatValue (HealthCurrent/Max, StaminaCurrent/Max, ManaCurrent/Max)
- Migres vers GetStatValue : BP_MagicComponent.ConsumeMana, BP_SoM_PlayerController.OnHeroDied, BP_SoM_GameMode.WriteSaveAndApplyFountainEffects, BP_Spell_Heal.ApplyEffect, ConsumeStamina, HandleStaminaRegen, StartStaminaRegen
- BP_CorruptionComponent.TrackDeityUsage : pre-clamp redondant (0,100) supprime

#### Bug critique resolu : HealthMax = 0
- Cause : guard HealthMax contenait FMin(Value, GetStatValue("HealthCurrent")) -- HealthCurrent absente de la Map au moment du ForEach -> FMin(100, 0) = 0
- Fix : Value connecte directement au SET HealthMax natif -- FMin supprime

#### Bug resolu : AttributeSetRef null dans UI_HUD_Main
- Cause : InitHUD appelait RefreshAllStats sans avoir SET HUD.AttributeSetRef
- Fix : ajout input pin AttributeSetRef sur InitHUD + SET en premier noeud

#### Session 1 -- Architecture TMap
- BP_AttributeSet_Base : TMap StatValues + StatMinValues + StatMaxValues
- InitStats() : ForEach DT_StatList -> Map_Add x3
- GetStatValue(Name) : Pure, Map_Find + debug
- SetStatValue : guards EssenceValue + Corruption + HealthMax + Default (FClamp) + 6 CallDelegate OnStatChanged
- BP_CorruptionComponent : OwnerAttributeSet supprimee -> variables locales dynamiques

#### Architecture post-jalon
- Variables natives BP_AttributeSet_Base : HealthMax, StaminaMax, ManaMax UNIQUEMENT
- HealthCurrent/StaminaCurrent/ManaCurrent : StatValues uniquement -- pas de native
- DT_StatList : 14 rows, pas de rows Current (initialisees post-ForEach via SetStatValue(Current=Max))

#### Etat final
SYS-StatSystem VALIDE PIE complet. Tous les systemes C1 core valides.

---

### 03/06/2026 -- SYS-SaveGame -- VALIDE PIE

#### Etat final
SYS-SaveGame VALIDE PIE. Overlap Fontaine -> save + restauration HP/ST/MP/Corruption. Mort -> drop Essence -> respawn Fontaine. Premiere mort sans save -> respawn PlayerStart.

---

### 02/06/2026 -- SYS-EssenceMana -- VALIDE PIE

#### Etat final
BP_EssenceDrop VALIDE PIE. Mort -> drop Essence + fade -> respawn. Pickup -> restitution Essence + HUD.

---

### 31/05/2026 -- SYS-CorruptionSystem -- VALIDE PIE

#### Etat final
BP_CorruptionComponent VALIDE PIE. TrackDeityUsage, PurgeCorruption, GetWeakDeity operationnels.

---

### 31/05/2026 -- COMBAT-SwordMoveset -- CLOS VALIDE PIE

#### Etat final
Combo epee fonctionnel (Light x2 + Heavy x1). TenaciteEtat dans AttributeSet (base 25).

---

### 31/05/2026 -- SaveDesign + C1-HUDCore -- VALIDE

#### Etat final
DESIGN-SaveDesign + HUD-Core valides.

---

### 30/05/2026 -- DESIGN-WeaponProgression -- VALIDE

---

### 29/05/2026 -- Session design Lore + C1-WeaponArchitecture -- CLOTURE

---

### 28/05/2026 -- Sessions design -- Stats / StatusEffects / Corruption / Economy / Lore

---

### 27/05/2026 -- C1-CleanupDettes + MagicUnlockSystem + RadialUnlock -- VALIDE PIE

---

### 25-26/05/2026 -- Data layer deites + Magic_Progression DESIGN

---

### 23/05/2026 -- C1-InputsUI COMPLET -- VALIDE PIE

---

### 18-21/05/2026 -- CollisionFix / HitFeel / ComboFix / TestBed / LockMove

---

### 17/05/2026 -- J-Camera COMPLET -- VALIDE PIE

---

### 15/05/2026 -- J-lock + J-Renommage COMPLET

---

### 14/05/2026 -- Session design Roadmap + J-Nettoyage + ART + MUS

---

### 12-13/05/2026 -- J-13 Radial Menu + J-15 HUD_Main + J-10 a J-14 POC Magie

---

### 11/05/2026 -- Sessions design + jalons #8 et #9

### 07/05/2026 -- Jalons #1 a #7

### 2025 -- Sessions fondatrices (voir historique complet)

---

## Rappel
Pour la roadmap detaillee : voir Docs/Roadmap_Gameplay.md
Pour les decisions architecturales : voir Docs/Architecture/Decisions.md
Pour les stats et progression : voir Docs/Architecture/Stats_Progression.md
Pour les effets de statut et corruption : voir Docs/Architecture/Combat_StatusEffects.md
Pour l'economie et les drops : voir Docs/Architecture/Economy_Drops.md
Pour le lore et la narrative : voir Docs/Lore_ShadowOfMana.md
Pour la progression armes : voir Docs/Architecture/Weapons_Progression.md
Pour le systeme de save : voir Docs/Architecture/SaveSystem.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 05/06/2026
