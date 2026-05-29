# Roadmap Gameplay — Shadow of Mana

Document de référence pour la planification complète du projet.
Mis à jour après chaque session de design ou de développement.

---

## Modules existants (état au 29/05/2026)

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
| Radial menu armes | ✅ VALIDE PIE | PopulateWeaponSlots depuis InventoryComponent, rotation sur arme equipee |
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
| Lore & Cast | ✅ DESIGN VALIDE enrichi | Structure actes, Armes Mana, Hub, Corruption heros -- Lore_ShadowOfMana.md |
| Archi armes/combo/inventaire | ✅ VALIDE PIE | ComboManager source verite, InventoryComponent, EquipWeapon refacto -- 29/05/2026 |

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

## Ordre de dépendances global (révisé 29/05/2026)

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
                                                                    └─> DESIGN-Lore ✅ enrichi 29/05
                                                                          └─> C1-WeaponArchitecture ✅ VALIDE PIE
                                                                                └─> C1-SwordMoveset
                                                                                      └─> C1-HUDCore
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

### ✅ DESIGN-Lore — DESIGN VALIDE enrichi (29/05/2026)

**Décisions actées :**
- Cast complet avec races (Humain, Celeste, Beastman Felin, Nain x2, DragonFolk, Sproutling, Beastman Loup)
- Fee = fragment ame soeur insuffle par Ondine -- noms Fee+Soeur a trouver ensemble ⚠️
- Sanctuaire d'Ombre = zone obligatoire milieu acte 1, revelation Corruption Phase 2
- Suivante (Beastman Felin) ≠ tribu du Garcon Loup (Beastmen Loups) -- races differentes
- Garcon Loup (sans deite) recoit Ondine en fin de jeu quand la soeur devient Deesse Mana
- Ordre deites provisoire : Lumina -> Luna -> Gnome -> Ombre -> Salamandre -> Sylphide -> Dryade -> Ondine
- Structure 4 actes : A1 monde brise, A2 restauration zones + Hub, A3 verite + soeur, A4 Demon Primordial
- Heros = seul humanoide impacte physiquement par Corruption -- Pretresse+Suivante le percoivent
- Armes Mana : amenees par la Deesse, trouvees deteriorees A1, restaurees par etapes forge + materiaux
- Hub non reconstruit a l'arrivee A2 -- se reconstruit zone par zone avec PNJs rencontres en route
- Liberation deite = changement esthetique visuel de la zone
- Soeur revelee vivante au boss fin A2 (General)
- Conflit Loup/DragonFolk : ancien, amplifie par cataclysme

**Spec complète :** Docs/Lore_ShadowOfMana.md

### ✅ C1-WeaponArchitecture + Refacto — COMPLET VALIDE PIE (29/05/2026)

**Décisions actées :**
- ComboManager = source de verite unique arme courante (HC.ChoosenWeapon supprime)
- BP_InventoryComponent cree (Content/Systems/Inventory/) -- DiscoveredWeapons migre depuis HC
- ComboManager.EquipWeapon(WeaponID, WeaponLevel) = point d'entree unique equipement
- InitComboTree allege : responsabilite unique (charger ComboStepMap)
- Switch arme en combo = reset combo complet (punition Dark Souls style)
- TenaciteEtat heros : base 25, cle supplementaire AttributeSet
- Rotation Radial corrigee a l'ouverture (TargetRotation depuis InventoryComponent)
- Dette curseur Radial position initiale -> C?-RadialRefacto

**Spec complète :** Docs/Architecture/Decisions.md

### C1-SwordMoveset — Moveset épée complet (PROCHAIN)
- [ ] Combo 3 coups légers, finisseur, coup chargé (heavy)
- [ ] RotateTowardLockTarget câblé avec lock-on
- [ ] TenaciteEtat : ajouter dans BP_AttributeSet_Base (base 25)
- [ ] BP_StatusEffectComponent (heros + ennemis)
- ⚠️ Nécessite C1-WeaponArchitecture ✅

### C1-HUDCore — Jauges HUD (PROCHAIN)
- [ ] Jauge Stamina
- [ ] Jauge Mana
- [ ] Jauge Essence
- [ ] Jauge Corruption
- ⚠️ Nécessite C1-SwordMoveset (TenaciteEtat + StatusEffect pour coherence)

