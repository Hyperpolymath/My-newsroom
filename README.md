# My-newsroom: Epistemic Programming for Neurosymbolic Journalism

[![RSR Compliance](https://img.shields.io/badge/RSR-Bronze%20%E2%86%92%20Silver-orange)](docs/RSR-COMPLIANCE.md)
[![TPCF Perimeter](https://img.shields.io/badge/TPCF-Perimeter%203%20(Community)-green)](https://gitlab.com/rhodium-project/tpcf)
[![License](https://img.shields.io/badge/License-MIT%20%2B%20Palimpsest%20v0.8-blue)](LICENSE.txt)

**Version:** 0.1.0-alpha
**Status:** Research Prototype
**Language Level:** Me ✅ | Solo 🚧 40% | Duet 📋 Spec | Ensemble 📋 Spec

---

## 🎯 What is My-newsroom?

**My-newsroom** is a research project exploring **epistemic programming languages** and **neurosymbolic AI** for journalism. It demonstrates how formal uncertainty quantification (Dempster-Shafer theory) and multi-agent systems can improve journalistic verification, fact-checking, and source credibility assessment.

### Core Innovation

The **My Language** family provides graduated trust semantics across four dialects:

1. **Me** - Epistemic types with belief states and probabilistic reasoning
2. **Solo** - Systems programming with affine types and arena allocation
3. **Duet** - Human-AI co-programming with formal verification
4. **Ensemble** - Multi-agent orchestration with belief fusion

Together, these enable type-safe reasoning about uncertainty, automated verification of journalistic claims, and politically autonomous software resistant to vendor lock-in.

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** (for prototyping)
- **Rust 1.75+** (for Solo dialect compiler)
- **Node.js 20+** (for Me dialect playground)
- **Ada 2022** (optional, for formal verification)

### Installation

```bash
# Clone repository
git clone https://gitlab.com/Hyperpolymath/My-newsroom.git
cd My-newsroom

# Install dependencies (Python prototype)
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Run examples
python examples/dempster_shafer_basic.py
```

### First Example: Belief Fusion

```my
# Me dialect: Epistemic types
belief source_a: Float where confidence(0.85);
belief source_b: Float where confidence(0.60);

# Fuse beliefs using Dempster-Shafer
result := fuse(source_a, source_b, rule=Dempster);
assert result.confidence >= 0.85;
```

```python
# Python prototype (current implementation)
from mynewsroom.dempster_shafer import BeliefMass, fuse_beliefs

# Define belief masses over frame Θ = {true, false}
m1 = BeliefMass({"true": 0.7, "false": 0.1, "Θ": 0.2})
m2 = BeliefMass({"true": 0.5, "false": 0.3, "Θ": 0.2})

# Combine using Dempster's rule
result = fuse_beliefs(m1, m2, method="dempster")
print(result)  # BeliefMass({"true": 0.877, "false": 0.081, "Θ": 0.041})
```

---

## 📚 Documentation

### Language Specifications

- **[My Language Master Index](docs/MY-LANGUAGE-INDEX.md)** - Complete overview of all dialects
- **[Me Dialect](docs/dialects/me.md)** - Epistemic types and belief states
- **[Solo Dialect](docs/dialects/solo.md)** - Systems programming (40% complete)
- **[Duet Dialect](docs/dialects/duet.md)** - Human-AI co-programming
- **[Ensemble Dialect](docs/dialects/ensemble.md)** - Multi-agent orchestration

### Project Documentation

- **[Newroom Roadmap](docs/NEWROOM-ROADMAP.md)** - 24-month demonstration project plan
- **[RSR Compliance](docs/RSR-COMPLIANCE.md)** - Repository standards checklist
- **[Academic Papers](docs/research/academic-papers.md)** - 5 paper outlines (ICSE, PLDI, CHI, etc.)
- **[Conference Materials](docs/research/conference-materials.md)** - 9 talk abstracts for 30+ venues
- **[Contributing Guide](CONTRIBUTING.md)** - How to participate (TPCF Perimeter 3)
- **[Security Policy](SECURITY.md)** - Vulnerability reporting and threat model

### Quick Reference

```bash
docs/
├── MY-LANGUAGE-INDEX.md       # Start here!
├── NEWROOM-ROADMAP.md         # Demonstration project
├── RSR-COMPLIANCE.md          # Standards checklist
├── dialects/
│   ├── me.md                  # Epistemic types
│   ├── solo.md                # Systems programming
│   ├── duet.md                # Human-AI co-programming
│   └── ensemble.md            # Multi-agent orchestration
├── research/
│   ├── academic-papers.md     # 5 paper outlines
│   └── conference-materials.md # 9 talk abstracts
└── guides/
    ├── migration-guide.md     # From Python/JS to My
    └── verification-guide.md  # Formal verification workflows
```

---

## 🏗️ Architecture

### Newroom Demonstration Project

The flagship demonstration is a **multi-agent newsroom** that verifies journalistic claims using distributed belief fusion:

```ensemble
comptime orchestrate NewsVerificationRing {
    agents: [
        ReporterAgent(domain: "politics"),
        ReporterAgent(domain: "science"),
        FactCheckerAgent(sources: [Snopes, FactCheck]),
        SourceEvaluatorAgent(credibility_db: "databases/sources.json"),
        EditorAgent(threshold: 0.85),
    ],
    topology: Ring,
    fusion: DempsterShafer,
    consensus: Threshold(0.85),
}
```

**Key Features:**
- 50-100 specialized agents (reporters, fact-checkers, editors)
- Dempster-Shafer belief fusion for evidence combination
- Formal uncertainty propagation (no false certainty)
- Explainable AI (trace belief updates through agent interactions)
- Offline-first (works air-gapped, no cloud dependencies)

### Technology Stack

| Layer | Technology | Status |
|-------|-----------|--------|
| Prototype | Python 3.11 + NumPy | ✅ Working |
| Me Dialect | TypeScript + HTML Playground | ✅ Complete |
| Solo Compiler | Rust + QBE backend | 🚧 40% |
| Duet Verifier | Ada 2022 + SPARK | 📋 Spec Only |
| Ensemble Runtime | Elixir + Haskell | 📋 Spec Only |
| Belief Fusion | Dempster-Shafer (Python) | ✅ Working |
| Agent Framework | Actor model (planned) | 📋 Design Phase |

---

## 🎓 Research Context

### Academic Foundations

This project builds on:

- **Dempster-Shafer Theory** (Shafer 1976) - Mathematical theory of evidence
- **Epistemic Programming** (Fagin et al. 1995) - Reasoning about knowledge
- **Type Systems** (Pierce 2002) - Affine types, dependent types
- **Multi-Agent Systems** (Wooldridge 2009) - Distributed AI coordination
- **Neurosymbolic AI** (Garcez et al. 2019) - Hybrid symbolic-neural systems

### Publications (Planned)

5 academic papers in preparation:

1. **"Rhodium Standard Repository Framework"** → ICSE 2026 (12 pages)
2. **"TPCF: Graduated Trust Model"** → CHI 2026 (10 pages)
3. **"CRDTs for Offline-First Systems"** → Middleware 2026 (12 pages)
4. **"iSOS: Multi-Language Verification"** → PLDI 2026 (12 pages)
5. **"Emotional Temperature Metrics"** → CHASE 2026 (8 pages)

See [`docs/research/academic-papers.md`](docs/research/academic-papers.md) for full outlines.

### Conference Talks (Planned)

9 talk abstracts targeting 30+ venues (FOSDEM, RustConf, Strange Loop, DEF CON, etc.):

- "Post-JavaScript Liberation" (45 min technical)
- "Distributed State Without Coordination" (60 min CRDTs)
- "10+ Dimensions of Security" (60 min security)
- "RSR: Politically Autonomous Software" (20 min research)

See [`docs/research/conference-materials.md`](docs/research/conference-materials.md) for details.

---

## 🛡️ Security & Privacy

### Threat Model

**Assumptions:**
- Adversary has network access (MITM attacks possible)
- Some agents may be compromised (Byzantine faults)
- Training data may contain poisoned examples

**Mitigations:**
- Offline-first design (works air-gapped)
- Cryptographic signing of belief updates
- Byzantine fault tolerance (33% malicious agents tolerated)
- Differential privacy for sensitive sources

### Vulnerability Reporting

**Coordinated Disclosure:** See [`.well-known/security.txt`](.well-known/security.txt)

- Email: security@[project-domain]
- PGP: [Key fingerprint]
- Timeline: 90 days before public disclosure

---

## 🤝 Contributing

**My-newsroom** follows the **Tri-Perimeter Contribution Framework (TPCF)**:

- **Perimeter 3: Community Sandbox** (current) - Fully open contributions
- **Perimeter 2: Verified Contributors** (future) - Review required
- **Perimeter 1: Core Maintainers** (future) - Direct commit access

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for:
- Code style guidelines
- Testing requirements (80%+ coverage)
- Documentation standards
- Review process

### Quick Contribution Workflow

```bash
# 1. Fork and clone
git clone https://gitlab.com/YourUsername/My-newsroom.git
cd My-newsroom

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Make changes and test
just test            # Run test suite
just validate        # Check RSR compliance

# 4. Commit and push
git commit -m "feat: add Dempster-Shafer normalization"
git push origin feature/your-feature-name

# 5. Open merge request on GitLab
```

---

## 📊 Project Status

### Completion Roadmap

| Milestone | Target | Status | Notes |
|-----------|--------|--------|-------|
| Me Dialect Complete | Q4 2024 | ✅ Done | HTML playground working |
| Solo MVP | Q1 2025 | 🚧 40% | Parser + QBE backend in progress |
| Duet Spec | Q2 2025 | 📋 Planning | Formal verification design |
| Ensemble Spec | Q3 2025 | 📋 Planning | Multi-agent architecture |
| Newroom Prototype | Q4 2025 | 📋 Planning | 5-agent proof of concept |
| Reuters-Scale Demo | Q4 2026 | 📋 Planning | 50-100 agents, production-ready |

### Current Focus (2025-11-22)

- ✅ Complete RSR compliance (Bronze → Silver level)
- 🚧 Finish Solo dialect parser (4-6 weeks)
- 📋 Write Duet + Ensemble formal specs
- 📋 Prototype Dempster-Shafer in Python
- 📋 Design Newroom agent architecture

---

## 📜 License

**Dual Licensed:**

- **MIT License** - Permissive open source (see `LICENSE.txt`)
- **Palimpsest License v0.8** - Remediation-first for harm prevention

**Why Dual License?**

- MIT allows maximum adoption and reuse
- Palimpsest adds ethical safeguards (no surveillance, no weaponization)
- Users choose which license to follow

**Documentation:** CC BY-SA 4.0
**Research Papers:** CC BY 4.0 (preprints)

---

## 🙏 Acknowledgments

See [`.well-known/humans.txt`](.well-known/humans.txt) for full credits.

**Theoretical Foundations:**
- Glenn Shafer (Dempster-Shafer theory)
- Benjamin Pierce (type systems)
- Michael Wooldridge (multi-agent systems)

**Tools & Infrastructure:**
- Anthropic (Claude AI assistance)
- GitLab (hosting and CI/CD)
- Rust Community (Solo dialect compiler)

---

## 📞 Contact

- **Project Lead:** Jonathan D.A. Jewell (hyperpolymath)
- **GitLab:** https://gitlab.com/Hyperpolymath/My-newsroom
- **Issues:** https://gitlab.com/Hyperpolymath/My-newsroom/-/issues
- **Discussions:** https://gitlab.com/Hyperpolymath/My-newsroom/-/discussions

---

## 🔗 Related Projects

- [Rhodium RSR](https://gitlab.com/rhodium-project/rsr) - Repository standards framework
- [TPCF](https://gitlab.com/rhodium-project/tpcf) - Tri-Perimeter access control
- [Dempster-Shafer Library](https://github.com/reineking/pyds) - Python implementation
- [SPARK Ada](https://www.adacore.com/about-spark) - Formal verification tools

---

**Built with epistemic humility and type safety.** 🔒📊🤖
