# Journal des Modifications -- Shadow of Mana

## Objectif
Suivi precis de toutes les evolutions majeures du projet.

## Entrees

### 31/05/2026 -- SYS-CorruptionSystem -- VALIDE PIE

#### BP_CorruptionComponent -- VALIDE PIE
- Cree dans Content/Systems/Corruption/
- Variables : DeityUsageMap (TMap<Name, int32>)
- Fonctions : InitCorruption, TrackDeityUsage(DeityName), GetWeakDeity() -> Name, PurgeCorruption(CostAmount)
- Ajoute sur BP_SoM_HeroCharacter via panneau Components

#### TrackDeityUsage -- logique
- Map_Find(DeityUsageMap, DeityName) -> bFound -> Branch
- TRUE (deja present) : Map_Add avec valeur + 1 (ecrase)
- FALSE (nouveau) : Map_Add avec valeur 1
- Apres Map_Add : GetOwner -> Cast to HC -> GET AttributeSetRef -> Corruption + 5.0 -> FClamp(0,100) -> SetStatValue("Corruption", value)
- Bug resolu : OwnerAttributeSet None apres premier sort -- cause : ordre BeginPlay non garanti entre composants -- fix : recup AttributeSetRef dynamiquement via GetOwner/Cast au moment de l'appel (pas de variable stockee)

#### PurgeCorruption -- logique
- Semantique : remet Corruption a 0 directement (purge totale), CostAmount reserve pour futur cout Essence
- SetStatValue("Corruption", 0.0) -> Map_Clear(DeityUsageMap)
- Bug resolu : PurgeCorruption(0.0) ne faisait rien (Corruption - 0 = Corruption) -- cause : mauvaise semantique initiale (soustraction) -- fix : remise a zero directe

#### GetWeakDeity -- logique
- Map_Keys(DeityUsageMap) -> ForEachLoop -> Map_Find(value) -> Branch(value > LocalMaxValue) -> SET LocalMaxValue + SET LocalWeakDeity
- Retourne la deite la plus utilisee depuis la derniere purge

#### Branchement BP_MagicComponent -- VALIDE PIE
- IncrementSpellUsage : apres Map_Add SpellUsageCounts -> GetOwner -> Cast to HC -> GetComponentByClass(BP_CorruptionComponent) -> Cast -> TrackDeityUsage(DeityID)
- DeityID provient du BreakStruct FSoM_SpellData

#### UI_HUD_Main -- Fix CorruptionBar -- VALIDE PIE
- CorruptionBar manquait de couleur Tint dans Fill Image -> ajoute (violet)
- Get_CorruptionBar_Percent pas reliee -> fonction marquee Pure + branchee sur Percent

#### BP_DebugFountain -- VALIDE PIE
- Actor debug dans Content/Debug/
- ActorBeginOverlap -> OtherActor == GetPlayerCharacter -> Cast to HC -> GetComponentByClass(BP_CorruptionComponent) -> PurgeCorruption(0.0)
- Test : marcher dessus remet Corruption a 0 + reset DeityUsageMap

#### Etat final
SYS-CorruptionSystem VALIDE PIE. Sorts Lumina montent la Corruption (+5/sort), barre HUD se met a jour, fontaine debug purge a 0. Tracking deites operationnel. Prochain jalon : SYS-EssenceMana.

---

### 31/05/2026 -- COMBAT-SwordMoveset -- CLOS VALIDE PIE

#### Audit combo Sword_01 -- VALIDE PIE
- DT_Combo_Sword : Start -> Light1 -> Light2 + Heavy1, montages AM_Light_Sword_1/2 et AM_Heavy_Sword_1 branches
- ComboManager : double lookup propre (CurrentStepID -> NextSteps -> AttackType), InitComboTree filtre par WeaponID ET LevelMin
- EquipWeapon : flux complet SET CurrentWeaponID/Level/StepID/CanAttack -> GetDataTableRow -> InitComboTree
- Chaine combo Light1 -> Light2 et Light1 -> Heavy1 validees PIE
- RotateTowardLockTarget presente dans ComboManager -- feeling lock-on a ameliorer ulterieurement (non bloquant)

