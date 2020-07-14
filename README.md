# About

Enables an easy way to download recordings from the [Parliament of Australia](https://www.aph.gov.au) website while also providing a way to by pass the obscene requirement of the Adobe Flash plugin.

# Installation

No dependencies beside `Python 3` is required (only standard libraries are used). Has been tested against `Python 3.8.3`. 

# Usage

```
parlview-dl.py [-h] url {audio,low,med,high}
```

# Further information

To search for recordings to download, [this page](https://www.aph.gov.au/Watch_Read_Listen) includes links to the last 100 sessions under *Latest Events*, however any further sessions can only be retrieved in the search under *Search Hansard* (may take a while to return results, it seems to be quite slow sometimes). 

URL's for the recordings will look like `http://parlview.aph.gov.au/mediaPlayer.php?videoID=xxxxxx&operation_mode=parlview`.
