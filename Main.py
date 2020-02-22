from UserInterface import *


class MainCanvas(Frame):

    commands = None
    user_interface = None
    root = None

    def __init__(self, root):
        """
        :param root:
        """
        super().__init__()
        self.root = root
        self.init_ui()

    def init_ui(self):
        """
        Main application setup
        :return:
        """
        self.master.title()
        self.pack(fill=BOTH, expand=1)
        self.user_interface = UserInterface(self.root)


def main():
    """
    :return:
    """
    root = Tk()
    main_canvas = MainCanvas(root)
    root.mainloop()


if __name__ == '__main__':
    main()
