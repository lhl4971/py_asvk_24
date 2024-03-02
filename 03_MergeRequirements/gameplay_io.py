import cowsay as cs
from io import StringIO
from cowsay import read_dot_cow
import random

cow = read_dot_cow(StringIO("""
$the_cow = <<EOC;
         $thoughts        
          $thoughts        
           $thoughts                                         ..vv---vvvvvv-
            $thoughts                                       --v--v----vvvvv-..
             $thoughts                                    v-v-------vv-----vvv-
              $thoughts                               -v-------------v-vvvvv---...
               $thoughts                            .-v--------..------vvvvvvv----.
                $thoughts                         vvv-..--......--------vvvvvvvv----
                 $thoughts                      ..v-...--.......-----------vvvvv--vv-.
                  $thoughts                    -v-....------.....-----------vvvvvvvvvv-
                   $thoughts                   --......-----..-------v--vvvvvvvvvvvvvvvv.
                    $thoughts                  -......-------vvvvvvvvvvvvvvvvvvvvvvvvvvvv
                     $thoughts                .-. ...-----vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
                      $thoughts              .-- ...------vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv-.
                       $thoughts             -v. ...-----vvvvvvvvvvvvvvvvvvvvvvv-vvvvvvvvv-
                        $thoughts            .-.....-----vvvvvvvvvvvvvvvvvvvvvvv---vv----v-
                         $thoughts           ..-.....----vvvvvvvvvvvvvvvvvvvvvvvv-.------v
                          $thoughts          ...   .---vvvvvvvvvvvvvvvvvvvvvvvvvv-..-----v
                                     .--   .-----.....---------....---vvvv-....--v
                                     .v-   .-............--...  ......--vv-.....-.
                                     ..-. ..-..         .---.      ...--vv-.---.-
                                       -- .--............vv-.. ...---..--vv-----v
                                       .-..------....--.-vvv.--....----vvvv--..--
                                       .--.-----vvvvv----vvv--vvvvvvv--vvvv--..-.
                                        -v.-.-------..---vvvvv---vvv----vvv--vvv.
                                        .v-.....--.. .--vvvvv--  .--------vvvvvv.
                                        . -.......  .......-. ..  ..-------vvv-..
                                          --.....   ....     ...   ....---vvvv.
                                          -......     .      ..     ...---vvv-
                                          -.......     .......     ...---vv-vv
                                          -....... .-..........-.....-------v.
                                          ..........---....------......----vv..
                                       .--. ......------....------....----.-MM.
                                       .-    ..-..-----------vvv---..----.  -M.
                                       .      ....----vvvvvvvvvvv--.---v-    --
                                  .---.        ....----------vvvv--.---v.   . ---
                              ....--.          ......-......------------    .  -v
                             --...              ........    .....-------    .   -.
                     ....--...                   .....       ....------..  ..    .-----.---.
                  .........                       ....         ...----...  ..      ......---..
                ----....                           ....        ..----..-.           .. ... ...----.
            -v--......                            ......     .....--..                       ....--v..
          .vv-.   ..                                ...............                           ......-v.
        .-v-                                           ----vvvvv-                        ..    .......-v.
EOC
"""))

def ask(prompt: str, valid: list[str] = None) -> str:
    cowname = random.choices(cs.list_cows())[0]
    word = input(cs.cowsay(prompt, cowfile=cow))
    return word

def inform(format_string: str, bulls: int, cows: int) -> None:
    cowname = random.choices(cs.list_cows())[0]
    print(cs.cowsay(format_string.format(bulls, cows), cow=cowname))