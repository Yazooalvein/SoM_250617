# Decisions Architecturales -- Shadow of Mana

Ce fichier centralise toutes les decisions importantes prises sur le projet :
design, architecture technique, choix d'implementation, abandons.
Objectif : retrouver en 30 secondes POURQUOI une chose a ete faite sans fouiller le journal.

Format : chaque decision = date + contexte + decision + raison + consequences.

---

## COMBAT & FEEDBACK

### [21/05/2026] Hit Flash ennemi -- ABANDONNE
**Contexte** : Architecture DMI (Dynamic Material Instance) implementee sur BP_Enemy_Base.
Le flash visuel ne fonctionnait pas car M_Mannequin est un material Engine partage, read-only en runtime.
Solution identifiee : dupliquer en M_Enemy_Base. Mais cout vs benefice questionne.
**Decision** : Abandonner le hit flash ennemi.
**Raison** : CS_EnemyDeath (screen shake camera) + animation hit reaction dediee suffisent pour le feedback visuel.
Le flash est un detail polish, pas une priorite sur la base de combat.
**Consequences** : Architecture DMI reste dans le code mais non utilisee. CS_EnemyDeath = seul feedback visuel mort ennemi.

### [18/05/2026] Hitstop -- REPORTE
**Contexte** : Hitstop prevu dans C1-HitFeel (Game Time Dilation 0.05 pendant 2-3 frames).
**Decision** : Reporter apres C2-EnemyMesh + C1-SFXCombat.
**Raison** : Impossible d'evaluer le feeling du hitstop sans animations de hit reaction et vrais SFX.
Reference Dark Souls : le feedback vient du son + animation stagger, pas d'un hitstop global.
**Consequences** : C1-HitFeel reste partiel. Hitstop evalue en C2 apres vrais assets.

### [18/05/2026] Knockback ennemi -- LaunchCharacter 400.0
**Contexte** : Premiere valeur de knockback.
**Decision** : 400.0 comme valeur initiale, override XY=true, Z=false.
**Raison** : Valeur empirique, a tuner selon feeling.
**Consequences** : Valeur exposee dans BP_Enemy_Base pour ajustement facile.

---

## ENNEMIS

### [23/05/2026] WeaponClass ennemi -- ABANDONNE, arme integree par ennemi
**Contexte** : BP_Enemy_Base avait une variable WeaponClass (hardcode BP_Enemy_Sword01)
prevue pour gerer les armes des ennemis via un systeme similaire au hero.
**Decision** : Supprimer toute notion de WeaponClass / systeme d'arme generique sur les ennemis.
Chaque ennemi a ses attaques et comportements integres directement dans son Blueprint child.
Pas de child BP dedie a la gestion d'arme.
**Raison** : Les ennemis dans SoM ne sont pas des clones du hero. Chaque type d'ennemi a une
identite combat propre (slime, chevalier, dragon...). Un systeme generique WeaponClass ajoute
de la complexite inutile. L'arme visuelle (mesh) est une partie du mesh ennemi ou un composant
statique sans logique separee.
**Consequences** :
- Supprimer WeaponClass de BP_Enemy_Base dans C2-EnemyMesh (ou des que touche)
- Pas de DT_Weapons cote ennemi, pas de ComboManager cote ennemi
- La dette "WeaponClass hardcode BP_Enemy_Sword01 (C2-EnemyMesh)" est CLOTUREE par cette decision
**Point ouvert** : Magie ennemie -- les ennemis capables de magie s'appuieront probablement
sur le meme referentiel que les sorts apprenables par le hero (meme DT_Spells ou sous-ensemble).
Decision reportee a C2 quand un premier ennemi magique sera concu.

---

## LOCK-ON

