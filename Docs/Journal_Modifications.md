# Journal des Modifications -- Shadow of Mana

## Objectif
Suivi precis de toutes les evolutions majeures du projet.

## Entrees

### 28/05/2026 -- Session design -- Economie, Drops, Consommables, Mana -- DESIGN VALIDE

#### Double monnaie
- Essence de Mana : progression (niveaux, deites, forge armes) -- perdue a la mort, recuperable DS-like
- Pieces d'Or (PO) : economie du monde (marchands, objets, armures) -- jamais perdues

#### Drops ennemis
- Toujours : Essence + PO (quantites variables par type)
- Aleatoire : objets consommables (15-25%), materiaux de forge (8-18%), coffres Seiken
- Boss : drop garanti x1 objet + x1 materiau

#### Consommables style Secret of Mana
- Bonbon/Noix/Miel (PV), Plante (Mana), Herbe (statut), Essence Purifiee (Corruption -15), Repas (+% drop temp)
- Stock max 9 unites par type, rechargeable Fontaine depuis stock mondial
- Utilisables en combat, via quickslot ou radial dedie (C7-HUDPolish)
- Taux de drop augmente uniquement via Repas -- pas de stat permanente

#### Materiaux de forge
- 3 tiers : Graine de Mana (commun), Cristal de Mana (rare), Essence Cristallisee (special)
- Non lies aux elements -- universels
- Forge narrative style Seiken : upgrade N+1 debloque par jalon narratif + materiaux requis

#### Equipement
- 3 slots : Casque, Armure, Accessoire
- Stats : Defense + Resistance uniquement
- Achat PO ou drop coffres/boss

#### Cout sorts Mana
- Formule : Base + (NiveauSort * Multiplicateur)
- ManaMax separee de Magie, monte avec Level global (+8/niveau, base 60)
- Cles : "ManaMax" / "ManaCurrent"
- Pas de regen Mana auto

#### Sauvegarde & respawn
- Sauvegarde tout sauf Essence non depensee
- Respawn : ennemis normaux oui, boss jamais
- Double mort = Essence definitivement perdue

#### Corruption Phase 1/2
- Phase 1 (debut jeu) : plafond 50, effets limites
- Phase 2 (apres revelation Hero/Ombre) : plafond 100, faiblesse = deite la plus utilisee au franchissement 75, effet statut = meme deite a 100
- Narrativement : Ombre leve involontairement le voile protecteur suite a la decheance de la Mana

#### Points encore ouverts
- Duree buff Repas -> C5-Equipment
- Prerequis niveau equipement -> C5-Equipment
- Quand exactement debloquer Corruption Phase 2 -> Session Lore Ombre
- Radial dedie objets vs integration radial existant -> C7-HUDPolish
- Prix PO + taux drops calibres -> Playtest acte 1

#### Etat final
DESIGN-Economy VALIDE. Spec dans Docs/Architecture/Economy_Drops.md.

---

### 28/05/2026 -- Session design -- Effets de statut & Corruption Magique -- DESIGN VALIDE

#### Etat final
8 effets par deite valides, Corruption systeme risque/recompense valide. Spec dans Combat_StatusEffects.md.

---

### 28/05/2026 -- Session design -- Stats & Progression personnage -- DESIGN VALIDE

#### Etat final
7 stats heros, progression hybride, Essence de Mana, formules degats. Spec dans Stats_Progression.md.

---

### 28/05/2026 -- Session planning -- Refacto armes/combo note

#### Etat final
C1-WeaponArchitecture elargi en "C1-WeaponArchitecture + Refacto". Note enregistree.

---

### 27/05/2026 -- C1-CleanupDettes COMPLET

#### Etat final
LockOnSwitchCooldown PC supprime, UsageThreshold FSoM_SpellData supprime. Compilation OK.

---

### 27/05/2026 -- RadialUnlock + blocages narratifs radial -- VALIDE PIE

#### Etat final
bRadialUnlocked + BP_Debug_UnlockDeity operationnels.

---

### 27/05/2026 -- C1-MagicUnlockSystem -- VALIDE PIE

#### Etat final
Chaine usage->niveau->points operationnelle avec courbe SoM adaptee.

---

### 26/05/2026 -- Session design -- Lore, Corruption, Fontaine de Fee

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
Pour les stats et progression : voir Docs/Architecture/Stats_Progression.md
Pour les effets de statut et corruption : voir Docs/Architecture/Combat_StatusEffects.md
Pour l'economie et les drops : voir Docs/Architecture/Economy_Drops.md
Pour le lore et la narrative : voir Docs/Lore_ShadowOfMana.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 28/05/2026
