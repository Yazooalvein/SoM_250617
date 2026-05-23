# Architecture Technique -- Systeme d'Entree & Controles

---

## Objectif du module

Centraliser la gestion des entrees :
- Enhanced Input (gamepad PS5, clavier/souris)
- Mapping contextuel par IMC dedie
- Regles de priorisation, cumul ou exclusivite selon le contexte

---

## ETAT ACTUEL (23/05/2026) -- C1-InputsUI VALIDE PIE

### IMC actifs
- `IMC_Gameplay` : inputs gameplay -- ACTIF (charge au ReceivePossessed dans BP_SoM_HeroCharacter)
- `IMC_Radial` : navigation radial -- ACTIF, swap dans OpenRadial/CloseRadial
- `IMC_Menu` : stub vide -- cable en C7
- `IMC_Dialogue` : stub vide -- cable en C4
- `IMC_Cutscene` : stub vide -- cable en C3

### Charge initiale
- `BP_SoM_HeroCharacter` -> `ReceivePossessed` -> IsPlayerController -> Cast -> GetSubsystemFromPC -> AddMappingContext(IMC_Gameplay, Priority=0)
- Chemin asset : `/Game/Input/InputMappings/IMC_Gameplay`

---

## Architecture IMC (decidee le 23/05/2026)

### Vue d'ensemble

| IMC | Contenu | Mode d'activation | Statut |
|---|---|---|---|
| `IMC_Gameplay` | Tout le gameplay (voir liste) | Exclusif -- base permanente | VALIDE PIE |
| `IMC_Radial` | Navigation radial (4 IA) | Exclusif -- remplace Gameplay | VALIDE PIE |
| `IMC_Menu` | Navigate, Confirm, Back | Exclusif -- menus uniquement | Stub / cable C7 |
| `IMC_Dialogue` | Confirm/Avance, Choix | **CUMULATIF** avec Gameplay | Stub / cable C4 |
| `IMC_Cutscene` | IA_Skip | Exclusif | Stub / cable C3 |

**IMC_Forge** et **IMC_Map** : points ouverts, decision reportee a C5/C3.

### Distinction cle : Exclusif vs Cumulatif
- **Exclusif** : Remove IMC_Gameplay -> Add IMC_X. Gameplay bloque pendant le contexte.
- **Cumulatif** : Add IMC_X par-dessus IMC_Gameplay (priority superieure). Les deux actifs en meme temps.
- `IMC_Dialogue` est le SEUL contexte cumulatif car le personnage peut bouger pendant les dialogues.

---

## IMC_Gameplay -- contenu complet

| InputAction | Bouton PS5 | Usage |
|---|---|---|
| IA_Move | Stick G | Deplacement |
| IA_Look | Stick D | Camera |
| IA_Jump | X | Saut |
| IA_Dodge | Carre | Dash / Roll |
| IA_Sprint | L3 | Sprint |
| IA_LockOn | R3 (appui) | Verrouillage cible |
| IA_LockOn (axis) | R3 (axis) | Switch cible |
| IA_Attack_Light | L1 | Attaque legere |
| IA_Attack_Heavy | R1 | Attaque forte |
| IA_Block | Rond | Parade |
| IA_UI_Radial_Open | Triangle (hold) | Ouvre le radial |
| IA_Quickslot_Up | Fl. Haut | Quickslot 1 |
| IA_Quickslot_Left | Fl. Gauche | Quickslot 2 |
| IA_Quickslot_Right | Fl. Droite | Quickslot 3 |

