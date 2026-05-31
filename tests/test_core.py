"""Tests for PluginForge-CLI."""

import json
import tempfile
from pathlib import Path

import pytest

from pluginforge.core import (
    PluginManager,
    PluginType,
    PluginValidator,
    PluginManifest,
    PluginStatus,
    BUILTIN_TEMPLATES,
)


class TestPluginManifest:
    """Tests for PluginManifest."""
    
    def test_create_manifest(self):
        """Test creating a plugin manifest."""
        manifest = PluginManifest(
            name="test-plugin",
            version="1.0.0",
            description="A test plugin",
            author="Test Author",
            plugin_type=PluginType.GENERIC,
            entry_point="main.py",
        )
        
        assert manifest.name == "test-plugin"
        assert manifest.version == "1.0.0"
        assert manifest.plugin_type == PluginType.GENERIC
    
    def test_manifest_to_dict(self):
        """Test manifest serialization to dict."""
        manifest = PluginManifest(
            name="test",
            version="0.1.0",
            description="Test",
            author="Author",
            plugin_type=PluginType.CLAUDE_CODE,
            entry_point="main.py",
        )
        
        data = manifest.to_dict()
        
        assert data["name"] == "test"
        assert data["plugin_type"] == "claude-code"
    
    def test_manifest_to_json(self):
        """Test manifest serialization to JSON."""
        manifest = PluginManifest(
            name="test",
            version="1.0.0",
            description="Test plugin",
            author="Author",
            plugin_type=PluginType.GENERIC,
            entry_point="main.py",
        )
        
        json_str = manifest.to_json()
        data = json.loads(json_str)
        
        assert data["name"] == "test"
    
    def test_manifest_from_dict(self):
        """Test creating manifest from dict."""
        data = {
            "name": "test",
            "version": "1.0.0",
            "description": "Test",
            "author": "Author",
            "plugin_type": "cursor",
            "entry_point": "main.py",
        }
        
        manifest = PluginManifest.from_dict(data)
        
        assert manifest.name == "test"
        assert manifest.plugin_type == PluginType.CURSOR


class TestPluginValidator:
    """Tests for PluginValidator."""
    
    def test_validate_structure_missing_path(self):
        """Test validation with missing path."""
        validator = PluginValidator(Path("/nonexistent/path"))
        result = validator.validate_structure()
        
        assert result is False
        assert len(validator.errors) > 0
    
    def test_validate_manifest_missing_fields(self):
        """Test manifest validation with missing fields."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = PluginValidator(Path(tmpdir))
            
            result = validator.validate_manifest({})
            
            assert result is False
            assert len(validator.errors) > 0
    
    def test_validate_manifest_valid(self):
        """Test valid manifest validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = PluginValidator(Path(tmpdir))
            
            manifest = {
                "name": "test",
                "version": "1.0.0",
                "description": "Test plugin",
                "author": "Author",
                "entry_point": "main.py",
            }
            
            result = validator.validate_manifest(manifest)
            
            assert result is True
    
    def test_scan_security_dangerous_patterns(self):
        """Test security scanning for dangerous patterns."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Create a file with dangerous pattern
            dangerous_code = '''
def bad_function():
    eval("print('dangerous')")
    exec("os.system('rm -rf /')")
'''
            (tmpdir_path / "bad.py").write_text(dangerous_code)
            
            validator = PluginValidator(tmpdir_path)
            issues = validator.scan_security()
            
            assert len(issues) > 0
    
    def test_get_report(self):
        """Test validation report generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = PluginValidator(Path(tmpdir))
            
            report = validator.get_report()
            
            assert "valid" in report
            assert "errors" in report
            assert "warnings" in report


class TestPluginManager:
    """Tests for PluginManager."""
    
    def test_create_plugin(self):
        """Test plugin creation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = PluginManager(Path(tmpdir) / "plugins")
            
            plugin_path = manager.create_plugin(
                name="test-plugin",
                plugin_type=PluginType.GENERIC,
                description="Test plugin",
                author="Test Author",
            )
            
            assert plugin_path.exists()
            assert (plugin_path / "plugin.json").exists()
            assert (plugin_path / "main.py").exists()
            assert (plugin_path / "README.md").exists()
    
    def test_list_plugins(self):
        """Test listing plugins."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = PluginManager(Path(tmpdir) / "plugins")
            
            # Create some plugins
            manager.create_plugin("plugin1", PluginType.GENERIC)
            manager.create_plugin("plugin2", PluginType.CLAUDE_CODE)
            
            plugins = manager.list_plugins()
            
            assert len(plugins) == 2
    
    def test_get_plugin(self):
        """Test getting plugin info."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = PluginManager(Path(tmpdir) / "plugins")
            
            manager.create_plugin("test-plugin", PluginType.GENERIC)
            
            plugin = manager.get_plugin("test-plugin")
            
            assert plugin is not None
            assert plugin["name"] == "test-plugin"
    
    def test_get_nonexistent_plugin(self):
        """Test getting nonexistent plugin."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = PluginManager(Path(tmpdir) / "plugins")
            
            plugin = manager.get_plugin("nonexistent")
            
            assert plugin is None
    
    def test_delete_plugin(self):
        """Test deleting plugin."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = PluginManager(Path(tmpdir) / "plugins")
            
            manager.create_plugin("to-delete", PluginType.GENERIC)
            
            result = manager.delete_plugin("to-delete")
            
            assert result is True
            assert manager.get_plugin("to-delete") is None
    
    def test_build_plugin(self):
        """Test building plugin package."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = PluginManager(Path(tmpdir) / "plugins")
            
            manager.create_plugin("build-test", PluginType.GENERIC)
            
            archive_path = manager.build_plugin("build-test")
            
            assert archive_path.exists()
            assert archive_path.suffix == ".zip"
    
    def test_export_plugin(self):
        """Test exporting plugin."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = PluginManager(Path(tmpdir) / "plugins")
            
            manager.create_plugin("export-test", PluginType.GENERIC)
            
            export_path = manager.export_plugin("export-test", "zip")
            
            assert export_path is not None
            assert export_path.exists()


class TestBuiltinTemplates:
    """Tests for built-in templates."""
    
    def test_templates_exist(self):
        """Test that built-in templates exist."""
        assert "basic" in BUILTIN_TEMPLATES
        assert "claude-code" in BUILTIN_TEMPLATES
        assert "cursor" in BUILTIN_TEMPLATES
    
    def test_template_render(self):
        """Test template rendering."""
        template = BUILTIN_TEMPLATES["basic"]
        
        context = {
            "name": "test-plugin",
            "description": "Test description",
            "author": "Test Author",
            "plugin_type": "generic",
        }
        
        rendered = template.render(context)
        
        assert "plugin.json" in rendered
        assert "test-plugin" in rendered["plugin.json"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
