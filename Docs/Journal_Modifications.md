# Journal des Modifications -- Shadow of Mana

## Objectif
Suivi precis de toutes les evolutions majeures du projet.

## Entrees

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
- Courbe progressive sans explosion exponentielle en fin de progression

#### BP_SpellCategoryThresholds -- nouvel asset
- Blueprint class (parent Object) dans Content/Systems/Magic/Data/
- TMap<E_SpellCategory, int> CategoryThresholds -- keyed directement par enum, zero conversion fragile
- Valeurs editables dans Class Defaults sans ouvrir BP_MagicComponent
- Acces via GetClassDefaults dans IncrementSpellUsage

#### Tests valides PIE
- Buff : LevelUp en 5 lancers (seuil effectif niveau 0 = 50/9 ~ 5)
- LevelUpSpell -> AddTalentPoint : "New Talent Point" visible en PIE
- IsDeityAccessible : bloque CastSpell si deite non debloquee

#### Dettes resolues
- Stub BeginPlay Lumina : supprime -- deblocage desormais via UnlockDeity(DeityID) depuis trigger narratif

#### Dettes nouvelles
- UsageThreshold dans FSoM_SpellData : encore present, a supprimer (remplace par BP_SpellCategoryThresholds)

#### Etat final
C1-MagicUnlockSystem VALIDE PIE. Chaine usage->niveau->points operationnelle avec courbe SoM adaptee.

---

### 26/05/2026 -- Session design -- Lore, Corruption, Fontaine de Fee, quetes deite

#### Lore_ShadowOfMana.md -- MIS A JOUR
- Athanor = Salamandre : deux noms pour la meme deite selon localisation (corrige partout)
- Deites : 8 au total (Lumina, Luna, Ombre, Sylphide, Gnome, Salamandre/Athanor, Ondine, Dryade)
- Structure deblocage deite finalisee : 4 paliers sequentiels obligatoires
  - Palier 0 Rencontre narratif -> sorts de base
  - Palier 1 Quete speciale -> paliers arbre 1-2
  - Palier 2 Donjon deite + rituel -> paliers arbre 3-4
  - Palier 3 Boss lore -> ultime
- Communion via rituel / priere propre a chaque deite, defini au cas par cas
- Fee liee au heros ajoutee : fee affaiblie, besoin des Fontaines de Fee pour se restaurer
- Fontaine de Fee : equivalent feu de camp DS, integre au lore via la fee
  - Repos -> fee restauree + Corruption purgee + stats restaurees + mobs respawn
  - Tension DS : se reposer coute (mobs respawn) vs ne pas se reposer (Corruption monte)
- Corruption Magique detaillee :
  - Usage magie -> accumulation Corruption, effets negatifs progressifs
  - Twist Representant d'Ombre : bonus degats a haut niveau de Corruption
  - Contreparties : soins indisponibles, certaines interactions PNJ bloquees
- Sessions design a planifier listees : Fee, Deites, SaveDesign, Economie

#### Magic_Progression.md -- MIS A JOUR
- Structure 3 paliers quetes deite finalisee (tableau palier 0-3)
- Section Corruption Magique ajoutee avec twist Representant d'Ombre
- Points ouverts mis a jour : seuils Corruption, cas Ondine

#### Etat final
Lore enrichi, mecanique Corruption posee, Fontaine de Fee integree narrativement.

---

### 26/05/2026 -- Session design -- Magic_Progression DESIGN

#### Magic_Progression.md -- DESIGN
- Nouveau fichier cree : Docs/Architecture/Magic_Progression.md
- Seuils progression differencies par role de sort
- Inspiration Secret of Mana : formule 9 - niveau actuel % par lancer
- Systeme de rattrapage tardif : objet/monnaie dedie

#### Etat final
Design progression magique pose dans Magic_Progression.md. Prochain jalon technique : C1-MagicUnlockSystem.

---

### 25/05/2026 -- Data layer deites + sortie mode dummy magie -- VALIDE PIE

#### Nouveaux assets data layer
- E_SpellTier, E_NodeType, FSoM_TalentNode, FSoM_DeityData, FSoM_SpellData etendu
- DT_Deities : row Lumina complete
- DT_TalentNodes : cree vide

#### BP_MagicComponent -- UnlockDeity refactore
- GetDataTableRow(DT_Deities) -> BaseSpells -> Set Members in FSoM_DeitySpells
- Bug resolu : logique Map_Contains inversee

#### UI_Radial_Main -- PopulateMagicSchools refactore
- GetDataTableRow(DT_Deities) -> DeityName + Icon

#### Etat final
Sortie du mode dummy magie. Data layer deites complet et data-driven.

---

### 25/05/2026 -- Session design + outils IA

#### C1-MagicProgressionDesign -- DESIGN VALIDE
- Boucle progression, structure arbre, sorts de base vs arbre

#### Etat final
C1-MagicProgressionDesign VALIDE.

---

### 23/05/2026 -- C1-InputsUI COMPLET -- VALIDE PIE

#### IMC crees et swap cable

#### Etat final
C1-InputsUI COMPLET VALIDE PIE.

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
