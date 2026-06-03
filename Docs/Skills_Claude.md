# Skills Claude -- Shadow of Mana

Ce fichier recense les skills Claude actifs pour le projet SoM,
ainsi que les skills recommandes a creer pour ameliorer le workflow.

Les skills sont des fichiers SKILL.md stockes dans `/mnt/skills/user/`
sur l'environnement Claude. Ils sont charges automatiquement quand
Claude detecte un declencheur correspondant dans la conversation.

Les versions de reference des skills sont stockees dans `Docs/Skills/`
sur ce repo. Copier le contenu dans `/mnt/skills/user/[nom]/SKILL.md` pour activer.

---

## Skills actifs

### `som-session-start`
**Declencheur :** "on travaille sur SoM", "lis le CLAUDE.md", "reprends le projet SoM"
**Role :** Protocole de demarrage de session. Lit CLAUDE.md + Journal, produit un resume
actionnable, verifie les regles critiques. Depuis 03/06/2026 : declenche automatiquement
`som-jalon-design` si Nico annonce un jalon technique.
**Fichier repo :** `Docs/Skills/som-session-start.md`
**Fichier local :** `/mnt/skills/user/som-session-start/SKILL.md`
**Version :** 2.0 (03/06/2026)

### `som-commit-protocol`
**Declencheur :** "mets a jour la doc", "committe", "note ca dans le journal", "pousse ca"
**Role :** Protocole de commit GitHub. Ordre exact des operations, format des entrees
de journal, checklist de fin de session. Depuis 03/06/2026 : checklist etendue avec
verification coherence fichiers d'archi et Project_Architecture_Index.
**Fichier repo :** `Docs/Skills/som-commit-protocol.md`
**Fichier local :** `/mnt/skills/user/som-commit-protocol/SKILL.md`
**Version :** 2.0 (03/06/2026)

### `som-jalon-design` -- NOUVEAU (03/06/2026)
**Declencheur :** "on attaque [NomJalon]", "on fait [NomJalon]", "prochaine etape c'est [NomJalon]"
**Role :** Phase de design obligatoire avant tout jalon technique. Force la lecture de
Decisions.md (Patterns Etablis), la verification de coherence documentaire, et la
production d'une fiche de design validee par Nico AVANT tout code.
**Fichier repo :** `Docs/Skills/som-jalon-design.md`
**Fichier local :** `/mnt/skills/user/som-jalon-design/SKILL.md`
**Version :** 1.0 (03/06/2026)

---

## Skills recommandes a creer

### `som-pie-validation` PRIORITE 1
**Declencheur :** "on teste en PIE", "valide PIE", "test PIE avant de committer"
**Role :** Checklist de validation PIE standardisee avant de clore un jalon.
Structure en 3 niveaux : cas nominal, cas limite (valeurs a 0/max, sequences rapides),
cas d'erreur (ref None, mort pendant Delay, overlap instantane).
**Valeur :** Evite de decouvrir des bugs en session suivante sur des jalons "valides".

### `som-blueprint-audit` PRIORITE 2
**Declencheur :** "audit du BP", "analyse ce blueprint", "qu'est-ce qui se passe dans X"
**Role :** Prompt standardise pour demander un audit T3D. Format de sortie normalise :
variables, fonctions exposees, flux exec principaux, fils morts, erreurs detectees.
**Valeur :** Format standardise = resultats comparables et plus faciles a lire.

### `som-debt-tracker` PRIORITE 3
**Declencheur :** "on reporte ca", "c'est une dette", "on fait ca en C2"
**Role :** Protocole de decision pour les dettes techniques. Classifie chaque dette :
bloquant C1 / bloquant PIE / dette standard / dette cosmetique.
Genere automatiquement la ligne de dette au bon format pour CLAUDE.md.
**Valeur :** Criteres objectifs pour "on fait maintenant ou on reporte ?".

---

## Procedure de mise a jour d'un skill

1. Modifier le fichier dans `Docs/Skills/[nom].md` sur le repo
2. Copier le contenu dans `/mnt/skills/user/[nom]/SKILL.md` sur l'environnement Claude
3. Mettre a jour la version et la date dans ce fichier

---

## Notes

- Un skill mal decrit ne se declenche pas -- la description doit contenir les phrases exactes que Nico utilise
- Les skills se declenchent par matching de la description sur la conversation
- Priorite d'activation : le skill le plus specifique l'emporte

---

*Derniere mise a jour : 03/06/2026*