### C1-SaveDesign / C1-BowPOC / C1-WeaponSwitching / C1-SFXCombat / C1-AnimationsPass1 / C1-MagicTreeModule
- Voir CLAUDE.md pour détails et ordre

---

## COUCHE 2 — Combat & Ennemis

### C2-SaveGame / C2-EnemyMesh / C2-EnemyAI / C2-EnemyTypes / C2-Boss1

Note : C2-EnemyTypes définira ResistanceElementaire et stats par type ennemi.

---

## COUCHE 3 — Monde & Navigation

### C3-MapTest / C3-MapHub / C3-MapStart / C3-Flammy / C3-ZoneTransition

Note C3-Flammy : debloque fin A3/A4, permet acces lieux inaccessibles.

---

## COUCHE 4 — Systèmes Narratifs & Progression

### C4-DialogueSystem / C4-Tutorial / C4-DeitiesSystem / C4-CorruptionSystem
### C4-MoralFlag / C4-HubState1/2/3 / C4-Companions / C4-QuestSystem
### C4-LoreCodex / C4-SisterReveal

Note C4 : Touchpad PS5 (carte/journal) à définir ici.
Note C4-HubState : 3 états Hub (arrivee A2 non reconstruit -> reconstruit progressivement -> complet).
Note C4-MoralFlag : choix General fin A2, consequences Suivante A4.

---

## COUCHE 5 — Forge & Équipement

### C5-ForgeSystem / C5-Equipment / C5-TalentTree

Notes C5 :
- C5-Equipment : prerequis niveau equipement, calibrage prix PO, duree buff Repas
- C5-ForgeSystem : Armes Mana (trouvees deteriorees A1), materiaux drop ennemis, paliers narratifs + materiaux = condition double, Forgeron actif tout le jeu

---

## COUCHE 6 — Audio & Feedback

### C6-SFXAmbiance / C6-SFXMagic / C6-Music1/2/3 / C6-AudioMix

---

## COUCHE 7 — UI/UX Complet

### C7-MainMenu / C7-OptionsMenu / C7-PauseMenu / C7-DeathScreen / C7-LoadingScreen
### C7-HUDPolish / C7-Localization

Note C7-HUDPolish : radial dedie objets consommables (ou integration radial existant).
Note C7-PauseMenu : pause complete confirmee (pas Time Dilation).

---

## COUCHE 8 — Qualité & Build

### C8-DebugPanel / C8-Act1Playtest / C8-Perf1/2 / C8-CrashSession / C8-Build1/2

---

## Sessions Créatives

| Session | Contenu |
|---------|---------|
| ART-Hero | LODs + correction 6 doigts + sockets (retopo 246K -> 10-15K) |
| ART-Enemies | Meshes ennemis (Knight + 1-2 types) |
| ART-Weapons | Assets armes Mana (Sword_01, 2HSword_01, Arc_01, Lance_01, Axe_01...) |
| ART-MagicIcons | Icônes déités (8 écoles) + icônes sorts |
| ART-NPC | Pretresse, Suivante, Forgeron placeholders |
| MAP-Test/Hub/Start | Maps terrain UE5 |
| MUS-1/2/3 | Thèmes musicaux (workflow Suno établi) |

---

## Points de Design Encore Ouverts

