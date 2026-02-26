"""
Operator library for execution units.
"""

from typing import List, Dict, Any
import openclaw as oc


class ExecutionUnit(oc.Module):
    """Base class for execution units."""
    
    def __init__(self, name: str, operators: List[str]):
        super().__init__(name)
        self.operators = operators
        self.input_count = 2
        self.output_count = 1
        
        for op in operators:
            self.add_instance(op)


class OperatorLibrary:
    """Library of available operators."""
    
    OPERATORS = {
        "ALU": {
            "latency": 1,
            "area": 45.2,
            "power": 12.5,
            "bitwidths": [32, 64],
        },
        "MUL": {
            "latency": 3,
            "area": 120.5,
            "power": 35.8,
            "bitwidths": [32, 64],
        },
        "FPU": {
            "latency": 4,
            "area": 210.5,
            "power": 85.2,
            "bitwidths": [32, 64],
        },
        "MAC": {
            "latency": 1,
            "area": 185.0,
            "power": 65.5,
            "bitwidths": [8, 16, 32],
        },
        "BRU": {
            "latency": 1,
            "area": 65.0,
            "power": 22.5,
            "bitwidths": [32, 64],
        },
    }
    
    @classmethod
    def get_operator(cls, name: str) -> Dict[str, Any]:
        """Get operator specifications."""
        return cls.OPERATORS.get(name, {})
    
    @classmethod
    def list_operators(cls) -> List[str]:
        """List all available operators."""
        return list(cls.OPERATORS.keys())
