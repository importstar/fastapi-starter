import typer
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
import time

app = typer.Typer()
console = Console()


@app.command()
def init():
    # 1. Header สวยๆ ด้วย Rich
    console.print(
        Panel.fit("[bold cyan]🚀 FastAPI Template CLI[/bold cyan]", border_style="cyan")
    )

    # 2. รับ Input แบบ Interactive ด้วย Questionary
    project_name = questionary.text("What is your project name?").ask()

    db_type = questionary.select(
        "Which database do you want to use?",
        choices=["PostgreSQL", "MySQL", "SQLite", "MongoDB"],
    ).ask()

    features = questionary.checkbox(
        "Select additional features:",
        choices=["Docker Support", "Redis Cache", "Celery Worker", "CI/CD Pipeline"],
    ).ask()

    # 3. แสดง Feedback และ Progress Bar ด้วย Rich
    console.print(f"\n[bold green]Creating project:[/bold green] {project_name}")
    console.print(f"[bold yellow]Database:[/bold yellow] {db_type}")

    # จำลองการสร้างไฟล์ (Fake loading)
    total_steps = 10
    for i in track(range(total_steps), description="[cyan]Scaffolding files...[/cyan]"):
        time.sleep(0.1)  # ใส่ Logic การ copy template จริงๆ ตรงนี้

    # 4. Success Message
    console.print(f"\n[bold green]✅ Successfully created {project_name}![/bold green]")
    console.print(f"To get started:\n  cd {project_name}\n  docker-compose up -d")


if __name__ == "__main__":
    app()
