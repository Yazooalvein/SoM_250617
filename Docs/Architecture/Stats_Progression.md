# Stats & Progression — Shadow of Mana
# Spec design validee le 28/05/2026

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

Toutes les stats passent par SetStatValue / OnStatChanged (architecture existante).
Nouvelles cles a ajouter dans BP_AttributeSet_Base.

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

Valeurs a ajuster au playtest -- courbe lineaire legerement acceleree.

### 3b. Progression par usage (deja implementee)

- Armes : niveau arme monte via ComboManager (InitComboTree / LevelMin existant)
- Magie : sorts montent via IncrementSpellUsage / LevelUpSpell existant
- Ces progressions sont independantes du niveau global

---

## 4. Ressource universelle -- Essence de Mana

### Concept lore
Energie vitale du monde de Mana, circulant dans les etres vivants, les armes et les esprits des deites.
Liberee en tuant des ennemis. Dispersee a la mort du heros -- mais recuperable.

### Mecanique
- Une seule ressource : Essence de Mana (float, cle "EssenceMana")
- Utilisations :
  - Monter de niveau global (stats physiques)
  - Investir dans un niveau de deite (puissance magique d'une ecole)
- Couts croissants dans les deux cas (courbes exponentielles)
- Perdue a la mort du heros
- Recuperable en retournant physiquement a l'endroit de la mort (style Dark Souls)
- Si le heros meurt une deuxieme fois avant recuperation : Essence definitivement perdue

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

### Cout investissement deite (a calibrer)
Courbe similaire mais par deite -- a definir en session Lore Deites.

---

## 5. Formule de degats

### Degats physiques
```
Degats = Max(1, (Attaque * CoeffArme * CoeffCritique) - (Defense * 0.5))
```

### Degats magiques
```
Degats = Max(1, (Magie * CoeffSort * CoeffCritique) - (Resistance * 0.5))
```

### Variables
- **CoeffArme** : float dans FWeaponData (Epee 1M=1.0, Epee 2H=1.4, Arc=0.8, Hache=1.6)
- **CoeffSort** : float dans FSoM_SpellData par sort
- **CoeffCritique** : 1.0 par defaut, 1.5 si coup critique
- Plancher a 1 degat minimum (Max(1, ...))

### Degats elementaires
```
Degats finaux = Degats * (1 - ResistanceElementaire[Element])
```
ResistanceElementaire : TMap<EElement, float> sur le heros ET les ennemis.
Valeurs negatives = faiblesse (ex. -0.5 = +50% de degats recus).
8 elements correspondant aux 8 deites : Lumina, Luna, Ombre, Sylphide, Gnome, Salamandre, Ondine, Dryade.

### Coups critiques
- Chance critique : stat flottante sur le heros (default 5%, soit 0.05)
- S'applique aux degats physiques ET magiques
- Les ennemis peuvent aussi critter (chance configurable par type)
- Cle SetStatValue : "ChanceCritique"

---

## 6. Vitesse d'attaque -- stat d'arme

VitesseAttaque est un multiplicateur dans FWeaponData, applique au PlayRate du montage d'animation.
Ne pas confondre avec la stat Vitesse du heros (deplacement + stamina).

| Arme | CoeffArme | VitesseAttaque | Feeling |
|------|-----------|----------------|---------|
| Epee 1M | 1.0 | 1.2 | Rapide, polyvalent |
| Epee 2M | 1.4 | 0.75 | Lent, lourd |
| Arc | 0.8 | 1.0 | Moyen, distance |
| Hache (futur) | 1.6 | 0.6 | Tres lent, tres fort |

Implementation : PlayAttackMontage -> PlayRate = WeaponData.VitesseAttaque
A ajouter dans FWeaponData lors de C1-WeaponArchitecture.

---

## 7. Stamina (Endurance)

- Jauge visible HUD (a ajouter a UI_HUD_Main via OnStatChanged)
- Couts :
  - Attaque legere : -10
  - Attaque lourde : -20
  - Esquive / roll : -25
  - Sprint : drain continu -5/seconde
- Recuperation : automatique apres 1s d'inaction, vitesse liee a la stat Vitesse
- En dessous de 0 : actions bloquees, pas de punition supplementaire pour l'acte 1

---

## 8. Effets de statut

Le heros ET les ennemis peuvent subir des effets de statut.

| Effet | Mechanique | Cible stat |
|-------|-----------|------------|
| Poison | Drain PV periodique (% PV / seconde) | PV |
| Ralentissement | Reduit Vitesse temporairement | Vitesse |
| Affaiblissement | Reduit Attaque ou Magie temporairement | Attaque / Magie |
| Etourdi | Bloque les actions pendant X secondes | -- (flag) |
| Brule | Drain PV + -Resistance Fire | PV + Resistance |

**TenaciteEtat** (float 0.0 a 1.0) : reduit la duree des effets subis.
Ex. TenaciteEtat=0.5 -> durees de tous les debuffs reduites de 50%.

Implementation recommandee : composant BP_StatusEffectComponent sur Character et Enemy_Base.
A creer lors de C1-SwordMoveset ou apres (les sorts Debuff Lumina existants peuvent utiliser un stub).

---

## 9. Pas de regeneration PV auto

Le heros ne regenere pas de PV naturellement hors combat.
Seules sources de soin : sorts Heal, objets consommables (futur), Fontaine de Fee.

---

## 10. Points encore ouverts

| Sujet | Lié a |
|-------|-------|
| Cout Essence par niveau de deite | Session Lore Deites |
| Ennemis peuvent-ils critter ? Quelle chance ? | C2-EnemyTypes |
| Valeurs ResistanceElementaire par type ennemi | C2-EnemyTypes |
| TenaciteEtat heros : valeur de base | C1-SwordMoveset |
| BP_StatusEffectComponent : quand creer ? | C1-SwordMoveset ou apres |
| Vitesse influe-t-elle sur vitesse d'anim de recuperation stamina ? | C1-WeaponArchitecture |

---

*Cree le 28/05/2026 -- session design Stats/Progression*
*Prochaine mise a jour prevue : C1-WeaponArchitecture (ajout CoeffArme + VitesseAttaque dans FWeaponData)*
