"""
RTL code generation and export.
"""

from typing import Dict, Any, List
from datetime import datetime
import textwrap


class VerilogExporter:
    """Exports generated processor to Verilog RTL."""
    
    def __init__(self, processor_gen: Any):
        self.gen = processor_gen
        self.indent = "  "
    
    def export(self, filename: str) -> None:
        """Export processor to Verilog file."""
        rtl_code = self.generate_rtl()
        
        with open(filename, 'w') as f:
            f.write(rtl_code)
        
        print(f"RTL exported to: {filename}")
    
    def generate_rtl(self) -> str:
        """Generate complete Verilog code."""
        lines = []
        
        # Header
        lines.extend(self._generate_header())
        lines.append("")
        
        # Module declaration
        lines.extend(self._generate_module_decl())
        lines.append("")
        
        # Internal signals
        lines.extend(self._generate_signals())
        lines.append("")
        
        # EU instantiation
        lines.extend(self._generate_eu_instances())
        lines.append("")
        
        # Interconnect
        lines.extend(self._generate_interconnect())
        lines.append("")
        
        # Control logic
        lines.extend(self._generate_control())
        lines.append("")
        
        # Memory
        lines.extend(self._generate_memory())
        lines.append("")
        
        # Endmodule
        lines.append("endmodule")
        
        return "\n".join(lines)
    
    def _generate_header(self) -> List[str]:
        """Generate file header."""
        return [
            "//============================================================================",
            "// ClawFlowGen Generated Processor",
            f"// Target: {self.gen.config.target}",
            f"// Parallelism: {self.gen.config.parallelism}",
            f"// ISA: {self.gen.config.isa}",
            f"// Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "//============================================================================",
            "",
            "`timescale 1ns/1ps",
            ""
        ]
    
    def _generate_module_decl(self) -> List[str]:
        """Generate module declaration."""
        config = self.gen.config
        
        lines = [
            f"module clawflowgen_{config.target.lower()}_p{config.parallelism} (",
            f"{self.indent}input  wire        clk,",
            f"{self.indent}input  wire        rst_n,",
            ""
        ]
        
        # Add instruction interface for CPU
        if config.target == "CPU":
            lines.extend([
                f"{self.indent}// Instruction Interface",
                f"{self.indent}input  wire [31:0]  instr_addr,",
                f"{self.indent}input  wire [31:0]  instr_data,",
                f"{self.indent}input  wire        instr_valid,",
                f"{self.indent}output wire        instr_ready,",
                ""
            ])
        
        # Add data interface
        lines.extend([
            f"{self.indent}// Data Interface",
            f"{self.indent}output wire [31:0]  data_addr,",
            f"{self.indent}inout  wire [63:0]  data,",
            f"{self.indent}output wire        data_we,",
            f"{self.indent}output wire [7:0]   data_be,",
            f"{self.indent}output wire        data_valid,",
            f"{self.indent}input  wire        data_ready,",
            ""
        ])
        
        # Add control interface
        lines.extend([
            f"{self.indent}// Control Interface",
            f"{self.indent}output wire        proc_busy,",
            f"{self.indent}output wire        proc_done",
            ");"
        ])
        
        return lines
    
    def _generate_signals(self) -> List[str]:
        """Generate internal signal declarations."""
        p = self.gen.config.parallelism
        
        lines = [
            "//============================================================================",
            "// Internal Signals",
            "//============================================================================",
            "",
            f"// EU control signals",
            f"wire [{p-1}:0] eu_valid;",
            f"wire [{p-1}:0] eu_ready;",
            f"wire [{p*64-1}:0] eu_result;",
            "",
            f"// Register file interface",
            f"wire [{p*2*5-1}:0] rf_read_addr;",
            f"wire [{p*2*64-1}:0] rf_read_data;",
            f"wire [{p*5-1}:0] rf_write_addr;",
            f"wire [{p*64-1}:0] rf_write_data;",
            f"wire [{p-1}:0] rf_write_en;",
            "",
            "// Control signals",
            "wire [31:0] pc;",
            "wire [31:0] instr;",
            "wire instr_valid_d;",
            ""
        ]
        
        return lines
    
    def _generate_eu_instances(self) -> List[str]:
        """Generate execution unit instances."""
        lines = [
            "//============================================================================",
            "// Execution Units",
            "//============================================================================",
            ""
        ]
        
        ops = self.gen._select_operators()
        for i in range(self.gen.config.parallelism):
            op = ops[i % len(ops)]
            lines.extend([
                f"// EU {i}: {op}",
                f"execution_unit #(",
                f"{self.indent}.OP_TYPE(\"{op}\"),",
                f"{self.indent}.LATENCY({self._get_latency(op)})",
                f") eu_{i} (",
                f"{self.indent}.clk(clk),",
                f"{self.indent}.rst_n(rst_n),",
                f"{self.indent}.valid(eu_valid[{i}]),",
                f"{self.indent}.ready(eu_ready[{i}]),",
                f"{self.indent}.operand_a(rf_read_data[{i*2*64+63}:{i*2*64}]),",
                f"{self.indent}.operand_b(rf_read_data[{(i*2+1)*64+63}:{(i*2+1)*64}]),",
                f"{self.indent}.result(eu_result[{i*64+63}:{i*64}])",
                ");",
                ""
            ])
        
        return lines
    
    def _generate_interconnect(self) -> List[str]:
        """Generate interconnect logic."""
        config = self.gen.config
        
        lines = [
            "//============================================================================",
            f"// Interconnect ({config.interconnect.topology})",
            "//============================================================================",
            ""
        ]
        
        if config.interconnect.topology == "crossbar":
            lines.extend([
                f"// {config.parallelism}x{config.parallelism} Crossbar",
                f"crossbar #(",
                f"{self.indent}.N({config.parallelism}),",
                f"{self.indent}.ARB_POLICY(\"{config.interconnect.arbitration}\")",
                ") xbar (",
                f"{self.indent}.clk(clk),",
                f"{self.indent}.rst_n(rst_n),",
                f"{self.indent}.req(eu_valid),",
                f"{self.indent}.grant(eu_ready),",
                f"{self.indent}.data_in(eu_result),",
                f"{self.indent}.data_out(rf_write_data)",
                ");",
                ""
            ])
        elif config.interconnect.topology == "mesh":
            lines.extend([
                "// Mesh Network",
                "// TODO: Implement mesh interconnect",
                ""
            ])
        else:  # noc
            lines.extend([
                "// Network-on-Chip",
                "// TODO: Implement NoC",
                ""
            ])
        
        return lines
    
    def _generate_control(self) -> List[str]:
        """Generate control logic."""
        config = self.gen.config
        
        lines = [
            "//============================================================================",
            "// Control Logic",
            "//============================================================================",
            ""
        ]
        
        if config.target == "CPU":
            lines.extend([
                "// Program Counter",
                "always_ff @(posedge clk or negedge rst_n) begin",
                "  if (!rst_n) begin",
                "    pc <= 32'h0;",
                "  end else if (instr_valid && instr_ready) begin",
                "    pc <= pc + 4;",
                "  end",
                "end",
                "",
                "// Instruction Fetch",
                "assign instr_addr = pc;",
                "assign instr_ready = !proc_busy;",
                "",
                "// Instruction Decode",
                "decoder dec (",
                f"{self.indent}.instr(instr_data),",
                f"{self.indent}.eu_sel(eu_valid),",
                f"{self.indent}.rf_read_addr(rf_read_addr),",
                f"{self.indent}.rf_write_addr(rf_write_addr),",
                f"{self.indent}.rf_write_en(rf_write_en)",
                ");",
                ""
            ])
        else:  # NPU
            lines.extend([
                "// NPU Controller",
                "// Systolic array control logic",
                "assign proc_busy = |eu_valid;",
                ""
            ])
        
        return lines
    
    def _generate_memory(self) -> List[str]:
        """Generate memory interface."""
        lines = [
            "//============================================================================",
            "// Memory Interface",
            "//============================================================================",
            ""
        ]
        
        # Register File
        lines.extend([
            "// Multi-port Register File",
            f"regfile #(",
            f"{self.indent}.NUM_READ_PORTS({self.gen.config.parallelism * 2}),",
            f"{self.indent}.NUM_WRITE_PORTS({self.gen.config.parallelism})",
            ") rf (",
            f"{self.indent}.clk(clk),",
            f"{self.indent}.rst_n(rst_n),",
            f"{self.indent}.read_addr(rf_read_addr),",
            f"{self.indent}.read_data(rf_read_data),",
            f"{self.indent}.write_addr(rf_write_addr),",
            f"{self.indent}.write_data(rf_write_data),",
            f"{self.indent}.write_en(rf_write_en)",
            ");",
            ""
        ])
        
        # LSU
        lines.extend([
            "// Load-Store Unit",
            f"lsu #(",
            f"{self.indent}.NUM_PORTS({self.gen.config.parallelism // 2})",
            ") lsu_inst (",
            f"{self.indent}.clk(clk),",
            f"{self.indent}.rst_n(rst_n),",
            f"{self.indent}.addr(data_addr),",
            f"{self.indent}.data(data),",
            f"{self.indent}.we(data_we),",
            f"{self.indent}.be(data_be),",
            f"{self.indent}.valid(data_valid),",
            f"{self.indent}.ready(data_ready)",
            ");",
            ""
        ])
        
        return lines
    
    def _get_latency(self, op: str) -> int:
        """Get operator latency."""
        latencies = {
            "ALU": 1,
            "MUL": 3,
            "FPU": 4,
            "MAC": 1,
            "BRU": 1,
            "LSU": 2
        }
        return latencies.get(op, 1)


