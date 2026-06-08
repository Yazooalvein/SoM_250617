# Roadmap Gameplay — Shadow of Mana

Document de reference pour la planification complete du projet.
Mis a jour apres chaque session de design ou de developpement.

---

## Vision des Cycles — Milestones jouables

Chaque cycle = un etat du jeu testable de bout en bout.
Les jalons a l'interieur d'un cycle utilisent un prefixe thematique (COMBAT-, SYS-, MAP-, etc.).

```
C1 — Proof of Concept jouable
     Couloir, epee, Lumina, 2-3 mobs, 1 boss, fontaine, save/respawn, corruption/essence draft
     => On peut jouer une session complete meme si tout est placeholder
     => PERIMETRE POC : mecaniques validees, valeurs calibrees en C2, assets placeholder OK

C2 — Premiere zone jouable
     Une zone quasi complete, 2-3 armes, 2-3 deites, ennemis types, forge draft, StatusEffects
     => On peut explorer, mourir, progresser dans une vraie zone

C3 — Contenu narratif draft
     Plusieurs zones, hub, compagnons (a definir en session C3), dialogues/quetes draft
     => On peut suivre un fil narratif de bout en bout meme sommaire

C4 — Alpha Test
     Acte 1 complet, polish suffisant pour faire tester a des externes
     => Premier vrai feedback joueur
```

---

## Modules existants (etat au 09/06/2026)

| Module | Etat | Notes |
|--------|------|-------|
| Stats (SetStatValue / OnStatChanged) | ✅ Stable | Architecture solide, ne bougera pas |
| HUD event-driven | ✅ VALIDE PIE | HP/ST/MP/Corruption/Essence -- HUD-Core complet |
| Iframes dash/roll | ✅ Stable | Via AnimNotify, Dark Souls style |
| Mort du joueur | ✅ Stable | bIsDead + OnPlayerDeath dispatcher |
| Flux mort/respawn | ✅ VALIDE PIE (C1 POC) | Fade + reset stats + TeleportTo PlayerStart -- LastFountainTransform en SYS-SaveGame |
| BP_EssenceDrop | ✅ VALIDE PIE (C1 POC) | Drop au sol uniquement -- mob porteur C2, destruction 2eme mort C2 |
| BP_EssenceOrb | ✅ VALIDE PIE (C1 POC) | Drop actif mort ennemi, vol automatique vers hero via VInterpTo |
| Lock-On | ✅ VALIDE PIE | COMBAT-LockOnRefacto complet 09/06/2026 |
| Strafe lock-on | ✅ VALIDE PIE | ABP_Manny_Platforming + BS_Unarmed_Strafe (placeholder) |
| Deplacement en lock-on | ✅ VALIDE PIE | Move() via CameraRotation, Rotation Rate -1 |
| Camera | ✅ VALIDE PIE | SpringArm regle, IA_Look dans PC, UpdateLockOnRotation V2 |
| Screen shake | ✅ VALIDE PIE | CS_HitReceived + CS_EnemyDeath |
| Knockback ennemi | ✅ VALIDE PIE | LaunchCharacter 400.0 depuis ReceiveDamage |
| Radial menu armes | ✅ VALIDE PIE | PopulateWeaponSlots depuis InventoryComponent, rotation sur arme equipee |
| Quickslot POC | ✅ POC | 3 slots operationnels |
| Combo system | ✅ VALIDE PIE | TMap + InitComboTree + LevelMin=0, attaque fonctionnelle |
| Sword_01 moveset | ✅ VALIDE PIE | Light x2 + Heavy x1, montages branches, TenaciteEtat dans AttributeSet |
| IA ennemis | ✅ POC | Behavior Tree + PawnSensing |
| Hit Flash joueur | ✅ Stable | M_Hero HitFlashAmount |
| Hit Flash ennemi | ❌ Abandonne | Decision 21/05 : screen shake + anim suffisent |
| Systeme de magie | ✅ VALIDE PIE | BP_MagicComponent + radial 2 niveaux + CastSpell valides PIE |
| Radial menu magie | ✅ VALIDE PIE | COMBAT-RadialMagie complet 25/05/2026 |
| Hero placeholder | ✅ PIE | Mesh Meshy + AccuRIG + retargeting Mannequin |
| TestBed | ✅ VALIDE PIE | Lvl_TestBed, BP_Enemy_TestBed, SFX placeholder |
| Collisions capsule | ✅ VALIDE PIE | CapsuleComponent Pawn = Block |
| IMC dedies (5 contextes) | ✅ VALIDE PIE | COMBAT-InputsUI complet -- swap OpenRadial/CloseRadial |
| Stats & Progression | ✅ DESIGN VALIDE | 7 stats, hybride, Essence+PO, formules, elements -- Stats_Progression.md |
| Effets de statut | ✅ DESIGN VALIDE | 8 effets par deite, interactions -- Combat_StatusEffects.md |
| Corruption Magique | ✅ VALIDE PIE | BP_CorruptionComponent, tracking deites, purge, barre HUD -- 31/05/2026 |
| EssenceMana (EssenceValue) | ✅ VALIDE PIE (C1 POC) | Perte mort + drop + pickup + HUD -- 02/06/2026 |
| Economie & Drops | ✅ DESIGN VALIDE | Double monnaie, Seiken drops, Mana, equipement -- Economy_Drops.md |
| Lore & Cast | ✅ DESIGN VALIDE enrichi | Structure actes, Armes Mana, Hub, Corruption heros -- Lore_ShadowOfMana.md |
| Archi armes/combo/inventaire | ✅ VALIDE PIE | ComboManager source verite, InventoryComponent, EquipWeapon refacto -- 29/05/2026 |
| Save System | ✅ VALIDE PIE | BPI_Saveable, BP_SaveGame_SoM, flux fontaine/respawn -- 03/06/2026 |
| SYS-StatSystem | ✅ VALIDE PIE | TMap stats, Option B GetStatValue -- 04/06/2026 |
| ENEMY-DropSystem | ✅ VALIDE PIE | BP_EssenceOrb vol auto + BP_ItemDrop stub -- 06/06/2026 |
| UI-FountainMenu | ✅ VALIDE PIE | BPI_Interactable, mini-menu fontaine, SetInputModeUIOnly -- 07/06/2026 |
| COMBAT-LockOnRefacto | ✅ VALIDE PIE | BPI_Lockable, refacto complete, HP bars hide/show -- 09/06/2026 |

