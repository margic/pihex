from client.stompclient import StompClient

__author__ = 'paul'


def main():
    stomp = StompClient('192.168.0.67', 61613, 'admin', 'admin')
    test_sequence = open('pitest/testsequence.json').read()
    stomp.send_message('hexOut', 'application/json', test_sequence)

if __name__ == "__main__":
    main()