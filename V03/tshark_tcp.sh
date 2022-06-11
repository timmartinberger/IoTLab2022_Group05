FILTER_STRING='tcp.port == 8000 && tcp contains Hello'

tshark -r report_tcp.pcap -Y "tcp.flags == 0x010 && ip.addr == 192.168.0.11" -T fields -E separator=/s -e ip.dst -e tcp.seq > sequence_numbers_tcp.log
tshark -r report_tcp.pcap -Y "${FILTER_STRING}" -qz io,stat,1,"COUNT(frame) frame" > packet_counts_tcp.log
tshark -r report_tcp.pcap -Y "${FILTER_STRING}" -T fields -E separator=/s -e frame.time_epoch -e frame.number -e tcp.seq > timestamps_tcp.log

# average one way delay for first 4000 pkgs (muss anders gemacht werden mit messungen bei host und sender)
tshark -r report_tcp.pcap -c 4000 -Y "${FILTER_STRING}" -qz io,stat,0,"AVG(frame.time_delta) frame.time_delta" > frame_delay_tcp.log