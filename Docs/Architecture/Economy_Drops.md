# Economie & Drops -- Shadow of Mana
# Spec design validee le 28/05/2026

---

## 1. Double monnaie

Deux ressources distinctes, deux usages distincts.

| Ressource | Gagnee via | Utilisee pour | Perdue a la mort |
|-----------|-----------|---------------|-----------------|
| **Essence de Mana** | Ennemis, quetes, exploration | Niveaux globaux, investissement deites, forge armes | Oui -- recuperable sur place (DS-like) |
| **Pieces d'Or (PO)** | Ennemis, coffres, quetes | Marchands (objets, armures, consommables) | Non |

L'Essence = progression long terme, ressource precieuse avec risque.
Les PO = economie du monde, filet de securite stable.

---

## 2. Drops ennemis

### Ce que droppent les ennemis

| Type de drop | Mechanique |
|-------------|-----------|
| Essence de Mana | Toujours -- quantite variable selon type ennemi |
| Pieces d'Or | Toujours -- quantite variable selon type ennemi |
| Objet consommable | Aleatoire -- % de chance selon type ennemi |
| Materiau de forge | Aleatoire -- % de chance selon type ennemi |
| Coffre | Aleatoire -- gimmick Seiken, % de chance selon type ennemi |

### Calibrage par type d'ennemi

| Type | Essence | PO | Drop objet | Drop materiau |
|------|---------|-----|-----------|---------------|
| Ennemi faible | 15-25 | 5-10 | 15% | 8% |
| Ennemi standard | 35-50 | 15-25 | 20% | 12% |
| Ennemi elite | 80-120 | 40-60 | 25% | 18% |
| Mini-boss (respawn) | 200-300 | 100-150 | 40% | 30% |
| Boss (no respawn) | 500-800 | 300-500 | Garanti x1 | Garanti x1 |

Valeurs a ajuster au playtest. Avec bonus Corruption x1.60, un joueur risque peut reduire le grind d'Essence d'environ 35%.

### Coffres droppes par ennemis

Gimmick Seiken : certains ennemis peuvent dropper un coffre a leur mort.
Contenu du coffre : objet consommable, materiau, ou PO en quantite elevee.
Le taux de drop coffre est inclus dans le % drop objet ci-dessus.

---

## 3. Coffres fixes

Coffres places dans le monde par l'equipe de design.
- **Coffres caches** : recompensent l'exploration, contenu superieur
- **Coffres standards** : jalonnent les zones, contenu moyen
- Coffres ouverts = sauvegardes, ne respawnent pas

---

## 4. Consommables

### Table des consommables (style Secret of Mana)

| Objet | Effet | Prix PO marchand |
|-------|-------|-----------------|
| Bonbon | Regen PV faible | 10 |
| Noix | Regen PV moyen | 25 |
| Miel | Regen PV fort | 50 |
| Plante | Regen Mana | 35 |
| Herbe | Purge effet de statut | 30 |
| Essence Purifiee | Reduit Corruption -15 | 80 |
| Repas (buff drop) | +% drop temporaire (duree X min) | 120 |

### Regles consommables

- Stock max : 9 unites par type
- Utilisation : via quickslot ou radial dedie objets (a ajouter -- C7-HUDPolish)
- Utilisables en combat avec animation courte interruptible
- Rechargement Fontaine de Fee : prend dans le stock mondial accumule (drops + achats)
  -- pas de recharge infinie, il faut farmer ou acheter
- Taux de drop augmente uniquement via Repas (buff temporaire) -- pas de stat permanente

---

## 5. Materiaux de forge

### Categories

| Tier | Nom placeholder | Sources | Usage |
|------|----------------|---------|-------|
| Commun | Graine de Mana | Drop ennemi commun ~8-12% | Upgrades de base armes/armures |
| Rare | Cristal de Mana | Drop ennemi rare ~3-5%, boss garanti | Upgrades avancees |
| Special | Essence Cristallisee | Exploration, recompenses quetes, boss | Upgrades ultimes |

### Forge narrative (style Secret of Mana)

- Les upgrades d'armes suivent une progression narrative : upgrade N+1 disponible SEULEMENT apres le jalon narratif associe
- Les materiaux empeche le rush immediat meme quand le jalon est atteint
- Materiaux NON lies aux elements -- ressources universelles pour toutes les armes
- Prerequis de niveau pour equiper : a definir en C5-Equipment

---

## 6. Equipement (slots hors armes)

3 slots : Casque, Armure, Accessoire.
Stats apportees : Defense + Resistance uniquement.
Achat chez marchands (PO) ou trouve en coffres/drops boss.

| Slot | Stats | Prix PO indicatif |
|------|-------|-------------------|
| Casque basique | +Defense, +Resistance | 150-300 |
| Armure basique | +Defense, +Resistance | 200-400 |
| Accessoire | +Defense, +Resistance | 200-350 |

Prerequis de niveau pour equiper : a definir en C5-Equipment.
Pas de gestion de poids.

---

## 7. Cout sorts en Mana

### Formule
```
Cout Mana = Base + (NiveauSort * Multiplicateur)
```

| Categorie | Base | Multiplicateur | Niv 1 | Niv 5 | Niv 8 |
|-----------|------|----------------|-------|-------|-------|
| Attaque | 5 | 2 | 7 | 15 | 21 |
| Debuff | 4 | 2 | 6 | 14 | 20 |
| Heal | 4 | 1.5 | 6 | 12 | 16 |
| Buff | 3 | 1 | 4 | 8 | 11 |

Ultimes : a definir quand disponibles.

### ManaMax

- Stat separee de Magie (Magie = puissance, ManaMax = taille jauge)
- Monte avec le niveau global (comme PV)
- Cles SetStatValue : "ManaMax" / "ManaCurrent"

| Niveau | ManaMax |
|--------|---------|
| 1 | 60 |
| 2 | 68 |
| 3 | 76 |
| 5 | 92 |
| 10 | 132 |

+8 par niveau. Pas de regen Mana auto -- restauration via Fontaine ou Plante consommable.

---

## 8. Sauvegarde & respawn Fontaine

### Ce qui est sauvegarde (jamais perdu)

- Niveau global + stats + points distribues
- Armes trouvees / equipement
- Sorts debloques + niveaux de sorts
- Niveaux de deites investis
- Jalons narratifs
- Coffres fixes ouverts
- PO accumulated
- Essence depensee

### Ce qui est perdu a la mort

- Essence non depensee -- recuperable sur le lieu de la mort (DS-like)
- Double mort avant recuperation = Essence definitivement perdue

### Respawn Fontaine

- Ennemis normaux : respawnent a chaque visite
- Boss : jamais respawn
- Ennemis uniques narratifs : jamais respawn
- Stock consommables : recharge depuis stock mondial accumule

---

## 9. Points encore ouverts

| Sujet | Lie a |
|-------|-------|
| Duree du buff Repas | C5-Equipment ou session Economie |
| Prerequis de niveau equipement | C5-Equipment |
| Noms definitifs consommables (lore Seiken) | Session Lore |
| Prix PO marchands calibres | Playtest acte 1 |
| Taux drops calibres | Playtest acte 1 |
| Radial dedie objets vs integration radial existant | C7-HUDPolish |
| Corruption Phase 1 plafond 50 : quand exactement debloquer Phase 2 ? | Session Lore Ombre |

---

*Cree le 28/05/2026 -- session design Economie & Drops*
*Prochaine mise a jour prevue : C5-Equipment (forge, prerequis, calibrage)*
