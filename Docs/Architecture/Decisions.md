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
**Systemes actuels** : BP_InventoryComponent, BP_ComboManagerComponent, BP_MagicComponent, BP_AttributeSet_Base
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
**Ne pas faire** : Stocker CurrentWeaponID a la fois dans HC et dans ComboManager.

### [PERMANENT] Extensibilite par interface Blueprint
**Regle** : Des qu'un comportement va concerner plusieurs systemes heterogenes, creer une interface Blueprint.
Ne pas brancher en dur sur des types concrets quand une interface suffit.
**Raison** : Un nouveau systeme = implementer l'interface, pas modifier tous les appelants.
**Interfaces actuelles** : BPI_Saveable
**Interfaces futures probables** : BPI_Damageable, BPI_Interactable, BPI_StatusEffectable
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
**Ne pas faire** : Appeler SaveGameToSlot directement depuis un Blueprint quelconque.

### [PERMANENT] Sauvegarde -- sauvegarder le delta, pas l'etat derive
**Regle** : Ne jamais sauvegarder une donnee qui peut etre reconstruite depuis une source existante (DataTable, calcul).
Sauvegarder uniquement ce qui ne peut pas etre recalcule : le delta, les flags, les compteurs.
**Exemple concret** : LockedDeities (Array<Name>) est sauvegarde, pas UnlockedSpells (Map<Name, FSoM_DeitySpells>).
Au load : reconstruction depuis DT_Deities via UnlockDeity() pour chaque deite non bloquee.
**Raison** : Robuste aux modifications futures des DataTables. Pas de desync possible entre SaveGame et source de verite.
**Ne pas faire** : Sauvegarder une Map complexe qui est une vue calculee depuis une DataTable.

---

## FONTAINE DE FEE -- DESIGN (05/06/2026)

### [05/06/2026] Interaction Fontaine -- deux etats, un seul type d'interaction
**Contexte** : Discussion design systeme Fontaine -- trigger automatique overlap vs interaction volontaire + menu.
**Decision** :
- Toute interaction avec la Fontaine est volontaire (touche/bouton dedie, pas overlap automatique).
- bIsActivated=false (1ere fois) : animation activation + SET bIsActivated=true + regen HP/ST/MP + save spawn. Pas de menu, pas de respawn ennemis. Identique a l'allumage d'un feu de camp DS.
- bIsActivated=true (fois suivantes) : ouvre UI_FountainMenu.
**Raison** : Reproduire la tension DS -- la 1ere activation est gratuite, les suivantes ont un cout (respawn ennemis). Coherence avec l'identite du jeu.
**Consequences** : Refacto BP_FountainComponent -- supprimer le trigger overlap actuel, ajouter logique interaction + bIsActivated. A faire dans UI-FountainMenu (C1).

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

### [05/06/2026] Vision ART Fontaine -- note de maturation
**Idee** : Racines de l'arbre Mana poussant a l'activation (animees par la Fee). Fee se reposant dans la Fontaine lors des interactions.
**Statut** : En maturation. Pas de pipeline ART confirme. Session ART-Fontaine a planifier quand Nico est pret.
**C1** : Changement couleur/materiau sur bIsActivated suffit.

---

## REPLANIFICATION C1 (05/06/2026)

### [05/06/2026] MAGIC-TreeModule -- reporte C2
**Decision** : MAGIC-TreeModule sort du scope C1 et passe en C2.
**Raison** : Lumina avec ses 4 sorts de base suffit pour valider le POC C1. L'arbre de talents est du contenu, pas une mecanique bloquante pour la boucle de jeu C1.
**Consequences** : C1 se concentre sur la boucle core (combat + drops + fontaine + boss).

### [05/06/2026] ANIM-Pass1 -- reporte C2
**Decision** : ANIM-Pass1 (rename ABP + roll en lock-on) sort du scope C1 et passe en C2.
**Raison** : Dette technique et amelioration, pas bloquant pour le POC C1. Le roll hors lock-on fonctionne. ABP_Manny_Platforming est fonctionnel meme mal nomme.
**Consequences** : Dettes associees maintenues dans la liste dettes C2.

