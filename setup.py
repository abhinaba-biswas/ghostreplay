from setuptools import setup, find_packages

setup(
    name="ghostreplay",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer[all]>=0.9.0",
        "pydantic>=2.0.0",
        "pytest>=7.0.0",
        "freezegun>=1.2.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ghostreplay=ghostreplay.cli:app",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="Turn production error logs into reproducible failing tests",
    long_description=open("README.md").read() if Path("README.md").exists() else "",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ghostreplay",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)