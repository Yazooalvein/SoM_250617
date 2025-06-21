# Architecture Technique — LockOn System

---

## 📌 Objectif du module

Décrire l’architecture technique et l’intégration du système LockOn :
- Ciblage dynamique d’ennemis
- Switching de cible (manuel et auto)
- Intégration avec le PlayerController, la caméra, le feedback UI
- Système compatible manette/clavier, full Blueprint
- Conformité avec le pipeline ARPG et la logique pause/stat/inputs

---

## 🧩 Composants principaux

- **BP_CombatLockOnComponent** : Composant principal ajouté au PlayerCharacter
- **BP_PlayerController** : Gère l’input LockOn, le relais d’événements, l’appel aux fonctions du composant, la gestion caméra
- **BP_PlayerCameraManager** : (optionnel) Pour la configuration avancée des limites caméra (pitch min/max)
- **UI_LockOnIndicator** : Widget optionnel pour l’affichage visuel du lock sur la cible
- **Struct FLockOnData** : (optionnel/à généraliser) Pour stocker les infos sur chaque cible (référence, distance, état)

---

## 📦 Variables, Fonctions & Structures clés

### **Variables principales**
- `bIsLockedOn` (bool) : Lock actif/inactif
- `CurrentTarget` (Actor Reference) : Cible actuellement verrouillée
- `LockOnCandidates` (Array<Actor>) : Liste des cibles potentielles
- `LockOnRange` (float) : Rayon de recherche
- `LockOnAngle` (float) : Angle de détection
- `SwitchCooldown` (float) : Délai min entre deux changements de cible
- `LockOnPitchMin` (float) : Limite verticale basse caméra en LockOn (ex : -60)
- `LockOnPitchMax` (float) : Limite verticale haute caméra en LockOn (ex : +60)

### **Fonctions publiques**
- `ActivateLockOn()` : Active/désactive le lock
- `DetectAvailableTargets()` : Met à jour la liste de cibles valides autour du joueur
- `SelectInitialTarget()` : Sélectionne la meilleure cible
- `SwitchLockOnTarget(Direction)` : Switch de cible manuellement (gauche/droite)
- `AutoSwitchTarget()` : Sélectionne automatiquement une nouvelle cible si la current n’est plus valide
- `ClearLockOn()` : Désactive le lock, reset UI
- `UpdateLockOnCamera()` : Gère la rotation caméra et le clamp pitch pendant le lock

---

## 🔁 Pipeline de fonctionnement

1. **Activation**  
   - Input LockOn (IMC), appel `ActivateLockOn()`
   - Recherche de cibles via `DetectAvailableTargets()`
   - Sélection, passage en mode LockOn si cible trouvée

2. **Pendant LockOn**
   - Tick ou Event UpdateLockOnCamera :
     - Caméra suit la cible en Yaw (horizontal), mais laisse Pitch libre
     - Pitch est **clampé** entre `LockOnPitchMin` et `LockOnPitchMax`
     - **Pitch normalisé** (si Pitch > 180, alors Pitch - 360) AVANT clamp
     - Si CurrentTarget devient invalide (hors range, morte, etc.) :
        - Appel `DetectAvailableTargets()` puis `AutoSwitchTarget()`
        - Si aucune cible valide, appel `ClearLockOn()`
   - UI/indicator actif tant que lock maintenu

3. **Switch manuel**
   - Input dédié (gauche/droite), appel `SwitchLockOnTarget(Direction)`
   - Liste de cibles **actualisée à chaque switch** (nouvel overlap/sphere check)

4. **Désactivation**
   - Input (ou perte de cible), appel `ClearLockOn()`
   - UI retirée, caméra rendue au contrôle classique

---

## 🗺️ Roadmap locale / TODO

- [ ] **Système d’auto-unlock** : Ajout d’une désactivation automatique si la cible sort du range ou meurt
- [ ] **Refactor struct FLockOnData** : Pour stocker plus d’infos par cible (état, type, distance…)
- [ ] **Intégration avancée UI** : Ajout de feedback visuel, indication directionnelle, warning si aucune cible, etc.
- [ ] **Gestion fine du Switch Auto** : Règle de priorité (plus proche, sur l’écran, etc.)
- [ ] **Documentation exhaustive des events BP et du pipeline d’intégration avec le menu radial**
- [x] **Pitch camera** : Normaliser puis clamp pour garantir les bonnes bornes d’angle vertical
- [ ] **Centraliser la gestion des inputs LockOn dans l’IMC** pour faciliter l’édition future

---

## 🔗 Liens & docs associées

- [UI_Architecture.md]
- [Journal_Modifications_ARPG.md]
- [Project_Architecture_Index.md]
- [RadialMenu_Architecture.md] (pour l’intégration UI)
- [IMC_ARPG_Main] (mappings d’input)

---

## 🕒 Historique

- Création : 19/06/2025
- Mise à jour : 19/06/2025 (import Shadow of Mana, pipeline LockOn, gestion du pitch normalisé/clampé)

---
