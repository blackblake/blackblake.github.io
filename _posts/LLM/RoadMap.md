---
title: "I. 首要任务"
date: 2024-12-31 11:12:01 +0800
categories: [LLM]
tags: ['dl', 'ml', 'llm']
---


# I. 首要任务

- **主修 CS224N** 的核心章节（尤其是Transformer），确保基础牢固。
- **跟学 CS336** 的课程，建立系统性的LLM理论知识。
- 将 **Berkeley CS294** 的讲座视频和阅读列表**作为前沿追踪材料**，了解现在顶级研究者都在关心什么问题。

# II. 路线图
## 🔹 一线研究者主讲的 LLM 高质量课程（推荐优先顺序）

### 1. Stanford CS25: Transformers United

- **主讲人**：Chris Ré、Matei Zaharia、Percy Liang 等
    
- **链接**：[https://cs25.stanford.edu/](https://cs25.stanford.edu/)
    
- **特点**：讨论大型语言模型的研究趋势、系统优化、推理与部署、安全性，嘉宾阵容豪华（OpenAI, Anthropic, Meta, Google DeepMind 等）
    

---

### 2. **Stanford CS224N: NLP with Deep Learning**

- **主讲人**：Chris Manning
    
- **链接**：[CS224N官网](https://web.stanford.edu/class/cs224n/)
    
- **特点**：从基础 NLP 到 transformer，再到 pretraining，非常系统，适合打牢基础
    
- **YouTube 视频**：2023年最新版已经更新
    

---

### 3. **Berkeley CS182: Transformers and Attention**

- **主讲人**：Dan Klein
    
- **链接**：[课程主页](https://inst.eecs.berkeley.edu/~cs182/sp24/)
    
- **特点**：Transformer 结构深入讲解，Attention 理论，前期基础牢靠者可略读部分内容
    

---

### 4. **Berkeley CS294-239: Large Language Models**

- **主讲人**：Jacob Andreas（Meta）、Dan Klein、John DeNero
    
- **链接**：[课程主页](https://people.eecs.berkeley.edu/~keutzer/classes/CS294/CS294.html)
    
- **特点**：聚焦 LLM 架构、训练机制、蒸馏、调优、工具链，阅读论文密度大，**非常科研导向**
    

---

### 5. **MIT 6.S898: Advanced NLP and LLMs**

- **主讲人**：Jacob Andreas
    
- **链接**：[课程主页](http://web.mit.edu/6.s898/www/)
    
- **特点**：专注 LLM 与 NLP 的进展，如指令微调、语言对齐、LLM 内部行为分析，非常适合科研方向
    

---

### 6. **CMU 11-667: LLM Alignment**

- **主讲人**：Denny Zhou（DeepMind），Noah Smith（AI2）
    
- **链接**：一般通过 YouTube 或 GitHub 发布（可以关注 Prof. Smith 和 AI2）
    
- **特点**：关注 RLHF、对齐、指令跟随等前沿方向，适合深入探究 RLHF 原理
    

---

## 🔸 系统性入门路线（如果你还没完全掌握 LLM 所需的基本理论）

### 👉 推荐自学路径：

| 阶段                | 推荐内容                                                                                                                                     |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| 1. 深度学习基础         | 吴恩达深度学习课程（Coursera）、Fast.ai 深度学习课程                                                                                                       |
| 2. NLP 基础         | Stanford CS224n                                                                                                                          |
| 3. Transformer 原理 | Illustrated Transformer（[链接](http://jalammar.github.io/illustrated-transformer/)）+ Annotated GPT (Andrej Karpathy 的 GitHub)              |
| 4. LLM 原理         | LLM.int8（[https://llm.int8.dev](https://llm.int8.dev/)），还有 Karpathy 的 [Zero to Hero LLM 视频](https://www.youtube.com/watch?v=zjkBMFhNj_g) |
| 5. 论文导读           | arXiv LLM Survey（《A Survey of Large Language Models》）或 ChatGPT 启动论文、GPT-4 技术报告等                                                          |
| 6. 微调和部署          | HuggingFace Transformers & PEFT 教程、ColossalAI、DeepSpeed、LoRA 教程                                                                          |
| 7. 对齐 / RLHF      | OpenAI InstructGPT 论文、Anthropic Constitutional AI 论文、Stanford Alpaca 复现过程等                                                               |

---

## 📚 推荐书籍

- 《自然语言处理综论》（Speech and Language Processing，第三版草稿）——Jurafsky & Martin
    
- 《Deep Learning for Coders with fastai and PyTorch》——适合用代码理解 Transformer
    
- 《Transformers for Natural Language Processing》by Denis Rothman
    

---

## 🎓 想读 PhD 或深度科研？你还需要关注这些：

- **LMSYS ([https://lmsys.org)**：LLM](https://lmsys.org\)%2A%2A:llm/) Benchmark 研究（Vicuna 作者团队）
    
- **HuggingFace Course**：轻量但务实，微调和部署的绝佳起点
    
- **Open LLM Leaderboard**：看社区开源模型进展
    
- **ArXiv Sanity (Karpathy)**：跟踪最新论文
    



# III. LLM 研究者成长学习计划**

## 🧠 总体思路

分为四大阶段（每个阶段建议持续 3~6 周）：

1. **基础夯实（构建Transformer/NLP/LLM底层原理认知）**
    
2. **深入理解LLM系统结构（架构、训练、推理）**
    
3. **专项深入（对齐、微调、安全性、多模态等方向选学）**
    
4. **科研产出与写作（论文复现、项目设计、投顶会）**
    

---

## 📆 学习计划概览（3~6个月）

|时间|阶段|内容概览|主要任务|
|---|---|---|---|
|第1~3周|基础夯实|NLP、Transformer、预训练|CS224n 精读 + Transformer from scratch|
|第4~6周|深入LLM|GPT/BERT/T5 架构 + Tokenizer + 预训练技巧|Annotated GPT2/BERT、理解 loss、mask|
|第7~9周|LLM训练|数据构建、预训练过程、RLHF、LoRA|Stanford Alpaca、RLHF 模型复现|
|第10~13周|工具链熟练|HuggingFace、PEFT、Deepspeed、Weights&Biases|自己训练/微调一个小模型|
|第14~17周|研究选题|Alignment / Prompt Engineering / Retrieval / Efficiency|阅读10篇顶会论文，设计实验|
|第18~24周|科研写作|实验跑通 + 论文撰写|跟踪 ACL/NeurIPS/ICLR 投稿节奏|



## 🧩 每阶段详细内容

---

### 🔹 阶段 1：基础夯实（第1~3周）

> 目标：掌握 LLM 所依赖的 Transformer + NLP 基础

#### 推荐课程 & 资料

- ✅ **Stanford CS224n（前6讲）**
    
- ✅ **The Illustrated Transformer**：[Jalammar博客](http://jalammar.github.io/illustrated-transformer/)
    
- ✅ Andrej Karpathy 的 [GPT from scratch](https://www.youtube.com/watch?v=kCc8FmEb1nY)
    

#### 任务清单：

-  理解 Self-Attention、Position Embedding、Multi-Head
    
-  掌握 Masked LM vs Causal LM 训练机制
    
-  用 PyTorch 复现最小 GPT
    

---

### 🔹 阶段 2：深入LLM结构（第4~6周）

> 目标：读懂 GPT/BERT/T5 论文，掌握 tokenizer、训练 pipeline

#### 推荐资源

- ✅ GPT 原论文（GPT-1、2、3）、BERT、T5
    
- ✅ HuggingFace Tokenizer 教程（含 Byte Pair Encoding）
    
- ✅ Annotated Transformer/GPT2/BERT（[Harvard NLP](https://nlp.seas.harvard.edu/2018/04/03/attention.html)）
    

#### 任务清单：

-  用 Transformers 库调用 GPT2 和 BERT
    
-  理解每个模型的输入输出格式、训练目标
    
-  尝试 tokenizer + 数据构建
    

---

### 🔹 阶段 3：LLM训练与调优（第7~13周）

> 目标：掌握 LLM 的微调、对齐、蒸馏、PEFT 等技术

#### 推荐实战教程

- ✅ Stanford Alpaca 或 HuggingFace 微调教程
    
- ✅ PEFT: LoRA, QLoRA 教程（[HuggingFace PEFT库](https://github.com/huggingface/peft)）
    
- ✅ DeepSpeed/ColossalAI/LLM.int8.dev 实践教程
    

#### 核心知识：

-  RLHF（阅读 InstructGPT 和 OpenAI 技术报告）
    
-  Prompt Tuning / LoRA / QLoRA
    
-  训练技巧（混合精度、梯度裁剪、EMA、RMSNorm）
    

#### 实践任务：

-  在开源数据集上微调一版 GPT 模型（alpaca、dolly、openchat）
    
-  尝试训练和部署一个轻量模型（如 tinyGPT、Phi）
    

---

### 🔹 阶段 4：科研选题与产出（第14~24周）

> 目标：准备可投稿的实验 / demo / 开源项目

#### 研究方向建议（任选 1~2）

|方向|推荐论文 / 项目|
|---|---|
|对齐 & 安全|RLHF、Constitutional AI、OpenAI GPTs|
|Prompt / In-Context|RAG、Toolformer、MetaICL|
|高效训练|LoRA、QLoRA、MoE、SFT/IFT|
|多模态 LLM|Flamingo, LLaVA, GPT-4V|
|开源模型追踪|Mistral, Zephyr, Phi, Yi 等|

#### 工具推荐：

- 🔧 Weights & Biases：训练可视化
    
- 🔧 HuggingFace Hub：发布和分享模型
    
- 🔧 Docker + Gradio：部署你的 LLM demo
    

---

## 📚 附录：你可以持续追踪的资源

- **ArXiv LLM专栏**：[https://arxiv.org/list/cs.CL/recent](https://arxiv.org/list/cs.CL/recent)
    
- **Papers with Code LLM板块**：[https://paperswithcode.com](https://paperswithcode.com/)
    
- **LMSYS Leaderboard**：跟踪最强开源模型：[https://lmsys.org/](https://lmsys.org/)