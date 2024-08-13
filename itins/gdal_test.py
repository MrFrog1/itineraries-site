import os
import sys

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"GDAL_LIBRARY_PATH: {os.environ.get('GDAL_LIBRARY_PATH')}")
print(f"GEOS_LIBRARY_PATH: {os.environ.get('GEOS_LIBRARY_PATH')}")

try:
    from osgeo import gdal
    print(f"GDAL version: {gdal.__version__}")
    print(f"GDAL library path: {gdal.__file__}")
except ImportError as e:
    print(f"Failed to import GDAL: {e}")

print("\nPython path:")
for path in sys.path:
    print(path)