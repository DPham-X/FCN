Fake Classifier Node (FCN)
==========================
The FCN is able to create RAP packets to classify flows based on command line parameters.

INTRODUCTION
------------
This is the README for the FCN

This README gives a brief overview on how to install and use the FCN.
Example configurations are provided

For more information regarding the FCN refer to the technical report

    http://caia.swin.edu.au/reports/160422A/CAIA-TR-160422A.pdf
    
For an updated FCN check:

    https://github.com/XykotiC/FCN/

REQUIREMENTS
------------
`python 2.7`

PARAMETERS
----------
    -h, --help                                  show this help message and exit
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
                        
INSTALLATION
------------

`$ cd FCN`

`$ git clone https://github.com/XykotiC/FCN.git`

GETTING STARTED
---------------
1. Install the Fake Classifier Node
2. Run the Ryu Action Node or DIFFUSE Action node
3. Send FCN Commands to the Action Node to create flow rules
    
    Example:
    
    `python fcn -i 10.0.0.1 -j 10.0.0.2 -k 80 -l 5000 -s 10 -u 6 -a 0 -t 60 -c myclass -n 20 -x 192.168.1.2 -y 5000 -z UDP`
    

LICENSE
-------

    # Copyright (c) 2016, Centre for Advanced Internet Architectures,
    # Swinburne University of Technology. All rights reserved.
    #
    # Author: Dzuy Pham (dhpham@swin.edu.au)
    #
    # Redistribution and use in source and binary forms, with or without
    # modification, are permitted provided that the following conditions
    # are met:
    #
    # 1. Redistributions of source code must retain the above copyright
    #    notice, this list of conditions and the following disclaimer.
    # 2. Redistributions in binary form must reproduce the above copyright
    #    notice, this list of conditions and the following disclaimer in the
    #    documentation and/or other materials provided with the distribution.
    #
    # THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
    # ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    # IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    # ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
    # FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    # DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
    # OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
    # HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
    # LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
    # OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
    # SUCH DAMAGE.
    #
    # The views and conclusions contained in the software and documentation are
    # those of the authors and should not be interpreted as representing official
    # policies, either expressed or implied, of the FreeBSD Project.

