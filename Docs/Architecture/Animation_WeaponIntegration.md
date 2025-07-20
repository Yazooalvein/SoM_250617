\# Animation\_WeaponIntegration.md



> Gestion des animations dépendantes des armes via `Blend Pose by Enum` et `DataTable`.



---



\## 🎯 Objectif



Permettre à chaque type d’arme d’avoir ses propres animations (Idle, Walk/Run, etc.) sans dupliquer l’AnimBP, et en conservant une architecture évolutive.



---



\## ⚙️ Fonctionnement global



\### 1. Données définies dans la `DT\_Weapons`



Chaque ligne d’arme dans la `DataTable` contient désormais :



\- Une référence `IdleAnim` (type : `Animation Sequence`)

\- Une référence `WalkRunBlendspace` (type : `Blendspace`)

\- Un champ `EWeaponType` (enum : `Unarmed`, `Sword`, `2HSword`, etc.)



\### 2. Utilisation dans l’AnimBP



L'`AnimGraph` utilise un \*\*Blend Pose by Enum\*\* pour chaque état animé dépendant de l’arme :



\- \*\*Idle\*\* :

&nbsp; - `Blend Pose by Enum (EWeaponType)`

&nbsp; - Une entrée par type d’arme (`DefaultPose`, `SwordPose`, etc.)

&nbsp; - Chacune connectée à un `Sequence Player` ciblant l’anim correspondante



\- \*\*Walk / Run\*\* :

&nbsp; - Même principe mais avec des `Blendspace Player` pour chaque type d’arme



\### 3. Variable de pilotage : `WeaponType`



\- Exposée dans l’`AnimBP`.

\- Mise à jour dynamiquement depuis le `BP\_PlayerCharacter` lors de l’équipement :



```blueprint

Get Mesh → Get Anim Instance → Cast to ABP\_MyCharacter → Set WeaponType

```



---



\## 🧠 Bonnes pratiques



\- Toute nouvelle arme nécessite uniquement :

&nbsp; \* Ajout dans `EWeaponType`

&nbsp; \* Création de ses anims (`Idle`, `BS\_WalkRun`)

&nbsp; \* Entrée dans `DT\_Weapons` avec les références nécessaires

\- Aucune logique custom ou duplication de blueprint.



---



\## 🛠️ Notes techniques



\- `Blend Pose by Enum` permet un changement fluide et natif.

\- Utilisation de `Expose on Spawn` et de variables `Instance Editable` pour les transitions si besoin.

\- Le déséquipement remet la valeur `WeaponType` sur `Unarmed`.



---



\## 🔗 Liens vers autres docs



\- \[Weapons\_System\_Architecture.md](Weapons\_System\_Architecture.md)

\- \[UI\_Architecture.md](UI\_Architecture.md)

\- \[Combat\_System\_Architecture.md](Combat\_System\_Architecture.md)



---



\## 🕘 Historique



\- Création : 20/07/2025  

\- Auteur : \[Ton nom]