Note : `IA_UI_Radial_Open` reste dans IMC_Gameplay (doit etre actif en jeu pour declencher l'ouverture).

---

## IMC_Radial -- contenu complet (VALIDE PIE)

| InputAction | Bouton PS5 / Clavier | Trigger | Modifiers | Usage |
|---|---|---|---|---|
| IA_UI_Radial_Rotate | Stick G X+ / D | Pressed, threshold 0.5 | Aucun | Rotation droite |
| IA_UI_Radial_Rotate | Stick G X- / Q | Pressed, threshold 0.5 | Negate X | Rotation gauche |
| IA_UI_Radial_Validate | Croix / C | Pressed | - | Valider selection |
| IA_UI_Radial_Cancel | Rond / B | Pressed | - | Annuler / fermer |
| IA_UI_Radial_ChangeCat | Stick G Y / Z+S | Pressed, threshold 0.5 | - | Changer categorie |

**Fix rotation** : le Negate X sur le binding gauche est OBLIGATOIRE.
Sans lui, Q et D envoient la meme valeur positive -> meme direction de rotation.

Swap dans BP_SoM_PlayerController :
- `OpenRadial` (apres SET bShowMouseCursor=true) :
  GetSubsystemFromPC(Self) -> RemoveMappingContext(IMC_Gameplay) -> AddMappingContext(IMC_Radial, Priority=1)
- `CloseRadial` (avant RemoveFromParent) :
  GetSubsystemFromPC(Self) -> RemoveMappingContext(IMC_Radial) -> AddMappingContext(IMC_Gameplay, Priority=0)

---

## IMC_Menu -- contenu prevu

| InputAction | Bouton PS5 | Usage |
|---|---|---|
| IA_UI_Navigate | Stick G / DPad | Navigation liste/grille |
| IA_UI_Confirm | X / Croix | Confirmer |
| IA_UI_Back | Rond / B | Retour / fermer |

Utilise par : Pause Menu, Ecran de mort, Main Menu. Cable en C7.

---

## IMC_Dialogue -- contenu prevu

| InputAction | Bouton PS5 | Usage |
|---|---|---|
| IA_Dialogue_Confirm | X / Croix | Avancer le dialogue |
| IA_Dialogue_Choice | Stick G Haut/Bas | Naviguer les choix moraux |

Mode CUMULATIF : s'ajoute par-dessus IMC_Gameplay (priority 1).
Le personnage continue a se deplacer pendant le dialogue.
Distance check Blueprint si trop loin du PNJ (seuil defini en C4-DialogueSystem).
Cable en C4.

---

## IMC_Cutscene -- contenu prevu

| InputAction | Bouton PS5 | Usage |
|---|---|---|
| IA_Skip | TBD | Passer le Level Sequence |

IA_Skip -> SequencePlayer->Stop() -> restore IMC_Gameplay. Cable en C3.

---

## Mapping Gamepad PS5 complet (ACTE)

```
X        = Saut / Confirmer (menus) / Valider radial
Carre    = Esquive / Roll
Rond     = Blocage / Retour (menus) / Cancel (radial)
Triangle = Ouvre Radial (hold)
L1       = Attaque legere
R1       = Attaque forte
L3       = Sprint
R3       = Lock-On (appui) / Switch cible (axis)
Fl. Haut / Gauche / Droite = Quickslots 1/2/3
Fl. Bas  = Switch page quickslot (point ouvert)
Options  = Menu Global
Stick G  = Deplacement / Rotation plateau radial (+ Negate gauche) / Navigation menus
Stick D  = Camera / Axe switch cible lock-on / Changement categorie radial
```

---

## Notes importantes

- IA_Look est dans le PC depuis J-Camera (pas dans HeroCharacter)
- Source unique : Content/Input/InputActions/ -- ne jamais creer d'IA ailleurs
- IMC charge au ReceivePossessed (HeroCharacter), pas au BeginPlay PC (pas de BeginPlay dans le PC)
- IMC_Dialogue est le SEUL IMC cumulatif du projet (voir Decisions.md)
- IA_UI_Radial_Rotate : OBLIGATOIRE Negate X sur le binding direction gauche
- Ne pas creer IMC_Combat, IMC_Swimming, IMC_Climbing (inutiles -- voir Decisions.md)
- Points ouverts : IMC_Forge (C5), IMC_Map (C3), seuil distance dialogue (C4)
- Point ouvert : Fl. Bas Quickslot = press utiliser ou hold changer page ?
- CloseRadial a un ErrorType=1 sur RemoveFromParent (reconnexion pin Target depuis RadialMainRef)

---

## Roadmap locale

- [x] Unification inputs (suppression vestiges ThirdPerson)
- [x] Source unique Content/Input/InputActions/
- [x] IA_Look deplace dans PC (J-Camera)
- [x] C1-InputsUI : IMC_Gameplay (ex IMC_Prototype), IMC_Radial cree et cable VALIDE PIE
- [x] C1-InputsUI : stubs IMC_Menu, IMC_Dialogue, IMC_Cutscene crees
- [x] C1-InputsUI : swap IMC dans OpenRadial / CloseRadial VALIDE PIE
- [ ] C4-DialogueSystem : cable IMC_Dialogue (cumulatif)
- [ ] C7 : cable IMC_Menu (pause, mort, main menu)
- [ ] C3 : cable IMC_Cutscene

---

## Liens

- Decisions.md (architecture IMC complete + raisons)
- RadialMenu_Architecture.md
- LockOn_Architecture.md

---

## Historique

- Creation : 17/06/2025
- MAJ 21/05/2026 : plan C1-InputsUI initial
- MAJ 23/05/2026 : architecture IMC complete (5 IMC), IMC_Dialogue cumulatif, correction noms IA
- MAJ 23/05/2026 : C1-InputsUI VALIDE PIE -- fix Negate X rotation, swap IMC OpenRadial/CloseRadial
