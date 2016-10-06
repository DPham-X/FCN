Fake Classifier Node 1.0 (FCN)
==========================
The FCN is able to create RAP packets to classify flows based on command line parameters.

INTRODUCTION
------------
This is the README for the FCN

This README gives a brief overview on how to install and use the FCN.
Example configurations are provided

For more information regarding the FCN refer to the technical report

[Developing a Fake Classifier Node for DIFFUSE](http://caia.swin.edu.au/reports/160422A/CAIA-TR-160422A.pdf)
    
The FCN application can be found at:

<http://caia.swin.edu.au/urp/diffuse/downloads/fcn-1.0.tar.gz>

REQUIREMENTS
------------
`python 2.7`
`pyQt4`

Get Python2.7 here https://www.python.org/download/releases/2.7/

If using the FCN GUI install PyQt4 from https://www.riverbankcomputing.com/software/pyqt/download

PARAMETERS
----------
    -h, --help                      Help
    -i, --srcip                     The Source IP address in x.x.x.x format
    -j, --destip                    Destination IP address in x.x.x.x format
    -s, --seqno                     Sequence Number
    -k, --srcport                   Source port 1-65535
    -l, --destport                  Destination port 1-65535
    -u, --prototype                 Protocol Type (Default: TCP)
                                        1: ICMP
                                        2: IGMP
                                        3: GGP
                                        4: IPENCAP
                                        5: ST2
                                        6: TCP
                                        17: UDP
    -a,  --mtype                    Message Type
                                    0: Add (Default)
                                    1: Remove
                                    2: Remove All                                
    -t,  --timeoutval               Timeout value in seconds (Default: 60)
    -e,  --export                   Name of export (Default: myexp)
    -c,  --class                    Name of class (Default: myclass)
    -n,  --prio                     Table Priority (Default: 1)
    -x, --host                      Action Node IP (Default: 127.0.0.1)
    -y, --port                      Output Port to Action Node (Default: 5000)
    -z, --proto                     Protocol to Action Node (Default: UDP)
    
GETTING STARTED
---------------
1. Install prequisites - python2.7 and PyQt4 if using the GUI.

2. Unzip the Fake Classifier Node

    ```sh
    $ tar -zxvf fcn-1.0.tar.gz
    $ cd fcn-1.0
    ```

3. Run the Ryu Action Node or DIFFUSE Action node implementation

    See [Ryu Action Node v1.01](http://caia.swin.edu.au/urp/diffuse/sdn)

4. Send FCN Commands to the Action Node to create flow rules
    
### Using the Command Line Interface
    
Example:
    
```sh
python ./fcn.py -i 10.0.0.1 -j 10.0.0.2 -k 80 -l 5000 -s 10 -u 6 -a 0 -t 60 -c myclass -n 20 -x 192.168.1.2 -y 5000 -z TCP
```
    
### Using the Graphical User Interface
   
Input parameters and press send

Example:

| 5-tuple 	   | 	      |	Settings        |	  | Host Settings |	        |
| ---------------- | -------- | --------------- | ------- | ------------- | ----------- |
| Source IP 	   | 10.0.0.1 | Sequence Number | 10	  | Host IP	  | 192.168.1.2 |
| Destination IP   | 10.0.0.2 | Message Type    | Add	  | Host Port	  | 5000	|
| Source Port 	   | 80	      | Timeout Val     | 60	  | Host Protocol | TCP	        |
| Destination Port | 5000     | Export Name     | myexp	  |		  |	        |
| Protocol 	   | 6 	      | Class Name      | myclass |		  |	        |
|		   |	      | Priority        | 20	  |		  |	        |
    

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

