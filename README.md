# MALSongs

This is a project that aims at helping people to track anisongs already downloaded/to download.

# Usage

First, export your MyAnimeList using [this link](https://myanimelist.net/panel.php?go=export) (log in to your account before going to this link). Then, run the following command :

```python src/main.py --xml [exported_xml_file]```


This will produce a `.tsv` file. You can then import this `tsv` file to a Google Sheets, and format it as you wish. The importing should work even with default values, but you may want to set `Separator type` to `Tabs` if it doesn't work properly.


# Recommended options for the Google Sheets

The first thing I recommend you is to convert all those "FALSE" and "TRUE" values in the first column with checkboxes. This can be achieved easily by selecting the first column, then clicking on `Insert > Checkbox`.
You can also strike the results that are checked. To do so, select every data using Ctrl + A, then right click on it and press `Conditional formatting`. On the right menu that just opened, set `Format cell if` to `Custom formula`, and put `=$A2` in the formula. Then, you can define your own formatting style; I recommand using "strikethrough" only but you can change the color if you want for example.


# Todo
- [ ] Maybe try to fix sorting on results like `"Bungako Shoujo" Movie`
- [x] Try to get the number of the OP/ED
- [x] Try to get the episodes in which the anisong was played
- [x] Try to get the singer/group who performed the song
- [x] Remove non-started animes from default option and add an option to include the non-started animes
- [ ] Remove potential duplicates (on OVAs for example)
- [ ] Add an option to set songs library directory(/ies ?) and set "Checked" to True if the results are already in the songs library
- [x] Add an option to take a previously computed .tsv and update it (/!\ try to keep the results sorted)
- [ ] Maybe check that each entry has an even number of `"`, and if that's not the case, append a `"` at the end of the entry (otherwise Google Sheets won't understand correctly)

# Long term todo
The following task are essential to make the project useable by other users. It may take more time than other tasks and is not essential to make the project work correctly
- [ ] Add an UI and display the list of anisongs inside this UI
- [ ] Add a save and load function (maybe by keeping the `.tsv` or maybe converting it to a more friendly format like `JSON`)
- [ ] If the format is changed to JSON, we should still be able to export the list as `.tsv` so users may still use Google Sheets if they wish to
- [ ] If this wasn't done before in the basic Todo, add the MAL link as hyperlink
