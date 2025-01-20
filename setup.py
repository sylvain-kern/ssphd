from setuptools import setup, find_packages

setup(
    name="ssphd",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "ssphd": ["config_schema.json"],
    },
    install_requires=[
        "click",
        "pypandoc",
        "pyyaml",
        "jsonschema",
        "rich",
        "pandocfilters",
    ],
    entry_points={
        'console_scripts': [
            'ssphd = ssphd.cli:main',
        ],
    },
    author="",
    description="Single-source PhD manuscript builder",
    long_description=open("readme.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sylvain-kern/ssphd/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
