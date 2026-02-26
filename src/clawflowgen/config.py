"""
Configuration management for ClawFlowGen.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
import yaml


@dataclass
class CacheConfig:
    """Cache configuration."""
    size: str = "32KB"
    ways: int = 4
    line_size: int = 64
    mshrs: int = 16
    write_policy: str = "writeback"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "size": self.size,
            "ways": self.ways,
            "line_size": self.line_size,
            "mshrs": self.mshrs,
            "write_policy": self.write_policy
        }


@dataclass
class InterconnectConfig:
    """Interconnect configuration."""
    topology: str = "crossbar"  # crossbar, mesh, noc
    arbitration: str = "LRU"    # LRU, priority, round_robin
    buffer_depth: int = 4
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "topology": self.topology,
            "arbitration": self.arbitration,
            "buffer_depth": self.buffer_depth
        }


@dataclass
class TimingConfig:
    """Timing configuration."""
    target_frequency: float = 2.5  # GHz
    process_node: str = "7nm"
    setup_time: float = 0.05  # ns
    hold_time: float = 0.05   # ns
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_frequency": self.target_frequency,
            "process_node": self.process_node,
            "setup_time": self.setup_time,
            "hold_time": self.hold_time
        }


@dataclass
class GeneratorConfig:
    """Main generator configuration."""
    target: str = "CPU"  # CPU or NPU
    parallelism: int = 4
    isa: str = "RISCV"
    
    # Sub-configs
    cache: CacheConfig = field(default_factory=CacheConfig)
    interconnect: InterconnectConfig = field(default_factory=InterconnectConfig)
    timing: TimingConfig = field(default_factory=TimingConfig)
    
    # Operator configuration
    operators: List[Dict[str, Any]] = field(default_factory=list)
    
    # Debug options
    debug: bool = False
    dump_intermediate: bool = False
    verbose: bool = False
    
    @classmethod
    def from_yaml(cls, filepath: str) -> "GeneratorConfig":
        """Load configuration from YAML file."""
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GeneratorConfig":
        """Create config from dictionary."""
        config = cls(
            target=data.get('target', 'CPU'),
            parallelism=data.get('parallelism', 4),
            isa=data.get('isa', 'RISCV'),
            debug=data.get('debug', False),
            dump_intermediate=data.get('dump_intermediate', False),
            verbose=data.get('verbose', False)
        )
        
        # Parse sub-configs
        if 'cache' in data:
            cache_data = data['cache']
            config.cache = CacheConfig(**cache_data)
        
        if 'interconnect' in data:
            iconn_data = data['interconnect']
            config.interconnect = InterconnectConfig(**iconn_data)
        
        if 'timing' in data:
            timing_data = data['timing']
            config.timing = TimingConfig(**timing_data)
        
        if 'operators' in data:
            config.operators = data['operators']
        
        return config
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "target": self.target,
            "parallelism": self.parallelism,
            "isa": self.isa,
            "cache": self.cache.to_dict(),
            "interconnect": self.interconnect.to_dict(),
            "timing": self.timing.to_dict(),
            "operators": self.operators,
            "debug": self.debug,
            "dump_intermediate": self.dump_intermediate,
            "verbose": self.verbose
        }
    
    def to_yaml(self, filepath: str) -> None:
        """Save configuration to YAML file."""
        with open(filepath, 'w') as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False)
    
    def validate(self) -> bool:
        """Validate configuration."""
        # Check target type
        if self.target not in ["CPU", "NPU"]:
            raise ValueError(f"Invalid target: {self.target}. Must be 'CPU' or 'NPU'")
        
        # Check parallelism
        if self.parallelism < 1 or self.parallelism > 1024:
            raise ValueError(f"Invalid parallelism: {self.parallelism}. Must be in [1, 1024]")
        
        # Check ISA
        valid_isas = ["RISCV", "ARM", "X86", "CUSTOM"]
        if self.isa not in valid_isas:
            raise ValueError(f"Invalid ISA: {self.isa}. Must be one of {valid_isas}")
        
        # Check topology
        valid_topologies = ["crossbar", "mesh", "noc"]
        if self.interconnect.topology not in valid_topologies:
            raise ValueError(f"Invalid topology: {self.interconnect.topology}")
        
        # Check arbitration
        valid_arbitrations = ["LRU", "priority", "round_robin"]
        if self.interconnect.arbitration not in valid_arbitrations:
            raise ValueError(f"Invalid arbitration: {self.interconnect.arbitration}")
        
        return True
    
    def __str__(self) -> str:
        return f"GeneratorConfig(target={self.target}, P={self.parallelism}, ISA={self.isa})"
