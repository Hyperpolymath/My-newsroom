"""
    MyNewsroom

Epistemic programming for neurosymbolic journalism using Dempster-Shafer theory.

# Exports
- `BeliefMass`: Core type for belief mass functions
- `fuse_beliefs`: Combine belief masses using various rules
- `calculate_conflict`: Measure conflict between beliefs
- `FusionRule`: Enum of fusion rules (Dempster, Yager, DuboisPrade, Average)

# Example
```julia
using MyNewsroom

# Create belief masses
θ = Set(["true", "false"])
m1 = BeliefMass(Dict(Set(["true"]) => 0.7, θ => 0.3))
m2 = BeliefMass(Dict(Set(["true"]) => 0.8, θ => 0.2))

# Fuse with Dempster's rule
result = fuse_beliefs(m1, m2, Dempster)
```
"""
module MyNewsroom

export BeliefMass, FusionRule, Dempster, Yager, DuboisPrade, Average
export fuse_beliefs, calculate_conflict, belief, plausibility

include("dempster_shafer.jl")

end # module
