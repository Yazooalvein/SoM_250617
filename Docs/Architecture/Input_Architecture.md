# Architecture Technique -- Systeme d'Entree & Controles

---

## Objectif du module

Centraliser la gestion des entrees :
- Enhanced Input (gamepad PS5, clavier/souris)
- Mapping contextuel : gameplay, menus, radial
- Regles de priorisation, isolation des contextes

---

## ETAT ACTUEL (21/05/2026)

### IMC actifs
- `IMC_Prototype` : inputs gameplay -- ACTIVE en jeu
- `IMC_UI` : inputs menus -- A CREER (C1-InputsUI)

### Probleme identifie
- IMC_Prototype trop chargee : inputs menus (radial) et gameplay cohabitent
- Pendant l'ouverture du radial, les inputs gameplay restent actifs
- Solution : creer IMC_UI, switcher au Open/CloseRadialMenu

---

## Composants principaux

- `IMC_Prototype` : InputMappingContext gameplay (source actuelle)
- `IMC_UI` : InputMappingContext menus (a creer -- C1-InputsUI)
- Source unique InputActions : `Content/Input/InputActions/`
- `BP_SoM_PlayerController` : consommateur principal (IA_Look, IA_LockOn, radial)
- `BP_SoM_HeroCharacter` : consommateur secondaire (IA_Move, IA_Jump, IA_Attack...)

---

## InputActions existantes

| InputAction | Usage | IMC cible |
|---|---|---|
| IA_Move | Deplacement | IMC_Prototype |
| IA_Look | Camera (souris + gamepad) | IMC_Prototype |
| IA_Jump | Saut | IMC_Prototype |
| IA_Dodge | Dash / Roll | IMC_Prototype |
| IA_Sprint | Sprint | IMC_Prototype |
| IA_LockOn | Verrouillage cible | IMC_Prototype |
| IA_Attack_Light | Attaque legere | IMC_Prototype |
| IA_Attack_Heavy | Attaque lourde | IMC_Prototype |
| IA_Block | Parade | IMC_Prototype |
| IA_RadialMenu | Ouvre/ferme le radial | IMC_Prototype |
| IA_Quickslot_Up | Quickslot haut | IMC_Prototype |
| IA_Quickslot_Left | Quickslot gauche | IMC_Prototype |
| IA_Quickslot_Right | Quickslot droite | IMC_Prototype |
| IA_UI_Radial_Cancel | Annuler / retour radial | -> IMC_UI (a migrer) |
| IA_validate_radial_selection | Valider selection radial | -> IMC_UI (a migrer) |
| IA_UI_RadialMenu_ChangeCat | Changer categorie radial | -> IMC_UI (a migrer) |

---

## Mapping Gamepad PS5 (ACTE)

```
X        = Saut
Carre    = Esquive / Roll
Rond     = Blocage
Triangle = Ouvre Radial (hold)
L1       = Attaque legere
R1       = Attaque forte
L3       = Sprint
R3       = Lock-On (appui) / Switch cible (axis)
Fl. Haut / Gauche / Droite = Quickslots 1/2/3
Fl. Bas  = Switch page quickslot
Options  = Menu Global
Stick G  = Deplacement / Rotation plateau radial
Stick D  = Camera / Axe switch cible lock-on
```

---

## C1-InputsUI -- plan d'implementation

1. Creer `IMC_UI` dans Content/Input/
2. Y migrer : IA_UI_Radial_Cancel, IA_validate_radial_selection, IA_UI_RadialMenu_ChangeCat
3. Retirer ces 3 IA de IMC_Prototype
4. Dans BP_SoM_PlayerController, OpenRadialMenu :
   - Remove IMC_Prototype
   - Add IMC_UI
5. Dans CloseRadialMenu :
   - Remove IMC_UI
   - Add IMC_Prototype
6. Tester : inputs gameplay bloques pendant radial, repris apres fermeture
7. Point ouvert : Quickslot switch (press = utiliser, hold = changer de page ?)

---

## Notes importantes

- IA_Look est dans le PC depuis J-Camera (pas dans HeroCharacter)
- Toutes les IA sont dans Content/Input/InputActions/ (source unique)
- Ne pas creer d'IA en dehors de ce dossier
- IMC_Prototype = gameplay only apres C1-InputsUI
- add_state MCP dans AnimGraph = shell corrompu garanti (rappel agent)

---

## Roadmap locale

- [x] Unification inputs (suppression vestiges ThirdPerson)
- [x] Source unique Content/Input/InputActions/
- [x] IA_Look deplace dans PC (J-Camera)
- [ ] C1-InputsUI : IMC_UI + switch au open/close radial
- [ ] Compatibilite future autres devices si besoin

---

## Liens

- RadialMenu_Architecture.md
- LockOn_Architecture.md
- Journal_Modifications.md

---

## Historique

- Creation : 17/06/2025
- Derniere mise a jour : 21/05/2026 -- ajout IMC_UI plan + mapping PS5 complet
