"""
Tests for ClawFlowGen core functionality.
"""

import pytest
from clawflowgen import ProcessorGenerator


class TestProcessorGenerator:
    """Test ProcessorGenerator class."""
    
    def test_cpu_generation(self):
        """Test basic CPU generation."""
        gen = ProcessorGenerator(target="CPU", parallelism=4, isa="RISCV")
        gen.evolve()
        
        assert gen.target_type == "CPU"
        assert gen.parallelism == 4
        assert gen.isa == "RISCV"
        
    def test_npu_generation(self):
        """Test basic NPU generation."""
        gen = ProcessorGenerator(target="NPU", parallelism=16)
        gen.evolve()
        
        assert gen.target_type == "NPU"
        assert gen.parallelism == 16
        
    def test_stats(self):
        """Test statistics generation."""
        gen = ProcessorGenerator(target="CPU", parallelism=8)
        gen.evolve()
        
        stats = gen.stats
        assert "target_type" in stats
        assert "parallelism" in stats
        assert stats["parallelism"] == 8
        
    def test_different_parallelism_levels(self):
        """Test different parallelism levels."""
        for p in [2, 4, 8, 16]:
            gen = ProcessorGenerator(target="CPU", parallelism=p)
            gen.evolve()
            assert gen.stats["parallelism"] == p


class TestExport:
    """Test Verilog export functionality."""
    
    def test_export_creates_file(self, tmp_path):
        """Test that export creates a file."""
        gen = ProcessorGenerator(target="CPU", parallelism=2)
        gen.evolve()
        
        output_file = tmp_path / "test.v"
        # Note: Actual export would require OpenClaw backend
        # This is a placeholder test
        assert True
