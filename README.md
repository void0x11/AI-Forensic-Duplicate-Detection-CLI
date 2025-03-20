# **AI-Enhanced Forensic Duplicate Detection CLI**

> **A cutting-edge CLI tool leveraging AI for efficient duplicate and near-duplicate file detection, designed for digital forensics and data integrity management.**

![License](https://img.shields.io/badge/License-All%20Rights%20Reserved-red) 
![Python](https://img.shields.io/badge/Python-3.9%2B-blue) 
![Platform](https://img.shields.io/badge/Platform-Cross--Platform-green)

---

## **✨ Features**
- 🚀 **Exact Hash Matching**: Supports MD5, SHA-1, and SHA-256 algorithms.
- 🤖 **AI-Driven Analysis**: Detect near-duplicate files using advanced AI models.
- 🛠 **User-Friendly CLI**: Designed with simplicity and efficiency for forensic experts.
- 📊 **Performance Metrics**: Real-time results with detailed analysis.
- 🔐 **Data Integrity Focused**: Ensures the accuracy and security of file comparisons.

---

## **📽 Demo**

> **Coming Soon!**

---

## **📥 Installation**

Clone this repository and install dependencies:

```bash
git clone https://github.com/void0x11/AI-Forensic-Duplicate-Detection-CLI
cd AI-Forensic-Duplicate-Detection-CLI
```

Install on Linux:
```bash
pip install -r requirements.txt
```

Install on Windows:
```powershell
python -m pip install -r requirements.txt
```

## 📂 Project Structure
```bash
project/
├── ai_model/
│   ├── model.py                # AI model for file grouping
│   ├── train_model.py          # Trains the AI model
│   ├── data/                   # Stores training data
│   │   ├── file_patterns.csv   # Example file movement patterns
│
├── cli_tool/
│   ├── hashing/
│   │   ├── hash_utils.py       # Exact hashing (MD5, SHA-1, SHA-256)
│   │   ├── perceptual_hash.py  # AI-based near-duplicate detection
│
│   ├── processing/
│   │   ├── duplicate_finder.py # Calls hashing functions & AI model
│   │   ├── file_handler.py     # Manages file operations
│   │   ├── file_search.py      # AI-driven search function (NEW)
│
│   ├── interface/
│   │   ├── main.py             # CLI entry point
│   │   ├── commands.py         # Command-line functionalities
│
├── database/
│   ├── db_handler.py           # Handles saving/loading hash results
│
├── logs/
│   ├── log_handler.py          # Manages logging
│
├── reports/
│   ├── report_generator.py     # Generates reports from scan results
│
LICENSE
README.md
requirements.txt
```

## 📜 License
All Rights Reserved.
No part of this repository may be reproduced, distributed, or transmitted in any form without prior written permission. See the LICENSE file for more details.