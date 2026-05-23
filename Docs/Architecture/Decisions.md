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
**Point ouvert -- Magie ennemie** : les ennemis capables de magie s'appuieront probablement
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
**Decision** : 5 IMC distincts, chacun a une responsabilite unique :

| IMC | Contenu | Mode |
|---|---|---|
| IMC_Gameplay | Move, Look, Jump, Dodge, Sprint, LockOn, Attack, Block, RadialOpen, Quickslots | Exclusif (base permanente) |
| IMC_Radial | Rotate, Validate, Cancel, ChangeCat | Exclusif (remplace Gameplay pendant radial) |
| IMC_Menu | Navigate, Confirm, Back | Exclusif (pause, mort, main menu) |
| IMC_Dialogue | Confirm/Avance, Choix | CUMULATIF avec IMC_Gameplay |
| IMC_Cutscene | IA_Skip | Exclusif |

**Raison** : Voir detail complet dans historique 23/05.
**Consequences** :
- IMC_Prototype renomme IMC_Gameplay dans C1-InputsUI
- OpenRadial : Remove IMC_Gameplay -> Add IMC_Radial (priority 1)
- CloseRadial : Remove IMC_Radial -> Add IMC_Gameplay (priority 0)

### [23/05/2026] IA Radial -- audit noms reels (correction doc)
**Correction** :
- `IA_UI_RadialMenu_ChangeCat` -> reel : `IA_UI_Radial_ChangeCat`
- `IA_RadialMenu` -> reel : `IA_UI_Radial_Open`
- Nouvelle IA identifiee : `IA_UI_Radial_Rotate`

### [07/05/2026] Source unique InputActions
**Decision** : Toutes les IA dans Content/Input/InputActions/ uniquement.
**Consequences** : Ne jamais creer d'IA en dehors de ce dossier.

---

## RADIAL MENU & MAGIE

### [23/05/2026] Radial Magie -- decisions actees pour C1-RadialMagie
**Contexte** : Choix d'architecture pour les 2 niveaux magie du radial.

**Decision 1 -- Validation N2 = CastSpell direct.**
Raison : L'assignation quickslot se fait hors combat via le menu general uniquement.
Le radial en combat = acces rapide pour lancer, pas pour organiser.
Consequences : ValidateSelectedSpell -> CastSpell(SpellID) via MagicComponent. Pas de logique d'assignation dans le radial.

**Decision 2 -- Source de verite ecoles = filtrage UnlockedSpells par ecole.**
Raison : Les ecoles se debloquent implicitement en apprenant un premier sort.
Ce modele est coherent avec une progression ou les sorts d'une meme ecole peuvent s'apprendre
a des niveaux differents (pas forcement tous en meme temps).
Pas de variable UnlockedSchools separee a maintenir.
Consequences : PopulateMagicSchools = loop sur UnlockedSpells -> extraire Category -> dedupliquer -> generer slots N1.
Une ecole disparait automatiquement du radial si tous ses sorts sont retires (cas edge, pas prioritaire).

**Decision 3 -- SelectedIndex arme = dette separee (C1-CleanupDettes).**
Raison : Fix mineur, ne bloque pas C1-RadialMagie. Sera traite avec LockOnSwitchCooldown PC.
Consequences : Ajoute a la liste C1-CleanupDettes.

**Point ouvert -- Magie ennemie.**
Les ennemis magiques utiliseront probablement DT_Spells (ou sous-ensemble) du hero.
Decision reportee a C2 quand un premier ennemi magique sera concu.

### [21/05/2026] Architecture Radial Magie -- 2 niveaux imbriques
**Decision** : N1 = ecoles (Lumina, Ondine, Ombre, Athanor, Sylphide, Gnome, Salamandre, Dryade) / N2 = sorts de l'ecole.
Navigation B = retour N2->N1, pas fermeture directe.

### [21/05/2026] SelectedIndex radial -- retour sur arme equipee (DETTE C1-CleanupDettes)
**Decision** : SelectedIndex doit pointer sur ChoosenWeapon dans DiscoveredWeapons a l'ouverture.
**Consequences** : Lookup ChoosenWeapon -> FindIndex dans DiscoveredWeapons. A traiter dans C1-CleanupDettes.

### [13/05/2026] Slow-mo radial -- Time Dilation 0.2
**Decision** : Time Dilation 0.2 a l'ouverture. CloseRadialMenu doit toujours restaurer a 1.0.

---

## MAGIE -- PROGRESSION

