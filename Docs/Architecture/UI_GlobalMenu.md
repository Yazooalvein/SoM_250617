# UI Global Menu -- Shadow of Mana

Document d'architecture et de design pour le menu global du jeu.
A completer au fur et a mesure des sessions de design.

---

## Vision generale

Menu global accessible via bouton Start/Options en jeu.
Style sobre, mix Dark Souls / Kingdom Hearts -- lisible, pas encombre.
PC/Console uniquement (pas de mobile).
Pause le jeu a l'ouverture (ou Time Dilation 0 ?).

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
- Apercu visuel du personnage equipe ?

### 5. Magie
- Liste des sorts debloques par divinite
- Details : ManaCost, Cooldown, effet
- Pas de gestion depuis ce menu (attribution quickslot seulement)

### 6. Configuration Quickslots
- Attribution des 3 slots (page 1 : sorts, page 2 : objets)
- Switch dynamique entre pages via L1/LB (a definir)
- Version actuelle : 1x3, evolution prevue : 2x3

### 7. Journal
- Epopee (quete principale) : toujours visible, progression
- Quetes annexes : liste complete, choisir quelle quete "suivre"
  - La quete suivie s'affiche dans le HUD a la demande (sous l'epopee)
- Lore / documents trouves dans le monde ?

### 8. Carte
- Minimap etendue / carte du monde
- Marqueurs de quetes, PNJ importants, points d'interet
- A designer quand un vrai niveau existe

### 9. Configuration
- Parametres graphiques, audio, commandes
- Remapping des touches ?

---

## HUD permanent (rappel)

Toujours visible en jeu :

```
┌─────────────────────────────────────────┐
│ [Arme]  HP ████░░  ST ████░░  MP ███░░  │
│         [Q1] [Q2] [Q3]                  │
│                              [Minimap]  │
└─────────────────────────────────────────┘
```

- HP / ST / MP : deja fait ✅
- Arme equipee : slot HUD deja prevu ✅
- Quickslotbar : J-13 en cours
- Minimap : a prevoir (apres vrai niveau)
- Indicateur compagnon actif : J-20+
- Indicateur corruption : J-24+

---

## HUD a la demande

Overlay declenche par bouton dedie (pas de pause) :

- **Quetes** : Epopee en haut + quete annexe suivie en dessous
- **Minimap etendue** : agrandissement de la minimap

---

## HUD contextuel (en combat)

- Barres HP ennemis : a revoir avec refonte Lock-On
- Feedback combo : subtil, dans le monde (flash arme, posture) -- pas d'UI visible
- Lock-On indicator : a revoir (logique + UI, jalon dedie)

---

## Quickslotbar -- detail

### Version actuelle (J-13) : 1x3
- 3 slots horizontaux
- Contenu : sorts et/ou objets
- Attribution depuis le menu global onglet "Configuration Quickslots"

### Evolution prevue : 2x3
- Page 1 : sorts actifs
- Page 2 : consommables / objets
- Switch via L1/LB (a confirmer)
- Declenchement : press = utiliser, hold = switcher de page ? (a definir)

---

## Lock-On -- dette technique

Problemes identifies :
- **Logique** : ne detecte pas les nouveaux ennemis entrant dans le radius sans reset manuel
- **UI** : indicateur en premier plan devant le heros (z-order incorrect)
- **UI** : barres HP ennemis mal positionnees

Actions a prevoir (jalon dedie entre J-13 et J-15) :
- Revoir la detection des cibles (PawnSensing ou overlap continu ?)
- Migrer / refactoriser / refaire from scratch ? (a evaluer)
- Corriger z-order de l'indicateur lock
- Revoir positionnement barres HP ennemis

---

## Points de design encore ouverts

- Menu global : pause complete (Time Dilation 0) ou jeu continue ?
- Equipement : apercu visuel du personnage equipe ou liste seule ?
- Journal : section Lore / documents narratifs a inclure ?
- Quickslot switch : L1/LB confirme ? Hold vs Press ?
- Remapping touches : prevu ou pas ?
- Nombre max de quetes annexes suivables : 1 seule ou plusieurs ?

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
