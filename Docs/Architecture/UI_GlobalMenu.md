# UI Global Menu -- Shadow of Mana

Document d'architecture et de design pour le menu global du jeu.
A completer au fur et a mesure des sessions de design.

---

## Vision generale

Menu global accessible via bouton Options en jeu.
Style sobre, mix Dark Souls / Kingdom Hearts -- lisible, pas encombre.
PC/Console uniquement (pas de mobile).
Pause le jeu a l'ouverture (ou Time Dilation 0 ? -- point ouvert).

---

## Mapping Gamepad PS5 -- ACTE

```
Croix (X)      : Saut
Carré          : Esquive / Dash
Rond           : Blocage
Triangle       : Ouvrir Radial Menu

L1             : Attaque légère
R1             : Attaque forte
L2             : Action PNJ compagnon 1
R2             : Action PNJ compagnon 2

L3 (stick G)   : Sprint
R3 (stick D)   : Lock-On (axis R3 = changement de cible)

Flèche ↑       : Quickslot 1
Flèche ←       : Quickslot 2
Flèche →       : Quickslot 3
Flèche ↓       : Switch page quickslots (A/B/C...)

Options        : Menu Global
Touchpad       : ? (carte / journal -- a definir)
```

---

## Structure du menu global (onglets)

### 1. Personnage / Stats
- Stats actuelles (HP max, ST max, MP max, Degats, Defense...)
- Points de stats disponibles (issus du level up)
- Distribution des points

### 2. Arbre de Talent
- Par type d'arme (Epee, Arc, Fléau, Lance...)
- Points de talent debloques par usage de l'arme (pas par level general)
- Branches : degats / vitesse / effets speciaux
- Lie a l'evolution forge

### 3. Inventaire
- Objets ramasses / consommables
- Materiaux de forge
- Cles / objets narratifs

### 4. Equipement
- Slots : armure, casque, gantelets, accessoires (x2 ?)
- Bonus % sur stats (ex: +10% HP, +5% MP...)
- Apercu visuel du personnage equipe ? (point ouvert)

### 5. Magie
- Liste des sorts debloques par divinite
- 4 sorts par ecole de magie (Attack, Buff, Debuff, Heal)
- Details : ManaCost, Cooldown, effet
- Attribution quickslot depuis cet onglet

### 6. Configuration Quickslots
- Attribution des 3 slots par page
- Switch de page via Fleche bas
- Version actuelle J-13 : 1 page x 3 slots
- Evolution prevue : multi-pages (sorts / objets / autre)

### 7. Journal
- Epopee (quete principale) : toujours visible, progression
- Quetes annexes : liste complete, choisir quelle quete "suivre"
  - 1 seule quete annexe suivie a la fois (affichee dans HUD a la demande)
- Lore / documents trouves dans le monde ? (point ouvert)

### 8. Carte
- Minimap etendue / carte du monde
- Marqueurs de quetes, PNJ importants, points d'interet
- A designer quand un vrai niveau existe

### 9. Configuration
- Parametres graphiques, audio, commandes
- Remapping des touches ? (point ouvert)

---

## HUD permanent

Toujours visible en jeu :

```
┌─────────────────────────────────────────┐
│ [Arme]  HP ████░░  ST ████░░  MP ███░░  │
│         [Q1] [Q2] [Q3]  [page]          │
│                              [Minimap]  │
└─────────────────────────────────────────┘
```

- HP / ST / MP : deja fait ✅
- Arme equipee : slot HUD deja prevu ✅
- Quickslotbar 1x3 : J-13 en cours
- Indicateur page active quickslot : a prevoir
- Minimap : a prevoir (apres vrai niveau)
- Indicateur compagnon actif (portrait + HP) : J-20+
- Indicateur corruption : J-24+

---

## HUD a la demande

Overlay declenche par bouton dedie (sans pause) :
- **Quetes** : Epopee en haut + quete annexe suivie en dessous
- **Minimap etendue** : agrandissement de la minimap

---

## HUD contextuel (en combat)

- Barres HP ennemis : a revoir avec refonte Lock-On
- Feedback combo : subtil, dans le monde (flash arme, posture) -- pas d'UI visible ✅ ACTE
- Lock-On indicator : a revoir (logique + UI, jalon dedie)

---

## Quickslotbar -- detail

### Version actuelle (J-13) : 1x3
- 3 slots : fleches ↑ ← →
- Contenu : sorts et/ou objets
- Attribution depuis menu global onglet "Configuration Quickslots"
- Fleche ↓ : switch de page

### Design strategique acte
- 4 sorts par ecole (Attack/Buff/Debuff/Heal) mais seulement 3 quickslots
- Force l'anticipation avant le combat -- choix strategique delibere
- Pas de "tout avoir sous la main" -- tension et preparation

### Evolution prevue : multi-pages
- Page A : sorts actifs
- Page B : consommables / objets
- Page C+ : a definir selon besoins
- Switch via Fleche bas (cycle entre pages)

---

## Lock-On -- dette technique

Problemes identifies :
- **Logique** : ne detecte pas les nouveaux ennemis entrant dans le radius sans reset manuel
- **UI** : indicateur en premier plan devant le heros (z-order incorrect)
- **UI** : barres HP ennemis mal positionnees
- Evaluation necessaire : migrer / refactoriser / refaire from scratch ?

Actions a prevoir (jalon dedie J-lock, entre J-13 et J-15) :
- Audit complet du systeme existant
- Revoir detection cibles (PawnSensing ou overlap continu ?)
- Corriger z-order indicateur lock
- Revoir positionnement barres HP ennemis

---

## Points de design encore ouverts

- Menu global : pause complete (Time Dilation 0) ou jeu continue ?
- Equipement : apercu visuel du personnage ou liste seule ?
- Journal : section Lore / documents narratifs ?
- Remapping touches : prevu ou pas ?
- Touchpad PS5 : carte, journal, ou autre ?
- Quickslot : press = utiliser, hold = switcher de page ?

---

## Jalons associes

| Jalon | Contenu |
|-------|---------|
| J-13 | Quickslotbar 1x3 (en cours) |
| J-lock | Revision Lock-On logique + UI |
| J-15+ | Refonte armes -> impacte onglet Equipement |
| J-24+ | Corruption -> indicateur HUD |
| J-27+ | Quetes -> Journal + HUD a la demande |
| J-30+ | Stats / Arbre de talent -> onglets Personnage + Talent |
| TBD | Menu global complet |

---

## Historique

- Creation : 13/05/2026
- Derniere mise a jour : 13/05/2026
