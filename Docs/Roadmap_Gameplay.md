# Roadmap Gameplay — Shadow of Mana

Document de référence pour la planification complète du projet.
Mis à jour après chaque session de design ou de développement.

---

## Modules existants (état au 28/05/2026)

| Module | État | Notes |
|--------|------|-------|
| Stats (SetStatValue / OnStatChanged) | ✅ Stable | Architecture solide, ne bougera pas |
| HUD event-driven | ✅ Stable | Zero polling, extensible |
| Iframes dash/roll | ✅ Stable | Via AnimNotify, Dark Souls style |
| Mort du joueur | ✅ Stable | bIsDead + OnPlayerDeath dispatcher |
| Lock-On | ✅ VALIDE PIE | J-LockOn complet + J-LockMove complet |
| Strafe lock-on | ✅ VALIDE PIE | ABP_Manny_Platforming + BS_Unarmed_Strafe (placeholder) |
| Déplacement en lock-on | ✅ VALIDE PIE | Move() via CameraRotation, Rotation Rate -1 |
| Caméra | ✅ VALIDE PIE | SpringArm réglé, IA_Look dans PC, UpdateLockOnRotation V2 |
| Screen shake | ✅ VALIDE PIE | CS_HitReceived + CS_EnemyDeath |
| Knockback ennemi | ✅ VALIDE PIE | LaunchCharacter 400.0 depuis ReceiveDamage |
| Radial menu armes | ✅ Stable | PopulateWeaponSlots, SwitchCategory, ValidateSelectedWeapon |
| Quickslot POC | ✅ POC | 3 slots opérationnels |
| Combo system | ✅ VALIDE PIE | TMap + InitComboTree + LevelMin=0, attaque fonctionnelle |
| IA ennemis | ✅ POC | Behavior Tree + PawnSensing |
| Hit Flash joueur | ✅ Stable | M_Hero HitFlashAmount |
| Hit Flash ennemi | ❌ Abandonné | Decision 21/05 : screen shake + anim suffisent |
| Système de magie | ✅ VALIDE PIE | BP_MagicComponent + radial 2 niveaux + CastSpell validés PIE |
| Radial menu magie | ✅ VALIDE PIE | C1-RadialMagie complet 25/05/2026 |
| Hero placeholder | ✅ PIE | Mesh Meshy + AccuRIG + retargeting Mannequin |
| TestBed | ✅ VALIDE PIE | Lvl_TestBed, BP_Enemy_TestBed, SFX placeholder |
| Collisions capsule | ✅ VALIDE PIE | CapsuleComponent Pawn = Block |
| IMC dédiés (5 contextes) | ✅ VALIDE PIE | C1-InputsUI complet -- swap OpenRadial/CloseRadial |
| Stats & Progression | ✅ DESIGN VALIDE | 7 stats, hybride, Essence+PO, formules, éléments -- Stats_Progression.md |
| Effets de statut | ✅ DESIGN VALIDE | 8 effets par déité, interactions -- Combat_StatusEffects.md |
| Corruption Magique | ✅ DESIGN VALIDE | Phase 1/2, lien Ombre, bonus Essence -- Combat_StatusEffects.md |
| Economie & Drops | ✅ DESIGN VALIDE | Double monnaie, Seiken drops, Mana, équipement -- Economy_Drops.md |
| Archi armes/combo | ⚠️ Dette | ChoosenWeapon (HC) redondant avec CurrentWeaponID (ComboManager) -- C1-WeaponArchitecture |

---

## Vue d'ensemble — Couches de développement

```
COUCHE 1 — Fondations gameplay        (en cours)
COUCHE 2 — Combat & Ennemis           (après fondations)
COUCHE 3 — Monde & Navigation         (en parallèle possible avec C2)
COUCHE 4 — Systèmes narratifs         (après monde + combat)
COUCHE 5 — Forge & Équipement         (après systèmes narratifs)
COUCHE 6 — Audio & Feedback           (C1-SFXCombat en C1, reste intercalé)
COUCHE 7 — UI/UX complet              (intercalé, avant build)
COUCHE 8 — Qualité & Build            (fin de développement)

Sessions créatives (ART / MUS / MAP) : intercalées librement.
```

---

## Ordre de dépendances global (révisé 28/05/2026)

