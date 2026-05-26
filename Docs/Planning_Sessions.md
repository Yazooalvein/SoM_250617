# Planning Sessions — Shadow of Mana

Ordre de priorité des jalons techniques et sessions design.
Mis à jour à chaque session quand un jalon change de statut.

Dernière mise à jour : 26/05/2026

---

## Tableau de planification

| Ordre | Type | Jalon | Dépendances | Bloque |
|---|---|---|---|---|
| 1 | Tech | C1-MagicUnlockSystem | - | Magie complète |
| 2 | Tech | C1-CleanupDettes | - | Dette technique |
| 3 | Design | Stats/Progression personnage | - | Combat, forge, économie |
| 4 | Tech | C1-WeaponArchitecture | Stats | Forge, talents |
| 5 | Design | Corruption Magique | Stats | SaveDesign, Stats |
| 6 | Tech | C1-SwordMoveset | Stats, WeaponArchi | Combat complet |
| 7 | Design | SaveDesign | Stats, Corruption | C2-SaveGame |
| 8 | Design | Arbre de talents | Stats | MagicUnlock complet |
| 9 | Tech | C2-SaveGame | SaveDesign | Sauvegarde en jeu |
| 10 | Design | Économie | Stats, Forge | Forge en jeu |
| 11 | Tech | C1-BowPOC | Stats | Arc |
| 12 | Tech | C1-WeaponSwitching | WeaponArchi | Switch combat |
| 13 | Tech | C1-SFXCombat | - | Polish son |
| 14 | Design | Lore Déités | - | Contenu narratif |
| 15 | Design | Lore Fée | - | Contenu narratif |
| 16 | Tech | C1-AnimationsPass1 | - | Fin Cycle 1 |

---

## Logique générale

- Alterner tech et design pour ne jamais bloquer le code sur un manque de spec
- Les jalons 1 et 2 (MagicUnlockSystem + CleanupDettes) démarrent immédiatement : aucune dépendance
- La session Stats (3) est le pivot central : elle débloque WeaponArchitecture, SwordMoveset, Corruption, Économie et Arbre de talents
- SaveDesign (7) dépend de Stats et Corruption pour être complet — ne pas l'ouvrir avant
- Lore Déités et Lore Fée (14-15) sont parallélisables avec le code à tout moment, mais non urgents

---

## Statuts

| Statut | Signification |
|---|---|
| A faire | Pas commencé |
| En cours | Session ouverte |
| Valide | Complété et validé |
| Bloqué | En attente d'une dépendance |

Tous les jalons ci-dessus sont au statut **A faire** au 26/05/2026.
