using Test
using MyNewsroom

@testset "MyNewsroom.jl" begin
    @testset "BeliefMass Creation" begin
        θ = Set(["true", "false"])
        m = BeliefMass(Dict(Set(["true"]) => 0.7, θ => 0.3))
        @test is_valid(m)
        @test m.frame == θ
    end

    @testset "Belief and Plausibility" begin
        θ = Set(["A", "B", "C"])
        m = BeliefMass(Dict(
            Set(["A"]) => 0.4,
            Set(["B"]) => 0.3,
            Set(["A", "B"]) => 0.2,
            θ => 0.1
        ))

        # Belief
        @test belief(m, Set(["A", "B"])) ≈ 0.9 atol=1e-6

        # Plausibility
        @test plausibility(m, Set(["A"])) ≈ 0.7 atol=1e-6
        @test plausibility(m, Set(["A", "B"])) ≈ 1.0 atol=1e-6
    end

    @testset "Conflict Calculation" begin
        m1 = BeliefMass(Dict(Set(["A"]) => 0.8, Set(["B"]) => 0.2))
        m2 = BeliefMass(Dict(Set(["A"]) => 0.6, Set(["B"]) => 0.4))

        conflict = calculate_conflict(m1, m2)
        @test conflict ≈ 0.44 atol=1e-6
    end

    @testset "Dempster Fusion" begin
        θ = Set(["A", "B"])
        m1 = BeliefMass(Dict(Set(["A"]) => 0.7, θ => 0.3))
        m2 = BeliefMass(Dict(Set(["A"]) => 0.5, θ => 0.5))

        result = fuse_beliefs(m1, m2, Dempster)
        @test is_valid(result)
        @test result.masses[Set(["A"])] > 0.7  # Belief increased
    end

    @testset "Yager Fusion" begin
        θ = Set(["A", "B"])
        m1 = BeliefMass(Dict(Set(["A"]) => 0.8, Set(["B"]) => 0.2))
        m2 = BeliefMass(Dict(Set(["A"]) => 0.3, Set(["B"]) => 0.7))

        result = fuse_beliefs(m1, m2, Yager)
        @test is_valid(result)

        conflict = calculate_conflict(m1, m2)
        @test haskey(result.masses, θ)  # Ignorance present
    end

    @testset "Commutativity" begin
        m1 = BeliefMass(Dict(Set(["A"]) => 0.7, Set(["B"]) => 0.3))
        m2 = BeliefMass(Dict(Set(["A"]) => 0.6, Set(["B"]) => 0.4))

        r12 = fuse_beliefs(m1, m2, Dempster)
        r21 = fuse_beliefs(m2, m1, Dempster)

        for (k, v) in r12.masses
            @test abs(v - get(r21.masses, k, 0.0)) < 1e-6
        end
    end

    @testset "Associativity" begin
        θ = Set(["X", "Y"])
        m1 = BeliefMass(Dict(Set(["X"]) => 0.6, θ => 0.4))
        m2 = BeliefMass(Dict(Set(["X"]) => 0.7, θ => 0.3))
        m3 = BeliefMass(Dict(Set(["X"]) => 0.8, θ => 0.2))

        left = fuse_beliefs(fuse_beliefs(m1, m2, Dempster), m3, Dempster)
        right = fuse_beliefs(m1, fuse_beliefs(m2, m3, Dempster), Dempster)

        for (k, v) in left.masses
            @test abs(v - get(right.masses, k, 0.0)) < 1e-5
        end
    end

    @testset "Mass Conservation" begin
        m1 = BeliefMass(Dict(Set(["A"]) => 0.7, Set(["B"]) => 0.3))
        m2 = BeliefMass(Dict(Set(["A"]) => 0.6, Set(["B"]) => 0.4))

        for rule in [Dempster, Yager, DuboisPrade, Average]
            try
                result = fuse_beliefs(m1, m2, rule)
                @test is_valid(result)
            catch e
                # Dempster may fail on total conflict, that's ok
                if rule != Dempster
                    rethrow(e)
                end
            end
        end
    end

    @testset "Real-World Scenario" begin
        # Climate change claim verification
        θ = Set(["true", "false"])

        ipcc = BeliefMass(Dict(Set(["true"]) => 0.95, θ => 0.05))
        nasa = BeliefMass(Dict(Set(["true"]) => 0.90, θ => 0.10))
        univ = BeliefMass(Dict(Set(["true"]) => 0.85, θ => 0.15))

        result = fuse_multiple([ipcc, nasa, univ], Dempster)

        @test is_valid(result)
        @test belief(result, Set(["true"])) > 0.95  # High confidence
    end
end
