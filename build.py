# read all *.md files in the current and all sub directories 
# create a new txt file containing all the text from the *.md files, seperated by its filename
# the filename is the first line of the text
# the text is the rest of the file
# the text is seperated by a newline

import os
import glob
import re
import sys
from pathlib import Path
from datetime import datetime
from datetime import timedelta
from datetime import date

# ignore all _config folder
ignoreFilePatternList = [
    '_config'
]
# true to generate code
IsGenCode = True
maxCodeLines = 15
# language that are allowed in codeblock ```lang
codeblockLangs = {
     'javascript' : True,
     '' : True,
     'lua' : True,
     'npl' : True,
     'c' : True,
}

def get_files():
    files = glob.glob('**/*.md', recursive=True)

    # ignore file containing any pattern in ignoreFilePatternList
    for ignoreFilePattern in ignoreFilePatternList:
        files = [file for file in files if ignoreFilePattern not in file]
    return files

# assume all text are in utf8 encoding
def get_text(file):
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
        
        # parse into lines
        lines = text.split('\n')
        # remove empty lines or lines containing only spaces
        lines = [line for line in lines if line.strip() != '']

        # for each line check if it begins with <some_xml_tag >
        # if it does, remove all lines until the line begins with </some_xml_tag>
        isInsideXMLTag = False
        newLines = []
        for line in lines:
            if isInsideXMLTag:
                if line.strip().startswith('</'):
                    isInsideXMLTag = False
            else:
                if line.strip().startswith('<'):
                    isInsideXMLTag = True
                else:
                    newLines.append(line)
        lines = newLines

        # for each line that begins with ```plus some text, remove all lines until the line begins with ```
        isInsideMod = False
        newLines = []
        codeLines = []
        modName = ''
        for line in lines:
            if isInsideMod:
                if line.strip().startswith('```'):
                    isInsideMod = False

                    # if codeLines size is smaller than maxCodeLines, then add it to newLines
                    if IsGenCode and (modName in codeblockLangs) and len(codeLines) <= maxCodeLines:
                        newLines += codeLines
                else:
                    codeLines.append(line)
            else:
                if line.strip().startswith('```'):
                    # get the text after ```
                    modName = line.strip()[3:]
                    # trim all leading and trailing spaces
                    modName = modName.strip()
                    codeLines = []
                    isInsideMod = True
                else:
                    newLines.append(line)
        lines = newLines
        
        # remove all markdown image tag like ![](...)                    
        lines = [re.sub(r'!\[.*\]\(.*\)', '', line) for line in lines]

        # replace all links like [text](url) but retain the text in square brackets
        lines = [re.sub(r'\[(.*)\]\(.*\)', r'\1', line) for line in lines]

        # remove all #* from the beginning of the line
        lines = [re.sub(r'^#*', '', line) for line in lines]

        # remove all text that begins with http plus non space words 
        lines = [re.sub(r'http\S*', '', line) for line in lines]

        # remove all ** in bold markdown text
        lines = [re.sub(r'\*\*', '', line) for line in lines]

        # remove > in the beginning of the line
        lines = [re.sub(r'^>', '', line) for line in lines]

        # remove lines that contains only -*
        lines = [line for line in lines if not re.match(r'^-*$', line)]

        # remove single occurange of `
        lines = [re.sub(r'`', '', line) for line in lines]

        # remove empty lines or lines containing only spaces
        lines = [line for line in lines if line.strip() != '']

        # remove emoji in :some_text:
        lines = [re.sub(r':.*:', '', line) for line in lines]
        
        # generate new text
        text = '\n'.join(lines)
        return text
    
def get_filename(file):
    return file.split('/')[-1].split('.')[0]

def write_text_to_file(text):
    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(text)
        f.close()
        print('output.txt created')
        print('output.txt contains ' + str(len(text)) + ' characters')

def main():
    files = get_files()
    text = []
    for file in files:
        print('reading ' + file)
        text.append(get_filename(file))
        text.append(get_text(file))
    text = '\n'.join(text)
    write_text_to_file(text)

if __name__ == '__main__':
    main()



        
