# import pandas as pd
# import numpy as np
import os
import re
import glob

"""
    Events:
    + : packet enque event
    -  : packet deque event
    r  : packet reception event
    d : packet drop (e.g., sent to dropHead_) event
    c : packet collision at the MAC level

    Times: Time at which the packet tracing string is created.

    (Source|Destination) Node: Source and destination ID's of tracing objects.

    Packet Type: Name of packet type

    Packet Size: Size of packet in bytes

    Flags:
    “-”: disable
    1st = “E”: ECN (Explicit Congestion Notification) echo is enabled.
    2nd = “P”: the priority in the IP header is enabled.
    3rd : Not in use
    4th = “A”: Congestion action
    5th = “E”: Congestion has occurred.
    6th = “F”: The TCP fast start is used.
    7th = “N”: Explicit Congestion Notification (ECN) is on.

    Flow ID

    (Source|Destination) Address : The format of these two fields
    is “a.b”, where “a" is the address and "b" is the port

    Sequence Number

    Packet Unique ID
    
"""


class TraceFileReader:

    def __regex(self):
        regex = r"^(( )*([+]|[-]|[r]|[d]|[c])( )+(\d+\.\d+)( )+(\d+)( )+(\d+)( )+(\w+)( )+(\d+)( )+(([E]|[-])([P]|[-])([-])([A]|[-])([E]|[-])([F]|[-])([N]|[-]))( )+(\d+)( )+(\d+\.\d+)( )+(\d+\.\d+)( )+(\d+)( )+(\d+)( )*)$"
        regex = re.compile(regex)
        return regex


    def __find_trace_files(self):
        trace_files = glob.glob("lib/*.tr")
        f = 'Find trace files: '
        for i in trace_files:
            f = f + "\"" + i +"\""
        print(f)
        if len(trace_files) == 1:
            print("Trace file found. Using \""+ trace_files[0] + "\".")
            return trace_files[0]
        elif len(trace_files) > 1:
            print("Too many trace files found. Using \""+ trace_files[0] + "\".")
            return trace_files[0]
        elif len(trace_files) < 1:
            print("No trace files found. Please add a trace file to \"lib\" folder.")
            exit()


    def __read_file(self):
        lines = []
        regex = self.__regex()
        trace_file = open(os.getcwd()+"/"+self.__find_trace_files(), 'r')
        while True:
            line = trace_file.readline().strip()
            if regex.fullmatch(line):
                lines.append(line)
            if not line:
                break
        return lines

    def __init__(self):
        self.__lines = self.__read_file()

    def set_columns(self):
        self.__events = []
        self.__times = []
        self.__fromnode = []
        self.__tonode = []
        self.__pkttype = []
        self.__pktsize = []
        self.__flags = []
        self.__fid = []
        self.__srcaddr = []
        self.__dstaddr = []
        self.__seqnum = []
        self.__pktid = []

        for line in self.__lines:
            line = line.split()
            self.__events.append(line[0])
            self.__times.append(float(line[1]))
            self.__fromnode.append(int(line[2]))
            self.__tonode.append(int(line[3]))
            self.__pkttype.append(line[4])
            self.__pktsize.append(int(line[5]))
            self.__flags.append(line[6])
            self.__fid.append(int(line[7]))
            self.__srcaddr.append(float(line[8]))
            self.__dstaddr.append(float(line[9]))
            self.__seqnum.append(int(line[10]))
            self.__pktid.append(int(line[11]))

    def lines(self):
        return self.__lines

    def length(self):
        return len(self.__lines)

    # Return columns

    def col_event(self):
        return tuple(self.__events)

    def col_time(self):
        return tuple(self.__times)

    def col_source_node(self):
        return tuple(self.__fromnode)

    def col_destination_node(self):
        return tuple(self.__tonode)

    def col_packet_type(self):
        return tuple(self.__pkttype)

    def col_packet_size(self):
        return tuple(self.__pktsize)

    def col_flags(self):
        return tuple(self.__flags)

    def col_frame_id(self):
        return tuple(self.__fid)

    def col_source_address(self):
        return tuple(self.__srcaddr)

    def col_destination_address(self):
        return tuple(self.__dstaddr)

    def col_sequence_number(self):
        return tuple(self.__seqnum)

    def col_packet_id(self):
        return tuple(self.__pktid)

    # return field by index

    def get_event(self, index):
        return self.__events[index]

    def get_time(self, index):
        return self.__times[index]

    def get_source_node(self, index):
        return self.__fromnode[index]

    def get_destination_node(self, index):
        return self.__tonode[index]

    def get_packet_type(self, index):
        return self.__pkttype[index]

    def get_packet_size(self, index):
        return self.__pktsize[index]

    def get_flags(self, index):
        return self.__flags[index]

    def get_frame_id(self, index):
        return self.__fid[index]

    def get_source_address(self, index):
        return self.__srcaddr[index]

    def get_destination_address(self, index):
        return self.__dstaddr[index]

    def get_sequence_number(self, index):
        return self.__seqnum[index]

    def get_packet_id(self, index):
        return self.__pktid[index]