---

## CYCLE 1 — Proof of Concept jouable

**Objectif :** couloir → 2-3 mobs → fontaine → arene boss. Epee + Lumina. Corruption et Essence en draft. Pas de son ni d'anim avancee. On teste la synergie des mecaniques.

**Philosophie POC C1 :** chaque jalon vise la mecanique validee en PIE, pas le polish. Les valeurs sont placeholder, les assets sont placeholder, les animations sont placeholder. Tout ce qui est marque "POC" sera enrichi en C2.

### Jalons completes C1

| Jalon | Statut | Date | Mode |
|---|---|---|---|
| COMBAT-LockOn | ✅ VALIDE PIE | 15/05/2026 | -- |
| COMBAT-Camera | ✅ VALIDE PIE | 17/05/2026 | -- |
| COMBAT-LockMove | ✅ VALIDE PIE | 18/05/2026 | -- |
| COMBAT-ComboFix | ✅ VALIDE PIE | 18/05/2026 | -- |
| COMBAT-CollisionFix | ✅ VALIDE PIE | 18/05/2026 | -- |
| COMBAT-HitFeel | 🔧 PARTIEL | 18/05/2026 | knockback+shake OK, gamepad+hitstop reportes C2 |
| COMBAT-HitFlashEnemies | ❌ ABANDONNE | 21/05/2026 | -- |
| COMBAT-InputsUI | ✅ VALIDE PIE | 23/05/2026 | -- |
| MAGIC-RadialMagie | ✅ VALIDE PIE | 25/05/2026 | -- |
| MAGIC-ProgressionDesign | ✅ DESIGN VALIDE | 25/05/2026 | -- |
| MAGIC-DataLayer | ✅ VALIDE PIE | 25/05/2026 | -- |
| MAGIC-UnlockSystem | ✅ VALIDE PIE | 27/05/2026 | -- |
| COMBAT-CleanupDettes | ✅ COMPLET | 27/05/2026 | -- |
| DESIGN-StatsProgression | ✅ DESIGN VALIDE | 28/05/2026 | -- |
| DESIGN-StatusEffects | ✅ DESIGN VALIDE | 28/05/2026 | -- |
| DESIGN-Corruption | ✅ DESIGN VALIDE | 28/05/2026 | -- |
| DESIGN-Economy | ✅ DESIGN VALIDE | 28/05/2026 | -- |
| DESIGN-Lore | ✅ DESIGN VALIDE enrichi | 29/05/2026 | -- |
| COMBAT-WeaponArchitecture | ✅ VALIDE PIE | 29/05/2026 | -- |
| DESIGN-WeaponProgression | ✅ DESIGN VALIDE | 30/05/2026 | -- |
| HUD-Core | ✅ VALIDE PIE | 31/05/2026 | -- |
| DESIGN-SaveDesign | ✅ DESIGN VALIDE | 31/05/2026 | -- |
| COMBAT-SwordMoveset | ✅ VALIDE PIE | 31/05/2026 | -- |
| SYS-CorruptionSystem | ✅ VALIDE PIE | 31/05/2026 | Calibrage +5/sort = POC, affinage SESSION-Economie |
| SYS-EssenceMana | ✅ VALIDE PIE | 02/06/2026 | POC : drop au sol uniquement, respawn PlayerStart, drop indefini |
| SYS-SaveGame | ✅ VALIDE PIE | 03/06/2026 | BPI_Saveable, BP_FountainComponent, flux save/load/respawn |
| INFRA-BlueprintSnapshotLayer | ✅ COMPLET | 04/06/2026 | -- |
| SYS-StatSystem | ✅ VALIDE PIE | 04/06/2026 | TMap stats, Option B GetStatValue, validation complete |
| ENEMY-DropSystem | ✅ VALIDE PIE | 06/06/2026 | BP_EssenceOrb vol auto + BP_ItemDrop stub C1 |
| UI-FountainMenu | ✅ VALIDE PIE | 07/06/2026 | BPI_Interactable, mini-menu, SetInputModeUIOnly |
| COMBAT-LockOnRefacto | ✅ VALIDE PIE | 09/06/2026 | BPI_Lockable, HP bars hide/show, plus d'erreurs pending kill |

