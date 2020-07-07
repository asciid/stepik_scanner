# stepik_scanner
A scanning script to get available courses on http://stepik.org.

Scanned courses are stored in `stepik_courses.txt`.

Markdown output is available by using `--markdown` or `-m` flag.

`--help` for the desctiption is also available.

To stop scanning just press `<Ctrl>+<C>`, and script will handle it.
All following scans will be continued where the last one was stopped.

## Downloads

Check out the Releases to get the latest version.

## Dependencies
If you want to build the scanner youeself or use it raw, script uses following external modules:
* `termcolor`
* `requests`
* `BeautifulSoup4`

Make sure they are installed.

## Troubleshooting
**Dear Windows users**! Scanner was made for \*nix and in \*nix. It is console oreinted and I can't take into account all the troubles that can happend in Windows. Don't be evil! Just make an issue if something goes wrong. 

Finally, I've fixed the position saving issue so feel free to terminate the code however you like.
