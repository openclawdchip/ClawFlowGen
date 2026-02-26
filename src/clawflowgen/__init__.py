"""
ClawFlowGen: Physically-Parallel Evolutionary Processor Generator

A Python-based hardware generation framework that grows processors
from parallel operator islands to complete systems.

Example:
    >>> from clawflowgen import ProcessorGenerator
    >>> cpu = ProcessorGenerator(target="CPU", parallelism=8)
    >>> cpu.evolve()
    >>> cpu.export("my_cpu.v")
"""

__version__ = "0.1.0"
__author__ = "OpenClaw Research Team"
__email__ = "xiao.lin@ia.ac.cn"
__license__ = "MIT"

from .core import ProcessorGenerator
from .operators import ExecutionUnit, OperatorLibrary
from .interconnect import Crossbar, Mesh, NoC
from .memory import RegFile, Cache, LSU

__all__ = [
    "ProcessorGenerator",
    "ExecutionUnit", 
    "OperatorLibrary",
    "Crossbar",
    "Mesh",
    "NoC",
    "RegFile",
    "Cache",
    "LSU",
]