### [23/05/2026] Montee de niveau des magies -- jalon design dedie
**Contexte** : Sujet ouvert : montee en puissance des sorts (lineaire simple ou arbre de talent).
**Decision** : Aucune implementation pour l'instant. Creer le jalon C1-MagicProgressionDesign (spec uniquement).
**Raison** : Question de game design non triviale. Merite une session de design dediee avant de coder quoi que ce soit.
**Consequences** : C1-MagicProgressionDesign ajoute a la roadmap apres C1-RadialMagie.
Aucune variable "niveau de sort" a creer avant cette session.

### [23/05/2026] UnlockedSpells -- stub test BeginPlay + dette systeme de deblocage
**Contexte** : UnlockedSpells (TMap<FName, FSoM_DeitySpells> sur BP_MagicComponent) n'est jamais alimente
au runtime. Les sorts Lumina existent dans DT_Spells mais aucun systeme ne les debloque.
Pour valider C1-RadialMagie en PIE, il faut que le radial ait des donnees a afficher.
**Decision** : Ajouter un remplissage test au BeginPlay de BP_MagicComponent :
  - Key = "Lumina", Value = FSoM_DeitySpells{ SpellIDs = ["Lumina_Heal", "Lumina_Attack", "Lumina_Buff", "Lumina_Debuff"] }
Ce stub est temporaire et sera retire quand le vrai systeme de deblocage existera.
**Raison** : Pragmatisme -- valider le radial sans attendre C1-MagicProgressionDesign.
**Consequences -- DETTE (C1-MagicUnlockSystem)** :
- Creer un systeme de deblocage de sorts (appel a une fonction UnlockSpell(SchoolID, SpellID) sur MagicComponent)
- Chaque nouvelle ecole ou sort appris doit passer par cette fonction
- Si de nouvelles ecoles sont creees (Ondine, Ombre...), elles doivent avoir leur DT_Spells dedie
  ET leurs SpellIDs doivent etre enregistres via UnlockSpell -- pas en dur dans BeginPlay
- Retirer le stub BeginPlay test quand UnlockSpell est opere en jeu
- Ce jalon C1-MagicUnlockSystem est a planifier apres C1-MagicProgressionDesign

---

## GAMEPLAY & NARRATION

### [23/05/2026] Dialogues quetes annexes -- personnage mobile
**Decision** : Personnage mobile pendant les dialogues de quetes annexes.
IMC_Dialogue = cumulatif avec IMC_Gameplay (priority 1).
Distance check via Blueprint, pas via inputs. Detail a definir en C4-DialogueSystem.

---

## SYSTEME DE STATS & COMBAT

### [07/05/2026] SetStatValue -- unique point de modification
**Decision** : SetStatValue(StatName, Value) = UNIQUE point de modification de toutes les stats.
OnStatChanged = dispatcher de notification.
**Consequences** : Jamais modifier une stat directement.

### [07/05/2026] UI HUD -- zero polling
**Decision** : UI_HUD_Main entierement event-driven via OnStatChanged. Zero Tick polling.

### [18/05/2026] ComboManager -- HandleAttack sans parametre ChoosenWeapon
**Decision** : ComboManager lit CurrentWeaponID en interne. Pas de parametre externe.
**Consequences** : EquipWeapon appelle InitComboTree(WeaponID, WeaponLevel).

---

## ASSETS & PIPELINE

### [11/05/2026] AnimGraph via MCP -- INTERDIT
**Decision** : Ne jamais creer d'etat AnimGraph via l'outil add_state du MCP.
**Raison** : add_state produit des shells corrompus non utilisables.
**Consequences** : Toute creation d'etat AnimGraph = manuelle dans l'editeur UE5.7. Regle absolue.

### [14/05/2026] LevelMin DT_Combo -- valeur 0
**Decision** : LevelMin = 0 sur toutes les rows DT_Combo (pas 1).
**Consequences** : Toute nouvelle row DT_Combo doit avoir LevelMin = 0 par defaut.

---

## Historique

- Creation : 21/05/2026
- 23/05/2026 : architecture IMC, dialogues mobiles, correction noms IA
- 23/05/2026 : architecture ennemis sans WeaponClass
- 23/05/2026 : decisions C1-RadialMagie actees (CastSpell direct, filtrage UnlockedSpells, SelectedIndex en dette)
- 23/05/2026 : jalon C1-MagicProgressionDesign cree (design uniquement)
- 23/05/2026 : stub test UnlockedSpells BeginPlay + dette C1-MagicUnlockSystem
