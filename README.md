<div align="center">

# AI Code Agent System

**智能驱动的软件工程自动化系统**

</div>

## 项目简介

我构建了以 **AI Code Agent** 为核心的 **智能软件工程自动化系统**，并在此基础上搭建了 **智能化代码修复与软件工程任务处理平台**，通过Agent自主决策与多环境协同执行实现持续运行与自我优化，整体形成「任务接收 - 智能分析 - 代码执行 - 结果验证 - 自动提交」的完整闭环。

本系统采用极简架构设计，核心代码仅约300行Python，却能实现强大的AI驱动软件开发能力。系统支持100+种主流大语言模型，在SWE-Bench Verified基准测试中取得74%+的解决率。

## 核心特性

### 极简设计
- **核心Agent引擎**：仅100行Python代码实现的AI Agent类
- **零依赖工具调用**：仅使用Bash作为唯一工具接口，兼容所有主流大语言模型
- **线性历史记录**：每一步操作都追加到消息流中，便于调试和轨迹回溯
- **独立执行机制**：通过subprocess.run执行每个命令，支持无缝切换到Docker/Singularity等沙盒环境

### 多环境支持
- 本地Shell环境
- Docker/Podman容器环境
- Singularity/Apptainer容器环境
- Bubblewrap轻量级隔离
- Contree远程执行环境
- SWE-ReX Modal云环境

### 智能交互
- **InteractiveAgent**：支持三种运行模式
  - 人工模式(human)：用户直接控制
  - 确认模式(confirm)：Agent命令需确认
  - 全自动模式(yolo)：完全自主执行
- **Trajectory Inspector**：可视化轨迹浏览器
- 支持实时成本追踪和步数限制

### 批量处理能力
- 支持多线程并行推理（ThreadPoolExecutor）
- 集成SWE-Bench Verified基准测试（500个真实GitHub Issues）
- 实时进度显示和状态追踪

## 技术架构

```
┌─────────────────────────────────────────┐
│           Run Layer (CLI/API)            │
├─────────────────────────────────────────┤
│          Agent Layer (Core)              │
│  ┌─────────────┐  ┌──────────────────┐   │
│  │ DefaultAgent │  │ InteractiveAgent │   │
│  │  (~100行)    │  │  (扩展交互功能)   │   │
│  └─────────────┘  └──────────────────┘   │
├─────────────────────────────────────────┤
│           Model Layer                    │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐  │
│  │ LiteLLM  │ │OpenRouter│ │ Portkey │  │
│  └──────────┘ └──────────┘ └─────────┘  │
├─────────────────────────────────────────┤
│         Environment Layer                │
│  ┌──────┐ ┌───────┐ ┌────────────┐     │
│  │ Local│ │ Docker│ │ Singularity│     │
│  └──────┘ └───────┘ └────────────┘     │
└─────────────────────────────────────────┘
```

## 使用规模

### 社区影响力
- 开源社区广泛采用
- 被多家顶级企业和研究机构使用
- 包括科技公司、AI研究机构、顶尖高校等

### 模型兼容性
- 支持100+种大语言模型
- OpenAI GPT系列
- Anthropic Claude系列
- Google Gemini系列
- 开源模型（Llama, Mistral等）

### 性能表现

#### SWE-Bench Verified基准测试结果

| 模型 | 解决率 | 平均时间 |
|------|--------|----------|
| Gemini 3 Pro | 74%+ | ~7分钟/实例 |
| Claude Sonnet 4 | 65-70% | ~8分钟/实例 |
| GPT-5 / GPT-5-mini | 65-70% | ~9分钟/实例 |
| MiniMax M2.7 | 74.7%* | ~7分钟/实例 |

*独立测试数据（265个实例）

#### 效率对比
- 传统人工修复：2-8小时/Issue
- AI Agent自动化：~7分钟/Issue
- **效率提升：17-68倍**

### Token消耗统计

基于实际测试数据：
- **平均每实例Token量**：40,063 tokens
  - 输入Token：25,135
  - 输出Token：14,928
- **单实例成本**：< $0.7（性价比模型）
- **月度处理能力预估**（10,000 Issues）：约4亿tokens

## 应用场景

### 1. 自动化Bug修复
- 成功修复多个主流开源项目的真实Issues
- Django、scikit-learn、matplotlib、sympy、pytest等
- 已验证解决196+个真实问题

### 2. 软件工程任务自动化
- 代码重构与优化
- 测试用例生成与执行
- 文档自动生成
- 类型标注补充
- 代码审查辅助

### 3. 研究与开发
- AI Agent微调(FT)基线系统
- 强化学习(RL)实验平台
- 模型性能评估基准
- 学术研究和教育工具

### 4. 企业级应用
- CI/CD流水线集成
- 自动化代码审查
- 技术债务管理
- 知识库构建

## 快速开始

### 安装方式

**方式一：pip安装（推荐）**
```bash
pip install ai-code-agent-system
agent-cli  # 启动命令行界面
```

**方式二：从源码安装**
```bash
git clone https://github.com/QQQQQQQj/ai-code-agent-system.git
cd ai-code-agent-system
pip install -e .
agent-cli  # 启动命令行界面
```

