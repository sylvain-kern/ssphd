# Markdown Kitchen Sink
This file is https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet plus a few fixes and additions. Used by [obedm503/bootmark](https://github.com/obedm503/bootmark) to [demonstrate](https://obedm503.github.io/bootmark/docs/markdown-cheatsheet.html) it's styling features.

This is intended as a quick reference and showcase. For more complete info, see [John Gruber's original spec](http://daringfireball.net/projects/markdown/) and the [Github-flavored Markdown info page](http://github.github.com/github-flavored-markdown/).

Note that there is also a [Cheatsheet specific to Markdown Here](./Markdown-Here-Cheatsheet) if that's what you're looking for. You can also check out [more Markdown tools](./Other-Markdown-Tools).

##### Table of Contents
[Headers](#headers)
[Emphasis](#emphasis)
[Lists](#lists)
[Links](#links)
[Images](#images)
[Code and Syntax Highlighting](#code)
[Tables](#tables)
[Blockquotes](#blockquotes)
[Inline HTML](#html)
[Horizontal Rule](#hr)
[Line Breaks](#lines)
[YouTube Videos](#videos)

<a name="headers"></a>

## Headers

```no-highlight
# H1
## H2
### H3
#### H4
##### H5
###### H6

Alternatively, for H1 and H2, an underline-ish style:

Alt-H1
======

Alt-H2
------
```

# H1
## H2
### H3
#### H4
##### H5
###### H6

Alternatively, for H1 and H2, an underline-ish style:

Alt-H1
======

Alt-H2
------

<a name="emphasis"></a>

## Emphasis

```no-highlight
Emphasis, aka italics, with *asterisks* or _underscores_.

Strong emphasis, aka bold, with **asterisks** or __underscores__.

Combined emphasis with **asterisks and _underscores_**.

Strikethrough uses two tildes. ~~Scratch this.~~
```

Emphasis, aka italics, with *asterisks* or _underscores_.

Strong emphasis, aka bold, with **asterisks** or __underscores__.

Combined emphasis with **asterisks and _underscores_**.

Strikethrough uses two tildes. ~~Scratch this.~~


<a name="lists"></a>

## Lists

(In this example, leading and trailing spaces are shown with with dots: ⋅)

```no-highlight
1. First ordered list item
2. Another item
⋅⋅* Unordered sub-list.
1. Actual numbers don't matter, just that it's a number
⋅⋅1. Ordered sub-list
4. And another item.

⋅⋅⋅You can have properly indented paragraphs within list items. Notice the blank line above, and the leading spaces (at least one, but we'll use three here to also align the raw Markdown).

⋅⋅⋅To have a line break without a paragraph, you will need to use two trailing spaces.⋅⋅
⋅⋅⋅Note that this line is separate, but within the same paragraph.⋅⋅
⋅⋅⋅(This is contrary to the typical GFM line break behaviour, where trailing spaces are not required.)

* Unordered list can use asterisks
- Or minuses
+ Or pluses
```

1. First ordered list item
2. Another item
  * Unordered sub-list.
1. Actual numbers don't matter, just that it's a number
  1. Ordered sub-list
4. And another item.

   You can have properly indented paragraphs within list items. Notice the blank line above, and the leading spaces (at least one, but we'll use three here to also align the raw Markdown).

   To have a line break without a paragraph, you will need to use two trailing spaces.
   Note that this line is separate, but within the same paragraph.
   (This is contrary to the typical GFM line break behaviour, where trailing spaces are not required.)

* Unordered list can use asterisks
- Or minuses
+ Or pluses

<a name="links"></a>

## Links

There are two ways to create links.

```no-highlight
[I'm an inline-style link](https://www.google.com)

[I'm an inline-style link with title](https://www.google.com "Google's Homepage")

[I'm a reference-style link][Arbitrary case-insensitive reference text]

[I'm a relative reference to a repository file](../blob/master/LICENSE)

[You can use numbers for reference-style link definitions][1]

Or leave it empty and use the [link text itself].

URLs and URLs in angle brackets will automatically get turned into links.
http://www.example.com or <http://www.example.com> and sometimes
example.com (but not on Github, for example).

Some text to show that the reference links can follow later.

[arbitrary case-insensitive reference text]: https://www.mozilla.org
[1]: http://slashdot.org
[link text itself]: http://www.reddit.com
```

[I'm an inline-style link](https://www.google.com)

[I'm an inline-style link with title](https://www.google.com "Google's Homepage")

[I'm a reference-style link][Arbitrary case-insensitive reference text]

[I'm a relative reference to a repository file](../blob/master/LICENSE)

[You can use numbers for reference-style link definitions][1]

Or leave it empty and use the [link text itself].

URLs and URLs in angle brackets will automatically get turned into links.
http://www.example.com or <http://www.example.com> and sometimes
example.com (but not on Github, for example).

Some text to show that the reference links can follow later.

[arbitrary case-insensitive reference text]: https://www.mozilla.org
[1]: http://slashdot.org
[link text itself]: http://www.reddit.com

<a name="images"></a>

## Images

```no-highlight
Here's our logo (hover to see the title text):

Inline-style:
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

Reference-style:
![alt text][logo]

[logo]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"
```

Here's our logo (hover to see the title text):

Inline-style:
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

Reference-style:
![alt text][logo]

[logo]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"

<a name="code"></a>

## Code and Syntax Highlighting

Code blocks are part of the Markdown spec, but syntax highlighting isn't. However, many renderers -- like Github's and *Markdown Here* -- support syntax highlighting. Which languages are supported and how those language names should be written will vary from renderer to renderer. *Markdown Here* supports highlighting for dozens of languages (and not-really-languages, like diffs and HTTP headers); to see the complete list, and how to write the language names, see the [highlight.js demo page](http://softwaremaniacs.org/media/soft/highlight/test.html).

```no-highlight
Inline `code` has `back-ticks around` it.
```

Inline `code` has `back-ticks around` it.

Blocks of code are either fenced by lines with three back-ticks <code>```</code>, or are indented with four spaces. I recommend only using the fenced code blocks -- they're easier and only they support syntax highlighting.

<pre lang="no-highlight"><code>```javascript
var s = "JavaScript syntax highlighting";
alert(s);
```

```python
s = "Python syntax highlighting"
print s
```

```
No language indicated, so no syntax highlighting.
But let's throw in a &lt;b&gt;tag&lt;/b&gt;.
```
</code></pre>



```javascript
var s = "JavaScript syntax highlighting";
alert(s);
```

```python
s = "Python syntax highlighting"
print s
```

```
No language indicated, so no syntax highlighting in Markdown Here (varies on Github).
But let's throw in a <b>tag</b>.
```


<a name="tables"></a>

## Tables

Tables aren't part of the core Markdown spec, but they are part of GFM and *Markdown Here* supports them. They are an easy way of adding tables to your email -- a task that would otherwise require copy-pasting from another application.

```no-highlight
Colons can be used to align columns.

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

There must be at least 3 dashes separating each header cell.
The outer pipes (|) are optional, and you don't need to make the
raw Markdown line up prettily. You can also use inline Markdown.

Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3
```

Colons can be used to align columns.

| Tables        | Are           | Cool |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

There must be at least 3 dashes separating each header cell. The outer pipes (|) are optional, and you don't need to make the raw Markdown line up prettily. You can also use inline Markdown.

Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3

<a name="blockquotes"></a>

## Blockquotes

```no-highlight
> Blockquotes are very handy in email to emulate reply text.
> This line is part of the same quote.

Quote break.

> This is a very long line that will still be quoted properly when it wraps. Oh boy let's keep writing to make sure this is long enough to actually wrap for everyone. Oh, you can *put* **Markdown** into a blockquote.
```

> Blockquotes are very handy in email to emulate reply text.
> This line is part of the same quote.

Quote break.

> This is a very long line that will still be quoted properly when it wraps. Oh boy let's keep writing to make sure this is long enough to actually wrap for everyone. Oh, you can *put* **Markdown** into a blockquote.

<a name="html"></a>

## Inline HTML

You can also use raw HTML in your Markdown, and it'll mostly work pretty well.

```no-highlight
<dl>
  <dt>Definition list</dt>
  <dd>Is something people use sometimes.</dd>

  <dt>Markdown in HTML</dt>
  <dd>Does *not* work **very** well. Use HTML <em>tags</em>.</dd>
</dl>
```

<dl>
  <dt>Definition list</dt>
  <dd>Is something people use sometimes.</dd>

  <dt>Markdown in HTML</dt>
  <dd>Does *not* work **very** well. Use HTML <em>tags</em>.</dd>
</dl>

<a name="hr"></a>

## Horizontal Rule

```
Three or more...

---

Hyphens

***

Asterisks

___

Underscores
```

Three or more...

---

Hyphens

***

Asterisks

___

Underscores

<a name="lines"></a>

## Line Breaks

My basic recommendation for learning how line breaks work is to experiment and discover -- hit &lt;Enter&gt; once (i.e., insert one newline), then hit it twice (i.e., insert two newlines), see what happens. You'll soon learn to get what you want. "Markdown Toggle" is your friend.

Here are some things to try out:

```
Here's a line for us to start with.

This line is separated from the one above by two newlines, so it will be a *separate paragraph*.

This line is also a separate paragraph, but...
This line is only separated by a single newline, so it's a separate line in the *same paragraph*.
```

Here's a line for us to start with.

This line is separated from the one above by two newlines, so it will be a *separate paragraph*.

This line is also begins a separate paragraph, but...
This line is only separated by a single newline, so it's a separate line in the *same paragraph*.

(Technical note: *Markdown Here* uses GFM line breaks, so there's no need to use MD's two-space line breaks.)

<a name="videos"></a>

## YouTube Videos

They can't be added directly but you can add an image with a link to the video like this:

```no-highlight
<a href="http://www.youtube.com/watch?feature=player_embedded&v=YOUTUBE_VIDEO_ID_HERE
" target="_blank"><img src="http://img.youtube.com/vi/YOUTUBE_VIDEO_ID_HERE/0.jpg"
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>
```

Or, in pure Markdown, but losing the image sizing and border:

```no-highlight
[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/YOUTUBE_VIDEO_ID_HERE/0.jpg)](http://www.youtube.com/watch?v=YOUTUBE_VIDEO_ID_HERE)
```

# Abstract {-}

At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facZilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.

# Acknowledgements {-}

My man

The family

The hood

# H1: chapter title

### header {-}

## All headings (this is level two)

### Level three

#### Level four

##### Level five (unnumbered) {-}

###### Level six

## Harmony & counterpoint (paragraph flow & balance)

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eget lorem dolor sed viverra ipsum nunc aliquet bibendum enim. Felis imperdiet proin fermentum leo vel orci porta non pulvinar. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Congue eu consequat ac felis donec et odio pellentesque diam. Sit amet nulla facilisi morbi tempus iaculis urna id. Eget dolor morbi non arcu risus. Nulla facilisi etiam dignissim diam quis enim lobortis. Mattis ullamcorper velit sed ullamcorper. Diam volutpat commodo sed egestas egestas fringilla phasellus. Non nisi est sit amet facilisis.

Aliquet nibh praesent tristique magna sit. Ullamcorper a lacus vestibulum sed arcu non. Sed risus pretium quam vulputate. In aliquam sem fringilla ut. Volutpat blandit aliquam etiam erat velit scelerisque in dictum non. Nec ultrices dui sapien eget mi. Massa placerat duis ultricies lacus sed turpis. Nulla facilisi etiam dignissim diam quis enim lobortis scelerisque. Tempus iaculis urna id volutpat lacus. Nulla facilisi cras fermentum odio eu.

Dignissim diam quis enim lobortis scelerisque fermentum dui faucibus. Diam quam nulla porttitor massa id. Ultrices mi tempus imperdiet nulla malesuada pellentesque. Quam lacus suspendisse faucibus interdum posuere lorem ipsum. Lorem dolor sed viverra ipsum nunc aliquet bibendum enim facilisis. Blandit cursus risus at ultrices mi. Justo laoreet sit amet cursus sit amet. Senectus et netus et malesuada fames ac. Faucibus scelerisque eleifend donec pretium vulputate. Rutrum quisque non tellus orci ac auctor augue. Mi tempus imperdiet nulla malesuada pellentesque elit eget gravida. Praesent tristique magna sit amet purus gravida quis blandit.

Amet purus gravida quis blandit. Tincidunt dui ut ornare lectus sit amet. Duis ultricies lacus sed turpis tincidunt id aliquet risus feugiat. Tortor vitae purus faucibus ornare suspendisse sed nisi lacus sed. Fringilla ut morbi tincidunt augue interdum. Id diam maecenas ultricies mi eget mauris pharetra et. Pellentesque nec nam aliquam sem et. Eleifend mi in nulla posuere. Et netus et malesuada fames ac turpis egestas. Platea dictumst vestibulum rhoncus est pellentesque elit ullamcorper. Quis risus sed vulputate odio ut.

Urna neque viverra justo nec ultrices. Pulvinar proin gravida hendrerit lectus a. Velit ut tortor pretium viverra suspendisse potenti nullam. Eget gravida cum sociis natoque penatibus et. Aliquet sagittis id consectetur purus ut. Sagittis eu volutpat odio facilisis mauris. Eget dolor morbi non arcu. Eget velit aliquet sagittis id consectetur purus ut faucibus. Urna porttitor rhoncus dolor purus non enim praesent elementum. Senectus et netus et malesuada fames ac turpis egestas.

Tempus iaculis urna id volutpat lacus laoreet. Senectus et netus et malesuada fames ac turpis egestas maecenas. Nisi est sit amet facilisis magna etiam tempor orci eu. Nibh praesent tristique magna sit amet. Eget egestas purus viverra accumsan in nisl. Ullamcorper eget nulla facilisi etiam dignissim diam quis. Ipsum suspendisse ultrices gravida dictum. Pellentesque dignissim enim sit amet venenatis urna cursus eget. Nec tincidunt praesent semper feugiat. Elementum nisi quis eleifend quam adipiscing. Sed risus pretium quam vulputate dignissim suspendisse in est ante. Massa ultricies mi quis hendrerit dolor magna eget est lorem. Condimentum lacinia quis vel eros donec ac odio tempor orci. Sagittis purus sit amet volutpat consequat mauris. Interdum consectetur libero id faucibus nisl tincidunt eget. Feugiat nibh sed pulvinar proin gravida hendrerit. Congue eu consequat ac felis donec et odio. Bibendum arcu vitae elementum curabitur vitae. Elit scelerisque mauris pellentesque pulvinar pellentesque habitant morbi tristique.

Eleifend donec pretium vulputate sapien nec. Nunc sed id semper risus in hendrerit gravida. A diam maecenas sed enim ut. Tempor orci dapibus ultrices in iaculis nunc sed augue. At consectetur lorem donec massa sapien faucibus et molestie ac. Natoque penatibus et magnis dis parturient montes. Tellus in hac habitasse platea dictumst vestibulum rhoncus. Risus viverra adipiscing at in tellus. Dignissim sodales ut eu sem integer vitae justo eget. Metus aliquam eleifend mi in nulla posuere. Turpis nunc eget lorem dolor sed viverra ipsum. Sed velit dignissim sodales ut eu sem. Vitae purus faucibus ornare suspendisse sed nisi. Id ornare arcu odio ut sem. Ut venenatis tellus in metus vulputate eu scelerisque felis. Cursus metus aliquam eleifend mi in. Donec adipiscing tristique risus nec feugiat. Nibh nisl condimentum id venenatis a condimentum vitae sapien pellentesque.

Cras fermentum odio eu feugiat pretium. Sed id semper risus in hendrerit gravida. Dolor sed viverra ipsum nunc. Non blandit massa enim nec dui nunc mattis. Nunc consequat interdum varius sit amet mattis. Vulputate dignissim suspendisse in est ante in nibh. Habitant morbi tristique senectus et netus et malesuada. Venenatis lectus magna fringilla urna porttitor rhoncus. Lobortis elementum nibh tellus molestie nunc non blandit massa enim. Volutpat lacus laoreet non curabitur gravida arcu ac. Amet consectetur adipiscing elit pellentesque habitant. Sed tempus urna et pharetra pharetra. Quam pellentesque nec nam aliquam. Id velit ut tortor pretium viverra suspendisse potenti nullam ac.

### Line length test

azertyuiopqsdfghjklmwxcvbnazertyuiopqsdfghjklmwxcvbnazertyuiopqsdfghjklmwxcvbnazertyuiopqsdfghjklmwxcvbn

## Unnumbered section {-}

Eleifend donec pretium vulputate sapien nec. Nunc sed id semper risus in hendrerit gravida. A diam maecenas sed enim ut. Tempor orci dapibus ultrices in iaculis nunc sed augue. At consectetur lorem donec massa sapien faucibus et molestie ac. Natoque penatibus et magnis dis parturient montes. Tellus in hac habitasse platea dictumst vestibulum rhoncus. Risus viverra adipiscing at in tellus. Dignissim sodales ut eu sem integer vitae justo eget. Metus aliquam eleifend mi in nulla posuere. Turpis nunc eget lorem dolor sed viverra ipsum. Sed velit dignissim sodales ut eu sem. Vitae purus faucibus ornare suspendisse sed nisi. Id ornare arcu odio ut sem. Ut venenatis tellus in metus vulputate eu scelerisque felis. Cursus metus aliquam eleifend mi in. Donec adipiscing tristique risus nec feugiat. Nibh nisl condimentum id venenatis a condimentum vitae sapien pellentesque.

Cras fermentum odio eu feugiat pretium. Sed id semper risus in hendrerit gravida. Dolor sed viverra ipsum nunc. Non blandit massa enim nec dui nunc mattis. Nunc consequat interdum varius sit amet mattis. Vulputate dignissim suspendisse in est ante in nibh. Habitant morbi tristique senectus et netus et malesuada. Venenatis lectus magna fringilla urna porttitor rhoncus. Lobortis elementum nibh tellus molestie nunc non blandit massa enim. Volutpat lacus laoreet non curabitur gravida arcu ac. Amet consectetur adipiscing elit pellentesque habitant. Sed tempus urna et pharetra pharetra. Quam pellentesque nec nam aliquam. Id velit ut tortor pretium viverra suspendisse potenti nullam ac.

## Markdown features

Lorem markdownum Niobe, in quae peracta, matrem ubi vates, blanditiis? **Dabitur
omnia aper** cacumina sensisse in idque passim datum, lupis terrent Aurora Maia.

```java
association_ascii_domain(hoverHibernateMatrix);
left_memory(design, ideReciprocalAtm);
var kilohertzHost = type_requirements_slashdot;
```

Aestus virgo cur languore **laudamus doluisse** tempora canis, ausorum habent ab
quoque dextra. Cum fecissem excussit patriosque quodque, et etiam subtemen
**quoque**, papyriferi ululasse, erat arida ab maerentes: Lichan.

> Inspiratque undas; feroxque seges graviore, tradidit et umero mandere: exuere
> atram magis *auctor excita*, o. Virque in in [discedentem haec
> deceptus](http://www.numferens.io/) nec inconcessaeque perosus flammas
> exarsit.

### Tectis praemonuisse plura

Dixerat hoc turbida mento nostri dolet fessos. Arcu sedit dumque. Amor campus
posco. Dilapsa est aquarum coimus cecidit et classis nos, regia nec erat lavit
undis ratis demugitaeque laetaque.

- Parente dixit
- Marem vix virides nihil cornua navis vultus
- Si non
- Fixit quas dilapsum iunctum imitata satis

Par armat fuit nomen in Aegides lingua colatur, non humani, anser ab **sibi**
Munychiosque *summa*. Dixit Mavortis auratum se frequens haerenti exosae: quam
et aequore, tuli ira omnis Neptunus florentia calido tacti.

1. Flammas trepidosque variabant terrae nisi ablatum cessit
2. Cinyra Herculeos in Pelasgi vultu adfixa
3. Telamonius adhuc questuque non Erysicthone deus permulcet
4. Quem mentisque

Quodsi rosarum gaudere quoque frigore timido cognoverat, insurgere esse: septem.
Ianigenam in **vestros** mihi tot fecit, qui freta conferat, **penates** nomen
quo Telamon fenestris, duae. Relinquitur voce graviore, me **puto**, discedit in
sumpta corpore.

Rule:

---

Quodsi rosarum gaudere quoque frigore timido cognoverat, insurgere esse: septem.
Ianigenam in **vestros** mihi tot fecit, qui freta conferat, **penates** nomen
quo Telamon fenestris, duae. Relinquitur voce graviore, me **puto**, discedit in
sumpta corpore.

Wide rule:

:::wide

---

:::

Quodsi rosarum gaudere quoque frigore timido cognoverat, insurgere esse: septem.
Ianigenam in **vestros** mihi tot fecit, qui freta conferat, **penates** nomen
quo Telamon fenestris, duae. Relinquitur voce graviore, me **puto**, discedit in
sumpta corpore.


## Notes

For example this is a side note[^example-side-note]. Side notes
are numbered, and the number shows at the anchor point in the
body text at all screen widths.

[^example-side-note]:
  This is the text in the side note. It is smaller and only
  supports inline elements, like **bold** or [links](#),
  but not lists or code blocks.

On the other hand, margin notes are not numbered. Instead,
they hang to the left and are only vaguely connected to the
text, like this.[^example-margin-note]

[^example-margin-note]:
  {-} `pandoc-sidenote` detects margin notes when the note
  starts with the text `{-}`. This is inspired by the syntax
  Pandoc uses for unnumbered headings.

### Side note symbols

[^note1] [^note2] [^note3] [^note4] [^note5] [^note6] [^note7] [^note8] [^note9] [^note10] [^note11] [^note12]

  [^note1]:
    this is a note.

  [^note2]:
    this is a note.

  [^note3]:
    this is a note.

  [^note4]:
    this is a note.

  [^note5]:
    this is a note.

  [^note6]:
    this is a note.

  [^note7]:
    this is a note.

  [^note8]:
    this is a note.

  [^note9]:
    this is a note.

  [^note10]:
    this is a note.

  [^note11]:
    this is a note.

  [^note12]:
    this is a note.


## Wide content

:::wide
Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam.
Postquam superi desiluit, flentibus posuerunt ferum! Fratremque derepta habet
aquarum. Lacertis horrentia Mavortius sanguineae silentia, num Caesarea mollia
candidus. Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam.
:::

:::wide
```zsh
> zsh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```
:::

## Pictures

A reference to the [image](#fig:label1), and another [reference](#fig:label2).

![Caption](_assets/pics/usa-census.png "This is a map of the USA census!"){#fig:label1}

![This is a second image](_assets/pics/usa-census.png){.wide #fig:label2}

![This is a reduced image](_assets/pics/usa-census.png){#fig:label3 width=50%}

![This is (meant to be) a margin image](_assets/pics/usa-census.png){.margin #fig:label}

See [@fig:label1;@fig:label2]

@Fig:label1.


### Subfigures ?

<div id="fig:figureRef">
![subfigure 1 caption](image1.png){#fig:figureRefA}

![subfigure 2 caption](image2.png){#fig:figureRefB}

Caption of figure
</div>


### Uncaptioned

![](_assets/pics/usa-census.png)

## Tables

Text before. I can reference the following table with its label : see @tbl:label3.

| Header 1       |   Header 2   | Header 3 |
| -------------- | :----------: | -------: |
| **bold style** | `code block` |     3.73 |
| \|escape pipe  |  \`backtick  |   220.34 |

Table: Caption of table. {#tbl:label3}

Text after. Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam.
Postquam superi desiluit, flentibus posuerunt ferum! Fratremque derepta habet
aquarum. Lacertis horrentia Mavortius sanguineae silentia, num Caesarea mollia
candidus. Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam.

### Wide table test

Check the stats @tbl:label4.

:::wide
| Mois                             | jan.  | fév.  | mars  | avril | mai   | juin  | jui.  | août  | sep.  | oct. | nov.  | déc.  | année  |
| -------------------------------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ---- | ----- | ----- | ------ |
| Temp. minimale moyenne (°C)      | −0.8  | −0.6  | 2.5   | 5.2   | 9.8   | 12.8  | 14.5  | 14.1  | 10.6  | 7.1  | 2.8   | 0.3   | 6.6    |
| Temp. moyenne (°C)               | 1.9   | 2.9   | 7     | 10.5  | 15    | 18.1  | 20.1  | 19.8  | 15.8  | 11.2 | 5.8   | 2.8   | 10.9   |
| Temp. maximale moyenne (°C)      | 4.5   | 6.4   | 11.1  | 15.7  | 20.2  | 23.4  | 25.7  | 25.4  | 21    | 15.3 | 8.8   | 5.2   | 15.3   |
| Record de froid (°C)             | −23.6 | −22.3 | −16.7 | −5.6  | −2.4  | 1.1   | 4.9   | 4.8   | −1.3  | −7.6 | −10.8 | −23.4 | −23.6  |
| Record de chaleur (°C)           | 17.5  | 21.1  | 25.7  | 30    | 33.8  | 38.8  | 38.9  | 38.7  | 33.4  | 29.1 | 22.1  | 18.3  | 38.9   |
| Nb. de jours avec gel            | 16.4  | 15.1  | 9     | 2.2   | 0.1   | 0     | 0     | 0     | 0     | 1.7  | 7.5   | 13.8  | 65.8   |
| Ensoleillement (h)               | 58.1  | 83.8  | 134.8 | 180   | 202.5 | 223.8 | 228.6 | 219.6 | 164.5 | 98.7 | 55.3  | 43.1  | 1692.7 |
| Précipitations (mm)              | 32.2  | 34.5  | 42.8  | 45.9  | 81.9  | 71.6  | 72.7  | 61.4  | 63.5  | 61.5 | 47    | 50    | 664.6  |
| Nb. de jours avec précipitations | 8.4   | 8.1   | 9.1   | 9.2   | 11.5  | 10.8  | 9.9   | 10.2  | 8.6   | 9.5  | 9.3   | 9.8   | 114.9  |
| Humidité relative (%)            | 86    | 82    | 76    | 72    | 73    | 74    | 72    | 76    | 80    | 85   | 86    | 86    | 79     |
| Nb. de jours avec neige          | 7.8   | 6.7   | 4     | 1.5   | 0.1   | 0     | 0     | 0     | 0     | 0    | 3.4   | 6.3   | 29.8   |
| Nb. de jours d'orage             | 0.1   | 0.2   | 0.5   | 1.5   | 5     | 6.1   | 6.2   | 5.5   | 2.7   | 0.5  | 0.2   | 0.2   | 28.7   |
| Nb. de jours avec brouillard     | 9.1   | 5.7   | 3.4   | 1.9   | 2     | 1.4   | 1     | 2.6   | 6.7   | 12.4 | 10    | 8.8   | 65     |

Table: La météo. {#tbl:label4}
:::

### Merge cells ?

| a   | b   |
| --- | --- |
| 1   | 2   |
| ^   | 4   |

Nope.

### Margin tables ?

:::margin

| Header 1       |   Header 2   | Header 3 |
| -------------- | :----------: | -------: |
| **bold style** | `code block` |     3.73 |
| \|escape pipe  |  \`backtick  |   220.34 |

Table: Margin table test. {#tbl:margin}

:::

Yeah baby

## Code

```c
int main() {
  printf("Hello world!");
  return 0;
}
```

Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam.
Postquam superi desiluit, flentibus posuerunt ferum! Fratremque derepta habet
aquarum. Lacertis horrentia Mavortius sanguineae silentia, num Caesarea mollia
candidus. Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam.

```css
@media (max-width: 1350px) {

  header, main, footer {
    width: 50%;
  }

  .sidenote,
  .marginnote,
  figcaption {
    margin-right: -55%;
    width: 50%;
  }

  .wide {
    width: 155%;
  }

}

/* intermédiaire : le main text est collé à gauche (burger ?) mais quand même les sidenotes */
@media (max-width: 1000px) {

  header, main, footer {
    margin-left: 20pt;
    width: 65%;
    margin-right: auto;
  }

  .sidenote, .marginnote, figcaption {
    margin-right: -45%;
    width: 40%;
  }

  .wide {
    width: 145%;
  }

}
```

Python:

```python
def factorial(n):
        return int(n==0) or n*factorial(n-1)
```

Wide code:

:::wide
```zsh
> zsh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```
:::

## Math

Inline : $y = ax + b$. Block:

$$
e^{i\pi}+1 = 0
$$

Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam.
Postquam superi desiluit, flentibus posuerunt ferum! Fratremque derepta habet
aquarum. Lacertis horrentia Mavortius sanguineae silentia, num Caesarea mollia
candidus. Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. This is inline in the flow: $e^x = \frac{\sum_{n = 0}^{\infty} \frac{x^n}{n!}}{\sum_{n = 0}^{\infty}0}$. Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam.
Postquam superi desiluit, flentibus posuerunt ferum! Fratremque derepta habet
aquarum. Lacertis horrentia Mavortius sanguineae silentia, num Caesarea mollia
candidus.

Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. Postquam superi desiluit, flentibus posuerunt ferum! Fratremque derepta habet aquarum. Lacertis horrentia Mavortius sanguineae silentia, num Caesarea mollia candidus. Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. This is inline in the flow: ex=∑n=0∞xnn!∑n=0∞0ex=∑n=0∞​0∑n=0∞​n!xn​​. Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. Postquam superi desiluit, flentibus posuerunt ferum! Fratremque derepta habet aquarum. Lacertis horrentia Mavortius sanguineae silentia, num Caesarea mollia candidus.

Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. Postquam superi desiluit, flentibus posuerunt ferum! Fratremque derepta habet aquarum. Lacertis horrentia Mavortius sanguineae silentia, num Caesarea mollia candidus. Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. This is inline in the flow: ex=∑n=0∞xnn!∑n=0∞0ex=∑n=0∞​0∑n=0∞​n!xn​​. Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. Postquam superi desiluit, flentibus posuerunt ferum! Fratremque derepta habet aquarum. Lacertis horrentia Mavortius sanguineae silentia, num Caesarea mollia candidus.

Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. Postquam superi desiluit, flentibus posuerunt ferum! Fratremque derepta habet aquarum. Lacertis horrentia Mavortius sanguineae silentia, num Caesarea mollia candidus. Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. This is inline in the flow: ex=∑n=0∞xnn!∑n=0∞0ex=∑n=0∞​0∑n=0∞​n!xn​​. Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. Postquam superi desiluit, flentibus posuerunt ferum! Fratremque derepta habet aquarum. Lacertis horrentia Mavortius sanguineae silentia, num Caesarea mollia candidus.

Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. Postquam superi desiluit, flentibus posuerunt ferum! Fratremque derepta habet aquarum. Lacertis horrentia Mavortius sanguineae silentia, num Caesarea mollia candidus. Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. This is inline in the flow: ex=∑n=0∞xnn!∑n=0∞0ex=∑n=0∞​0∑n=0∞​n!xn​​. Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. Postquam superi desiluit, flentibus posuerunt ferum! Fratremque derepta habet aquarum. Lacertis horrentia Mavortius sanguineae silentia, num Caesarea mollia candidus.

$$
e^x = \sum_{n = 0}^{\infty} \frac{x^n}{n!}.
$$

$$
\tau_\text w(\omega)=-\frac{1}{c} \sqrt{j \omega \nu} \tanh \left(a \sqrt{\frac{j \omega}{\nu}}\right) \frac{e^{j k d_s}-R e^{-j k d_s}}{1+R} p^{\prime} e^{j \omega t}
$$

### Chonky formulae

:::wide
$$
\frac{J_{p}^{\text {diff }}(X n)}{J_{g}(X n)}=\frac{\frac{\alpha L n}{(\alpha L n+1)} e^{-\alpha X n}}{\left(e^{-\alpha X n}-1\right)}=\frac{\frac{50000 * 0,0001}{50000 * 0,0001+1} e^{-50000 * 0,0001}}{\left(e^{-500000000001}-1\right)}=-1,6 * 10^{-22} \ll 1
$$
:::

### Labelled

Here's a reference to @eq:description:

$$
M=N \mu_{0} \pi \frac{\pi R_{2}^{2}}{2 R_{1}}
$$ {#eq:description}

### Margin math ?

Math displayed in the margin!

:::margin
$$
e^{i\pi}+1 = 0
$$ {#eq:margin}

Yeah baby!
:::

### Math in note

For example this is a side note[^example-side-note2]. Side notes
are numbered, and the number shows at the anchor point in the
body text at all screen widths.

[^example-side-note2]:
  This is the text in the side note. It is smaller and only
  supports inline elements, like **bold** or [links](#),
  or math: $e^{i\pi} +1 = 0$ !

Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. Postquam superi desiluit, flentibus posuerunt ferum! Fratremque derepta habet aquarum. Lacertis horrentia Mavortius sanguineae silentia, num Caesarea mollia candidus. Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. This is inline in the flow: ex=∑n=0∞xnn!∑n=0∞0ex=∑n=0∞​0∑n=0∞​n!xn​​. Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. Postquam superi desiluit, flentibus posuerunt ferum! Fratremque derepta habet aquarum. Lacertis horrentia Mavortius sanguineae silentia, num Caesarea mollia candidus.

Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. Postquam superi desiluit, flentibus posuerunt ferum! Fratremque derepta habet aquarum. Lacertis horrentia Mavortius sanguineae silentia, num Caesarea mollia candidus. Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. This is inline in the flow: ex=∑n=0∞xnn!∑n=0∞0ex=∑n=0∞​0∑n=0∞​n!xn​​. Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. Postquam superi desiluit, flentibus posuerunt ferum! Fratremque derepta habet aquarum. Lacertis horrentia Mavortius sanguineae silentia, num Caesarea mollia candidus.

Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. Postquam superi desiluit, flentibus posuerunt ferum! Fratremque derepta habet aquarum. Lacertis horrentia Mavortius sanguineae silentia, num Caesarea mollia candidus. Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. This is inline in the flow: ex=∑n=0∞xnn!∑n=0∞0ex=∑n=0∞​0∑n=0∞​n!xn​​. Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. Postquam superi desiluit, flentibus posuerunt ferum! Fratremque derepta habet aquarum. Lacertis horrentia Mavortius sanguineae silentia, num Caesarea mollia candidus.

Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. Postquam superi desiluit, flentibus posuerunt ferum! Fratremque derepta habet aquarum. Lacertis horrentia Mavortius sanguineae silentia, num Caesarea mollia candidus. Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. This is inline in the flow: ex=∑n=0∞xnn!∑n=0∞0ex=∑n=0∞​0∑n=0∞​n!xn​​. Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam. Postquam superi desiluit, flentibus posuerunt ferum! Fratremque derepta habet aquarum. Lacertis horrentia Mavortius sanguineae silentia, num Caesarea mollia candidus.

## Margin

Margin environment:

:::margin
Unreferenced, unformatted margin stuff, uncaptioned image :
:::

:::margin
![](./_assets/pics/usa-census.png)
:::

Dixerat hoc turbida mento nostri dolet fessos. Arcu sedit dumque. Amor campus
posco. Dilapsa est aquarum coimus cecidit et classis nos, regia nec erat lavit
undis ratis demugitaeque laetaque.

Also works with class :

![](./_assets/pics/usa-census.png){.margin}

- Parente dixit
- Marem vix virides nihil cornua navis vultus
- Si non
- Fixit quas dilapsum iunctum imitata satis

Par armat fuit nomen in Aegides lingua colatur, non humani, anser ab **sibi**
Munychiosque *summa*. Dixit Mavortis auratum se frequens haerenti exosae: quam
et aequore, tuli ira omnis Neptunus florentia calido tacti.

1. Flammas trepidosque variabant terrae nisi ablatum cessit
2. Cinyra Herculeos in Pelasgi vultu adfixa
3. Telamonius adhuc questuque non Erysicthone deus permulcet
4. Quem mentisque

Quodsi rosarum gaudere quoque frigore timido cognoverat, insurgere esse: septem.
Ianigenam in **vestros** mihi tot fecit, qui freta conferat, **penates** nomen
quo Telamon fenestris, duae. Relinquitur voce graviore, me **puto**, discedit in
sumpta corpore.


## Content with citations

This is a citation @chandrasekharanMicroscaleDifferentialCapacitive2011 [postnote], @ghouila-houriDeveloppementMicrocapteursFrottement2018 with `pandoc-citeproc`.

This is a citation @ghouila-houriDeveloppementMicrocapteursFrottement2018 with `pandoc-citeproc`.

@strakaGenerationDetectionCharacterization2019

Note [^a]

[^a]: yooo

Note [^*]

[^*]: yooo

Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas proxima iam.
Postquam superi desiluit, flentibus posuerunt ferum! Fratremque derepta habet
aquarum. Lacertis horrentia Mavortius sanguineae silentia, num Caesarea mollia
candidus. Lorem markdownum quod labooribus fecit, gravis aures supplex Pallas proxima iam.

Another citation,[@10/dfwrxt] this time with the filter

```sh
--filter pandoc-manubot-cite
```

## Cross-references

### To headers using `pandoc-secnos` filter

See section: @sec:chonky-formulae

eyop

## Abbreviations (not yet working)

This is HTML! (not in glossary ?)

This is +html (in glossary)!

This is a test using the `[pandoc-acronyms](https://pypi.org/project/pandoc-acronyms/)` filter.

- [!html>] inserts the long form ("beer brewing attitude").
- [!html<] inserts the short form ("BBA").
- [!html!] inserts the explained form ("beer brewing attitude (BBA)").

## Smart typography

En: --

Em: ---

Ellipse... text again

"Curly quotes" ?

## Esoteric (but not that much ?)

### Plots :

[`pandoc-plot`](https://github.com/LaurentRDC/pandoc-plot)

```{.matplotlib caption="Test plot figure" id="fig:plot"}
import matplotlib.pyplot as plt

plt.figure()
plt.plot([0,1,2,3,4], [1,2,3,4,5])
```

### Mermaid ?

Using [`mermaid-filter`](https://github.com/raghur/mermaid-filter)

~~~mermaid
sequenceDiagram
    Alice->>John: Hello John, how are you?
    John-->>Alice: Great!
~~~


# Rippledoc example


Paragraphs are separated by a blank line.

2nd paragraph. *Italic*, **bold**, and `monospace`. Itemized lists
look like:

  * this one
  * that one
  * the other one

Note that --- not considering the asterisk --- the actual text
content starts at 4-columns in.

> Block quotes are
> written like so.
>
> They can span multiple paragraphs,
> if you like.

Use 3 dashes for an em-dash. Use 2 dashes for ranges (ex., "it's all
in chapters 12--14"). Three dots ... will be converted to an ellipsis.
Unicode is supported. ☺

| a   | b   |
| --- | --- |
| c   | d   |

Table: table in just a chapter section {#tbl:chaptab}

## An h2 header

Here's a numbered list:

 1. first item
 2. second item
 3. third item

Note again how the actual text starts at 4 columns in (4 characters
from the left side). Here's a code sample:

    # Let me re-iterate ...
    for i in 1 .. 10 { do-something(i) }

As you probably guessed, indented 4 spaces. By the way, instead of
indenting the block, you can use delimited blocks, if you like:

~~~
define foobar() {
    print "Welcome to flavor country!";
}
~~~

(which makes copying & pasting easier). You can optionally mark the
delimited block for Pandoc to syntax highlight it:

~~~python
import time
# Quick, count to ten!
for i in range(10):
    # (but not *too* quick)
    time.sleep(0.5)
    print(i)
~~~



### An h3 header

Now a nested list:

 1. First, get these ingredients:

      * carrots
      * celery
      * lentils

 2. Boil some water.

 3. Dump everything in the pot and follow
    this algorithm:

        find wooden spoon
        uncover pot
        stir
        cover pot
        balance wooden spoon precariously on pot handle
        wait 10 minutes
        goto first step (or shut off burner when done)

    Do not bump wooden spoon or it will fall.

Notice again how text always lines up on 4-space indents (including
that last line which continues item 3 above).

Here's a link to [a website](http://foo.bar), to a [local
doc](local-doc.html), and to a [section heading in the current
doc](#an-h2-header). Here's a footnote [^1].

[^1]: Some footnote text.

Tables can look like this:

Name           Size  Material      Color
------------- -----  ------------  ------------
All Business      9  leather       brown
Roundabout       10  hemp canvas   natural
Cinderella       11  glass         transparent

Table: Shoes sizes, materials, and colors. {#tbl:table2}

(The above is the caption for the table.) Pandoc also supports
multi-line tables:

--------  -----------------------
Keyword   Text
--------  -----------------------
red       Sunsets, apples, and
          other red or reddish
          things.

green     Leaves, grass, frogs
          and other things it's
          not easy being.
--------  -----------------------

A horizontal rule follows.

***

Here's a definition list:

apples
  : Good for making applesauce.

oranges
  : Citrus!

tomatoes
  : There's no "e" in tomatoe.

Again, text is indented 4 spaces. (Put a blank line between each
term and  its definition to spread things out more.)

Here's a "line block" (note how whitespace is honored):

| Line one
|   Line too
| Line tree

and images can be specified like so:

![example image](example-image.jpg "An exemplary image"){#fig:example-image}

Inline math equation: $\omega = d\varphi / dt$. Display
math should get its own line like so:

$$I = \int \rho R^{2} dV$$

And note that you can backslash-escape any punctuation characters
which you wish to be displayed literally, ex.: \`foo\`, \*bar\*, etc.

---

## Test links

See section: @sec:chonky-formulae

Figure: @fig:label

Figure: @fig:label2

Figure: @fig:label3

Figure: @fig:example-image

Table: @tbl:table2

@tbl:label4

@tbl:chaptab

@eq:description

[link](#fig:label1)
