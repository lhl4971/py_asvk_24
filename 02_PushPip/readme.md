usage: cow_say [-h] [-f cow] [-m preset] [-e eyes] [-T tongue] [-W width] [-n wrap_text] [-l list_cows] [-cf cowfile]
               message

This program works similarly python-cowsay

positional arguments:
  message       The message to be displayed

options:
  -h, --help    show this help message and exit
  -f cow        The available cows can be found by paramater -l
  -m preset     Presets of eyes and tongue
  -e eyes       Custom eyes string
  -T tongue     Custom tougue string
  -W width
  -n wrap_text
  -l list_cows  Lists all cow file names in the given directory
  -cf cowfile   Custom cowfile path

Similar to the cowsay command. Parameters are listed. Prints the resulting cowsay string