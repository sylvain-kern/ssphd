# ssphd's syntax

It is a superset of [pandoc's markdown](https://pandoc.org/MANUAL.html#pandocs-markdown), with added expressiveness needed for more complex documents.

## Figure attributes

Figures like

```markdown
![Caption of the figure.](./foo.jpg){#fig:foo}
```

can have two additional class attributes:

- `.margin`: to indicate a smaller figure placed in the margin.
- `.wide`: to indicate a wide figure, which will take all available width.

Example:

```markdown
![Caption of the figure.](./foo.jpg){#fig:foo .margin}
```

## Acronyms

Acronyms's syntax is similar to footnotes. To declare an acronym, use this line surrounded by blank lines:

```markdown
+[NASA]: National Aeronautics and Space Administration
```

It is used like this, anywhere in the document:


```markdown
Project Apollo was the United States human spaceflight program led by +[NASA].
```

This will produce a tooltip in the web output and a glossary entry in the LaTeX output.