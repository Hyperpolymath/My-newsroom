"""
Dempster-Shafer Theory of Evidence implementation in Julia.

References:
- Shafer, G. (1976). A Mathematical Theory of Evidence.
- Smets, P. (1990). The Combination of Evidence in the TBM.
"""

# Fusion rules
@enum FusionRule Dempster Yager DuboisPrade Average

"""
    BeliefMass{T}

Belief mass function over a frame of discernment Θ.

# Fields
- `masses::Dict{Set{T}, Float64}`: Focal sets → probability masses
- `frame::Set{T}`: Frame of discernment (universe)
- `ε::Float64`: Tolerance for floating-point comparisons

# Example
```julia
θ = Set(["true", "false"])
m = BeliefMass(Dict(Set(["true"]) => 0.7, θ => 0.3))
```
"""
struct BeliefMass{T}
    masses::Dict{Set{T}, Float64}
    frame::Set{T}
    ε::Float64

    function BeliefMass{T}(masses::Dict{Set{T}, Float64},
                           frame::Union{Set{T}, Nothing}=nothing;
                           ε::Float64=1e-6) where T
        isempty(masses) && error("Belief mass cannot be empty")

        # Infer frame from masses if not provided
        actual_frame = if frame === nothing
            reduce(∪, keys(masses))
        else
            frame
        end

        # Validate masses
        for (focal_set, mass) in masses
            !(0.0 ≤ mass ≤ 1.0 + ε) && error("Mass $mass out of range [0,1]")
            !issubset(focal_set, actual_frame) && error("Focal set not in frame")
        end

        # Check sum
        total = sum(values(masses))
        !isapprox(total, 1.0, atol=ε) && error("Masses sum to $total, must sum to 1.0")

        # Normalize if close to 1.0
        normalized_masses = if abs(total - 1.0) < ε && total != 1.0
            Dict(k => v/total for (k,v) in masses)
        else
            masses
        end

        new{T}(normalized_masses, actual_frame, ε)
    end
end

# Constructor convenience
BeliefMass(masses::Dict{Set{T}, Float64}, args...; kwargs...) where T =
    BeliefMass{T}(masses, args...; kwargs...)

"""
    is_valid(m::BeliefMass)

Check if belief mass function is valid (masses sum to 1.0).
"""
is_valid(m::BeliefMass) = isapprox(sum(values(m.masses)), 1.0, atol=m.ε)

"""
    belief(m::BeliefMass, proposition::Set)

Calculate belief (lower probability) in a proposition.
Bel(A) = Σ m(B) for all B ⊆ A
"""
function belief(m::BeliefMass{T}, proposition::Set{T}) where T
    sum(mass for (focal_set, mass) in m.masses if issubset(focal_set, proposition))
end

"""
    plausibility(m::BeliefMass, proposition::Set)

Calculate plausibility (upper probability) in a proposition.
Pl(A) = Σ m(B) for all B ∩ A ≠ ∅
"""
function plausibility(m::BeliefMass{T}, proposition::Set{T}) where T
    sum(mass for (focal_set, mass) in m.masses if !isdisjoint(focal_set, proposition))
end

"""
    calculate_conflict(m1::BeliefMass, m2::BeliefMass)

Calculate conflict between two belief masses.
K = Σ m₁(A) · m₂(B) for all A ∩ B = ∅
"""
function calculate_conflict(m1::BeliefMass{T}, m2::BeliefMass{T}) where T
    m1.frame != m2.frame && error("Incompatible frames")

    conflict = 0.0
    for (set_a, mass_a) in m1.masses
        for (set_b, mass_b) in m2.masses
            if isdisjoint(set_a, set_b)
                conflict += mass_a * mass_b
            end
        end
    end
    conflict
end

