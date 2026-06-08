# Decisions Architecturales -- Shadow of Mana

Ce fichier centralise toutes les decisions importantes prises sur le projet.
Objectif : retrouver en 30 secondes POURQUOI une chose a ete faite sans fouiller le journal.

Format : chaque decision = date + contexte + decision + raison + consequences.

---

## PATTERNS ETABLIS -- Constitution technique du projet

Ces regles s'appliquent a TOUT nouveau systeme. Les lire avant de concevoir quoi que ce soit.

### [PERMANENT] Persistance -- BPI_Saveable
**Regle** : Tout systeme ayant un etat a persister entre les sessions implemente BPI_Saveable.
SaveData() ecrit dans BP_SaveGame_SoM. LoadData() reconstruit l'etat depuis les donnees sauvegardees.
Le GameMode itere sur GetComponentsByInterface(BPI_Saveable) -- il ne connait pas les details.
**Raison** : Decouplage total. Ajouter un nouveau systeme = implementer l'interface, zero modification du GameMode.
**Systemes actuels** : BP_InventoryComponent, BP_ComboManagerComponent, BP_MagicComponent, BP_AttributeSet_Base, BP_FountainComponent
**Systemes futurs** : BP_QuestComponent (C4), BP_ForgeComponent (C3), BP_CorruptionComponent si etat persistant
**Ne pas faire** : Collecter les donnees directement dans GameMode.OnFountainRest par type concret.

### [PERMANENT] Modification de stats -- SetStatValue
**Regle** : Toute modification de stat passe par SetStatValue(StatName, Value). Zero exception.
Notification via OnStatChanged. L'UI ne poll jamais.
**Raison** : Un seul point de modification = debug trivial, pas de desync UI possible.
**Ne pas faire** : SET direct sur une variable de stat depuis un Blueprint externe.

### [PERMANENT] Etat metier -- jamais dans HC
**Regle** : BP_SoM_HeroCharacter = coordinateur leger uniquement. Tout etat metier vit dans un composant dedie.
Si une donnee peut appartenir a un composant existant, elle y va.
Si aucun composant n'est adapte, creer un nouveau composant avant d'ajouter a HC.
**Raison** : HC devient un God Object si on y accumule de l'etat. Chaque composant est testable et remplacable independamment.
**Composants actuels** : BP_ComboManagerComponent (arme+combat), BP_InventoryComponent (armes connues),
BP_MagicComponent (sorts+deites), BP_CorruptionComponent (corruption), BP_CombatLockOnComponent (lock-on)
**Ne pas faire** : Ajouter une variable d'etat directement sur HC sans passer par un composant.

### [PERMANENT] Source de verite unique
**Regle** : Toute donnee a un et un seul proprietaire. Jamais dupliquer une donnee entre deux systemes.
| Donnee | Proprietaire unique |
|---|---|
| Arme equipee | ComboManager.CurrentWeaponID |
| Armes connues | InventoryComponent.DiscoveredWeapons |
| Etat magie (sorts, deites) | MagicComponent |
| Stats heros | AttributeSet |
| Etat corruption | CorruptionComponent |
| Save courante | GameMode.CurrentSaveGame |
| Etat activation Fontaine | BP_FountainComponent.bIsActivated |
| Etat lock-on | BP_CombatLockOnComponent |
**Ne pas faire** : Stocker CurrentWeaponID a la fois dans HC et dans ComboManager.

### [PERMANENT] Extensibilite par interface Blueprint
**Regle** : Des qu'un comportement va concerner plusieurs systemes heterogenes, creer une interface Blueprint.
Ne pas brancher en dur sur des types concrets quand une interface suffit.
**Raison** : Un nouveau systeme = implementer l'interface, pas modifier tous les appelants.
**Interfaces actuelles** : BPI_Saveable, BPI_Interactable, BPI_Lockable
**Interfaces futures probables** : BPI_Damageable, BPI_StatusEffectable
**Ne pas faire** : Switch sur des types concrets pour appeler des comportements communs.

### [PERMANENT] Points d'entree uniques
**Regle** : Toute action significative a un unique point d'entree nomme explicitement.
Ne jamais contourner ces points d'entree, meme "pour aller plus vite".
| Action | Point d'entree unique |
|---|---|
| Changer l'arme equipee | ComboManager.EquipWeapon(WeaponID, WeaponLevel) |
| Modifier une stat | AttributeSet.SetStatValue(StatName, Value) |
| Declencher une save | GameMode.OnFountainRest(FountainID) |
| Lancer un sort | MagicComponent.CastSpell(SpellID) |
| Ajouter une arme connue | InventoryComponent.AddWeapon(WeaponID) |
| Interagir avec un Actor | BPI_Interactable.Interact(Instigator) |
| Activer le lock-on | BP_CombatLockOnComponent.ActivateLockOn |
**Ne pas faire** : Appeler SaveGameToSlot directement depuis un Blueprint quelconque.

