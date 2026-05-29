# Stats & Progression — Shadow of Mana
# Spec design validee le 28/05/2026 -- MAJ 29/05/2026

---

## 1. Caracteristiques du heros (7 stats)

| Stat | Role | Base niveau 1 | Cle SetStatValue |
|------|------|---------------|-----------------|
| Vitalite | Points de vie max | 100 | "HealthMax" / "HealthCurrent" |
| Attaque | Degats physiques bruts | 10 | "Attaque" |
| Defense | Reduction degats physiques | 5 | "Defense" |
| Magie | Puissance des sorts | 10 | "Magie" |
| Resistance | Reduction degats magiques | 5 | "Resistance" |
| Endurance | Jauge stamina max | 100 | "EnduranceMax" / "EnduranceCurrent" |
| Vitesse | Deplacement + recuperation stamina | 10 | "Vitesse" |

Stats supplementaires (cles a ajouter dans BP_AttributeSet_Base) :
- "Level", "EssenceMana", "EssenceManaDropped", "PiecesOr", "ChanceCritique", "Corruption"
- "ManaMax", "ManaCurrent" (separees de Magie -- voir section 8)
- "TenaciteEtat" : base 25, cle supplementaire (pas une 8eme stat visible) -- impactee par equipement + debuffs + Corruption

Toutes les stats passent par SetStatValue / OnStatChanged (architecture existante).

---

## 2. Stats ennemis

Systeme simplifie dedie, pas les memes stats que le heros.

| Stat | Role |
|------|------|
| PV / PVMax | Points de vie |
| Attaque | Degats physiques bruts |
| Defense | Reduction degats physiques recus |
| Resistance | Reduction degats magiques recus |
| Vitesse | Cible des debuffs ralentissement |
| VitesseAttaque | Cible des debuffs offensifs, multiplieur PlayRate montage |
| TenaciteEtat | Resistance aux effets de statut (0.0 a 1.0) |

A ajouter sur BP_Enemy_Base comme variables Instance Editable.
Ennemis n'ont PAS de jauge stamina, de niveau global, ni de progression par usage.

---

## 3. Modele de progression hybride

### 3a. Niveau global (1 -> 10 pour l'acte 1)

A chaque level up :
- Toutes les stats montent automatiquement (courbe fixe ci-dessous)
- +2 points a distribuer librement dans n'importe quelle stat

Courbe automatique par niveau :

| Niveau | PV | Attaque | Defense | Magie | Resistance | Endurance | Vitesse |
|--------|----|---------|---------|-------|------------|-----------|---------| 
| 1 | 100 | 10 | 5 | 10 | 5 | 100 | 10 |
| 2 | 115 | 11 | 6 | 11 | 6 | 105 | 10 |
| 3 | 130 | 12 | 7 | 12 | 7 | 110 | 11 |
| 4 | 147 | 13 | 8 | 13 | 8 | 115 | 11 |
| 5 | 165 | 15 | 9 | 15 | 9 | 120 | 12 |
| 6 | 184 | 17 | 10 | 17 | 10 | 125 | 12 |
| 7 | 205 | 18 | 11 | 18 | 11 | 130 | 13 |
| 8 | 220 | 19 | 12 | 19 | 12 | 135 | 13 |
| 9 | 235 | 21 | 13 | 21 | 13 | 140 | 14 |
| 10 | 250 | 22 | 14 | 22 | 14 | 145 | 15 |

Valeurs a ajuster au playtest.

### 3b. Progression par usage (deja implementee)

- Armes : niveau arme monte via ComboManager (InitComboTree / LevelMin existant)
- Magie : sorts montent via IncrementSpellUsage / LevelUpSpell existant
- Ces progressions sont independantes du niveau global

---

## 4. Ressource universelle -- Essence de Mana

### Concept lore
Energie vitale du monde de Mana, liberee en tuant des ennemis.
Dispersee a la mort du heros -- recuperable sur le lieu de la mort (DS-like).
Double mort avant recuperation = Essence definitivement perdue.

### Mecanique
- Cle SetStatValue : "EssenceMana"
- Utilisations : monter de niveau global + investir dans une deite
- Couts croissants (courbes exponentielles)
- Bonus selon Corruption : x1.0 / x1.15 / x1.35 / x1.60 selon seuil

