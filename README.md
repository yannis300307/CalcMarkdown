# **CalcMardown**
CalcMarkdown is a python script that is able to read markdown documents and display them on your calculator with the markdown formating.

You can download the script on your calculator [on the numworks website](https://my.numworks.com/python/yannis300307/calcmd).

## Features
It supports basic mardown formating:
- Titles
- Titles 2
- Titles 3
- Bold text
- Strike text

I will implement more syntax in the future.

**The markdown parser is not perfectly acurate!** 

It is not currently able to process a lot of features such as lists, italic text or escaping formating characters.

## Compatibility
The script has been tested on N0110 and it seems to crash on emulator.

You should not try to open the script directly on your calculator because It makes the code editor very buggy due to very looooong line.

## How to use?
Download the script on your calculator and create another Python script with the name of your choise. 

In this file, type `doc="""markdown"""`. Replace `markdown` with you markdown document. You can use line returns.
Next, run calcmd.py and give the python file name as the document name (without the `.py`) and your document is displayed!
