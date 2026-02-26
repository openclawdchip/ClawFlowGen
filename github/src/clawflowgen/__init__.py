"""
ClawFlowGen: Physically-Parallel Evolutionary Processor Generator

A Python-based hardware generation framework that grows processors
from parallel operator islands to complete systems.

Example:
    >>> from clawflowgen import ProcessorGenerator
    >>> cpu = ProcessorGenerator(target="CPU", parallelism=8)
    >>> cpu.evolve()
    >>> cpu.export("my_cpu.v")

Modules:
    core: Main processor generator
    operators: Operator library
    interconnect: Interconnect generation
    memory: Memory hierarchy
    config: Configuration management
    validator: Design validation
    exporter: RTL code export
    cli: Command-line interface
"""

__version__ = "0.1.0"
__author__ = "OpenClaw Research Team"
__email__ = "xiao.lin@ia.ac.cn"
__license__ = "MIT"
__url__ = "https://github.com/openclawdchip/clawflowgen"

# Core classes
from .core import ProcessorGenerator

# Configuration
from .config import (
    GeneratorConfig,
    CacheConfig,
    InterconnectConfig,
    TimingConfig
)

# Components
from .operators import ExecutionUnit, OperatorLibrary
from .interconnect import Crossbar, Mesh, NoC
from .memory import RegFile, Cache, LSU

# Utilities
from .validator import (
    DesignValidator,
    ValidationResult,
    TimingAnalyzer,
    AreaEstimator,
    PowerEstimator
)
from .exporter import VerilogExporter, RTLTemplate

__all__ = [
    # Core
    "ProcessorGenerator",
    
    # Configuration
    "GeneratorConfig",
    "CacheConfig",
    "InterconnectConfig",
    "TimingConfig",
    
    # Components
    "ExecutionUnit",
    "OperatorLibrary",
    "Crossbar",
    "Mesh",
    "NoC",
    "RegFile",
    "Cache",
    "LSU",
    
    # Validation
    "DesignValidator",
    "ValidationResult",
    "TimingAnalyzer",
    "AreaEstimator",
    "PowerEstimator",
    
    # Export
    "VerilogExporter",
    "RTLTemplate",
]
