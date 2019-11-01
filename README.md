##RegSkewer

This script is built to aid in parsing windows registry artfacts for forensics or incident response investigation rather than imaging the whole hard drive.
installing dependences

To install RegSkewer dependences run the following command on a privileged terminal:

pip3 install -r requirment.txt

###Usage

Make sure that install python3 and thre depecies mentioned on requirements.txt.RegSkewer can read diret file and logs or just specify the path for the whole collected hives. There are multiple options including webview that goes with "-w" arges once you finished parsing your artifacts. For more details (try python3 regskewer.py -h). The following is the list of argument :

usage: regskewer.py [-h] [-p PATH] [-f FILE] [-l [LOG [LOG ...]]] [-pl PLUGIN]
                  [-w] [-a] [-ls] [-v] [-k]

###optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Path to all hives
  -f FILE, --file FILE  Parse single file
  -l [LOG [LOG ...]], --log [LOG [LOG ...]]
                        Parse the log files
  -pl PLUGIN, --plugin PLUGIN
                        select single plugin
  -w, --web             View rsults in webmode
  -a, --all_plugins     select all plugins
  -ls, --list           list all plugins
  -v, --verbose         Enable verbose output
  -k, --kuiper          Enable kuiper output

####Example

Let's say you want to parse all of the artifacts that collected eariler using Horder or Kape then all you need to do is:

python3 regskewer.py -p [folder] -a

After the script finishes it will generate the results on "Results" folder located on the same foldered as regskewer.py file.

To view the result using your browser, all you have to do: python3 regskewer.py -w From the web view you can download the results with multiple format including "csv,xlsx,pdf" or even print it right away.

###Licence

    this project depends on YARP havily https://github.com/msuhanov/yarp
    GPLv3, unless mentioned otherwise.

THanks for visiting
