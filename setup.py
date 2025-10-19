from setuptools import setup, find_packages

setup(
    name="NoteMood",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PyQt6>=6.0"
    ],
    entry_points={
        "gui_scripts": [
            "notemood=main:main"
        ]
    },
)
