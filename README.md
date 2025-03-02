# Custom Keybinder 🔑

![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A Python application for creating and managing custom keyboard shortcuts with system-wide accessibility.

## Features ✨

- **System-wide hotkey support**  
  Bind keys even when app is in background
- **Multi-action support**  
  Assign complex key combinations to single triggers
- **compatibility**  
  Works on Windows
- **Configuration wizard**  
  Easy to use for managing shortcuts
- **Profile system**  
  Save and load different shortcut configurations

## Installation 🛠️

### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a modern Python package installer and resolver that's significantly faster than pip. To install with uv:

```bash
# Clone repository
git clone https://github.com/nix24/custom_keybinder.git
cd custom_keybinder

# Method 1: Using the helper script
python uv_install.py

# Method 2: Manual installation
uv venv .venv
uv pip install -r requirements-uv.txt

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Unix/MacOS:
# source .venv/bin/activate
```

### Using pip (Legacy)

```bash
# Clone repository
git clone https://github.com/nix24/custom_keybinder.git
cd custom_keybinder

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Unix/MacOS:
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage 🚀

```bash
python main.py
```

## Contributing 🤝

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄

Distributed under the MIT License. See `LICENSE` for more information.
