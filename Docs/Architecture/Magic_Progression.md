# Magic_Progression.md — Design Progression Magique

## Objectif

Définir la boucle de progression magique du joueur : comment les sorts évoluent,
comment les déités débloquent les paliers d'arbre, et comment le joueur rattrape
les sorts sous-évolués en fin de jeu.

Dernière mise à jour : 26/05/2026

---

## 1. Progression par usage

### Principe
Chaque sort monte en niveau via l'usage en combat. Les seuils sont différenciés
par **rôle du sort**, pas par sort individuel, pour refléter la fréquence d'usage
naturelle sans forcer le grind.

### Seuils par rôle (ordre croissant)
| Rôle | Seuil | Rationale |
|---|---|---|
| Attack | Bas | Utilisé naturellement à chaque combat |
| Heal | Moyen | Utilisé situationnellement |
| Buff | Moyen-haut | Souvent négligé par le joueur |
| Debuff | Haut | Le moins utilisé naturellement |

> **Valeurs exactes : à calibrer** selon la durée de vie visée du jeu.

### Inspiration
Système Secret of Mana : `9 - niveau actuel` % par lancer (courbe décroissante).
SoM adapte ce principe avec des seuils différenciés par rôle plutôt qu'une formule unique.

---

## 2. Cap narratif — Déblocage par quêtes de déité

### Structure de déblocage
1. **Rencontrer une déité** → sorts de base débloqués immédiatement
2. **Compléter la quête de déité** → paliers d'arbre de talents débloqués

### Paliers débloqués par quête
- Nombre variable selon la déité / difficulté de la quête : 2, 3 ou 4 paliers
- Exemple pressenti : Lumina (déité introductive) = 2 paliers

### Points ouverts
- Nombre exact de paliers par quête : fixe ou variable ? → à décider
- Structure des quêtes (narrative, épreuve thématique liée à la déité, mixte) → session Lore
- Timing de disponibilité : dès la rencontre ou après avancement histoire principale ? → session Lore
- Ordre de déblocage des déités → **session Lore dédiée**

---

## 3. Système de rattrapage (fin de jeu)

### Principe
En fin de jeu, le joueur peut accélérer la progression de sorts sous-évolués
via un coût dédié, sans casser la progression naturelle en early/mid game.

### Format envisagé
- Objet spécifique lié à la magie, monnaie dédiée, ou les deux selon la rareté
- **À nommer et définir** dans un jalon dédié

---

## 4. Points ouverts globaux

| Sujet | Statut | Jalon cible |
|---|---|---|
| Ordre de déblocage des déités | Ouvert | Session Lore |
| Structure quêtes de déité | Ouvert | Session Lore |
| Calibration seuils d'usage par rôle | Ouvert | C1-MagicUnlockSystem |
| Nombre de paliers débloqués par quête | Ouvert | À décider |
| Nom et format du système de rattrapage | Ouvert | Jalon dédié |
| Structure de l'arbre de talents | Ouvert | Jalon dédié arbre |

---

## Références
- `Docs/Architecture/Magic_System.md` : architecture technique BP_MagicComponent
- `Docs/Architecture/Decisions.md` : décisions d'abandon et choix archi
- `Docs/Roadmap_Gameplay.md` : jalons magie
