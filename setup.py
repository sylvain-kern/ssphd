from setuptools import setup, find_packages

setup(
    name="ssphd",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandoc-python",
        "click",
    ],
    entry_points={
        'console_scripts': [
            'ssphd = ssphd.cli:main',
        ],
    },
    author="",
    description="Single-source PhD manuscript builder",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ssphd",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
