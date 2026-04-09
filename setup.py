from setuptools import setup, find_packages

setup(
    name="ssphd",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pypandoc",
        "pandocfilters",
        "rich",
        "bs4",
        "lunr",
        "PyYAML",
    ],
    entry_points={
        "console_scripts": [
            "ssphd=ssphd.build:main",
        ],
    },
    package_data={
        'ssphd': [
            'assets/templates/*.html',
            'assets/templates/*.tex',
            'assets/css/*.css',
            'assets/js/*.js',
            'assets/fonts/**/*',
            'assets/csl/*.csl',
            'assets/meta/*.yaml',
            'default.config.yaml',
        ],
    },
    include_package_data=True,
    author="Sylvain Kern",
    author_email="TODO",
    description="A document processor for PhD thesis and academic writing",
    long_description=open("readme.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sylvain-kern/ssphd",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
