# LLM-Based Procedural Building Generator for Minecraft

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![LLM](https://img.shields.io/badge/Model-Gemini%202.5%20Pro-orange)](https://deepmind.google/technologies/gemini/)
[![Minecraft](https://img.shields.io/badge/Minecraft-Java%20Edition-green)](https://www.minecraft.net/)

**[日本語の説明は下にあります (Japanese Description Below)](#-概要)**

## 📖 Overview
This project introduces a novel system for procedurally generating detailed buildings in **Minecraft** using Large Language Models (LLMs). Unlike traditional methods that focus only on exterior shells, this system generates **fully furnished interiors, logical room layouts, and functional connections** (doors/passages).

Powered by **Google Gemini 2.5 Pro** and **LangChain**, the generation process is divided into 7 distinct steps to ensure structural consistency and spatial reasoning.

### Key Features
- **7-Step Generation Pipeline**: Decomposes the complex architecture task into Style, Modules, Furniture, Layout, Connections, Integration, and Code Generation.
- **Interior & Layout Focus**: Generates playable interiors with furniture appropriate for each room's function.
- **Spatial Reasoning**: Uses a coordinate-based logic to determine room adjacencies and door placements.
- **Parallel Processing**: Utilizes threading to generate furniture and layouts simultaneously for efficiency.
- **Automated Construction**: Converts the generated plan into Python code using the **GDPC (Generative Design in Minecraft)** library to build directly in the game.

## 🛠️ Requirements
- **Python 3.11+**
- **Minecraft Java Edition** (Supported versions by GDPC, e.g., 1.19, 1.20)
- **GDPC HTTP Interface Mod** (running on a local Minecraft server or single-player world)
- **Google Gemini API Key**

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YourUsername/Minecraft-LLM-Architect.git
   cd Minecraft-LLM-Architect
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Environment**
   - **Important**: Do not hardcode your API Key.
   - Set your Gemini API key in an environment variable or create a `.env` file (if implemented).

## 🚀 Usage

1. Open Minecraft and ensure the GDPC mod is active.
2. Run the main script:
   ```bash
   python main.py
   ```
3. Follow the CLI prompts:
   - Enter a description (e.g., *"A luxurious Victorian mansion"*).
   - (Optional) Upload a reference image path.
4. The system will process the steps and build the structure near the player.

## 🏗️ System Architecture (The 7 Steps)

The system utilizes a **Chain-of-Thought** approach implemented via LangChain:

1.  **Style Design**: Defines the architectural style and materials based on user input.
2.  **Module Definition**: Lists necessary rooms (e.g., Living Room, Kitchen).
3.  **Furniture Design**: Plans furniture for each room (Parallelized).
4.  **Layout Design**: Determines the 2D/3D arrangement of rooms (Parallelized).
5.  **Connection Logic**: Calculates door positions and connectivity between adjacent modules.
6.  **JSON Integration**: Compiles all data into a structured JSON format.
7.  **Code Generation**: Generates executable Python code (GDPC) to place blocks.

## 📂 Project Structure

```text
.
├── chains/                 # Logic for each generation step (LangChain models)
│   ├── model_style.py      # Step 1
│   ├── model_modules.py    # Step 2
│   ├── ...                 # Steps 3-7
├── utils/                  # Utility functions (File I/O, Logging)
├── materials/              # Material definitions (materials.txt)
├── generated/              # Output logs and generated code
├── main.py                 # Main entry point
└── README.md
```

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

# 🇯🇵 概要

本プロジェクトは、大規模言語モデル（LLM）を用いて、**マインクラフト**内で内装付きの建築物を自動生成するシステムです。
従来の手法では困難だった「部屋の機能に基づいた家具配置」や「論理的な間取り（レイアウト）」の生成を実現しています。

**Google Gemini 2.5 Pro** と **LangChain** を活用し、生成プロセスを7つのステップに分割することで、複雑な建築タスクを高い整合性で実行します。

### 主な特徴
- **7段階の生成パイプライン**: スタイル決定、部屋定義、家具配置、レイアウト、接続推論、統合、コード生成にタスクを分割。
- **内装とレイアウトの重視**: 外観だけでなく、居住可能な内装と動線を生成。
- **並列処理**: 家具生成とレイアウト生成を並列化し、処理時間を短縮。
- **自動建築**: **GDPC** ライブラリを介して、生成されたPythonコードを即座にゲーム内に反映。

## 動作環境
- Python 3.11以上
- Minecraft Java Edition
- GDPC (Generative Design in Minecraft) 環境
- Google Gemini API Key

## 使い方

1. マインクラフトを起動し、GDPC導入済みのワールドに入ります。
2. `main.py` を実行します。
3. プロンプト（建築物の説明）を入力します（例: *"A modern house with glass walls"*）。
4. システムが推論を行い、プレイヤーの近くに建築物が自動生成されます。

## 開発者
- **Affiliation**: College of Information Science and Engineering, Ritsumeikan University
