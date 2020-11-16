from .TraceFileReader import TraceFileReader


class PerformanceMeasures:

    def __init__(self):
        self.__tf = TraceFileReader()


    def congestion(self):
        lines = self.__tf.lines()
        graph_params = []
        s_congestion = 0
        r_congestion = 0
        time_index = 0.0
        time_index_increment = 0.5
        initialize_time_index = True
        for line_ in lines:
            line = line_.split()
            time = float(line[1])
            flags = line[6]
            if initialize_time_index == True:
                while time > time_index:
                    graph_params.append((time_index, 0, 0))
                    time_index += time_index_increment
                initialize_time_index = False


            if flags[3] == 'A' and line[0] == '+':
                s_congestion += 1
            elif flags[3] == 'A' and line[0] == 'r':
                r_congestion += 1


            if time >= time_index and time < time_index + time_index_increment:
                graph_params.append((time_index, s_congestion, r_congestion))
                time_index += time_index_increment
            elif time >= time_index + time_index_increment:
                while time > time_index:
                    graph_params.append(
                        (time_index, s_congestion, r_congestion))
                    time_index += time_index_increment

        # finally
        graph_params.append((time, s_congestion, r_congestion))
        return graph_params


    def packet_drop(self):
        lines = self.__tf.lines()
        graph_params = []
        total_packet_drop = 0
        time = 0.0
        time_index = 0.0
        time_index_increment = 0.5
        initialize_time_index = True
        for line in lines:
            line = line.split()
            time = float(line[1])
            event = line[0]
            packet_type = line[4]


            if event == 'd' and packet_type == 'tcp':
                if initialize_time_index == True:
                    while time > time_index:
                        graph_params.append((time_index, 0))
                        time_index += time_index_increment
                    initialize_time_index = False
                total_packet_drop += 1


            if time >= time_index and time < time_index + time_index_increment:
                graph_params.append((time_index, total_packet_drop))
                time_index += time_index_increment
            elif time >= time_index + time_index_increment:
                while time > time_index:
                    graph_params.append((time_index, total_packet_drop))
                    time_index += time_index_increment
        return graph_params


    def throughtput(self):
        lines = self.__tf.lines()
        graph_params = []
        avrg_throughtput = []
        total_time = 0.0
        time_index = 0.0
        time_index_increment = 0.5
        initialize_time_index = True
        total_size = 0
        packets_sent = []
        send_time = 0.0
        for line in lines:
            line = line.split()
            packet_type = line[4]
            packet_size = int(line[5])
            time = float(line[1])
            event = line[0]
            packet_id = int(line[11])
            if initialize_time_index == True:
                while time > time_index:
                    graph_params.append((time_index, 0))
                    time_index += time_index_increment
                initialize_time_index = False


            if packet_size >= 512 and packet_type == 'tcp':
                if event == '+' or event == 's':
                    packets_sent.append([packet_id, time])
                elif event == 'r':
                    for sublist in packets_sent[::-1]:
                        if sublist[0] == packet_id:
                            send_time = sublist[1]
                            del sublist
                            break
                    total_time += time - send_time
                    packet_size -= packet_size % 512
                    total_size += packet_size


                if time >= time_index and time < time_index + time_index_increment and total_time != 0.0:
                    throughtput = (
                        float(total_size) / total_time)*(8.0/1000)
                    avrg_throughtput = [time_index, throughtput]
                    graph_params.append(tuple(avrg_throughtput))
                    time_index += time_index_increment
                    packets_sent.clear()
                    total_size = 0
                    total_time = 0.0
                elif time >= time_index + time_index_increment:
                    graph_params.append((time_index, 0))
                    time_index += time_index_increment
        # do it last time
        if total_time != 0:
            throughtput = (float(total_size) / total_time)*(8.0/1000)
            avrg_throughtput = [time, time_index]
            graph_params.append(tuple(avrg_throughtput))


        return graph_params


    def packet_delivery_ratio(self):
        lines = self.__tf.lines()
        graph_params = []
        delivery_count = 0
        drop_count = 0
        time_index = 0.0
        time_index_increment = 0.5
        initialize_time_index = True
        for line in lines:
            line = line.split()
            event = line[0]
            time = float(line[1])
            packet_type = line[4]
            if initialize_time_index == True:
                while time > time_index:
                    time_index += time_index_increment
                initialize_time_index = False


            if event == 'r' and packet_type == 'tcp':
                delivery_count += 1
            elif event == 'd' and packet_type == 'tcp':
                drop_count += 1


            if time >= time_index and time < time_index + time_index_increment and (event == 'd' or event == 'r'):
                time_index += time_index_increment
                packet_delivery_ratio = float(float(delivery_count/(delivery_count + drop_count))*100)
                graph_params.append((time_index, packet_delivery_ratio))
            elif time >= time_index + time_index_increment and (event == 'd' or event == 'r'):
                while time > time_index:
                    time_index += time_index_increment
                packet_delivery_ratio = float(float(delivery_count/(delivery_count + drop_count))*100)
                graph_params.append((time_index, packet_delivery_ratio))


        return graph_params


    def end_to_end_delay(self):
        lines = self.__tf.lines()
        graph_params = []
        total_delay = 0.0
        time_index = 0.0
        time_index_increment = 0.5
        recv_count = 0
        initialize_time_index = True
        packets_sent = []
        for line in lines:
            line = line.split()
            packet_type = line[4]
            time = float(line[1])
            packet_id = int(line[11])
            event = line[0]
            if initialize_time_index == True:
                while time > time_index:
                    graph_params.append((time_index, 0))
                    time_index += time_index_increment
                initialize_time_index = False

            if (event == '+' or event == 's') and packet_type == 'tcp':
                packets_sent.append([packet_id, time])
            elif event == 'r' and packet_type == 'tcp':
                for sublist in packets_sent[::-1]:
                    if sublist[0] == packet_id:
                        send_time = sublist[1]
                        del sublist
                        break
                recv_count += 1
                total_delay += time - send_time

            if time >= time_index and time < time_index + time_index_increment and recv_count > 0:
                delay = int(total_delay*1000/recv_count)
                graph_params.append((time_index, delay))
                time_index += time_index_increment
                recv_count = 0
                total_delay = 0.0
            elif time >= time_index + time_index_increment:
                delay = int(time_index_increment*1000)
                while time > time_index:
                    graph_params.append((time_index, delay))
                    time_index += time_index_increment
                recv_count = 0
                total_delay = 0.0


        return graph_params
