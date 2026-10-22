# Contributing to Windows 11 Explorer for Linux

Thank you for considering contributing to Windows 11 Explorer!

## How to Contribute

1. **Fork the Repository** on GitHub.
2. **Clone your fork**:
   ```bash
   git clone https://github.com/Lucy134645/win11-explorer.git
   cd win11-explorer
   ```
3. **Set up a Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```
4. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/my-cool-feature
   ```
5. **Run Tests / Verification**:
   ```bash
   python test_app.py
   ```
6. **Commit & Push**:
   ```bash
   git commit -m "feat: add my new feature"
   git push origin feature/my-cool-feature
   ```
7. **Open a Pull Request** against `master`.

## Code Style & Guidelines
- Follow standard Python PEP 8 conventions.
- Keep Fluent Design 2 / Windows 11 aesthetic integrity.
- Use vector SVG icons where possible (`win11_explorer/icons.py`).