### [05/06/2026] ENEMY-DropSystem -- ajoute en C1
**Decision** : Nouveau jalon C1 -- mort ennemi spawn BP_EssenceDrop + chance objet simple.
**Raison** : Sans drop ennemi, tuer un ennemi n'a pas de retour tangible. Indispensable pour que MAP-C1Level soit satisfaisante a jouer.
**Architecture** : BP_Enemy_Base.OnDeath -> SpawnActor(BP_EssenceDrop) avec EssenceValue configurable. Table de drop simple (1 type d'objet max en C1). Calibrage valeurs en C2.

---

## ARMES & INVENTAIRE

### [29/05/2026] Source de verite arme courante -- ComboManager
**Contexte** : Doublon entre HC.ChoosenWeapon et ComboManager.CurrentWeaponID.
**Decision** : BP_ComboManagerComponent = source de verite unique pour l'arme courante et le niveau arme.
HC.ChoosenWeapon supprime. EquipWeapon vit sur ComboManager.
**Raison** : Coherent avec la philosophie composants dedies. HC delegue, ne stocke pas.
**Consequences** : Tout appelant (Radial, PC, HC) passe par ComboManager.EquipWeapon. Ne jamais recreer de variable arme sur HC.

### [29/05/2026] DiscoveredWeapons -- migration vers InventoryComponent
**Decision** : DiscoveredWeapons migre vers BP_InventoryComponent.
Component accueillera aussi : consommables Seiken, materiaux de craft, equipement.
**Raison** : ComboManager = combat/combo uniquement. L'inventaire est une donnee de progression.
**Consequences** : Radial interroge InventoryComponent.GetWeapons() pour peupler ses slots.

### [29/05/2026] Switch arme en cours de combo -- reset combo (punition)
**Decision** : Switch arme = reset combo complet. ComboManager.EquipWeapon reinitialise l'etat combo.
**Raison** : Coherent avec l'identite Dark Souls. Pas de grisage UI Radial pendant combo.

---

## SYSTEME DE STATS & COMBAT

### [29/05/2026] TenaciteEtat heros -- valeur de base 25
**Decision** : TenaciteEtat heros = 25 en valeur de base. Cle supplementaire dans BP_AttributeSet_Base.
Modifiable par equipement, buffs/debuffs, et Corruption.
**Raison** : Heros vulnerable par defaut aux effets de statut (Dark Souls style).
**Consequences** : BP_StatusEffectComponent lit TenaciteEtat via GetStatValue pour calculer la resistance.

---

## SAVE SYSTEM

### [03/06/2026] Architecture save -- BPI_Saveable (pattern interface)
**Contexte** : Premiere approche = GameMode collecte directement les donnees de chaque composant.
Problem : God Function, couplage fort, chaque nouveau systeme = modification du GameMode.
**Decision** : Architecture interface BPI_Saveable. Chaque composant est responsable de ses propres donnees.
GameMode.OnFountainRest appelle uniquement GetComponentsByInterface + ForEachLoop SaveData/LoadData.
**Raison** : Evolutivite maximale. BP_QuestComponent en C4 = implementer BPI_Saveable, zero modification ailleurs.
**Consequences** :
- Tout nouveau systeme persistant implemente BPI_Saveable
- GameMode ne connait jamais les types concrets des composants
- Voir Pattern PERMANENT ci-dessus

### [03/06/2026] LockedDeities vs UnlockedSpells -- sauvegarder le delta
**Contexte** : UnlockedSpells est une Map<Name, FSoM_DeitySpells> -- type complexe, vue calculee depuis DT_Deities.
**Decision** : Sauvegarder LockedDeities (Array<Name>) uniquement.
Au load : GetDataTableRowNames(DT_Deities) -> ForEachLoop -> NOT IN LockedDeities -> UnlockDeity(RowName).
**Raison** : Si DT_Deities est modifie (nouvelle deite, reequilibrage), le load se reconstruit proprement.
Sauvegarder UnlockedSpells = risque de desync si la DataTable change entre deux sessions.
**Consequences** : Principe generalise -> Pattern PERMANENT "sauvegarder le delta, pas l'etat derive".

### [03/06/2026] HP/ST/MP -- non persistees
**Decision** : HealthCurrent, StaminaCurrent, ManaCurrent ne sont pas sauvegardees.
Au load (apres mort), elles sont restaurees a leur valeur Max via SetStatValue.
**Raison** : Le respawn restaure toujours a 100%. Sauvegarder l'etat instantane de combat est sans valeur.
**Consequences** : AttributeSet.LoadData = SET EssenceValue uniquement + SetStatValue HP/ST/MP=Max.

---

## COMBAT & FEEDBACK

### [21/05/2026] Hit Flash ennemi -- ABANDONNE
**Decision** : Abandonner le hit flash ennemi. CS_EnemyDeath + animation hit reaction suffisent.

### [18/05/2026] Hitstop -- REPORTE C2
**Decision** : Reporter apres C2-EnemyMesh + C1-SFXCombat.
**Raison** : Impossible d'evaluer le feeling sans animations de hit reaction et vrais SFX.

### [18/05/2026] Knockback ennemi -- LaunchCharacter 400.0
**Decision** : 400.0 comme valeur initiale, override XY=true, Z=false. A tuner.

---

## ENNEMIS

### [23/05/2026] WeaponClass ennemi -- ABANDONNE
**Decision** : Supprimer WeaponClass de BP_Enemy_Base. Chaque ennemi a ses attaques integrees.
**Raison** : Les ennemis ne sont pas des clones du hero. Systeme generique WeaponClass = complexite inutile.
**Point ouvert** : Magie ennemie -> probablement DT_Spells ou sous-ensemble. Decision reportee C2.

---

## LOCK-ON

### [21/05/2026] Cooldown switch cible -- source de verite = Component
**Decision** : SwitchCooldown dans BP_CombatLockOnComponent = source de verite unique.
**Consequences** : Ne jamais creer LockOnSwitchCooldown dans le PC.

### [15/05/2026] Strafe -- animations placeholder jusqu'a C2-ANIM-Pass1

---

## CAMERA & MOUVEMENT

### [18/05/2026] Roll en lock-on -- REPORTE ANIM-Pass1 (C2)
**Cause racine** : Root Motion World Space + UseControllerRotationYaw=true annule SetActorRotation.
**Solution prevue** : LaunchCharacter direction stick+camera + animation visuelle sans Root Motion.

### [17/05/2026] IA_Look -- dans le PC (pas HC)
**Raison** : La gestion camera appartient au Controller, pas au Character.

### [17/05/2026] UpdateLockOnRotation -- conditionnel V2
**Decision** : bPlayerIsLooking + LookReturnDelay (1.5s) + LockOnReturnSpeed (3.0).
Branch(IsRolling) en guard : si rolling, pas de SetControlRotation.

---

## INPUTS

### [23/05/2026] Architecture IMC -- 5 IMC distincts
| IMC | Contenu | Mode |
|---|---|---|
| IMC_Gameplay | Move, Look, Jump, Dodge, Sprint, LockOn, Attack, Block, RadialOpen, Quickslots | Exclusif |
| IMC_Radial | Rotate, Validate, Cancel, ChangeCat | Exclusif |
| IMC_Menu | Navigate, Confirm, Back | Exclusif |
| IMC_Dialogue | Confirm/Avance, Choix | Cumulatif avec Gameplay |
| IMC_Cutscene | IA_Skip | Exclusif |

### [07/05/2026] Source unique InputActions -- Content/Input/InputActions/ uniquement

---

## RADIAL MENU & MAGIE

### [25/05/2026] ValidateRadial -- fonction dediee PC + condition CurrentCategory
**Decision** : Extraire la logique dans ValidateRadial(). Variables locales TempSchoolID et TempSpellID.
Condition N1/N2 sur CurrentCategory (ERadialMode), pas CurrentMagicSchool.

### [25/05/2026] ERadialMode -- 3 valeurs : Weapons / Deity / Spell

### [25/05/2026] UnlockDeity -- "Set Members in FSoM_DeitySpells" (pas Make)
**Raison** : Make FSoM_DeitySpells a bDefaultValueIsIgnored=True sur SpellIDs -> bug silencieux.

### [21/05/2026] Architecture Radial Magie -- 2 niveaux imbriques N1=ecoles, N2=sorts

### [13/05/2026] Slow-mo radial -- Time Dilation 0.2

---

## MAGIE -- PROGRESSION

### [23/05/2026] Montee de niveau des magies -- jalon design dedie
**Decision** : Aucune implementation avant la session design C1-MagicProgressionDesign.

### [23/05/2026] UnlockedSpells -- stub test BeginPlay (DETTE C1-MagicUnlockSystem)
**Decision** : Stub temporaire Lumina en BeginPlay MagicComponent. A retirer quand UnlockSpell en production.

---

## GAMEPLAY & NARRATION

### [23/05/2026] Dialogues quetes annexes -- personnage mobile
**Decision** : IMC_Dialogue cumulatif avec IMC_Gameplay. Distance check via Blueprint.

---

## SYSTEME DE STATS & COMBAT

### [07/05/2026] SetStatValue -- unique point de modification
**Decision** : SetStatValue(StatName, Value) = UNIQUE point de modification. OnStatChanged = dispatcher.

### [07/05/2026] UI HUD -- zero polling
**Decision** : UI_HUD_Main entierement event-driven via OnStatChanged.

### [18/05/2026] ComboManager -- HandleAttack sans parametre ChoosenWeapon
**Decision** : ComboManager lit CurrentWeaponID en interne. Pas de parametre externe.

---

## ASSETS & PIPELINE

### [11/05/2026] AnimGraph via MCP -- INTERDIT
**Decision** : Ne jamais creer d'etat AnimGraph via add_state MCP. Toujours manuel dans UE5.7.

### [14/05/2026] LevelMin DT_Combo -- valeur 0
**Decision** : LevelMin = 0 sur toutes les rows DT_Combo.

---

## Historique

- Creation : 21/05/2026
- 23/05/2026 : architecture IMC, dialogues, correction noms IA, ennemis sans WeaponClass
- 25/05/2026 : ERadialMode, SwitchCategory, bug Make FSoM_DeitySpells, ValidateRadial
- 29/05/2026 : ComboManager source verite arme, DiscoveredWeapons -> InventoryComponent, TenaciteEtat 25
- 03/06/2026 : SECTION PATTERNS ETABLIS ajoutee (constitution technique permanente)
- 03/06/2026 : decisions SYS-SaveGame : BPI_Saveable, LockedDeities vs UnlockedSpells, HP/ST/MP non persistees
- 05/06/2026 : section FONTAINE DE FEE -- design deux interactions, UI_FountainMenu, Essence monnaie unique, vision ART
- 05/06/2026 : section REPLANIFICATION C1 -- MAGIC-TreeModule et ANIM-Pass1 reportes C2, ENEMY-DropSystem et UI-FountainMenu ajoutes C1