### Jalons restants C1

| Jalon | Prefixe | Contenu | Mode POC C1 | Dependances |
|---|---|---|---|---|
| ENEMY-Base | ENEMY | Stats sur BP_Enemy_Base, ResistanceElementaire, HandleTargetDeath | POC : valeurs hardcodees, callback mort cible -- calibrage et types C2 | DESIGN-StatsProgression ✅, COMBAT-LockOnRefacto ✅ |
| ENEMY-Boss1 | ENEMY | 1 boss, 1-2 patterns simples | POC : gros mob avec saut + magie placeholder -- patterns enrichis C2 | ENEMY-Base |
| MAP-C1Level | MAP | Mini map couloir : spawn → mobs → fontaine → arene boss | POC : geometrie BSP ou kit, assets placeholder -- vraie zone C2 | UI-FountainMenu ✅, ENEMY-Boss1 |

**Critere de completion C1 :** la MAP-C1Level est jouable de bout en bout -- spawn, combattre, mourir, respawn a la fontaine, tuer le boss. Tout en placeholder, tout fonctionnel.

---

## CYCLE 2 — Premiere zone jouable

**Objectif :** une zone quasi complete, 2-3 armes (epee + arc + une autre), 2-3 deites, ennemis types avec resistances, forge draft, StatusEffects. On peut explorer, mourir, progresser.

| Jalon | Contenu |
|---|---|
| MAGIC-TreeModule | Arbre talents Lumina, deblocage sorts via noeuds. Effets placeholder en C1, vrais effets en C2. |
| ANIM-Pass1 | Rename ABP_Manny_Platforming -> ABP_Hero. Roll fonctionnel en lock-on (LaunchCharacter + animation visuelle). |
| COMBAT-BowPOC | Arc basique, 1 type de tir |
| COMBAT-WeaponSwitching | Switch epee/arc via Radial en combat |
| COMBAT-SFX | Sons placeholder combat |
| COMBAT-HitFeel-Full | Vibration gamepad, hitstop (complete le partiel C1) |
| SYS-StatusEffects | Quelques effets de base (Poison, Burn, Buff) testables en combat |
| SYS-ForgeSystem | Forge draft -- upgrade arme niveau 1→2, materiaux drops |
| SYS-EssenceMana-Full | Mob porteur Essence, destruction drop 2eme mort, calibrage valeurs |
| ENEMY-Types | 2-3 types ennemis avec stats differentes, ResistanceElementaire |
| ENEMY-AI-Pass1 | Comportements ennemis enrichis (distance, patrol, aggro) |
| ANIM-DeathMontage | AnimMontage mort reelle heros |
| MAP-Zone1 | Premiere vraie zone (territoire Gnome ou village heros) |
| MAGIC-Deities2-3 | Luna + Gnome deblocables, sorts placeholder |
| UI-RadialRefacto | Refonte curseur Radial, position initiale correcte |
| UI-FountainMenu-Polish | Polish UI mini-menu Fontaine : icones, navigation fluide, animations |
| ART-Enemies | Meshes ennemis basiques |

---

