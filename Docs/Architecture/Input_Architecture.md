# Architecture Technique -- Systeme d'Entree & Controles

---

## Objectif du module

Centraliser la gestion des entrees :
- Enhanced Input (gamepad PS5, clavier/souris)
- Mapping contextuel par IMC dedie
- Regles de priorisation, cumul ou exclusivite selon le contexte

---

## ETAT ACTUEL (23/05/2026)

### IMC existants
- `IMC_Prototype` : inputs gameplay -- actif, A RENOMMER en IMC_Gameplay (C1-InputsUI)

### Probleme identifie
- IMC_Prototype trop chargee : inputs radial et gameplay cohabitent
- Inputs gameplay restent actifs pendant l'ouverture du radial
- Solution : architecture 5 IMC (voir ci-dessous)

---

## Architecture IMC cible (decidee le 23/05/2026)

### Vue d'ensemble

| IMC | Contenu | Mode d'activation | Jalon |
|---|---|---|---|
| `IMC_Gameplay` | Tout le gameplay (voir liste) | Exclusif -- base permanente | C1-InputsUI |
| `IMC_Radial` | Navigation radial (4 IA) | Exclusif -- remplace Gameplay | C1-InputsUI |
| `IMC_Menu` | Navigate, Confirm, Back | Exclusif -- menus uniquement | Stub C1 / cable C7 |
| `IMC_Dialogue` | Confirm/Avance, Choix | **CUMULATIF** avec Gameplay | Stub C1 / cable C4 |
| `IMC_Cutscene` | IA_Skip | Exclusif | Stub C1 / cable C3 |

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

## IMC_Radial -- contenu complet

| InputAction | Bouton PS5 | Usage |
|---|---|---|
| IA_UI_Radial_Rotate | Stick G (X) | Rotation plateau / selection |
| IA_validate_radial_selection | X / Croix | Valider selection |
| IA_UI_Radial_Cancel | Rond / B | Annuler / retour / fermer |
| IA_UI_Radial_ChangeCat | Stick D (Y) | Changer categorie (Armes<->Magie) |

Swap dans BP_SoM_PlayerController :
- `OpenRadial` : Remove IMC_Gameplay -> Add IMC_Radial (priority 1)
- `CloseRadial` : Remove IMC_Radial -> Add IMC_Gameplay (priority 0)

---

## IMC_Menu -- contenu prevu

| InputAction | Bouton PS5 | Usage |
|---|---|---|
| IA_UI_Navigate | Stick G / DPad | Navigation liste/grille |
| IA_UI_Confirm | X / Croix | Confirmer |
| IA_UI_Back | Rond / B | Retour / fermer |

Utilise par : Pause Menu, Ecran de mort, Main Menu.
Cable en C7. Stub a creer maintenant (IMC vide).

---

## IMC_Dialogue -- contenu prevu

| InputAction | Bouton PS5 | Usage |
|---|---|---|
| IA_Dialogue_Confirm | X / Croix | Avancer le dialogue |
| IA_Dialogue_Choice | Stick G Haut/Bas | Naviguer les choix moraux |

Mode CUMULATIF : s'ajoute par-dessus IMC_Gameplay (priority 1).
Le personnage continue a se deplacer pendant le dialogue.
Si le joueur s'eloigne trop du PNJ -> dialogue interrompu (distance check Blueprint, pas input).
Seuil de distance et relance : definis en C4-DialogueSystem.
Cable en C4. Stub a creer maintenant (IMC vide).

---

## IMC_Cutscene -- contenu prevu

| InputAction | Bouton PS5 | Usage |
|---|---|---|
| IA_Skip | N'importe quel bouton (TBD) | Passer la cinematique |

Cable en C3. Stub a creer maintenant (IMC vide).

---

## Mapping Gamepad PS5 complet (ACTE)

```
X        = Saut / Confirmer (menus)
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
Stick G  = Deplacement / Rotation plateau radial / Navigation menus
Stick D  = Camera / Axe switch cible lock-on / Changement categorie radial
```

---

## C1-InputsUI -- plan d'implementation

1. Renommer `IMC_Prototype` -> `IMC_Gameplay` (Fix Up Redirectors)
2. Creer `IMC_Radial` avec les 4 IA (voir tableau IMC_Radial)
3. Retirer ces 4 IA de `IMC_Gameplay`
4. Creer stubs vides : `IMC_Menu`, `IMC_Dialogue`, `IMC_Cutscene`
5. Ajouter variable `IMC_Gameplay` + `IMC_Radial` dans BP_SoM_PlayerController
6. Verifier/creer fonction `OpenRadial` (ErrorType=1 detecte dans ToggleRadial T3D)
7. Dans `OpenRadial` : Remove IMC_Gameplay -> Add IMC_Radial (priority 1)
8. Dans `CloseRadial` : Remove IMC_Radial -> Add IMC_Gameplay (priority 0)
9. PIE test :
   - Triangle -> inputs gameplay morts, radial naviguable
   - Rond -> fermeture, inputs gameplay reviennent
   - Attaque pendant radial ouvert -> rien
   - IA_UI_Radial_Open toujours fonctionnel depuis le gameplay

---

## Notes importantes

- IA_Look est dans le PC depuis J-Camera (pas dans HeroCharacter)
- Source unique : Content/Input/InputActions/ -- ne jamais creer d'IA ailleurs
- IMC_Dialogue est le SEUL IMC cumulatif du projet (voir Decisions.md)
- Ne pas creer IMC_Combat, IMC_Swimming, IMC_Climbing (inutiles -- voir Decisions.md)
- Points ouverts : IMC_Forge (C5), IMC_Map (C3), seuil distance dialogue (C4)
- Point ouvert : Fl. Bas Quickslot = press utiliser ou hold changer page ?

---

## Roadmap locale

- [x] Unification inputs (suppression vestiges ThirdPerson)
- [x] Source unique Content/Input/InputActions/
- [x] IA_Look deplace dans PC (J-Camera)
- [ ] C1-InputsUI : renommer IMC_Prototype, creer IMC_Radial, stubs IMC_Menu/Dialogue/Cutscene
- [ ] C1-InputsUI : swap IMC dans OpenRadial / CloseRadial
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
- MAJ 23/05/2026 : architecture IMC complete (5 IMC), IMC_Dialogue cumulatif, correction noms IA, plan implementation final
