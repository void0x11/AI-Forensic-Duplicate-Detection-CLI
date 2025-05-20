# **AI-Enhanced Forensic Duplicate Detection CLI**

> **A cutting-edge CLI tool leveraging AI for efficient duplicate and near-duplicate file detection, designed for digital forensics and data integrity management.**

![License](https://img.shields.io/badge/License-All%20Rights%20Reserved-red)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Cross--Platform-green)

---

## **✨ Features**

* 🚀 **Exact Hash Matching**: Supports MD5, SHA-1, and SHA-256 algorithms.
* 🤖 **AI-Driven Analysis**: Detect near-duplicate files using advanced AI models (CLIP, ResNet, SBERT, etc).
* 🛠 **User-Friendly CLI**: Designed with simplicity and efficiency for forensic experts.
* 📊 **Snapshot-Based Tracking**: Automatically compares folders over time using deep AI hashes.
* 🔐 **Data Integrity Focused**: Ensures the accuracy and security of file comparisons.

---

## **📹 Demo Screenshots**

### 🔧 CLI Bootup Process

Tool starts by loading core forensic modules and initializing AI models:
![Boot Process](/src/img/dupli-hq-booting.png)

### 🛰 Main CLI Environment

ASCII-art welcome message with command shell (Dupli-HQ):
![CLI Banner](/src/img/dupli-hq-cli.png)

### 🧭 Mode Interaction + Tool Switching

Switch between modes like `duplicates`, `snapshot`, `scan` via interactive shell:
![Mode Set Example](/src/img/dupli-hq-interaction.png)

---

## **📵 Installation**

Clone this repository and install dependencies:

```bash
git clone https://github.com/void0x11/AI-Forensic-Duplicate-Detection-CLI
cd AI-Forensic-Duplicate-Detection-CLI
```

Create virtual environment:

```bash
python3 -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 📂 Project Structure

```bash
AI-FORENSIC-DUPLICATE-DETECTION-CLI/
├── ai_model/                    # AI model wrappers (CLIP, ResNet, SBERT, etc.)
│   ├── clip_model.py
│   ├── codebert_model.py
│   ├── dinov2_model.py
│   └── ...
│
├── cli_tool/
│   ├── automation/             # Automation tools (snapshots, tracking)
│   │   ├── daily_snapshot.py
│   │   ├── folder_tracker.py
│   │   └── scan_duplicates.py
│   │
│   ├── hashing/                # Hash-based utilities
│   │   ├── hash_utils.py
│   │   └── perceptual_hash.py
│   │
│   └── interface/              # CLI interaction logic
│       ├── commands.py
│       ├── cli_shell.py
│       ├── ascii_art.py
│       └── logger.py
│
├── modules-loader/             # Model/dynamic module loader
│   └── loader.py
│
├── reports/                    # Output reports
│   ├── snapshots/
│   ├── scan/
│   └── diffs/
│
├── testing/                    # Unit tests
│   ├── test_resnet18_model.py
│   ├── test_sbert_deep_model.py
│   └── ...
│
├── LICENSE
├── README.md
└── requirements.txt
```

---

## ⚖️ Usage

Launch the CLI shell:

```bash
python src/cli_tool/interface/cli_shell.py
```

Set mode:

```bash
set mode snapshot       # Take snapshot of folder state
set mode duplicates     # Find duplicate and near-duplicate files
```

Run mode:

```bash
run /path/to/folder
```

> Output is saved under the `reports/` directory.

### 🔍 Available Modes in V1

* **snapshot** – Performs a one-time scan of the selected folder, creating a saved AI-based representation.
* **duplicates** – Compares all files in the folder using AI and hash-based similarity to detect duplicates and near-duplicates.
* **scan** *(WIP)* – Reserved for future full-system recursive scans with advanced automation.

---

## ✅ Current Status

* [x] Snapshot engine (folder-based, AI embedded)
* [x] Exact hash comparison (MD5, SHA-1, SHA-256)
* [x] Near-duplicate detection using CLIP, ResNet, SBERT

> **Note:** Divergent OS file tracker is not implemented by design.

---

## 📄 License

**All Rights Reserved.** &#x20;
No part of this repository may be reproduced, distributed, or transmitted without prior written permission. See `LICENSE` for more info.