# Weapons_Progression.md - Design Progression des Armes

## Objectif

Définir la boucle de progression des armes : montée en niveau par usage,
forge comme condition de déblocage de palier, et arbre de choix par arme.

Créé le : 30/05/2026

---

## 1. Progression par usage

### Principe
Chaque arme monte en niveau via l'usage en combat (nombre d'attaques portées).
Inspiration Secret of Mana : formule `9 - niveau actuel %` par usage (courbe décroissante),
identique au système magie.

### Structure de progression
- Niveau 1 → 2 : accessible dès le début, progression par usage
- Niveau 2 → 3+ : nécessite d'avoir forgé la version suivante de l'arme avant
  que l'XP commence à s'accumuler

### Parallèle avec la magie
| | Magie | Armes |
|---|---|---|
| Progression | Usage (par rôle) | Usage (par arme) |
| Cap de palier | Narratif (quête déité) | Forge (matériaux) |
| Récompense niveau | Sorts / paliers arbre | Choix dans arbre (stats/combos) |
| Rattrapage | Objet dédié (à définir) | Aucun |

---

## 2. Forge — Condition de déblocage

### Matériaux requis par forge
- **Drop commun x N** (mobs) : Minerai, Bois, etc. — type selon l'arme
- **Drop rare x 1** (Boss ou Récompense Narrative) : Essence de Mana, Graine de Mana, Esprit Mana, etc.

### Règle
Sans avoir forgé la version suivante, l'XP vers le niveau supérieur ne s'accumule pas.
La forge déverrouille l'accès au palier — la progression par usage fait le reste.

---

## 3. Arbre de progression par arme

### Structure
- Tous les X niveaux (à calibrer au playtest) : choix entre deux branches
- **Branche Combo** : nouveau step de combo, finisher, variante d'attaque
- **Branche Stat** : bonus de stat (dégâts, vitesse d'attaque, portée, etc.)
- D'autres types de choix possibles selon l'arme — à définir au cas par cas

### Philosophie
La dichotomie combo/stat crée une tension de gameplay naturelle :
- Joueur efficacité → stats
- Joueur exploration → combos et découvertes

Le contenu exact de chaque arbre est défini par arme dans un jalon dédié.

---

## 4. Accessibilité et end-game

### Principe
- ~50% des armes peuvent atteindre le niveau max naturellement via le jeu normal
- Les autres nécessitent des **quêtes annexes haut level**

### Quêtes annexes haut level
- Récompense : matériaux rares manquants (pas la forge complète directement)
- Le joueur garde le choix de quelle arme maxer avec les matériaux obtenus
- Crée une boucle end-game pour les completionnistes sans bloquer la progression principale

---

## 5. Points ouverts

| Sujet | Statut | Jalon cible |
|---|---|---|
| Valeur X (tous les X niveaux = choix arbre) | Ouvert | Calibrage/Playtest |
| Matériaux spécifiques par arme | Ouvert | Session Forge/Économie |
| Contenu exact de chaque arbre par arme | Ouvert | Jalon dédié par arme |
| Nombre de niveaux max par arme | Ouvert | Session Forge/Économie |
| Formule XP exacte (calibration) | Ouvert | C1-MagicUnlockSystem (mutualisé) |

---

## Références
- `Docs/Architecture/Magic_Progression.md` : système parallèle magie
- `Docs/Architecture/Weapons_System_Architecture.md` : architecture technique armes
- `Docs/Architecture/Decisions.md` : décisions d'architecture
