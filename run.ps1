param(
    [string]$action = "run"
)

if ($action -eq "setup") {
    Write-Host "Creating virtual environment..."
    python -m venv .venv

    Write-Host "Activating virtual environment..."
    . .\.venv\Scripts\Activate.ps1

    Write-Host "Installing requirements..."
    pip install -r requirements.txt

    Write-Host "Setup complete. Run './run.ps1 run' to start the app."
}
elseif ($action -eq "run") {
    if (-Not (Test-Path ".venv")) {
        Write-Error ".venv not found. Run './run.ps1 setup' first."
        exit 1
    }

    $env:PYTHONUTF8 = "1"
    . .\.venv\Scripts\Activate.ps1
    python main.py
}
else {
    Write-Error "Unknown action '$action'. Use 'setup' or 'run'."
}
