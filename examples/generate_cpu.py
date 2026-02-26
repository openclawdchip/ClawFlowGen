"""
Example: Generate a 4-issue RISC-V CPU
"""

from clawflowgen import ProcessorGenerator


def main():
    """Generate a simple CPU."""
    print("=" * 60)
    print("ClawFlowGen Example: 4-issue RISC-V CPU")
    print("=" * 60)
    
    # Create generator
    cpu = ProcessorGenerator(
        target="CPU",
        parallelism=4,
        isa="RISCV"
    )
    
    print(f"\nConfiguration:")
    print(f"  Target: CPU")
    print(f"  Parallelism: 4")
    print(f"  ISA: RISCV")
    
    # Evolve processor
    print("\nEvolving processor...")
    cpu.evolve()
    
    # Show stats
    print("\nGenerated Processor Stats:")
    for key, value in cpu.stats.items():
        print(f"  {key}: {value}")
    
    # Export
    output_file = "cpu_4way.v"
    print(f"\nExporting to {output_file}...")
    cpu.export(output_file)
    
    print("\nDone!")


if __name__ == "__main__":
    main()
