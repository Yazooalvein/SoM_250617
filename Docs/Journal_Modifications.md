# Journal des Modifications -- Shadow of Mana

## Objectif
Suivi precis de toutes les evolutions majeures du projet.

## Entrees

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
- HC.EquipWeapon delgue vers ComboManager.EquipWeapon au lieu d'appeler InitComboTree directement
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

#### Dettes restantes
- HC.DiscoveredWeapons : variable encore presente sur HC (a supprimer proprement)
- InitComboTree : pin WeaponID encore dans la signature (inutilise, a nettoyer)
- DiscoveredWeapons par defaut : renseignees en Details panel instance HC (pas BeginPlay) -> dette SaveGame
- HandleAttack ErrorType=1 sur HC : toujours ouvert -> C1-WeaponArchitecture
- Bug reouverture Radial : toujours ouvert -> C1-WeaponArchitecture

#### Etat final
Refacto EquipWeapon valide PIE. ComboManager = source de verite arme. InventoryComponent cree et branche. Switch arme + combos fonctionnels. Radial peuple correctement depuis InventoryComponent.

---

### 29/05/2026 -- Session design -- Archi WeaponArchitecture + Inventaire + TenaciteEtat -- DESIGN VALIDE

#### Contexte
Session de design preparatoire avant C1-WeaponArchitecture. Objectif : trancher 4 points bloques
qui empechaient d'attaquer la refonte EquipWeapon proprement.

#### Decision 1 -- Source de verite arme courante : ComboManager
- HC.ChoosenWeapon supprime -- redondant avec ComboManager.CurrentWeaponID
- BP_ComboManagerComponent = source de verite unique (arme equipee + niveau arme)
- EquipWeapon migre sur ComboManager
- HC delegue, ne stocke pas -- coherent avec philosophie de factorisation du projet
- SaveGame lira ComboManager.CurrentWeaponID directement

#### Decision 2 -- DiscoveredWeapons -> BP_InventoryComponent
- DiscoveredWeapons sort de HC et migre vers un BP_InventoryComponent dedie (a creer)
- InventoryComponent accueillera : armes, consommables Seiken, materiaux craft, equipement (Casque/Armure/Accessoire)
- ComboManager ne connait que l'arme equipee, pas l'inventaire
- Radial interroge InventoryComponent pour peupler ses slots armes
- Separation propre, extensible vers C5-Equipment et C5-ForgeSystem

#### Decision 3 -- Switch arme en combo = reset combo (punition)
- EquipWeapon reinitialise l'etat combo immediatement
- Pas de fenetre de grace, pas de conservation de step cross-arme
- Pas de grisage UI Radial pendant combo
- Slow-mo Radial (Time Dilation 0.2) = seule concession au joueur
- Coherent avec identite Dark Souls du projet

#### Decision 4 -- TenaciteEtat heros
- Valeur de base : 25 (cle supplementaire BP_AttributeSet_Base, pas une 8eme stat visible)
- Modifiable par : equipement, buffs/debuffs, Corruption
- Corruption reduit la TenaciteEtat -> boucle de pression (plus corrompu = plus vulnerable aux effets de statut)
- Passe par SetStatValue comme toutes les stats
- Calibrage Corruption -> reduction TenaciteEtat : a definir en session Economie/Calibrage

#### Etat final
4 decisions actees. C1-WeaponArchitecture peut demarrer sans ambiguite d'architecture.
Spec complete dans Docs/Architecture/Decisions.md.

---

### 28/05/2026 -- C1-WeaponArchitecture -- Etapes 5-6-7 + Radial curseur -- PARTIEL

#### Etape 5 -- Suppression CanAttack sur HC -- VALIDE
- Guards input (IA_Attack_Light, IA_Attack_Heavy) lisent ComboManager.CanAttack directement
- Variables HC.CanAttack supprimees
- Source unique : BP_ComboManagerComponent.CanAttack

#### Etape 6 -- UpgradeWeaponLevel -- VALIDE
- Option A implementee : runtime only, sans SaveGame
- Flux : CurrentWeaponLevel +1 -> GetDataTableRow DT_Weapons -> InitComboTree(CurrentWeaponID, FWeaponData)
- Parametre NewLevel en entree existe mais non utilise (Option A)

#### Etape 7 -- Radial curseur position initiale -- PARTIEL
- Mecanique confirmee par audit : roue tourne, curseur fixe en haut (position 0)
- PopulateWeaponSlots : TargetRotation = -(EquippedIndex * AnglePerSlot), CurrentRotation = TargetRotation, SelectedIndex = 0
- AnglePerSlot recalcule localement (360 / Array_Length(SlotDataList)) -- pas de variable globale
- Guard ajoute : si CurrentWeaponID == None -> ne pas modifier les rotations
- Premiere ouverture avec arme equipee : OK
- Bug ouvert : a la reouverture apres changement d'arme, la roue ne se repositionne pas correctement
- Cause suspectee : CurrentWeaponID dans ComboManager non mis a jour apres ValidateSelectedWeapon -> EquipWeapon

#### Dettes identifiees cette session
- Refonte EquipWeapon (dette C1) : logique eparpillee HC / ComboManager / UI_Radial / PC -> unifier avant cloture C1-WeaponArchitecture
- HandleAttack ErrorType=1 sur HC : a verifier PIE
- SaveGame : BeginPlay charger arme -> EquipWeapon
- BP_Enemy_Base : stats manquantes + WeaponClass generique

#### Etat final
Etapes 5 et 6 completes. Etape 7 partielle -- curseur OK premiere ouverture, bug reouverture ouvert. Refonte EquipWeapon identifiee comme dette C1 critique.

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

#### Etat final
C1-WeaponArchitecture elargi. Note enregistree.

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

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 29/05/2026
