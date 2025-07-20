\# 📄 Enemy Attack System – Collision \& Damage



Ce document décrit l’implémentation du système de collision d’arme ennemi et la transmission des dégâts au joueur via interface `BPI\_TakeDamage`.



---



\## 🔧 Composants utilisés



\### Côté Ennemi (`BP\_EnemyBase`)

\- \*\*`SpawnedWeapon`\*\* : référence vers l’arme spawnée dynamiquement.

\- \*\*`EquipWeapon`\*\* : fonction qui :

&nbsp; - Spawne une `WeaponClass` (BP\_Enemy\_Sword01).

&nbsp; - Attache dynamiquement l’acteur à `SkeletalMesh` sur le socket `HandGrip\_R`.



\### Côté Arme (`BP\_Enemy\_Sword01`)

\- \*\*`Box`\*\* : composant `BoxCollision` utilisé pour les overlaps.

\- `Bind Event to OnComponentBeginOverlap` vers `OnComponentBeginOverlap\_Event`.



---



\## ⚔️ Collision \& dégâts



\### Fonction `OnComponentBeginOverlap\_Event` (BP\_Enemy\_Sword01)

Déroulement :

1\. Vérifie que l’acteur touché ≠ Owner.

2\. Vérifie l’implémentation de `BPI\_TakeDamage`.

3\. Vérifie si `HasAlreadyHit` est false.

4\. Appelle `ReceiveDamage` via interface avec :

&nbsp;  - \*\*DamageAmount\*\* = `5.0`

&nbsp;  - \*\*Instigator\*\* = Self

&nbsp;  - \*\*Causer\*\* = Self

5\. Passe `HasAlreadyHit = true`



---



\## 📦 Activation de la collision



\### Fonctions dans `BP\_EnemyBase` :



\#### `EnableWeaponCollision`

\- Active les collisions `QueryOnly` sur `Box` de `SpawnedWeapon`.

\- Réinitialise `HasAlreadyHit = false`.



\#### `DisableWeaponCollision`

\- Coupe toutes les collisions sur `Box`.



\### Déclenchement via AnimNotifies :

\- `AN\_Enemy\_EnableCollision` → appelle `EnableWeaponCollision`

\- `AN\_Enemy\_DisableCollision` → appelle `DisableWeaponCollision`



---



\## 🛡️ Interface `BPI\_TakeDamage`



\### Fonction `ReceiveDamage` (implémentée dans `BP\_PlatformingCharacter`)

\- Applique les dégâts reçus au joueur.

\- Permet de découpler totalement le système de dégâts du type d’attaquant.



---



\## ✅ Conditions de bon fonctionnement



\- L’arme doit être bien attachée à `SkeletalMesh` (pas `Mesh`).

\- Les collisions du player doivent être configurées pour recevoir les overlaps de type `Pawn`.

\- Le `Box` de l’arme doit être positionné et dimensionné de façon crédible.

\- L’interface `BPI\_TakeDamage` doit être bien ajoutée dans les `Class Settings` du `BP\_PlatformingCharacter`.



---



\## 🧪 Résultat attendu



| Situation                        | Résultat attendu                        |

|----------------------------------|-----------------------------------------|

| L'ennemi lance une attaque       | La collision est activée temporairement |

| L’arme touche le joueur          | Le joueur reçoit des dégâts             |

| La collision sort du joueur      | La collision est désactivée automatiquement |

| La cible est déjà touchée        | Aucun effet (évite les doublons)        |



---



\## 🔄 Historique



\- \*\*Mise en place :\*\* 2025-07-04

\- \*\*Auteur :\*\* IA Ennemie – ARPG Blueprint

\- \*\*Statut :\*\* ✅ stable



