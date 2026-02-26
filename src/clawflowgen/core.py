"""
Core processor generator implementation.
"""

from typing import List, Optional, Dict, Any
import openclaw as oc

from .config import GeneratorConfig
from .validator import DesignValidator, TimingAnalyzer, AreaEstimator, PowerEstimator
from .exporter import VerilogExporter


class ProcessorGenerator:
    """
    Main processor generator class implementing the four-stage evolutionary algorithm.
    
    This class generates processors from the inside out:
    1. Physical tiling of operator islands
    2. Data flow layer generation  
    3. Control flow collapse
    4. Memory periphery integration
    
    Args:
        target_type: Type of processor to generate ("CPU" or "NPU")
        parallelism: Degree of parallelism (number of execution units)
        isa: Instruction set architecture (for CPU mode)
        config: Detailed configuration object (optional)
        
    Example:
        >>> gen = ProcessorGenerator(target="CPU", parallelism=8, isa="RISCV")
        >>> gen.evolve()
        >>> gen.validate()
        >>> gen.export("my_cpu.v")
    """
    
    def __init__(
        self,
        target_type: str = "CPU",
        parallelism: int = 4,
        isa: Optional[str] = "RISCV",
        config: Optional[GeneratorConfig] = None,
        debug: bool = False,
        **kwargs: Any
    ):
        self.target_type = target_type
        self.parallelism = parallelism
        self.isa = isa
        self.debug = debug
        
        # Use provided config or create default
        if config is None:
            self.config = GeneratorConfig(
                target=target_type,
                parallelism=parallelism,
                isa=isa,
                debug=debug,
                **kwargs
            )
        else:
            self.config = config
        
        # Evolution state
        self._eu_pool: List[oc.Module] = []
        self._regfile: Optional[oc.Module] = None
        self._interconnect: Optional[oc.Module] = None
        self._controller: Optional[oc.Module] = None
        self._memory: Optional[oc.Module] = None
        
        # Validators
        self._validator: Optional[DesignValidator] = None
        self._timing_analyzer: Optional[TimingAnalyzer] = None
        self._area_estimator: Optional[AreaEstimator] = None
        self._power_estimator: Optional[PowerEstimator] = None
        
        # Exporter
        self._exporter: Optional[VerilogExporter] = None
        
    def evolve(self) -> None:
        """
        Execute the four-stage evolutionary algorithm.
        
        This method orchestrates the complete processor generation process,
        from bare operators to a complete system.
        """
        if self.debug:
            print(f"[ClawFlowGen] Starting evolution: {self.target_type}, P={self.parallelism}")
        
        self._phase1_operator_tiling()
        if self.debug:
            print(f"[Phase 1] Generated {len(self._eu_pool)} execution units")
        
        self._phase2_dataflow_generation()
        if self.debug:
            print(f"[Phase 2] Generated interconnect: {self.config.interconnect.topology}")
        
        self._phase3_control_collapse()
        if self.debug:
            print(f"[Phase 3] Generated controller: {self.target_type} mode")
        
        self._phase4_memory_integration()
        if self.debug:
            print(f"[Phase 4] Integrated memory hierarchy")
        
        # Initialize validators
        self._validator = DesignValidator(self)
        self._timing_analyzer = TimingAnalyzer(self)
        self._area_estimator = AreaEstimator(self)
        self._power_estimator = PowerEstimator(self)
        self._exporter = VerilogExporter(self)
        
        if self.debug:
            print("[ClawFlowGen] Evolution complete!")
        
    def _phase1_operator_tiling(self) -> None:
        """Phase 1: Physical tiling of execution units."""
        ops = self._select_operators()
        for i in range(self.parallelism):
            eu = oc.Module(f"EU_{i}")
            for op in ops:
                eu.add_instance(op)
            self._eu_pool.append(eu)
            
    def _phase2_dataflow_generation(self) -> None:
        """Phase 2: Generate interconnect and register file."""
        # Calculate port requirements
        total_reads = sum(eu.input_count for eu in self._eu_pool)
        total_writes = sum(eu.output_count for eu in self._eu_pool)
        
        # Generate multi-port register file
        self._regfile = oc.MultiPortRegFile(
            depth=32,
            rd_ports=total_reads,
            wr_ports=total_writes
        )
        
        # Generate interconnect
        self._interconnect = self._generate_interconnect()
        
    def _phase3_control_collapse(self) -> None:
        """Phase 3: Generate decoder and scheduler."""
        if self.target_type == "CPU":
            self._controller = oc.OoOScheduler(
                width=self.parallelism,
                rob_entries=self.parallelism * 4
            )
        else:  # NPU
            self._controller = oc.SystolicController(
                dim=self.parallelism
            )
            
    def _phase4_memory_integration(self) -> None:
        """Phase 4: Integrate LSU and cache."""
        self._memory = oc.LoadStoreUnit(
            ports=self.parallelism // 2,
            mshrs=self.parallelism * 2
        )
        
    def _select_operators(self) -> List[str]:
        """Select appropriate operators based on target type."""
        if self.target_type == "CPU":
            return ["ALU", "MUL", "FPU", "BRU"]
        else:  # NPU
            return ["MAC", "VEC_ADD", "VEC_MUL"]
            
    def _generate_interconnect(self) -> oc.Module:
        """Generate appropriate interconnect based on parallelism."""
        if self.parallelism <= 4:
            return oc.Crossbar(self._eu_pool)
        elif self.parallelism <= 16:
            return oc.Mesh(self._eu_pool)
        else:
            return oc.NoC(self._eu_pool)
    
    def validate(self) -> bool:
        """
        Validate the generated design.
        
        Returns:
            True if design is valid, False otherwise
        """
        if self._validator is None:
            raise RuntimeError("Design not evolved yet. Call evolve() first.")
        
        result = self._validator.validate_all()
        print(result)
        return result.is_valid()
    
    def analyze_timing(self) -> Dict[str, Any]:
        """
        Analyze timing of the generated design.
        
        Returns:
            Timing analysis results
        """
        if self._timing_analyzer is None:
            raise RuntimeError("Design not evolved yet. Call evolve() first.")
        
        return self._timing_analyzer.analyze_critical_path()
    
    def estimate_area(self) -> Dict[str, float]:
        """
        Estimate area of the generated design.
        
        Returns:
            Area estimation results
        """
        if self._area_estimator is None:
            raise RuntimeError("Design not evolved yet. Call evolve() first.")
        
        return self._area_estimator.estimate_total_area()
    
    def estimate_power(self, activity_factor: float = 0.5) -> Dict[str, float]:
        """
        Estimate power consumption of the generated design.
        
        Args:
            activity_factor: Activity factor (0.0 to 1.0)
            
        Returns:
            Power estimation results
        """
        if self._power_estimator is None:
            raise RuntimeError("Design not evolved yet. Call evolve() first.")
        
        return self._power_estimator.estimate_power(activity_factor)
            
    def export(self, filename: str) -> None:
        """
        Export generated processor to Verilog.
        
        Args:
            filename: Output filename (e.g., "my_cpu.v")
        """
        if self._exporter is None:
            raise RuntimeError("Design not evolved yet. Call evolve() first.")
        
        self._exporter.export(filename)
        
    @property
    def stats(self) -> Dict[str, Any]:
        """Return generation statistics."""
        return {
            "target_type": self.target_type,
            "parallelism": self.parallelism,
            "num_operators": len(self._eu_pool),
            "isa": self.isa,
            "interconnect": self.config.interconnect.topology,
            "arbitration": self.config.interconnect.arbitration,
        }
    
    def dump_phase1(self) -> None:
        """Dump phase 1 (tiling) results for debugging."""
        print("=== Phase 1: Physical Tiling ===")
        print(f"EU Count: {len(self._eu_pool)}")
        for i, eu in enumerate(self._eu_pool):
            print(f"  EU_{i}: {eu}")
    
    def dump_interconnect(self) -> None:
        """Dump interconnect details for debugging."""
        print("=== Interconnect Details ===")
        print(f"Type: {self.config.interconnect.topology}")
        print(f"Arbitration: {self.config.interconnect.arbitration}")
        print(f"EU Pool Size: {len(self._eu_pool)}")


def create_cpu(parallelism: int = 8, **kwargs) -> ProcessorGenerator:
    """
    Convenience function to create a CPU generator.
    
    Args:
        parallelism: Number of execution units
        **kwargs: Additional configuration options
        
    Returns:
        Configured ProcessorGenerator for CPU
    """
    return ProcessorGenerator(
        target_type="CPU",
        parallelism=parallelism,
        isa="RISCV",
        **kwargs
    )


def create_npu(parallelism: int = 256, **kwargs) -> ProcessorGenerator:
    """
    Convenience function to create an NPU generator.
    
    Args:
        parallelism: Number of PEs (should be perfect square for systolic)
        **kwargs: Additional configuration options
        
    Returns:
        Configured ProcessorGenerator for NPU
    """
    return ProcessorGenerator(
        target_type="NPU",
        parallelism=parallelism,
        **kwargs
    )
