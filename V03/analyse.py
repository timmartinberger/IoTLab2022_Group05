import pandas as pd
import datetime
import argparse
import matplotlib.pyplot as plt


def load_df(filename):
    df = pd.read_csv(filename, names=["timestamp", "packet_number", "sequence_number", "tcp_len"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s", origin="unix")
    return df


def load_df_udp(filename):
    df = pd.read_csv(filename, names=["timestamp", "packet_number", "data_len"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s", origin="unix")
    return df


def main(csv1, csv2):
    df_tcp_server = load_df(csv1)
    df_tcp_client = load_df(csv2)

    grouped = df_tcp_server.groupby(pd.Grouper(key="timestamp", freq="S"))["sequence_number"].count()
    grouped.plot(x='timestamp', y='count', kind='line')

    grouped_client = df_tcp_client.groupby(pd.Grouper(key="timestamp", freq="S"))["sequence_number"].count()
    grouped_client.plot(x='timestamp', y='count', kind='line')

    joined_df = df_tcp_client.join(df_tcp_server.set_index("sequence_number"), on="sequence_number", lsuffix="_client",
                                   rsuffix="_server")
    joined_df["owd"] = (joined_df['timestamp_server'] - joined_df['timestamp_client']).astype('timedelta64[ms]')

    print(f"Mean owd: {joined_df.head(4000)['owd'].mean()}")
    print(f"Std owd: {joined_df.head(4000)['owd'].std()}")
    total_seconds = (df_tcp_server['timestamp'].max() - df_tcp_server['timestamp'].min()).total_seconds()
    df_tcp_server['data_bits'] = (df_tcp_server['tcp_len'] - 40) * 8
    print(f"Bitrate recieved: {df_tcp_server['data_bits'].sum() / total_seconds}")
    plt.legend(["Empfänger", "Sender"])
    plt.show()


def main_udp(csv1, csv2):
    df_tcp_server = load_df_udp(csv1)
    df_tcp_client = load_df_udp(csv2)

    grouped = df_tcp_server.groupby(pd.Grouper(key="timestamp", freq="S"))["packet_number"].count()
    grouped.plot(x='timestamp', y='count', kind='line')

    grouped_client = df_tcp_client.groupby(pd.Grouper(key="timestamp", freq="S"))["packet_number"].count()
    grouped_client.plot(x='timestamp', y='count', kind='line')

    joined_df = df_tcp_client.join(df_tcp_server.set_index("packet_number"), on="packet_number", lsuffix="_client",
                                   rsuffix="_server")

    joined_df["owd"] = (joined_df['timestamp_server'] - joined_df['timestamp_client']).astype('timedelta64[ms]')

    print(f"Mean owd: {joined_df.head(4000)['owd'].mean()}")
    print(f"Std owd: {joined_df.head(4000)['owd'].std()}")

    plt.legend(["Empfänger", "Sender"])
    plt.show()


if __name__ == "__main__":
    csv_sender = None
    csv_receiver = None
    parser = argparse.ArgumentParser('Plot statistics about udp/tcp connections.')
    parser.add_argument('-s', '--sender', required=True)
    parser.add_argument('-r', '--receiver', required=True)
    parser.add_argument('-u', '--udp', required=False)
    args = vars(parser.parse_args())
    if args['sender'] is not None:
        csv_sender = args['sender']
    if args['receiver'] is not None:
        csv_receiver = args['receiver']

    udp = False
    if args['udp'] is not None:
        udp = True
    if not udp:
        main(csv_receiver, csv_sender)
    else:
        main_udp(csv_receiver, csv_sender)