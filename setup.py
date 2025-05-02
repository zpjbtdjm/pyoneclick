from setuptools import setup, find_packages

setup(
    name="pyoneclick",
    version="0.0.1",
    author="zpjbtdjm",
    description="Automatically filter control variables, similar to Stata's oneclick command but with more function.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    install_requires=[
        "stata_setup",
        "tqdm"
    ],
    entry_points={
        "console_scripts": [
            "pyoneclick=src.main:main",
        ],
    },
)