### [PERMANENT] Sauvegarde -- sauvegarder le delta, pas l'etat derive
**Regle** : Ne jamais sauvegarder une donnee qui peut etre reconstruite depuis une source existante (DataTable, calcul).
Sauvegarder uniquement ce qui ne peut pas etre recalcule : le delta, les flags, les compteurs.
**Exemple concret** : LockedDeities (Array<Name>) est sauvegarde, pas UnlockedSpells (Map<Name, FSoM_DeitySpells>).
Au load : reconstruction depuis DT_Deities via UnlockDeity() pour chaque deite non bloquee.
**Raison** : Robuste aux modifications futures des DataTables. Pas de desync possible entre SaveGame et source de verite.
**Ne pas faire** : Sauvegarder une Map complexe qui est une vue calculee depuis une DataTable.

---

## LOCK-ON -- BPI_Lockable (08/06/2026)

### [08/06/2026] BPI_Lockable -- interface de ciblage universelle
**Contexte** : Refacto COMBAT-LockOnRefacto -- BP_CombatLockOnComponent avait 6 casts concrets sur BP_Enemy_Base, couplage fort.
**Decision** : Creer BPI_Lockable avec 3 elements :
- GetLockSocketName() -> FName : retourne le nom du socket de ciblage (ex: "HeadLock")
- IsDeadOrDestroyed() -> bool : retourne (bIsDead OR IsActorBeingDestroyed)
- OnLockableTargetDied (Event) : declenche quand l'ennemi meurt, notifie le composant lock-on
**Raison** : Le composant lock-on ne connait plus BP_Enemy_Base. Tout Actor futur (boss, piege, vehicule) peut etre lockable en implementant BPI_Lockable.
**Consequences** :
- BP_Enemy_Base implemente BPI_Lockable des C1
- GetLockMesh() a ajouter en C2 pour eliminer le dernier Cast BP_Enemy_Base dans UpdateLockOnUIIndicator
- HandleTargetDeath doit etre declenche uniquement depuis OnLockableTargetDied (pas depuis SelectInitialTarget)

### [08/06/2026] GOTCHA -- SelectInitialTarget -- bIsDead doit etre inverse
**Contexte** : Lors du debug COMBAT-LockOnRefacto, SelectInitialTarget selectionnait uniquement les ennemis morts.
**Cause** : bIsDead output de Message IsDeadOrDestroyed connecte directement a AND.B sans NOT.
**Fix** : Inserer NOT Boolean entre bIsDead et AND.B. Condition correcte = AND(IsValid, NOT bIsDead) = vivants uniquement.
**Regle** : Dans tout contexte de filtrage de cibles lockables, toujours verifier que la condition "est vivant" = NOT bIsDead.

### [08/06/2026] GOTCHA -- HandleTargetDeath inconditionnel = infinite loop
**Contexte** : HandleTargetDeath appele apres ForEachLoop.Completed dans SelectInitialTarget -> infinite loop.
**Cause** : L'appel etait systematique, pas conditionnel a la mort d'une cible.
**Fix** : Supprimer l'appel inconditionnel. HandleTargetDeath doit etre appele uniquement depuis le callback OnLockableTargetDied.
**Regle** : Ne jamais appeler HandleTargetDeath directement depuis SelectInitialTarget.

### [08/06/2026] GetComponentByClass(BP_CombatLockOnComponent) -- sur Hero pas PlayerController
**Regle** : Le composant BP_CombatLockOnComponent est sur BP_SoM_HeroCharacter, pas sur BP_SoM_PlayerController.
Toujours utiliser GetPlayerCharacter(0) comme cible de GetComponentByClass, jamais GetPlayerController(0).

---

## INTERACTION -- BPI_Interactable (07/06/2026)

### [07/06/2026] BPI_Interactable -- interface d'interaction universelle
**Contexte** : Refacto BP_FountainComponent -- besoin d'un systeme d'interaction volontaire extensible (fontaines, vendeurs, PNJ, leviers...).
**Decision** : Creer BPI_Interactable avec une seule fonction Interact(Instigator: BP_SoM_PlayerController).
PC.OnInteract (IA_Interact) : GetOverlappingActors(HC) -> ForEachLoop -> DoesImplementInterface(BPI_Interactable) -> Message Interact.
**Raison** : Le PC ne connait jamais les types concrets des interactables. Ajouter un vendeur = implementer l'interface, zero modification du PC.
**Consequences** :
- BP_Fountain_Actor implemente BPI_Interactable des C1
- Vendeurs, PNJ, leviers implementeront BPI_Interactable en C2/C3
- Priorite entre interactables superposees -> UI-InteractPriority C2

