# Architecture Technique — Combat System

---

## 📌 Objectif du module

Définir et centraliser toute la logique technique liée au système de combat :
- Attaques (combo, light/heavy)
- Esquive, parade, gestion stamina
- Système Lock-On, ciblage dynamique
- Iframes (invincibilité pendant Dash/Roll)
- Intégration pipeline stat system, animation, FX/SFX, UI

---

## 🧩 Composants principaux

- BP_CombatComponent (logique principale d'action/attaque)
- BP_CombatLockOnComponent (module Lock-On)
- AnimMontage_AttackLight/Heavy (animation de combat)
- BP_PlatformingCharacter / BP_EnemyBase (utilisateurs du composant)
- EventDispatchers pour feedback UI, FX, etc.
- BP_WeaponBase (structure pour les armes)
- UI_LockOnIndicator (affichage/suivi)

---

## 📦 Variables, Fonctions & Structures clés

### BP_PlatformingCharacter — Variables combat

| Variable | Type | Description |
|---|---|---|
| bIsInvincible | Bool | Invincibilite active (iframes) |
| bIsDead | Bool | Mort du joueur |
| bIsDashing | Bool | Dash en cours |
| bIsRolling | Bool | Roll en cours |

### Pipeline iframes (Jalon #5 — 08/05/2026)

- **bIsInvincible** : flag unique partage par Dash et Roll
- **Dash** : SET bIsInvincible = true au debut → AN_EndDash (AnimNotify) → SET bIsInvincible = false
- **Roll** : SET bIsInvincible = true au debut → AN_EndRoll (AnimNotify) → SET bIsInvincible = false
- **ReceiveDamage** : premier check = Branch(bIsInvincible?) → True : exit (damage ignore)
- Duree iframe = duree animation, pilotee par AnimNotify (approche Dark Souls)
- Extensible : tout futur mouvement peut SET bIsInvincible sans toucher ReceiveDamage

### Pipeline ReceiveDamage (BPI_TakeDamage)

```
Event ReceiveDamage
→ Branch (bIsInvincible?) → True : exit
→ Branch (IsDead?) → True : exit
→ SetStatValue("HealthCurrent", HealthCurrent - DamageAmount)
→ HitFlash ON (0.12s) → HitFlash OFF
→ Branch (HealthCurrent == 0?)
  → True : SET bIsDead → DisableInput → AM_Death → Delay → CallOnPlayerDeath
```

### Pipeline dégâts par collision

- Pendant un montage d'attaque, une BoxCollision est activee sur l'arme via AnimNotify
- Si ennemi touche : appel ReceiveDamage via BPI_TakeDamage
- L'ennemi applique les degats et verifie son seuil de mort
- Si mort : dispatcher OnDeath → LoseAggro + destruction acteur
- Methode modulaire, sans ApplyDamage natif UE

---

## 🔁 Pipeline de fonctionnement

1. Input "attaque/defense" recu via Enhanced Input
2. Test validite/action possible (canAttack, stamina, etat joueur)
3. Execution de l'anim, detection hit/collision, application effet
4. Application degats via BPI_TakeDamage → ReceiveDamage → SetStatValue("HealthCurrent")
5. OnStatChanged fire → HUD mis a jour automatiquement
6. Consommation stat, feedbacks UI, FX
7. Gestion Lock-On dynamique, changement cible, synchro camera/indicateur

---

## 🗺️ Roadmap locale

- [x] Systeme de degats par collision (interface + dispatcher OnDeath)
- [x] HitFlash joueur (M_Hero HitFlashAmount, flash 0.12s)
- [x] Iframes dash/roll (bIsInvincible, pilote par AnimNotify) — 08/05/2026
- [x] ReceiveDamage → SetStatValue pour notifier le HUD — 10/05/2026
- [ ] Hit Flash ennemis
- [ ] Recuperer composants Combat/LockOn du precedent projet
- [ ] Refactor gestion combos et synchro Stat System
- [ ] Preparer base pour magie, armes multiples, effets speciaux

---

## 🔗 Liens & docs associées

- [Journal_Modifications.md]
- [Project_Architecture_Index.md]
- [Stats_Architecture.md]
- [BasicGameplay_Architecture.md]
- [UI_Architecture.md]

---

## 🕒 Historique

- Création : 17/06/2025
- Dernière mise à jour : 10/05/2026

---