class RTLTemplate:
    """Provides RTL code templates."""
    
    @staticmethod
    def execution_unit() -> str:
        return textwrap.dedent("""\
            module execution_unit #(
                parameter OP_TYPE = "ALU",
                parameter LATENCY = 1
            ) (
                input  wire        clk,
                input  wire        rst_n,
                input  wire        valid,
                output wire        ready,
                input  wire [63:0] operand_a,
                input  wire [63:0] operand_b,
                output wire [63:0] result
            );
                // Execution unit implementation
                // TODO: Add specific operation logic
                
                assign ready = valid;  // Simplified
                assign result = operand_a + operand_b;  // Default: ADD
                
            endmodule
        """)
    
    @staticmethod
    def regfile() -> str:
        return textwrap.dedent("""\
            module regfile #(
                parameter NUM_READ_PORTS = 8,
                parameter NUM_WRITE_PORTS = 4
            ) (
                input  wire                      clk,
                input  wire                      rst_n,
                input  wire [NUM_READ_PORTS*5-1:0]  read_addr,
                output wire [NUM_READ_PORTS*64-1:0] read_data,
                input  wire [NUM_WRITE_PORTS*5-1:0] write_addr,
                input  wire [NUM_WRITE_PORTS*64-1:0] write_data,
                input  wire [NUM_WRITE_PORTS-1:0]   write_en
            );
                reg [63:0] registers [0:31];
                
                // Read logic
                genvar i;
                generate
                    for (i = 0; i < NUM_READ_PORTS; i = i + 1) begin: read_port
                        assign read_data[i*64+:64] = registers[read_addr[i*5+:5]];
                    end
                endgenerate
                
                // Write logic
                integer j;
                always @(posedge clk) begin
                    for (j = 0; j < NUM_WRITE_PORTS; j = j + 1) begin
                        if (write_en[j]) begin
                            registers[write_addr[j*5+:5]] <= write_data[j*64+:64];
                        end
                    end
                end
                
            endmodule
        """)
    
    @staticmethod
    def crossbar() -> str:
        return textwrap.dedent("""\
            module crossbar #(
                parameter N = 4,
                parameter ARB_POLICY = "LRU"
            ) (
                input  wire        clk,
                input  wire        rst_n,
                input  wire [N-1:0]   req,
                output reg  [N-1:0]   grant,
                input  wire [N*64-1:0] data_in,
                output reg  [N*64-1:0] data_out
            );
                // Arbitration logic
                // TODO: Implement LRU/priority/round-robin
                
                always @(*) begin
                    grant = req;  // Simplified: grant all
                    data_out = data_in;
                end
                
            endmodule
        """)
    
    @staticmethod
    def lsu() -> str:
        return textwrap.dedent("""\
            module lsu #(
                parameter NUM_PORTS = 2
            ) (
                input  wire        clk,
                input  wire        rst_n,
                output reg  [31:0] addr,
                inout  wire [63:0] data,
                output reg         we,
                output reg  [7:0]  be,
                output reg         valid,
                input  wire        ready
            );
                // Load-store unit implementation
                // TODO: Add address generation and data alignment
                
            endmodule
        """)
