from argparse import ArgumentParser
from client.stompclient import StompClient

__author__ = 'paul'


def main():
    queue_config = dict()
    queue_config['remote_queue_host'] = '192.168.0.67'
    queue_config['remote_queue_port'] = 61613
    queue_config['remote_queue_username'] = 'admin'
    queue_config['remote_queue_password'] = 'admin'

    parser = ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    stomp = StompClient(queue_config)
    test_sequence = open('pitest/' + args.filename).read()
    stomp.send_message('hexOut', 'application/json', test_sequence)

if __name__ == "__main__":
    main()