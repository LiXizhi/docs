## this is repo mirror of keepwork.com official repos

The repo is mostly used for backup and creating paracraft LLM Agent as long context. 

DO NOT Modify this repo, use the following repos official repos instead:
- https://keepwork.com/official/docs
- https://keepwork.com/official/open
- https://keepwork.com/official/paracraft
- https://keepwork.com/official/tips
- https://keepwork.com/lesson9527/codeLessons


## How to Generate Text for LLM

```
python ./build.py
```

This will generate `output.txt` in current folder. You can feed this to LLM as training data or long context. 

```
# this will generate just for a single file relative to current folder
python ./build.py  official\paracraft\docs\cmd_sendevent.md
```