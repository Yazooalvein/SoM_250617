# Magic_Progression.md - Design Progression Magique

## Objectif

Definir la boucle de progression magique du joueur : comment les sorts evoluent,
comment les deites debloquent les paliers d'arbre, et comment le joueur rattrape
les sorts sous-evolues en fin de jeu.

Derniere mise a jour : 26/05/2026

---

## 1. Progression par usage

### Principe
Chaque sort monte en niveau via l'usage en combat. Les seuils sont differencies
par role du sort, pas par sort individuel, pour refleter la frequence d'usage
naturelle sans forcer le grind.

### Seuils par role (ordre croissant)
| Role | Seuil | Rationale |
|---|---|---|
| Attack | Bas | Utilise naturellement a chaque combat |
| Heal | Moyen | Utilise situationnellement |
| Buff | Moyen-haut | Souvent neglige par le joueur |
| Debuff | Haut | Le moins utilise naturellement |

Valeurs exactes : a calibrer selon la duree de vie visee du jeu.

### Inspiration
Systeme Secret of Mana : 9 - niveau actuel % par lancer (courbe decroissante).
SoM adapte ce principe avec des seuils differencies par role plutot qu'une formule unique.

---

## 2. Cap narratif - Deblocage par quetes de deite

### Structure de deblocage - 4 paliers sequentiels

| Palier | Declencheur | Recompense |
|---|---|---|
| 0 - Rencontre | Evenement narratif (rencontre la deite / son representant) | Sorts de base debloques immediatement |
| 1 - Quete speciale | Quete narrative liee a la deite | Paliers arbre 1 et 2 debloques |
| 2 - Donjon de deite | Donjon specifique a la deite, rituel / priere de communion | Paliers arbre 3 et 4 debloques |
| 3 - Boss lore | Boss narrativement lie a la deite | Ultime debloque |

Ordre sequentiel obligatoire - sequencement narratif strict, pas de saut possible.

La communion avec la deite (acces au donjon) passe par un rituel ou une priere
propre a chaque sanctuaire - defini au cas par cas selon la deite et son identite.

### Points ouverts
- Ordre de deblocage des deites -> session Lore dediee
- Structure exacte des quetes et rituels par deite -> session Lore
- Cas particulier Ondine (statut ambigu, fusion soeur) -> session Lore

---

## 3. Corruption Magique

### Principe
L'usage de la magie accumule de la Corruption sur le heros. Effets principalement negatifs
et progressifs selon des seuils (legere / moderee / severe - a definir).

### Purge
Repos a la Fontaine de Fee -> Corruption purgee integralement.

### Twist - Representant d'Ombre
Le heros etant lie a la deite Ombre, il peut tirer parti de la Corruption a hauts niveaux :
- Bonus pressentis : augmentation des degats
- Contreparties pressenties : soins indisponibles, certaines interactions PNJ bloquees

Points ouverts : seuils exacts, reversibilite partielle hors Fontaine, reactions ennemis
face a un heros corrompu, impact visuel - a brainstormer en session dediee.

---

## 4. Systeme de rattrapage (fin de jeu)

### Principe
En fin de jeu, le joueur peut accelerer la progression de sorts sous-evolues
via un cout dedie, sans casser la progression naturelle en early/mid game.

### Format envisage
- Objet specifique lie a la magie, monnaie dediee, ou les deux selon la rarete
- A nommer et definir dans un jalon dedie (session Economie)

---

## 5. Points ouverts globaux

| Sujet | Statut | Jalon cible |
|---|---|---|
| Ordre de deblocage des deites | Ouvert | Session Lore |
| Structure quetes et rituels par deite | Ouvert | Session Lore |
| Cas Ondine (statut ambigu) | Ouvert | Session Lore |
| Calibration seuils d'usage par role | Ouvert | C1-MagicUnlockSystem |
| Seuils Corruption (legere/moderee/severe) | Ouvert | Session dediee Corruption |
| Nom et format systeme de rattrapage | Ouvert | Session Economie |
| Structure de l'arbre de talents | Ouvert | Jalon dedie arbre |

---

## References
- `Docs/Lore_ShadowOfMana.md` : lore complet, section Corruption Magique et Fontaine de Fee
- `Docs/Architecture/Magic_System.md` : architecture technique BP_MagicComponent
- `Docs/Architecture/Decisions.md` : decisions d'abandon et choix archi
- `Docs/Roadmap_Gameplay.md` : jalons magie
