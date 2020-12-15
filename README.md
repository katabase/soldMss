# Sold manuscripts

This repository contains results of the manuscripts clustering.

## Workflow

Using the JSON file, [export.json](https://github.com/katabase/soldMss/blob/main/export.json), produced by the script [extractor_json.py](https://github.com/katabase/3_TaggedData/blob/main/script/extractor_json.py), we want to cluster all the entries and, doing so, know exactly how many manuscripts have been sold multiple times.

The entries are clustered are clustered based on their traits :
* author
* format
* number of pages
* price
* date

## Installation and use

If you want to cluster all the entries of `export.json`, try this :

```bash
* git clone https://github.com/katabase/soldMss.git
* cd soldMss
* python3 -m venv my_env
* source my_env/bin/activate
* pip install -r requirements.txt
* cd scripts
* python3 reconciliator_all.py
```

*Note that the output file of this clustering is available [here](https://github.com/katabase/soldMss/blob/main/output/reconciliated.json).*

Now you can try some data analysis, being in the `scripts` folder :

* about the price with 
```bash
python3 price.py
```

* about the authors with 
```bash
python3 author.py
```
* about the number of sales of each manuscript with 
```bash
python3 mss_list.py
```

All the results will be in the `output`folder.

## Credits

* The scripts were created by Alexandre Bartz and Matthias Gille Levenson with the help of Simon Gabay.


## Cite this repository
Alexandre Bartz, Simon Gabay, Matthias Gille Levenson, Ljudmila Petkovic and Lucie Rondeau du Noyer, _Manuscript sale catalogues : clustering_, Neuchâtel: Université de Neuchâtel, 2020, [https://github.com/katabase/soldMss](https://github.com/katabase/soldMss).

## Licence
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Licence Creative Commons" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International Licence</a>.