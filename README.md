# stepik_scanner
A scanning script to get available courses on http://stepik.org.

Scanned courses are stored in `stepik_courses.txt`.

To stop scanning just press `<Ctrl>+<C>`, and script will handle it.
All following scans will be continued where the last one was stopped.

## Downloads

Check out the Releases to get the latest version.

## Dependencies
Script uses following external modules:
* `termcolor`
* `requests`
* `BeautifulSoup4`

So make sure they are installed.

## Troubleshooting
**Dear Windows users**! Scanner was made for Linux users and in Linux and I made a Win binary just to let it be as the most of the users are Win-boys.

**!!!PLEASE, CLOSE PARSER.PY WITH CTRL+C. CLOSING THE CONSOLE WINDOW WON'T LET A LAST POSITION TO BE SAVED!!!**
