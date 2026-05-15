# Architecture Technique — Weapons System

---

## 📌 Objectif du module

Décrire l'architecture et le pipeline complet du système d'armes :
- Gestion data-driven : struct FWeaponData + DataTable DT_Weapons
- Découverte, évolution, et stockage dynamique des armes par type
- Equipement, attachement et détachement sur le personnage
- Variables, Blueprints et process centraux liés aux armes

---

## 🧩 Composants principaux

- **DT_Weapons** (DataTable principale, type : FWeaponData)
- **BP_Weapon_Base** (parent commun, pipeline d'attache)
- **BP_Weapon_X** (enfant, cas particulier/override)
- **BP_SoM_HeroCharacter** (ou composant inventaire/arme)
- **FWeaponData** (struct data-driven, voir détail)
- **FDiscoveredWeapon** (struct pour stockage des armes découvertes)
- **Array<Name> DiscoveredWeapons** (liste dynamique des RowNames débloqués)
- **Variables d'état** : ChoosenWeapon, CurrentWeapon, CurrentWeaponID/Type/Level

---

## 📦 Structures & Variables clés

### **FWeaponData**
- RowName (Name) : identifiant unique (ex : Sword_01)
- WeaponType (EWeaponType) : type d'arme (Sword, Axe…)
- Level (int) : niveau d'évolution
- Mesh (SkeletalMesh)
- Icon (Texture2D)
- SocketName (Name)
- Stats (struct ou DataTable ref)
- WeaponBPClass (Class Reference)
- (Optionnel : Offset, Rotation, SFX/VFX…)

### **FDiscoveredWeapon**
- RowName (Name)
- Type (EWeaponType)
- Level (int)

### **Variables globales**
- **DiscoveredWeapons** (Array<Name> ou Array<FDiscoveredWeapon>)
- **SlotRowNames** (Array<Name> pour le radial)
- **ChoosenWeapon** (Name, l'arme sélectionnée via UI)
- **CurrentWeapon** (BP_Weapon_Base, arme actuellement attachée)
- **CurrentWeaponID / Level** (si utilisé pour filtrage combo/stats)

---

## 🔁 Pipeline de fonctionnement

1. **Découverte/évolution d'arme**
    - Lors de la découverte ou l'upgrade : ajoute/maj l'entrée dans DiscoveredWeapons.
    - Si une arme évolue : update le RowName/Level associé.

2. **Ouverture du menu radial**
    - Récupération dynamique des armes débloquées via DiscoveredWeapons.
    - Génération des arrays : SlotRowNames (RowName), SlotIcons (icon via DT_Weapons).
    - Alimentation dynamique des slots UI.

3. **Sélection d'une arme**
    - Lors de la validation dans le radial, transmet le RowName sélectionné à ChoosenWeapon.
    - Appel de la fonction d'équipement.

4. **Equipement/détachement**
    - Lookup dans DT_Weapons via RowName pour récupérer FWeaponData (mesh, socket, BPClass, offsets…).
    - Spawn du BP_Weapon_X via WeaponBPClass.
    - Attachement sur le socket du personnage, application des offsets/rotations si nécessaires.
    - Detach/destroy de l'arme précédente proprement.

5. **Lien combo/arme**
    - Mise à jour de l'ID/type/level pour le système combo lors de l'équipement.
    - Le système combo lit l'ID/type/level courant pour filtrer les combos accessibles.

---

## 🛠️ Bonnes pratiques & patterns utilisés

- **Data-Driven** : Ajout/suppression d'armes exclusivement via la DataTable, pas de duplication de Blueprint.
- **Pipeline modulaire** : séparation stricte des responsabilités (DataTable ↔ BP_Weapon_Base ↔ Character/Inventory).
- **Structs évolutives** : possibilité d'étendre FWeaponData pour ajout de champs (offset, rarity, upgrades…).
- **Synchronisation UI/arme** : menu radial auto-sync sur DiscoveredWeapons.

---

## 🗺️ TODO / Roadmap

- [ ] Ajouter support offset/rotation spécifique par arme dans FWeaponData et appliquer au spawn/attach.
- [ ] Préparer le pipeline d'intégration du système d'inventaire (ramassage, drop…)
- [ ] Intégrer feedback UI avancé lors de l'équipement (FX, SFX…)
- [ ] Factoriser le process multi-personnages (support IA, alliés…)
- [ ] (Bonus) Prévoir extension pour les upgrades, rarity, skills liés à l'arme.

---

## 🕒 Historique

- Création : 24/06/2025
- Nommage mis à jour : 15/05/2026 (J-Renommage)
