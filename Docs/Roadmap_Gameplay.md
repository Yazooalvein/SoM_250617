# Roadmap Gameplay — Shadow of Mana

Document de reference pour la planification des modules a implémenter.
Mis a jour apres chaque session de design ou de developpement.

---

## Modules existants (POC valides)

| Module | Etat | Notes |
|--------|------|-------|
| Stats (SetStatValue / OnStatChanged) | ✅ Stable | Architecture solide, ne bougera pas |
| HUD event-driven | ✅ Stable | Zero polling, extensible |
| Iframes dash/roll | ✅ Stable | Via AnimNotify, Dark Souls style |
| Mort du joueur | ✅ Stable | bIsDead + OnPlayerDeath dispatcher |
| Lock-On | ✅ Stable | BP_PlatformingPlayerController |
| Radial menu (armes) | ✅ POC | Data-driven, base solide |
| Combo system | ✅ POC | TMap + fenetre dynamique, a evaluer pour multi-types |
| IA ennemis | ✅ POC | Behavior Tree + PawnSensing, base ennemie uniquement |
| Hit Flash joueur | ✅ Stable | M_Hero HitFlashAmount |
| Hit Flash ennemi | ⚠️ Partiel | Necessite DMI + vrai enemy mesh |

---

## Jalons a venir — par priorite

---

### PRIORITE 1 — Nettoyage technique restant
*A faire avant tout nouveau developpement pour garder la base propre.*

- [ ] **J-A** : Supprimer BP_PlatformingGameMode via Content Browser (C4 final)
- [ ] **J-B** : Consolidation animations en double — rediriger BP_PlatformingCharacter vers Weapons/Animation/ (I1)
- [ ] **J-C** : Verification et consolidation IMC dans Enhanced Input UI (I2)
- [ ] **J-D** : Reorganisation dossier Enemies via Content Browser (I4)
- [ ] **J-E** : Hit Flash ennemis finalise — vrai enemy mesh + M_Enemy_Base + DMI au BeginPlay
- [ ] **J-F** : Systeme SaveGame — session dediee

---

### PRIORITE 2 — POC Systeme de Magie
*Colonne vertebrale du gameplay. Tout le reste s'equilibre par rapport a elle.*

**Pourquoi en premier :** sans definir ce que la magie peut faire (puissance, cout, situations sauvables), impossible de designer correctement la difficulte du cac ni l'equilibre global.

- [ ] **J-10** : Architecture magie — BP_MagicComponent, jauge Mana independante de Stamina
  - Deux ressources totalement separees : Mana (magie) / Stamina (physique)
  - ConsumeMana() via SetStatValue, notification OnStatChanged
  - ManaRegen passif (plus lent que Stamina)

- [ ] **J-11** : Structure des sorts — BP_SpellBase + DT_Spells
  - DataTable : SpellName, Element, ManaCost, Damage/Effect, Cooldown, AnimMontage
  - 4 categories par element : Attaque / Buff / Debuff / Soin
  - Sort ultime (5e categorie) debloque plus tard

- [ ] **J-12** : Systeme de deblocage — liaison representants / deites
  - Chaque deite debloque un niveau de magie a sa rencontre narrative
  - BP_MagicUnlockComponent ou flag dans GameInstance
  - Ordre : Lumina (soin) -> Luna (buff) -> Sylphide (vent) -> ... -> Ondine (eau, fin)

- [ ] **J-13** : Integration radial menu magie
  - Second radial (ou sous-menu du radial existant) pour selection des sorts
  - Navigation : radial armes (physique) / radial magie (elementaire)
  - Compatible avec switching en combat

- [ ] **J-14** : POC magie jouable — 1 sort par categorie, 1 element (Lumina)
  - Soin basique, attaque lumiere, buff defense, debuff ennemi
  - Validation de l'equilibre Mana cost vs effet vs regeneration

---

### PRIORITE 3 — Refonte Combat Multi-Armes
*Identite visuelle et sensorielle du jeu. Secret of Mana 1 comme reference.*

**Pourquoi apres la magie :** l'equilibre du cac depend de ce que la magie peut compenser.

- [ ] **J-15** : Audit BP_ComboManagerComponent — evaluer extensibilite vs refonte
  - Question cle : le ComboManager actuel peut-il gerer des logiques radicalement differentes (melee / distance / chaine) ?
  - Decision : extension ou refonte vers architecture par type d'arme

- [ ] **J-16** : Architecture par type d'arme — BP_WeaponType_Base
  - Classe mere abstraite par TYPE (Epee, Arc, Fléau, Lance...)
  - Chaque type = moveset propre + hitbox propre + animations propres
  - BP_Weapon_Base devient instance d'un type, pas classe mere

- [ ] **J-17** : POC Epee — moveset complet
  - Combo 3 coups, finisseur, coup chargé
  - Hitbox melee, feedback hit, integration iframes existantes

