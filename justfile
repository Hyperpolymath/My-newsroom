# Justfile for My-newsroom (Julia + Rust)

# Default: show help
default:
    @just --list

# Install Julia dependencies
install:
    julia --project=. -e 'using Pkg; Pkg.instantiate()'

# Run Julia tests
test:
    julia --project=. test/runtests.jl

# Run examples
example-basic:
    julia --project=. examples/julia/basic_fusion.jl

# Build Rust Solo compiler
build-solo:
    cd solo-compiler && cargo build --release

# Test Solo compiler
test-solo:
    cd solo-compiler && cargo test

# Lint Solo compiler
lint-solo:
    cd solo-compiler && cargo clippy -- -D warnings
    cd solo-compiler && cargo fmt -- --check

# RSR validation
validate:
    @echo "Checking RSR Bronze level compliance..."
    @test -f README.md || (echo "❌ README.md missing" && exit 1)
    @test -f LICENSE.txt || (echo "❌ LICENSE.txt missing" && exit 1)
    @test -f SECURITY.md || (echo "❌ SECURITY.md missing" && exit 1)
    @test -f .well-known/security.txt || (echo "❌ security.txt missing" && exit 1)
    @echo "✅ RSR Bronze level requirements met"

# Full CI pipeline
ci: test test-solo lint-solo validate
    @echo "✅ Full CI pipeline passed"

# Clean build artifacts
clean:
    rm -rf target/
    rm -rf solo-compiler/target/
    find . -name "*.ji" -delete

# Count lines of code
loc:
    @echo "=== Julia ==="
    @find src -name "*.jl" | xargs wc -l | tail -1
    @echo ""
    @echo "=== Rust (Solo) ==="
    @find solo-compiler/src -name "*.rs" | xargs wc -l | tail -1
