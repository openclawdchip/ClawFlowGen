"""
Design validation for generated processors.
"""

from typing import List, Dict, Any, Tuple
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ValidationLevel(Enum):
    """Validation severity levels."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ValidationResult:
    """Validation result container."""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.infos: List[str] = []
    
    def add_error(self, message: str) -> None:
        self.errors.append(message)
        logger.error(f"[VALIDATION ERROR] {message}")
    
    def add_warning(self, message: str) -> None:
        self.warnings.append(message)
        logger.warning(f"[VALIDATION WARNING] {message}")
    
    def add_info(self, message: str) -> None:
        self.infos.append(message)
        logger.info(f"[VALIDATION INFO] {message}")
    
    def is_valid(self) -> bool:
        return len(self.errors) == 0
    
    def __str__(self) -> str:
        lines = ["Validation Report:"]
        if self.errors:
            lines.append(f"  Errors: {len(self.errors)}")
            for e in self.errors:
                lines.append(f"    - {e}")
        if self.warnings:
            lines.append(f"  Warnings: {len(self.warnings)}")
            for w in self.warnings:
                lines.append(f"    - {w}")
        if self.infos:
            lines.append(f"  Infos: {len(self.infos)}")
        return "\n".join(lines)


class DesignValidator:
    """Validates generated processor designs."""
    
    def __init__(self, processor_gen: Any):
        self.gen = processor_gen
        self.result = ValidationResult()
    
    def validate_all(self) -> ValidationResult:
        """Run all validation checks."""
        self.validate_structure()
        self.validate_timing()
        self.validate_area()
        self.validate_power()
        self.validate_connectivity()
        return self.result
    
    def validate_structure(self) -> None:
        """Validate design structure."""
        # Check EU pool
        if not hasattr(self.gen, '_eu_pool') or len(self.gen._eu_pool) == 0:
            self.result.add_error("No execution units found in design")
        elif len(self.gen._eu_pool) != self.gen.config.parallelism:
            self.result.add_warning(
                f"EU count mismatch: expected {self.gen.config.parallelism}, "
                f"found {len(self.gen._eu_pool)}"
            )
        
        # Check register file
        if not hasattr(self.gen, '_regfile') or self.gen._regfile is None:
            self.result.add_error("Register file not generated")
        
        # Check interconnect
        if not hasattr(self.gen, '_interconnect') or self.gen._interconnect is None:
            self.result.add_error("Interconnect not generated")
        
        # Check controller
        if not hasattr(self.gen, '_controller') or self.gen._controller is None:
            self.result.add_error("Controller not generated")
        
        logger.info("Structure validation completed")
    
    def validate_timing(self) -> None:
        """Validate timing constraints."""
        config = self.gen.config
        
        # Check frequency feasibility
        if config.timing.target_frequency > 4.0:
            self.result.add_warning(
                f"Target frequency {config.timing.target_frequency} GHz may be "
                "challenging for standard cells"
            )
        
        # Check setup/hold times
        if config.timing.setup_time < 0.02:
            self.result.add_warning("Setup time may be too aggressive")
        
        logger.info("Timing validation completed")
    
    def validate_area(self) -> None:
        """Validate area constraints."""
        # Estimate area based on parallelism
        p = self.gen.config.parallelism
        est_area = p * 200  # μm² per EU (rough estimate)
        
        # Crossbar area grows as O(P²)
        if self.gen.config.interconnect.topology == "crossbar":
            xbar_area = p * p * 2
            est_area += xbar_area
            
            if xbar_area > est_area * 0.5:
                self.result.add_warning(
                    f"Crossbar area ({xbar_area} μm²) dominates design. "
                    "Consider Mesh or NoC topology for better scalability"
                )
        
        logger.info(f"Estimated area: {est_area} μm²")
    
    def validate_power(self) -> None:
        """Validate power constraints."""
        # Estimate dynamic power
        p = self.gen.config.parallelism
        est_power = p * 50  # mW per EU
        
        if est_power > 5000:  # 5W
            self.result.add_warning(
                f"Estimated power ({est_power} mW) is high. "
                "Consider clock gating or power domains"
            )
        
        logger.info(f"Estimated power: {est_power} mW")
    
    def validate_connectivity(self) -> None:
        """Validate connectivity."""
        # Check for unconnected ports
        # This would require deeper inspection of the design
        
        # Check for potential deadlocks in NoC
        if self.gen.config.interconnect.topology == "noc":
            self.result.add_info(
                "NoC topology selected. Ensure deadlock-free routing algorithm"
            )
        
        logger.info("Connectivity validation completed")


class TimingAnalyzer:
    """Analyzes timing of generated designs."""
    
    def __init__(self, processor_gen: Any):
        self.gen = processor_gen
    
    def analyze_critical_path(self) -> Dict[str, Any]:
        """Analyze critical path delay."""
        # Simplified timing model
        
        config = self.gen.config
        
        # Component delays (in ps)
        regfile_read = 85
        xbar_transit = 95 if config.interconnect.topology == "crossbar" else 50
        eu_compute = 180
        writeback = 70
        
        total_delay = regfile_read + xbar_transit + eu_compute + writeback
        
        # Calculate max frequency
        max_freq = 1000 / total_delay  # GHz
        
        return {
            "total_delay_ps": total_delay,
            "max_frequency_ghz": max_freq,
            "target_frequency_ghz": config.timing.target_frequency,
            "slack_ps": (1000 / config.timing.target_frequency) - total_delay,
            "components": {
                "regfile_read": regfile_read,
                "interconnect": xbar_transit,
                "execution": eu_compute,
                "writeback": writeback
            }
        }
    
    def check_setup_hold(self) -> Dict[str, bool]:
        """Check setup and hold time constraints."""
        timing = self.analyze_critical_path()
        
        cycle_time = 1000 / self.gen.config.timing.target_frequency
        
        setup_ok = timing["total_delay_ps"] < cycle_time - self.gen.config.timing.setup_time * 1000
        hold_ok = timing["total_delay_ps"] > self.gen.config.timing.hold_time * 1000
        
        return {
            "setup_ok": setup_ok,
            "hold_ok": hold_ok,
            "cycle_time_ps": cycle_time
        }


class AreaEstimator:
    """Estimates area of generated designs."""
    
    AREA_TABLE = {
        "ALU": 45.2,
        "MUL": 120.5,
        "FPU": 210.5,
        "MAC": 185.0,
        "BRU": 65.0,
        "LSU": 150.0,
    }
    
    def __init__(self, processor_gen: Any):
        self.gen = processor_gen
    
    def estimate_total_area(self) -> Dict[str, float]:
        """Estimate total design area."""
        p = self.gen.config.parallelism
        
        # EU area
        eu_area = sum(self.AREA_TABLE.get(op, 50) for op in self.gen._select_operators()) * p
        
        # RegFile area (rough estimate)
        regfile_area = p * 100
        
        # Interconnect area
        if self.gen.config.interconnect.topology == "crossbar":
            iconn_area = p * p * 5
        elif self.gen.config.interconnect.topology == "mesh":
            iconn_area = p * 20
        else:  # noc
            iconn_area = p * 30
        
        # Control logic area
        control_area = 500 if self.gen.config.target == "CPU" else 300
        
        # Memory area
        memory_area = 1000  # Fixed for now
        
        total = eu_area + regfile_area + iconn_area + control_area + memory_area
        
        return {
            "eu_area": eu_area,
            "regfile_area": regfile_area,
            "interconnect_area": iconn_area,
            "control_area": control_area,
            "memory_area": memory_area,
            "total_um2": total,
            "total_mm2": total / 1e6
        }


class PowerEstimator:
    """Estimates power consumption."""
    
    POWER_TABLE = {
        "ALU": 12.5,
        "MUL": 35.8,
        "FPU": 85.2,
        "MAC": 65.5,
        "BRU": 22.5,
        "LSU": 45.0,
    }
    
    def __init__(self, processor_gen: Any):
        self.gen = processor_gen
    
    def estimate_power(self, activity_factor: float = 0.5) -> Dict[str, float]:
        """Estimate power consumption."""
        p = self.gen.config.parallelism
        
        # Dynamic power (mW)
        eu_power = sum(self.POWER_TABLE.get(op, 20) for op in self.gen._select_operators()) * p * activity_factor
        
        # Interconnect power
        iconn_power = p * 10 * activity_factor
        
        # Clock power
        clock_power = p * 15
        
        # Memory power
        memory_power = 100
        
        dynamic = eu_power + iconn_power + clock_power + memory_power
        
        # Leakage power (10% of dynamic)
        leakage = dynamic * 0.1
        
        return {
            "dynamic_mw": dynamic,
            "leakage_mw": leakage,
            "total_mw": dynamic + leakage,
            "activity_factor": activity_factor
        }