### [21/05/2026] Cooldown switch cible -- source de verite = Component
**Contexte** : Doublon detecte : LockOnSwitchCooldown dans BP_SoM_PlayerController
et SwitchCooldown dans BP_CombatLockOnComponent.
**Decision** : SwitchCooldown dans BP_CombatLockOnComponent = source de verite unique.
Supprimer LockOnSwitchCooldown du PC.
**Raison** : Le Component gere tout l'etat du lock-on (bisLockOnActive, CurrentTarget, AvailableTargets...).
Le cooldown en fait partie logiquement. Le PC ne doit pas avoir d'etat lock-on en propre.
Si un systeme externe interroge le cooldown, il le trouvera sur le Component.
**Consequences** : A implementer dans C1-CleanupDettes. Verifier que tout le code qui lisait
LockOnSwitchCooldown PC pointe sur GetBP_CombatLockOnComponent -> SwitchCooldown.

### [15/05/2026] Strafe -- animations placeholder
**Contexte** : Strafe gauche et droite en lock-on utilisent la meme animation (Jog_Left mirrored).
**Decision** : Garder le placeholder jusqu'a C1-AnimationsPass1.
**Raison** : Le systeme fonctionne, les animations distinctes sont un polish.
**Consequences** : Dette notee dans C1-AnimationsPass1.

---

## CAMERA & MOUVEMENT

### [18/05/2026] Roll en lock-on -- REPORTE
**Contexte** : En lock-on, le roll part vers l'ennemi au lieu de suivre le stick.
**Cause racine** : Root Motion en World Space + UseControllerRotationYaw=true force
le character a regarder l'ennemi chaque frame, annulant SetActorRotation.
**Decision** : Reporter la correction a C1-AnimationsPass1.
**Solution prevue** : LaunchCharacter dans direction stick+camera + animation visuelle sans Root Motion (architecture DS/KH).
**Consequences** : Roll hors lock-on fonctionne. Roll en lock-on visuellement incorrect jusqu'a C1-AnimationsPass1.

### [17/05/2026] IA_Look -- deplace dans le PC
**Contexte** : IA_Look etait dans BP_SoM_HeroCharacter.
**Decision** : Deplacer dans BP_SoM_PlayerController (fonction Aim).
**Raison** : La gestion camera appartient au Controller, pas au Character. Separation des responsabilites.
**Consequences** : Ne jamais rebrancher IA_Look dans HeroCharacter.

### [17/05/2026] UpdateLockOnRotation -- conditionnel V2
**Contexte** : La camera suivait la cible meme quand le joueur regardait ailleurs.
**Decision** : V2 avec bPlayerIsLooking + LookReturnDelay (1.5s) + LockOnReturnSpeed (3.0).
**Raison** : Le joueur doit pouvoir regarder librement en lock-on, la camera revient
automatiquement sur la cible apres un delai d'inactivite.
**Consequences** : Branch(IsRolling) en guard : si rolling, pas de SetControlRotation.

---

## INPUTS

### [23/05/2026] Architecture IMC -- liste definitive et modes d'activation
**Contexte** : IMC_Prototype trop chargee (gameplay + radial melange). Refonte complete de l'architecture IMC.
Question posee : faut-il 2 IMC generiques (Gameplay + UI) ou des IMC par contexte metier ?
**Decision** : 5 IMC distincts, chacun a une responsabilite unique :

| IMC | Contenu | Mode |
|---|---|---|
| IMC_Gameplay | Move, Look, Jump, Dodge, Sprint, LockOn, Attack, Block, RadialOpen, Quickslots | Exclusif (base permanente) |
| IMC_Radial | Rotate, Validate, Cancel, ChangeCat | Exclusif (remplace Gameplay pendant radial) |
| IMC_Menu | Navigate, Confirm, Back | Exclusif (pause, mort, main menu) |
| IMC_Dialogue | Confirm/Avance, Choix | CUMULATIF avec IMC_Gameplay |
| IMC_Cutscene | IA_Skip | Exclusif |

IMC_Forge et IMC_Map : points ouverts, decision reportee a C5/C3 selon besoins reels.

**Raison pour rejeter 2 IMC generiques** : IMC_Radial et IMC_Menu utilisent tous deux le stick
mais avec des comportements differents (rotation plateau vs navigation liste). Un fourre-tout
necessiterait des branches dans le code pour distinguer les contextes -- exactement ce qu'on evite.

