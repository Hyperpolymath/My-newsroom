#!/usr/bin/env python3
"""
Basic Dempster-Shafer Belief Fusion Example

Demonstrates how to create and fuse belief masses representing
uncertainty about a claim's truth.
"""

from mynewsroom import BeliefMass, fuse_beliefs, FusionRule, calculate_conflict


def main():
    print("=" * 70)
    print("Dempster-Shafer Belief Fusion Demo")
    print("=" * 70)
    print()

    # Define frame of discernment
    theta = frozenset({"true", "false"})

    # Source A: Reuters (high credibility)
    # 85% believe claim is true, 15% uncertain
    print("Source A (Reuters):")
    source_a = BeliefMass({
        frozenset({"true"}): 0.85,
        theta: 0.15
    })
    print(f"  Belief in 'true': {source_a[frozenset({'true'})]:.2f}")
    print(f"  Uncertainty: {source_a[theta]:.2f}")
    print()

    # Source B: Twitter user (lower credibility)
    # 60% believe claim is true, 40% uncertain
    print("Source B (Twitter):")
    source_b = BeliefMass({
        frozenset({"true"}): 0.60,
        theta: 0.40
    })
    print(f"  Belief in 'true': {source_b[frozenset({'true'})]:.2f}")
    print(f"  Uncertainty: {source_b[theta]:.2f}")
    print()

    # Calculate conflict
    conflict = calculate_conflict(source_a, source_b)
    print(f"Conflict between sources: {conflict:.4f}")
    print()

    # Fuse using Dempster's rule
    print("Fusing with Dempster's rule:")
    result_dempster = fuse_beliefs(source_a, source_b, rule=FusionRule.DEMPSTER)
    print(f"  Combined belief in 'true': {result_dempster[frozenset({'true'})]:.4f}")
    print(f"  Combined uncertainty: {result_dempster[theta]:.4f}")
    print()

    # Compare with Yager's rule (more conservative)
    print("Fusing with Yager's rule (more conservative):")
    result_yager = fuse_beliefs(source_a, source_b, rule=FusionRule.YAGER)
    print(f"  Combined belief in 'true': {result_yager[frozenset({'true'})]:.4f}")
    print(f"  Combined uncertainty: {result_yager[theta]:.4f}")
    print()

    # Show uncertainty intervals
    print("Uncertainty Intervals:")
    bel, pl = result_dempster.uncertainty_interval(frozenset({"true"}))
    print(f"  [Belief, Plausibility] = [{bel:.4f}, {pl:.4f}]")
    print(f"  Width of interval: {pl - bel:.4f}")
    print()

    print("=" * 70)
    print("✅ Fusion complete! Both sources agree, increasing confidence.")
    print("=" * 70)


if __name__ == "__main__":
    main()
