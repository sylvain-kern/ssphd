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

