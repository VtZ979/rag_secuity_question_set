# Quick Fix: NumPy Version Issue

## Problem

If you see this error:
```
ERROR: Failed to build 'numpy' when getting requirements to build wheel
AttributeError: module 'pkgutil' has no attribute 'ImpImporter'
```

This happens because:
- You're using **Python 3.13**
- `numpy==1.24.4` doesn't support Python 3.13
- Python 3.13 removed `pkgutil.ImpImporter`

## Quick Fix (30 seconds)

**Option 1: Update requirements.txt (Already done)**
The `requirements.txt` has been updated to:
```txt
numpy>=1.24.0,<1.27.0
```

Just reinstall:
```powershell
cd rag-backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Option 2: Manual fix (if Option 1 doesn't work)**
```powershell
cd rag-backend
.\venv\Scripts\Activate.ps1
pip install "numpy>=1.26.0" --upgrade
pip install -r requirements.txt
```

## Why This Works

- `numpy>=1.24.0,<1.27.0` allows pip to choose a compatible version
- For Python 3.13, it will install numpy 1.26.x (which supports Python 3.13)
- For Python 3.11/3.12, it will install numpy 1.24.x or 1.25.x

## Alternative: Use Python 3.11 or 3.12

If you prefer to use the exact `numpy==1.24.4`:
1. Install Python 3.11 or 3.12
2. Recreate virtual environment with that Python version

But the version range fix is simpler and works with all Python versions.

