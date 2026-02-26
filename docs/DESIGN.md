# ClawFlowGen 设计文档

## 1. 系统架构设计

### 1.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    ClawFlowGen Framework                      │
├─────────────────────────────────────────────────────────────┤
│  API Layer    │  ProcessorGenerator, OperatorLibrary         │
├───────────────┼──────────────────────────────────────────────┤
│  Core Layer   │  EvolutionEngine, ConfigManager              │
├───────────────┼──────────────────────────────────────────────┤
│  Phase Layer  │  Phase1_Tiling → Phase2_Interconnect         │
│               │  Phase3_Control → Phase4_Memory              │
├───────────────┼──────────────────────────────────────────────┤
│  RTL Layer    │  VerilogExporter, TimingAnalyzer             │
└───────────────┴──────────────────────────────────────────────┘
```

### 1.2 核心组件设计

#### 1.2.1 ProcessorGenerator (核心生成器)

```python
class ProcessorGenerator:
    """
    主生成器类，协调四阶段演化过程
    
    Attributes:
        target_type (str): "CPU" 或 "NPU"
        parallelism (int): 并行度 P
        isa (str): 指令集架构
        config (dict): 详细配置参数
        
    Methods:
        evolve(): 执行完整演化流程
        export(filename): 导出 Verilog RTL
        validate(): 验证设计约束
    """
```

#### 1.2.2 四阶段演化引擎

**阶段 1: PhysicalTiler (物理平铺)**
- 输入: 算子类型列表、并行度 P
- 输出: 平铺的运算单元池 (EU Pool)
- 关键算法: 网格布局、时钟门控插入

**阶段 2: InterconnectGenerator (互连生成)**
- 输入: EU Pool、目标频率
- 输出: 互联网络 (Crossbar/Mesh/NoC)
- 关键算法: 拓扑选择、冲突仲裁、时序优化

**阶段 3: ControlSynthesizer (控制合成)**
- 输入: ISA 定义、目标类型
- 输出: 控制逻辑 (Decoder/Scheduler)
- 关键算法: 译码表生成、调度策略

**阶段 4: MemoryIntegrator (存储集成)**
- 输入: 存储需求、带宽要求
- 输出: 存储层次 (LSU/Cache/DRAM)
- 关键算法: MSHR 计算、一致性协议

### 1.3 数据流设计

```
┌──────────────┐
│   User API   │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│  Config Parser   │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────┐
│      Evolution Orchestrator       │
│  ┌─────┐┌─────┐┌─────┐┌─────┐  │
│  │ P1  │→│ P2  │→│ P3  │→│ P4  │  │
│  │Tile ││Conn ││Ctrl ││Mem  │  │
│  └─────┘└─────┘└─────┘└─────┘  │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────┐
│  RTL Exporter    │
│  (Verilog-2001)  │
└──────────────────┘
```

## 2. 详细模块设计

### 2.1 算子库设计 (Operator Library)

#### 2.1.1 算子接口定义

```python
class Operator(ABC):
    """算子抽象基类"""
    
    @property
    @abstractmethod
    def latency(self) -> int:
        """算子延迟 (cycles)"""
        pass
    
    @property
    @abstractmethod
    def area(self) -> float:
        """算子面积 (μm²)"""
        pass
    
    @property
    @abstractmethod
    def power(self) -> float:
        """算子功耗 (mW)"""
        pass
    
    @abstractmethod
    def generate_rtl(self) -> str:
        """生成 RTL 代码"""
        pass
```

#### 2.1.2 标准算子实现

| 算子 | 延迟 | 面积 | 功耗 | 功能 |
|------|------|------|------|------|
| IntALU | 1 | 45.2 | 12.5 | 整数加减、逻辑运算 |
| IntMUL | 3 | 120.5 | 35.8 | 整数乘法 |
| FPAdd | 4 | 210.5 | 85.2 | 浮点加法 |
| FPMUL | 4 | 185.0 | 75.5 | 浮点乘法 |
| MAC | 1 | 185.0 | 65.5 | 乘累加 (NPU) |
| BRU | 1 | 65.0 | 22.5 | 分支单元 |
| LSU | 2 | 150.0 | 45.0 | 存取单元 |

### 2.2 互联网络设计

#### 2.2.1 拓扑选择策略

```python
def select_topology(parallelism: int, area_budget: float) -> Topology:
    """
    根据并行度和面积预算选择最优拓扑
    
    Args:
        parallelism: 并行度 P
        area_budget: 面积预算 (μm²)
        
    Returns:
        最优拓扑类型
    """
    xbar_area = parallelism ** 2 * WIRE_AREA
    
    if xbar_area < area_budget * 0.3:
        return CrossbarTopology()
    elif parallelism <= 16:
        return MeshTopology(dim=4)
    else:
        return NoCTopology(routing='XY')
