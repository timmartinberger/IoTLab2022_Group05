FILTER_STRING='tcp.dstport == 8000 and frame.len >= 500'

tshark -r report_tcp_server_wifi.pcap -Y "tcp.flags == 0x010 && ip.addr == 172.23.90.118" -T fields -E separator=/s -e ip.dst -e tcp.seq > sequence_numbers_tcp_server_wifi.log
tshark -r report_tcp_server_wifi.pcap -Y "${FILTER_STRING}" -qz io,stat,1,"COUNT(frame) frame" > packet_counts_tcp_server_wifi.log
tshark -r report_tcp_server_wifi.pcap -Y "${FILTER_STRING}" -T fields -E separator=, -e frame.time_epoch -e frame.number -e tcp.seq -e tcp.len > timestamps_tcp_server_wifi.csv