```
[FAIT] J-LockOn -> J-Camera -> J-LockMove -> J-TestBed -> J-ComboFix
  └─> C1-CollisionFix ✅
        └─> C1-HitFeel (partiel)
              └─> C1-InputsUI ✅ VALIDE PIE
                    └─> C1-RadialMagie ✅ VALIDE PIE
                          └─> C1-MagicProgressionDesign ✅
                                └─> C1-MagicUnlockSystem ✅ VALIDE PIE
                                      └─> C1-CleanupDettes ✅
                                            └─> DESIGN-StatsProgression ✅
                                                  └─> DESIGN-StatusEffects ✅
                                                        └─> DESIGN-Corruption ✅
                                                              └─> DESIGN-Economy ✅
                                                                    └─> C1-WeaponArchitecture + Refacto
                                                                          └─> C1-SwordMoveset
                                                                                └─> C1-SaveDesign (spec)
                                                                                      └─> C1-BowPOC
                                                                                            └─> C1-WeaponSwitching
                                                                                                  └─> C2-SaveGame
                                                                                                        └─> C1-AnimationsPass1

C1-SFXCombat : peut démarrer dès maintenant
C1-HitFlashEnemies : ABANDONNE (21/05/2026)
```

---

## COUCHE 1 — Fondations gameplay

### ✅ J-LockOn — COMPLET VALIDE PIE (15/05/2026)
### ✅ J-Camera — COMPLET VALIDE PIE (17/05/2026)
### ✅ J-LockMove — COMPLET VALIDE PIE (18/05/2026)
### ✅ J-TestBed — COMPLET VALIDE PIE (18/05/2026)
### ✅ J-ComboFix — COMPLET VALIDE PIE (18/05/2026)
### ✅ C1-CollisionFix — COMPLET VALIDE PIE (18/05/2026)
### ❌ C1-HitFlashEnemies — ABANDONNE (21/05/2026)

### 🔧 C1-HitFeel — Feedback physique des coups (partiel)
- [x] Knockback VALIDE PIE
- [x] Screen shake VALIDE PIE
- [ ] Vibration gamepad
- [ ] Hitstop : reporté après C2-EnemyMesh + C1-SFXCombat

### ✅ C1-InputsUI — COMPLET VALIDE PIE (23/05/2026)
### ✅ C1-RadialMagie — COMPLET VALIDE PIE (25/05/2026)
### ✅ C1-MagicProgressionDesign — DESIGN VALIDE (25/05/2026)
### ✅ C1-MagicUnlockSystem — COMPLET VALIDE PIE (27/05/2026)
### ✅ C1-CleanupDettes — COMPLET (27/05/2026)
### ✅ DESIGN-StatsProgression — DESIGN VALIDE (28/05/2026)
### ✅ DESIGN-StatusEffects — DESIGN VALIDE (28/05/2026)
### ✅ DESIGN-Corruption — DESIGN VALIDE (28/05/2026)

### ✅ DESIGN-Economy — DESIGN VALIDE (28/05/2026)

**Décisions actées :**
- Double monnaie : Essence (progression, perdue mort) + PO (economie, stable)
- Drops : Essence + PO toujours, consommables + materiaux + coffres Seiken en aleatoire
- Consommables Seiken : 9 unites max par type, rechargeable Fontaine
- Materiaux forge : 3 tiers, non lies aux elements, forge narrative jalons narratifs
- Equipement : 3 slots (Casque, Armure, Accessoire) -- Defense + Resistance
- ManaMax separee de Magie, base 60, +8/niveau -- pas de regen auto
- Cout sorts : Base + (NiveauSort * Multiplicateur)
- Corruption Phase 1 plafond 50, Phase 2 plafond 100 apres revelation Hero/Ombre
- Corruption faiblesse a 75 = deite la plus utilisee (deterministe)
- Respawn Fontaine : ennemis normaux oui, boss jamais
- Sauvegarde : tout sauf Essence non depensee

**Spec complète :** Docs/Architecture/Economy_Drops.md

### C1-WeaponArchitecture + Refacto
- [ ] Audit BP_Weapon_Base, DT_Weapons, FWeaponData, BP_ComboManagerComponent
- [ ] Source de vérité unique arme courante
- [ ] Périmètre HC vs Component
- [ ] Ajouter CoeffArme + VitesseAttaque dans FWeaponData
- [ ] Ajouter nouvelles stats dans BP_AttributeSet_Base (Level, EssenceMana, PiecesOr, Corruption, ManaMax, ManaCurrent...)
- [ ] Ajouter stats ennemis enrichies sur BP_Enemy_Base
- [ ] Ajouter jauges HUD : Stamina, Mana, Essence, Corruption
- [ ] Implem minimale du refacto
- [ ] Doc de décision dans Decisions.md
- ⚠️ Conditionne C1-SwordMoveset, C1-BowPOC, C5-ForgeSystem, C5-TalentTree

### C1-SwordMoveset — Moveset épée complet
- [ ] Combo 3 coups légers, finisseur, coup chargé (heavy)
- [ ] RotateTowardLockTarget câblé avec lock-on
- [ ] BP_StatusEffectComponent (heros + ennemis)
- ⚠️ Nécessite C1-WeaponArchitecture

### C1-SaveDesign — Session design respawn & sauvegarde
- [ ] Spec détaillée Fontaine de Fée, respawn, ce qui est sauvegardé
- [ ] Livrable : spec SaveGame.md

