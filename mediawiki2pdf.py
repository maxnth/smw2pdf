import argparse

from parser import Parser

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Semantic MediaWiki XML output to PDF converter')
    parser.add_argument('--inputFilename', '-i', help='', required=True)
    parser.add_argument('--outputName', '-o', default='out')
    parser.add_argument('--exportFormat', '-e', default='pdf', choices=['pdf', 'html'],
                        help='Specifies the export formats.')
    parser.add_argument('--cssFile', '-css', default='style.css',
                        help='Specifies the css file to use for styling the output.')

    args = parser.parse_args()

    p = Parser(file=args.inputFilename, out=args.outputName, out_format=args.exportFormat, style=args.cssFile)

    p.export()