### [07/06/2026] Input mode UI -- SetInputModeUIOnly obligatoire
**Contexte** : Swap IMC seul (RemoveIMC/AddIMC) ne bloque pas le mouvement du personnage a l'ouverture d'un menu UMG.
**Decision** : Toute ouverture de menu UMG doit utiliser SetInputModeUIOnly + SetShowMouseCursor=true. Fermeture : SetInputModeGameOnly + SetShowMouseCursor=false.
**Raison** : SetInputModeUIOnly capture la souris et bloque les inputs gameplay. Swap IMC seul est insuffisant.
**Consequences** : Pattern a appliquer a tous les futurs menus UMG (inventaire, forge, dialogue...).

### [07/06/2026] Feedback visuel Fontaine -- notification directe Component -> Actor
**Contexte** : Le PointLight ne se mettait pas a jour si le joueur restait dans la zone d'overlap lors de l'activation.
**Decision** : BP_FountainComponent pousse directement la mise a jour visuelle (SetIntensity + SetLightColor) sur FountainLight de BP_Fountain_Actor au moment de SET bIsActivated=true. Le BeginOverlap gere uniquement l'affichage a l'approche.
**Raison** : BeginOverlap ne se retrigger pas si le joueur ne quitte pas la zone. La notification directe garantit l'immediacy du feedback.

---

## FONTAINE DE FEE -- DESIGN (05/06/2026)

### [05/06/2026] Interaction Fontaine -- deux etats, un seul type d'interaction
**Contexte** : Discussion design systeme Fontaine -- trigger automatique overlap vs interaction volontaire + menu.
**Decision** :
- Toute interaction avec la Fontaine est volontaire (touche/bouton dedie, pas overlap automatique).
- bIsActivated=false (1ere fois) : animation activation + SET bIsActivated=true + regen HP/ST/MP + save spawn. Pas de menu, pas de respawn ennemis. Identique a l'allumage d'un feu de camp DS.
- bIsActivated=true (fois suivantes) : ouvre UI_FountainMenu.
**Raison** : Reproduire la tension DS -- la 1ere activation est gratuite, les suivantes ont un cout (respawn ennemis). Coherence avec l'identite du jeu.
**Consequences** : Refacto BP_FountainComponent -- supprimer le trigger overlap actuel, ajouter logique interaction + bIsActivated. Fait dans UI-FountainMenu (C1).

