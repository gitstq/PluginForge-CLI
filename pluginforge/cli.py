"""
PluginForge-CLI Command Line Interface
Interactive CLI with TUI dashboard support.
"""

import json
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from pluginforge.core import (
    BUILTIN_TEMPLATES,
    PluginManager,
    PluginType,
    PluginValidator,
    PluginStatus,
)

console = Console()


def print_banner():
    """Print PluginForge banner."""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🦞 PluginForge-CLI - AI IDE Plugin Management Engine       ║
║   轻量级终端AI IDE插件智能管理与发布引擎                      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""
    console.print(banner, style="bold cyan")


def print_success(message: str):
    """Print success message."""
    console.print(f"✅ {message}", style="bold green")


def print_error(message: str):
    """Print error message."""
    console.print(f"❌ {message}", style="bold red")


def print_warning(message: str):
    """Print warning message."""
    console.print(f"⚠️  {message}", style="bold yellow")


def print_info(message: str):
    """Print info message."""
    console.print(f"ℹ️  {message}", style="bold blue")


@click.group(invoke_without_command=True)
@click.option("--version", "-v", is_flag=True, help="Show version")
@click.option("--banner", "-b", is_flag=True, help="Show banner")
@click.pass_context
def main(ctx, version, banner):
    """🦞 PluginForge-CLI - Lightweight Terminal AI IDE Plugin Management Engine"""
    if version:
        from pluginforge import __version__
        console.print(f"PluginForge-CLI v{__version__}")
        return
    
    if banner:
        print_banner()
        return
    
    if ctx.invoked_subcommand is None:
        print_banner()
        console.print("\n📖 Use --help to see available commands\n")


@main.command()
@click.argument("name")
@click.option("--type", "-t", "plugin_type", default="generic", 
              type=click.Choice(["claude-code", "cursor", "codex", "copilot", "generic"]),
              help="Plugin type")
@click.option("--description", "-d", default="", help="Plugin description")
@click.option("--author", "-a", default="", help="Plugin author")
@click.option("--template", "-T", default="basic", help="Template to use")
def create(name, plugin_type, description, author, template):
    """🆕 Create a new plugin project."""
    print_banner()
    
    try:
        manager = PluginManager()
        plugin_type_enum = PluginType(plugin_type)
        
        console.print(f"\n🔨 Creating plugin: [bold cyan]{name}[/]")
        console.print(f"   Type: {plugin_type}")
        console.print(f"   Template: {template}\n")
        
        plugin_path = manager.create_plugin(
            name=name,
            plugin_type=plugin_type_enum,
            description=description,
            author=author,
        )
        
        print_success(f"Plugin created successfully!")
        console.print(f"\n📁 Plugin path: [bold]{plugin_path}[/]")
        console.print(f"\n📝 Next steps:")
        console.print(f"   1. Edit {plugin_path}/plugin.json")
        console.print(f"   2. Implement {plugin_path}/main.py")
        console.print(f"   3. Run: pluginforge validate {name}")
        console.print(f"   4. Build: pluginforge build {name}\n")
        
    except FileExistsError as e:
        print_error(str(e))
        sys.exit(1)
    except Exception as e:
        print_error(f"Failed to create plugin: {e}")
        sys.exit(1)


@main.command("list")
@click.option("--format", "-f", "output_format", default="table",
              type=click.Choice(["table", "json", "tree"]),
              help="Output format")
