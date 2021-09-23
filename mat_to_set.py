import matlab.engine
import os

eng = matlab.engine.start_matlab()
for i in [i for i in os.listdir('./dataset') if 'ADHD' in i or 'Control' in i ]:
    try:
        path=rf'./adhd/{i}'
        os.makedirs(path)
    except:
        pass

    for n,j in enumerate(os.listdir(f'./dataset/{i}'),start=1):
        if 'ADHD' in i:
            name='ADHD'
        elif 'Control' in i:
            name='Control'
        eng.eval(rf"EEG=pop_importdata('setname','{name}_{n}', 'data','C:\Users\tjqn1\PycharmProjects\PythonProject\dataset\{i}\{j}', 'dataformat','matlab', 'srate', 128, 'chanlocs','C:\Users\tjqn1\PycharmProjects\PythonProject\dataset\Standard-10-20-Cap19new\Standard-10-20-Cap19new.ced')", nargout=0)
        eng.eval(rf"pop_saveset(EEG, 'filename', '{name}_{n}', 'filepath', '{path}', 'savemode', 'onefile')", nargout=0)
