FILTER_STRING='udp.dstport == 8000 and frame.len >= 500'
tshark -r report_udp_server.pcap -Y "${FILTER_STRING}" -T fields -E separator=, -e frame.time_epoch -e frame.number -e data.len > timestamps_udp_server.csv
