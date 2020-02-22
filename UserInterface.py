from Commands import *
from Commands_Struct import *
from tkinter import *
from tkinter.filedialog import askopenfilename
from functools import partial


class UserInterface:
    TAG_NAME = 0
    TAG_ID = 1

    # GUI references
    tool_frame = None
    drawing_canvas = None
    drawing_frame = None
    shapes_listbox = None

    # Selection helpers
    current_command = None
    selected_shape = None
    is_multi_selection = False
    commands = None
    shapes_list = []

    # drag start and stop coordinates
    motion_start_coordinates = [0, 0]
    motion_end_coordinates = [0, 0]

    def __init__(self, master):
        """
        Constructor
        :param master:
        """
        self.master = master
        self.draw_tools()

    def draw_tools(self):
        """
        Setup all the GUI elements
        :return:
        """
        # container for tools
        self.create_tool_frame()
        # container for drawing pane
        self.create_drawing_frame()

        # create buttons
        self.gui_rectangle_button()
        self.gui_ellipse_button()
        self.gui_select_button()
        self.gui_move_button()
        self.gui_resize_button()
        self.gui_undo_button()
        self.gui_redo_button()
        self.gui_import_button()

        # shapes listbox
        self.gui_shapes_listbox()

        # event listeners
        self.event_listeners()

    def event_listeners(self):
        """
        Setup all the event listeners on global level
        :return:
        """
        self.drawing_canvas.bind('<Button-1>', self.mouse_button_down)
        self.drawing_canvas.bind('<ButtonRelease-1>', self.mouse_button_up)
        self.master.bind('<KeyPress>', self.key_down)
        self.master.bind('<KeyRelease>', self.key_up)

    def mouse_button_down(self, event):
        """
        Handles the mouse button down event
        :param event:
        :return:
        """
        self.motion_start_coordinates = [event.x, event.y]

    def mouse_button_up(self, event):
        """
        Handles the mouse button up event
        :param event
        """
        self.motion_end_coordinates = [event.x, event.y]
        if self.commands.get_current_command() is COMMAND_CREATE:
            if self.selected_shape is Rectangle.name:
                rectangle = self.create(Rectangle.name, self.motion_start_coordinates + self.motion_end_coordinates)
                self.shapes_list.insert(0, rectangle)  # do a push
                self.shapes_listbox_add(Rectangle.name)
            elif self.selected_shape is Ellipse.name:
                ellipse = self.create(Ellipse.name, self.motion_start_coordinates + self.motion_end_coordinates)
                self.shapes_list.insert(0, ellipse)  # do a push
                self.shapes_listbox_add(Ellipse.name)
        elif self.commands.get_current_command() is COMMAND_SELECT:
            self.select(event)
        elif self.commands.get_current_command() is COMMAND_MOVE:
            self.move(event)
        elif self.commands.get_current_command() is COMMAND_RESIZE:
            self.resize(event)

    def key_down(self, event):
        """
        Handles the key press down event
        :param event:
        :return None:
        """
        if event.keycode == 16:  # right of left shift
            self.is_multi_selection = True

    def key_up(self, event):
        """
        Handles the key press up event
        :param event:
        :return None:
        """
        if event.keycode == 16:  # right of left shift
            self.is_multi_selection = False

    def create_tool_frame(self):
        """
        Renders a frame for the tool buttons to be stored in
        :return:
        """
        self.tool_frame = Frame(self.master, height=800, width=200, bg='#dbdbdb')
        self.tool_frame.pack_propagate(0)
        self.tool_frame.pack(side=LEFT, expand=0)

    def create_drawing_frame(self):
        """
        Renders the drawing frame and initializes the Commands object
        :return:
        """
        self.drawing_frame = Frame(self.master, height=800, width=1240)
        self.drawing_frame.pack_propagate(0)
        self.drawing_frame.pack(side=RIGHT, expand=0)
        self.drawing_canvas = Canvas(self.drawing_frame)
        self.drawing_canvas.pack(fill=BOTH, expand=1)
        self.commands = Commands(self.drawing_canvas)

    def gui_rectangle_button(self):
        """
        Renders the Rectangle button
        :return:
        """
        button = Button(self.tool_frame, text='Rectangle', bg='#b3b3b3',
                        command=partial(self.set_shape, Rectangle.name))
        button.pack(fill=BOTH)

    def gui_ellipse_button(self):
        """
        Renders the Ellipse button
        :return:
        """
        button = Button(self.tool_frame, text='Ellipse', bg='#b3b3b3',
                        command=partial(self.set_shape, Ellipse.name))
        button.pack(fill=BOTH)

    def gui_select_button(self):
        """
        Renders the Select button
        :return:
        """
        button = Button(self.tool_frame, text='Select', bg='#b3b3b3',
                        command=partial(self.set_command, COMMAND_SELECT))
        button.pack(fill=BOTH)

    def gui_shapes_listbox(self):
        """
        Renders the shapes Listbox and binds the ListboxSelect event
        :return:
        """
        frame = Frame(self.tool_frame)
        scrollbar = Scrollbar(frame, orient=VERTICAL)
        self.shapes_listbox = Listbox(frame, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.shapes_listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.shapes_listbox.pack(side=LEFT, fill=BOTH, expand=1)
        frame.pack(side=BOTTOM, fill=BOTH, expand=0)
        self.shapes_listbox.bind('<<ListboxSelect>>', self.shapes_listbox_get)

    def gui_move_button(self):
        """
        Renders the Move button
        :return:
        """
        button = Button(self.tool_frame, text='Move', bg='#b3b3b3',
                        command=partial(self.set_command, COMMAND_MOVE))
        button.pack(fill=BOTH)

    def gui_resize_button(self):
        """
        Renders the Resize button
        :return:
        """
        button = Button(self.tool_frame, text='Resize', bg='#b3b3b3',
                        command=partial(self.set_command, COMMAND_RESIZE))
        button.pack(fill=BOTH)

    def gui_undo_button(self):
        """
        Renders the Undo button
        :return:
        """
        button = Button(self.tool_frame, text='Undo', bg='#b3b3b3', command=self.undo)
        button.pack(fill=BOTH)

    def gui_redo_button(self):
        """
        Renders the Undo button
        :return:
        """
        button = Button(self.tool_frame, text='Redo', bg='#b3b3b3', command=self.redo)
        button.pack(fill=BOTH)

    def gui_import_button(self):
        """
        Renders the Import button
        :return:
        """
        button = Button(self.tool_frame, text='Import', bg='#b3b3b3', command=self._import)
        button.pack(fill=BOTH)

    def shapes_listbox_get(self, event):
        """
        Handles the user click in the listbox, finds the shape and set the active state
        :param event:
        :return:
        """
        widget = event.widget
        index = int(widget.curselection()[0])
        self.shapes_set_active()

    def shapes_set_all_inactive(self):
        """
        Sets all shapes to their inactive state
        :return:
        """
        for shape in range(0, self.shapes_listbox.size()):
            self.shapes_list[shape].set_inactive_state()

    def shapes_set_active(self):
        """
        Sets shape at index to it's active state
        :return:
        """
        for shape in self.selected_shape:
            shapes_max_index = self.drawing_canvas.find_all()[0] + len(self.drawing_canvas.find_all()) - 1
            shape_index = self.drawing_canvas.find_withtag(shape)[0]
            self.shapes_list[shapes_max_index - shape_index].set_active_state()

    def shapes_listbox_add(self, shape):
        """
        Adds an shape to the listbox
        :param shape:
        :return:
        """
        self.shapes_listbox.insert(0, shape)

    def shapes_listbox_pop(self, index):
        """
        Removes an shape from the listbox
        :param index:
        :return:
        """
        self.shapes_list.insert(0, self.shapes_list.pop(self.shapes_list.index(index)))

    def set_shape(self, shape):
        """
        Handles the Ellipse/Rectangle button click
        :param shape:
        :return:
        """
        self.commands.set_current_command(COMMAND_CREATE)
        self.selected_shape = shape

    def create(self, shape, coordinates):
        """
        Triggers the create command in Commands
        :param shape:
        :param coordinates:
        :return:
        """
        return Commands.create(self.commands, shape, coordinates)

    def set_command(self, command):
        """
        Sets the current command in Commands object
        :param command:
        :return:
        """
        self.commands.set_current_command(command)

    def select(self, event):
        """
        Triggers the select command in Commands
        Allows for multi selection
        :param event:
        :return:
        """
        if self.is_multi_selection:
            if isinstance(self.selected_shape, str):
                self.selected_shape = []  # parse to list to allow multi selection
            self.selected_shape += [Commands.select(self.commands, [event.x, event.y])[self.TAG_ID]]
        else:
            self.selected_shape = [Commands.select(self.commands, [event.x, event.y])[self.TAG_ID]]
        self.shapes_set_all_inactive()
        self.shapes_set_active()

    def move(self, event):
        """
        Triggers the move command in Commands
        :param event:
        :return:
        """
        for shape in self.selected_shape:
            Commands.move(self.commands, shape, [event.x, event.y])

    def resize(self, event):
        """
        Triggers the resize command in Commands
        :param event:
        :return:
        """
        for shape in self.selected_shape:
            Commands.resize(self.commands, shape, [event.x, event.y])

    def undo(self):
        """
        Handles the undo button click
        :return:
        """
        Commands(self.drawing_canvas).undo()
        self.shapes_set_active()

    def redo(self):
        """
        Handles the redo button click
        :return:
        """
        Commands(self.drawing_canvas).redo()
        self.shapes_set_active()

    def _import(self):
        """
        Handles the import button click
        :return:
        """
        filename = askopenfilename()
        Commands(self.drawing_canvas).import_(filename)

    def remove(self, shape):
        """
        Currently no implementation, mainly a placeholder
        :param shape:
        :return:
        """
        pass
