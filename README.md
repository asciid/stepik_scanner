# stepik_scanner
A scanning script to get available courses on http://stepik.org.

Scanned courses are stored in `stepik_parse.txt`.

To stop scanning just press `<Ctrl>+<C>`, and script will handle it.
All following scans will be continued where the last one was stopped.

## Dependencies
Script uses following external modules:
* `termcolor`
* `requests`
* `BeautifulSoup4`

So make sure they are installed.

Good luck!
