"""
Interconnect generation for parallel execution units.
"""

from typing import List
import openclaw as oc


class Crossbar(oc.Module):
    """Full crossbar interconnect."""
    
    def __init__(self, units: List[oc.Module]):
        super().__init__("Crossbar")
        self.units = units
        
        # Generate full crossbar connections
        for i, src in enumerate(units):
            for j, dst in enumerate(units):
                if i != j:
                    self.connect(src.output, dst.input)


class Mesh(oc.Module):
    """2D mesh interconnect."""
    
    def __init__(self, units: List[oc.Module], dim: int = 4):
        super().__init__("Mesh")
        self.units = units
        self.dim = dim
        
        # Connect in 2D grid topology
        for i, unit in enumerate(units):
            x = i % dim
            y = i // dim
            
            # Connect to neighbors
            if x < dim - 1 and i + 1 < len(units):
                self.connect(unit, units[i + 1])
            if y < dim - 1 and i + dim < len(units):
                self.connect(unit, units[i + dim])


class NoC(oc.Module):
    """Network-on-Chip interconnect for large parallelism."""
    
    def __init__(self, units: List[oc.Module]):
        super().__init__("NoC")
        self.units = units
        
        # Generate packet-switched network
        for unit in units:
            router = self.add_instance("Router")
            self.connect(unit, router)
