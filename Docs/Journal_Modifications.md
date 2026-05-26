# Journal des Modifications -- Shadow of Mana

## Objectif
Suivi precis de toutes les evolutions majeures du projet.

## Entrees

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

#### Points ouverts documentes
- Fee : nom, personnalite, histoire, lien Ombre/Corruption -> session Lore Fee
- Deites : ordre deblocage, structure rituel par deite -> session Lore Deites
- Fontaine de Fee : frequence, montee Corruption hors repos, HUD fee -> session SaveDesign
- Seuils Corruption (legere/moderee/severe), reversibilite, reactions ennemis -> session dediee
- Cas particulier Ondine (statut ambigu) -> session Lore

#### Etat final
Lore enrichi, mecanique Corruption posee, Fontaine de Fee integree narrativement.
Sessions Lore et SaveDesign a planifier pour debloquer les points ouverts restants.

---

### 26/05/2026 -- Session design -- Magic_Progression DESIGN

#### Magic_Progression.md -- DESIGN
- Nouveau fichier cree : Docs/Architecture/Magic_Progression.md
- Seuils progression differencies par role de sort : Attack (bas) < Heal (moyen) < Buff (moyen-haut) < Debuff (haut)
- Rationale : refleter la frequence d'usage naturelle en combat, eviter le grind artificiel
- Inspiration Secret of Mana : formule 9 - niveau actuel % par lancer, adaptee avec seuils differencies
- Systeme de rattrapage tardif : objet/monnaie dedie pour injecter XP sur sorts sous-evolues en fin de jeu
- Cap narratif : rencontrer une deite = sorts de base, completer quete de deite = paliers arbre debloques

#### Etat final
Design progression magique pose dans Magic_Progression.md. Prochain jalon technique : C1-MagicUnlockSystem.

---

### 25/05/2026 -- Data layer deites + sortie mode dummy magie -- VALIDE PIE

#### Nouveaux assets data layer
- E_SpellTier (enum) : Base / TreeActive / TreeEvolution / Ultime
- E_NodeType (enum) : Active / Passive / Ultime
- FSoM_TalentNode (struct) : NodeID, DeityID, NodeType, SpellID, PassiveStat, PassiveValue, PointCost, Prerequisites
- FSoM_DeityData (struct) : DeityID, DeityName, Icon, UnlockOrder, BaseSpells
- FSoM_SpellData : SpellTier (E_SpellTier) + ReplacesSpellID (Name) ajoutes
- DT_Deities : row Lumina (UnlockOrder=1, BaseSpells=[Lumina_Attack, Lumina_Heal, Lumina_Buff, Lumina_Debuff], Icon placeholder)
- DT_TalentNodes : cree vide, pret pour C1-MagicTreeModule
- Convention BaseSpells : ordre fixe [0=Attack, 1=Heal, 2=Buff, 3=Debuff] pour toutes les deites

#### BP_MagicComponent -- UnlockDeity refactore
- Avant : TempSpellsIDs hardcode en default value -> mode dummy
- Apres : GetDataTableRow(DT_Deities, DeityName) -> BaseSpells -> Set Members in FSoM_DeitySpells
- TempSpellsIDs supprime
- Bug resolu : logique Map_Contains inversee (TRUE=deja present->return, FALSE=absent->debloquer)

#### UI_Radial_Main -- PopulateMagicSchools refactore
- Avant : Conv_NameToText(Map Key) -> DisplayName, Icon null
- Apres : GetDataTableRow(DT_Deities, Map Key) -> DeityData.DeityName + DeityData.Icon -> MakeStruct
- Icone deite reelle affichee dans le radial N1

#### Tests valides PIE
- Radial N1 (Deity) : icone Lumina affichee, DeityName = "Lumina"
- Radial N2 (Spell) : 4 sorts Lumina accessibles, CastSpell fonctionnel

#### Dettes
- Stub BeginPlay Lumina : toujours present, a retirer quand C1-MagicUnlockSystem opere en jeu

#### Etat final
Sortie du mode dummy magie. Data layer deites complet et data-driven. Prochain jalon : C1-MagicUnlockSystem.

---

### 25/05/2026 -- Session design + outils IA

#### C1-MagicProgressionDesign -- DESIGN VALIDE
- Boucle de progression arretee : usage sorts -> montee niveau -> points talent -> arbre de talent
- Structure par deite : 2-4 sorts de base immediats, arbre = 3-4 actifs + 2-3 passifs + 1 ulti
- Points insuffisants pour completer l'arbre -> choix force -> builds differents
- Evolution d'un sort de base : remplace le sort (pas de coexistence)
- Sorts supplementaires d'arbre : s'ajoutent au pool radial/quickslots
- Deites : aucun cout de switch, pas d'equipement, apparition immediate au deblocage

