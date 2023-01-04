## Code

``` c
int main() {
  printf("Hello world!");
  return 0;
}
```

Lorem markdownum quod laboribus fecit, gravis aures supplex Pallas
proxima iam. Postquam superi desiluit, flentibus posuerunt ferum!
Fratremque derepta habet aquarum. Lacertis horrentia Mavortius
sanguineae silentia, num Caesarea mollia candidus. Lorem markdownum quod
laboribus fecit, gravis aures supplex Pallas proxima iam.

``` css
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

/* intermÃ©diaire : le main text est collÃ© Ã  gauche (burger ?) mais quand mÃªme les sidenotes */
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

``` python
def factorial(n):
        return int(n==0) or n*factorial(n-1)
```

Wide code:

::: wide
``` zsh
> zsh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```
:::
