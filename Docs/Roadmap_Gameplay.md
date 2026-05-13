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
| Lock-On | ⚠️ A revoir | Logique + UI a revoir (J-lock) |
| Radial menu unifie | ⚠️ WIP | J-13 quasi-complet, Quickslot POC restant |
| Combo system | ✅ POC | TMap + fenetre dynamique, a evaluer J-15 |
| IA ennemis | ✅ POC | Behavior Tree + PawnSensing |
| Hit Flash joueur | ✅ Stable | M_Hero HitFlashAmount |
| Hit Flash ennemi | ⚠️ Partiel | Necessite DMI + vrai enemy mesh |
| Systeme de magie | ✅ POC | BP_MagicComponent + 4 sorts Lumina valides PIE |

---

## Timeline reorganisee -- ordre de dependances

```
J-13 final
  └─> J-A/C/D (nettoyage rapide)
        └─> J-lock (Lock-On revision)
              └─> J-15/16/17 (Armes : audit -> archi -> POC Epee)
                    └─> J-F (SaveGame -- avant de complexifier)
                          └─> J-18/19 (Arc + Switching)
                                └─> J-B/E (animations + Hit Flash)
                                      └─> J-20/21/22/23 (Compagnons)
                                            └─> J-24/25/26 (Corruption)
                                                  └─> J-27/28/29 (Hub + Forge)
                                                        └─> J-30/31/32 (Progression)
```

Sessions creatives intercalees (voir section dediee).

---

## Jalons detailles

---

### J-13 -- Radial Menu + Quickslot (EN COURS)

- [x] Navigation par cran, lerp fluide, wrap correct
- [x] UpdateCenterInfo
- [x] Fix surbrillance 12h + drift
- [x] PopulateWeaponSlots (pont temporaire DiscoveredWeapons)
- [x] SwitchCategory Weapons/Magic
- [x] ValidateSelectedWeapon + EquipWeapon
- [x] Cancel bouton B (IA_UI_Radial_Cancel)
- [ ] **Quickslot POC mecanique** : assigner sort -> declencher via fleches ↑←→
- [ ] **Quickslot HUD minimal** : afficher 3 icones dans le HUD

---

### J-A/C/D -- Nettoyage rapide (1 session)

- [ ] **J-A** : Supprimer BP_PlatformingGameMode via Content Browser
- [ ] **J-C** : Verification et consolidation IMC (creer IMC_UI, clean IMC_Prototype)
- [ ] **J-D** : Reorganisation dossier Enemies via Content Browser

---

### J-lock -- Revision Lock-On

- [ ] Audit complet systeme existant
- [ ] Fix detection nouvelles cibles dans le radius (sans reset manuel)
- [ ] Fix z-order indicateur lock (derriere le heros)
- [ ] Fix positionnement barres HP ennemis
- [ ] Decision : migrer / refactoriser / refaire from scratch ?

---

### J-15/16/17 -- Refonte Combat Armes

- [ ] **J-15** : Audit BP_ComboManagerComponent -- extensible ou refonte ?
- [ ] **J-16** : Architecture BP_WeaponType_Base
  - Classe mere abstraite par TYPE (Epee, Arc, Fléau, Lance...)
  - BP_Weapon_Base devient instance d'un type
  - ⚠️ Conditionne J-17/18/19/31/32
- [ ] **J-17** : POC Epee -- moveset complet (combo 3 coups, finisseur, coup charge)
  - Feedback combo : subtil, dans le monde (flash arme, posture) -- pas d'UI ✅ ACTE

---

### J-F -- SaveGame (avant J-18)

- [ ] Systeme SaveGame complet
  - Stats joueur, armes debloquees, sorts debloques
  - Progression hub, quetes
  - ⚠️ A faire avant J-18 pour ne pas complexifier le save apres

---

### J-18/19 -- Arc + Switching

- [ ] **J-18** : POC Arc
  - ✅ ACTE : munitions illimitees
  - Systeme de visee (lock-on oriente la fleche, visee libre sans lock)
  - Projectile BP, charge optionnelle
- [ ] **J-19** : Switching en combat
  - Conservation du combo si switching rapide ou reset ? (point ouvert)

---

### J-B/E -- Animations + Hit Flash (moins urgent)

- [ ] **J-B** : Consolidation animations en double
- [ ] **J-E** : Hit Flash ennemis finalise -- DMI au BeginPlay + M_Enemy_Base

---

### J-20/21/22/23 -- Compagnons PNJ

- [ ] **J-20** : Architecture IA alliee -- BP_AIController_Companion_Base
- [ ] **J-21** : Gestion formation (2 compagnons max, positions relatives)
- [ ] **J-22** : Compagnon combattant POC -- Luna
  - Actions via L2 (mapping PS5)
- [ ] **J-23** : Compagnon non combattant POC -- Lumina
  - Actions via R2 (mapping PS5)

---

### J-24/25/26 -- Corruption Magique

- [ ] **J-24** : BP_CorruptionComponent (0-100) + indicateur HUD
- [ ] **J-25** : Effets par seuil (25 / 50 / 75 / 100)
- [ ] **J-26** : Integration narrative (PNJ reagissent, sanctuaires purification)

---

### J-27/28/29 -- Ville Hub Evolutive

- [ ] **J-27** : Variable progression globale -- GameInstance (HubProgressionLevel)
- [ ] **J-28** : Actors conditionnels dans le niveau
- [ ] **J-29** : Systeme de forge -- BP_ForgeComponent (NPC Forgeron)
  - ⚠️ Conditionne J-31 (Equipement) et J-32 (Talent)

---

### J-30/31/32 -- Systeme de Progression

- [ ] **J-30** : Level general + stats de base
- [ ] **J-31** : Systeme d'equipement -- bonus % sur stats
- [ ] **J-32** : Arbre de talent par type d'arme

---

## Sessions creatives (intercalees selon envie)

Sessions de changement de rythme, sans pression de gameplay.
A planifier librement entre les jalons techniques.

- [ ] **J-MAP-1** : Creation niveau de test / prototype de zone (foret ? ruines ?)
  - Terrain de base, collisions, lighting
  - Pas besoin de finition -- juste assez pour tester le gameplay en situation
- [ ] **J-MAP-2** : Premiere zone jouable -- ville de l'Oracle (hub)
- [ ] **J-ART-1** : Sprites / textures -- personnages principaux (ComfyUI RTX 3080Ti)
- [ ] **J-ART-2** : Sprites / textures -- ennemis de base
- [ ] **J-ART-3** : Sprites / textures -- decors et props
- [ ] **J-MUS-1** : Theme principal + theme combat (composition ou integration)
- [ ] **J-MUS-2** : Ambiances par zone
- [ ] **J-MUS-3** : Musique de boss

---

## Points de design encore ouverts

- **Forge** : quel materiau / systeme de graines Mana exactement ?
- ~~**Arc** : munitions limitees ou tir libre ?~~ ✅ ACTE : munitions illimitees
- **Switching armes** : reset combo ou conservation ?
- **Corruption** : les sorts de soin corrompent-ils moins ou pas du tout ?
- **Compagnons** : les PNJ peuvent-ils mourir de facon permanente (hors choix moral) ?
- **Deites Loup et Colosse** : Salamandre ou Gnome pour le Loup ?
- **Flammy** : quel moment narratif debloque le voyage rapide ?
- **Touchpad PS5** : carte, journal, ou autre ?
- **Menu global** : pause complete ou Time Dilation 0 ?
- **Quickslot switch** : press = utiliser, hold = changer de page ?

---

## Historique

- Creation : 11/05/2026
- Derniere mise a jour : 13/05/2026
