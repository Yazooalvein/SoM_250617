# Architecture Technique — Système de Dégâts

---

## 📌 Objectif du module

Décrire l'architecture du système de gestion des dégâts basé sur les collisions d'armes :
- 100 % local (non réseau)
- Interface dédiée pour les cibles recevables
- Système d'appel unifié depuis les armes
- Dispatcher `OnDeath` pour découplage des réactions
- Pipeline scalable compatible multi-armes et DataTables
- Aucun usage d'`ApplyDamage` / `AnyDamage` (évité volontairement)

---

## 🧩 Composants principaux

- **BP_Weapon_Base** (acteur de base des armes avec box de collision)
- **WeaponCollisionBox** (BoxCollision activée temporairement via montage)
- **TryDealDamage** (logique de validation + appel interface)
- **BPI_TakeDamage** (interface Blueprint pour tout acteur recevant des dégâts)
- **BP_Enemy_Base** (ennemi standard, implémente `ReceiveDamage`)
- **OnDeath** (Event Dispatcher déclenché à la mort)
- **DT_Weapons** (DataTable contenant les stats, y compris le `DamageAmount`)

---

## 📦 Structures & Variables clés

### **Variables dans BP_Weapon_Base**
- `WeaponCollisionBox` : composant de collision utilisé pendant l'attaque
- `TouchedActors` : liste des acteurs déjà touchés dans cette fenêtre d'attaque
- `CanDealDamage` : booléen indiquant si la collision est active

### **Fonction TryDealDamage**
- Valide :
  - Que le `OtherActor` est ≠ `Owner`
  - Que `CanDealDamage == true`
  - Que `OtherActor` n'est pas déjà dans `TouchedActors`
  - Que l'acteur implémente `BPI_TakeDamage`
- Appelle `ReceiveDamage` avec :
  - `DamageAmount` (depuis DT_Weapons via WeaponID)
  - `Instigator` = owner
  - `Causer` = self

### **Interface BPI_TakeDamage**
- Fonction : `ReceiveDamage(float DamageAmount, Actor Instigator, Actor Causer)`
- Décorrèle totalement la source et la cible des dégâts

### **Dans BP_Enemy_Base**
- `MaxHealth`, `CurrentHealth` : gestion de la vie
- `bIsDead` : statut de l'entité
- `OnDeath` : dispatcher notifiant la mort
- `ReceiveDamage` :
  - Affiche debug
  - Applique les dégâts
  - Vérifie la mort
  - Appelle `OnDeath` + `DestroyActor`

---

## 🔁 Pipeline de fonctionnement

### **1. Activation de la collision**
- `EnableWeaponCollision` est appelé par Notify (AnimMontage)
- `DisableWeaponCollision` est appelé par Notify (fin de frappe)
- L'arme devient capable de toucher via `WeaponCollisionBox`

### **2. Détection de collision**
- Sur `BeginOverlap`, appel de `TryDealDamage(OtherActor)`
- Si valide, appel de l'interface `ReceiveDamage`

### **3. Réception et réaction**
- L'ennemi réduit sa vie via `CurrentHealth -= DamageAmount`
- Si vie ≤ 0 :
  - `bIsDead = true`
  - Appelle le dispatcher `OnDeath`
  - `DestroyActor`

### **4. Bind dynamique externe**
- Tout système peut se binder à `OnDeath` pour réagir :
  - UI, score, loot, FX...

---

## 🛠️ Bonnes pratiques & patterns utilisés

- **Interface dédiée** : aucune dépendance au système natif réseau Unreal
- **Dispatchers** pour découpler les systèmes de réaction
- **Validation stricte** dans `TryDealDamage` (Owner, doublons, interface…)
- **DataTable** pour centraliser les données d'attaque (`DamageAmount`)
- **Aucune logique dupliquée dans les enfants (BP_Sword01, etc.)**

---

## 🗺️ TODO / Roadmap

- [ ] Ajouter des types de dégâts (ex : Feu, Poison, Critique…)
- [ ] Gérer les résistances ennemies et immunités spécifiques
- [ ] Intégrer FX/SFX/CameraShake à la réception des dégâts
- [ ] Ajouter animations de mort (ragdoll, blend out, etc.)
- [ ] Ajouter signal visuel de hit (clignotement, flash, etc.)
- [ ] Préparer une base commune pour le multijoueur (RPC)

---

## 🕒 Historique

- Création : 24/06/2025
- Implémentation initiale (armes → interface → dispatcher → destruction validée)
- Dernière mise à jour : 26/06/2025
- Nommage mis à jour : 15/05/2026 (J-Renommage)

---

## **Fin du doc — relu et validé par [à compléter]**
