"""
PluginForge-CLI Core Module
Core functionality for plugin management, validation, and publishing.
"""

import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    import yaml
except ImportError:
    yaml = None

try:
    import toml
except ImportError:
    toml = None

try:
    from jinja2 import Environment, FileSystemLoader, Template
except ImportError:
    Environment = None


class PluginType(Enum):
    """Supported plugin types for different AI IDEs."""
    CLAUDE_CODE = "claude-code"
    CURSOR = "cursor"
    CODEX = "codex"
    COPILOT = "copilot"
    GENERIC = "generic"


class PluginStatus(Enum):
    """Plugin development status."""
    DRAFT = "draft"
    DEVELOPMENT = "development"
    TESTING = "testing"
    READY = "ready"
    PUBLISHED = "published"
    DEPRECATED = "deprecated"


@dataclass
class PluginManifest:
    """Plugin manifest configuration."""
    name: str
    version: str
    description: str
    author: str
    plugin_type: PluginType
    entry_point: str
    dependencies: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    license: str = "MIT"
    homepage: Optional[str] = None
    repository: Optional[str] = None
    min_version: str = "1.0.0"
    max_version: Optional[str] = None
    config_schema: Optional[Dict[str, Any]] = None
    hooks: Dict[str, str] = field(default_factory=dict)
    permissions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert manifest to dictionary."""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "plugin_type": self.plugin_type.value,
            "entry_point": self.entry_point,
            "dependencies": self.dependencies,
            "keywords": self.keywords,
            "license": self.license,
            "homepage": self.homepage,
            "repository": self.repository,
            "min_version": self.min_version,
            "max_version": self.max_version,
            "config_schema": self.config_schema,
            "hooks": self.hooks,
            "permissions": self.permissions,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PluginManifest":
        """Create manifest from dictionary."""
        data["plugin_type"] = PluginType(data.get("plugin_type", "generic"))
        return cls(**data)
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    def to_yaml(self) -> str:
        """Convert to YAML string."""
        if yaml is None:
            raise ImportError("PyYAML is required for YAML export")
        return yaml.dump(self.to_dict(), allow_unicode=True, default_flow_style=False)


@dataclass
class PluginTemplate:
    """Plugin template for quick scaffolding."""
    name: str
    description: str
    plugin_type: PluginType
    files: Dict[str, str]  # filename -> content template
    default_config: Dict[str, Any] = field(default_factory=dict)
    
    def render(self, context: Dict[str, Any]) -> Dict[str, str]:
        """Render template files with context."""
        if Environment is None:
            # Simple string formatting without Jinja2
            return {
                filename: content.format(**context)
                for filename, content in self.files.items()
            }
        
        rendered = {}
        for filename, content in self.files.items():
            template = Template(content)
            rendered[filename] = template.render(**context)
        return rendered


class PluginValidator:
    """Plugin validation and security scanning."""
    
    # Dangerous patterns to detect
    DANGEROUS_PATTERNS = [
        r"eval\s*\(",
        r"exec\s*\(",
        r"__import__\s*\(",
        r"subprocess\.call\s*\([^)]*shell\s*=\s*True",
        r"os\.system\s*\(",
        r"compile\s*\(",
    ]
    
    # Required manifest fields
    REQUIRED_FIELDS = ["name", "version", "description", "author", "entry_point"]
    
    def __init__(self, plugin_path: Path):
        self.plugin_path = Path(plugin_path)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
    
    def validate_structure(self) -> bool:
        """Validate plugin directory structure."""
        if not self.plugin_path.exists():
            self.errors.append(f"Plugin path does not exist: {self.plugin_path}")
            return False
        
        if not self.plugin_path.is_dir():
            self.errors.append(f"Plugin path is not a directory: {self.plugin_path}")
            return False
        
        # Check for manifest file
        manifest_files = ["plugin.json", "plugin.yaml", "plugin.yml", "plugin.toml"]
        found_manifest = False
        for manifest in manifest_files:
            if (self.plugin_path / manifest).exists():
                found_manifest = True
                self.info.append(f"Found manifest: {manifest}")
                break
        
        if not found_manifest:
            self.errors.append("No plugin manifest found (plugin.json/yaml/toml)")
        
        return found_manifest
    
    def validate_manifest(self, manifest: Dict[str, Any]) -> bool:
        """Validate plugin manifest content."""
        valid = True
        
        for field in self.REQUIRED_FIELDS:
            if field not in manifest or not manifest[field]:
                self.errors.append(f"Missing required field: {field}")
                valid = False
        
        # Validate version format
        if "version" in manifest:
            version = manifest["version"]
            if not re.match(r"^\d+\.\d+\.\d+", str(version)):
                self.warnings.append(f"Version '{version}' does not follow semantic versioning")
        
        # Validate plugin type
        if "plugin_type" in manifest:
            try:
                PluginType(manifest["plugin_type"])
            except ValueError:
                self.warnings.append(f"Unknown plugin type: {manifest['plugin_type']}")
        
        return valid
    
    def scan_security(self, code_path: Optional[Path] = None) -> List[Dict[str, Any]]:
        """Scan plugin code for security issues."""
        issues = []
        scan_path = code_path or self.plugin_path
        
        for py_file in scan_path.rglob("*.py"):
            try:
                content = py_file.read_text(encoding="utf-8")
                for pattern in self.DANGEROUS_PATTERNS:
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        line_num = content[:match.start()].count("\n") + 1
                        issues.append({
                            "file": str(py_file.relative_to(scan_path)),
                            "line": line_num,
                            "pattern": pattern,
                            "severity": "warning",
                            "message": f"Potentially dangerous pattern detected: {pattern}"
                        })
            except Exception as e:
                self.warnings.append(f"Could not scan file {py_file}: {e}")
        
        return issues
    
    def validate_dependencies(self, dependencies: List[str]) -> Tuple[bool, List[str]]:
        """Validate plugin dependencies."""
        missing = []
        for dep in dependencies:
            # Extract package name from dependency string
            pkg_name = re.split(r"[<>=!~]", dep)[0].strip()
            try:
                __import__(pkg_name.replace("-", "_"))
            except ImportError:
                missing.append(pkg_name)
        
        return len(missing) == 0, missing
    
    def get_report(self) -> Dict[str, Any]:
        """Get validation report."""
        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
            "info": self.info,
            "summary": {
                "error_count": len(self.errors),
                "warning_count": len(self.warnings),
                "info_count": len(self.info),
            }
        }


class PluginManager:
    """Main plugin management class."""
    
    def __init__(self, plugins_dir: Optional[Path] = None):
        self.plugins_dir = Path(plugins_dir) if plugins_dir else Path.home() / ".pluginforge" / "plugins"
        self.plugins_dir.mkdir(parents=True, exist_ok=True)
        self.registry_file = self.plugins_dir.parent / "registry.json"
        self._load_registry()
    
    def _load_registry(self) -> None:
        """Load plugin registry."""
        if self.registry_file.exists():
            try:
                self.registry = json.loads(self.registry_file.read_text(encoding="utf-8"))
            except Exception:
                self.registry = {"plugins": {}, "version": "1.0.0"}
        else:
            self.registry = {"plugins": {}, "version": "1.0.0"}
    
    def _save_registry(self) -> None:
        """Save plugin registry."""
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        self.registry_file.write_text(
            json.dumps(self.registry, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
    
    def create_plugin(
        self,
        name: str,
        plugin_type: PluginType,
        description: str = "",
        author: str = "",
        template: Optional[PluginTemplate] = None,
    ) -> Path:
        """Create a new plugin from template."""
        # Sanitize name
        safe_name = re.sub(r"[^a-zA-Z0-9_-]", "-", name.lower())
        plugin_path = self.plugins_dir / safe_name
        
        if plugin_path.exists():
            raise FileExistsError(f"Plugin already exists: {plugin_path}")
        
        plugin_path.mkdir(parents=True)
        
        # Create manifest
        manifest = PluginManifest(
            name=safe_name,
            version="0.1.0",
            description=description or f"{name} plugin",
            author=author or "Anonymous",
            plugin_type=plugin_type,
            entry_point="main.py",
        )
        
        # Write manifest
        (plugin_path / "plugin.json").write_text(
            manifest.to_json(), encoding="utf-8"
        )
        
        # Create main.py template
        main_py = '''"""
{name} - {description}
"""

def activate(context):
    """Called when the plugin is activated."""
    print(f"Plugin {name!r} activated!")
    return True


def deactivate(context):
    """Called when the plugin is deactivated."""
    print(f"Plugin {name!r} deactivated.")
    return True


def execute(command: str, **kwargs):
    """Main plugin execution entry point."""
    return {{"status": "ok", "command": command, "result": None}}
'''.format(name=safe_name, description=description or f"{name} plugin")
        
        (plugin_path / "main.py").write_text(main_py, encoding="utf-8")
        
        # Create README
        readme = f"""# {name}

