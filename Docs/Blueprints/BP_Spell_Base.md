# BP_Spell_Base -- Snapshot

**Path UE5 :** `/Game/Systems/Magic/Core/BP_Spell_Base`
**Parent :** Actor
**Noeuds totaux :** 8
**Dernier snapshot :** 05/06/2026 -- Audit global

---

## Variables

| Nom | Type | Notes |
|---|---|---|
| Caster | BP_SoM_HeroCharacter_C* | |
| Target | Actor* | |
| SpellData | FSoM_SpellData | Donnees du sort depuis DT_Spells |

## Fonctions

| Nom | Notes |
|---|---|
| Execute() | Point d'entree -- appelle ApplyEffect |
| ApplyEffect() | Override par sous-classes |

## Sous-classes Lumina

| BP | Variables propres | ApplyEffect | Noeuds |
|---|---|---|---|
| BP_Spell_Heal | -- | HP regen via SetStatValue | 21 |
| BP_Spell_Attack | -- | Degats sur cible | 18 |
| BP_Spell_Buff | OriginalHealthMax:double | Boost HealthMax temporaire | 34 |
| BP_Spell_Debuff | OriginalMaxWalkSpeed:float | Slow cible | 31 |

## Dependances

**Appelle :** BP_AttributeSet_Base (SetStatValue)
**Spawn par :** BP_MagicComponent.CastSpell
