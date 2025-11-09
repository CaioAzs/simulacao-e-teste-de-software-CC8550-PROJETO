"""
Arquivo conftest.py raiz que importa fixtures da pasta fixtures.
Pytest automaticamente descobre fixtures em arquivos conftest.py em subdiretórios.
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para imports funcionarem corretamente
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Importa fixtures do conftest.py dentro de fixtures/
pytest_plugins = ["tests.fixtures.conftest"]