{description or 'A PluginForge plugin'}

## Installation

```bash
pluginforge install {safe_name}
```

## Usage

```bash
pluginforge run {safe_name}
```

## License

MIT
"""
        (plugin_path / "README.md").write_text(readme, encoding="utf-8")
        
        # Register plugin
        self.registry["plugins"][safe_name] = {
            "path": str(plugin_path),
            "installed_at": datetime.now().isoformat(),
            "status": PluginStatus.DRAFT.value,
        }
        self._save_registry()
        
        return plugin_path
    
    def list_plugins(self) -> List[Dict[str, Any]]:
        """List all registered plugins."""
        plugins = []
        for name, info in self.registry.get("plugins", {}).items():
            plugin_path = Path(info.get("path", ""))
            manifest = None
            
            if plugin_path.exists():
                manifest_file = plugin_path / "plugin.json"
                if manifest_file.exists():
                    try:
                        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
                    except Exception:
                        pass
            
            plugins.append({
                "name": name,
                "path": info.get("path"),
                "status": info.get("status", "unknown"),
                "installed_at": info.get("installed_at"),
                "manifest": manifest,
            })
        
        return plugins
    
    def get_plugin(self, name: str) -> Optional[Dict[str, Any]]:
        """Get plugin information by name."""
        if name not in self.registry.get("plugins", {}):
            return None
        
        info = self.registry["plugins"][name]
        plugin_path = Path(info.get("path", ""))
        
        if not plugin_path.exists():
            return None
        
        manifest_file = plugin_path / "plugin.json"
        manifest = None
        if manifest_file.exists():
            try:
                manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        
        return {
            "name": name,
            "path": str(plugin_path),
            "status": info.get("status"),
            "installed_at": info.get("installed_at"),
            "manifest": manifest,
        }
    
    def validate_plugin(self, name: str) -> Dict[str, Any]:
        """Validate a plugin."""
        plugin_info = self.get_plugin(name)
        if not plugin_info:
            return {"valid": False, "errors": [f"Plugin not found: {name}"]}
        
        validator = PluginValidator(Path(plugin_info["path"]))
        
        # Run validations
        validator.validate_structure()
        
        if plugin_info.get("manifest"):
            validator.validate_manifest(plugin_info["manifest"])
        
        security_issues = validator.scan_security()
        
        report = validator.get_report()
        report["security_issues"] = security_issues
        
        return report
    
    def build_plugin(self, name: str, output_dir: Optional[Path] = None) -> Path:
        """Build plugin into distributable package."""
        plugin_info = self.get_plugin(name)
        if not plugin_info:
            raise ValueError(f"Plugin not found: {name}")
        
        plugin_path = Path(plugin_info["path"])
        output = Path(output_dir) if output_dir else plugin_path / "dist"
        output.mkdir(parents=True, exist_ok=True)
        
        # Create distribution archive
        archive_name = f"{name}-v{plugin_info.get('manifest', {}).get('version', '0.0.1')}"
        archive_path = output / archive_name
        
        shutil.make_archive(
            str(archive_path),
            "zip",
            plugin_path,
        )
        
        return Path(f"{archive_path}.zip")
    
    def delete_plugin(self, name: str) -> bool:
        """Delete a plugin."""
        if name not in self.registry.get("plugins", {}):
            return False
        
        plugin_info = self.registry["plugins"][name]
        plugin_path = Path(plugin_info.get("path", ""))
        
        if plugin_path.exists():
            shutil.rmtree(plugin_path)
        
        del self.registry["plugins"][name]
        self._save_registry()
        
        return True
    
    def export_plugin(self, name: str, format: str = "zip") -> Optional[Path]:
        """Export plugin to specified format."""
        plugin_info = self.get_plugin(name)
        if not plugin_info:
            return None
        
        plugin_path = Path(plugin_info["path"])
        export_dir = plugin_path / "exports"
        export_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_name = f"{name}_{timestamp}"
        
        if format == "zip":
            export_path = export_dir / f"{export_name}.zip"
            shutil.make_archive(str(export_path.with_suffix("")), "zip", plugin_path)
        elif format == "tar":
            export_path = export_dir / f"{export_name}.tar.gz"
            shutil.make_archive(str(export_path.with_suffix("")), "gztar", plugin_path)
        else:
            raise ValueError(f"Unsupported export format: {format}")
        
        return export_path


# Built-in templates
BUILTIN_TEMPLATES = {
    "basic": PluginTemplate(
        name="basic",
        description="Basic plugin template with minimal structure",
        plugin_type=PluginType.GENERIC,
        files={
            "plugin.json": '''{
    "name": "{{ name }}",
    "version": "0.1.0",
    "description": "{{ description }}",
    "author": "{{ author }}",
    "plugin_type": "{{ plugin_type }}",
    "entry_point": "main.py"
}''',
            "main.py": '''"""{{ name }} - {{ description }}"""

def activate(context):
    return True

def deactivate(context):
    return True

def execute(command: str, **kwargs):
    return {"status": "ok"}
''',
            "README.md": """# {{ name }}

