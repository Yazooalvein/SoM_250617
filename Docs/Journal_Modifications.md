# Journal des Modifications -- Shadow of Mana

## Objectif
Suivi precis de toutes les evolutions majeures du projet.

## Entrees

### 31/05/2026 -- C1-HUDCore -- VALIDE

#### BP_AttributeSet_Base -- VALIDE
- Ajout variables : EssenceMana (Float), Corruption (Float), bCorruptionUnlocked (Bool, default=false)
- SetStatValue case Corruption : Branch(bCorruptionUnlocked) -> FClamp(0,100) ou FClamp(0,50) -> SET Corruption -> OnStatChanged
- EssenceMana pas dans SetStatValue (pas de clamp necessaire, SET direct)

#### UI_HUD_Main BP -- VALIDE
- Ajout variables widget : EssenceValue (Float), CorruptionPercent (Float)
- Switch HUD_OnStatChanged etendu a 8 cases : + EssenceMana (SET EssenceValue direct) + Corruption (NewValue/100 -> SET CorruptionPercent)
- InitHUD mis a jour : GET AttributeSetRef.EssenceMana -> SET EssenceValue + GET Corruption/100 -> SET CorruptionPercent
- Binding Get_CorruptionBar_Percent cree : retourne CorruptionPercent (meme pattern Stamina/Mana)
- Fonction UpdateEssenceText : EssenceValue -> Conv_DoubleToInt64 -> Conv_Int64ToString -> Conv_StringToText -> SetText(TextBlock_Essence)
- Choix Int64 : gere les grandes valeurs souls-like sans overflow

#### UI_HUD_Main Designer -- VALIDE
- TextBlock_Essence ajoute sous HUD_Anchor > SizeBox_Essence (pres de l'arme -- hors VertBox, choix volontaire)
- CorruptionBar (ProgressBar) ajoutee dans HUD_Main_VertBox en bas
- Architecture : barres HP/ST/MP/Corruption dans VertBox, compteur Essence separe pres arme = meilleure UX

#### Decisions architecture
- bCorruptionUnlocked dans AttributeSet = variable simple (future logique dans BP_CorruptionComponent)
- BP_CorruptionComponent : jalon dedie C2-CorruptionSystem (tracking deites, purge, faiblesse 75, TenaciteEtat)
- C3-EssenceMana : jalon dedie pour le systeme complet Essence (collecte, perte mort, recuperation DS-like)
- Det designer mineure : TextBlock_Essence et CorruptionBar hors structure Overlay/SizeBox standard -> acceptable pour l'instant

#### Dettes restantes
- Dette designer legere : restructurer Essence/Corruption dans Overlay/SizeBox si besoin (C7-HUDPolish)
- UpdateStatText ne couvre pas encore Essence (TextBlock deja connecte via UpdateEssenceText, non via UpdateStatText)

#### Etat final
C1-HUDCore VALIDE. Architecture event-driven HP/ST/MP/Essence/Corruption operationnelle. Deux nouveaux jalons crees : C2-CorruptionSystem et C3-EssenceMana.

---

### 30/05/2026 -- Session design -- Weapons_Progression -- DESIGN VALIDE

#### DESIGN-WeaponProgression -- DESIGN VALIDE
- Systeme de progression armes defini : usage en combat (nombre d'attaques), formule identique magie (9 - niveau actuel %)
- Structure progression : Niveau 1->2 libre, Niveau 2->3+ conditionne par forge (XP ne s'accumule pas avant)
- Materiaux forge : Drop commun x N (Minerai/Bois/etc.) + Drop rare x 1 (Essence/Graine/Esprit Mana -- Boss ou Narratif)
- Arbre par arme : tous les X niveaux (a calibrer) -- choix entre Branche Combo ou Branche Stat
- Accessibilite : ~50% des armes maxables naturellement, reste via quetes annexes haut level
- Quetes annexes haut level : donnent les materiaux rares manquants (pas la forge directe -- joueur garde le choix)
- Parallele magie : meme philosophie usage + condition externe, divergence sur la nature de la condition (narratif vs craft)
- Pas de systeme de rattrapage pour les armes (contrairement a la magie)
- Nouveau fichier : Docs/Architecture/Weapons_Progression.md

#### Recadrage C1-SwordMoveset
- Jalon C1-SwordMoveset recadre : TenaciteEtat + BP_StatusEffectComponent n'ont pas de lien logique avec le moveset epee
- Ces sujets seront traites dans leur contexte naturel (magie, ennemis)
- Moveset epee actuel (Light1/Light2/Heavy1) = fonctionnel, refactor combo potentiel a prevoir ulterieurement

#### Etat final
Session design productive. Weapons_Progression.md cree et pousse. Index et docs mis a jour.

---

### 29/05/2026 -- Session design Lore -- Structure narrative + Armes Mana + Hub -- DESIGN VALIDE

#### Etat final
Session lore productive. Structure des 4 actes clarifiee et documentee. Systeme Armes Mana pose. Hub reconstruction defini.

---

### 29/05/2026 -- C1-WeaponArchitecture -- CLOTURE

#### Etat final
C1-WeaponArchitecture clos. Rotation Radial fonctionnelle. Curseur position initiale reporte en dette RadialRefacto.

---

### 29/05/2026 -- C1-WeaponArchitecture -- Refacto EquipWeapon + BP_InventoryComponent -- VALIDE PIE

#### Etat final
Refacto EquipWeapon valide PIE. ComboManager = source de verite arme. InventoryComponent cree et branche.

---

### 29/05/2026 -- Session design -- Archi WeaponArchitecture + Inventaire + TenaciteEtat -- DESIGN VALIDE

#### Etat final
4 decisions actees. C1-WeaponArchitecture peut demarrer sans ambiguite d'architecture.

---

### 28/05/2026 -- C1-WeaponArchitecture -- Etapes 5-6-7 + Radial curseur -- PARTIEL

#### Etat final
Etapes 5 et 6 completes. Etape 7 partielle -- curseur OK premiere ouverture, bug reouverture ouvert.

---

### 28/05/2026 -- Session design -- Lore, Cast, Fee, Ombre, Deites -- DESIGN VALIDE

#### Etat final
DESIGN-Lore VALIDE (provisoire). Spec dans Docs/Lore_ShadowOfMana.md.

---

### 28/05/2026 -- Session design -- Economie, Drops, Consommables, Mana -- DESIGN VALIDE

#### Etat final
Double monnaie, drops Seiken, Mana, equipement. Spec dans Economy_Drops.md.

---

### 28/05/2026 -- Session design -- Effets de statut & Corruption Magique -- DESIGN VALIDE

#### Etat final
8 effets par deite, Corruption Phase 1/2, bonus Essence. Spec dans Combat_StatusEffects.md.

---

### 28/05/2026 -- Session design -- Stats & Progression personnage -- DESIGN VALIDE

#### Etat final
7 stats heros, progression hybride, Essence de Mana, formules degats. Spec dans Stats_Progression.md.

---

### 28/05/2026 -- Session planning -- Refacto armes/combo note

---

### 27/05/2026 -- C1-CleanupDettes COMPLET

---

### 27/05/2026 -- RadialUnlock VALIDE PIE

---

### 27/05/2026 -- C1-MagicUnlockSystem VALIDE PIE

---

### 26/05/2026 -- Session design -- Lore, Corruption, Fontaine de Fee

---

### 26/05/2026 -- Session design -- Magic_Progression DESIGN

---

### 25/05/2026 -- Data layer deites + sortie mode dummy magie -- VALIDE PIE

---

### 25/05/2026 -- Session design + outils IA

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

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 31/05/2026
