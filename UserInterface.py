from Commands import *
from Commands_Struct import *
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfile
from functools import partial
from Rectangle import *
from Ellipse import *


class UserInterface:
    TAG_NAME = 0
    TAG_ID = 1

    # GUI references
    tool_frame = None
    drawing_canvas = None
    drawing_frame = None
    shapes_listbox = None
    description_dialog_box = None
    description_input = None
    description_position = None

    # Selection helpers
    current_command = None
    selected_shape = None
    commands = None
    shapes_list = []
    group_list = []

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
        self.gui_export_button()
        self.gui_group_button()
        self.gui_description_button()

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
        self.commands = Commands(self.drawing_canvas, self.shapes_list)

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

    def gui_export_button(self):
        """
        Renders the Export button
        :return:
        """
        button = Button(self.tool_frame, text='Export', bg='#b3b3b3', command=self._export)
        button.pack(fill=BOTH)

    def gui_group_button(self):
        """
        Renders the Group button
        :return:
        """
        button = Button(self.tool_frame, text='Group', bg='#b3b3b3', command=self.group)
        button.pack(fill=BOTH)

    def gui_description_button(self):
        """
        Renders the Description button
        :return:
        """
        button = Button(self.tool_frame, text='Description', bg='#b3b3b3', command=self.description_dialog)
        button.pack(fill=BOTH)

    def shapes_listbox_get(self):
        """
        Handles the user click in the listbox, finds the shape and set the active state
        :return:
        """
        self.shapes_set_active()

    def shapes_set_all_inactive(self):
        """
        Sets all shapes to their inactive state
        :return:
        """
        for shape in self.shapes_list:
            shape.set_inactive_state()

    def shapes_set_active(self):
        """
        Sets shape at index to it's active state
        :return:
        """
        for shape in self.selected_shape:
            shape.set_active_state()

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
        if isinstance(self.selected_shape, str) or self.selected_shape is None:
            self.selected_shape = []

        selected_shapes = Commands(self.drawing_canvas, self.shapes_list).select([event.x, event.y], self.group_list)
        print(selected_shapes)
        for selected_shape in selected_shapes:
            if selected_shape in self.selected_shape:
                self.selected_shape.remove(selected_shape)
            else:
                self.selected_shape.append(selected_shape)
        self.shapes_set_all_inactive()
        self.shapes_set_active()

    def move(self, event):
        """
        Triggers the move command in Commands
        :param event:
        :return:
        """
        Commands(self.drawing_canvas, self.shapes_list).move(self.selected_shape, [event.x, event.y])

    def resize(self, event):
        """
        Triggers the resize command in Commands
        :param event:
        :return:
        """
        Commands(self.drawing_canvas, self.shapes_list).resize(self.selected_shape, [event.x, event.y])

    def undo(self):
        """
        Handles the undo button click
        Needs a predefined class instance to manipulate stack pointer
        :return:
        """
        self.commands.undo()

    def redo(self):
        """
        Handles the redo button click
        Needs a predefined class instance to manipulate stack pointer
        :return:
        """
        self.commands.redo()

    def _import(self):
        """
        Handles the import button click
        :return:
        """
        filename = askopenfilename()
        shapes = Commands(self.drawing_canvas, self.shapes_list).import_(filename)
        for shape in shapes:
            if isinstance(shape, Group):
                self.group_list.append(shape)
            else:
                self.shapes_list.append(shape)

    def _export(self):
        file = asksaveasfile('w', defaultextension='.txt')
        if file is None:
            return
        shapes = Commands(self.drawing_canvas, self.shapes_list).export_()
        file.write(shapes)
        file.close()

    def group(self):
        """
        Handles the group button click
        :return:
        """
        self.group_list.append(Commands(self.drawing_canvas, self.shapes_list).group(self.selected_shape))

    def description_dialog(self):
        """
        Opens a dialog box to enter a description and a position for that description
        :return:
        """
        if not isinstance(self.selected_shape, list):
            return

        self.description_dialog_box = Toplevel(self.master)

        description_label = Label(self.description_dialog_box, text='Description')
        description_label.pack()

        self.description_input = Entry(self.description_dialog_box)
        self.description_input.pack()

        position_label = Label(self.description_dialog_box, text='Position')
        position_label.pack()

        position_options = {'Left', 'Right', 'Top', 'Bottom'}
        self.description_position = StringVar(self.description_dialog_box)
        self.description_position.set('Bottom')
        option_menu = OptionMenu(self.description_dialog_box, self.description_position, *position_options)
        option_menu.pack()

        submit = Button(self.description_dialog_box, text='Submit', command=self.description)
        submit.pack()

    def description(self):
        """
        Handles the description
        :return:
        """
        Commands(self.drawing_canvas, self.shapes_list).description(self.selected_shape, self.description_input.get(),
                                                                    self.description_position.get())
        self.description_dialog_box.destroy()

    def remove(self, shape):
        """
        Currently no implementation, mainly a placeholder
        :param shape:
        :return:
        """
        pass
