# stepik_scanner
A scanning script to get available courses on http://stepik.org.

Scanned courses are stored in `stepik_parse.txt`.

To stop scanning just press `<Ctrl>+<C>`, and script will handle it.
All following scans will be continued where the last one was stopped.

## Downloads

* Windows (x64) binary (24/04/2020) ==> [parser.exe](https://github.com/asciid/stepik_scanner/raw/bin/parser-win64-24062020.exe)
* Linux (amd64) binary (24/04/2020) ==> [parser.run](https://github.com/asciid/stepik_scanner/raw/bin/parser-linux_x64-24062020.run)

## Dependencies
Script uses following external modules:
* `termcolor`
* `requests`
* `BeautifulSoup4`

So make sure they are installed.

## Troubleshooting
**Dear Windows users**! Scanner was made for Linux users and in Linux and I made a Win binary just to let it be as the most of the users are Win-boys.

**!!!PLEASE, CLOSE PARSER.PY WITH CTRL+C. CLOSING THE CONSOLE WINDOW WON'T LET A LAST POSITION TO BE SAVED!!!**

And if you see something like:

`Blah-blah-blah: get_position() -- index out of range`

It means that the last time you shut the programm down not properly. You are a dick.

Delete `.stepik_scan file` in the directory of a binary, restart it and never do the same again.

Good luck!