### C1-BowPOC / C1-WeaponSwitching / C1-SFXCombat / C1-AnimationsPass1
- Voir CLAUDE.md pour détails

---

## COUCHE 2 — Combat & Ennemis

### C2-SaveGame / C2-EnemyMesh / C2-EnemyAI / C2-EnemyTypes / C2-Boss1

Note : C2-EnemyTypes définira ResistanceElementaire et stats par type ennemi.

---

## COUCHE 3 — Monde & Navigation

### C3-MapTest / C3-MapHub / C3-MapStart / C3-Flammy / C3-ZoneTransition

---

## COUCHE 4 — Systèmes Narratifs & Progression

### C4-DialogueSystem / C4-Tutorial / C4-DeitiesSystem / C4-CorruptionSystem
### C4-MoralFlag / C4-HubState1/2/3 / C4-Companions / C4-QuestSystem
### C4-LoreCodex / C4-SisterReveal

---

## COUCHE 5 — Forge & Équipement

### C5-ForgeSystem / C5-Equipment / C5-TalentTree

Notes C5 :
- C5-Equipment : prerequis niveau equipement, calibrage prix PO, duree buff Repas
- C5-ForgeSystem : materiaux exacts, prix forge, integration jalons narratifs

---

## COUCHE 6 — Audio & Feedback

### C6-SFXAmbiance / C6-SFXMagic / C6-Music1/2/3 / C6-AudioMix

---

## COUCHE 7 — UI/UX Complet

### C7-MainMenu / C7-OptionsMenu / C7-PauseMenu / C7-DeathScreen / C7-LoadingScreen
### C7-HUDPolish / C7-Localization

Note C7-HUDPolish : radial dedie objets consommables (ou integration radial existant).

---

## COUCHE 8 — Qualité & Build

### C8-DebugPanel / C8-Act1Playtest / C8-Perf1/2 / C8-CrashSession / C8-Build1/2

---

## Sessions Créatives

| Session | Contenu |
|---------|---------|
| ART-Hero | LODs + correction 6 doigts + sockets (retopo 246K -> 10-15K) |
| ART-Enemies | Meshes ennemis (Knight + 1-2 types) |
| ART-Weapons | Assets armes (Sword_01, 2HSword_01, Arc_01...) |
| ART-MagicIcons | Icônes déités (8 écoles) + icônes sorts |
| ART-NPC | Lumina, Luna, Athanor placeholders |
| MAP-Test/Hub/Start | Maps terrain UE5 |
| MUS-1/2/3 | Thèmes musicaux (workflow Suno établi) |

---

## Points de Design Encore Ouverts

| Sujet | Lié à |
|-------|-------|
| Source de vérité arme courante : HC ou Component ? | C1-WeaponArchitecture |
| Périmètre EquipWeapon/DiscoveredWeapons | C1-WeaponArchitecture |
| Switching armes : reset combo ou conservation ? | C1-WeaponSwitching |
| Cout Essence par niveau de deite | Session Lore Deites |
| Valeurs ResistanceElementaire par type ennemi | C2-EnemyTypes |
| BP_StatusEffectComponent : quand créer ? | C1-SwordMoveset |
| TenaciteEtat valeur de base heros | C1-SwordMoveset |
| Quand debloquer Corruption Phase 2 (revelation Ombre) ? | Session Lore Ombre |
| Effet narratif Corruption=100 (dialogue fee ?) | Session Lore Fee |
| Aura visuelle Corruption >= 25 | ART ou C4 |
| Faiblesse Corruption 75 : deite la plus utilisee sur quelle periode ? | A preciser |
| Prerequis niveau pour equiper | C5-Equipment |
| Duree buff Repas | C5-Equipment |
| Noms definitifs consommables (lore Seiken) | Session Lore |
| Radial dedie objets vs integration radial existant | C7-HUDPolish |
| Calibrage PO/Essence/prix marchands | Playtest acte 1 |
| Spec détaillée Fontaine de Fée (respawn, penalites) | C1-SaveDesign |
| Compagnons : mort permanente possible hors choix moral ? | C4-Companions |
| Garçon Loup : Salamandre ou Gnome ? | C4-DeitiesSystem |
| Flammy : quel jalon narratif débloque le voyage rapide ? | C3-Flammy |
| Menu pause : Time Dilation 0 ou pause complète ? | C7-PauseMenu |
| Touchpad PS5 : carte, journal, ou autre ? | C7-PauseMenu |
| Distribution future : Steam / itch.io / perso | C8-Build2 |

---

## Historique

- Création : 11/05/2026
- Refonte complète : 14/05/2026
- Resynchro complète : 18/05/2026
- MAJ 28/05/2026 : session design complete -- Stats, Effets statut, Corruption Phase 1/2, Economie Seiken, double monnaie, Mana, equipement
