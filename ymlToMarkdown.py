'''
Author: LiXizhi
Date: 2024.5.27
Desc: convert keepwork menu yml to markdown bullet list
cmd: python ymlToMarkdown.py
input file: ./menu.md
output file: ./list.md
'''
import re
import sys

def main():
    # read filename from command line
    filename = "menu.md"
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    
    # read the utf8 text from links.txt
    print(f"reading {filename}")
    ''' folowing is some example text
          name: 如何推广Paracraft
          link: 'https://keepwork.com/official/docs/videos/spread_video'
    '''
    text = ""
    with open(filename, "r", encoding="utf8") as f:
        text = f.read()

    # replace regular expression ">-%s+"  with ""
    text = re.sub(r">\-\s+", "", text)
  

    # print text count 
    print(f"text count: {len(text)}")

    # read name: and link: pairs from text, and put them into a list
    list = []
    for line in text.split("\n"):
        if "name:" in line:
            list.append(line.split(": ")[1].strip())
        if "link:" in line:
            line = line.split(": ")[1].strip()
            # remove all ' from the link
            line = line.replace("'", "")
            list.append(line)
    # print list coont
    print(f"list count: {len(list)/2}")
    
    outputFilename = "list.md"
    print(f"writing to {outputFilename}")

    # print the list in markdown format `-[name](link)` on each line to a markdown file: list.md
    # list.md is in utf8 format
    with open(outputFilename, "w", encoding="utf8") as f:
        for i in range(0, len(list), 2):
            f.write(f"- [{list[i]}]({list[i+1]})\n")

if __name__ == '__main__':
    main()