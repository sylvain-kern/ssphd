## Tables

Text before. I can reference the following table with its label : see +@tbl:label3.

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

Check the stats +@tbl:label4.

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

