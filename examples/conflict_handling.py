#!/usr/bin/env python3
"""
Conflict Handling Example

Demonstrates different fusion rules when sources strongly disagree.
Shows when to use Dempster, Yager, or Dubois-Prade rules.
"""

import warnings
from mynewsroom import BeliefMass, fuse_beliefs, FusionRule, calculate_conflict


def compare_fusion_rules(m1, m2, scenario_name):
    """Compare all fusion rules for a given scenario."""
    print(f"\n{'=' * 70}")
    print(f"  {scenario_name}")
    print(f"{'=' * 70}\n")

    # Show sources
    print("Source A:", m1)
    print("Source B:", m2)
    print()

    # Calculate conflict
    conflict = calculate_conflict(m1, m2)
    print(f"Conflict (K): {conflict:.4f} ({conflict * 100:.1f}%)")
    print()

    # Try each fusion rule
    rules = [
        (FusionRule.DEMPSTER, "Dempster (normalizes conflict)"),
        (FusionRule.YAGER, "Yager (conflict → ignorance)"),
        (FusionRule.DUBOIS_PRADE, "Dubois-Prade (conflict → union)"),
    ]

    for rule, description in rules:
        print(f"{description}:")
        try:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = fuse_beliefs(m1, m2, rule=rule)

                if w:
                    print(f"  ⚠️  Warning: {w[0].message}")

                print(f"  Result: {result}")
        except ValueError as e:
            print(f"  ❌ Error: {e}")
        print()


def main():
    print("=" * 70)
    print("  Conflict Handling: Comparison of Fusion Rules")
    print("=" * 70)

    # Scenario 1: Low conflict (sources mostly agree)
    theta = frozenset({"true", "false"})
    m1 = BeliefMass({
        frozenset({"true"}): 0.8,
        theta: 0.2
    })
    m2 = BeliefMass({
        frozenset({"true"}): 0.7,
        theta: 0.3
    })
    compare_fusion_rules(m1, m2, "Scenario 1: Low Conflict (Sources Agree)")

    # Scenario 2: Moderate conflict
    m3 = BeliefMass({
        frozenset({"true"}): 0.7,
        frozenset({"false"}): 0.3
    })
    m4 = BeliefMass({
        frozenset({"true"}): 0.4,
        frozenset({"false"}): 0.6
    })
    compare_fusion_rules(m3, m4, "Scenario 2: Moderate Conflict (Partial Disagreement)")

    # Scenario 3: High conflict (sources strongly disagree)
    m5 = BeliefMass({
        frozenset({"true"}): 0.95,
        frozenset({"false"}): 0.05
    })
    m6 = BeliefMass({
        frozenset({"true"}): 0.05,
        frozenset({"false"}): 0.95
    })
    compare_fusion_rules(m5, m6, "Scenario 3: High Conflict (Strong Disagreement)")

    # Scenario 4: Total conflict (complete contradiction)
    m7 = BeliefMass({frozenset({"true"}): 1.0})
    m8 = BeliefMass({frozenset({"false"}): 1.0})
    compare_fusion_rules(m7, m8, "Scenario 4: Total Conflict (Complete Contradiction)")

    # Summary recommendations
    print(f"\n{'=' * 70}")
    print("  Recommendations")
    print(f"{'=' * 70}\n")
    print("When to use each fusion rule:")
    print()
    print("📊 Dempster's Rule:")
    print("   ✅ Use when: Sources are generally reliable, conflict < 0.9")
    print("   ❌ Avoid when: Total or near-total conflict (K ≈ 1.0)")
    print("   💡 Behavior: Normalizes by (1-K), strengthens agreement")
    print()
    print("🛡️  Yager's Rule:")
    print("   ✅ Use when: High conflict, want to be conservative")
    print("   ✅ Use when: Sources may be unreliable")
    print("   💡 Behavior: Assigns conflict to ignorance (theta)")
    print()
    print("🔀 Dubois-Prade Rule:")
    print("   ✅ Use when: Want to preserve all information")
    print("   ✅ Use when: Conflict represents genuine ambiguity")
    print("   💡 Behavior: Assigns conflict to union of conflicting sets")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
