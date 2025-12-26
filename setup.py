"""Setup configuration for Rural Connectivity Mapper 2026."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip() 
        for line in requirements_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="rural-connectivity-mapper-2026",
    version="1.0.0",
    author="Daniel Azevedo Novais",
    author_email="",
    description="Python-based tool to map and analyze rural internet connectivity in Brazil",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Telecommunications Industry",
        "Topic :: Scientific/Engineering :: GIS",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "connectivity-mapper=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
