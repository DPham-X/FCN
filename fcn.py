#!/usr/local/bin/python
""" Fake Classifier Node
Creates Remote Action Protocol Messages using the Command Line Interface

Parameters
----------
-h, --help            show this help message and exit
-i Source IP, --srcip Source IP
                                The Source IP address in x.x.x.x format
-j Destination IP, --destip Destination IP
                                Destination IP address in x.x.x.x format
-s Sequence Number, --seqno Sequence Number
                                Sequence Number
-k Source port, --srcport Source port
                                Source port 1-65535
-l Destination port, --destport Destination port
                                Destination port 1-65535
-u Protocol Type, --prototype Protocol Type
                                Protocol Type (Default: TCP)
                                1: ICMP
                                2: IGMP
                                3: GGP
                                4: IPENCAP
                                5: ST2
                                6: TCP
                                17: UDP
-a Msg Type, --mtype Msg Type
                                0: Add (Default)
                                1: Remove
                                2: Remove All
-t Timeout Value, --timeoutval Timeout Value
                                Timeout value in seconds (Default: 60)
-e Export, --export Export
                                Name of export (Default: myexp)
-c Class, --class Class
                                Name of class (Default: myclass)
-n Priority, --prio Priority
                                Table Priority (Default: 1)
-x Host, --host Host
                                Action Node IP (Default: 127.0.0.1)
-y Port, --port Port
                                Output Port to Action Node (Default: 5000)
-z Proto, --proto Proto
                                Protocol to Action Node (Default: UDP)
"""

# Import dependencies
import socket
import sys
import time
import binascii
import argparse


