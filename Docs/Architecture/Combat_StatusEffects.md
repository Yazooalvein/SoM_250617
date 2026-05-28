# Effets de Statut & Corruption Magique -- Shadow of Mana
# Spec design validee le 28/05/2026

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
- **Brulure (Salamandre) + Empoisonne (Dryade)** = double drain, efficace en combat de harcèlement

### Variables d'effet de statut

Chaque effet est represente par :
- `bIsActive` (bool) : effet actif ou non
- `Duration` (float) : duree restante en secondes
- `Stacks` (int, si applicable) : nombre de stacks actifs (ex. Empoisonne max 3)
- `SourceDeity` (FName) : deite source de l'effet

Reduction par TenaciteEtat : `DureeEffective = Duration * (1 - TenaciteEtat)`

### Implementation recommandee

`BP_StatusEffectComponent` sur BP_SoM_HeroCharacter ET BP_Enemy_Base.
A creer lors de C1-SwordMoveset ou apres selon priorites.
Les sorts Debuff Lumina existants peuvent utiliser un stub en attendant.

---

## 2. Corruption Magique

### Concept

La Corruption mesure le degre auquel le heros utilise la magie des deites a des fins violentes.
Plus la Corruption est haute, plus le heros est instable -- mais aussi plus il attire l'Essence des ennemis.
C'est un systeme de risque/recompense, pas une pure punition.

### Jauge Corruption

- Float 0.0 -> 100.0 sur BP_SoM_HeroCharacter, cle SetStatValue : "Corruption"
- Visible dans le HUD (a ajouter a UI_HUD_Main)
- Purge complete a la Fontaine de Fee

### Generation de Corruption par sort

| Type de sort | Corruption generee |
|--------------|-------------------|
| Attaque | +3 |
| Debuff | +2 |
| Buff | +1 |
| Heal | 0 (ou +0.5 si soin excessif sur PV pleins) |

### Modificateurs par deite

Certaines deites tolerent mieux l'usage offensif de leur magie :

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
| 25-49 | Aura visible (cosmétique -- signal d'alerte) | x1.15 |
| 50-74 | -20% resistances elementaires heros | x1.35 |
| 75-99 | Un element aleatoire devient faiblesse active (-50% resistance) + perte stamina a chaque sort | x1.60 |
| 100 | Effet de statut aleatoire toutes les 30s sur le heros -- Fontaine obligatoire pour purger | x1.60 (plafond -- le jeu ne recompense plus d'aller au-dela) |

### Mechanique de bonus Essence

Plus la Corruption est haute, plus les ennemis vaincus laissent d'Essence de Mana.
Le bonus est progressif et plafonne a x1.60 -- atteindre 100 ne donne aucun avantage supplementaire
mais ajoute des penalites. Le joueur doit donc choisir son niveau de risque optimal.

**Tension centrale :**
- Purger souvent = securite + farming lent
- Rester haut en Corruption = farming rapide + vulnerabilite croissante
- Les Fontaines font respawn les mobs : purger trop souvent = moins d'Essence nette

### Role des sorts Heal dans la gestion Corruption

Les sorts Heal ne generent pas de Corruption mais reduisent legerement le bonus Essence en cours.
Soigner "refroidit" la dynamique de Corruption sans aller a la Fontaine, mais au prix du farming.
Cela donne aux sorts Heal un role strategique au-dela du simple soin.

### Purge a la Fontaine de Fee

- Remet Corruption a 0
- Si Corruption >= 75 au moment de la purge : la fee est "epuisee" -- impossible de monter le niveau
  d'une deite lors de cette visite (cout narratif et gameplay)
- Si Corruption = 100 : purge forcee, pas de choix, la fee gronde (effet narratif a definir en Session Lore Fee)
- Mobs respawn a chaque visite Fontaine (comportement DS)

---

## 3. Points encore ouverts

| Sujet | Lie a |
|-------|-------|
| Duree des effets de statut par defaut | C1-SwordMoveset (premier test en combat) |
| TenaciteEtat valeur de base heros | C1-SwordMoveset |
| Effet narratif exact Corruption=100 (dialogue fee ?) | Session Lore Fee |
| Aura visuelle Corruption >= 25 : shader, particules ? | ART ou C4 |
| Quel element devient faiblesse a 75 : aleatoire a chaque seuil ou fixe par run ? | A trancher |
| Soins excessifs corrompent-ils vraiment (+0.5) ? | A confirmer au playtest |

---

*Cree le 28/05/2026 -- session design Effets de Statut & Corruption*
*Prochaine mise a jour prevue : C1-SwordMoveset (premier contact avec BP_StatusEffectComponent)*
