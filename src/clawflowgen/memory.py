"""
Memory hierarchy components.
"""

import openclaw as oc


class RegFile(oc.Module):
    """Multi-port register file."""
    
    def __init__(self, depth: int = 32, rd_ports: int = 8, wr_ports: int = 4):
        super().__init__(f"RegFile_{depth}x{rd_ports}R{wr_ports}W")
        self.depth = depth
        self.rd_ports = rd_ports
        self.wr_ports = wr_ports
        
        # Generate multi-port memory
        for i in range(rd_ports):
            self.add_output(f"rd_data_{i}", 64)
        for i in range(wr_ports):
            self.add_input(f"wr_data_{i}", 64)


class Cache(oc.Module):
    """Cache memory."""
    
    def __init__(self, size: str = "32KB", ways: int = 4, line_size: int = 64):
        super().__init__(f"Cache_{size}")
        self.size = size
        self.ways = ways
        self.line_size = line_size
        
        # Generate cache structure
        for i in range(ways):
            self.add_instance(f"Way_{i}")


class LSU(oc.Module):
    """Load-Store Unit."""
    
    def __init__(self, ports: int = 4, mshrs: int = 16):
        super().__init__(f"LSU_{ports}P{mshrs}MSHR")
        self.ports = ports
        self.mshrs = mshrs
        
        # Generate parallel load/store buffers
        for i in range(ports):
            self.add_instance(f"LoadBuffer_{i}")
            self.add_instance(f"StoreBuffer_{i}")
        
        # Generate MSHRs for cache miss handling
        for i in range(mshrs):
            self.add_instance(f"MSHR_{i}")
