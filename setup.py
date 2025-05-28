from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="user-behavior-simulator",
    version="1.0.0",
    author="User Behavior Simulator",
    author_email="amrihahm@yorku.ca",
    description="A cross-platform user behavior simulation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aahmadnejad/user-behavior-simiulator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "user-behavior-simulator=user_behavior_simulator.main:main",
            "ubs=user_behavior_simulator.main:main",
        ],
    },
    package_data={
        "user_behavior_simulator": ["config.json"],
    },
    include_package_data=True,
    zip_safe=False,
)