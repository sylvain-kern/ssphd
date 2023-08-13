\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{tufte-pandoc}[]

%  _________  ___  ___  ________ _________  _______
% |\___   ___\\  \|\  \|\  _____\\___   ___\\  ___ \
% \|___ \  \_\ \  \\\  \ \  \__/\|___ \  \_\ \   __/|    ____________
%      \ \  \ \ \  \\\  \ \   __\    \ \  \ \ \  \_|/__|\____________\
%       \ \  \ \ \  \\\  \ \  \_|     \ \  \ \ \  \_|\ \|____________|
%        \ \__\ \ \_______\ \__\       \ \__\ \ \_______\
%         \|__|  \|_______|\|__|        \|__|  \|_______|

%  ________  _________    ___    ___ ___       _______
% |\   ____\|\___   ___\ |\  \  /  /|\  \     |\  ___ \
% \ \  \___|\|___ \  \_| \ \  \/  / | \  \    \ \   __/|    ____________
%  \ \_____  \   \ \  \   \ \    / / \ \  \    \ \  \_|/__|\____________\
%   \|____|\  \   \ \  \   \/  /  /   \ \  \____\ \  \_|\ \|____________|
%     ____\_\  \   \ \__\__/  / /      \ \_______\ \_______\
%    |\_________\   \|__|\___/ /        \|_______|\|_______|
%    \|_________|       \|___|/

%  ________  ________  _________  ___  ________  ___       _______
% |\   __  \|\   __  \|\___   ___\\  \|\   ____\|\  \     |\  ___ \
% \ \  \|\  \ \  \|\  \|___ \  \_\ \  \ \  \___|\ \  \    \ \   __/|
%  \ \   __  \ \   _  _\   \ \  \ \ \  \ \  \    \ \  \    \ \  \_|/__
%   \ \  \ \  \ \  \\  \|   \ \  \ \ \  \ \  \____\ \  \____\ \  \_|\ \
%    \ \__\ \__\ \__\\ _\    \ \__\ \ \__\ \_______\ \_______\ \_______\
%     \|__|\|__|\|__|\|__|    \|__|  \|__|\|_______|\|_______|\|_______|


% 	This is tufte-style-article.cls,
% 	a LaTeX class inherited from article
%	with a style similar to E.Tufte's designs.

% 	For more information about installation and usage,
% 	see readme.md and documentation.pdf.

%	This class is hosted and maintained
%	by Sylvain Kern
%	on https://github.com/sylvain-kern/tufte-style-article.