"""
    fuse_dempster(m1::BeliefMass, m2::BeliefMass)

Dempster's rule: normalize by (1 - K).
"""
function fuse_dempster(m1::BeliefMass{T}, m2::BeliefMass{T}) where T
    conflict = calculate_conflict(m1, m2)

    conflict >= 1.0 - m1.ε && error("Total conflict (K=$conflict). Cannot use Dempster's rule.")

    if conflict >= 0.9
        @warn "High conflict (K=$conflict). Result may be unreliable."
    end

    # Conjunctive combination
    combined = Dict{Set{T}, Float64}()
    for (set_a, mass_a) in m1.masses
        for (set_b, mass_b) in m2.masses
            intersection = set_a ∩ set_b
            if !isempty(intersection)
                combined[intersection] = get(combined, intersection, 0.0) + mass_a * mass_b
            end
        end
    end

    # Normalize
    normalization = 1.0 - conflict
    normalized = Dict(k => v/normalization for (k,v) in combined)

    BeliefMass(normalized, m1.frame)
end

"""
    fuse_yager(m1::BeliefMass, m2::BeliefMass)

Yager's rule: assign conflict to ignorance (frame).
"""
function fuse_yager(m1::BeliefMass{T}, m2::BeliefMass{T}) where T
    conflict = calculate_conflict(m1, m2)

    combined = Dict{Set{T}, Float64}()
    for (set_a, mass_a) in m1.masses
        for (set_b, mass_b) in m2.masses
            intersection = set_a ∩ set_b
            if !isempty(intersection)
                combined[intersection] = get(combined, intersection, 0.0) + mass_a * mass_b
            end
        end
    end

    # Add conflict to frame
    if conflict > m1.ε
        combined[m1.frame] = get(combined, m1.frame, 0.0) + conflict
    end

    BeliefMass(combined, m1.frame)
end

"""
    fuse_dubois_prade(m1::BeliefMass, m2::BeliefMass)

Dubois-Prade rule: redistribute conflict to union.
"""
function fuse_dubois_prade(m1::BeliefMass{T}, m2::BeliefMass{T}) where T
    combined = Dict{Set{T}, Float64}()

    for (set_a, mass_a) in m1.masses
        for (set_b, mass_b) in m2.masses
            product = mass_a * mass_b
            intersection = set_a ∩ set_b

            if !isempty(intersection)
                combined[intersection] = get(combined, intersection, 0.0) + product
            else
                # Conflict: assign to union
                union_set = set_a ∪ set_b
                combined[union_set] = get(combined, union_set, 0.0) + product
            end
        end
    end

    BeliefMass(combined, m1.frame)
end

"""
    fuse_average(m1::BeliefMass, m2::BeliefMass)

Simple averaging (not proper Dempster-Shafer, but useful baseline).
"""
function fuse_average(m1::BeliefMass{T}, m2::BeliefMass{T}) where T
    all_sets = union(keys(m1.masses), keys(m2.masses))
    averaged = Dict{Set{T}, Float64}()

    for focal_set in all_sets
        mass_a = get(m1.masses, focal_set, 0.0)
        mass_b = get(m2.masses, focal_set, 0.0)
        averaged[focal_set] = (mass_a + mass_b) / 2.0
    end

    BeliefMass(averaged, m1.frame)
end

"""
    fuse_beliefs(m1::BeliefMass, m2::BeliefMass, rule::FusionRule=Dempster)

Fuse two belief masses using specified rule.

# Arguments
- `m1`, `m2`: Belief masses to fuse
- `rule`: Fusion rule (Dempster, Yager, DuboisPrade, Average)

# Returns
Combined belief mass
"""
function fuse_beliefs(m1::BeliefMass{T}, m2::BeliefMass{T},
                      rule::FusionRule=Dempster) where T
    m1.frame != m2.frame && error("Incompatible frames")

    if rule == Dempster
        fuse_dempster(m1, m2)
    elseif rule == Yager
        fuse_yager(m1, m2)
    elseif rule == DuboisPrade
        fuse_dubois_prade(m1, m2)
    else  # Average
        fuse_average(m1, m2)
    end
end

"""
    fuse_multiple(masses::Vector{BeliefMass}, rule::FusionRule=Dempster)

Fuse multiple belief masses iteratively.
"""
function fuse_multiple(masses::Vector{BeliefMass{T}},
                       rule::FusionRule=Dempster) where T
    isempty(masses) && error("Cannot fuse empty list")
    length(masses) == 1 && return masses[1]

    reduce((m1, m2) -> fuse_beliefs(m1, m2, rule), masses)
end
