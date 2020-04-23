import argparse
import time
import threading

from sip2.wrapper import Sip2Wrapper

sip2Params = {
    'hostName': '127.0.0.1',
    'hostPort': 3004,
    'tlsEnable': False,
    'tlsAcceptSelfsigned': True,
    'hostEncoding': 'utf-8',
    'language': '000',
    'institutionId': 'institution_id',
    'scLocation': 'selfcheck_location',
}


def selfcheck_client(user, password):
    cur_thread = threading.current_thread()

    while True:
        try:
            time.sleep(5)
            print('[{thread}] : try to connect to server...'.format(
                thread=cur_thread.name
            ))
            # Create instance and automatically connect
            wrapper = Sip2Wrapper(sip2Params, True)

            print('[{thread}] : login to server...'.format(
                thread=cur_thread.name
            ))
            wrapper.login_device(user, password, True)

            print('[{thread}] : status...'.format(
                thread=cur_thread.name
            ))
            wrapper.sip_sc_status()

            print('[{thread}] : disconnect from server...'.format(
                 thread=cur_thread.name
            ))
            wrapper.disconnect()

        except Exception as err:
            print(err)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SIP2 Client")
    parser.add_argument('-c', '--concurrency', type=int, default=1)
    parser.add_argument('-u', '--user')
    parser.add_argument('-p', '--password')
    args = parser.parse_args()

    # check user and password (must be recognize by automated circulation system)
    if args.user and args.password:
        for t in range(args.concurrency) :
            client = threading.Thread(target=selfcheck_client,
                                      args=(args.user, args.password))
            client.start()
            time.sleep(1)

    else:
        raise Exception('missing user or password argument')