| Sujet | Lié à | Statut |
|-------|-------|--------|
| Noms de TOUS les personnages (Soeur + Fee ensemble ⚠️) | Session Noms | ❌ Ouvert |
| Nom de la ville hub (ref Wendel + Tsaata) | Session Noms | ❌ Ouvert |
| Cout Essence par niveau de deite | Session Lore Deites | ❌ Ouvert |
| Rituels de communion par deite | Session Lore Deites | ❌ Ouvert |
| Origine precise conflit Tribu Loup / DragonFolk | Session zones acte 2 | ❌ Ouvert |
| Structure zones acte 1 + placement Fontaines | Session zones acte 1 | ❌ Ouvert |
| Presence General avant boss A2 (Option A ou B) | Session lore A2 | ❌ En maturation |
| Circonstances mort Oracle | Session lore A3/A4 | ❌ En maturation |
| Histoire propre de Flammy | C3-Flammy | ❌ Ouvert |
| Effet narratif Fee Corruption=100 | Session Lore Fee | ❌ Ouvert |
| Aura visuelle Corruption >= 25 | ART ou C4 | ❌ Ouvert |
| Valeurs ResistanceElementaire par type ennemi | C2-EnemyTypes | ❌ Ouvert |
| Types Armes Mana -- liste complete | Session Armes Mana | ❌ Ouvert |
| Nombre d'etapes evolution par arme | Session Armes Mana | ❌ A calibrer |
| Prerequis niveau pour equiper | C5-Equipment | ❌ Ouvert |
| Duree buff Repas | C5-Equipment | ❌ Ouvert |
| Noms definitifs consommables (lore Seiken) | Session Noms/Lore | ❌ Ouvert |
| Radial dedie objets vs integration radial existant | C7-HUDPolish | ❌ Ouvert |
| Calibrage PO/Essence/prix marchands | Playtest acte 1 | ❌ Ouvert |
| Spec détaillée Fontaine de Fée | C1-SaveDesign | ❌ Ouvert |
| Compagnons : mort permanente hors choix moral ? | C4-Companions | ❌ Ouvert |
| Distribution future : Steam / itch.io / perso | C8-Build2 | ❌ Ouvert |
| Touchpad PS5 : carte, journal, autre ? | C4 | ⏳ Réservé C4 |
| Menu pause : Time Dilation ou pause complète ? | C7-PauseMenu | ✅ Résolu : pause complète |
| Corruption 75 : depuis début jeu ou dernière purge ? | Combat_StatusEffects | ✅ Résolu : depuis dernière purge |
| Garçon Loup : Salamandre ou Gnome ? | Lore_ShadowOfMana | ✅ Résolu : sans déité, reçoit Ondine |
| Colosse : Gnome confirmé ? | Lore_ShadowOfMana | ✅ Résolu : Gnome confirmé |
| Source de vérité arme courante : HC ou Component ? | C1-WeaponArchitecture | ✅ Résolu : ComboManager |
| Périmètre EquipWeapon/DiscoveredWeapons | C1-WeaponArchitecture | ✅ Résolu : InventoryComponent |
| Switching armes : reset combo ou conservation ? | C1-WeaponArchitecture | ✅ Résolu : reset complet (punition) |
| TenaciteEtat valeur de base heros | C1-WeaponArchitecture | ✅ Résolu : base 25 |
| BP_StatusEffectComponent : quand creer ? | C1-SwordMoveset | ✅ Résolu : C1-SwordMoveset |

---

## Sessions Design à Planifier

| Session | Contenu | Priorité |
|---------|---------|---------| 
| **Session Noms** | Tous les personnages -- Soeur ET Fee ENSEMBLE ⚠️, ville hub | Haute |
| **Session Lore Deites** | Rituels par deite, cout Essence, confirmation ordre | Haute |
| **Session zones acte 1** | Structure zones, Fontaines, enchaînement narratif | Haute |
| **Session zones acte 2** | Origine conflit Loup/DragonFolk, structure regions A2 | Moyenne |
| **Session Armes Mana** | Liste types armes, nombre etapes evolution, calibrage materiaux | Moyenne |
| **Session SaveDesign** | Fontaine de Fee detaillee, respawn, penalites mort | Moyenne |
| **Session Economie** | Calibrage PO/Essence, prix marchands, taux drops (apres playtest) | Basse |

---

## Historique

- Création : 11/05/2026
- Refonte complète : 14/05/2026
- Resynchro complète : 18/05/2026
- MAJ 28/05/2026 : session design complete -- Stats, Effets statut, Corruption Phase 1/2, Economie, Lore/Cast
- MAJ 28/05/2026 (correctif) : DESIGN-Lore ajoute modules, points ouverts nettoyes, session Noms ajoutee
- MAJ 29/05/2026 : C1-WeaponArchitecture COMPLET VALIDE PIE, DESIGN-Lore enrichi (structure actes/Armes Mana/Hub), 5 points ouverts resolus, sessions design zones A2 + Armes Mana ajoutees, modules tableau mis a jour
