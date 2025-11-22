#!/usr/bin/env python3
"""
Realistic Newsroom Scenario: Multi-Source Fact-Checking

Demonstrates how a newsroom would use Dempster-Shafer fusion to
verify a controversial claim using multiple sources with different
credibility levels.
"""

from mynewsroom import BeliefMass, fuse_multiple, FusionRule, calculate_conflict


def print_section(title):
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


def main():
    print_section("Newsroom Fact-Checking: Climate Change Claim")

    # Claim: "Global temperatures have risen 1.1°C since pre-industrial times"
    theta = frozenset({"true", "false"})

    print("Gathering evidence from multiple sources...\n")

    # Source 1: IPCC Report (highest credibility)
    print("📊 Source 1: IPCC Scientific Report")
    ipcc = BeliefMass({
        frozenset({"true"}): 0.95,  # Very high confidence
        theta: 0.05  # Minimal uncertainty
    })
    print(f"   Credibility: ★★★★★")
    print(f"   Belief: {ipcc[frozenset({'true'})] * 100:.0f}% true")
    print()

    # Source 2: NASA temperature data
    print("🛰️  Source 2: NASA Temperature Records")
    nasa = BeliefMass({
        frozenset({"true"}): 0.90,
        theta: 0.10
    })
    print(f"   Credibility: ★★★★★")
    print(f"   Belief: {nasa[frozenset({'true'})] * 100:.0f}% true")
    print()

    # Source 3: Independent university study
    print("🎓 Source 3: University Climate Research")
    university = BeliefMass({
        frozenset({"true"}): 0.85,
        theta: 0.15
    })
    print(f"   Credibility: ★★★★☆")
    print(f"   Belief: {university[frozenset({'true'})] * 100:.0f}% true")
    print()

    # Source 4: Think tank (lower credibility, some skepticism)
    print("🏛️  Source 4: Policy Think Tank")
    think_tank = BeliefMass({
        frozenset({"true"}): 0.60,
        frozenset({"false"}): 0.10,  # Some doubt
        theta: 0.30
    })
    print(f"   Credibility: ★★★☆☆")
    print(f"   Belief: {think_tank[frozenset({'true'})] * 100:.0f}% true, "
          f"{think_tank[frozenset({'false'})] * 100:.0f}% false")
    print()

    # Source 5: Social media aggregation (lowest credibility)
    print("📱 Source 5: Social Media Sentiment Analysis")
    social = BeliefMass({
        frozenset({"true"}): 0.55,
        frozenset({"false"}): 0.20,  # Significant dissent
        theta: 0.25
    })
    print(f"   Credibility: ★★☆☆☆")
    print(f"   Belief: {social[frozenset({'true'})] * 100:.0f}% true, "
          f"{social[frozenset({'false'})] * 100:.0f}% false")
    print()

    # Fuse all sources
    print_section("Belief Fusion Analysis")

    # Progressive fusion to show how evidence accumulates
    sources = [ipcc, nasa, university, think_tank, social]
    source_names = ["IPCC", "NASA", "University", "Think Tank", "Social Media"]

    cumulative = sources[0]
    print(f"Starting with {source_names[0]}: {cumulative[frozenset({'true'})] * 100:.1f}% confidence\n")

    for i, (source, name) in enumerate(zip(sources[1:], source_names[1:]), 1):
        conflict = calculate_conflict(cumulative, source)
        cumulative = fuse_beliefs(cumulative, source, rule=FusionRule.DEMPSTER)
        print(f"After adding {name}:")
        print(f"   Conflict: {conflict * 100:.1f}%")
        print(f"   Combined belief in 'true': {cumulative[frozenset({'true'})] * 100:.2f}%")
        print(f"   Uncertainty: {cumulative[theta] * 100:.2f}%")
        print()

    # Final assessment
    print_section("Editorial Decision")

    final_belief = cumulative[frozenset({"true"})]
    final_uncertainty = cumulative[theta]

    print(f"Final Assessment:")
    print(f"   Belief in claim truth: {final_belief * 100:.2f}%")
    print(f"   Remaining uncertainty: {final_uncertainty * 100:.2f}%")
    print()

    # Decision threshold: 85% confidence
    threshold = 0.85
    if final_belief >= threshold:
        print(f"✅ PUBLISH: Confidence ({final_belief * 100:.1f}%) exceeds threshold ({threshold * 100:.0f}%)")
        print(f"\nRecommended headline:")
        print(f'   "Scientific consensus confirms: Global temperatures')
        print(f'    have risen 1.1°C since pre-industrial era"')
    else:
        print(f"⚠️  HOLD: Confidence ({final_belief * 100:.1f}%) below threshold ({threshold * 100:.0f}%)")
        print(f"   Recommendation: Gather more evidence from high-credibility sources")

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
