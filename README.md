# Python Visualizer Framework 🐍

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-green)
![Status](https://img.shields.io/badge/Status-Stable-success)

The **Python Visualizer Framework** is a lightweight, modular engine built with `CustomTkinter` designed to host, visualize, and hot-reload graphical experiments.

It acts as a container application that dynamically loads external Python scripts (plugins) into a main viewport, allowing developers to iterate on UI/UX and animation code without restarting the application.

## ✨ Core Features

* **Dynamic Module Loading**: Automatically scans the `plugins/` directory and lists available effects.
* **Hot Reload System**: Edit your plugin code while the app is running and click **"Reload Code"** to see changes instantly.
* **Lifecycle Management**: Handles setup (`__init__`) and cleanup (`teardown`) to prevent memory leaks or ghost threads between effect switches.
* **Focus Mode**: Toggle the sidebar (Press `Esc`) to view animations in full distraction-free mode.
* **Adaptive UI**: Built on `CustomTkinter` with a modern dark theme and responsive grid layout.

## 📂 System Architecture

The application is structured around a "Host-Plugin" relationship:
