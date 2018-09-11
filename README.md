# MALSongs

This is a project that aims at helping people to track anisongs already downloaded/to download.

# Usage

First, export your MyAnimeList using [this link](https://myanimelist.net/panel.php?go=export) (log in to your account before going to this link). Then, run the following command :

```python src/main.py --xml [exported_xml_file]```


This will produce a `.csv` file. You can then import this `csv` file to a Google Sheets, and format it as you wish.


# Recommended options for the Google Sheets

The first thing I recommend you is to convert all those "FALSE" and "TRUE" values in the first column with checkboxes. This can be achieved easily by selecting the first column, then clicking on `Insert > Checkbox`.
You can also strike the results that are checked. To do so, select every data using Ctrl + A, then right click on it and press `Conditional formatting`. On the right menu that just opened, set `Format cell if` to `Custom formula`, and put `=$A2` in the formula. Then, you can define your own formatting style; I recommand using "strikethrough" only but you can change the color if you want for example.


# Todo
- [ ] Maybe try to fix sorting on results like `"Bungako Shoujo" Movie`
- [ ] Remove non-started animes from default option and add an option to include the non-started animes
- [ ] Add an option to set songs library directory(/ies ?) and set "Checked" to True if the results are already in the songs library
- [ ] Add an option to take a previously computed .csv and update it (/!\ try to keep the results sorted)
