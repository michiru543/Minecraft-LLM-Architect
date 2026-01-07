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
   git clone [https://github.com/YourUsername/Minecraft-LLM-Architect.git](https://github.com/YourUsername/Minecraft-LLM-Architect.git)
   cd Minecraft-LLM-Architect
