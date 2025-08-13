"""
FT Connect Attribute Tool for Maya.

This tool provides a GUI for quickly connecting attributes between objects in Maya.
It allows for connecting one driver attribute to multiple driven attributes at once.
"""

import maya.cmds as cmds


class ConnectAttrUI:
    """Class to handle the Connect Attribute tool UI and functionality."""

    WINDOW_NAME = 'FTConnectAttrUI'
    WINDOW_TITLE = 'FT Connect Attribute v1.0'

    def __init__(self):
        """Initialize the UI class."""
        self.driver_field = None
        self.driven_list = None
        self.create_ui()

    def create_ui(self):
        """Create the main UI window and its elements."""
        # Delete existing window if it exists
        if cmds.window(self.WINDOW_NAME, exists=True):
            cmds.deleteUI(self.WINDOW_NAME)

        # Create main window
        cmds.window(
            self.WINDOW_NAME,
            title=self.WINDOW_TITLE,
            widthHeight=(300, 400),
            minimizeButton=False
        )

        # Create main layout
        main_layout = cmds.formLayout()

        # Create UI elements
        driver_label = cmds.text(label='Driver:')
        self.driver_field = cmds.textField()
        driver_button = cmds.button(
            label='<<',
            annotation='Set the Selected as Driver Attribute',
            command=self.get_driver_attr
        )

        driven_label = cmds.text(label='Driven:')
        self.driven_list = cmds.textScrollList(
            allowMultiSelection=True,
            height=200
        )
        add_button = cmds.button(
            label='Add',
            annotation='Add Selected as Driven Attribute',
            command=self.add_driven_attr
        )
        remove_button = cmds.button(
            label='Remove',
            annotation='Remove Selected Driven Attribute',
            command=self.remove_driven_attr
        )
        connect_button = cmds.button(
            label='Connect All',
            annotation='Connect All Attributes',
            command=self.connect_all_attr
        )

        # Layout positioning
        cmds.formLayout(
            main_layout,
            edit=True,
            attachForm=[
                (driver_label, 'left', 2),
                (driver_label, 'top', 4),
                (driver_button, 'right', 2),
                (driver_button, 'top', 2),
                (driven_label, 'left', 2),
                (self.driven_list, 'left', 2),
                (self.driven_list, 'right', 2),
                (add_button, 'left', 2),
                (remove_button, 'right', 2),
                (connect_button, 'left', 2),
                (connect_button, 'right', 2),
            ],
            attachControl=[
                (self.driver_field, 'left', 2, driver_label),
                (self.driver_field, 'right', 2, driver_button),
                (driver_button, 'left', 2, self.driver_field),
                (driven_label, 'top', 14, driver_label),
                (self.driven_list, 'top', 7, driven_label),
                (add_button, 'top', 2, self.driven_list),
                (remove_button, 'top', 2, self.driven_list),
                (connect_button, 'top', 3, add_button),
            ],
            attachPosition=[
                (self.driver_field, 'right', 0, 80),
                (add_button, 'right', 0, 49),
                (remove_button, 'left', 0, 51),
            ]
        )

        cmds.showWindow(self.WINDOW_NAME)

    def get_driver_attr(self, *args):
        """Get the selected attribute as driver."""
        try:
            selected_objects = cmds.ls(selection=True)
            channel_box_attrs = cmds.channelBox(
                'mainChannelBox',
                query=True,
                selectedMainAttributes=True
            )

            if not selected_objects or not channel_box_attrs:
                raise ValueError("Please select an object and attribute")

            if len(selected_objects) > 1 or len(channel_box_attrs) > 1:
                raise ValueError("Please select only one object and attribute")

            attr_path = f"{selected_objects[0]}.{channel_box_attrs[0]}"
            cmds.textField(self.driver_field, edit=True, text=attr_path)

        except Exception as e:
            cmds.error(str(e))

    def add_driven_attr(self, *args):
        """Add selected attributes to the driven list."""
        try:
            selected_objects = cmds.ls(selection=True)
            channel_box_attrs = cmds.channelBox(
                'mainChannelBox',
                query=True,
                selectedMainAttributes=True
            )

            if not selected_objects or not channel_box_attrs:
                raise ValueError("Please select objects and attributes")

            # Get existing items to check for duplicates
            existing_items = cmds.textScrollList(
                self.driven_list,
                query=True,
                allItems=True
            ) or []

            # Add new attributes
            for obj in selected_objects:
                for attr in channel_box_attrs:
                    attr_path = f"{obj}.{attr}"
                    if attr_path not in existing_items:
                        cmds.textScrollList(
                            self.driven_list,
                            edit=True,
                            append=attr_path
                        )

        except Exception as e:
            cmds.error(str(e))

    def remove_driven_attr(self, *args):
        """Remove selected attributes from the driven list."""
        try:
            selected_items = cmds.textScrollList(
                self.driven_list,
                query=True,
                selectItem=True
            )

            if selected_items:
                for item in selected_items:
                    cmds.textScrollList(
                        self.driven_list,
                        edit=True,
                        removeItem=item
                    )

        except Exception as e:
            cmds.error(str(e))

    def connect_all_attr(self, *args):
        """Connect the driver attribute to all driven attributes."""
        try:
            driver_attr = cmds.textField(self.driver_field, query=True, text=True)
            driven_attrs = cmds.textScrollList(
                self.driven_list,
                query=True,
                allItems=True
            )

            if not driver_attr:
                raise ValueError("No driver attribute specified")
            if not driven_attrs:
                raise ValueError("No driven attributes specified")

            for driven_attr in driven_attrs:
                cmds.connectAttr(driver_attr, driven_attr)
                print(f"Connected {driver_attr} to {driven_attr}")

        except Exception as e:
            cmds.error(str(e))


def show_window():
    """Show the Connect Attribute window."""
    ConnectAttrUI()


if __name__ == "__main__":
    show_window()