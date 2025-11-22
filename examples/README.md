# My-newsroom Examples

This directory contains runnable examples demonstrating the My Language family
and Dempster-Shafer belief fusion.

## Python Examples (Dempster-Shafer)

### Basic Examples

**dempster_shafer_basic.py** - Introduction to belief fusion
```bash
python examples/dempster_shafer_basic.py
```
- Creating belief masses
- Fusing with Dempster and Yager rules
- Calculating uncertainty intervals

**newsroom_scenario.py** - Realistic fact-checking workflow
```bash
python examples/newsroom_scenario.py
```
- Multi-source evidence gathering (IPCC, NASA, universities, social media)
- Progressive belief fusion
- Editorial decision-making with confidence thresholds

**conflict_handling.py** - Comparison of fusion rules
```bash
python examples/conflict_handling.py
```
- Low, moderate, high, and total conflict scenarios
- Side-by-side comparison of Dempster, Yager, and Dubois-Prade
- Recommendations for when to use each rule

### Advanced Examples

Coming soon:
- Multi-agent newsroom simulation
- Byzantine fault tolerance demonstration
- Epistemic ledger with audit trails
- Performance benchmarks (1000+ agents)

## Me Dialect Examples

Located in `examples/me/` - Interactive HTML playground

**Features:**
- Belief state visualization
- Bayesian inference
- Trust propagation graphs

**Usage:**
```bash
# Serve locally
python -m http.server 8000
# Open http://localhost:8000/examples/me/playground.html
```

## Solo Dialect Examples

Located in `examples/solo/` (coming soon)

**Planned:**
- hello_world.solo - Basic syntax
- arena_allocation.solo - Memory management
- parser.solo - Recursive descent parser
- belief_fusion.solo - High-performance Dempster-Shafer

**Compile:**
```bash
solo build examples/solo/hello_world.solo
./hello_world
```

## Duet Dialect Examples

Located in `examples/duet/` (coming soon)

**Planned:**
- verified_sort.duet - Provably correct quicksort
- dempster_verified.duet - Formally verified belief fusion
- parser_synth.duet - AI-synthesized parser

**Compile & Verify:**
```bash
duet build --verify-level=2 examples/duet/verified_sort.duet
```

## Ensemble Dialect Examples

Located in `examples/ensemble/` (coming soon)

**Planned:**
- simple_newsroom.ens - 5-agent proof of concept
- reuters_scale.ens - 100-agent simulation
- bft_consensus.ens - Byzantine fault tolerance

**Run:**
```bash
ensemble run examples/ensemble/simple_newsroom.ens
```

## Expected Output

### dempster_shafer_basic.py
```
======================================================================
Dempster-Shafer Belief Fusion Demo
======================================================================

Source A (Reuters):
  Belief in 'true': 0.85
  Uncertainty: 0.15

Source B (Twitter):
  Belief in 'true': 0.60
  Uncertainty: 0.40

Conflict between sources: 0.0000

Fusing with Dempster's rule:
  Combined belief in 'true': 0.9194
  Combined uncertainty: 0.0806

Fusing with Yager's rule (more conservative):
  Combined belief in 'true': 0.5100
  Combined uncertainty: 0.4900

Uncertainty Intervals:
  [Belief, Plausibility] = [0.9194, 1.0000]
  Width of interval: 0.0806

======================================================================
✅ Fusion complete! Both sources agree, increasing confidence.
======================================================================
```

### newsroom_scenario.py
```
======================================================================
  Newsroom Fact-Checking: Climate Change Claim
======================================================================

Gathering evidence from multiple sources...

📊 Source 1: IPCC Scientific Report
   Credibility: ★★★★★
   Belief: 95% true

...

======================================================================
  Editorial Decision
======================================================================

Final Assessment:
   Belief in claim truth: 98.56%
   Remaining uncertainty: 1.44%

✅ PUBLISH: Confidence (98.6%) exceeds threshold (85%)

Recommended headline:
   "Scientific consensus confirms: Global temperatures
    have risen 1.1°C since pre-industrial era"

======================================================================
```

## Contributing Examples

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on adding examples.

**Requirements:**
- Clear, runnable code
- Docstrings explaining purpose
- Expected output documented
- Real-world use cases preferred
