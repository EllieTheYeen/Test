# Test

Just testing some random stuff  
[Junk](/Junk.md)

Will an embed appear below?

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=./blogpost.py) -->
<!-- The below code snippet is automatically added from ./blogpost.py -->
```py
#!/usr/bin/python3
import datetime
import pathlib
import os

fdir = pathlib.Path(__file__).parent.absolute()
#fdir = os.path.abspath(os.path.split(__file__)[0])
if not fdir.samefile(os.getcwd()):
    os.chdir(fdir)

title = input('Title: ')
if not title:
    exit('No title specified. Exiting')

ftitle = title.strip().replace(' ', '-')
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2)))

shor = now.strftime("%Y-%m-%d")
long = now.strftime(
    "%Y-%m-%d %H:%M:%S %z"
)

fn = pathlib.Path(f'_posts/{shor}-{ftitle}.md')

template = """
---
layout: post
date:   {now:%Y-%m-%d %H:%M:%S %z}
title:  {title}
---
""".strip()

temp = template.format(now=now, title=title)
fn.write_text(temp)
print(fn)

if not os.environ.get('EDITOR'):
    os.environ['EDITOR'] = 'nano'
os.system(f'$EDITOR {fn}')

posttext = fn.read_text()

if posttext == temp:
    fn.unlink()
    exit('post was not written')
```
<!-- MARKDOWN-AUTO-DOCS:END -->
