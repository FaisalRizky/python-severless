# medical/doctor/v1/core/typeB/__init__.py
import pkgutil
import importlib

# Dynamically import all modules in this package
for module_info in pkgutil.iter_modules(__path__):
    if module_info.ispkg:
        continue
    module_name = f"{__name__}.{module_info.name}"
    importlib.import_module(module_name)
