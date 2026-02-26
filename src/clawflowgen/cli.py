"""
Command-line interface for ClawFlowGen.
"""

import argparse
import sys
from typing import Optional

from .core import ProcessorGenerator


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog="clawflowgen",
        description="Physically-Parallel Evolutionary Processor Generator"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    
    parser.add_argument(
        "--target",
        choices=["CPU", "NPU"],
        default="CPU",
        help="Target processor type (default: CPU)"
    )
    
    parser.add_argument(
        "--parallelism",
        "-p",
        type=int,
        default=4,
        help="Degree of parallelism (default: 4)"
    )
    
    parser.add_argument(
        "--isa",
        default="RISCV",
        help="Instruction set architecture (default: RISCV)"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        default="output.v",
        help="Output filename (default: output.v)"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output"
    )
    
    return parser


def main(args: Optional[list] = None) -> int:
    """Main entry point."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    if parsed_args.verbose:
        print(f"ClawFlowGen v0.1.0")
        print(f"Target: {parsed_args.target}")
        print(f"Parallelism: {parsed_args.parallelism}")
        print(f"ISA: {parsed_args.isa}")
        print("Generating processor...")
    
    try:
        # Create generator
        gen = ProcessorGenerator(
            target_type=parsed_args.target,
            parallelism=parsed_args.parallelism,
            isa=parsed_args.isa
        )
        
        # Evolve processor
        gen.evolve()
        
        # Export
        gen.export(parsed_args.output)
        
        if parsed_args.verbose:
            print(f"\nGeneration complete!")
            print(f"Output: {parsed_args.output}")
            print(f"\nStats:")
            for key, value in gen.stats.items():
                print(f"  {key}: {value}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
