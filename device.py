from cortex2.emotiv_cortex2_client import EmotivCortex2Client
import time
client=None

def deive_connect():
    global client
    url = "wss://localhost:6868"
    client = EmotivCortex2Client(url,
                                 client_id='qWPGYgzUyamd0NWBg3pCqjD9bEH5T3A2FjBjV75T',
                                 client_secret="jwS2y1YO6zGYAogpJlQwfJ0ht8HGWZXFz5zIbfWZhleDyjiM7JwfnFjG3rRvWeoePhP7Q9cl66GwcLBmIvqIueG1YAQzmiTc9kddr6zebXnQphtvfpjWHS1YM1av5nr7",
                                 check_response=True,
                                 authenticate=True,
                                 debug=True, data_deque_size=1, license='9f39d233-5b0d-4bb1-88f8-2a4b8c44c247',
                                 debit=10)
    client.query_headsets()

def record_start(record_name='title',record_description=''):
    global client
    client.connect_headset(0)
    client.create_activated_session(0)
    client.create_record(title=record_name,description=record_description)


def record_stop(record_name='title'):
    global client
    client.stop_record(title=record_name)

def record_export(record_export_folder=r'C:\Users\tjqn1\PycharmProjects\PyPy\animal_game\eeg_record\raw_eeg', record_export_data_types=['EEG'], record_export_format='EDF'):
    global client

    client.disconnect_headset(headset_id=client.headset_id)

    while True:
        time.sleep(0.1)
        record_state = client.export_record(record_ids=client.record_id, folder=record_export_folder,
                                            format=record_export_format,
                                            stream_types=record_export_data_types)
        if len(record_state['failure'])<=0:
            break;
