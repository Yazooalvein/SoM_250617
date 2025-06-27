# Architecture Technique — Barre de Vie des Ennemis

---

## 📌 Objectif du module

Mettre en place un système d’UI localisé pour afficher dynamiquement la **barre de vie des ennemis** au-dessus de leur tête.  
Le widget s’actualise à chaque réception de dégâts et sera à terme contrôlé par un système de **visibilité contextuelle** (lock/dégâts récents).

---

## 🧩 Composants principaux

- **UI_Enemy_HealthBar** (widget contenant la barre de vie)
- **WidgetComponent → Widget_HealthBar** (dans `BP_EnemyBase`)
- **BP_EnemyBase** (acteur ennemi implémentant l’interface `ReceiveDamage`)
- **Fonction SetHealthPercent(float)** (dans le widget)
- **Variable EnemyHealthBarRef** (référence stockée dans l’ennemi)

---

## 📦 Variables & Fonctions clés

### Dans `UI_Enemy_HealthBar`

| Nom | Type | Description |
|-----|------|-------------|
| `HealthPercent` | Float | Valeur entre 0.0 et 1.0, utilisée pour afficher la vie |
| `SetHealthPercent(float)` | Fonction | Met à jour `HealthPercent` et redessine la `ProgressBar_Health` |

### Dans `BP_EnemyBase`

| Nom | Type | Description |
|-----|------|-------------|
| `EnemyHealthBarRef` | UI_Enemy_HealthBar | Référence initialisée dans le `BeginPlay` |
| `SetHealthPercent(Current / Max)` | Appel | Réactualise la barre à chaque modification de vie |

---

## 🧱 Structure du widget `UI_Enemy_HealthBar`

- `CanvasPanel_Root`
  - `Overlay`
    - `VerticalBox_HealthBar`
      - `Text_EnemyName` *(optionnel)*
      - `Border_Background`
        - `ProgressBar_Health`

### Détails :
- `ProgressBar_Health` : alignement `Fill`, height ≈ 20–30px, percent initial = 1.0
- `Draw Size` (côté WidgetComponent) : `400 x 80` recommandé
- `WidgetComponent` en `Screen Space`, pivot `(0.5, 1.0)`, `RelativeLocation.Z ≈ +160`

---

## 🔁 Pipeline d'intégration

### 1. **Initialisation dans `BP_EnemyBase`**

```blueprint
BeginPlay →
  Widget_HealthBar
    → Get User Widget Object
      → Cast to UI_Enemy_HealthBar
        → Promote to EnemyHealthBarRef
        → SetHealthPercent(CurrentHealth / MaxHealth)
```

### 2. **Mise à jour en jeu (ReceiveDamage)**

```blueprint
→ EnemyHealthBarRef → SetHealthPercent(Current / Max)
```

---

## ✅ Comportement actuel

| Cas | Affichage de la barre |
|-----|------------------------|
| Spawn ennemi | Barre affichée à 100% |
| Prise de dégâts | Barre mise à jour immédiatement |
| Lock/délock | Pas encore implémenté (prévu) |

---

## 🗺️ Roadmap locale

- [x] Intégration du widget dans chaque ennemi via WidgetComponent
- [x] Réception dynamique des dégâts → mise à jour visuelle
- [ ] Ajout de la logique de visibilité (lock actif ou dégâts récents)
- [ ] Effets visuels (fade, apparition, disparition)
- [ ] Gestion du nom/level de l’ennemi (si nécessaire)

---

## 🔗 Liens & docs associées

- [HUD_Architecture.md]  
- [Combat_Architecture.md]  
- [Damage_System_Architecture.md]  
- [UI_Architecture.md]  
- [Journal_Modifications_ARPG.md]  

---

## 🕒 Historique

- Création : 26/06/2025  
- Dernière mise à jour : 26/06/2025

---
