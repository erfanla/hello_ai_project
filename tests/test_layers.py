"""AD-1 layer rule: routes -> services -> models. Nothing imports from routes."""

import ast
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent / "app"
PROJECT_ROOT = APP_DIR.parent


def package_of(path: Path, root: Path) -> list[str]:
    """The package a file belongs to, as parts: app/routes/pages.py -> ["app", "routes"]."""
    parts = list(path.relative_to(root).with_suffix("").parts)
    # For pages.py the package is its folder. For __init__.py it is the folder too.
    return parts[:-1]


def imported_modules(path: Path, root: Path = PROJECT_ROOT) -> set[str]:
    """Return every module name that a Python file imports (relative imports resolved)."""
    tree = ast.parse(path.read_text(), filename=str(path))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:
                base = node.module
            else:
                # "from . import x" = this package; each extra dot goes one package up.
                package = package_of(path, root)
                up = node.level - 1
                package = package[: len(package) - up] if up else package
                base = ".".join(package + ([node.module] if node.module else []))
            if not base:
                continue
            names.add(base)
            names.update(f"{base}.{alias.name}" for alias in node.names)
    return names


def imports_package(names: set[str], package: str) -> bool:
    return any(name == package or name.startswith(package + ".") for name in names)


def python_files():
    return sorted(APP_DIR.rglob("*.py"))


def test_nobody_imports_routes():
    routes_dir = APP_DIR / "routes"
    main_file = APP_DIR / "main.py"
    bad = [
        str(path.relative_to(APP_DIR))
        for path in python_files()
        if path != main_file
        and routes_dir not in path.parents
        and imports_package(imported_modules(path), "app.routes")
    ]
    assert bad == [], f"These files import app.routes: {bad}"


def test_models_do_not_import_services():
    models_dir = APP_DIR / "models"
    bad = [
        str(path.relative_to(APP_DIR))
        for path in models_dir.rglob("*.py")
        if imports_package(imported_modules(path), "app.services")
    ]
    assert bad == [], f"These model files import app.services: {bad}"


def test_layer_checker_catches_a_bad_import(tmp_path):
    """Make sure the checker itself works, also for relative imports."""
    bad_file = tmp_path / "bad.py"
    bad_file.write_text("from app.routes.pages import router\n")
    assert imports_package(imported_modules(bad_file, root=tmp_path), "app.routes")

    services_dir = tmp_path / "app" / "services"
    services_dir.mkdir(parents=True)

    up_two = services_dir / "up_two.py"
    up_two.write_text("from ..routes import pages\n")
    assert imports_package(imported_modules(up_two, root=tmp_path), "app.routes")

    from_app = tmp_path / "app" / "helper.py"
    from_app.write_text("from . import routes\n")
    assert imports_package(imported_modules(from_app, root=tmp_path), "app.routes")

    fine = services_dir / "fine.py"
    fine.write_text("from . import errors\nfrom ..models import types\n")
    assert not imports_package(imported_modules(fine, root=tmp_path), "app.routes")