def list_plugins(output_format):
    """📋 List all registered plugins."""
    print_banner()
    
    manager = PluginManager()
    plugins = manager.list_plugins()
    
    if not plugins:
        print_info("No plugins found. Create one with: pluginforge create <name>")
        return
    
    if output_format == "json":
        console.print_json(data=plugins)
        return
    
    if output_format == "tree":
        tree = Tree("🦞 [bold]PluginForge Plugins[/]")
        for plugin in plugins:
            branch = tree.add(f"📦 {plugin['name']}")
            branch.add(f"Type: {plugin.get('manifest', {}).get('plugin_type', 'unknown')}")
            branch.add(f"Status: {plugin.get('status', 'unknown')}")
            branch.add(f"Path: {plugin.get('path', 'N/A')}")
        console.print(tree)
        return
    
    # Table format
    table = Table(title="🦞 PluginForge Plugins", show_header=True, header_style="bold magenta")
    table.add_column("Name", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Version", style="yellow")
    table.add_column("Status", style="blue")
    table.add_column("Description", style="white")
    
    for plugin in plugins:
        manifest = plugin.get("manifest", {})
        table.add_row(
            plugin["name"],
            manifest.get("plugin_type", "unknown"),
            manifest.get("version", "N/A"),
            plugin.get("status", "unknown"),
            manifest.get("description", "")[:40] + "..." if len(manifest.get("description", "")) > 40 else manifest.get("description", ""),
        )
    
    console.print(table)
    console.print(f"\n📊 Total: {len(plugins)} plugin(s)\n")


@main.command()
@click.argument("name")
def info(name):
    """ℹ️  Show plugin information."""
    print_banner()
    
    manager = PluginManager()
    plugin = manager.get_plugin(name)
    
    if not plugin:
        print_error(f"Plugin not found: {name}")
        sys.exit(1)
    
    manifest = plugin.get("manifest", {})
    
    # Create info panel
    info_text = f"""
[bold cyan]Name:[/] {manifest.get('name', name)}
[bold cyan]Version:[/] {manifest.get('version', 'N/A')}
[bold cyan]Type:[/] {manifest.get('plugin_type', 'generic')}
[bold cyan]Author:[/] {manifest.get('author', 'Unknown')}
[bold cyan]Status:[/] {plugin.get('status', 'unknown')}
[bold cyan]Path:[/] {plugin.get('path', 'N/A')}
[bold cyan]Installed:[/] {plugin.get('installed_at', 'N/A')}

[bold cyan]Description:[/]
{manifest.get('description', 'No description')}

[bold cyan]Dependencies:[/] {', '.join(manifest.get('dependencies', [])) or 'None'}
[bold cyan]Keywords:[/] {', '.join(manifest.get('keywords', [])) or 'None'}
"""
    
    console.print(Panel(info_text, title=f"📦 Plugin: {name}", border_style="cyan"))


@main.command()
@click.argument("name")
@click.option("--security", "-s", is_flag=True, help="Run security scan")
def validate(name, security):
    """✅ Validate plugin structure and manifest."""
    print_banner()
    
    manager = PluginManager()
    
    console.print(f"\n🔍 Validating plugin: [bold cyan]{name}[/]\n")
    
    report = manager.validate_plugin(name)
    
    if report["valid"]:
        print_success("Plugin validation passed!")
    else:
        print_error("Plugin validation failed!")
    
    if report.get("errors"):
        console.print("\n❌ [bold red]Errors:[/]")
        for error in report["errors"]:
            console.print(f"   • {error}")
    
    if report.get("warnings"):
        console.print("\n⚠️  [bold yellow]Warnings:[/]")
        for warning in report["warnings"]:
            console.print(f"   • {warning}")
    
    if report.get("info"):
        console.print("\nℹ️  [bold blue]Info:[/]")
        for info in report["info"]:
            console.print(f"   • {info}")
    
    if security and report.get("security_issues"):
        console.print("\n🔒 [bold magenta]Security Issues:[/]")
        for issue in report["security_issues"]:
            console.print(f"   • {issue['file']}:{issue['line']} - {issue['message']}")
    
    # Summary
    summary = report.get("summary", {})
    console.print(f"\n📊 [bold]Summary:[/]")
    console.print(f"   Errors: {summary.get('error_count', 0)}")
    console.print(f"   Warnings: {summary.get('warning_count', 0)}")
    console.print(f"   Info: {summary.get('info_count', 0)}\n")
    
    sys.exit(0 if report["valid"] else 1)


@main.command()
@click.argument("name")
@click.option("--output", "-o", "output_dir", default=None, help="Output directory")
def build(name, output_dir):
    """📦 Build plugin into distributable package."""
    print_banner()
    
    manager = PluginManager()
    
    console.print(f"\n📦 Building plugin: [bold cyan]{name}[/]\n")
    
    try:
        output_path = manager.build_plugin(name, Path(output_dir) if output_dir else None)
        print_success(f"Plugin built successfully!")
        console.print(f"\n📁 Package: [bold]{output_path}[/]")
        console.print(f"📦 Size: {output_path.stat().st_size / 1024:.2f} KB\n")
    except ValueError as e:
        print_error(str(e))
        sys.exit(1)
    except Exception as e:
        print_error(f"Build failed: {e}")
        sys.exit(1)


@main.command()
@click.argument("name")
@click.option("--force", "-f", is_flag=True, help="Force deletion without confirmation")
def delete(name, force):
    """🗑️  Delete a plugin."""
    print_banner()
    
    manager = PluginManager()
    plugin = manager.get_plugin(name)
    
    if not plugin:
        print_error(f"Plugin not found: {name}")
        sys.exit(1)
    
    if not force:
        if not click.confirm(f"Are you sure you want to delete '{name}'?"):
            print_info("Deletion cancelled.")
            return
    
    if manager.delete_plugin(name):
        print_success(f"Plugin '{name}' deleted successfully!")
    else:
        print_error(f"Failed to delete plugin '{name}'")


@main.command()
@click.argument("name")
@click.option("--format", "-f", "export_format", default="zip",
              type=click.Choice(["zip", "tar"]),
              help="Export format")
def export(name, export_format):
    """📤 Export plugin to archive."""
    print_banner()
    
    manager = PluginManager()
    
    console.print(f"\n📤 Exporting plugin: [bold cyan]{name}[/]")
    console.print(f"   Format: {export_format}\n")
    
    try:
        export_path = manager.export_plugin(name, export_format)
        if export_path:
            print_success("Plugin exported successfully!")
            console.print(f"\n📁 Export: [bold]{export_path}[/]\n")
        else:
            print_error(f"Plugin not found: {name}")
    except Exception as e:
        print_error(f"Export failed: {e}")
        sys.exit(1)


@main.command()
def templates():
    """📋 List available plugin templates."""
    print_banner()
    
    console.print("\n📋 [bold]Available Templates:[/]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Description", style="white")
    
    for name, template in BUILTIN_TEMPLATES.items():
        table.add_row(
            name,
            template.plugin_type.value,
            template.description,
        )
    
    console.print(table)
    console.print("\n💡 Use: pluginforge create <name> --template <template_name>\n")


@main.command()
def dashboard():
    """📊 Launch interactive TUI dashboard."""
    print_banner()
    
    console.print("\n📊 [bold]PluginForge Dashboard[/]\n")
    
    manager = PluginManager()
    plugins = manager.list_plugins()
    
    # Statistics
    total = len(plugins)
    by_type = {}
    by_status = {}
    
    for plugin in plugins:
        ptype = plugin.get("manifest", {}).get("plugin_type", "generic")
        status = plugin.get("status", "unknown")
        by_type[ptype] = by_type.get(ptype, 0) + 1
        by_status[status] = by_status.get(status, 0) + 1
    
    # Stats panel
    stats_text = f"""
[bold cyan]Total Plugins:[/] {total}

[bold cyan]By Type:[/]
{chr(10).join(f'  • {k}: {v}' for k, v in by_type.items()) or '  No plugins'}

[bold cyan]By Status:[/]
{chr(10).join(f'  • {k}: {v}' for k, v in by_status.items()) or '  No plugins'}
"""
    
    console.print(Panel(stats_text, title="📊 Statistics", border_style="cyan"))
    
    # Recent plugins
    if plugins:
        console.print("\n📦 [bold]Recent Plugins:[/]\n")
        for plugin in plugins[:5]:
            manifest = plugin.get("manifest", {})
            console.print(f"  • [cyan]{plugin['name']}[/] ({manifest.get('version', 'N/A')}) - {manifest.get('description', '')[:50]}")
    
    console.print("\n")


@main.command()
@click.argument("name")
@click.argument("key")
@click.argument("value")
def config(name, key, value):
    """⚙️  Set plugin configuration."""
    print_banner()
    
    manager = PluginManager()
    plugin = manager.get_plugin(name)
    
    if not plugin:
        print_error(f"Plugin not found: {name}")
        sys.exit(1)
    
    plugin_path = Path(plugin["path"])
    manifest_file = plugin_path / "plugin.json"
    
    try:
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
        
        # Handle nested keys with dot notation
        keys = key.split(".")
        current = manifest
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        # Try to parse value as JSON, otherwise keep as string
        try:
            parsed_value = json.loads(value)
        except json.JSONDecodeError:
            parsed_value = value
        
        current[keys[-1]] = parsed_value
        
        manifest_file.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        
        print_success(f"Configuration updated: {key} = {parsed_value}")
        
    except Exception as e:
        print_error(f"Failed to update configuration: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