class FCN:

    def __init__(self):
        # Get command line inputs
        inputs = self.parser()

        # Serialise data
        c_msg = self.create_msg_payload(cli_inputs=inputs)
        c_temp = self.create_template(payload_len=len(c_msg))
        c_header = self.create_header(cli_inputs=inputs,
                                      payload_len=len(c_msg),
                                      template_len=len(c_temp))

        # Convert to byte hex
        rap = binascii.a2b_hex(c_msg + c_temp + c_header)

        # Send RAP message
        self.send_message(rap, inputs)

    def create_msg_payload(self, cli_inputs):
        """Serialises the parameters for the RAP packet

        Parameters
        ----------
        cli_inputs:
            The imported command line interface inputs

        Returns
        -------
        msg:
            The parameters and data about made by a classifier

        """
        packet_count = 0
        kbyte_count = 0

        # Check the message variables
        msg_type = self.msg_type_check(cli_inputs.msgtype)
        prototype = self.prototype_check(cli_inputs.prototype)
        export_name = self.export_name_check(cli_inputs.export)
        table_priority = self.priority_check(cli_inputs.prio)
        source_port = self.port_check(cli_inputs.srcport)
        destination_port = self.port_check(cli_inputs.destport)
        class_name = cli_inputs.mclass

        # Create & Check Source IP
        try:
            source_ip = self.ip_check(cli_inputs.srcip)
            source_ip = source_ip.split('.')
            for i, j in enumerate(source_ip):
                source_ip[i] = int(j)
        except IndexError:
            sys.exit('Error: Invalid Source IP address detected')

        # Create & Check Destination IP
        try:
            destination_ip = self.ip_check(cli_inputs.destip)
            destination_ip = destination_ip.split('.')
            for i, j in enumerate(destination_ip):
                destination_ip[i] = int(j)
        except IndexError:
            sys.exit('Error: Invalid Source IP address detected')

        # Assign data variables from CLI
        o_export_name = export_name.encode('hex').ljust(16, '0')
        o_msg_type = self.convert_to_hexbyte(msg_type, 1)
        o_source_ip = (self.convert_to_hexbyte(source_ip[0], 1) +
                       self.convert_to_hexbyte(source_ip[1], 1) +
                       self.convert_to_hexbyte(source_ip[2], 1) +
                       self.convert_to_hexbyte(source_ip[3], 1))
        o_destination_ip = (self.convert_to_hexbyte(destination_ip[0], 1) +
                            self.convert_to_hexbyte(destination_ip[1], 1) +
                            self.convert_to_hexbyte(destination_ip[2], 1) +
                            self.convert_to_hexbyte(destination_ip[3], 1))
        o_source_port = self.convert_to_hexbyte(source_port, 2)
        o_destination_port = self.convert_to_hexbyte(destination_port, 2)
        o_protocol = self.convert_to_hexbyte(prototype, 1)
        o_packet_count = self.convert_to_hexbyte(packet_count, 4)
        o_kbyte_count = self.convert_to_hexbyte(kbyte_count, 4)
        o_classname_len = self.convert_to_hexbyte(len(class_name) + 4, 1)
        o_classname = class_name.encode('hex').ljust(
            len(cli_inputs.mclass) * 2 + 4, '0')
        o_table_priority = self.convert_to_hexbyte(table_priority, 1)
        o_timeout_type = self.convert_to_hexbyte(0, 1)
        o_timeout_value = self.convert_to_hexbyte(cli_inputs.timeoutval, 2)
        o_action = self.convert_to_hexbyte(0, 8)
        o_action_flag = self.convert_to_hexbyte(cli_inputs.a_flg, 2)
        o_action_parameter = self.convert_to_hexbyte(0, 16)

        # Create data section
        msg = (o_export_name +
               o_msg_type +
               o_source_ip +
               o_destination_ip +
               o_source_port +
               o_destination_port +
               o_protocol +
               o_packet_count +
               o_kbyte_count +
               o_classname_len +
               o_classname +
               o_table_priority +
               o_timeout_type +
               o_timeout_value +
               o_action +
               o_action_flag +
               o_action_parameter)

        return msg

    def create_template(self, payload_len):
        """Creates the template

        Parameters
        ----------
        payload_len:
            The length of the payload message after template

        Returns
        -------
        temp:
            The template format
        """
        class TemplateClass:
            t_id = self.convert_to_hexbyte(256, 2)
            t_flag = self.convert_to_hexbyte(0, 2)
            NOP = self.convert_to_hexbyte(0, 2)                  # 0
            SRC_IPV4 = self.convert_to_hexbyte(1, 2)             # 1
            DST_IPV4 = self.convert_to_hexbyte(2, 2)             # 2
            SRC_PORT = self.convert_to_hexbyte(3, 2)             # 3
            DST_PORT = self.convert_to_hexbyte(4, 2)             # 4
            PROTO = self.convert_to_hexbyte(5, 2)                # 5
            # SRC_IPV6 = self.convert_to_hex(6, 2)                 # 6
            # DST_IPV6 = self.convert_to_hex(7, 2)                 # 7
            IPV4_TOS = self.convert_to_hexbyte(8, 2)             # 8
            IPV6_LABEL = self.convert_to_hexbyte(9, 2)           # 9
            CLASS_LABEL = self.convert_to_hexbyte(10, 2)         # A
            MATCH_DIR = self.convert_to_hexbyte(11, 2)           # B
            MSG_TYPE = self.convert_to_hexbyte(12, 2)            # C
            TIMEOUT_TYPE = self.convert_to_hexbyte(13, 2)        # D
            TIMEOUT = self.convert_to_hexbyte(14, 2)             # E
            ACTION_FLAGS = self.convert_to_hexbyte(15, 2)        # F
            PCKT_CNT = self.convert_to_hexbyte(16, 2)            # 10
            KBYTE_CNT = self.convert_to_hexbyte(17, 2)           # 11
            ACTION = self.convert_to_hexbyte(32768, 2)           # 8000
            ACTION_PARAMS = self.convert_to_hexbyte(32769, 2)    # 8001
            EXPORT_NAME = self.convert_to_hexbyte(32770, 2)      # 8002
            CLASSIFIER_NAME = self.convert_to_hexbyte(32771, 2)  # 8003
            CLASSES = self.convert_to_hexbyte(49152, 2)          # C000
            set_id = str(self.convert_to_hexbyte(256, 2))  # Set ID = 256 for msg
            set_len = self.convert_to_hexbyte(
                                (payload_len/2) + 4, 2)  # Set length of msg
        ts = TemplateClass

        # Optionals
        len_exp = self.convert_to_hexbyte(8, 2)  # Length of export name
        len_act = self.convert_to_hexbyte(8, 2)  # Length of action
        len_actp = self.convert_to_hexbyte(16, 2)  # Length of action parameter

        # Create template message
        temp = (ts.t_id +
                ts.t_flag +
                ts.EXPORT_NAME +
                len_exp +
                ts.MSG_TYPE +
                ts.SRC_IPV4 +
                ts.DST_IPV4 +
                ts.SRC_PORT +
                ts.DST_PORT +
                ts.PROTO +
                ts.PCKT_CNT +
                ts.KBYTE_CNT +
                ts.CLASSES +
                ts.TIMEOUT_TYPE +
                ts.TIMEOUT +
                ts.ACTION +
                len_act +
                ts.ACTION_FLAGS +
                ts.ACTION_PARAMS +
                len_actp +
                ts.set_id +
                ts.set_len)

        return temp

    def send_message(self, data, inputs):
        """Connects to a remote host using TCP or UDP and sends the RAP
        message

        Parameters
        ----------
        data:
            The serialised message to be sent
        inputs:
            The Host IP, Port Number, Protocol name

        """
        # Host socket assign
        port = self.port_check(inputs.PORT)
        proto = self.protocol_check(inputs.PROTO)  # Proto check

        try:
            # Open UDP Socket if UDP
            if proto.lower() in ["udp"]:
                print(
                    "Opening UDP socket on port", port)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

                # Send UDP Message
                sock.sendto(data, (inputs.HOST, port))

            # Open TCP Socket if TCP
            else:
                print(
                    "Opening TCP socket on port", port)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Send TCP Message
                sock.settimeout(10)
                sock.connect((inputs.HOST, port))
                sock.send(data)
                sock.close()

        except socket.timeout:
            sys.exit('Error: Couldn\'t connect to socket')

    def create_header(self, cli_inputs, payload_len, template_len):
        """Creates the packet header

        Parameters
        ----------
        cli_inputs:
            The imported command line interface inputs
        payload_len:
            The length of the payload packet
        template_len:
            The length of the template

        Returns
        -------
        header: Tuple
            The header information

        """
        # Get current time
        current_time = int(time.time())

        # Create initial header variables
        ver = self.convert_to_hexbyte(_input=1, _len=2)
        seq_no = cli_inputs.seq_no
        time_hexed = self.convert_to_hexbyte(_input=current_time, _len=4)
        set_id = self.convert_to_hexbyte(1, 2)  # Set ID = 1 for template
        set_len = self.convert_to_hexbyte(
            template_len / 2, 2)  # Set length of template
        m_len = self.convert_to_hexbyte((payload_len + template_len) / 2 + 16,
                                        2)  # Size of payload
        # Create header
        header = (str(ver) +
                  str(seq_no) +
                  str(time_hexed) +
                  str(set_id) +
                  str(set_len) +
                  str(m_len))

        return header

    @staticmethod
    def parser():
        """Command Line Interface for the FCN

        Returns
        -------
        args:
            The command line interface inputs

        """
        parser = argparse.ArgumentParser(
            description='CLI Scanning Utility\n',
            formatter_class=argparse.RawTextHelpFormatter)

        parser.add_argument('-i', '--srcip',
                            action="store",
                            dest="srcip",
                            default='0.0.0.0',
                            metavar='Source IP',
                            help="\t\t\t"
                                 "Source IP address in x.x.x.x format")
        parser.add_argument("-j", "--destip",
                            action="store",
                            dest="destip",
                            default='0.0.0.0',
                            # required = True,
                            metavar='Destination IP',
                            help='\t\t\t'
                                 'Destination IP address in x.x.x.x format')
        parser.add_argument("-s", "--seqno",
                            action="store",
                            dest="seq_no",
                            type=int,
                            # required = True,
                            default=20,
                            metavar='Sequence Number',
                            help='\t\t\tSequence Number')
        parser.add_argument("-k", "--srcport",
                            action="store",
                            dest="srcport",
                            type=int,
                            default=0,
                            metavar='Source port',
                            help='\t\t\tSource port 1-65535')
        parser.add_argument("-l", "--destport",
                            action="store",
                            dest="destport",
                            type=int,
                            default=0,
                            metavar='Destination port',
                            help='\t\t\tDestination port 1-65535')
        parser.add_argument("-u", "--prototype",
                            action="store",
                            dest="prototype",
                            type=int,
                            default=0,  # nothin
                            metavar='Protocol Type',
                            help='\t\t\t'
                                 'Protocol Type (Default: TCP)\n\t\t\t'
                                 '1: ICMP\n\t\t\t'
                                 '2: IGMP\n\t\t\t'
                                 '3: GGP\n\t\t\t'
                                 '4: IPENCAP\n\t\t\t'
                                 '5: ST2\n\t\t\t'
                                 '6: TCP\n\t\t\t'
                                 '17: UDP\n')
        # 7cbt#8egp#9ip
        parser.add_argument("-a", '--mtype',
                            action="store",
                            dest="msgtype",
                            type=int,
                            default=0,
                            metavar='Msg Type',
                            help='\t\t\t'
                                 '0: Add (Default)\n\t\t\t'
                                 '1: Remove\n\t\t\t'
                                 '2: Remove All\n')
        parser.add_argument(
            "-t",
            "--timeoutval",
            action="store",
            dest="timeoutval",
            type=int,
            default=60,
            metavar='Timeout Value',
            help='\t\t\tTimeout value in seconds (Default: 60)')
        parser.add_argument("-e", "--export",
                            action="store",
                            dest="export",
                            default='myexp',
                            metavar='Export',
                            help='\t\t\tName of export (Default: myexp)')
        parser.add_argument("-c", "--class",
                            action="store",
                            dest="mclass",
                            default='myclass',
                            metavar='Class',
                            help='\t\t\t'
                                 'Name of class (Default: myclass)')
        parser.add_argument("-n", "--prio",
                            action="store",
                            dest="prio",
                            type=int,
                            default=1,
                            metavar='Priority',
                            help='\t\t\t'
                                 'Class Priority (Default: 1)')
        # Global
        parser.add_argument("-x", "--host",
                            action="store",
                            dest="HOST",
                            default='127.0.0.1',
                            metavar='Host',
                            help='\n\t\t\t'
                                 'Action Node IP (Default: 127.0.0.1)')
        parser.add_argument("-y", "--port",
                            action="store",
                            dest="PORT",
                            type=int,
                            default=5000,
                            metavar='Port',
                            help='\n\t\t\t'
                                 'Output Port to Action Node (Default: 5000)')
        parser.add_argument("-z", "--proto",
                            action="store",
                            dest="PROTO",
                            default='UDP',
                            metavar='Proto',
                            help='\t\t\t'
                                 'Protocol to Action Node (Default: UDP)')
        parser.add_argument("-o",  # uni/bidirectional to be added
                            action="store",
                            dest="a_flg",
                            type=int,
                            default=1,
                            metavar='Action Flag',
                            help='(Experimental)\n\t\t\t'
                                 '0: Unidirectional\n\t\t\t'
                                 '1: Bidirectional\n')
        cli_inputs = parser.parse_args()

        return cli_inputs

    @staticmethod
    def port_check(port):
        """Checks if if the port number is valid

        Parameters
        ----------
        port:
            The port number

        Returns
        -------
            The port number for valid numbers

        """
        try:
            if 0 <= port <= 65535:
                return port
            else:
                raise NameError(
                    'Flow Source/Destination port must be between 0 and 65535')
        except Exception:
            raise NameError(
                'Flow Source/Destination port must be between 0 and 65535')


    @staticmethod
    def priority_check(priority):
        """Checks if if the priority number is a valid number

        Parameters
        ----------
        priority:
            The priority number

        Returns
        -------
            The priority for valid numbers

        """
        try:
            if 0 <= priority < 256:
                return priority
            else:
                raise NameError('Error: Priority must be between 0 and 255')
        except Exception:
            raise NameError('Error: Priority must be between 0 and 255')

    @staticmethod
    def prototype_check(protocol_type):
        """Checks if if the protocol type is a valid number

        Parameters
        ----------
        protocol_type:
            The protocol type number

        Returns
        -------
            The protocol type if valid

        """
        try:
            if 0 <= protocol_type < 256:
                return protocol_type
            else:
                raise NameError('Error: Invalid protocol type')
        except Exception:
            raise NameError('Error: Invalid protocol type')

    @staticmethod
    def msg_type_check(msg_type):
        """Checks if msg type if valid between 0 and 2

        Parameters
        ----------
        msg_type:
            The msg type number

        Returns
        -------
            The msg_type if valid

        """
        try:
            if 0 <= msg_type < 3:
                return msg_type
            else:
                raise NameError('Invalid Msg Type')
        except Exception:
            raise NameError('Invalid Msg Type')

    @staticmethod
    def export_name_check(export_name):
        """Checks if the name of the exporter is 8 chars or less

        Parameters
        ----------
        export_name:
            The name of an exporter

        Returns
        -------
            The export name if it is valid
        """
        try:
            if len(export_name) <= 8:
                return export_name
            else:
                raise NameError('Invalid Export Name')
        except Exception:
                raise NameError('Invalid Export Name')

    @staticmethod
    def protocol_check(protocol):
        """Checks if the protocol in either TCP or UDP

        Parameters
        ----------
        protocol:
            The input protocol

        Returns
        -------
            The protocol if it is valid
        """
        try:
            if protocol.lower() in ["tcp", "udp"]:
                return protocol
            else:
                raise NameError("Invalid Protocol")
        except Exception:
            raise NameError("Invalid Protocol")

    @staticmethod
    def ip_check(address):
        """Checks if IP address is a valid IPv4 address

        Parameters
        ----------
        address:
            The input IP address

        Returns
        -------
            The IP address if it is valid

        """
        try:
            socket.inet_pton(socket.AF_INET, address)
        except Exception:
            raise NameError('Invalid IP')
        else:
            return address

    @staticmethod
    def convert_to_hexbyte(_input, _len):
        """Converts to hexbyte format
        00 -> 0x00
        15 -> 0x0F
        
        Parameters
        ----------
        _input:
            The input integer to be converted
        _len:
            The length required for output format
        Returns
        -------
            The hexbyte format
            
        """
        if _len == 1:
            _input = '{:0>2x}'.format(_input)
            _input = '{:.2}'.format(_input)
        elif _len == 2:
            _input = '{:0>4x}'.format(_input)
            _input = '{:.4}'.format(_input)
        elif _len == 4:
            _input = '{:0>8x}'.format(_input)
            _input = '{:.8}'.format(_input)
        elif _len == 8:
            _input = '{:0>16x}'.format(_input)
            _input = '{:.16}'.format(_input)
        elif _len == 16:
            _input = '{:0>32x}'.format(_input)
            _input = '{:.32}'.format(_input)
        else:
            print('Error: Variable couldn\'t be converted')
        return _input

if __name__ == '__main__':
    FCN()
