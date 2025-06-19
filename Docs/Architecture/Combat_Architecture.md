# Architecture Technique — Combat System

---

## 📌 Objectif du module

Définir et centraliser toute la logique technique liée au système de combat :  
- Attaques (combo, light/heavy)
- Esquive, parade, gestion stamina
- Système Lock-On, ciblage dynamique
- Intégration pipeline stat system, animation, FX/SFX, UI

---

## 🧩 Composants principaux

- BP_CombatComponent (logique principale d’action/attaque)
- BP_CombatLockOnComponent (module Lock-On)
- AnimMontage_AttackLight/Heavy (animation de combat)
- BP_PlayerCharacter / BP_EnemyBase (utilisateurs du composant)
- EventDispatchers pour feedback UI, FX, etc.
- BP_WeaponBase (structure pour les armes)
- UI_LockOnIndicator, UI_DebugWidget (affichage/suivi)

---

## 📦 Variables, Fonctions & Structures clés

> **Basé sur l’itération précédente du projet (ancienne doc Combat System Architecture + LockOn).  
> Les méthodes, variables, structures, conventions et pipelines seront récupérés, revus et adaptés ici.**

---

## Gameplay de base

> Tout ce qui concerne la logique Dash/Roll/Jump, gestion stamina associée, flags de mouvement, VFX, etc. est désormais **centralisé dans le doc dédié : [BasicGameplay_Architecture.md]**.
>  
> Ce document “Combat” reste dédié à la logique d’attaque, lock-on, dégâts, enchaînements, IA ennemie, etc.

---

## 🔁 Pipeline de fonctionnement

1. Input “attaque/defense” reçu via Enhanced Input
2. Test de validité/action possible (canAttack, stamina, état du joueur…)
3. Exécution de l’anim, détection hit/collision, application effet
4. Consommation stat, envoi des feedbacks UI, FX, etc.
5. Gestion Lock-On dynamique, changement de cible, synchro caméra/indicateur

---

## 🗺️ Roadmap locale

- [ ] Récupérer les composants Combat/LockOn du précédent projet
- [ ] Adapter à la logique Enhanced Input/ABP du nouveau template
- [ ] Refactor de la gestion des combos et de la synchro avec le Stat System
- [ ] Préparer la base pour extension magie, armes multiples, effets spéciaux

---

## 🔗 Liens & docs associées

- [Journal_Modifications.md]
- [Project_Architecture_Index.md]
- [Présentation_Générale_du_Projet.md]
- [Stats_Architecture.md]
- [UI_Architecture.md]
- [RadialMenu_Architecture.md]

---

## 🕒 Historique

- Création : 17/06/2025
- Dernière mise à jour : [19/06/2025]

---
