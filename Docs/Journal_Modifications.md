# Journal des Modifications -- Shadow of Mana

## Objectif
Suivi precis de toutes les evolutions majeures du projet.

## Entrees

### 27/05/2026 -- RadialUnlock + blocages narratifs radial -- VALIDE PIE

#### BP_SoM_HeroCharacter -- nouvelle variable
- bRadialUnlocked (bool, default=false) : bloque l'ouverture complete du radial jusqu'a un evenement narratif

#### BP_SoM_PlayerController -- OpenRadial modifie
- Branch(bRadialUnlocked) en entree : FALSE -> Return, TRUE -> continuer flow existant
- Simule le deblocage narratif du radial en debut de jeu

#### UI_Radial_Main -- SwitchCategory modifie
- Branch avant switch vers Magic : MagicComponentRef.UnlockedSpells.Num() > 0
  - FALSE -> Return (pas de deite debloquee, switch bloque)
  - TRUE -> continuer

#### BP_Debug_UnlockDeity -- mis a jour
- Suppression UnlockDeity("Lumina") du BeginPlay de BP_SoM_HeroCharacter (stub hardcode)
- BP_Debug_UnlockDeity : overlap -> Cast BP_SoM_HeroCharacter -> UnlockDeity("Lumina") + SET bRadialUnlocked=true
- Simule l'evenement narratif complet : deblocage radial + deblocage deite

#### Decision architecture
- Pas de check DiscoveredWeapons >= 2 dans SwitchCategory
- bRadialUnlocked = flag narratif unique pour l'ouverture complete
- Grisage des categories = systeme existant (LockedDeities) pour les blocages ponctuels narratifs
- Raison : les blocages armes/magie sont rares et narratifs, pas mecaniques

#### Tests valides PIE
- Sans overlap : radial inaccessible (Triangle bloque)
- Apres overlap : radial ouvert, Lumina visible, sorts castables
- Sans overlap Lumina mais bRadialUnlocked=true : radial ouvert en mode Weapons, switch Magic bloque

#### Etat final
Systeme de deblocage narratif radial operationnel. bRadialUnlocked + UnlockedSpells.Num() couvrent les cas du debut de jeu.

---

### 27/05/2026 -- C1-MagicUnlockSystem -- VALIDE PIE

#### BP_MagicComponent -- Nouvelles variables
- LockedDeities (TArray<FName>) : deites temporairement verrouillee narrativement
- SpellUsageCounts (TMap<FName, int>) : compteur d'usage par sort
- SpellLevels (TMap<FName, int>) : niveau actuel par sort
- TalentPoints (int) : points talent disponibles
- CategoryThresholdsConfig (Class Reference BP_SpellCategoryThresholds) : config seuils par categorie

#### BP_MagicComponent -- Nouvelles fonctions
- IsDeityAccessible(DeityID) -> bool : Contains(UnlockedSpells) AND NOT Contains(LockedDeities)
- LockDeity(DeityID) : AddUnique(LockedDeities) -- pour evenements narratifs
- IncrementSpellUsage(SpellID) : usage -> seuil effectif -> LevelUpSpell si atteint
- LevelUpSpell(SpellID) : SpellLevels +1, reset compteur, AddTalentPoint
- AddTalentPoint() : TalentPoints +1, debug print

#### BP_MagicComponent -- CastSpell modifie
- Verification IsDeityAccessible(DeityID) en entree, avant CanCast
- IncrementSpellUsage(SpellID) branche apres Map_Add(SpellCooldowns)
- BeginPlay : stub UnlockDeity("Lumina") supprime

#### Systeme de progression -- formule SoM adaptee
- Courbe inspiree Secret of Mana : EffectiveThreshold = BaseThreshold / Max(1, 9 - CurrentSpellLevel)
- BaseThreshold differencie par categorie (Attack=150, Heal=100, Buff=50, Debuff=35, Ultime=200)
- Logique : Buff/Debuff (peu utilises) montent vite, Attack/Heal (spammes) montent lentement

