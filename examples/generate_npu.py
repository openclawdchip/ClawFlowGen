"""
Example: Generate a 16x16 Systolic NPU
"""

from clawflowgen import ProcessorGenerator


def main():
    """Generate a systolic NPU."""
    print("=" * 60)
    print("ClawFlowGen Example: 16x16 Systolic NPU")
    print("=" * 60)
    
    # Create generator
    npu = ProcessorGenerator(
        target="NPU",
        parallelism=256,  # 16x16 systolic array
        systolic_dim=(16, 16)
    )
    
    print(f"\nConfiguration:")
    print(f"  Target: NPU")
    print(f"  Parallelism: 256 (16x16 array)")
    print(f"  Type: Systolic Array")
    
    # Evolve processor
    print("\nEvolving NPU...")
    npu.evolve()
    
    # Show stats
    print("\nGenerated NPU Stats:")
    for key, value in npu.stats.items():
        print(f"  {key}: {value}")
    
    # Export
    output_file = "npu_16x16.v"
    print(f"\nExporting to {output_file}...")
    npu.export(output_file)
    
    print("\nDone!")


if __name__ == "__main__":
    main()
