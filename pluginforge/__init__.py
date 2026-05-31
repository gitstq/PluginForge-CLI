"""
PluginForge-CLI - Lightweight Terminal AI IDE Plugin Intelligent Management & Publishing Engine
轻量级终端AI IDE插件智能管理与发布引擎

A zero-dependency-core CLI tool for managing AI IDE plugins with TUI dashboard support.
"""

__version__ = "1.0.0"
__author__ = "PluginForge Team"
__license__ = "MIT"

from pluginforge.core import PluginManager, PluginTemplate, PluginValidator
from pluginforge.cli import main

__all__ = [
    "PluginManager",
    "PluginTemplate", 
    "PluginValidator",
    "main",
    "__version__",
]
