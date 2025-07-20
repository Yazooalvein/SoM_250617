\# Architecture — IA Ennemi : Attaque de base



Version stable du 2025-07-01



---



\## 🎯 Objectif



Mettre en place une IA de type \*\*ennemi de mêlée basique\*\* capable :

\- de détecter le joueur via `PawnSensing`,

\- de s’approcher du joueur via `MoveTo`,

\- d’attaquer avec une animation `Montage` si le joueur est dans le `AttackRadius`,

\- de se désengager si le joueur s’éloigne (`LoseAggroRadius`).



---



\## 🧠 Blackboard (BB\_enemy)



| Clé              | Type   | Description                                 |

|------------------|--------|---------------------------------------------|

| `TargetActor`    | Object | Acteur poursuivi par l’IA                   |

| `HomeLocation`   | Vector | Position d’origine de l’ennemi              |

| `HasAggro`       | Bool   | Si l’ennemi est en état d’aggro             |

| `IsInAttackRange`| Bool   | Mise à jour par `BTService\_CheckAggroDistance` |



---



\## 🧩 Behavior Tree



\### Arborescence



```

Selector

├── Sequence "AggroBehavior"

│   ├── BTService\_CheckAggroDistance

│   ├── MoveTo (TargetActor)

│   └── BTTask\_PerformAttack

└── MoveTo (HomeLocation)

```



---



\## 🔄 Service : `BTService\_CheckAggroDistance`



Fréquence : 0.4 – 0.6 s (aléatoire)



\### Rôle :

\- Vérifie la distance entre le joueur (`TargetActor`) et l’ennemi.

\- Met à jour la clé `IsInAttackRange`.



```plaintext

Distance = GetDistanceTo(TargetActor)



If Distance <= AttackRadius:

&nbsp;   Set IsInAttackRange = true

Else:

&nbsp;   Set IsInAttackRange = false

```



---



\## 🔁 Fonction : `PerformAttack` (`BP\_EnemyBase`)



```plaintext

PerformAttack():

\- If IsAttacking → return

\- Set IsAttacking = true

\- SetActorRotation(FindLookAtRotation(Self, TargetActor))

\- GetAnimInstance → Montage Play (AM\_Light\_Sword)

\- Delay = AnimMontage Length

\- Set IsAttacking = false

```



Le montage est joué via `GetAnimInstance → Montage Play` (pas `PlayAnimMontage` direct).



---



\## 🎮 Animation



\- Le montage utilise le slot `DefaultSlot`.

\- Le slot doit être connecté dans l’`AnimGraph` :



```plaintext

StateMachine

&nbsp; ↓

Slot "DefaultSlot"

&nbsp; ↓

OutputPose

```



---



\## 🧭 Contrôle de la rotation



Assuré par le `CharacterMovementComponent` et configuré dans `AIController` :



```plaintext

OrientRotationToMovement = true

UseControllerRotationYaw = false

RotationRate = (0, 540, 0)

```



Initialisé dynamiquement dans `BP\_AIController\_Enemy\_Base` :



```plaintext

Event OnPossess:

→ Cast to BP\_EnemyBase

→ Get CharacterMovement

→ Set OrientRotationToMovement = true

→ Set RotationRate (Z = 540)

```



---



\## ✅ Résultat attendu



| Situation                  | Comportement                           |

|---------------------------|----------------------------------------|

| Joueur entre dans `AttackRadius` | Ennemi attaque via Montage         |

| Joueur reste en portée     | `IsAttacking` empêche la répétition    |

| Joueur sort de portée      | Ennemi revient à `MoveTo` ou désaggro  |



---



\## 🔧 Extensions prévues



\- Activation d’une `BoxCollision` sur l’arme via Notifies.

\- Interface `BPI\_TakeDamage` pour appliquer les dégâts au joueur.

\- Ajout de stagger, feedback FX, hit animation.

\- Blocage par bouclier, interruption, variations d’attaque.



---



\## 🕘 Historique



\- Mise en place initiale : 2025-07-01  

\- Auteur : IA ennemie — ARPG Blueprint  

\- Statut : ✅ stable



