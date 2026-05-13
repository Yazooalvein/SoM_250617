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
| Radial menu unifie | ⚠️ WIP | J-13 en cours, navigation + fixes valides PIE |
| Combo system | ✅ POC | TMap + fenetre dynamique, a evaluer pour multi-types |
| IA ennemis | ✅ POC | Behavior Tree + PawnSensing, base ennemie uniquement |
| Hit Flash joueur | ✅ Stable | M_Hero HitFlashAmount |
| Hit Flash ennemi | ⚠️ Partiel | Necessite DMI + vrai enemy mesh |
| Systeme de magie | ✅ POC | BP_MagicComponent + 4 sorts Lumina valides PIE |

---

## Jalons a venir — par priorite

---

### PRIORITE 1 — Nettoyage technique restant

- [ ] **J-A** : Supprimer BP_PlatformingGameMode via Content Browser
- [ ] **J-B** : Consolidation animations en double
- [ ] **J-C** : Verification et consolidation IMC dans Enhanced Input UI
- [ ] **J-D** : Reorganisation dossier Enemies via Content Browser
- [ ] **J-E** : Hit Flash ennemis finalise — vrai enemy mesh + M_Enemy_Base + DMI au BeginPlay
- [ ] **J-F** : Systeme SaveGame — session dediee

---

### PRIORITE 2 — POC Systeme de Magie

- [x] **J-10** : Architecture magie — BP_MagicComponent
- [x] **J-11** : Structure des sorts — BP_SpellBase + DT_Spells
- [x] **J-12** : Systeme de deblocage — liaison representants / deites
- [ ] **J-13** : Integration radial menu unifie (armes + magie) -- EN COURS
  - [x] Navigation par cran (stick G/D), lerp fluide, wrap correct
  - [x] UpdateCenterInfo (textes centre)
  - [x] Fix surbrillance a 12h des l'ouverture
  - [x] Fix drift (RadialContainer 0.01x0.01, RadialRadius 330)
  - [ ] Pont temporaire armes : DiscoveredWeapons -> FSoM_RadialSlotData
    ⚠️ Temporaire — sera refactore lors de la refonte armes (J-15 a J-19)
  - [ ] Changement de categorie stick Haut/Bas (Weapons <-> Magic)
  - [ ] Confirmation bouton A + Retour bouton B
  - [ ] UI_QuickslotBar : 3 slots HUD
- [x] **J-14** : POC magie jouable — 4 sorts Lumina valides PIE

---

### PRIORITE 3 — Refonte Combat Multi-Armes

- [ ] **J-15** : Audit BP_ComboManagerComponent
- [ ] **J-16** : Architecture par type d'arme — BP_WeaponType_Base
  - Classe mere abstraite par TYPE (Epee, Arc, Fléau, Lance...)
  - BP_Weapon_Base devient instance d'un type, pas classe mere
- [ ] **J-17** : POC Epee — moveset complet
- [ ] **J-18** : POC Arc — logique distance
  - ✅ ACTE : munitions illimitees
  - Systeme de visee (lock-on oriente la fleche, visee libre sans lock)
  - Projectile BP, charge optionnelle
- [ ] **J-19** : Switching en combat — validation fluidite
  - Conservation du combo si switching rapide ou reset ? (point de design ouvert)

---

### PRIORITE 4 — POC Compagnons PNJ

- [ ] **J-20** : Architecture IA alliee — BP_AIController_Companion_Base
- [ ] **J-21** : Gestion formation (2 compagnons max, positions relatives)
- [ ] **J-22** : Compagnon combattant POC — Luna
- [ ] **J-23** : Compagnon non combattant POC — Lumina

---

### PRIORITE 5 — Corruption Magique

- [ ] **J-24** : Compteur de corruption — BP_CorruptionComponent (0-100)
- [ ] **J-25** : Effets par seuil (25 / 50 / 75 / 100)
- [ ] **J-26** : Integration narrative

---

### PRIORITE 6 — Ville Hub Evolutive (Ville de l'Oracle)

- [ ] **J-27** : Variable de progression globale — GameInstance
- [ ] **J-28** : Actors conditionnels dans le niveau
- [ ] **J-29** : Systeme de forge — BP_ForgeComponent (NPC Forgeron)

---

### PRIORITE 7 — Systeme de Progression (Arbre de Talent + Gear)

- [ ] **J-30** : Level general + stats de base
- [ ] **J-31** : Systeme d'equipement — bonus % sur stats
- [ ] **J-32** : Arbre de talent par type d'arme

---

## Points de design encore ouverts

- **Forge** : quel materiau / systeme de graines Mana exactement ?
- ~~**Arc** : munitions limitees ou tir libre ?~~ ✅ ACTE : munitions illimitees
- **Switching armes** : reset combo ou conservation ?
- **Corruption** : les sorts de soin corrompent-ils moins ou pas du tout ?
- **Compagnons** : les PNJ peuvent-ils mourir de facon permanente (hors choix moral) ?
- **Deites Loup et Colosse** : Salamandre ou Gnome pour le Loup ?
- **Flammy** : quel moment narratif debloque le voyage rapide ?

---

## Historique

- Creation : 11/05/2026
- Derniere mise a jour : 13/05/2026
