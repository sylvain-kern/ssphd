---
title: Capteurs MEMS pour la mesure d'écoulements en environnements sévères
author: Sylvain Kern
lang: en
type: A PhD thesis
abstract: |
  Lorem ipsum **dolor** sit amet, *consectetur* adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim. Felis imperdiet proin fermentum leo vel orci porta non pulvinar. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Congue eu consequat ac felis donec et odio pellentesque diam. Sit amet nulla facilisi morbi tempus iaculis urna id. Eget dolor morbi non arcu risus. Nulla facilisi etiam dignissim diam quis enim lobortis. Mattis ullamcorper velit sed ullamcorper. Diam volutpat commodo sed egestas egestas fringilla phasellus. Non nisi est sit amet facilisis.
---

# Introduction

Lorem ipsum **dolor** sit amet, *consectetur* adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim. Felis imperdiet proin fermentum leo vel orci porta non pulvinar. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Congue eu consequat ac felis donec et odio pellentesque diam. Sit amet nulla facilisi morbi tempus iaculis urna id. Eget dolor morbi non arcu risus. Nulla facilisi etiam dignissim diam quis enim lobortis. Mattis ullamcorper velit sed ullamcorper. Diam volutpat commodo sed egestas egestas fringilla phasellus. Non nisi est sit amet facilisis.

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim. Felis imperdiet proin fermentum leo vel orci porta non pulvinar. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Congue eu consequat ac felis donec et odio pellentesque diam. Sit amet nulla facilisi morbi tempus iaculis urna id. Eget dolor morbi non arcu risus. Nulla facilisi etiam dignissim diam quis enim lobortis. Mattis ullamcorper velit sed ullamcorper. Diam volutpat commodo sed egestas egestas fringilla phasellus. Non nisi est sit amet facilisis. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim. Felis imperdiet proin fermentum leo vel orci porta non pulvinar. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Congue eu consequat ac felis donec et odio pellentesque diam. Sit amet nulla facilisi morbi tempus iaculis urna id. Eget dolor morbi non arcu risus. Nulla facilisi etiam dignissim diam quis enim lobortis. Mattis ullamcorper velit sed ullamcorper. Diam volutpat commodo sed egestas egestas fringilla phasellus. Non nisi est sit amet facilisis. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim. Felis imperdiet proin fermentum leo vel orci porta non pulvinar. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Congue eu consequat ac felis donec et odio pellentesque diam. Sit amet nulla facilisi morbi tempus iaculis urna id. Eget dolor morbi non arcu risus. Nulla facilisi etiam dignissim diam quis enim lobortis. Mattis ullamcorper velit sed ullamcorper. Diam volutpat commodo sed egestas egestas fringilla phasellus. Non nisi est sit amet facilisis.

# Graphics

## Graphs

### Using `mpld3`

