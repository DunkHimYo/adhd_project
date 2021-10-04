import os
from cortex2.emotiv_cortex2_client import EmotivCortex2Client
import time
import yaml
import make_eeg_db
import preprocessing
import model
import joblib
import numpy as np

#warnings.filterwarnings(action='ignore')
with open('C:/eeg_record/user.yaml') as f:
    user = yaml.load(f, Loader=yaml.FullLoader)

def get_eeg_data(message):
    print('good')
    before_message = None
    url = "wss://localhost:6868"
    while True:
        message_method = message['method']

        if before_message!=message_method:
            print(message_method)
            if message_method=='emotiv_create':
                client = EmotivCortex2Client(url,
                                             client_id=user['emotiv']['id'],
                                             client_secret=user['emotiv']['secret'],
                                             check_response=True,
                                             authenticate=True,
                                             debug=True, data_deque_size=1, license='9f39d233-5b0d-4bb1-88f8-2a4b8c44c247',
                                             debit=10)
                client.query_headsets()
                client.connect_headset(0)
                client.request_access()
                client.create_activated_session(0)
                sub = ["eeg"]
                client.subscribe(streams=sub)
                a = make_eeg_db.frame_calculator(client, sub)
                message['loading_chk'] = True

            if message_method == 'record_start':
                c = list()
                tm = list()

                while True:
                    if message['method'] == 'record_stop':
                        try:
                            os.makedirs(f'/eeg_record/raw_eeg')
                        except FileExistsError:
                            pass

                        frame = a.data_request_mk_data_frame(c, tm)
                        frame.to_csv(rf'.\eeg_record\raw_eeg\{time.time()}.csv')
                        break

                    rcv = client.receive_data()

                    if rcv != None:
                        c.append(rcv[sub[0]])
                        tm.append(rcv['time'])

            if message_method =='adhd_result':

                preprocessing.preprocessing()

                scaler = joblib.load('bp_scaler/scale.pkl')
                x = model.feature_data(path='./bandPower/').reshape(1, 19, 10, 7)
                scale_form_bp = np.array([x[:, :, :, i].flatten() for i in range(7)])
                scale_bp = scaler.transform(scale_form_bp.transpose()).reshape(1, 19, 10, 7)
                bp_pred, = model.bp_pred(scale_bp)

                x = model.feature_data(path='./channel_correlation/').reshape(1, 19, 10, 10)
                ch_corr_pred, = model.corr_pred(x)

                x = model.feature_data(path='./psd_correlation/').reshape(1, 19, 10, 10)
                psd_corr_pred, = model.corr_pred(x)

                message['adhd_result']=[bp_pred,ch_corr_pred,psd_corr_pred]
                print(message['adhd_result'])
                message['loading_chk']=True

            before_message = message_method