```

#### 2.2.2 仲裁器设计

**LRU 仲裁器**: 
- 最近最少使用策略
- 适用于公平性要求高的场景
- 硬件实现: 计数器矩阵

**优先级仲裁器**:
- 固定优先级
- 适用于实时性要求高的场景
- 硬件实现: 优先级编码器

**轮询仲裁器**:
- 循环优先级
- 适用于负载均衡场景
- 硬件实现: 环形计数器

### 2.3 控制逻辑设计

#### 2.3.1 CPU 控制流

```
Fetch (8-wide) → Decode → Rename → Dispatch → 
Issue Window → Execute (8 EU) → Writeback → Commit
```

**关键组件**:
- **Branch Predictor**: TAGE-SC-L 预测器
- **ROB**: 32-entry 重排序缓存
- **Issue Queue**: 16-entry 发射队列
- **RegFile**: 16R/8W 多端口寄存器堆

#### 2.3.2 NPU 控制流

```
Command Queue → DMA Controller → 
Systolic Array (16×16) → Accumulator → Writeback
```

**关键组件**:
- **Weight Stationary**: 权重驻留数据流
- **Static Scheduler**: 编译时确定调度
- **Accumulator**: 32-bit 累加器阵列

### 2.4 存储层次设计

#### 2.4.1 缓存配置公式

```python
def calculate_cache_config(parallelism: int) -> CacheConfig:
    """计算最优缓存配置"""
    
    # MSHR 数量计算
    mem_latency = 100  # cycles
    bandwidth = parallelism * 16  # bytes/cycle
    line_size = 64  # bytes
    mshr_count = (mem_latency * bandwidth) // line_size
    
    return CacheConfig(
        size=f"{32}KB",
        ways=4,
        line_size=64,
        mshrs=min(mshr_count, 32),
        write_policy='writeback'
    )
```

#### 2.4.2 存储一致性

- **CPU**: MESI 协议，支持乱序内存访问
- **NPU**: 松散一致性，Scratchpad 管理

## 3. 接口设计

### 3.1 Python API

```python
from clawflowgen import ProcessorGenerator, CacheConfig

# 创建配置
gen = ProcessorGenerator(
    target="CPU",
    parallelism=8,
    isa="RISCV_RV64G",
    cache=CacheConfig(size="32KB", ways=4),
    ooo=True
)

# 执行演化
gen.evolve()

# 导出 RTL
gen.export("my_cpu.v")

# 获取统计信息
stats = gen.stats
print(f"面积: {stats['area']} μm²")
print(f"频率: {stats['frequency']} GHz")
```

### 3.2 命令行接口

```bash
# 生成 CPU
clawflowgen --target CPU --parallelism 8 --isa RISCV -o cpu.v

# 生成 NPU
clawflowgen --target NPU --parallelism 256 --systolic 16x16 -o npu.v

# 详细配置
clawflowgen --config config.yaml --verbose
```

### 3.3 配置文件格式 (YAML)

```yaml
# config.yaml
target: CPU
parallelism: 8
isa: RISCV_RV64G

operators:
  - type: ALU
    count: 4
  - type: MUL
    count: 2
  - type: FPU
    count: 2

cache:
  l1d:
    size: 32KB
    ways: 4
    mshrs: 16
  
interconnect:
  topology: crossbar
  arbitration: LRU

timing:
  target_frequency: 2.5GHz
  process_node: 7nm
```

## 4. 验证与测试策略

### 4.1 单元测试

```python
# tests/test_core.py
def test_cpu_generation():
    gen = ProcessorGenerator(target="CPU", parallelism=4)
    gen.evolve()
    assert len(gen.eu_pool) == 4
    assert gen.validate()

def test_npu_systolic_array():
    gen = ProcessorGenerator(target="NPU", parallelism=256)
    gen.evolve()
    assert gen.controller.type == "systolic"
```

### 4.2 集成测试

- **ISA 兼容性测试**: 运行 RISC-V 测试套件
- **性能回归测试**: 对比 CoreMark 分数
- **时序收敛测试**: 检查关键路径延迟

### 4.3 形式验证

- **死锁检测**: 检查互联网络死锁
- **活锁检测**: 检查仲裁器公平性
- **协议验证**: 验证缓存一致性

## 5. 性能优化策略

### 5.1 面积优化

- **算子共享**: 多功能算子复用
- **时钟门控**: 动态功耗管理
- **存储折叠**: Bank 冲突优化

### 5.2 时序优化

- **流水线平衡**: 均匀分布延迟
- **关键路径优化**: 减少逻辑级数
- **布线优化**: 减少线长

### 5.3 功耗优化

- **DVFS**: 动态电压频率调节
- **电源门控**: 空闲单元断电
- **数据门控**: 减少无效切换

## 6. 扩展性设计

### 6.1 插件架构

```python
# 自定义算子插件
class CustomOperator(Operator):
    def generate_rtl(self):
        return "// Custom RTL"

# 注册插件
OperatorLibrary.register("custom", CustomOperator)
```

### 6.2 后端支持

- **综合工具**: 支持 Genus, Design Compiler
- **布局布线**: 支持 Innovus, ICC2
- **签核工具**: 支持 Tempus, PrimeTime

## 7. 错误处理与调试

### 7.1 错误分类

| 级别 | 类型 | 处理策略 |
|------|------|---------|
| ERROR | 配置错误 | 抛出异常，终止生成 |
| ERROR | 资源冲突 | 自动仲裁，记录警告 |
| WARN | 时序违例 | 优化建议，继续生成 |
| INFO | 优化提示 | 记录日志，供参考 |

### 7.2 调试工具

```python
# 启用调试模式
gen = ProcessorGenerator(debug=True, dump_intermediate=True)
gen.evolve()

# 查看中间结果
gen.dump_phase1()  # 输出阶段1结果
gen.dump_interconnect()  # 输出互连网络
```

## 8. 部署与发布

### 8.1 PyPI 包结构

```
clawflowgen/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── generator.py
│   ├── config.py
│   └── validator.py
├── phases/
│   ├── __init__.py
│   ├── tiling.py
│   ├── interconnect.py
│   ├── control.py
│   └── memory.py
├── rtl/
│   ├── __init__.py
│   ├── exporter.py
│   └── templates/
└── utils/
    ├── __init__.py
    ├── logger.py
    └── timing.py
```

### 8.2 Docker 支持

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -e .
ENTRYPOINT ["clawflowgen"]
```

---

**联系信息**:
- 组织: @openclawdchip
- 邮箱: xiao.lin@ia.ac.cn
- 文档: https://docs.clawflowgen.ai
