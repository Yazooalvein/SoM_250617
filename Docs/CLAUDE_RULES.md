# Règles de collaboration Claude ↔ GitHub

## RÈGLE ABSOLUE — Commits sur les docs

**Claude ne commit JAMAIS sans avoir d'abord récupéré le SHA actuel du fichier.**

Procédure obligatoire avant tout commit :
1. `get_file_contents` sur le fichier → récupérer le SHA courant
2. Vérifier que le contenu récupéré correspond à ce qu'on attend
3. Seulement ensuite : `create_or_update_file` avec le SHA exact

**Claude ne commit JAMAIS en milieu de session de dev.**
- Les commits de doc se font UNIQUEMENT quand le dev demande explicitement une mise à jour
- Jamais de commit "préventif" ou "de fin de conversation" sans confirmation
- Si le dev dit "je vais commiter", Claude attend et ne touche à rien

**En cas de doute sur l'état du repo :**
- Claude demande : "Est-ce que tu as des modifications non commitées en local ?"
- Si oui : Claude attend que le dev commite d'abord
- Claude ne commit jamais par-dessus des modifications locales non pushées

## Pourquoi cette règle existe

Claude a causé des conflits en commitant des versions de fichiers
sans connaître l'état local du dev. Le dev a dû tout reprendre manuellement.
Ce n'est pas acceptable. Le repo appartient au dev, pas à Claude.

## Workflow correct

```
Dev travaille en local
  ↓
Dev dit "mets à jour la doc"
  ↓
Claude : get_file_contents → vérifier SHA
  ↓
Claude : create_or_update_file avec SHA correct
  ↓
Claude confirme le commit
```

## Historique des incidents

- 25/05/2026 : Claude a committé Roadmap et Decisions pendant une session active,
  écrasant les modifications locales du dev. Le dev a dû tout reprendre manuellement.