## CYCLE 3 — Contenu narratif draft

**Objectif :** plusieurs zones enchainables, hub, compagnons (mecanique a definir en session C3), dialogues et quetes en draft. On suit un fil narratif.

| Jalon | Contenu |
|---|---|
| MAP-Hub | Ville hub niveau 1 (non reconstruite) |
| MAP-Zone2+ | Zones supplementaires (Salamandre, Sylphide...) |
| NAR-DialogueSystem | Systeme dialogue draft |
| NAR-QuestSystem | Quetes draft (objectifs simples) |
| NAR-Companions | Compagnons IA (mecanique a definir) |
| NAR-HubState | Hub qui se reconstruit zone par zone |
| NAR-MoralFlag | Choix moral General fin A2 |
| SYS-SaveGame-Full | Save complete avec flags narratifs, etat monde |
| FORGE-Full | Forge complete avec Armes Mana et materiaux narratifs |

---

## CYCLE 4 — Alpha Test

**Objectif :** acte 1 complet jouable de bout en bout, polish suffisant pour feedback externe.

| Jalon | Contenu |
|---|---|
| MAP-Act1Complete | Toutes les zones A1 enchainables |
| AUDIO-Full | Musique + SFX complets |
| UI-Full | Menus, HUD polish, ecrans mort/chargement |
| QA-Playtest1 | Session de test externe, collecte feedback |
| BUILD-Alpha | Premier build distribuable |

---

## Sessions Creatives (intercalees librement)

| Session | Contenu |
|---------|---------|
| ART-Hero | LODs + correction 6 doigts + sockets (retopo 246K -> 10-15K) |
| ART-Enemies | Meshes ennemis (Knight + 1-2 types) |
| ART-Weapons | Assets armes Mana (Sword_01, 2HSword_01, Arc_01, Lance_01, Axe_01...) |
| ART-MagicIcons | Icones deites (8 ecoles) + icones sorts |
| ART-NPC | Pretresse, Suivante, Forgeron placeholders |
| ART-Fontaine | Vision : racines arbre Mana poussant a l'activation (Fee), Fee se reposant dans la Fontaine lors des interactions. A elaborer quand pipeline ART confirme. |
| MAP-Test/Hub/Start | Maps terrain UE5 |
| MUS-1/2/3 | Themes musicaux (workflow Suno etabli) |
| SESSION-Noms | Tous les personnages -- Soeur ET Fee ENSEMBLE ⚠️, ville hub |
| SESSION-LoreDeites | Rituels par deite, cout Essence, confirmation ordre |
| SESSION-ZonesA1 | Structure zones, Fontaines, enchainement narratif |
| SESSION-ZonesA2 | Origine conflit Loup/DragonFolk, structure regions A2 |
| SESSION-ArmesMana | Liste types armes, nombre etapes evolution, calibrage materiaux |
| SESSION-Economie | Calibrage PO/Essence, prix marchands, couts purge Corruption, montee Corruption par sort |

---

## Points de Design Encore Ouverts