{{ description }}

## Usage

```
pluginforge run {{ name }}
```
""",
        }
    ),
    "claude-code": PluginTemplate(
        name="claude-code",
        description="Claude Code plugin template with hooks support",
        plugin_type=PluginType.CLAUDE_CODE,
        files={
            "plugin.json": '''{
    "name": "{{ name }}",
    "version": "0.1.0",
    "description": "{{ description }}",
    "author": "{{ author }}",
    "plugin_type": "claude-code",
    "entry_point": "main.py",
    "hooks": {
        "pre_command": "on_pre_command",
        "post_command": "on_post_command",
        "on_file_change": "on_file_change"
    },
    "permissions": ["file_read", "file_write", "command_execute"]
}''',
            "main.py": '''"""{{ name }} - Claude Code Plugin"""

def activate(context):
    """Called when plugin is activated."""
    print("{{ name }} plugin activated for Claude Code")
    return True

def deactivate(context):
    """Called when plugin is deactivated."""
    return True

def on_pre_command(command: str, context: dict):
    """Hook: Called before command execution."""
    return {"proceed": True}

def on_post_command(command: str, result: dict, context: dict):
    """Hook: Called after command execution."""
    pass

def on_file_change(file_path: str, change_type: str, context: dict):
    """Hook: Called when file changes."""
    pass
''',
            "README.md": """# {{ name }}

