# mooch-settings

![PyPI](https://img.shields.io/pypi/v/mooch-settings?label=mooch-settings)
![Python Versions](https://img.shields.io/badge/python-3.9+-blue?logo=python)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/mooch-settings)](https://pypistats.org/packages/mooch-settings)
[![GitHub issues](https://img.shields.io/github/issues/nickstuer/mooch-settings.svg)](https://github.com/nickstuer/mooch-settings/issues)

![Lines Of Code](https://tokei.rs/b1/github/nickstuer/mooch-settings)
[![Codecov](https://img.shields.io/codecov/c/github/nickstuer/mooch-settings)](https://app.codecov.io/gh/nickstuer/mooch-settings)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/nickstuer/mooch-settings/run_tests.yml)](https://github.com/nickstuer/mooch-settings/actions/workflows/run_tests.yml)

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
[![license](https://img.shields.io/github/license/nickstuer/mooch-settings.svg)](LICENSE)

A lightweight, TOML-backed configuration/settings utility that that exposes project settings as standard Python dictionaries.

mooch-settings is a Python configuration library designed for simplicity and developer ergonomics. It loads settings data from TOML files and exposes them as standard Python dictionaries — allowing you to work with settings in a familiar, Pythonic way.

## Table of Contents

- [Features](https://github.com/nickstuer/mooch-settings?tab=readme-ov-file#-features)
- [Install](https://github.com/nickstuer/mooch-settings?tab=readme-ov-file#-install)
- [Usage](https://github.com/nickstuer/mooch-settings?tab=readme-ov-file#-usage)
- [Contributing](https://github.com/nickstuer/mooch-settings?tab=readme-ov-file#-contributing)
- [License](https://github.com/nickstuer/mooch-settings?tab=readme-ov-file#-license)

## 📖 Features

- TOML-powered: Uses TOML under the hood for modern, human-friendly settings files.
- Dictionary-like interface: Access and manipulate settings with regular dictionary operations.
- Nested access: Supports nested keys with dotted key notation.
- Optional `defaults`: Provide default values for initializing the settings file or for when a key is missing in the settings file.
- Optional `always_reload`: Reload the setting file everytime a key is read. (Enabled by default)


## 🛠 Install

```
# PyPI
pip install mooch-settings
```
or
```
uv add mooch-settings
```

##  📌 Dependencies
Python 3.9 or greater

## 🎮 Usage

### Example
This will create/use a 'settings.toml' file located in the '.mooch' directory of the user's home directory.
```python
from mooch-settings import Settings

defaults = {
    "settings": {
        "name": "MyName",
        "mood": "happy",
    },
}

settings = Settings("mooch", defaults) # Change 'mooch' to your application's name

print(settings["settings.mood"])
settings["settings.mood"] = "angry"
print(settings["settings.mood"])
```
## 🏆 Contributing

PRs accepted.

If editing the Readme, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

#### Bug Reports and Feature Requests
Please use the [issue tracker](https://github.com/nickstuer/mooch-settings/issues) to report any bugs or request new features.

#### Contributors

<a href = "https://github.com/nickstuer/mooch-settings/graphs/contributors">
  <img src = "https://contrib.rocks/image?repo=nickstuer/mooch-settings"/>
</a>

## 📃 License

[MIT © Nick Stuer](LICENSE)