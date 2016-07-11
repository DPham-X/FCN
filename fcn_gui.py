"""Fake Classifier Node Graphical User Interface
- Send FCN Messages Easily

"""
import sys
import binascii

from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QApplication

from fcn import FCN


class FCNGui(QWidget):
    """FCN GUI
    Creates FCN GUI using the existing FCN modules

    """
    # Default values
    protocol = 6
    host_protocol = 'TCP'
    msg_type = 0

    def get_var(self):
        """Gets the variables from the GUI

        Returns
        -------
        The class containing all the parameters in the same format as the CLI
        """
        class ImportVariables:
            """Contains the FCN parameters

            """
            # Try get IPs and Ports
            try:
                srcip = str(self.source_ip_edit.text())
            except RuntimeError:
                pass
            try:
                destip = str(self.destination_ip_edit.text())
            except RuntimeError:
                pass
            try:
                srcport = int(self.source_port_edit.text())
            except RuntimeError:
                pass
            try:
                destport = int(self.destination_port_edit.text())
            except RuntimeError:
                pass

                # Get the rest of the parameters
                seq_no = int(self.seq_no_edit.text())
                prototype = self.protocol
                msgtype = self.msg_type
                timeoutval = int(self.timeout_val_edit.text())
                export = str(self.export_name_edit.text())
                mclass = str(self.class_name_edit.text())
                prio = int(self.priority_edit.text())
                HOST = str(self.host_ip_edit.text())
                PORT = int(self.host_port_edit.text())
                PROTO = self.host_protocol
                a_flg = 0

        return ImportVariables

    def __init__(self, parent=None):
        """Main function

        """
        super(FCNGui, self).__init__(parent)
        # Title
        title_name = 'Fake Classifier Node GUI'

        # Create Grid
        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        # Set Layout parameters
        self.setLayout(self.grid)
        self.setGeometry(300, 300, 1024, 300)
        self.setWindowTitle(title_name)
        self.show()

        # Run UI settings
        self.header_ui()
        self.main_ui()
        self.message_type_dropdown()

        # Send button handler
        self.send_button.clicked.connect(self.send_message_handler)

    def header_ui(self):
        """Creates the header UI labels
        """
        tuple_label = QLabel('Match 5-tuple Parameters')
        self.grid.addWidget(tuple_label, 0, 0)

        setting_label = QLabel('Settings')
        self.grid.addWidget(setting_label, 0, 2)

        host_label = QLabel('Host Settings')
        self.grid.addWidget(host_label, 0, 4)

    def message_type_dropdown(self):
        """Creates the message type drop down menu

        """
        msg_type_dropdown = QComboBox(self)
        self.grid.addWidget(msg_type_dropdown, 2, 3)
        msg_type_dropdown.addItems(["Add",
                                    "Delete Matching",
                                    "Delete All IP"])
        msg_type_dropdown.activated[str].connect(self.msg_type_dropdown_active)

    def main_ui(self):
        """Creates all the parameter UI elements


        """
        # Initiate Widgets
        self.tuple_widgets()
        self.settings_widgets()
        self.host_widgets()

        # Send Button
        self.send_button = QPushButton("Send", self)
        self.grid.addWidget(self.send_button, 7, 6)
        self.send_button.setEnabled(True)

    def tuple_widgets(self):
        """Creates tuple widgets


        """
        # 1st Column Labels
        source_ip_label = QLabel('Source IP')
        destination_ip_label = QLabel('Destination IP')
        source_port_label = QLabel('Source Port')
        destination_port_label = QLabel('Destination Port')
        protocol_label = QLabel('Protocol')

        # 2nd Column edit box
        self.source_ip_edit = QLineEdit()
        self.destination_ip_edit = QLineEdit()
        self.source_port_edit = QLineEdit()
        self.destination_port_edit = QLineEdit()

        # Dropdown for protocol
        protocol_dropdown = QComboBox(self)
        protocol_dropdown.addItem("TCP")
        protocol_dropdown.addItem("UDP")
        protocol_dropdown.addItem("ICMP")
        protocol_dropdown.activated[str].connect(self.protocol_dropdown_active)

        # Add Tuple Widgets
        self.grid.addWidget(source_ip_label, 1, 0)
        self.grid.addWidget(self.source_ip_edit, 1, 1)

        self.grid.addWidget(destination_ip_label, 2, 0)
        self.grid.addWidget(self.destination_ip_edit, 2, 1)

        self.grid.addWidget(source_port_label, 3, 0)
        self.grid.addWidget(self.source_port_edit, 3, 1)

        self.grid.addWidget(destination_port_label, 4, 0)
        self.grid.addWidget(self.destination_port_edit, 4, 1)

        self.grid.addWidget(protocol_label, 5, 0)
        self.grid.addWidget(protocol_dropdown, 5, 1)

        self.source_port_edit.setDisabled(False)
        self.destination_port_edit.setDisabled(False)

    def settings_widgets(self):
        """Creates settings widgets

        """
        # 3rd Column Labels
        seq_no_label = QLabel('Sequence Number')
        msg_type_label = QLabel('Message Type')
        timeout_val_label = QLabel('Timeout Value')
        export_name_label = QLabel('Export Name')
        class_name_label = QLabel('Class Name')
        priority_label = QLabel('Priority')

        # Settings Widgets
        self.seq_no_edit = QLineEdit('1')
        self.timeout_val_edit = QLineEdit('60')
        self.export_name_edit = QLineEdit('myexp')
        self.class_name_edit = QLineEdit('myclass')
        self.priority_edit = QLineEdit('0')

        # Add Settings Widgets Labels
        self.grid.addWidget(seq_no_label, 1, 2)
        self.grid.addWidget(msg_type_label, 2, 2)
        self.grid.addWidget(timeout_val_label, 3, 2)
        self.grid.addWidget(export_name_label, 4, 2)
        self.grid.addWidget(class_name_label, 5, 2)
        self.grid.addWidget(priority_label, 6, 2)

        # Add Settings Widgets
        self.grid.addWidget(self.seq_no_edit, 1, 3)
        self.grid.addWidget(self.timeout_val_edit, 3, 3)
        self.grid.addWidget(self.export_name_edit, 4, 3)
        self.grid.addWidget(self.class_name_edit, 5, 3)
        self.grid.addWidget(self.priority_edit, 6, 3)

        # Default placeholder
        self.source_ip_edit.setPlaceholderText('Eg. 10.0.0.1')
        self.destination_ip_edit.setPlaceholderText('Eg. 10.0.0.1')
        self.source_port_edit.setPlaceholderText('Eg. 80')
        self.destination_port_edit.setPlaceholderText('Eg. 80')

    def host_widgets(self):
        """Creates Host widgets

        """
        # 5th Column Labels
        host_ip_label = QLabel('Host IP')
        host_port_label = QLabel('Host Port')
        host_protocol_label = QLabel('Host Protocol')

        # Host Widgets
        self.host_ip_edit = QLineEdit()
        self.host_port_edit = QLineEdit()
        host_protocol_dropdown = QComboBox(self)
        host_protocol_dropdown.addItem("TCP")
        host_protocol_dropdown.addItem("UDP")
        host_protocol_dropdown.activated[
            str].connect(self.host_protocol_active)

        # Add Host Widgets Label
        self.grid.addWidget(host_ip_label, 1, 4)
        self.grid.addWidget(host_port_label, 2, 4)
        self.grid.addWidget(host_protocol_label, 3, 4)

        # Add Host Widgets
        self.grid.addWidget(self.host_ip_edit, 1, 5)
        self.grid.addWidget(self.host_port_edit, 2, 5)
        self.grid.addWidget(host_protocol_dropdown, 3, 5)

    def protocol_dropdown_active(self, text):
        """Disables/Enabled the match ports depending on protocol type
        Parameters
        ----------
        text:
            The protocol

        """
        # Enables ports if TCP
        if text == 'TCP':
            self.protocol = 6
            self.source_port_edit.setDisabled(False)
            self.destination_port_edit.setDisabled(False)
        # Enables ports if UDP
        elif text == 'UDP':
            self.protocol = 17
            self.source_port_edit.setDisabled(False)
            self.destination_port_edit.setDisabled(False)
        # Disables ports if ICMP
        else:
            self.protocol = 1
            self.source_port_edit.setDisabled(True)
            self.destination_port_edit.setDisabled(True)

    def host_protocol_active(self, text):
        """Checks if the current host protocol is TCP or UDP

        Parameters
        ----------
        text:
            The dropdown host protocol

        Returns
        -------
        host_protocol:
            The host protocol
        """
        if text == 'TCP':
            self.host_protocol = 'TCP'
        elif text == 'UDP':
            self.host_protocol = 'UDP'

    def msg_type_dropdown_active(self, text):
        """Checks the current message type

        Parameters
        ----------
        text:
            The message type
        Returns
        -------
        msg_type:
            The message type number

        """
        if text == 'Add':
            self.msg_type = 0
        elif text == 'Delete Matching':
            self.msg_type = 1
        elif text == 'Delete All IP':
            self.msg_type = 2

    def send_message_handler(self):
        """Sends the FCN message when Send button is pressed

        """
        # Get HOST IP and PORT
        host_ip = self.host_ip_edit.text()
        host_port = self.host_port_edit.text()
        # Check if HOST and PORT have inputs
        if host_ip == '' or host_port == '':
            QMessageBox.information(self, 'Empty Field', "Need Host Inputs.")
            return
        else:
            # Get Parameter Inputs
            inputs = self.get_var()

            # Defaults values
            if inputs.srcip == '':
                inputs.srcip = '0.0.0.0'
            if inputs.destip == '':
                inputs.destip = '0.0.0.0'
            if 'srcport' not in inputs.__dict__:
                inputs.srcport = 0
            if 'destport' not in inputs.__dict__:
                inputs.destport = 0

            # Instantiate FCN Modules without __init__
            fake = FCN.__new__(FCN)

            # Parse Variables
            c_msg = fake.create_msg_payload(cli_inputs=inputs)
            c_temp = fake.create_template(payload_len=len(c_msg))
            c_header = fake.create_header(cli_inputs=inputs,
                                          payload_len=len(c_msg),
                                          template_len=len(c_temp))

            # Create message
            message = binascii.a2b_hex(c_header + c_temp + c_msg)

            # Send Message
            fake.send_message(message, inputs)


if __name__ == '__main__':
    APPLICATION = QApplication(sys.argv)

    SCREEN = FCNGui()
    SCREEN.show()

    sys.exit(APPLICATION.exec_())
