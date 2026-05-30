# Journal des Modifications -- Shadow of Mana

## Objectif
Suivi precis de toutes les evolutions majeures du projet.

## Entrees

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

#### Decheance Mana -- impact monde et exception heros
- Decheance Mana = impact visuel global (zones assombries, faune/flore corrompues/mutees)
- Humanoïdes normaux non impactes physiquement
- Heros = seule exception : subit la Corruption de la Mana (lien Ombre, a reveiller progressivement)
- Indices visuels subtils de Corruption sur le heros
- Pretresse (Lumina) et Suivante (Luna) percoivent ces signes (sensibilite Mana de leurs deites)
- Garcon Loup et Colosse ne les percoivent pas (pas encore eveilles a leur deite)

#### Structure actes -- enrichissement
- Acte 1 : mise en place monde brise, equipe, mystere heros/Ombre -- theme principal
- Acte 2 : retour Hub (non reconstruit a l'arrivee), restauration zone par zone, liberation deite = changement esthetique zone + PNJs reviennent au Hub + reconstruction progressive
- Boss A2 = General de l'Empire : choix moral + revelation soeur encore en vie (fragment)
- Acte 3 : recherche soeur + verite Grande Guerre + Epee Mana restauree + Demon Mana
- Acte 4 : Demon Primordial + Flammy debloque + resolution toutes lignes narratives
- Question ouverte : presence General avant boss A2 (Option A = present dans zones, Option B = boss surprise) -- en maturation

#### Ville Hub -- reconstruction progressive
- Non reconstruite a l'arrivee du groupe (debut A2) -- zone encore instable
- Se reconstruit step by step a chaque zone liberee
- PNJs rencontres en route reviennent et participent activement
- Forge debloquee avec Salamandre, services supplementaires avec chaque liberation
- Reference narrative : Wendel (Seiken 2/3) + Tsaata (Vision of Mana) -- lien Lumina + centralite monde

#### Armes Mana -- systeme complet
- Armes amenees sur terre par la Deesse Mana (pas liees a une deite specifique)
- Trouvees deteriorees dans le monde, principalement en Acte 1
- Types : Epee, Greatsword, Axe, Bow, Lance... (liste a completer)
- Restauration par etapes via Forgeron Nain : jalon narratif + materiaux (drop ennemis)
- Materiaux = condition suffisante qui empeche de tout maxer au deblocage narratif
- Nombre d'etapes calibre selon longueur totale du jeu (a definir)
- Forgeron actif et utile tout au long du jeu

#### Epee Mana -- parcours narratif
- Pretresse transporte l'Epee brisee depuis le debut
- Forgeron : premiere reparation (A1) = echec partiel, epee fonctionnelle mais incomplète
- Heros l'utilise, elle se brise -> signal fort : reconnu par l'epee
- Evolution par etapes jusqu'a etat final (type "Excalibur") en A3
- Epee Mana completement restauree = condition pour affronter Demon Mana

#### Divers
- Flammy : debloque fin A3 / debut A4, acces lieux inaccessibles, histoire propre a developper (basse priorite)
- Conflit Loup/DragonFolk : ancien (anterieur au cataclysme), amplifie par la Decheance Mana
- Mort Oracle : lie soeur + Empire, initie A4, circonstances a definir

#### Etat final
Session lore productive. Structure des 4 actes clarifiee et documentee. Systeme Armes Mana pose. Hub reconstruction defini. Plusieurs questions en maturation (General, mort Oracle, nom Hub, noms personnages).

---

### 29/05/2026 -- C1-WeaponArchitecture -- CLOTURE

#### Radial -- rotation a l'ouverture -- VALIDE PIE (partiel)
- Bug rotation corrige : PopulateWeaponSlots positionne maintenant la roue sur l'arme equipee (CurrentWeaponID) a chaque ouverture
- Fix : TargetRotation = -(EquippedIndex * AnglePerSlot) calcule depuis Array_Find(CurrentWeaponID) dans GetWeapons()
- Fix : SET SelectedIndex branche sur Array Index du ForEach SlotDataList (etait hardcode a 0)
- Fix : pin A du Equal(Integer) dans ForEach SlotWidgets branche sur Array Index (etait non connecte)
- Bug curseur position initiale : toujours sur slot 0 independamment de l'arme equipee
- Cause : systeme Radial heterogene (melange ancienne base + factorisations recentes) -- audit UnrealClaude realise
- Decision : dette reportee vers C?-RadialRefacto (refonte complete du systeme Radial a planifier)

#### Dettes resolues cette session
- HC.DiscoveredWeapons supprimee de HC : FAIT
- InitComboTree pin WeaponID inutilise nettoye : FAIT
- HandleAttack ErrorType=1 : VERIFIE / RESOLU

#### Dettes restantes -> reportees
- Radial curseur position initiale a l'ouverture -> C?-RadialRefacto
- Jauges HUD Stamina/Mana/Essence/Corruption -> C1-HUDCore

#### Etat final
C1-WeaponArchitecture clos. Rotation Radial fonctionnelle. Curseur position initiale reporte en dette RadialRefacto. Prochain jalon : C1-SwordMoveset ou C1-HUDCore.

---

### 29/05/2026 -- C1-WeaponArchitecture -- Refacto EquipWeapon + BP_InventoryComponent -- VALIDE PIE

#### BP_InventoryComponent -- VALIDE PIE
- Cree en Actor Component (Content/Systems/Inventory/)
- Variables : DiscoveredWeapons (Array<Name>)
- Fonctions : AddWeapon(WeaponID : Name) -> Array_AddUnique, GetWeapons() -> return DiscoveredWeapons
- Ajoute sur BP_SoM_HeroCharacter comme composant InventoryComponent
- Valeurs par defaut (Sword_01, 2HSword_01) renseignees dans Details panel de l'instance HC

#### ComboManager.EquipWeapon -- VALIDE PIE
- Nouvelle fonction EquipWeapon(WeaponID, WeaponLevel) sur BP_ComboManagerComponent
- Flux : SET CurrentWeaponID -> SET CurrentWeaponLevel -> SET CurrentStepID="Start" -> SET CanAttack=true -> GetDataTableRow(DT_Weapons, WeaponID) -> InitComboTree(WeaponData)
- HC.EquipWeapon delegue vers ComboManager.EquipWeapon au lieu d'appeler InitComboTree directement
- Bug resolu : InitComboTree avait pin WeaponID orphelin (supprime de la signature) -> Refresh Node + rebranching

#### InitComboTree -- allege -- VALIDE PIE
- Supprime : SET CurrentWeaponID, SET CurrentWeaponLevel, SET CurrentStepID, SET NextStepID, SET CanAttack
- Conserve : Map_Clear(ComboStepMap) -> GetDataTableRowNames(DT_Combo) -> ForEach -> GetDataTableRow -> Branch -> Map_Add
- Signature simplifiee : WeaponData (FWeaponData) uniquement (WeaponID supprime de la signature)
- Separation propre : InitComboTree = responsabilite unique (charger ComboStepMap)

#### HC.EquipWeapon -- mis a jour -- VALIDE PIE
- Array_AddUnique(HC.DiscoveredWeapons) remplace par InventoryComponent.AddWeapon(RowName)
- Appel InitComboTree remplace par ComboManager.EquipWeapon(WeaponID, WeaponLevel)
- HC.ChoosenWeapon supprime (plus reference nulle part)

#### PopulateWeaponSlots -- mis a jour -- VALIDE PIE
- Lecture HC.DiscoveredWeapons remplacee par InventoryComponent.GetWeapons()
- Cast HC -> GET InventoryComponent -> GetWeapons() -> ForEach

#### Etat final
Refacto EquipWeapon valide PIE. ComboManager = source de verite arme. InventoryComponent cree et branche. Switch arme + combos fonctionnels. Radial peuple correctement depuis InventoryComponent.

---

### 29/05/2026 -- Session design -- Archi WeaponArchitecture + Inventaire + TenaciteEtat -- DESIGN VALIDE

#### Etat final
4 decisions actees. C1-WeaponArchitecture peut demarrer sans ambiguite d'architecture.
Spec complete dans Docs/Architecture/Decisions.md.

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
- Derniere mise a jour : 30/05/2026
