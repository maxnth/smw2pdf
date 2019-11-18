# smw2pdf
Small CLI tool to transform Semantic MediaWiki XML exports to PDF (or HTML) files

## Setup
Optional:
* python -m venv venv 
* source venv/bin/activate

* pip install -r requirements.txt

## Usage

```
convert.py [-h] --inputFilename INPUTFILENAME [--outputName OUTPUTNAME]
                  [--exportFormat {pdf,html}] [--cssFile CSSFILE]

Semantic MediaWiki XML output to PDF converter

optional arguments:
  -h, --help            show this help message and exit
  --inputFilename INPUTFILENAME, -i INPUTFILENAME
  --outputName OUTPUTNAME, -o OUTPUTNAME
  --exportFormat {pdf,html}, -e {pdf,html}
                        Specifies the export formats.
  --cssFile CSSFILE, -css CSSFILE
                        Specifies the css file to use for styling the output.
```

## Example

```
python convert.py -i export.xml -o MyExportFile -e pdf -css custom.css
```