### Courbe XP / Essence niveau global
```
Essence requise niveau N = 100 * 1.5^(N-1)
Niv 1->2 :  100 Essence
Niv 2->3 :  150 Essence
Niv 3->4 :  225 Essence
Niv 4->5 :  338 Essence
Niv 5->6 :  506 Essence
Niv 6->7 :  759 Essence
Niv 7->8 : 1139 Essence
Niv 8->9 : 1708 Essence
Niv 9->10: 2563 Essence
Total acte 1 : ~7488 Essence a distribuer via ennemis + quetes
```

---

## 5. Pieces d'Or (PO)

Monnaie secondaire stable -- jamais perdue a la mort.
Cle SetStatValue : "PiecesOr"
Utilisee pour : marchands (objets consommables, armures, equipement).
Voir Docs/Architecture/Economy_Drops.md pour calibrage et prix.

---

## 6. Formule de degats

### Degats physiques
```
Degats = Max(1, (Attaque * CoeffArme * CoeffCritique) - (Defense * 0.5))
```

### Degats magiques
```
Degats = Max(1, (Magie * CoeffSort * CoeffCritique) - (Resistance * 0.5))
```

### Degats elementaires
```
Degats finaux = Degats * (1 - ResistanceElementaire[Element])
```
ResistanceElementaire : TMap<EElement, float> sur le heros ET les ennemis.
Valeurs negatives = faiblesse. 8 elements / 8 deites.

### Coups critiques
- Chance critique : 5% de base (cle "ChanceCritique")
- x1.5 degats -- heros ET ennemis

---

## 7. Vitesse d'attaque -- stat d'arme

VitesseAttaque = multiplicateur PlayRate montage dans FWeaponData.
Ne pas confondre avec la stat Vitesse du heros.

| Arme | CoeffArme | VitesseAttaque |
|------|-----------|----------------|
| Epee 1M | 1.0 | 1.2 |
| Epee 2M | 1.4 | 0.75 |
| Arc | 0.8 | 1.0 |
| Hache (futur) | 1.6 | 0.6 |

---

## 8. Mana (jauge de sorts)

### ManaMax -- stat separee de Magie

- Magie = puissance des sorts (deja en place)
- ManaMax = taille de la jauge (nouvelle stat)
- Monte avec le niveau global (+8/niveau)
- Cles : "ManaMax" / "ManaCurrent"
- Pas de regen auto -- restauration via Fontaine de Fee ou Plante consommable

| Niveau | ManaMax |
|--------|---------|
| 1 | 60 |
| 2 | 68 |
| 3 | 76 |
| 5 | 92 |
| 10 | 132 |

### Formule cout sorts
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

---

## 9. Stamina (Endurance)

- Jauge visible HUD (a ajouter a UI_HUD_Main via OnStatChanged)
- Couts :
  - Attaque legere : -10
  - Attaque lourde : -20
  - Esquive / roll : -25
  - Sprint : drain continu -5/seconde
- Recuperation : automatique apres 1s d'inaction, vitesse liee a la stat Vitesse
- En dessous de 0 : actions bloquees, pas de punition supplementaire pour l'acte 1

---

## 10. Equipement (slots hors armes)

3 slots : Casque, Armure, Accessoire.
Stats apportees : Defense + Resistance uniquement (additifs aux stats de base).
Achat PO chez marchands ou trouve en coffres/drops boss.
Prerequis de niveau pour equiper : a definir en C5-Equipment.
Pas de gestion de poids.

---

## 11. Pas de regeneration PV auto

Seules sources de soin : sorts Heal, consommables (Bonbon/Noix/Miel), Fontaine de Fee.

---

## 12. Points encore ouverts

| Sujet | Lie a |
|-------|-------|
| Cout Essence par niveau de deite | Session Lore Deites |
| Valeurs ResistanceElementaire par type ennemi | C2-EnemyTypes |
| Vitesse influe-t-elle sur vitesse anim recuperation stamina ? | C1-SwordMoveset |
| Prerequis niveau equipement | C5-Equipment |
| Calibrage prix PO et drops | Playtest acte 1 |

---

*Cree le 28/05/2026*
*MAJ 28/05/2026 : ajout ManaMax, PO, equipement, formule cout sorts*
*MAJ 29/05/2026 : TenaciteEtat heros base 25 acte (RESOLU -- C1-WeaponArchitecture), points ouverts nettoyes*
