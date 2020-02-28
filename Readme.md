## Motley Fool Transcript Extractor

### Files
#### transcript_dl.py: Python script to download earning call transcripts from Motley Fool (www.fool.com). The period of the call transcripts are 7 quarters. All downloaded transcripts will be placed in the folder (Transcripts) with their respective company and the transcripts (HTML files) in a subfolder
#### transcripts_parse.py: Python script that has a function which directly parses the downloaded transcript and returns a DataFrame with the relevant information in it
#### requirements.txt: The file contains of all the various python libraries required to be used in order to successfully run the scripts

### Folder
#### Transcripts: Folder where all the downloaded transcripts will be found
#### Chrome: Folder for the Webdriver to be used by Selenium 