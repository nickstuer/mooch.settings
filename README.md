# Python mooch.config

![PyPI](https://img.shields.io/pypi/v/mooch.config?label=mooch.config)
![PyPI - Downloads](https://img.shields.io/pypi/dm/mooch.config)
<img alt="GitHub Issues or Pull Requests" src="https://img.shields.io/github/issues/nickstuer/mooch.config">

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
[![license](https://img.shields.io/github/license/nickstuer/mooch.config.svg)](LICENSE)

This Python package is a collection of useful Python code that is commonly used on all types of Python projects.

## Table of Contents

- [Features](https://github.com/nickstuer/mooch?tab=readme-ov-file#-features)
- [Install](https://github.com/nickstuer/mooch?tab=readme-ov-file#-install)
- [Usage](https://github.com/nickstuer/mooch?tab=readme-ov-file#-usage)
- [Contributing](https://github.com/nickstuer/mooch?tab=readme-ov-file#-contributing)
- [License](https://github.com/nickstuer/mooch?tab=readme-ov-file#-license)

## 📖 Features


### Config File
Uses a TOML config file. Easily get/set configuration values. Automatically sets values to defaults if they're not currently saved in the configuration file.


## 🛠 Install

```
# PyPI
pip install mooch.config
```
or
```
uv add mooch.config
```

##  📌 Dependencies
Python 3.9 or greater

## 🎮 Usage

### Config File
```python
from mooch import Config
default_settings = {
    "settings": {
        "name": "MyName,
        "mood": "happy",
    },
}

config = Config("settings.toml", default_settings)

print(config["settings.mood"])
config["settings.mood"] = "angry"
print(config["settings.mood"])
```
## 🏆 Contributing

PRs accepted.

If editing the Readme, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

#### Bug Reports and Feature Requests
Please use the [issue tracker](https://github.com/nickstuer/mooch.config/issues) to report any bugs or request new features.

#### Contributors

<a href = "https://github.com/nickstuer/mooch.config/graphs/contributors">
  <img src = "https://contrib.rocks/image?repo=nickstuer/mooch.config"/>
</a>

## 📃 License

[MIT © Nick Stuer](LICENSE)