# Effets de Statut & Corruption Magique -- Shadow of Mana
# Spec design validee le 28/05/2026 -- MAJ 29/05/2026

---

## 1. Effets de statut par deite

Chaque deite possede un effet de statut signature appliquable aux ennemis ET au heros.

| Deite | Element | Effet | Mecanique |
|-------|---------|-------|-----------|
| **Lumina** | Lumiere | Eblouissement | Reduit la chance de toucher ennemie + revele ennemis invisibles |
| **Luna** | Lune | Sommeil | Bloque toutes les actions -- se reveille si touche -- degats de reveil x1.5 |
| **Ombre** | Ombre | Malediction | Reduit les soins recus de 75% -- pernicieux, invisible au premier regard |
| **Sylphide** | Vent | Desequilibre | Reduit Defense + empeche le sprint |
| **Gnome** | Terre | Alourdi | Reduit Vitesse et VitesseAttaque severement |
| **Salamandre** | Feu | Brulure | Drain PV periodique + -Resistance Feu (la brulure s'entretient) |
| **Ondine** | Eau | Gele | Ralentissement severe -- si deja Ralenti : Fige (immobilisation totale breve) |
| **Dryade** | Nature | Empoisonne | Drain PV lent mais long + se cumule jusqu'a 3 stacks |

### Interactions notables

- **Sommeil (Luna) + attaque** = reveil brutal x1.5 degats -- invite a combo inter-sorts
- **Desequilibre (Sylphide) + Gele (Ondine)** = Fige -- synergie entre deux deites
- **Malediction (Ombre) + Drain (Dryade ou Salamandre)** = combo tres punitif sur ennemis a gros PV
- **Brulure (Salamandre) + Empoisonne (Dryade)** = double drain, efficace en combat de harcelement

### Variables d'effet de statut

Chaque effet est represente par :
- `bIsActive` (bool) : effet actif ou non
- `Duration` (float) : duree restante en secondes
- `Stacks` (int, si applicable) : nombre de stacks actifs (ex. Empoisonne max 3)
- `SourceDeity` (FName) : deite source de l'effet

Reduction par TenaciteEtat : `DureeEffective = Duration * (1 - TenaciteEtat)`

### TenaciteEtat heros -- RESOLU (29/05/2026)

- Valeur de base heros : **25** (cle supplementaire BP_AttributeSet_Base -- pas une 8eme stat visible)
- Modifiable par : equipement, buffs/debuffs, Corruption
- Corruption reduit TenaciteEtat -> boucle de pression (plus corrompu = plus vulnerable)
- Passe par SetStatValue comme toutes les stats
- A implementer dans C1-SwordMoveset

### Implementation

`BP_StatusEffectComponent` sur BP_SoM_HeroCharacter ET BP_Enemy_Base.
A creer lors de **C1-SwordMoveset**.

---

## 2. Corruption Magique

### Concept

La Corruption mesure le degre auquel le heros utilise la magie des deites a des fins violentes.
C'est un systeme de risque/recompense : haute Corruption = farming accelere mais heros fragilise.

### Deux phases de Corruption

**Phase 1 -- debut du jeu (avant la revelation Hero/Ombre)**
- Plafond : 50
- Seuils actifs : 25 (aura visible), 50 (-20% resistances)
- Pas de faiblesse elementaire, pas d'effets de statut
- Le joueur apprend le systeme sans risque maximal

**Phase 2 -- apres le Sanctuaire d'Ombre (milieu acte 1)**
- Plafond : 100 (leve involontairement par Ombre suite a la decheance de la Mana)
- Narrativement : Ombre ne "choisit" pas de corrompre le heros -- c'est la consequence de son etat blesse
- Faiblesse a 75 : element de la **deite la plus utilisee DEPUIS LA DERNIERE PURGE** (deterministe, lisible)
- Effet de statut a 100 : celui de cette **meme deite** toutes les 30s -- consequence directe des choix de jeu

### Jauge Corruption

- Float 0.0 -> plafond (50 ou 100 selon phase) sur BP_SoM_HeroCharacter
- Cle SetStatValue : "Corruption"
- Visible dans le HUD (a ajouter a UI_HUD_Main -- C1-HUDCore)
- Purge complete a la Fontaine de Fee

### Generation de Corruption par sort

| Type de sort | Corruption generee |
|--------------|-------------------|
| Attaque | +3 |
| Debuff | +2 |
| Buff | +1 |
| Heal | 0 (ou +0.5 si soin excessif sur PV pleins -- a confirmer au playtest) |

### Modificateurs par deite

| Deite | Modificateur Corruption |
|-------|------------------------|
| Ombre | x0.5 (elle attend qu'on cede) |
| Lumina | x1.5 (la lumiere se corrompt vite si mal utilisee) |
| Salamandre | x1.25 (le feu devore tout y compris son utilisateur) |
| Dryade | x0.75 (la nature est patiente) |
| Luna, Sylphide, Gnome, Ondine | x1.0 |

### Effets par seuil

| Seuil | Effet negatif | Bonus Essence ennemis |
|-------|--------------|----------------------|
| 0-24 | Aucun | x1.0 (base) |
| 25-49 | Aura visible (cosmetique -- signal d'alerte) | x1.15 |
| 50-74 | -20% resistances elementaires heros | x1.35 |
| 75-99 | Faiblesse element (deite la plus utilisee depuis purge) + perte stamina a chaque sort | x1.60 |
| 100 | Effet de statut (deite la plus utilisee) toutes les 30s | x1.60 (plafond) |

Le bonus Essence plafonne a x1.60 -- atteindre 100 n'apporte aucun farming supplementaire mais ajoute des penalites.
Le joueur doit choisir son niveau de risque optimal.

### Role des sorts Heal

Les sorts Heal ne generent pas de Corruption mais reduisent legerement le bonus Essence actif.
Cela donne aux sorts Heal un role strategique au-dela du simple soin.

### Purge a la Fontaine de Fee

- Remet Corruption a 0
- Si Corruption >= 75 : la fee est "epuisee" -- impossible de monter le niveau d'une deite lors de cette visite
- Si Corruption = 100 : purge forcee, la fee gronde (effet narratif a definir -- Session Lore Fee)
- Mobs normaux respawnent a chaque visite

---

## 3. Points encore ouverts

| Sujet | Lie a |
|-------|-------|
| Duree des effets de statut par defaut | C1-SwordMoveset |
| Effet narratif exact Corruption=100 (dialogue fee ?) | Session Lore Fee |
| Aura visuelle Corruption >= 25 : shader, particules ? | ART ou C4 |
| Soins excessifs corrompent-ils vraiment (+0.5) ? | Playtest |
| Calibrage Corruption -> reduction TenaciteEtat (valeurs exactes) | Session Economie/Calibrage |

---

*Cree le 28/05/2026*
*MAJ 28/05/2026 : Corruption Phase 1/2, lien narratif Ombre, faiblesse = deite la plus utilisee depuis purge*
*MAJ 29/05/2026 : TenaciteEtat heros base 25 RESOLU (C1-WeaponArchitecture), points ouverts nettoyes*
