import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from .parser import LogParser
from .generators import TestGenerator, AIFixSuggester
from .models import TestGenerationConfig

app = typer.Typer(
    name="ghostreplay",
    help="🔄 GhostReplay - Turn production errors into reproducible tests",
    rich_markup_mode="rich"
)
console = Console()


@app.command()
def ingest(
    log_file: str = typer.Argument(..., help="Path to the JSON log file"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file for parsed context")
):
    """
    📥 Parse structured error log into an IncidentContext object
    """
    try:
        console.print(f"[bold blue]Parsing log file:[/bold blue] {log_file}")
        
        incident = LogParser.parse_log_file(log_file)
        
        console.print("[green]✅ Successfully parsed log file![/green]")
        console.print(Panel.fit(
            f"[bold]Method:[/bold] {incident.method}\n"
            f"[bold]Endpoint:[/bold] {incident.endpoint}\n"
            f"[bold]Timestamp:[/bold] {incident.timestamp}\n"
            f"[bold]Status:[/bold] {incident.status_code}\n"
            f"[bold]Error:[/bold] {incident.error_message}",
            title="Incident Summary"
        ))
        
        if output:
            with open(output, 'w') as f:
                f.write(incident.json(indent=2))
            console.print(f"[green]💾 Saved incident context to:[/green] {output}")
    
    except Exception as e:
        console.print(f"[red]❌ Error parsing log file:[/red] {e}")
        raise typer.Exit(1)


@app.command("gen-test")
def generate_test(
    log_file: Optional[str] = typer.Option(None, "--log", help="Log file to parse"),
    framework: str = typer.Option("pytest", "--framework", help="Testing framework"),
    output: str = typer.Option("tests/test_bug.py", "--out", help="Output path for test file"),
    context_file: Optional[str] = typer.Option(None, "--context", help="Use existing incident context file")
):
    """
    🧪 Generate a reproducible test file from error logs
    """
    try:
        # Parse incident context
        if context_file:
            console.print(f"[blue]Loading context from:[/blue] {context_file}")
            with open(context_file, 'r') as f:
                import json
                incident_data = json.load(f)
                incident = LogParser.parse_log_dict(incident_data)
        elif log_file:
            console.print(f"[blue]Parsing log file:[/blue] {log_file}")
            incident = LogParser.parse_log_file(log_file)
        else:
            console.print("[red]❌ Must provide either --log or --context[/red]")
            raise typer.Exit(1)
        
        # Generate test
        config = TestGenerationConfig(framework=framework, output_path=output)
        generator = TestGenerator(config)
        
        console.print(f"[yellow]🔨 Generating {framework} test...[/yellow]")
        output_path = generator.write_test_file(incident)
        
        console.print(f"[green]✅ Generated test file:[/green] {output_path}")
        
        # Show preview of generated test
        with open(output_path, 'r') as f:
            test_content = f.read()
        
        syntax = Syntax(test_content[:500] + "...", "python", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title=f"Generated Test Preview - {output_path}"))
        
        console.print(f"\n[bold green]🚀 Next steps:[/bold green]")
        console.print(f"1. Run: [bold]pytest {output_path}[/bold]")
        console.print(f"2. Get fix suggestions: [bold]ghostreplay suggest-fix {output_path}[/bold]")
    
    except Exception as e:
        console.print(f"[red]❌ Error generating test:[/red] {e}")
        raise typer.Exit(1)


@app.command("suggest-fix")
def suggest_fix(
    test_file: str = typer.Argument(..., help="Path to the generated test file")
):
    """
    🤖 Get AI-powered patch suggestions for the failing test
    """
    try:
        console.print(f"[yellow]🤖 Analyzing test file:[/yellow] {test_file}")
        
        if not Path(test_file).exists():
            console.print(f"[red]❌ Test file not found:[/red] {test_file}")
            raise typer.Exit(1)
        
        suggestion = AIFixSuggester.suggest_fix(test_file)
        
        console.print(Panel(
            suggestion,
            title="🤖 AI Fix Suggestion",
            border_style="cyan"
        ))
    
    except Exception as e:
        console.print(f"[red]❌ Error generating suggestion:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def demo():
    """
    🎯 Run a complete demo workflow
    """
    console.print("[bold cyan]🎯 GhostReplay Demo Workflow[/bold cyan]\n")
    
    # Create sample log
    sample_log = {
        "method": "POST",
        "endpoint": "/api/users/create",
        "body": {"username": "testuser", "email": "test@example.com"},
        "stack": "Traceback (most recent call last):\n  File \"/app/users.py\", line 42, in create_user\n    user.save()\n  File \"/app/models.py\", line 15, in save\n    raise ValidationError('Email already exists')",
        "timestamp": "2024-01-15T10:30:45Z",
        "status_code": 400,
        "error_message": "Email already exists",
        "user_id": "user_123"
    }
    
    # Save sample log
    with open("sample_error.json", "w") as f:
        import json
        json.dump(sample_log, f, indent=2)
    
    console.print("1️⃣ [bold]Created sample error log:[/bold] sample_error.json")
    
    # Demo commands
    console.print("\n2️⃣ [bold]Demo Commands:[/bold]")
    console.print("   [dim]# Parse the log[/dim]")
    console.print("   ghostreplay ingest sample_error.json")
    console.print("\n   [dim]# Generate test[/dim]")  
    console.print("   ghostreplay gen-test --log sample_error.json --out tests/demo_test.py")
    console.print("\n   [dim]# Get AI suggestions[/dim]")
    console.print("   ghostreplay suggest-fix tests/demo_test.py")
    
    console.print("\n[green]✨ Demo setup complete! Try running the commands above.[/green]")


if __name__ == "__main__":
    app()