| Sujet | Lie a | Statut |
|-------|-------|--------|
| Noms de TOUS les personnages (Soeur + Fee ensemble ⚠️) | SESSION-Noms | ❌ Ouvert |
| Nom de la ville hub (ref Wendel + Tsaata) | SESSION-Noms | ❌ Ouvert |
| Cout Essence par niveau de deite | SESSION-LoreDeites | ❌ Ouvert |
| Rituels de communion par deite | SESSION-LoreDeites | ❌ Ouvert |
| Origine precise conflit Tribu Loup / DragonFolk | SESSION-ZonesA2 | ❌ Ouvert |
| Structure zones acte 1 + placement Fontaines | SESSION-ZonesA1 | ❌ Ouvert |
| Presence General avant boss A2 (Option A ou B) | SESSION lore A2 | ❌ En maturation |
| Circonstances mort Oracle | SESSION lore A3/A4 | ❌ En maturation |
| Histoire propre de Flammy | C3 | ❌ Ouvert |
| Effet narratif Fee Corruption=100 | SESSION Lore Fee | ❌ Ouvert |
| Aura visuelle Corruption >= 25 | ART ou C3 | ❌ Ouvert |
| Valeurs ResistanceElementaire par type ennemi | ENEMY-Types (C2) | ❌ Ouvert |
| Types Armes Mana -- liste complete | SESSION-ArmesMana | ❌ Ouvert |
| Nombre d'etapes evolution par arme | SESSION-ArmesMana | ❌ A calibrer |
| Prerequis niveau pour equiper | FORGE-Full (C3) | ❌ Ouvert |
| Duree buff Repas | FORGE-Full (C3) | ❌ Ouvert |
| Noms definitifs consommables (lore Seiken) | SESSION-Noms/Lore | ❌ Ouvert |
| Calibrage PO/Essence/prix marchands | SESSION-Economie | ❌ Ouvert |
| Calibrage couts purge Corruption (75-99% et 100%) | SESSION-Economie | ❌ Ouvert |
| Calibrage montee Corruption par sort (+5 actuel) | SESSION-Economie | ❌ Ouvert |
| Cout Essence Se reposer (purge Corruption) en Fontaine | UI-FountainMenu (C1) | ❌ Ouvert |
| Compagnons : mecanique en combat + mort permanente ? | SESSION C3 | ❌ Ouvert |
| Distribution future : Steam / itch.io / perso | C4 | ❌ Ouvert |
| Touchpad PS5 : carte, journal, autre ? | C3/C4 | ⏳ Reserve C3/C4 |
| Vision ART Fontaine definitive | ART-Fontaine | ⏳ En maturation |
| Menu pause : pause complete ? | -- | ✅ Resolu : pause complete |
| Corruption 75 : depuis derniere purge ? | Combat_StatusEffects | ✅ Resolu : depuis derniere purge |
| Garcon Loup : deite ? | Lore_ShadowOfMana | ✅ Resolu : sans deite, recoit Ondine |
| Colosse : Gnome confirme ? | Lore_ShadowOfMana | ✅ Resolu : Gnome confirme |
| Source de verite arme courante | COMBAT-WeaponArchitecture | ✅ Resolu : ComboManager |
| Perimetre EquipWeapon/DiscoveredWeapons | COMBAT-WeaponArchitecture | ✅ Resolu : InventoryComponent |
| Switching armes : reset combo ? | COMBAT-WeaponArchitecture | ✅ Resolu : reset complet (punition) |
| TenaciteEtat valeur de base heros | COMBAT-SwordMoveset | ✅ Resolu : base 25, Float AttributeSet, FClamp(0,100) |
| StatusEffects : quand implementer ? | -- | ✅ Resolu : C2 (SYS-StatusEffects) |
| SaveDesign : spec Fontaine de Fee | DESIGN-SaveDesign | ✅ Resolu : voir SaveSystem.md |
| Slots de save | DESIGN-SaveDesign | ✅ Resolu : multi-slots inter-parties, 1 slot par partie |
| Essence au sol vs mob porteur | DESIGN-SaveDesign | ✅ Resolu : environnement=sol C1, mob porteur C2, boss=sol |
| PurgeCorruption semantique | SYS-CorruptionSystem | ✅ Resolu : remet a 0 (pas soustraction) -- CostAmount = futur cout Essence |
| EssenceValue : perte mort + recuperation | SYS-EssenceMana | ✅ Resolu VALIDE PIE (02/06/2026) -- POC C1 |
| MAGIC-TreeModule : perimetre C1 ? | -- | ✅ Resolu : reporte C2 -- Lumina 4 sorts suffit pour POC C1 |
| ANIM-Pass1 : perimetre C1 ? | -- | ✅ Resolu : reporte C2 -- dette technique, pas bloquant pour POC |
| Fontaine : trigger automatique ou interaction ? | UI-FountainMenu | ✅ Resolu : interaction volontaire, 1ere activation = regen/save sans menu |
| Fontaine : menu accessible partout ou lieu dedie ? | UI-FountainMenu | ✅ Resolu : Fontaine uniquement (style DS) |
| Essence : monnaie unique pour level/magie/purge ? | UI-FountainMenu | ✅ Resolu : oui, tension intentionnelle (style DS souls) |

---

## Historique

- Creation : 11/05/2026
- Refonte complete : 14/05/2026
- Resynchro complete : 18/05/2026
- MAJ 28/05/2026 : session design complete
- MAJ 29/05/2026 : C1-WeaponArchitecture COMPLET VALIDE PIE
- MAJ 31/05/2026 : refonte complete -- cycles milestones jouables
- MAJ 31/05/2026 : COMBAT-SwordMoveset + SYS-CorruptionSystem VALIDE PIE
- MAJ 02/06/2026 : SYS-EssenceMana VALIDE PIE
- MAJ 05/06/2026 : replanification C1 -- ENEMY-DropSystem + UI-FountainMenu ajoutes
- MAJ 07/06/2026 : ENEMY-DropSystem + UI-FountainMenu VALIDE PIE
- MAJ 09/06/2026 : COMBAT-LockOnRefacto VALIDE PIE -- 3 jalons restants C1