%	O P T I O N S
%
\DeclareOption{raggedright}{	% makes all paragraphs left-aligned
	\AtBeginDocument{
		\setlength{\RaggedRightParindent}{1em}
		\RaggedRight
	}
}
\DeclareOption{parskip}{		% changes paragraph indents vor vertical skips
	\AtBeginDocument{\usepackage{parskip}}
	\setlength{\parskip}{\baselineskip}
}
\DeclareOption{noheaders}{		% disables section titles on page headers
	\renewcommand{\leftmark}{}
	\renewcommand{\rightmark}{}
}
\DeclareOption{casual}{		% removes header numbering --still puts them in toc
	\AtBeginDocument{\setcounter{secnumdepth}{0}}
}
\newif\if@sans\@sansfalse
\DeclareOption{sans}{
	\@sanstrue
	\renewcommand{\familydefault}{\sfdefault}
}
\newif\if@colorful\@colorfulfalse
\newif\if@black\@blackfalse
\DeclareOption{colorful}{
	\@colorfultrue
	\@blackfalse
}
\DeclareOption{black}{
	\@blacktrue
	\@colorfulfalse
}
\newif\if@nomargins\@nomarginsfalse
\DeclareOption{notufte}{
	\@nomarginstrue
	\AtBeginDocument{
		\captionsetup{width = .7\textwidth}
		\renewcommand{\sidecaption}[2][]{
    		\caption[#1]{#2}
		}
		\renewenvironment{marginfigure}[1][]{
			\begin{figure}[!htb]
		}{
			\end{figure}
		}
		\renewenvironment{figure*}[1][]{
			\begin{figure}[!htb]
		}{
			\end{figure}
		}
		\renewenvironment{margintable}[1][]{
			\begin{table}[!htb]
		}{
			\end{table}
		}		\renewenvironment{table*}[1][]{
			\begin{table}[!htb]
		}{
			\end{table}
		}
		\renewcommand{\textfig}[4][]{%
			\begin{figure}[ht!]
				\noindent\includegraphics[width=#1\textwidth]{#2}%
				\caption{#3}%
				\label{#4}%
			\end{figure}
		}
		\renewcommand{\marginfig}[3]{%
			\begin{figure}[ht!]
				\noindent\includegraphics[width=.5\textwidth]{#1}%
				\caption{#2}%
				\label{#3}%
			\end{figure}
		}
		\renewcommand{\widefig}[4][]{%
			\begin{figure}[ht!]
				\noindent\includegraphics[width=#1\textwidth]{#2}%
				\caption{#3}%
				\label{#4}%
			\end{figure}
		}
		\renewcommand{\plainfig}[4][]{%
			\begin{figure}[ht!]
				\noindent\includegraphics[width=#1\textwidth]{#2}%
				\caption{#3}%
				\label{#4}%
			\end{figure}
		}
		\renewcommand{\plainwidefig}[4][]{%
			\begin{figure}[ht!]
				\noindent\includegraphics[width=#1\textwidth]{#2}%
				\caption{#3}%
				\label{#4}%
			\end{figure}
		}
		\renewcommand{\sidenote}[1]{
			\footnote{#1}
		}
		\renewcommand{\sidetext}[1]{
			\footnote{#1}
		}
	}
}
\ExecuteOptions{black}
\ProcessOptions\relax
\LoadClassWithOptions{article}

%	P A C K A G E   D E F I N I T I O N
%
% \RequirePackage{geometry}		% page geometry, margin definition
\RequirePackage{emptypage}		% if a page is empty, is is really empty
\RequirePackage{fullwidth}		% for wide environments
\RequirePackage{marginnote}
\RequirePackage{sidenotes}		% for margin stuff
\RequirePackage[
	hypcap=false				% hypcap=true spits an error
]{caption}						% for caption formatting
\RequirePackage[T1]{fontenc}	% font encoding
\RequirePackage[osf]{libertinus}% main font
\RequirePackage{libertinust1math}
\RequirePackage[osf, scale=.92]{sourcesanspro}		% sans font
\if@sans
	\RequirePackage[			% font for full sans document
		osf,
		default
	]{sourcesanspro}
\fi
\RequirePackage[
	defaultmono,
	scale=.8
]{droidsansmono}				% mono font
\RequirePackage{ragged2e}		% for better raggedright
\RequirePackage{titlesec}		% header customization
\RequirePackage{titletoc}		% toc customization
\RequirePackage{fancyhdr}		% page header customization
\RequirePackage{graphicx}		% for images
\RequirePackage[
	protrusion=true,
	expansion=true,
	final,
	% tracking,
]{microtype}					% microtypography: fine-tuning in text
\RequirePackage{amsfonts}		% math fonts
\RequirePackage{amsmath}		% math stuff
\RequirePackage{mathtools}		% amsmath extension
\RequirePackage{physics}		% handy shortcuts for physics
\RequirePackage[table]{xcolor}			% colorz
\RequirePackage[framemethod=TikZ]{mdframed} % for custom code boxes
\RequirePackage{tabularx}		% adaptive columns on tables
\RequirePackage{booktabs}		% better looking tables
\RequirePackage{longtable}
\RequirePackage{enumitem}		% better looking lists
\RequirePackage{setspace}
\RequirePackage[
	hidelinks,
    final,
    breaklinks,
    bookmarks,
	pdfusetitle,
]{hyperref}	% automatic references in pdf
\RequirePackage{etoolbox}		% really idk what this does
\RequirePackage[strict]{changepage}	% needed by sidenotes
\RequirePackage{placeins}		% for floatbarrier
\RequirePackage[]{listingsutf8}
\RequirePackage[titles]{tocloft}
\RequirePackage[
	% doi=false,
	% isbn=false,
	% url=false,
	autocite 	= superscript,
	backend 	= biber,
	citestyle 	= numeric-comp,
	style 		= nature,
	% citecolor   = niceBlue,
	sorting		= none,
	bibencoding = utf8,
]{biblatex}
\RequirePackage{csquotes}
%%% TEST footmisc
\RequirePackage[
    perpage,
    symbol*,
    flushmargin,
    side,
    ragged,
]{footmisc}
% \RequirePackage{marginfix}
\makeatletter
  \renewcommand\@makefnmark{%
    \hbox{%
      \ifx\@fnsymbol\FN@fnsymbol@sym
        \expandafter\@firstofone
      \else
        \expandafter\@textsuperscript
      \fi
      {\normalfont\@thefnmark}%
    }%
  }
\makeatother
\RequirePackage{xifthen}

%	C O L O R  D E F I N I T I O N
%
\definecolor{niceRed}{HTML}{980326}
\definecolor{niceBlue}{HTML}{025472}
\definecolor{tooRed}{HTML}{cc0000}
\if@colorful
	\hypersetup{
		colorlinks = true,
		linkcolor = niceBlue,
		% anchorcolor = niceBlue,
		citecolor = .,
		urlcolor = niceBlue,
	}
\else
\fi
\if@black
	\definecolor{niceRed}{HTML}{000000}
	\definecolor{niceBlue}{HTML}{000000}
\else
\fi
\newcommand\red[1]{\textcolor{niceRed}{#1}}


%	G E O M E T R Y  D E F I N I T I O N
%
% \newgeometry{
% 	tmargin = 80pt,
% 	bmargin = 80pt,
% 	lmargin = 100pt,
% 	rmargin = 100pt,
% }
% \savegeometry{titlepage}
% \newgeometry{
% 	textwidth = .56\paperwidth,
% 	textheight = .8\paperheight,
% 	lmargin = 70pt,
% 	marginparwidth = .38\textwidth,
% 	marginparsep = 28pt,
% 	headheight = 16pt,
% 	tmargin = 80pt,
% 	% showframe,
% }
% \savegeometry{regular}
% \newgeometry{
% 	tmargin = 80pt,
% 	bmargin = 80pt,
% 	lmargin = 70pt,
% 	rmargin = 70pt,
% }
% \savegeometry{evenmargins}

\newcommand\loadgeometry[1]{}

\if@nomargins
	\newgeometry{
		textheight = .8\paperheight,
		lmargin = 80pt,
		rmargin = 80pt,
		marginparwidth = 50pt,
		marginparsep = 10pt,
		headheight = 15pt,
		tmargin = 100pt,
		%showframe,
	}
	\savegeometry{regular}
\fi

%	M A R G I N S
%

\makeatletter
  \renewcommand\@makefnmark{%
    \hbox{%
      \ifx\@fnsymbol\FN@fnsymbol@sym
        \expandafter\@firstofone
      \else
        \expandafter\@textsuperscript
      \fi
      {\normalfont\@thefnmark}%
    }%
  }
\makeatother

% formatting sidenote text

% \makeatletter
% \RenewDocumentCommand\sidenotetext{ o o +m }{%
%     \IfNoValueOrEmptyTF{#1}{%
%         \@sidenotes@placemarginal{#2}{\setstretch{1.0}\noindent\footnotesize\RaggedRight{\thesidenote{}}~~ #3}%
%         \refstepcounter{sidenote}%
%     }{%
%         \@sidenotes@placemarginal{#2}{\textsuperscript{#1}~#3}%
%     }%
% }
% \makeatother

% \newcommand{\sidetext}[1]
% {\marginpar{\setstretch{1.0}\RaggedRight\footnotesize\noindent #1 \vskip 4pt}}
\newcommand{\sidetext}[1]{\footnotetext[0]{#1}}

\newenvironment{wide}{
\begin{fullwidth}[outermargin=-\marginparwidth-\marginparsep, width=\linewidth+\marginparwidth+\marginparsep]
}%
{
\end{fullwidth}
}


%	P A G E  H E A D E R S
%
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\fancyhead[LO]{%
	\textls{\scshape\sffamily\nouppercase{\MakeLowercase{\rightmark}}}
}
\fancyhead[RO]{%
	\sffamily\normalsize\thepage
}%
\fancyhead[LE]{%
	\sffamily\normalsize\thepage
}
\fancyhead[RE]{%
	\textls{\scshape\sffamily\nouppercase{\MakeLowercase{\leftmark}}}
}
\fancypagestyle{plain}{
\fancyhf{}
\fancyhead[RO]{\sffamily\thepage}
\fancyhead[LE]{\sffamily\thepage}
}
\setlength{\headheight}{13.6pt}

%	T I T L E  H E A D E R S
%
\titleformat{\section}
	{\sffamily\LARGE}
	{\thesection}
	{1em}
	{\setstretch{0.9}\raggedright}
\titleformat{\subsection}
	{\fontseries{b}\selectfont\sffamily}
	{\thesubsection}
	{1em}
	{\setstretch{0.9}\raggedright}[]
\titleformat{\subsubsection}[runin]
	{\normalfont\sffamily}
	{\thesubsubsection}
	{1ex}
	{}[~~$\cdot$]
% \titleformat{\subsubsection}
% 	{\itshape}
% 	{\normalfont\thesubsubsection}
% 	{1em}
% 	{\setstretch{0.9}\raggedright\itshape}
\titlespacing*{\section}{0em}{4em}{1em}
\titlespacing*{\subsection}{0em}{2em}{.2em}


%	M A K E T I T L E
%
\makeatletter
\newcommand\@maketitlebis{%
	\hfill
    \bgroup
    \setstretch{1.0}
		\vskip -40pt
		\let\footnote\thanks
		{\huge\raggedright \@title \par }
		\vskip 8pt
        {\noindent\Large\raggedright \@subtitle \par}
        \vskip 20pt
		{\noindent\large \itshape \@author{}~~$\cdot$~~\@date}
		\vskip 28pt~
    \egroup
	\setstretch{1.12}
}
\renewcommand\maketitle{
	\@maketitlebis
	\thispagestyle{empty}
}

\newcommand\subtitle[1]{\renewcommand\@subtitle{#1}}
\newcommand\@subtitle{}
\makeatother

%	M E T A D A T A
%
%
% \makeatletter
% \def\author#1{\gdef\insertauthor{#1}\gdef\@author{#1}\hypersetup{pdfauthor={#1}}}
% \def\title#1{\gdef\inserttitle{#1}\gdef\@title{#1}\hypersetup{pdftitle={#1}}}
% \def\firstsupervisor#1{\gdef\insertsupervisor{#1}}
% \def\secondsupervisor#1{\gdef\insertsupervisor{#1}}
% \def\institution#1{\gdef\insertinstitution{#1}}
% \def\degree#1{\gdef\insertdegree{#1}}
% \def\faculty#1{\gdef\insertfaculty{#1}}
% \def\department#1{\gdef\insertdepartment{#1}}
% \def\submitdate#1{\gdef\insertsubmitdate{#1}}
% \def\keywords#1{\gdef\insertkeywords{#1}\hypersetup{pdfkeywords={#1}}}
% \submitdate{\number\the\year}
% \makeatother
% \hypersetup{%
%     pdfcreator  = {\LaTeX\ with class \flqq tufte-style-article\frqq},
%     pdfproducer = {pdfeTeX-0.\the\pdftexversion\pdftexrevision}
% }

%	F I G U R E S  A N D  S T U F F
%
% 	caption formatting
\DeclareCaptionLabelFormat{lc}{\MakeLowercase{#1}~#2}
\DeclareCaptionLabelSeparator{mysep}{.\quad}
\DeclareCaptionLabelSeparator{mysepside}{.\\}
\captionsetup{
	labelfont = {bf},
	%labelformat = lc,
	labelsep = mysep,
	justification=RaggedRight,
	font={footnotesize, stretch=1},
	singlelinecheck=on,
}
\captionsetup[subfigure]{justification=centering}
\DeclareCaptionStyle{sidecaption}{
    labelfont = {bf},
	%labelformat = lc,
	labelsep = mysepside,
	justification=RaggedRight,
	font={footnotesize, stretch=1},
	singlelinecheck=off,
}
\DeclareCaptionStyle{marginfigure}{
    labelfont = {bf},
	%labelformat = lc,
	labelsep = mysepside,
	justification=RaggedRight,
	font={footnotesize, stretch=1},
	singlelinecheck=off,
}
\DeclareCaptionStyle{widefigure}{
    labelfont = {bf},
	%labelformat = lc,
	labelsep = mysep,
	justification=RaggedRight,
	font={footnotesize, stretch=1},
	singlelinecheck=off,
}
\DeclareCaptionStyle{margintable}{
    labelfont = {bf},
	%labelformat = lc,
	labelsep = mysep,
	justification=RaggedRight,
	font={footnotesize, stretch=1},
	singlelinecheck=off,
}
\DeclareCaptionStyle{widetable}{
    labelfont = {bf},
	%labelformat = lc,
	labelsep = mysep,
	justification=RaggedRight,
	font={footnotesize, stretch=1},
	singlelinecheck=off,
}


%	figures

%	figure macros
\AtBeginDocument{\usepackage[export]{adjustbox}}
% \newcommand{\textfig}[4][]{%
% 	\medskip%
% 	\marginpar{%
% 		\vskip 8pt%
% 		\captionof{figure}{#3}%
% 		\label{#4}%
% 	}\nopagebreak%
% 	\noindent\includegraphics[width=#1\textwidth, outer]{#2}%
% 	\medskip%
% }
\newcommand{\textfig}[4][]{%
	\FloatBarrier
	\begin{figure}[!htb]%
		\sidecaption{#3\label{#4}}%
		\includegraphics[width = #1\linewidth, outer]{#2}%
	\end{figure}%
}
\newcommand{\marginfig}[3]{%
	\FloatBarrier%
	\begin{marginfigure}%
		\includegraphics[width = \linewidth]{#1}%
		\caption{#2\label{#3}}%
	\end{marginfigure}%
}
\newcommand{\widefig}[4][]{%
	\FloatBarrier%
	\begin{figure*}[t]%
		\includegraphics[width=#1\linewidth, outer]{#2}%
		\sidecaption{#3\label{#4}}%
	\end{figure*}%
}
\newcommand{\plainfig}[4][]{%
	\FloatBarrier%
	\begin{figure}[!htb]%
		\includegraphics[width=#1\linewidth, left]{#2}%
		\caption{#3\label{#4}}%
	\end{figure}%
}
\newcommand{\plainwidefig}[4][]{%
	\FloatBarrier%
	\begin{figure*}[!htb]%
		\includegraphics[width=#1\linewidth, left]{#2}%
		\caption{#3\label{#4}}%
	\end{figure*}%
}

%	table macros
\newcolumntype{Y}{>{\centering\arraybackslash}X} % tabularx column type
\newenvironment{texttable}[2]{%
	\begingroup%
	\small%
	\marginpar{%
		\vskip 8pt%
		\captionof{table}{#1}%
		\label{#2}%
	}

	\noindent%
}
{
	\endgroup%
}

\AtBeginEnvironment{table}{\small\RaggedRight}

%	T O C  C U S T O M I Z A T I O N
%
\titlecontents{section}[30pt]
	{\vspace{26pt}\large\sffamily\fontseries{sb}\selectfont\hspace*{-30pt}}
	{\makebox[30pt][l]{\thecontentslabel}}
	{}
	{\textcolor{niceBlue}{\contentspage}}[\vspace{10pt}]
\titlecontents{subsection}[30pt]
	{\sffamily\fontseries{sl}\selectfont}
	{\hspace*{-30pt}\makebox[30pt][l]{\thecontentslabel}}
	{}
	{\textcolor{niceBlue}{\contentspage}}[\vspace{1pt}]

% TOCLOFT (stolen from classicthesis)
\renewcommand{\cftfigpresnum}{\scshape\MakeTextLowercase}%
\renewcommand{\cftfigfont}{\normalfont}%
\renewcommand{\cftfigleader}{\hspace{2.5em}}%
\renewcommand{\cftfigafterpnum}{\cftparfillskip}%
\renewcommand{\cftfigpresnum}{\figurename~}%Fig.~}
\newlength{\figurelabelwidth}
\settowidth{\figurelabelwidth}{\cftfigpresnum~999}
\addtolength{\figurelabelwidth}{1em}
\cftsetindents{figure}{0em}{\figurelabelwidth}
% tables
\renewcommand{\cfttabfont}{\normalfont}%
\renewcommand{\cfttableader}{\hspace{2.5em}}%
\renewcommand{\cfttabafterpnum}{\cftparfillskip}%
\renewcommand{\cfttabpresnum}{\tablename~}%Tab.~}
\newlength{\tablelabelwidth}
\settowidth{\tablelabelwidth}{\cfttabpresnum~999}
\addtolength{\tablelabelwidth}{1em}
%\cftsetindents{table}{0em}{\tablelabelwidth}
\cftsetindents{table}{0em}{\figurelabelwidth}
% listings
\newcommand\listingsname{Listing}
\renewcommand\lstlistingname{Listing}
\renewcommand\lstlistlistingname{List of Listings}
\newlistof{listings}{lol}{\lstlistlistingname}%
\renewcommand{\cftlistingspresnum}{\scshape\MakeTextLowercase}%
\renewcommand{\cftlistingsfont}{\normalfont}%
\renewcommand{\cftlistingspresnum}{\lstlistingname~}%
\renewcommand{\cftlistingspagefont}{\normalfont}%
\renewcommand{\cftlistingsleader}{\hspace{1.5em}}%
\renewcommand{\cftlistingsafterpnum}{\cftparfillskip}%
\newlength{\listingslabelwidth}%
\settowidth{\listingslabelwidth}{\cftlistingspresnum~999}%
\addtolength{\listingslabelwidth}{2.5em}%
\cftsetindents{listings}{0em}{\figurelabelwidth}%
% \let\l@lstlisting\l@listings%
\let\lstlistoflistings\listoflistings%
% blue page numbers
\renewcommand{\cftsecpagefont}{\color{niceBlue}}
\renewcommand{\cftsubsecpagefont}{\color{niceBlue}}
\renewcommand{\cftsubsubsecpagefont}{\color{niceBlue}}
\renewcommand{\cftfigpagefont}{\color{niceBlue}}
\renewcommand{\cfttabpagefont}{\color{niceBlue}}
\renewcommand{\cftlistingspagefont}{\color{niceBlue}}
% TOCLOFT over

%	toc offset
\let\oldtoc\tableofcontents
\renewcommand{\tableofcontents}{%
	\bgroup
	\thispagestyle{plain}
	\setstretch{1}
	\oldtoc
	\egroup
}


%	B I B L I O G R A P H I C
%	      R E F E R E N C E S  %this is black magic to me but it seems 2b working

%	POUR LES AUTOCITE ENTRE [BRACKETS]
%
% \DeclareCiteCommand{\supercite}[\mkbibsuperscript]
%   {\usebibmacro{cite:init}%
%    \let\multicitedelim=\supercitedelim
%    \iffieldundef{prenote}
%      {}
%      {\BibliographyWarning{Ignoring prenote argument}}%
%    \iffieldundef{postnote}
%      {}
%      {\BibliographyWarning{Ignoring postnote argument}}%
%   \bibopenbracket}%
%   {\usebibmacro{citeindex}%
%    \usebibmacro{cite:comp}}
%   {}
%   {\usebibmacro{cite:dump}\bibclosebracket}

\makeatletter
\newcommand\sidecite[2][]{\autocite{#2}\sidetext{\ifthenelse{\equal{#1}{}}{}{\vskip #1}%
\@for\cle:={#2}\do{\makebox[0pt][r]{\autocite{\cle}}\fullcite{\cle}.\\\vskip 4pt}%
}}
\newcommand\sidetextcite[2][]{\sidetext{\ifthenelse{\equal{#1}{}}{}{\vskip #1}%
\@for\cle:={#2}\do{\makebox[0pt][r]{\autocite{\cle}}\fullcite{\cle}.\\\vskip 4pt}%
}}
\makeatother

\DeclareCiteCommand{\fullcite}
  {\usebibmacro{prenote}}
  {\clearfield{url}%
   \clearfield{pagetotal}%
   \clearfield{edition}%
   \usedriver
     {\DeclareNameAlias{sortname}{default}}
     {\thefield{entrytype}}}
  {\multicitedelim}
  {\usebibmacro{postnote}}

%	flush T I G H T  L I S T S
%
\AtBeginDocument{
	\setlist{topsep=0pt, itemsep=0pt, noitemsep}
}
% 	diamond bullets
% \renewcommand{\labelitemi}{$\vcenter{\hbox{\small$\diamond$}}$}

%	C O D E
%
%   colors
\definecolor{bg}{rgb}{.95,.95,.95}
\definecolor{key}{HTML}{333399}
\definecolor{comment}{HTML}{6b6b99}
\definecolor{codegray}{rgb}{0.4,0.4,0.4}
\definecolor{string}{HTML}{2b4f2b}
%   boxes
\mdfdefinestyle{code_box}{%
    roundcorner= 2pt,
	backgroundcolor=white,
    linecolor = lightgray,
    linewidth = .5pt,
    topline = true,
    bottomline = true,
    leftline = true,
    rightline = true,
	innertopmargin=.2em,
	innerbottommargin=.2em,
}
%   listing styles
\lstdefinestyle{unnumbered}{
    commentstyle=\color{comment},
    keywordstyle=\color{key},
    stringstyle=\color{string},
    basicstyle=\ttfamily\normalsize\lst@ifdisplaystyle\small\fi,
    breakatwhitespace=false,
    breaklines=true,
    keepspaces=true,
    showspaces=false,
    showstringspaces=false,
    showtabs=false,
    tabsize=4,
    framexleftmargin=30pt,
}
\lstdefinestyle{numbered}{
    commentstyle=\color{comment},
    keywordstyle=\color{key},
    stringstyle=\color{string},
    basicstyle=\ttfamily\normalsize\lst@ifdisplaystyle\small\fi,
    breakatwhitespace=false,
    breaklines=true,
    keepspaces=true,
    numbers=left,
    numberstyle = \color{codegray}\footnotesize\ttfamily,
    numbersep=10pt,
    showspaces=false,
    showstringspaces=false,
    showtabs=false,
    tabsize=4,
    framexleftmargin=30pt,
    framextopmargin=100pt,
    framexbottommargin=30pt,
}
%   code macros
\lstset{inputencoding=utf8/latin1}
\lstnewenvironment{codebox}[1]{%
	\mdframed[style = code_box, innerleftmargin=10pt]%
	\lstset{style=unnumbered, language=#1}
}
{
    \endmdframed
}
\lstnewenvironment{altcodebox}[1]{%
	\mdframed[style = code_box, innerleftmargin=10pt]%
	\lstset{style=unnumbered, language=#1}
}
{
    \endmdframed
}
\lstnewenvironment{codeboxnum}[1]{%
	\mdframed[style = code_box, innerleftmargin=25pt]%
	\lstset{style=numbered, language=#1}
}
{
    \endmdframed
}
\newcommand{\inlinecode}[1]{\lstinline[style=unnumbered, language=#1]}
%	snippet environments
\lstnewenvironment{snippet}[3]{%
	\marginpar{~\vskip 10pt\captionof{listings}{#2}}
	\mdframed[style = code_box, innerleftmargin=10pt]%
	\lstset{style=unnumbered, language=#1}
}
{
    \endmdframed
}
\lstnewenvironment{snippetnum}[3]{%
	\marginpar{~\vskip 10pt\captionof{listings}{#2\label{#3}}}
	\mdframed[style = code_box, innerleftmargin=25pt]%
	\lstset{style=numbered, language=#1}
}
{
    \endmdframed
}

% by-chapter numbering
% \counterwithin{listing}{chapter}


%	I N - T E X T  F I N E T U N I N G
%
% widows and orphans
\clubpenalty = 10000
\widowpenalty = 10000
\displaywidowpenalty = 10000


%	M I S C E L L A N E O U S
%
%	for  t i g h t  lists (pandoc style)
\providecommand{\tightlist}{%
	\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}
}
\providecommand{\toight}{%
	\tightlist%
}
%	minipages with margin notes
\usepackage{minipage-marginpar}
%	no page break environment
\newenvironment{absolutelynopagebreak}
  {\par\nobreak\vfil\penalty0\vfilneg
   \vtop\bgroup}
  {\par\xdef\tpd{\the\prevdepth}\egroup
   \prevdepth=\tpd}

%	M A T H  &  P H Y S I C S
%	S H O R T C U T S
%\iffalse
% uncomment this \iffalse
%and the \fi at the end to disable (or delete)

	% i find it more pleasing
	\renewcommand{\phi}{\varphi}
	\renewcommand{\epsilon}{\varepsilon}
	\newcommand{\N}{\mathbb{N}}     % shortcuts for usual number sets
	\newcommand{\Z}{\mathbb{Z}}
	\newcommand{\Q}{\mathbb{Q}}
	\newcommand{\R}{\mathbb{R}}
	\newcommand{\C}{\mathbb{C}}
	% powers of 10
	\newcommand{\ee}[1]{\cdot 10^{#1}}
	% new vect with overrightarrow style
	\newcommand{\vect}[1]{\:\overrightarrow{#1}}
%fi

% TODO
\newlistof{todos}{tod}{\bfseries \textls{TO DO} list}
\let\oldlistoftodos\listoftodos
\renewcommand{\listoftodos}{\bgroup\color{tooRed}{\oldlistoftodos}\egroup}
\newcommand{\todolist}{\listoftodos}

\newcounter{todo}
\setcounter{todo}{1}
\newcommand{\todo}[2][]{
    \addcontentsline{tod}{todos}{\protect\numberline{\bfseries\#\thetodo}#1}
    \bgroup\color{tooRed}

    \noindent\large\textsc{todo \#\arabic{todo}}~~\hrulefill%
    \refstepcounter{todo}%
    \smallskip

    \normalsize\noindent #2

    \noindent\hrulefill
    \egroup
}

%		S  T   R   E   T     C      H
%
\AtBeginDocument{%
	\setstretch{1.12}
}