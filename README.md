# Python mooch.settings

![PyPI](https://img.shields.io/pypi/v/mooch.settings?label=mooch.settings)
![PyPI - Downloads](https://img.shields.io/pypi/dm/mooch.settings)
<img alt="GitHub Issues or Pull Requests" src="https://img.shields.io/github/issues/nickstuer/mooch.settings">

![Python Versions](https://img.shields.io/badge/python-3.9%20|%203.10%20|%203.11%20|%203.12|%203.13-blue?logo=python)
![Codecov](https://img.shields.io/codecov/c/github/nickstuer/mooch.settings)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/nickstuer/mooch.settings/run_tests.yml)

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
[![license](https://img.shields.io/github/license/nickstuer/mooch.settings.svg)](LICENSE)

A lightweight, TOML-backed configuration/settings utility that feels like a dictionary.

mooch.settings is a Python configuration library designed for simplicity and developer ergonomics. It loads settings data from TOML files and exposes them as standard Python dictionaries — allowing you to work with settings in a familiar, Python way.

## Table of Contents

- [Features](https://github.com/nickstuer/mooch.settings?tab=readme-ov-file#-features)
- [Install](https://github.com/nickstuer/mooch.settings?tab=readme-ov-file#-install)
- [Usage](https://github.com/nickstuer/mooch.settings?tab=readme-ov-file#-usage)
- [Contributing](https://github.com/nickstuer/mooch.settings?tab=readme-ov-file#-contributing)
- [License](https://github.com/nickstuer/mooch.settings?tab=readme-ov-file#-license)

## 📖 Features

 - TOML-powered: Uses toml under the hood for modern, human-friendly config files.
 - Dictionary-like interface: Access and manipulate settings with regular dict operations.
 - Nested access: Supports nested structures and dotted key notation.
 - Safe defaults: Easily provide fallback values or defaults when keys are missing from the config file.
 - Optional dynamic reload: Reloads config file everytime a key is read. (Enabled by default)


## 🛠 Install

```
# PyPI
pip install mooch.settings
```
or
```
uv add mooch.settings
```

##  📌 Dependencies
Python 3.9 or greater

## 🎮 Usage

### Example
This will create/use a 'settings.toml' file located in the .mooch directory of the user's home directory.
```python
from mooch.settings import Settings
from pathlib import Path

default_settings = {
    "settings": {
        "name": "MyName",
        "mood": "happy",
    },
}

settings = Settings(Path.home() / ".mooch/settings.toml", default_settings)

print(settings["settings.mood"])
settings["settings.mood"] = "angry"
print(settings["settings.mood"])
```
## 🏆 Contributing

PRs accepted.

If editing the Readme, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

#### Bug Reports and Feature Requests
Please use the [issue tracker](https://github.com/nickstuer/mooch.settings/issues) to report any bugs or request new features.

#### Contributors

<a href = "https://github.com/nickstuer/mooch.settings/graphs/contributors">
  <img src = "https://contrib.rocks/image?repo=nickstuer/mooch.settings"/>
</a>

## 📃 License

[MIT © Nick Stuer](LICENSE)