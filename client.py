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
    'language': '002',
    'institutionId': 'UCLouvain',
    'scLocation': 'selfcheck_location',
}


def selfcheck_client(user, password):
    cur_thread = threading.current_thread()
    while True:
        try:
            print('[{thread}] : try to connect to server...'.format(
                thread=cur_thread.name
            ))
            # Create instance and automatically connect
            wrapper = Sip2Wrapper(sip2Params, True)

            while True:
                try:

                    time.sleep(5)

                    # 1. login device (93)
                    print('[{thread}] : login to server...'.format(
                        thread=cur_thread.name
                    ))
                    wrapper.login_device(user, password, True)

                    # 2. get ACS status (98)
                    print('[{thread}] : status...'.format(
                        thread=cur_thread.name
                    ))
                    wrapper.sip_sc_status()

                    # 3. patron login (23)
                    print('[{thread}] : login patron...'.format(
                        thread=cur_thread.name
                    ))

                    # test wiht Simonetta
                    #wrapper.login_patron('2233230', '123456')
                    # test wiht Simonetta
                    wrapper.login_patron('2050124311', '123456')
                    # test with Giulia
                    #wrapper.login_patron('2050124312', '123456')

                    # 4. enable patron (25)
                    print('[{thread}] : enable patron...'.format(
                         thread=cur_thread.name
                    ))
                    wrapper.sip_patron_enable()

                    # 5. patron information (63)
                    print('[{thread}] : patron information...'.format(
                        thread=cur_thread.name
                    ))
                    patron_info = wrapper.sip_patron_information()

                    # 6. item information (17)
                    print('[{thread}] : item information...'.format(
                        thread=cur_thread.name
                    ))
                    print('patron_info:', patron_info)
                    items = patron_info.get('variable').get('AS', [])
                    print('items:', items)
                    for item_id in items:
                        item = wrapper.sip_item_information(item_id)
                        print('[{thread}] : hold item information...'.format(
                            thread=cur_thread.name
                        ))
                    items = patron_info.get('variable').get('AT', [])
                    for item_id in items:
                        item = wrapper.sip_item_information(item_id)
                        print('[{thread}] : overdue item information...'.format(
                            thread=cur_thread.name
                        ))
                    items = patron_info.get('variable').get('AU', [])
                    for item_id in items:
                        item = wrapper.sip_item_information(item_id)
                        print('[{thread}] : charged item information...'.format(
                            thread=cur_thread.name
                        ))
                    # 7. end patron session (35)
                    print('[{thread}] : patron session end...'.format(
                        thread=cur_thread.name
                    ))

                    wrapper.sip_patron_session_end()

                    time.sleep(5)

                    # print('[{thread}] : disconnect from server...'.format(
                    #      thread=cur_thread.name
                    # ))
                    # wrapper.disconnect()

                except (ConnectionError, ConnectionRefusedError) as e:
                    print('[{thread}] : Connection lose! Try to reconnect to server'.format(
                            thread=cur_thread.name
                    ))
                    wrapper = Sip2Wrapper(sip2Params, True)
                    pass

                except Exception as err:
                    print(err)
                    print(
                        '[{thread}] : Connection lose! Try to reconnect to server'.format(
                            thread=cur_thread.name
                        ))
                    wrapper = Sip2Wrapper(sip2Params, True)
                    pass
        except Exception as e:
            print(e)
            print(
                '[{thread}] : Connection lose! Try to reconnect to server'.format(
                    thread=cur_thread.name
                ))
            time.sleep(5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SIP2 Client")
    parser.add_argument('-c', '--concurrency', type=int, default=1)
    parser.add_argument('-u', '--user')
    parser.add_argument('-p', '--password')
    args = parser.parse_args()

    # check user and password (must be recognize by automated circulation system)
    if args.user and args.password:
            try:
                for t in range(args.concurrency) :
                    client = threading.Thread(target=selfcheck_client,
                                              args=(args.user, args.password))
                    client.start()
                    time.sleep(1)
            except Exception as e:
                print(e)
                time.sleep(5)

    else:
        raise Exception('missing user or password argument')