**Raison cle pour IMC_Dialogue CUMULATIF** : le personnage peut bouger pendant les dialogues
(dialogues de quetes annexes). IMC_Dialogue s'ajoute par-dessus IMC_Gameplay (priority 1)
plutot que de le remplacer. Le systeme de distance (dialogue s'arrete si trop loin) est gere
cote Blueprint (distance check), pas par les inputs.

**Raison pour rejeter IMC_Combat** : le combat est une sous-couche du gameplay, pas un contexte
d'input distinct. Lock-on, attaques, tout est dans IMC_Gameplay.

**Raison pour rejeter IMC_Swimming/IMC_Climbing** : UE5 gere via CharacterMovement.
Les inputs restent les memes (IA_Move, IA_Jump), seul le mouvement change en interne.

**Consequences** :
- IMC_Prototype renomme IMC_Gameplay dans C1-InputsUI
- OpenRadial : Remove IMC_Gameplay -> Add IMC_Radial (priority 1)
- CloseRadial : Remove IMC_Radial -> Add IMC_Gameplay (priority 0)
- IMC_Menu, IMC_Dialogue, IMC_Cutscene : stubs crees maintenant, cables en C4/C7
- IA_UI_Radial_Open reste dans IMC_Gameplay (doit etre actif en jeu pour ouvrir le radial)
- IA_UI_Radial_Rotate migre dans IMC_Radial (etait oublie dans la liste initiale)

### [23/05/2026] IA Radial -- audit noms reels (correction doc)
**Contexte** : Les noms des IA dans CLAUDE.md et Input_Architecture.md etaient incorrects.
Audit T3D du PC a revele les vrais noms.
**Correction** :
- `IA_UI_RadialMenu_ChangeCat` -> reel : `IA_UI_Radial_ChangeCat`
- `IA_RadialMenu` -> reel : `IA_UI_Radial_Open`
- Nouvelle IA identifiee : `IA_UI_Radial_Rotate` (rotation stick, etait absente de la doc)
**Consequences** : Tous les fichiers doc corriges dans cette session.

### [23/05/2026] ToggleRadial -- architecture open/close separee
**Contexte** : Audit T3D de ToggleRadial revele :
- IsValid(RadialMainRef) ? TRUE -> CloseRadial() : FALSE -> OpenRadial()
- OpenRadial a ErrorType=1 (fonction manquante ou mal nommee -- a verifier en editeur)
**Decision** : Le swap IMC va dans OpenRadial et CloseRadial, pas dans ToggleRadial.
**Raison** : Responsabilites claires. ToggleRadial = routeur. Open/Close = logique metier.
**Consequences** : Verifier/creer OpenRadial avant d'implémenter le swap IMC.

### [21/05/2026] IMC separation initiale -- SUPERSEDE par decision 23/05/2026
**Note** : La decision initiale d'un IMC_UI generique est remplacee par l'architecture 5 IMC ci-dessus.

### [07/05/2026] Source unique InputActions
**Decision** : Toutes les IA dans Content/Input/InputActions/ uniquement.
**Raison** : Eviter la proliferation d'IA dupliquees dans des dossiers divers.
**Consequences** : Ne jamais creer d'IA en dehors de ce dossier.

---

## RADIAL MENU & MAGIE

### [21/05/2026] Architecture Radial Magie -- 2 niveaux imbriques
**Contexte** : Le radial actuel gere les armes. La magie n'est accessible que via quickslots.
**Decision** : 2 niveaux pour la magie dans le meme widget UI_Radial_Main :
- N1 : ecoles de magie (Lumina, Ondine, Ombre, Athanor, Sylphide, Gnome, Salamandre, Dryade)
- N2 : sorts de l'ecole selectionnee (Attack, Buff, Debuff, Soin)
**Raison** : Coherent avec le lore (8 deites). Le radial 1 seul niveau serait trop charge avec tous les sorts.
Navigation B = retour N2->N1, pas fermeture directe.
**Consequences** : SwitchCategory branche Magic = stub a implementer. PopulateMagicSchools + PopulateMagicSpells a creer.
Point ouvert : validation N2 = CastSpell ou assignation quickslot ?

### [21/05/2026] SelectedIndex radial -- retour sur arme equipee
**Contexte** : A chaque ouverture du radial Armes, SelectedIndex est remis a 0.
**Decision** : SelectedIndex doit pointer sur ChoosenWeapon dans DiscoveredWeapons a l'ouverture.
**Raison** : UX -- le joueur retrouve directement son arme equipee selectionnee, pas le premier slot.
**Consequences** : Lookup ChoosenWeapon -> FindIndex dans DiscoveredWeapons a ajouter dans OpenRadialMenu ou PopulateWeaponSlots.

### [13/05/2026] Slow-mo radial -- Time Dilation 0.2
**Decision** : Time Dilation 0.2 a l'ouverture du radial (pas de pause complete).
**Raison** : Maintenir la pression du combat. Le joueur prend une decision rapide, pas dans un menu hors-temps.
**Consequences** : CloseRadialMenu doit toujours restaurer Time Dilation a 1.0.

---

## GAMEPLAY & NARRATION

### [23/05/2026] Dialogues quetes annexes -- personnage mobile
**Contexte** : Reflexion sur le systeme de dialogue. Distinction entre cinematiques (personnage immobile)
et dialogues de quetes annexes (PNJ dans le monde).
**Decision** : Le personnage peut se deplacer pendant les dialogues de quetes annexes.
Comportement envisage (non definitif) : si le joueur s'eloigne trop du PNJ, le dialogue s'interrompt
et peut etre relance. Implementation via distance check Blueprint, pas via inputs.
**Raison** : Liberte de mouvement = moins de friction. Coherent avec le style ARPG ouvert.
**Consequences** : IMC_Dialogue = cumulatif avec IMC_Gameplay (pas de remplacement).
Distance check a definir lors de C4-DialogueSystem.
Point ouvert : seuil de distance exact, relance automatique ou manuelle ?

---

## SYSTEME DE STATS & COMBAT

### [07/05/2026] SetStatValue -- unique point de modification
**Decision** : SetStatValue(StatName, Value) = UNIQUE point de modification de toutes les stats.
OnStatChanged = dispatcher de notification.
**Raison** : Centralisation = auditabilite, prevention des modifications concurrentes, UI event-driven triviale.
**Consequences** : Jamais modifier une stat directement. Passer TOUJOURS par SetStatValue.

### [07/05/2026] UI HUD -- zero polling
**Decision** : UI_HUD_Main entierement event-driven via OnStatChanged. Zero Tick polling.
**Raison** : Performance + architecture propre. Le HUD ne sait pas quand les stats changent, il reagit.
**Consequences** : Toute nouvelle stat affichee dans le HUD doit passer par OnStatChanged.

### [18/05/2026] ComboManager -- HandleAttack sans parametre ChoosenWeapon
**Contexte** : HandleAttack prenait ChoosenWeapon en parametre.
**Decision** : Supprimer le parametre. Le ComboManager lit CurrentWeaponID en interne.
**Raison** : Single source of truth. Le ComboManager gere son propre etat d'arme via InitComboTree.
**Consequences** : EquipWeapon appelle InitComboTree(WeaponID, WeaponLevel). Aucun appel externe ne passe l'arme a HandleAttack.

---

## ASSETS & PIPELINE

### [11/05/2026] AnimGraph via MCP -- INTERDIT
**Decision** : Ne jamais creer d'etat AnimGraph via l'outil add_state du MCP.
**Raison** : add_state produit des shells corrompus non utilisables dans l'editeur.
**Consequences** : Toute creation d'etat AnimGraph = manuelle dans l'editeur UE5.7. Regle absolue pour l'agent UnrealClaude.

### [14/05/2026] LevelMin DT_Combo -- valeur 0
**Decision** : LevelMin = 0 sur toutes les rows DT_Combo (pas 1).
**Raison** : Le niveau de base est 0. Une valeur 1 excluait les armes non upgradees du combo.
**Consequences** : Toute nouvelle row DT_Combo doit avoir LevelMin = 0 par defaut.

---

## Historique

- Creation : 21/05/2026
- Derniere mise a jour : 23/05/2026 -- architecture ennemis sans WeaponClass, magie ennemie point ouvert
