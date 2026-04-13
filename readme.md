# ssphd

Single-source conversion tool for PhD manuscripts build on top of [`pandoc`](https://pandoc.org). 

Learn more about Single-Source Publishing (SSP) [here](https://coko.foundation/articles/single-source-publishing.html).

## Output format support

| No functionality | Limited | Full           |
| ---------------- | ------- | -------------- |
| `docx`           |         | `html` `latex` |

## Getting started

### Installation

- **Pandoc**

  refer to https://github.com/jgm/pandoc/blob/main/INSTALL.md.

- **Haskell and stuff** (for pandoc filters)

  install ghcup: https://www.haskell.org/ghcup/.
  
  ```bash
  ghcup install ghc
  ghcup install cabal
  cabal v2-update
  ```

- **Pandoc filters**
  - pandoc-sidenote
    
    ```bash
    cabal v2-install pandoc-sidenote
    ```

  - pandoc-crossref

    ```bash
    cabal v2-install --install-method=copy pandoc-cli pandoc-crossref
    ```

    for Windows users, you might need to put pandoc-crossref (`C:/cabal/bin/pandoc-crossref.exe`) manually to the PATH.

- **Package**
  
    ```bash
    pip install -e .
    ```

### Usage

Create your `main.md`, using our [extended syntax of Pandoc markdown](./syntax.md).

To produce the output(s), run

- HTML output:
  ```bash
  ssphd main.md -H
  ```

- LaTeX output:
  ```bash
  ssphd main.md -L
  ```

## Roadmap

### Core features

- Refactor into a clean architecture to achieve true separation of concerns
- Make a `v0.1` first release and open the repo to contributors

### New output formats support

- `docx`

### Add functionalities

- Interactive graphs (`mpld3`, `matplotlib` jupyter widget style, `plotly`, `dygraphs`) without compromising expressiveness
- 3D objects visualization
- Dynamic unit conversion (like in [ciechanow.ski](https://ciechanow.ski) exquisite articles)
- More granular search (search over figures, graphs, data, bibliographic references)
- Multiple output formats at once (`ssphd -HL`)