- [ ] **J-18** : POC Arc — logique distance
  - Systeme de visee (lock-on oriente la fleche, visee libre sans lock)
  - Projectile BP, charge optionnelle
  - Pas de Stamina sur les fleches (ressource munitions ? ou libre ?)

- [ ] **J-19** : Switching en combat — validation fluidite
  - Transition animation entre types d'armes
  - Conservation du combo si switching rapide ou reset ?
  - Test de gameplay : est-ce que switcher en combat est fun et lisible ?

---

### PRIORITE 4 — POC Compagnons PNJ
*Experience de jeu complete — le joueur ne doit jamais se sentir seul.*

- [ ] **J-20** : Architecture IA alliee — BP_AIController_Companion_Base
  - Separe completement de BP_AIController_Enemy_Base
  - Behavior Tree dedie : suivre / combattre / se replier / soin (si Lumina)
  - Perception : allie du joueur, pas de friendly fire

- [ ] **J-21** : Gestion formation
  - 2 compagnons max actifs simultanement
  - Positions relatives au joueur (flancs, arriere)
  - Pathfinding en terrain de jeu DS (obstacles, denivelee)

- [ ] **J-22** : Compagnon combattant POC — Luna
  - Moveset propre, animations, priorites de ciblage
  - Agression moderee (ne vole pas les kills, cree des ouvertures)

- [ ] **J-23** : Compagnon non combattant POC — Lumina
  - Soin automatique conditionnel (seuil HP joueur)
  - Buff passif de presence (aura lumiere ?)
  - Ne s'expose pas au danger

---

### PRIORITE 5 — Corruption Magique
*Tension permanente, identite unique du jeu.*

- [ ] **J-24** : Compteur de corruption — BP_CorruptionComponent
  - Variable CorruptionLevel (0-100), monte a chaque usage de magie
  - Decroissance lente passive, decroissance rapide via purification (sanctuaires ?)
  - Pas de corruption sur les sorts de soin (ou moins)

- [ ] **J-25** : Effets par seuil
  - Seuil 25 : debuff mineur (vitesse de regen Mana reduite)
  - Seuil 50 : effet visuel (aura sombre sur le personnage), ennemis plus agressifs
  - Seuil 75 : debuff combat (fenetre combo reduite)
  - Seuil 100 : etat critique — sort suivant declenche un effet negatif majeur

- [ ] **J-26** : Integration narrative
  - Certains PNJ reagissent a la corruption visible du heros
  - Zones de purification dans le monde (sanctuaires elementaires)

---

### PRIORITE 6 — Ville Hub Evolutive (Ville de l'Oracle)
*Narration mecanique — le monde reagit a ta progression.*

- [ ] **J-27** : Variable de progression globale — GameInstance
  - HubProgressionLevel (int) incrementee par jalons narratifs (boss, quetes, PNJ sauves)
  - Accessible depuis tous les blueprints

- [ ] **J-28** : Actors conditionnels dans le niveau
  - Batiments/zones qui changent visuellement selon HubProgressionLevel
  - PNJ qui apparaissent a des seuils definis
  - Forgeron nain qui s'installe (debloque systeme de forge)

- [ ] **J-29** : Systeme de forge — BP_ForgeComponent (NPC Forgeron)
  - Evolution arme liee a HubProgressionLevel + jalons narratifs specifiques
  - Interface forgeron : arme actuelle -> prochaine evolution -> conditions requises
  - Materiaux / graines Mana comme ressource de forge (a definir)

---

### PRIORITE 7 — Systeme de Progression (Arbre de Talent + Gear)
*Long terme — a designer apres validation des systemes de combat et magie.*

- [ ] **J-30** : Level general + stats de base
  - XP -> Level -> points de stats (HP, Agilite, autres)
  - Integration OnStatChanged existant

- [ ] **J-31** : Systeme d'equipement — bonus % sur stats
  - +10% HP, +5% MP, Stamina regen plus rapide...
  - Slots : armure, casque, gantelets, accessoires (x2 ?)

- [ ] **J-32** : Arbre de talent par type d'arme
  - Points de talent debloques par usage de l'arme (pas par level general)
  - Branches : degats / vitesse / effets speciaux
  - Lie a l'evolution forge (arme niveau superieur = nouvelles branches)

---

## Points de design encore ouverts

Ces questions doivent etre tranchees avant d'implémenter les modules concernes :

- **Forge** : quel materiau / systeme de graines Mana exactement ?
- **Arc** : munitions limitees ou tir libre ?
- **Switching armes** : reset combo ou conservation ?
- **Corruption** : les sorts de soin corrompent-ils moins ou pas du tout ?
- **Compagnons** : les PNJ peuvent-ils mourir de facon permanente (hors choix moral) ?
- **Deites Loup et Colosse** : Salamandre ou Gnome pour le Loup ? Confirmer la repartition.
- **Flammy** : quel moment narratif debloque le voyage rapide ?

---

## Historique

- Creation : 11/05/2026
- Derniere mise a jour : 11/05/2026
