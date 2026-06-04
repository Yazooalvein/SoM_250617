# BP_Spell_Heal -- Snapshot

**Dernier snapshot :** 04/06/2026  
**Jalon :** SYS-StatSystem pre-audit  
**Path UE5 :** `Content/Systems/Magic/Spells/Lumina/BP_Spell_Heal`  
**Type :** Actor (Parent : BP_Spell_Base)  
**Variables propres :** aucune

---

## SetStatValue -- 1 appel dans ApplyEffect

```
Get Caster -> Cast HC -> Get AttributeSetRef
-> Get HealthCurrent + SpellData.EffectValues -> addition
-> Min(sum, HealthMax)   <- guard correct et fonctionnel
-> SetStatValue("HealthCurrent", clamped)
-> DestroyActor
```

StatName fixe : "HealthCurrent". Guard Min(HealthCurrent+effect, HealthMax) fonctionnel (contrairement au bug dans SetStatValue.HealthMax case).

---

*Snapshot produit par audit agent UnrealClaude -- session 04/06/2026*
