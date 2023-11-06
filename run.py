import sys
import os

print(f'Using absolute path: {os.getcwd()}')
abs_path = os.getcwd()
dlc_path = abs_path + 'DeepLabCut/deeplabcut'
if not os.path.exists(dlc_path):
    dlc_path = abs_path + 'dlc/deeplabcut'
sys.path.insert(0, '')

start = sys.argv[1]

import deeplabcut
import time

project = sys.argv[3]
print(f'Project: {project}')

project_path = os.getcwd() + project
if not os.path.exists(project_path):
    print('Default project does not exist')
    exit()

config_path = project_path + 'config.yaml'
if not os.path.exists(config_path):
    print('Configuration file not detected')
    exit()

if start == "train":
    print(f'Max iterations: {sys.argv[2]}')
    display_interval = int(sys.argv[2]) / 100
    print(f'Display interval: {display_interval}')

    if not os.path.exists(project_path + 'training-datasets'):
        print('Training dataset not found...')
        print('Creating training dataset')

        start = time.time()
        res = deeplabcut.create_training_dataset(
            config=config_path,
            net_type='resnet_50'
        )

        if res is None:
            print('Failed to create training dataset')
            exit()

        end = time.time()
        print(f'Created in {end - start}ms')

    print('Training network')

    start = time.time()
    deeplabcut.train_network(
        config=config_path,
        maxiters=int(sys.argv[1]),
        saveiters=int(sys.argv[1]) / 10,
        displayiters=display_interval,
    )
    end = time.time()

    print(f'Training completed in {end - start}ms')

elif start == "eval":
    print('Attempting Evaluate...')

    start = time.time()

    deeplabcut.evaluate_network(
        config=config_path,
        Shuffles=[1],
        plotting=True,
    )

    end = time.time()

    print(f'Finished eval in {end - start}ms')

elif start == 'analyze':
    print('Attempting Analyze...')

    videos = []

    if not sys.argv[2] == '*':
        for x in sys.argv:
            index = x.find('.')
            if index == -1:
                continue
            ending = x[index+1:]
            if ending == 'mp4':
                videos.append(x)
    else:
        videos.append(project_path + '/videos')

    deeplabcut.analyze_videos(
        config=config_path,
        videos=videos,
        save_as_csv=True,
        videotype='mp4'
    )