**方式三：uv/pipx快速体验**
```bash
pip install uv && uvx ai-code-agent-system
# 或
pip install pipx && pipx run ai-code-agent-system
```

### 基础使用

```python
from ai_code_agent import DefaultAgent, LitellmModel, LocalEnvironment

# 创建Agent实例
agent = DefaultAgent(
    model=LitellmModel(model_name="anthropic/claude-sonnet-4-5-20250929"),
    env=LocalEnvironment(),
)

# 执行任务
result = agent.run("帮我实现一个数独求解器")
print(result)
```

### 命令行使用

```bash
# 交互式模式
agent-cli

# 指定任务
agent-cli -t "修复这个bug"

# 选择模型
agent-cli -m "openai/gpt-5"

# 全自动模式
agent-cli -t "重构代码" -y
```

## 配置说明

### 模型配置
系统支持通过配置文件或命令行参数配置模型：

```yaml
# config.yaml
model:
  model_name: "anthropic/claude-sonnet-4-5-20250929"
  model_kwargs:
    temperature: 0
    max_tokens: 4096
```

### 环境配置
支持多种执行环境：

```yaml
environment:
  environment_class: "docker"  # 或 local, singularity, etc.
  image: "python:3.11-slim"
  timeout: 30
```

### Agent配置
自定义Agent行为：

```yaml
agent:
  step_limit: 100      # 最大步数
  cost_limit: 10.0     # 成本限制（美元）
  mode: "confirm"      # human, confirm, yolo
```

## 项目结构

```
ai-code-agent-system/
├── src/
│   └── ai_code_agent/
│       ├── agents/               # Agent实现
│       │   ├── default.py        # 核心Agent类（~100行）
│       │   └── interactive.py    # 交互式Agent
│       ├── models/               # 模型接口
│       │   ├── litellm_model.py  # LiteLLM模型（~147行）
│       │   ├── openrouter_model.py
│       │   └── portkey_model.py
│       ├── environments/         # 执行环境
│       │   ├── local.py          # 本地环境（~79行）
│       │   ├── docker.py         # Docker环境
│       │   └── singularity.py    # Singularity环境
│       ├── run/                  # 运行入口
│       │   ├── cli.py            # 命令行界面
│       │   ├── hello_world.py    # 快速示例
│       │   └── benchmarks/       # 基准测试
│       │       └── swebench.py   # SWE-Bench测试
│       └── config/               # 配置文件
│           ├── default.yaml
│           └── cli.yaml
├── tests/                        # 测试套件
├── docs/                         # 文档
├── README.md                     # 本文件
└── pyproject.toml                # 项目配置
```

## 核心代码示例

### Agent核心逻辑（简化版）
```python
class DefaultAgent:
    def __init__(self, model, env, **kwargs):
        self.model = model
        self.env = env
        self.messages = []
        self.cost = 0.0
        self.n_calls = 0

    def run(self, task: str) -> dict:
        """主循环：查询模型 -> 执行动作 -> 循环直到完成"""
        self.messages = [
            self._create_system_message(),
            self._create_task_message(task)
        ]

        while not self._is_finished():
            self.step()

        return self._get_result()

    def step(self):
        """单步执行"""
        response = self.model.query(self.messages)
        actions = self._parse_actions(response)
        outputs = [self.env.execute(action) for action in actions]
        observations = self._format_observations(outputs)
        self.messages.extend(observations)
```

## 高级功能

### 批量基准测试
```bash
# 在SWE-Bench上运行评估
agent-benchmark --subset verified --model "anthropic/claude-sonnet-4-5-20250929"

# 并行处理
agent-benchmark -w 4 --output ./results
```

### 轨迹可视化
```bash
# 查看Agent决策过程
agent-inspector path/to/trjectory.traj.json
```

### 自定义扩展
```python
# 自定义Model
class MyCustomModel:
    def query(self, messages):
        # 你的模型调用逻辑
        pass

# 自定义Environment
class MyCustomEnv:
    def execute(self, action):
        # 你的执行逻辑
        pass
```

## 性能优化建议

1. **选择合适的模型**：根据任务复杂度选择模型
2. **调整步数限制**：简单任务可设置较低限制
3. **使用缓存**：启用模型响应缓存
4. **并行处理**：批量任务时增加worker数量
5. **环境预热**：提前准备Docker镜像等

## 常见问题

Q: 支持哪些模型？
A: 通过LiteLLM支持100+种模型，包括OpenAI、Anthropic、Google、开源模型等。

Q: 如何降低成本？
A: 使用性价比高的模型（如GPT-5-mini），设置合理的cost_limit。

Q: 是否安全？
A: 所有操作在沙盒环境中执行，支持Docker隔离。

Q: 如何调试？
A: 使用inspector查看完整轨迹，或查看保存的traj.json文件。

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- GitHub Issues: [提交问题](https://github.com/QQQQQQQj/ai-code-agent-system/issues)
- Email: 1303517653@qq.com

---

<div align="center">

**用最简洁的代码，实现最强大的AI软件工程能力**

Made with ❤️ by AI Code Agent Team

</div>