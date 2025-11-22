"""
Property-based tests for Dempster-Shafer using Hypothesis.

Tests mathematical properties that should hold for all valid inputs:
- Commutativity
- Associativity
- Idempotence
- Belief ≤ Plausibility
- Conservation of mass
"""

import pytest
from hypothesis import given, strategies as st, assume, settings
from mynewsroom import BeliefMass, fuse_beliefs, FusionRule, calculate_conflict


# Strategy for generating valid belief masses
@st.composite
def belief_mass_strategy(draw, min_sets=1, max_sets=3):
    """Generate valid belief masses for property testing."""
    # Create frame with 2-4 elements
    n_elements = draw(st.integers(min_value=2, max_value=4))
    elements = [f"elem{i}" for i in range(n_elements)]
    frame = frozenset(elements)

    # Generate focal sets (non-empty subsets)
    n_focal = draw(st.integers(min_value=min_sets, max_value=max_sets))

    # Generate probability masses that sum to 1.0
    masses_raw = draw(st.lists(
        st.floats(min_value=0.01, max_value=0.98),
        min_size=n_focal,
        max_size=n_focal
    ))

    # Normalize to sum to 1.0
    total = sum(masses_raw)
    masses = [m / total for m in masses_raw]

    # Create random focal sets
    focal_sets = []
    for _ in range(n_focal):
        # Random subset size (1 to n_elements)
        subset_size = draw(st.integers(min_value=1, max_value=n_elements))
        subset = frozenset(draw(st.lists(
            st.sampled_from(elements),
            min_size=subset_size,
            max_size=subset_size,
            unique=True
        )))
        focal_sets.append(subset)

    # Combine into belief mass
    belief_dict = {}
    for focal_set, mass in zip(focal_sets, masses):
        if focal_set in belief_dict:
            belief_dict[focal_set] += mass
        else:
            belief_dict[focal_set] = mass

    # Renormalize (in case of duplicates)
    total = sum(belief_dict.values())
    belief_dict = {k: v/total for k, v in belief_dict.items()}

    return BeliefMass(belief_dict, frame=frame)


class TestCommutativeProperty:
    """Test that fusion is commutative: fuse(A, B) == fuse(B, A)"""

    @given(
        m1=belief_mass_strategy(),
        m2=belief_mass_strategy()
    )
    @settings(max_examples=100, deadline=1000)
    def test_dempster_commutative(self, m1, m2):
        """Dempster's rule should be commutative."""
        assume(m1.frame == m2.frame)
        assume(calculate_conflict(m1, m2) < 0.99)  # Avoid total conflict

        result_12 = fuse_beliefs(m1, m2, rule=FusionRule.DEMPSTER)
        result_21 = fuse_beliefs(m2, m1, rule=FusionRule.DEMPSTER)

        # Check that results are equal (within floating-point tolerance)
        for focal_set in set(result_12.masses.keys()) | set(result_21.masses.keys()):
            mass_12 = result_12.masses.get(focal_set, 0.0)
            mass_21 = result_21.masses.get(focal_set, 0.0)
            assert abs(mass_12 - mass_21) < 1e-6, f"Commutativity violated for {focal_set}"

    @given(
        m1=belief_mass_strategy(),
        m2=belief_mass_strategy()
    )
    @settings(max_examples=50)
    def test_yager_commutative(self, m1, m2):
        """Yager's rule should be commutative."""
        assume(m1.frame == m2.frame)

        result_12 = fuse_beliefs(m1, m2, rule=FusionRule.YAGER)
        result_21 = fuse_beliefs(m2, m1, rule=FusionRule.YAGER)

        for focal_set in set(result_12.masses.keys()) | set(result_21.masses.keys()):
            mass_12 = result_12.masses.get(focal_set, 0.0)
            mass_21 = result_21.masses.get(focal_set, 0.0)
            assert abs(mass_12 - mass_21) < 1e-6


class TestAssociativeProperty:
    """Test that fusion is associative: (A⊕B)⊕C == A⊕(B⊕C)"""

    @given(
        m1=belief_mass_strategy(),
        m2=belief_mass_strategy(),
        m3=belief_mass_strategy()
    )
    @settings(max_examples=50, deadline=2000)
    def test_dempster_associative(self, m1, m2, m3):
        """Dempster's rule should be associative."""
        assume(m1.frame == m2.frame == m3.frame)
        assume(calculate_conflict(m1, m2) < 0.95)
        assume(calculate_conflict(m2, m3) < 0.95)

        # (m1 ⊕ m2) ⊕ m3
        left = fuse_beliefs(
            fuse_beliefs(m1, m2, rule=FusionRule.DEMPSTER),
            m3,
            rule=FusionRule.DEMPSTER
        )

        # m1 ⊕ (m2 ⊕ m3)
        right = fuse_beliefs(
            m1,
            fuse_beliefs(m2, m3, rule=FusionRule.DEMPSTER),
            rule=FusionRule.DEMPSTER
        )

        for focal_set in set(left.masses.keys()) | set(right.masses.keys()):
            mass_left = left.masses.get(focal_set, 0.0)
            mass_right = right.masses.get(focal_set, 0.0)
            assert abs(mass_left - mass_right) < 1e-5, f"Associativity violated for {focal_set}"


