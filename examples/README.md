# My-newsroom Examples

## Julia Examples (Dempster-Shafer)

### basic_fusion.jl
```bash
julia --project=. examples/julia/basic_fusion.jl
```

Demonstrates:
- Creating belief masses
- Fusing with Dempster and Yager rules
- Calculating uncertainty intervals

## Solo Examples

### hello_world.solo
```bash
cd solo-compiler
cargo build --release
./target/release/solo check ../examples/solo/hello_world.solo
```

### belief_example.solo
Demonstrates epistemic types with affine ownership.

## Running Examples

```bash
# Julia
just example-basic

# Solo (after building compiler)
just build-solo
cd solo-compiler
./target/release/solo check ../examples/solo/hello_world.solo
```
