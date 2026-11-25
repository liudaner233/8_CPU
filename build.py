import subprocess
import sys
from pathlib import Path

folder = Path(__file__).resolve().parent

try:
    for script in ["controller.py", "compiler.py"]:
        subprocess.run(
            [sys.executable, str(folder / script)],
            check=True
        )

except subprocess.CalledProcessError as e:
    print(f"error :{e.returncode}")
    sys.exit(1)
