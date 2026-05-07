# CLAUDE.md -- Shadow of Mana / Contexte IA

Ce fichier est lu par Claude au debut de chaque session pour retrouver le contexte du projet rapidement.

---

## Projet

- **Nom** : Shadow of Mana (SoM)
- **Genre** : ARPG Blueprint Only, inspire Secret of Mana + Dark Souls
- **Developpeur** : Nico (GitHub : Yazooalvein)
- **Repo** : https://github.com/Yazooalvein/SoM_250617
- **Moteur** : Unreal Engine 5.6 (migration UE5.7 + UnrealClaude prevue)

---

## Setup technique Claude <> Projet

- **Claude Desktop** + plugin **UnrealGenAISupport** (MCP `unreal-handshake`)
  - Python 3.14 officiel (C:/Users/nmarc/AppData/Local/Programs/Python/Python314/)
  - fastmcp v0.9 (downgrade necessaire)
  - Socket server port 9877, auto-start active dans Project Settings
- **GitHub MCP** : node.exe --use-system-ca + NODE_TLS_REJECT_UNAUTHORIZED=0
  - Token Classic scope `repo` complet
  - Writes GitHub via script Python urllib (contournement SSL)
- **Claude** : plan Pro, memoire activee

---

## Conventions de travail

### Git
```
git add .
git commit -m "description courte et coherente"
git push
```
-> Nico pushe d'abord, puis Claude committe le journal

### Journal
- Fichier : `Docs/Journal_Modifications.md`
- Claude le met a jour apres chaque jalon via script Python urllib
- SHA recupere dynamiquement avant chaque commit

### Documentation
- Toute nouvelle feature -> doc dans `Docs/Architecture/`
- Index : `Docs/Project_Architecture_Index.md`

---

## Architecture clé (resume)

- **Personnage** : `BP_PlatformingCharacter` (Blueprint Only)
  - Stats via `BP_AttributeSet_Base` (ref : `AttributeSetRef`)
  - `bIsDead` (private) + `IsDead()` (public pure)
  - `OnPlayerDeath` dispatcher (sans params)
  - `OnStatChanged(StatName, NewValue)` dispatcher dans AttributeSet
- **GameMode** : `BP_SoM_GameMode` (`/Game/Core/`)
- **Ennemis** : `BP_EnemyBase` -> `BP_AIController_Enemy_Base`
  - Behavior Tree + Blackboard
  - `LoseAggro()` pour desengagement
- **Combat** : `BPI_TakeDamage` + `BP_ComboManagerComponent`
- **Armes** : `DT_Weapons` + `BP_Weapon_Base`
- **UI** : `UI_HUD_Main`, `UI_Enemy_HealthBar`, `UI_LockOnIndicator`

---

## Roadmap actuelle

- [x] Setup MCP Claude Desktop <> Unreal
- [x] Hit Flash joueur (M_Hero HitFlashAmount)
- [x] Mort du joueur (bIsDead, OnPlayerDeath, AM_Death, LoseAggro)
- [x] OnStatChanged dispatcher
- [ ] Unification inputs dupliques (IA_Jump, IA_Move, IA_Look)
- [ ] Iframes dash/roll (bIsInvincible dans ReceiveDamage)
- [ ] Migration UE5.7 + UnrealClaude (session dediee)
- [ ] Setup ComfyUI generation textures/concepts (RTX 3080Ti)
- [ ] Hit Flash ennemis
- [ ] OnStatChanged -> bindings UI event-driven

---

## Comment demarrer une session

1. Nico donne le contexte : "on travaille sur Shadow of Mana, reprends le CLAUDE.md et le journal"
2. Claude lit ce fichier + `Docs/Journal_Modifications.md`
3. Claude fait un resume de l'etat du projet et propose la suite

---

## Notes techniques importantes

- UE5.6 : erreur threading Python (`Attempted to access Unreal API from outside the main game thread`) -> contournee via `execute_python_script`
- GitHub MCP writes echouent via le serveur MCP -> utiliser script Python urllib avec SSL desactive
- `BP_SoM_GameMode` cree via Python MCP, Default Pawn = BP_PlatformingCharacter
- Substrate material system desactive (UE5.6)
- Toutes les anims de mort sur SK_Mannequin, retargeter `RTG_NewRetargeter` disponible

---

*Derniere mise a jour : 07/05/2026*
