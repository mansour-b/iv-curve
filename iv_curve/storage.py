import os
from pathlib import Path

IV_CURVE_PATH = Path(
    os.environ.get("IV_CURVE_PATH", Path.home() / ".data" / "iv_curve")
)
IV_CURVE_PATH.mkdir(parents=True, exist_ok=True)


def timestamp(path: Path) -> str:
    return "_".join(path.stem.split("_")[-2:])
