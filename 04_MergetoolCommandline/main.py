import cmd
import cowsay as cs
from shlex import split

class cowsay(cmd.Cmd):
    prompt = "cowsay>> "

    def do_list_cows(self, arg):
        """Lists all cow file names in the given directory"""
        print(cs.list_cows(*split(arg)))

    def do_make_bubble(self, arg):
        """
        Wraps text is wrap_text is true, then pads text and sets inside a bubble.
        This is the text that appears above the cows
        """
        print(cs.make_bubble(*split(arg)))

    def do_cowsay(self, arg):
        """
        Similar to the cowsay command. Parameters are listed with their
        corresponding options in the cowsay command. Returns the resulting cowsay
        string

        :param message: The message to be displayed
        :param cow: -f – the available cows can be found by calling list_cows
        :param preset: -[bdgpstwy]
        :param eyes: -e or eye_string
        :param tongue: -T or tongue_string
        """
        arg = split(arg)
        arg_list = {arg[i]: arg[i + 1] for i in range(0, len(arg) - 1)}
        print(
            cs.cowsay(
                arg[0], 
                cow = arg_list.get("-f") if arg_list.get("-f") else 'default', 
                eyes = arg_list.get("-e") if arg_list.get("-e") else 'oo', 
                tongue = arg_list.get("-T") if arg_list.get("-T") else '  ', 
                width = arg_list.get("-W") if arg_list.get("-W") else 40,
                preset = "-[bdgpstwy]" if arg_list.get("-[bdgpstwy]") else None
            )
        )

    def do_cowthink(self, arg):
        """
        Similar to the cowthink command. Parameters are listed with their
        corresponding options in the cowthink command. Returns the resulting
        cowthink string

        :param message: The message to be displayed
        :param cow: -f – the available cows can be found by calling list_cows
        :param preset: -[bdgpstwy]
        :param eyes: -e or eye_string
        :param tongue: -T or tongue_string
        """
        arg = split(arg)
        arg_list = {arg[i]: arg[i + 1] for i in range(0, len(arg) - 1)}
        print(
            cs.cowthink(
                arg[0], 
                cow = arg_list.get("-f") if arg_list.get("-f") else 'default', 
                eyes = arg_list.get("-e") if arg_list.get("-e") else 'oo', 
                tongue = arg_list.get("-T") if arg_list.get("-T") else '  ', 
                width = arg_list.get("-W") if arg_list.get("-W") else 40,
                preset = "-[bdgpstwy]" if arg_list.get("-[bdgpstwy]") else None
            )
        )

if __name__ == '__main__':
    cowsay().cmdloop() 