### [05/06/2026] UI_FountainMenu -- deux actions
**Decision** :
- **Se reposer** : regen HP/ST/MP + save + respawn ennemis zone + PurgeCorruption + restock objets.
- **Menu Inventaire** : quickslots + upgrade magie/deites + level up hero (depense Essence).
**Raison** : Separer l'action "dangereuse" (respawn + purge) du menu de gestion. Le joueur choisit consciemment.
**Consequences** : UI draft en C1 (listes texte, pas d'icones). Polish en C2 (UI-FountainMenu-Polish).

### [05/06/2026] Essence -- monnaie unique
**Decision** : L'Essence est la monnaie unique pour tout : montee de niveau hero, upgrade magie/deites, purge Corruption.
**Raison** : Tension intentionnelle -- chaque depense d'Essence exclut les autres (style DS souls). Simplicite economique en C1.
**Point ouvert** : Calibrage des couts -> SESSION-Economie.

### [05/06/2026] Acces au menu de gestion -- Fontaine uniquement
**Decision** : Le menu inventaire/magie/level n'est accessible qu'aux Fontaines. Pas de menu pause global pour ces fonctions.
**Raison** : Coherent avec l'identite DS. Les Fontaines ont un role fort (repos, gestion, progression). Cree de la tension en combat (pas de gestion a la volee).

---

## REPLANIFICATION C1 (05/06/2026)

### [05/06/2026] MAGIC-TreeModule -- reporte C2
**Decision** : MAGIC-TreeModule sort du scope C1 et passe en C2.

### [05/06/2026] ANIM-Pass1 -- reporte C2
**Decision** : ANIM-Pass1 (rename ABP + roll en lock-on) sort du scope C1 et passe en C2.

### [05/06/2026] ENEMY-DropSystem -- ajoute en C1
**Decision** : Nouveau jalon C1 -- mort ennemi spawn BP_EssenceDrop + chance objet simple.
**Architecture** : BP_Enemy_Base.OnDeath -> SpawnActor(BP_EssenceOrb) avec EssenceDropValue configurable.

---

## ARMES & INVENTAIRE

### [29/05/2026] Source de verite arme courante -- ComboManager
**Decision** : BP_ComboManagerComponent = source de verite unique pour l'arme courante et le niveau arme.
HC.ChoosenWeapon supprime. EquipWeapon vit sur ComboManager.

### [29/05/2026] DiscoveredWeapons -- migration vers InventoryComponent
**Decision** : DiscoveredWeapons migre vers BP_InventoryComponent.

### [29/05/2026] Switch arme en cours de combo -- reset combo (punition)
**Decision** : Switch arme = reset combo complet. ComboManager.EquipWeapon reinitialise l'etat combo.

---

## SYSTEME DE STATS & COMBAT

### [29/05/2026] TenaciteEtat heros -- valeur de base 25
**Decision** : TenaciteEtat heros = 25 en valeur de base.

---

## SAVE SYSTEM

### [03/06/2026] Architecture save -- BPI_Saveable (pattern interface)
**Decision** : Architecture interface BPI_Saveable. Chaque composant est responsable de ses propres donnees.

### [03/06/2026] LockedDeities vs UnlockedSpells -- sauvegarder le delta
**Decision** : Sauvegarder LockedDeities (Array<Name>) uniquement.

### [03/06/2026] HP/ST/MP -- non persistees
**Decision** : HealthCurrent, StaminaCurrent, ManaCurrent ne sont pas sauvegardees.

---

## COMBAT & FEEDBACK

### [21/05/2026] Hit Flash ennemi -- ABANDONNE
### [18/05/2026] Hitstop -- REPORTE C2
### [18/05/2026] Knockback ennemi -- LaunchCharacter 400.0

---

## ENNEMIS

### [23/05/2026] WeaponClass ennemi -- ABANDONNE

---

## LOCK-ON

### [21/05/2026] Cooldown switch cible -- source de verite = Component
**Decision** : SwitchCooldown dans BP_CombatLockOnComponent = source de verite unique.

### [15/05/2026] Strafe -- animations placeholder jusqu'a C2-ANIM-Pass1

---

## CAMERA & MOUVEMENT

### [18/05/2026] Roll en lock-on -- REPORTE ANIM-Pass1 (C2)
### [17/05/2026] IA_Look -- dans le PC (pas HC)
### [17/05/2026] UpdateLockOnRotation -- conditionnel V2

---

## INPUTS

### [07/06/2026] IA_Interact -- ajout UI-FountainMenu
**Decision** : Nouvelle InputAction IA_Interact (Digital/bool), binding touche E + Gamepad Face Button Bottom dans IMC_Gameplay.

### [23/05/2026] Architecture IMC -- 5 IMC distincts
| IMC | Contenu | Mode |
|---|---|---|
| IMC_Gameplay | Move, Look, Jump, Dodge, Sprint, LockOn, Attack, Block, RadialOpen, Quickslots, Interact | Exclusif |
| IMC_Radial | Rotate, Validate, Cancel, ChangeCat | Exclusif |
| IMC_Menu | Navigate, Confirm, Back | Exclusif |
| IMC_Dialogue | Confirm/Avance, Choix | Cumulatif avec Gameplay |
| IMC_Cutscene | IA_Skip | Exclusif |

### [07/05/2026] Source unique InputActions -- Content/Input/InputActions/ uniquement

---

## RADIAL MENU & MAGIE

### [25/05/2026] ValidateRadial -- fonction dediee PC + condition CurrentCategory
### [25/05/2026] ERadialMode -- 3 valeurs : Weapons / Deity / Spell
### [25/05/2026] UnlockDeity -- "Set Members in FSoM_DeitySpells" (pas Make)
### [21/05/2026] Architecture Radial Magie -- 2 niveaux imbriques N1=ecoles, N2=sorts
### [13/05/2026] Slow-mo radial -- Time Dilation 0.2

---

## MAGIE -- PROGRESSION

### [23/05/2026] Montee de niveau des magies -- jalon design dedie
### [23/05/2026] UnlockedSpells -- stub test BeginPlay (DETTE C1-MagicUnlockSystem)

---

## ASSETS & PIPELINE

### [11/05/2026] AnimGraph via MCP -- INTERDIT
### [14/05/2026] LevelMin DT_Combo -- valeur 0

---

## Historique

- Creation : 21/05/2026
- 08/06/2026 : section LOCK-ON BPI_Lockable, gotchas SelectInitialTarget, HandleTargetDeath, GetComponentByClass
- 07/06/2026 : section INTERACTION BPI_Interactable, SetInputModeUIOnly, feedback PointLight
- 07/06/2026 : IA_Interact dans INPUTS, BPI_Interactable dans PATTERNS interfaces actuelles
- 05/06/2026 : section FONTAINE DE FEE, REPLANIFICATION C1
- 03/06/2026 : PATTERNS ETABLIS, decisions SYS-SaveGame
- 29/05/2026 : ComboManager, InventoryComponent, TenaciteEtat
- 23/05/2026 : IMC, dialogues, ennemis sans WeaponClass
- 25/05/2026 : ERadialMode, SwitchCategory, bug Make FSoM_DeitySpells