#### Etat final
C1-MagicProgressionDesign VALIDE. Prochain jalon : C1-MagicUnlockSystem.

---

### 23/05/2026 -- C1-InputsUI COMPLET -- VALIDE PIE

#### IMC crees
- IMC_Gameplay (ex IMC_Prototype renomme) : charge au ReceivePossessed dans BP_SoM_HeroCharacter
- IMC_Radial : 4 IA navigation radial
- IMC_Menu, IMC_Dialogue, IMC_Cutscene : stubs vides

#### Swap IMC cable dans BP_SoM_PlayerController
- OpenRadial : RemoveMappingContext(IMC_Gameplay) -> AddMappingContext(IMC_Radial, Priority=1)
- CloseRadial : RemoveMappingContext(IMC_Radial) -> AddMappingContext(IMC_Gameplay, Priority=0)

#### Fix rotation radial
- Bug : rotations multiples et sens incorrect
- Fix 1 : trigger Pressed avec threshold 0.5 sur IA_UI_Radial_Rotate
- Fix 2 : Modifier Negate X sur binding direction gauche

#### Etat final
C1-InputsUI COMPLET VALIDE PIE.

---

### 23/05/2026 -- Session design -- Architecture IMC complete
- 5 IMC decides (Gameplay/Radial/Menu/Dialogue/Cutscene)
- IMC_Dialogue = SEUL cumulatif

---

### 21/05/2026 -- Session design & documentation
- C1-HitFlashEnemies ABANDONNE, C1-CleanupDettes 3/4, C1-InputsUI PRIORITAIRE

---

### 19/05/2026 -- C1-HitFlashEnemies -- ARCHITECTURE COMPLETE
- Architecture DMI faite, blocage M_Mannequin identifie

---

### 18/05/2026 -- C1-HitFeel PARTIEL -- VALIDE PIE
- Knockback + screen shake valides, hitstop reporte, vibration gamepad manque

---

### 18/05/2026 -- C1-CollisionFix COMPLET -- VALIDE PIE
- CapsuleComponent Pawn=Block, weapon collision audit

---

### 18/05/2026 -- J-ComboFix COMPLET -- VALIDE PIE
- ChoosenWeapon, InitComboTree, HandleAttack sans parametre, LevelMin=0

---

### 18/05/2026 -- J-TestBed COMPLET -- VALIDE PIE
- Lvl_TestBed BSP, BP_Enemy_TestBed, SFX placeholder

---

### 18/05/2026 -- J-LockMove COMPLET -- VALIDE PIE
- Move() en lock-on via CameraRotation, Rotation Rate -1, LastAxisX/Y

---

### 17/05/2026 -- J-Camera COMPLET -- VALIDE PIE
- SpringArm regle, IA_Look dans PC, UpdateLockOnRotation V2, Screen Shake valide

---

### 15/05/2026 -- J-Renommage COMPLET
- Convention nommage unifiee, Fix Up Redirectors, VALIDE PIE

---

### 15/05/2026 -- J-lock COMPLET -- VALIDE PIE
- Fix IsLockOnActive, fix dispatcher espace, fix bind PC, UpdateLockOnUIIndicator
- ABP_Manny_Platforming Strafe VALIDE PIE

---

### 14/05/2026 -- Session design -- Roadmap globale refondee
- ~50 jalons, 8 couches, projet complet de A a Z

---

### 14/05/2026 -- J-Nettoyage COMPLET
- Suppression assets obsoletes, reorganisation dossier Enemies

---

### 14/05/2026 -- Session creative J-ART ; Hero PLACEHOLDER COMPLET
- Workflow Dessin -> Leonardo.ai -> Gemini -> Meshy 5 -> AccuRIG -> UE5.7 valide

---

### 14/05/2026 -- Session creative J-MUS (exploration workflow)
- Workflow Fredonnement -> Suno -> Export MP3 -> UE5 etabli

---

### 12-13/05/2026 -- Jalon J-13 COMPLET -- Radial Menu + Quickslot VALIDE PIE

---

### 12/05/2026 -- Jalon J-15 -- UI_HUD_Main FINALISE

---

### 12/05/2026 -- Jalons J-10 a J-14 -- POC Systeme Magie VALIDE PIE

---

### 11/05/2026 -- Session design
- Lore, Roadmap, Architecture magie

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
- Derniere mise a jour : 26/05/2026
