"""
Core processor generator implementation.
"""

from typing import List, Optional, Dict, Any
import openclaw as oc


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
        
    Example:
        >>> gen = ProcessorGenerator(target="CPU", parallelism=8, isa="RISCV")
        >>> gen.evolve()
        >>> gen.export("my_cpu.v")
    """
    
    def __init__(
        self,
        target_type: str = "CPU",
        parallelism: int = 4,
        isa: Optional[str] = "RISCV",
        **kwargs: Any
    ):
        self.target_type = target_type
        self.parallelism = parallelism
        self.isa = isa
        self.config = kwargs
        
        # Evolution state
        self._eu_pool: List[oc.Module] = []
        self._regfile: Optional[oc.Module] = None
        self._interconnect: Optional[oc.Module] = None
        self._controller: Optional[oc.Module] = None
        self._memory: Optional[oc.Module] = None
        
    def evolve(self) -> None:
        """
        Execute the four-stage evolutionary algorithm.
        
        This method orchestrates the complete processor generation process,
        from bare operators to a complete system.
        """
        self._phase1_operator_tiling()
        self._phase2_dataflow_generation()
        self._phase3_control_collapse()
        self._phase4_memory_integration()
        
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
            
    def export(self, filename: str) -> None:
        """
        Export generated processor to Verilog.
        
        Args:
            filename: Output filename (e.g., "my_cpu.v")
        """
        top = oc.Module("Top")
        # Connect all components
        top.connect(self._eu_pool, self._regfile, self._interconnect, 
                   self._controller, self._memory)
        top.export(filename)
        
    @property
    def stats(self) -> Dict[str, Any]:
        """Return generation statistics."""
        return {
            "target_type": self.target_type,
            "parallelism": self.parallelism,
            "num_operators": len(self._eu_pool),
            "isa": self.isa,
        }
