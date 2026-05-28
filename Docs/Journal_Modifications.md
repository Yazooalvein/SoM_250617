# Journal des Modifications -- Shadow of Mana

## Objectif
Suivi precis de toutes les evolutions majeures du projet.

## Entrees

### 28/05/2026 -- Session design -- Effets de statut & Corruption Magique -- DESIGN VALIDE

#### Effets de statut par deite

Table complete validee -- 8 deites, 8 effets signatures :
- Lumina : Eblouissement (reduit precision ennemie + revele invisibles)
- Luna : Sommeil (bloque actions, reveil x1.5 degats si touche)
- Ombre : Malediction (-75% soins recus)
- Sylphide : Desequilibre (-Defense + bloque sprint)
- Gnome : Alourdi (-Vitesse et -VitesseAttaque severe)
- Salamandre : Brulure (drain PV + -Resistance Feu)
- Ondine : Gele (ralentissement severe, Fige si deja Ralenti)
- Dryade : Empoisonne (drain PV lent, 3 stacks max)

Interactions cles : Sommeil+attaque=x1.5, Desequilibre+Gele=Fige, Malediction+Drain=combo punitif

Implementation : BP_StatusEffectComponent sur HC et Enemy_Base -- a creer en C1-SwordMoveset

#### Corruption Magique -- systeme risque/recompense

- Generation : Attaque+3, Debuff+2, Buff+1, Heal+0
- Modificateurs par deite : Ombre x0.5, Lumina x1.5, Salamandre x1.25, Dryade x0.75
- Seuils negatifs : 25 (aura), 50 (-20% resistances), 75 (faiblesse element + drain stamina), 100 (statut aleatoire /30s)
- Bonus Essence ennemis par seuil : x1.0 / x1.15 / x1.35 / x1.60 / x1.60 (plafond a 100)
- Sorts Heal : 0 Corruption mais reduisent legerement le bonus Essence actif
- Purge Fontaine : Corruption=0. Si >=75 : fee epuisee (pas de montee deite cette visite). Si 100 : fee gronde
- Tension centrale : purger souvent = securite, rester haut = farming rapide mais risque

#### Points encore ouverts
- Duree effets de statut + TenaciteEtat base heros -> C1-SwordMoveset
- Element faiblesse a 75 : aleatoire ou fixe par run -> a trancher
- Aura visuelle Corruption >= 25 -> ART ou C4
- Effet narratif Corruption=100 (dialogue fee ?) -> Session Lore Fee

#### Etat final
DESIGN-StatusEffects + DESIGN-Corruption VALIDES. Spec dans Docs/Architecture/Combat_StatusEffects.md.

---

### 28/05/2026 -- Session design -- Stats & Progression personnage -- DESIGN VALIDE

#### Decisions actees

**Stats heros (7) :** Vitalite, Attaque, Defense, Magie, Resistance, Endurance, Vitesse
- Toutes via SetStatValue / OnStatChanged (architecture existante)
- Nouvelles cles BP_AttributeSet_Base : Magie, Resistance, EnduranceMax, EnduranceCurrent, Vitesse, Level, EssenceMana, EssenceManaDropped, ChanceCritique

**Progression hybride :**
- Niveaux globaux 1-10 (acte 1) : stats auto + 2 points libres a distribuer
- Courbe exponentielle XP : 100 * 1.5^(N-1) par niveau
- Progression par usage armes/magie : inchangee (systeme existant)

**Ressource universelle -- Essence de Mana :**
- Remplace XP : sert a monter de niveau global ET a investir dans les deites
- Perdue a la mort, recuperable en retournant sur le lieu de la mort (DS-like)
- Double mort = Essence definitivement perdue

**Formules degats :**
- Physique : Max(1, (Attaque * CoeffArme * CoeffCritique) - (Defense * 0.5))
- Magique : Max(1, (Magie * CoeffSort * CoeffCritique) - (Resistance * 0.5))
- Elementaire : * (1 - ResistanceElementaire[Element])
- 8 elements correspondant aux 8 deites

**Critique :** 5% de base, x1.5, heros ET ennemis
**Stamina :** -10 att legere, -20 att lourde, -25 esquive, -5/s sprint -- recuperation auto 1s
**Stats ennemis (systeme simplifie dedie) :** PV, Attaque, Defense, Resistance, Vitesse, VitesseAttaque, TenaciteEtat + ResistanceElementaire TMap
**VitesseAttaque armes :** multiplicateur PlayRate montage dans FWeaponData

#### Etat final
DESIGN-StatsProgression VALIDE. Spec complete dans Docs/Architecture/Stats_Progression.md.

---

### 28/05/2026 -- Session planning -- Refacto armes/combo note

#### Etat final
C1-WeaponArchitecture elargi en "C1-WeaponArchitecture + Refacto". Note enregistree.

---

### 27/05/2026 -- C1-CleanupDettes COMPLET

#### Suppressions effectuees
- LockOnSwitchCooldown dans BP_SoM_PlayerController : supprime
- UsageThreshold dans FSoM_SpellData : supprime, remplace par BP_SpellCategoryThresholds
- Fix Up Redirectors execute, compilation OK

#### Etat final
C1-CleanupDettes COMPLET.

---

### 27/05/2026 -- RadialUnlock + blocages narratifs radial -- VALIDE PIE

#### Etat final
Systeme de deblocage narratif radial operationnel (bRadialUnlocked + BP_Debug_UnlockDeity).

---

### 27/05/2026 -- C1-MagicUnlockSystem -- VALIDE PIE

#### Etat final
C1-MagicUnlockSystem VALIDE PIE. Chaine usage->niveau->points operationnelle.

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
Pour le lore et la narrative : voir Docs/Lore_ShadowOfMana.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 28/05/2026