![Test graph](_assets/graphs/test.pkl){#fig:test-graph}


### Using `pandoc-plot` and `plotly`

```{.plotly_python format="html"}
import plotly.express as px

df = px.data.gapminder().query("continent == 'Oceania'")
p = px.line(df, x='year', y='lifeExp', color='country', markers=True)

```

Works well and it really beautiful, but too slow! (and has a watermark)

Comparison with Matplotlib:

```{.matplotlib format="svg"}
import matplotlib.pyplot as plt

plt.figure()
plt.plot([0,1,2,3,4], [1,2,3,4,5])
plt.title('This is an example figure')
```

## +[SVG] images

+[SVG]: Standard Vector Graphics {.description This is a standard vector graphics standard, based on XML}

## Subfigures

With `<div>` syntax:

<div id="fig:figureRef">
![subfigure 1 caption +[SVG]](_assets/pics/usa-census.png){#fig:figureRefA}

![subfigure 2 caption](_assets/pics/usa-census.png){#fig:figureRefB}

Caption of figure
</div>

With `::: {#fig:figureRef}` syntax (and in line):

::: {#fig:figureRef2}
![subfigure 1 caption](_assets/pics/usa-census.png){#fig:figureRef2A}
![subfigure 2 caption](_assets/pics/usa-census.png){#fig:figureRef2B}

Caption of figure
:::

Grid:

:::{#fig:coolfig}
![caption a](_assets/pics/usa-census.png){#fig:cfa}
![caption b](_assets/pics/usa-census.png){#fig:cfb}
![caption c](_assets/pics/usa-census.png){#fig:cfc}

![caption d](_assets/pics/usa-census.png){#fig:cfd}
![Eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim. Felis imperdiet proin fermentum leo vel orci porta non pulvinar. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor.](_assets/pics/usa-census.png){#fig:cfe}
![caption f](_assets/pics/usa-census.png){#fig:cff}

Cool figure!
:::

Grid 2 :

:::{#fig:grid2 .wide}
![caption a](_assets/pics/usa-census.png){#fig:cfa}
![caption b](_assets/pics/usa-census.png){#fig:cfb}
![caption c](_assets/pics/usa-census.png){#fig:cfc}
![caption d](_assets/pics/usa-census.png){#fig:cfd}

![Eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim. Felis imperdiet proin fermentum leo vel orci porta non pulvinar. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor.](_assets/pics/usa-census.png){#fig:cfe}
![caption f](_assets/pics/usa-census.png){#fig:cff}
![caption g](_assets/pics/usa-census.png){#fig:cfg}

Cool figure!
:::

:::{#fig:widefig .wide}
![caption a](_assets/pics/usa-census.png){#fig:cfa}
![caption b](_assets/pics/usa-census.png){#fig:cfb}
![caption c](_assets/pics/usa-census.png){#fig:cfc}

![caption d](_assets/pics/usa-census.png){#fig:cfd}
![Eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim. Felis imperdiet proin fermentum leo vel orci porta non pulvinar. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor.](_assets/pics/usa-census.png){#fig:cfe}
![caption f](_assets/pics/usa-census.png){#fig:cff}

Wide figure!
:::

Regular figure :

![Figure caption.](_assets/pics/usa-census.png){#fig:regular}


# Cross-links with `pandoc-crossref`

Regardez la [@sec:section-after-references].

[L'équation @eq:example est assez stock]

[@Eq:example; @eq:conservation]

Regarde [l'équation de continuité @eq:conservation]

Le @tbl:example

La @fig:test-graph

Check @fig:figureRef2B

# Citations

1 nobrackets @almogThermalStabilityThin2021

1 brackets [@almogThermalStabilityThin2021]

2 brackets [@mauriceDesignMicrofabricationCharacterization2016]

3 nobrackets : this text is taken from Talbi. @talbiMicroscaleHotWire2015

Citations list [@arwatzDynamicCalibrationModeling2013; @comte-bellotHotWireAnemometry1976; @cahillThermalConductivityMeasurement1990] (not working --only with semicolons ?)

@fanLowdimensionalSiCNanostructures2006

@pisanoBridgeConceptualFrameworks2015

@ummelsStochasticMultiplayerGames2010

Notes after punctuation [@ummelsStochasticMultiplayerGames2010]. It works.


# Numbered chapter

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim. Felis imperdiet proin fermentum leo vel orci porta non pulvinar. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Congue eu consequat ac felis donec et odio pellentesque diam. Sit amet nulla facilisi morbi tempus iaculis urna id. Eget dolor morbi non arcu risus. Nulla facilisi etiam dignissim diam quis enim lobortis. Mattis ullamcorper velit sed ullamcorper. Diam volutpat commodo sed egestas egestas fringilla phasellus. Non nisi est sit amet facilisis.

## Section

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim. Felis imperdiet proin fermentum leo vel orci porta non pulvinar. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Congue eu consequat ac felis donec et odio pellentesque diam. Sit amet nulla facilisi morbi tempus iaculis urna id. Eget dolor morbi non arcu risus. Nulla facilisi etiam dignissim diam quis enim lobortis. Mattis ullamcorper velit sed ullamcorper. Diam volutpat commodo sed egestas egestas fringilla phasellus. Non nisi est sit amet facilisis. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim. Felis imperdiet proin fermentum leo vel orci porta non pulvinar. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Congue eu consequat ac felis donec et odio pellentesque diam. Sit amet nulla facilisi morbi tempus iaculis urna id. Eget dolor morbi non arcu risus. Nulla facilisi etiam dignissim diam quis enim lobortis. Mattis ullamcorper velit sed ullamcorper. Diam volutpat commodo sed egestas egestas fringilla phasellus. Non nisi est sit amet facilisis. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim. Felis imperdiet proin fermentum leo vel orci porta non pulvinar. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Congue eu consequat ac felis donec et odio pellentesque diam. Sit amet nulla facilisi morbi tempus iaculis urna id. Eget dolor morbi non arcu risus. Nulla facilisi etiam dignissim diam quis enim lobortis. Mattis ullamcorper velit sed ullamcorper. Diam volutpat commodo sed egestas egestas fringilla phasellus. Non nisi est sit amet facilisis. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim. Felis imperdiet proin fermentum leo vel orci porta non pulvinar. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Congue eu consequat ac felis donec et odio pellentesque diam. Sit amet nulla facilisi morbi tempus iaculis urna id. Eget dolor morbi non arcu risus. Nulla facilisi etiam dignissim diam quis enim lobortis. Mattis ullamcorper velit sed ullamcorper. Diam volutpat commodo sed egestas egestas fringilla phasellus. Non nisi est sit amet facilisis.

### Subsection

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim. Felis imperdiet proin fermentum leo vel orci porta non pulvinar. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Congue eu consequat ac felis donec et odio pellentesque diam. Sit amet nulla facilisi morbi tempus iaculis urna id.

#### Subsubsection

Eget dolor morbi non arcu risus. Nulla facilisi etiam dignissim diam quis enim lobortis. Mattis ullamcorper velit sed ullamcorper. Diam volutpat commodo sed egestas egestas fringilla phasellus. Non nisi est sit amet facilisis. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim. Felis imperdiet proin fermentum leo vel orci porta non pulvinar. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Congue eu consequat ac felis donec et odio pellentesque diam. Sit amet nulla facilisi morbi tempus iaculis urna id. Eget dolor morbi non arcu risus. Nulla facilisi etiam dignissim diam quis enim lobortis. Mattis ullamcorper velit sed ullamcorper. Diam volutpat commodo sed egestas egestas fringilla phasellus. Non nisi est sit amet facilisis. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim. Felis imperdiet proin fermentum leo vel orci porta non pulvinar. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Congue eu consequat ac felis donec et odio pellentesque diam. Sit amet nulla facilisi morbi tempus iaculis urna id. Eget dolor morbi non arcu risus. Nulla facilisi etiam dignissim diam quis enim lobortis. Mattis ullamcorper velit sed ullamcorper. Diam volutpat commodo sed egestas egestas fringilla phasellus. Non nisi est sit amet facilisis. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim. Felis imperdiet proin fermentum leo vel orci porta non pulvinar.

##### Level 5 heading

Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Congue eu consequat ac felis donec et odio pellentesque diam. Sit amet nulla facilisi morbi tempus iaculis urna id. Eget dolor morbi non arcu risus. Nulla facilisi etiam dignissim diam quis enim lobortis. Mattis ullamcorper velit sed ullamcorper. Diam volutpat commodo sed egestas egestas fringilla phasellus. Non nisi est sit amet facilisis.

###### Level 6 heading



## Other section

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim. Felis imperdiet proin fermentum leo vel orci porta non pulvinar. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Congue eu consequat ac felis donec et odio pellentesque diam. Sit amet nulla facilisi morbi tempus iaculis urna id. Eget dolor morbi non arcu risus. Nulla facilisi etiam dignissim diam quis enim lobortis. Mattis ullamcorper velit sed ullamcorper. Diam volutpat commodo sed egestas egestas fringilla phasellus. Non nisi est sit amet facilisis.
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim. Felis imperdiet proin fermentum leo vel orci porta non pulvinar. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Congue eu consequat ac felis donec et odio pellentesque diam. Sit amet nulla facilisi morbi tempus iaculis urna id. Eget dolor morbi non arcu risus. Nulla facilisi etiam dignissim diam quis enim lobortis. Mattis ullamcorper velit sed ullamcorper. Diam volutpat commodo sed egestas egestas fringilla phasellus. Non nisi est sit amet facilisis. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim. Felis imperdiet proin fermentum leo vel orci porta non pulvinar. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Congue eu consequat ac felis donec et odio pellentesque diam. Sit amet nulla facilisi morbi tempus iaculis urna id. Eget dolor morbi non arcu risus. Nulla facilisi etiam dignissim diam quis enim lobortis. Mattis ullamcorper velit sed ullamcorper. Diam volutpat commodo sed egestas egestas fringilla phasellus. Non nisi est sit amet facilisis.

## Math

Inline: $y = ax+b$.

$$
M=N \mu_{0} \pi \frac{\pi R_{2}^{2}}{2 R_{1}}
$$ {#eq:example}

$$
\frac{\mathrm{d}}{\mathrm{d} t} \int_V \phi \mathrm{d} V+\int_{\partial V} \phi \vec{v} \cdot \vec{n} \mathrm{~d} A=\int_V S \mathrm{~d} V
$$ {#eq:conservation}

## Tables



  Right     Left     Center     Default
-------     ------ ----------   -------
     12     12        12            12
    123     123       123          123
      1     1          1             1

Table: simple table {#tbl:example}

-------------------------------------------------------------
 Centered   Default           Right Left
  Header    Aligned         Aligned Aligned
----------- ------- --------------- -------------------------
   First    row                12.0 Example of a row that
                                    spans multiple lines.

  Second    row                 5.0 Here's another one. Note
                                    the blank line between
                                    rows.
-------------------------------------------------------------

Table: another table {#tbl:example2}


Table: Table with no header {#tbl:noheader}

----------- ------- --------------- -------------------------
   First    row                12.0 Example of a row that
                                    spans multiple lines.

  Second    row                 5.0 Here's another one. Note
                                    the blank line between
                                    rows.
----------- ------- --------------- -------------------------


: Sample grid table (this table is unnumbered (the *grid tables* extension does not work for now)).

+----------------------+-------------------------------+
|                      | Temperature 1961-1990\        |
| Location             | (°C)                          |
|                      +--------+-----------+----------+
|                      | min    | mean      | max      |
+:=====================+=======:+==========:+=========:+
| Antarctica           | -89.2  | N/A       | 19.8[^1] |
+----------------------+--------+-----------+----------+
| Earth                | -89.2  | >  list 1 | 56.7     |
+----------------------+--------+ >  list 2 +----------+
|                      | -89.2  |           | 56.7     |
+----------------------+--------+-----------+----------+
[^1]: Table footnote.

+-------------------+-------------------+
| Grid Tables       | Are Beautiful     |
+:==================+:==================+
|                   | In code and docs  |
| Easy to read      |                   |
|                   |                   |
+-------------------+-------------------+
| Exceptionally flexible and powerful   |
+-------+-------+-------+-------+-------+
| Col 1 | Col 2 | Col 3 | Col 4 | Col 5 |
+-------+-------+-------+-------+-------+

+---------------------+----------+
| Property            | Earth    |
+:============+======:+=========:+
|             | min   | -89.2 °C |
| Temperature +-------+----------+
| 1961-1990   | mean  | 14 °C    |
|             +-------+----------+
|             | max   | 56.7 °C  |
+-------------+-------+----------+

+--------------------------+
| Number alignment test\   |
| (*spoiler: it works!*)   |
+=========================:+
| 9008.68                  |
+--------------------------+
| 112.41                   |
+--------------------------+

I test a grid table in plain +[HTML] in order to see how it works with my +[CSS]!

+[CSS]: Cascading Style Sheets

<table>
<thead>
  <tr>
    <th rowspan="2">Location</th>
    <th colspan="3">Temperature 1961-1990 (°C)<br></th>
  </tr>
  <tr>
    <th>min</th>
    <th>avg</th>
    <th>max</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Antactica</td>
    <td>-89.2</td>
    <td>-</td>
    <td>19.8</td>
  </tr>
  <tr>
    <td>Earth</td>
    <td>-80.2</td>
    <td>14</td>
    <td>56.7</td>
  </tr>
</tbody>
</table>


::: {#refs}
:::

::: {#abbr}
:::

# Section after references

Lorem ipsum dolor sit amet, *consectetur* adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim. Felis imperdiet proin fermentum leo vel orci porta non pulvinar. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Congue eu consequat ac felis donec et odio pellentesque diam. Sit amet nulla facilisi morbi tempus iaculis urna id. Eget dolor morbi non arcu risus. Nulla facilisi etiam dignissim diam quis enim lobortis. Mattis ullamcorper velit sed ullamcorper. Diam volutpat commodo sed egestas egestas fringilla phasellus. Non nisi est sit amet facilisis.



# Abbreviations

Ok, so this is +[HTML].

Ok, so this is HTML.

+[MD]: MarkDown

## Test (in titles ? Yes, and even in +[TOC] !)

La filière +[MEMS] est active depuis les années 1970, notamment avec les développement technologiques associés
aux économies d'échelle de l'industrie des semiconducteurs.
En particulier, le travail de @arwatzDevelopmentCharacterizationNanoscale2015, avec le +[T-NSTAP], a permis de montrer...

Comparaison avec une footnote.[^T-NSTAP]

Comparaison avec un lien : +[HTML] [HTML](#){.relative-link}

+[T-NSTAP]:
  Temperature Nano-Scale Thermal Anemometer Probe.
  Ceci est une description un peu plus complexe, qui tient sur plusieurs lignes.
  En effet...

[^T-NSTAP]:
  Temperature Nano-Scale Thermal Anemometer Probe.
  Ceci est une description un peu plus complexe, qui tient sur plusieurs lignes.
  En effet...

+[TOC]: Table Of Contents!

+[MEMS]: Micro Electro-Mechanical Systems

Extreme cases: abbr with only one letter +[C]. Minuscule ? +[Laser].

+[Laser]: Light Amplification by Stimulated Emission of Radiation

+[C]: Follows B.

+[JSON] this is not defined, so not parsed by the filter.

+[Sylvain] nice underlining style with descenders.

+[Sylvain]: That's me!

Can I illustrate with code ?

[Links](https://www.youtube.com/watch?v=OvAbJClwZyo&t) still get right.

```markdown
**it works !**

Extreme cases: abbr with only one letter +[C]. Minuscule ? +[Laser].

+[Laser]: Light Amplification by Stimulated Emission of Radiation

+[C]: Follows B.

+[JSON] this is not defined, so not parsed by HTML.

[Links](https://www.youtube.com/watch?v=OvAbJClwZyo&t) do still get right.

```



**PROBLEMS:**

- deletes character just after it: +[MEMS]. **OK!**
- does not work if in the same line of text (conflicts with italics) Test +[MD] -> +[HTML]. **Fixed!**
- need to delete the acronym definitions. **OK!**
- acronym list ?
- Use case +[HTML]~: i want to get this in the main text. I want an unbreakable space here between `]` and `:`.

+[HTML]: Hypertext Markup Language

### This is a sub-section

# And a chapter

### And a level 3 section {-}

## And a level 2 section

## Markdown **formatting** in *section-headings*

# What if two headings have the same title ?

See @sec:this-is-a-title-1

## This is a title

## This is a title

# Lists


`\listoffigures` is not satisfactory. I want

```markdown
::: {#lof}
:::
```

::: {#lof}
:::


<!-- hack to split raw blocks -->
