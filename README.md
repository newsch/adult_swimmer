# adult_swimmer
A Python script to check for updates to https://www.asseenonadultswim.com.

## Getting Started
1. Make sure you have the [required libraries](requirements.txt) installed.
2. Set up an IFTTT channel (used here) or something similar if you want push notifications.
    1. Connect a [Maker webhook trigger](https://ifttt.com/maker_webhooks) with whatever you want (I used [push notifications]).
    2. Make a copy of the [sample configuration file](sample_config.yaml) called _config.yaml_ and add your webhook info.
3. Run _as_checker.py_ - output is saved to _log.txt_.
4. Add it to your Cron file to run it periodically (if using a Unix-like system).
    1. Edit your Cron file with `crontab -e`.
    2. Add a line similar to `@daily /full/path/to/as_checker.py` (This one runs daily - more about Cron [here](https://en.wikipedia.org/wiki/Cron)).
    3. Make sure the script is executable with `chmod a+x as_checker.py`.


## Useful Resources
Readings that helped me, roughly grouped by topic and arranged in the order I googled them
- [Loading settings from a configuration file](https://martin-thoma.com/configuration-files-in-python/)
- [Pickling section from Olin's Software Design course](https://sd17spring.github.io//toolboxes/pickling/)
- [Pickling docs](https://docs.python.org/3.5/library/pickle.html?highlight=pickling#module-pickle)
- [Python logging docs](https://docs.python.org/3.5/howto/logging.html)
- [Using Cron to schedule this script](https://en.wikipedia.org/wiki/Cron)
- [Comparing objects](http://stackoverflow.com/questions/1227121/compare-object-instances-for-equality-by-their-attributes-in-python#1227325)
- [Rich comparison docs](https://docs.python.org/3/reference/datamodel.html#object.__eq__)
- [Beautiful Soup docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [A quick introduction to debugging in Python](https://pythonconquerstheuniverse.wordpress.com/2009/09/10/debugging-in-python/)
- [Stackoverflow with more pdb resources](http://stackoverflow.com/questions/4228637/getting-started-with-the-python-debugger-pdb)
- [Maker webhooks for IFTTT](https://ifttt.com/maker_webhooks)