#### BP_SpellCategoryThresholds -- nouvel asset
- Blueprint class (parent Object) dans Content/Systems/Magic/Data/
- TMap<E_SpellCategory, int> CategoryThresholds -- keyed directement par enum
- Acces via GetClassDefaults dans IncrementSpellUsage

#### Etat final
C1-MagicUnlockSystem VALIDE PIE. Chaine usage->niveau->points operationnelle avec courbe SoM adaptee.

---

### 26/05/2026 -- Session design -- Lore, Corruption, Fontaine de Fee, quetes deite

#### Etat final
Lore enrichi, mecanique Corruption posee, Fontaine de Fee integree narrativement.

---

### 26/05/2026 -- Session design -- Magic_Progression DESIGN

#### Etat final
Design progression magique pose dans Magic_Progression.md.

---

### 25/05/2026 -- Data layer deites + sortie mode dummy magie -- VALIDE PIE

#### Etat final
Sortie du mode dummy magie. Data layer deites complet et data-driven.

---

### 25/05/2026 -- Session design + outils IA

#### Etat final
C1-MagicProgressionDesign VALIDE.

---

### 23/05/2026 -- C1-InputsUI COMPLET -- VALIDE PIE

---

### 23/05/2026 -- Session design -- Architecture IMC complete

---

### 21/05/2026 -- Session design & documentation

---

### 19/05/2026 -- C1-HitFlashEnemies -- ARCHITECTURE COMPLETE

---

### 18/05/2026 -- C1-HitFeel PARTIEL -- VALIDE PIE

---

### 18/05/2026 -- C1-CollisionFix COMPLET -- VALIDE PIE

---

### 18/05/2026 -- J-ComboFix COMPLET -- VALIDE PIE

---

### 18/05/2026 -- J-TestBed COMPLET -- VALIDE PIE

---

### 18/05/2026 -- J-LockMove COMPLET -- VALIDE PIE

---

### 17/05/2026 -- J-Camera COMPLET -- VALIDE PIE

---

### 15/05/2026 -- J-Renommage COMPLET

---

### 15/05/2026 -- J-lock COMPLET -- VALIDE PIE

---

### 14/05/2026 -- Session design -- Roadmap globale refondee

---

### 14/05/2026 -- J-Nettoyage COMPLET

---

### 14/05/2026 -- Session creative J-ART ; Hero PLACEHOLDER COMPLET

---

### 14/05/2026 -- Session creative J-MUS (exploration workflow)

---

### 12-13/05/2026 -- Jalon J-13 COMPLET -- Radial Menu + Quickslot VALIDE PIE

---

### 12/05/2026 -- Jalon J-15 -- UI_HUD_Main FINALISE

---

### 12/05/2026 -- Jalons J-10 a J-14 -- POC Systeme Magie VALIDE PIE

---

### 11/05/2026 -- Session design

### 11/05/2026 -- Jalon #9 -- Audit complet + nettoyage

### 11/05/2026 -- Jalon #8 -- Migration UE5.7 + UnrealClaude

### 07/05/2026 -- Jalons #1 a #7

### 20/07/2025 -- Nico -- Animation Weapon Integration

### 27/06/2025 -- Nico -- BP_AIController_Enemy_Base, PawnSensing

### 26/06/2025 -- Nico -- BPI_TakeDamage, BP_Enemy_Base

### 24/06/2025 -- Nico -- Systeme armes data-driven, Radial, Combo

### 21/06/2025 -- Nico -- Refactorisation BP_ComboManagerComponent

### 19-20/06/2025 -- Nico -- Lock-On, Menu Radial, refonte Combo

### 18/06/2025 -- Nico -- Refactoring pipeline Gameplay de base

### 17/06/2025 -- Nico -- Creation du projet

---

## Rappel
Pour la roadmap detaillee : voir Docs/Roadmap_Gameplay.md
Pour les decisions architecturales : voir Docs/Architecture/Decisions.md
Pour les inputs et IMC : voir Docs/Architecture/Input_Architecture.md
Pour le radial menu : voir Docs/Architecture/RadialMenu_Architecture.md
Pour la progression magique : voir Docs/Architecture/Magic_Progression.md
Pour le lore et la narrative : voir Docs/Lore_ShadowOfMana.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 27/05/2026
