# Contributing to J.A.R.V.I.S.

Thank you for your interest in contributing to J.A.R.V.I.S.! This project is built for developers who want a local, private, and highly extensible voice assistant on their desktops.

---

## Code of Conduct

By participating in this project, you agree to abide by standard open-source community guidelines:
- Be respectful and professional.
- Focus on constructive criticism.
- Protect personal/sensitive details in logs and issues.

---

## How Can I Contribute?

### 1. Reporting Bugs
- Search existing issues to verify the bug has not been reported.
- Open a new issue using the **Bug Report** template.
- Provide a clear description, reproduction steps, and system logs (`jarvis.log`).

### 2. Suggesting Features
- Open an issue using the **Feature Request** template.
- Explain the user benefit, proposed voice command keywords, and implementation idea.

### 3. Submitting Pull Requests
- Fork the repository and create a new branch from `main` or `development`.
- Align your code with PEP 8 coding standards.
- Ensure all imports are portable across Windows, Linux, and macOS.
- Centralize all configurable settings in `config.py` using `.env` environment variables.
- Update `commands.txt` and `README.md` if your PR introduces new voice command triggers.

---

## Local Development Setup

1. Fork and clone the repository.
2. Initialize a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create your `.env` file from `.env.example`:
   ```bash
   cp .env.example .env
   ```
5. Run the neural voice download script:
   ```bash
   python download_jarvis_voice.py
   ```
6. Launch J.A.R.V.I.S.:
   ```bash
   python jarvis.py
   ```