class TestBeliefPlausibilityInequality:
    """Test that Belief ≤ Plausibility for all propositions"""

    @given(m=belief_mass_strategy())
    @settings(max_examples=100)
    def test_belief_le_plausibility(self, m):
        """For any proposition A, Bel(A) ≤ Pl(A)"""
        # Test all possible subsets
        for focal_set in m.masses.keys():
            bel = m.belief(focal_set)
            pl = m.plausibility(focal_set)
            assert bel <= pl + 1e-9, f"Belief ({bel}) > Plausibility ({pl}) for {focal_set}"


class TestMassConservation:
    """Test that fusion preserves total mass (sums to 1.0)"""

    @given(
        m1=belief_mass_strategy(),
        m2=belief_mass_strategy()
    )
    @settings(max_examples=100)
    def test_dempster_conserves_mass(self, m1, m2):
        """Dempster fusion should preserve total mass."""
        assume(m1.frame == m2.frame)
        assume(calculate_conflict(m1, m2) < 0.99)

        result = fuse_beliefs(m1, m2, rule=FusionRule.DEMPSTER)
        assert result.is_valid()
        total = sum(result.masses.values())
        assert abs(total - 1.0) < 1e-6, f"Mass not conserved: {total}"

    @given(
        m1=belief_mass_strategy(),
        m2=belief_mass_strategy()
    )
    @settings(max_examples=50)
    def test_yager_conserves_mass(self, m1, m2):
        """Yager fusion should preserve total mass."""
        assume(m1.frame == m2.frame)

        result = fuse_beliefs(m1, m2, rule=FusionRule.YAGER)
        assert result.is_valid()
        total = sum(result.masses.values())
        assert abs(total - 1.0) < 1e-6


class TestIdempotence:
    """Test fusion of a belief mass with itself"""

    @given(m=belief_mass_strategy())
    @settings(max_examples=50)
    def test_dempster_idempotence(self, m):
        """Fusing a belief with itself using Dempster should strengthen beliefs."""
        assume(calculate_conflict(m, m) < 0.95)

        result = fuse_beliefs(m, m, rule=FusionRule.DEMPSTER)

        # Check that focal sets with high mass get higher mass after fusion
        for focal_set, mass in m.masses.items():
            if mass > 0.5:  # If already dominant
                result_mass = result.masses.get(focal_set, 0.0)
                assert result_mass >= mass, "Dominant beliefs should strengthen"


class TestVacuousBelief:
    """Test fusion with vacuous belief (total ignorance)"""

    @given(m=belief_mass_strategy())
    @settings(max_examples=50)
    def test_fusion_with_ignorance(self, m):
        """Fusing with vacuous belief should leave other mass unchanged."""
        # Create vacuous belief (all mass on frame)
        m_vacuous = BeliefMass({m.frame: 1.0}, frame=m.frame)

        result = fuse_beliefs(m, m_vacuous, rule=FusionRule.DEMPSTER)

        # Result should equal m (within tolerance)
        for focal_set, mass in m.masses.items():
            result_mass = result.masses.get(focal_set, 0.0)
            assert abs(mass - result_mass) < 1e-6, "Vacuous fusion should be identity"


class TestConflictRange:
    """Test that conflict is always in [0, 1]"""

    @given(
        m1=belief_mass_strategy(),
        m2=belief_mass_strategy()
    )
    @settings(max_examples=100)
    def test_conflict_bounds(self, m1, m2):
        """Conflict should always be in range [0, 1]"""
        assume(m1.frame == m2.frame)

        conflict = calculate_conflict(m1, m2)
        assert 0.0 <= conflict <= 1.0, f"Conflict {conflict} out of bounds"


class TestMonotonicity:
    """Test that adding supporting evidence increases belief"""

    @given(
        m1=belief_mass_strategy(min_sets=1, max_sets=2),
    )
    @settings(max_examples=30)
    def test_evidence_monotonicity(self, m1):
        """Adding evidence for a proposition should not decrease its belief."""
        # Find the focal set with highest mass
        max_focal = max(m1.masses.items(), key=lambda x: x[1])[0]

        # Create supporting evidence (high mass on same focal set)
        m2 = BeliefMass({max_focal: 0.8, m1.frame: 0.2}, frame=m1.frame)

        result = fuse_beliefs(m1, m2, rule=FusionRule.DEMPSTER)

        # Belief in max_focal should not decrease
        initial_belief = m1.belief(max_focal)
        final_belief = result.belief(max_focal)

        assert final_belief >= initial_belief - 1e-6, \
            f"Supporting evidence decreased belief: {initial_belief} -> {final_belief}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-m", "property"])