{{ description }}

A Claude Code plugin with hook support.

## Hooks

- `pre_command`: Before command execution
- `post_command`: After command execution  
- `on_file_change`: On file modifications

## Installation

```bash
pluginforge install {{ name }}
```
""",
        }
    ),
    "cursor": PluginTemplate(
        name="cursor",
        description="Cursor IDE plugin template",
        plugin_type=PluginType.CURSOR,
        files={
            "plugin.json": '''{
    "name": "{{ name }}",
    "version": "0.1.0",
    "description": "{{ description }}",
    "author": "{{ author }}",
    "plugin_type": "cursor",
    "entry_point": "main.py",
    "config_schema": {
        "enabled": {"type": "boolean", "default": true}
    }
}''',
            "main.py": '''"""{{ name }} - Cursor Plugin"""

def activate(context):
    """Activate the plugin in Cursor."""
    return True

def deactivate(context):
    """Deactivate the plugin."""
    return True

def provide_completions(context):
    """Provide code completions."""
    return []

def analyze_code(code: str, context: dict):
    """Analyze code and provide suggestions."""
    return {"suggestions": []}
''',
            "README.md": """# {{ name }}

{{ description }}

A Cursor IDE plugin.

## Features

- Code completions
- Code analysis
- Smart suggestions

## Installation

```bash
pluginforge install {{ name }}
```
""",
        }
    ),
}