#### BP_AttributeSet_Base -- TenaciteEtat -- VALIDE
- Ajout variable TenaciteEtat (Float, default 25.0, Instance Editable)
- SetStatValue case TenaciteEtat : FClamp(0, 100, Value) -> SET TenaciteEtat -> OnStatChanged
- Meme pattern que les autres stats -- Switch case 12 branche sur K2Node_VariableSet_13

#### Dettes restantes
- Lock-on feeling pendant attaques : RotateTowardLockTarget a affiner -> ANIM-Pass1 ou jalon dedie C2
- NextStepID et AnimToPlay : variables declarees non utilisees, candidats a suppression -> nettoyage futur
- DebugPrint HandleAttack "Can Attack & reset combo" : a conditionner a un flag debug avant ship

#### Etat final
COMBAT-SwordMoveset CLOS. Combo epee fonctionnel (Light x2 + Heavy x1), TenaciteEtat dans AttributeSet (base 25).

---

### 31/05/2026 -- SaveDesign -- DESIGN VALIDE

#### Fontaine de Fee -- lore et mecanique -- DESIGN VALIDE
- Justification narrative : la Fee "grave" le souvenir du monde aux Fontaines (pas le heros qui sauvegarde)
- Fontaines contextuelles : apparaissent dans le monde a des moments cles (post-boss, entree zone, apres cinematique) -- remplace le concept de "save silencieuse sur jalon narratif"
- Jalons narratifs : sauvegardent la progression uniquement, ne deplacent pas le respawn point
- Respawn : ennemis normaux oui, boss et mini-boss jamais
- Interaction Fontaine : restore HP/ST/MP + purge Corruption (cout variable) + regenere la Fee + respawn ennemis

#### Systeme Corruption / Essence / Fontaine -- DESIGN VALIDE
- Cout depenses Essence : 0-74% = x1.0 / 75-99% = x1.15 / 100% = inutilisable
- Cout purge Corruption a la Fontaine : 0-74% = gratuit / 75-99% = petit cout Essence / 100% = grand cout Essence
- Montee niveau deite : 0-74% = normal / 75-99% = cout +15% / 100% = bloque
- Calibrage exact des couts de purge -> session Economie/Drops
- Tension de design : double penalite economique si Corruption haute (depenses + purge)

#### Essence au sol -- mecanique mort -- DESIGN VALIDE
- Mort par environnement -> Essence tombe au sol (objet physique ramassable)
- Mort par ennemi -> mob fatal porte l'Essence (doit etre tue pour recuperer)
- Exception boss/mini-boss -> Essence tombe au sol (jamais re-tuables)
- Essence non recuperee avant 2eme mort -> perdue definitivement

#### Slots de sauvegarde -- DESIGN VALIDE
- Multi-parties : plusieurs slots (ex. 3), chaque slot = une partie distincte
- Intra-partie : slot unique, ecrasement automatique -- souls-like strict

#### Architecture technique -- DESIGN VALIDE
- BP_SaveGame_SoM : structure complete (stats, inventaire, magie, progression monde, Essence au sol)
- BP_FountainComponent : FountainID Name editable, bIsActivated, OnPlayerInteract()
- Convention nommage FountainID : Fountain_[Acte]_[Zone]_[Index]
- Flux save : GameMode.OnFountainRest(FountainID) -> collecte -> SaveGameToSlot
- Flux mort : dropper Essence -> LoadGameFromSlot -> restaurer -> teleporter a LastFountainTransform
- Nouveau fichier : Docs/Architecture/SaveSystem.md

#### Etat final
DESIGN-SaveDesign VALIDE. Spec complete dans Docs/Architecture/SaveSystem.md.

---

### 31/05/2026 -- C1-HUDCore -- VALIDE

#### Etat final
C1-HUDCore VALIDE. Architecture event-driven HP/ST/MP/Essence/Corruption operationnelle.

---

### 30/05/2026 -- Session design -- Weapons_Progression -- DESIGN VALIDE

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
Pour le systeme de save : voir Docs/Architecture/SaveSystem.md

## Historique
- Creation : 17/06/2025
- Derniere mise a jour : 31/05/2026
