---
title: "一、 综述与前瞻性论文 (Surveys and Position Papers)"
date: 2024-12-31 11:12:01 +0800
categories: [Suervey]
tags: ['algorithm']
---


### 一、 综述与前瞻性论文 (Surveys and Position Papers)

这些论文为你提供了该领域的宏观视角、核心挑战和未来趋势。

1. **《A Survey on LLM-based Multi-Agent System: Recent Advances and New Frontiers in Application》** (arXiv:2412.17481)
    
    - **摘要**: 这篇综述系统地介绍了基于LLM的多智能体系统（LLM-MAS）的定义、关键组成部分（如配置文件、记忆、规划、行动）、各类应用以及未来的研究方向。它为理解整个生态系统提供了一个全面的框架。
2. **《Meta-Thinking in Large Language Models via Multi-Agent Reinforcement Learning: A Survey》** (arXiv:2504.14520)
    
    - **摘要**: 聚焦于一个有趣的方向：如何利用MARL来激发LLM的元认知能力，即自我反思、评估和修正的能力。这对于提升LLM智能体在复杂任务中的可靠性至关重要。
3. **《Large Language Models Miss the Multi-Agent Mark》** (arXiv:2505.21298)
    
    - **摘要**: 这是一篇重要的批判性分析文章，指出了当前LLM在真正理解和应对多智能体复杂性（如协调、竞争、信号传递）方面的根本性不足，并提出了关键的研究机会。
4. **《POSITION: WHAT’S THE NEXT FRONTIER FOR DATA-CENTRIC AI? DATA SAVVY AGENTS!》** (OpenReview)
    
    - **摘要**: 这篇立场文件虽然不直接针对MARL，但它提出了未来智能体需要具备的四种核心“数据感知”能力（主动获取、复杂处理、交互式测试、持续自适应），这对于构建能在真实世界中稳定运行的MARL+LLM系统具有指导意义。

### 二、 核心框架与代表性算法 (Core Frameworks and Algorithms)

这些论文提出了具体的算法和框架，展示了LLM如何与MARL的技术栈相结合。

1. **LGC-MARL: 《Enhancing Multi-Agent Systems via Reinforcement Learning with LLM-based Planner and Graph-based Policy》** (arXiv:2503.10049)
    
    - **摘要**: 提出了一个名为LGC-MARL的框架。其核心思想是利用LLM作为高级“规划器”来分解复杂任务并生成子目标，然后一个基于图的策略网络负责执行这些子目标。LLM同时还扮演了评论家和奖励生成器的角色，展示了LLM在MARL中扮演多种角色的潜力。
2. **SEMDIV: 《LLM-Assisted Semantically Diverse Teammates Generation for Multi-Agent Coordination》**
    
    - **摘要**: 该框架利用LLM在语义层面生成多样化的协调行为描述，并将其转化为奖励函数来训练不同的“队友”策略。这使得智能体能够学会与具有不同（甚至是未见过）行为模式的队友进行高效协作，解决了零样本协调（Zero-Shot Coordination）的一大难题。
3. **Hypothetical Minds: 《Hypothetical Minds: TuM for Multi-Agent Cooperation in the eyes of LLMs》**
    
    - **摘要**: 这篇论文在游戏AI领域探索了如何利用LLM进行“心智理论”（Theory of Mind, ToM）推理。通过让LLM对其他智能体的意图和信念进行假设性推理，来提升多智能体之间的合作效率，尤其是在信息不完全的环境中。
4. **MARFT: 《MARFT: Multi-Agent Reinforcement Fine-Tuning》** (arXiv:2504.16129)
    
    - **摘要**: （根据摘要信息）该论文可能关注于如何利用强化学习来微调LLM，使其更好地适应多智能体环境中的交互和决策。这代表了将MARL的训练范式直接应用于优化LLM本身的一个方向。

### 三、 关键应用 (Key Applications)

这些论文展示了MARL+LLM在不同领域的应用潜力。

1. **自动驾驶 (Autonomous Driving):** **《Multi-Agent Autonomous Driving Systems with Large Language Models: A Survey of Recent Advances》**
    
    - **摘要**: 这篇综述详细探讨了LLM如何在多智能体自动驾驶系统中发挥作用，包括用于高级决策、风险场景理解、人车交互以及多车之间的协商与协作。
2. **推荐系统 (Recommendation Systems):** **《Envisioning Recommendations on an LLM-Based Agent Platform》** (CACM)
    
    - **摘要**: 这篇文章提出了一个名为`Rec4Agentverse`的概念框架。它设想将每个“物品”（如商品、电影）都变成一个LLM驱动的智能体，而推荐过程则变成了一个多智能体系统，由一个“代理推荐官”来协调这些物品智能体与用户进行交互，这为推荐系统开辟了全新的思路。
3. **机器人学 (Robotics):** **MARLIN: 《Multi-Agent Reinforcement Learning Guided by Language-Based Inter-Robot Negotiation》** (arXiv:2410.14383)
    
    - **摘要**: （根据摘要信息）MARLIN框架利用LLM来促进多机器人之间的语言协商。机器人可以通过自然语言进行沟通、协商任务分配和解决冲突，然后这些高级的语言指令会指导底层的MARL策略执行，从而实现更复杂和灵活的协作。

### 四、 评估与基准 (Evaluation and Benchmarks)

这类研究关注如何科学地衡量LLM在多智能体环境下的能力。

1. **《Evaluating Multi-agent Coordination Abilities in Large Language Models》** (NAACL 2025 Findings)
    - **摘要**: 该研究提出了一个专门用于评估LLM多智能体协调能力的基准测试`LLM-Coordination Benchmark`。通过在一系列合作游戏（如《Hanabi》, 《Overcooked》）中的测试，系统地揭示了当前LLM在环境理解、心智理论和联合规划方面的优势与不足。