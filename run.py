import sys
import os
from deeplabcut import auxiliaryfunctions, train_network, create_training_dataset, evaluate_network, calibrate_cameras, analyze_videos, extract_frames
import time
import ruamel.yaml.representer
import yaml
from ruamel.yaml import YAML
from pathlib import Path


def detect_shuffle(path):
    models = path + '/dlc-models'
    if not os.path.exists(models):
        print('Path does not exist')
        return -1
    iteration = os.scandir(models)
    max_shuffle = -1
    for directory in iteration:
        directory_name = directory.name
        if directory.is_dir() and directory_name.__contains__("iteration"):
            shuffle_number = ""
            for char in directory_name:
                if char.isnumeric():
                    shuffle_number = shuffle_number + char
            max_shuffle = max(int(shuffle_number), max_shuffle)
    return max_shuffle


def verify_paths(cfg, slash):
    p = cfg['project_path']
    cfg_yaml = p + slash + 'config.yaml'

    cfg_videos = dict(cfg['video_sets'].copy())

    for video in cfg_videos.copy():
        video = str(video)
        video_index = str(video).find(slash + "videos")
        reconstruct = p + video[video_index:]
        if video.find(p) == -1 and os.path.exists(reconstruct):
            cfg_videos[reconstruct] = cfg_videos[video]
            cfg_videos.pop(video, None)

    auxiliaryfunctions.edit_config(cfg_yaml, {'video_sets': cfg_videos})
    return True


start = sys.argv[1]
print(f'Using absolute path: {os.getcwd()}')
abs_path = os.getcwd()

slash_char = '/'
project = sys.argv[2]
if project[0] == '.':
    project = project[1:]
if project[0] == '\\':
    slash_char = '\\'
print(f'Project: {project}')

project_path = os.getcwd() + project
print(f'Project Path: {project_path}')
if not os.path.exists(project_path):
    print('Project specified does not exist')
    exit()

config_path = project_path + 'config.yaml'
if not project_path[-1] == '\\' and not project_path[-1] == '/':
    config_path = project_path + slash_char + 'config.yaml'
print(f'Configuration File Path: {config_path}')
if not os.path.exists(config_path):
    print('Configuration file not found')
    exit()

config = auxiliaryfunctions.read_config(configname=config_path)
verify_paths(config, slash_char)

if start == "train":
    max_iters = int(sys.argv[3])
    display_iters = int(sys.argv[3]) / 25

    print(f'Max iterations: {max_iters}')
    print(f'Display interval: {display_iters}')

    if not os.path.exists(project_path + 'training-datasets'):
        print('Training dataset not found...')
        print('Creating training dataset')

        start = time.time()
        res = create_training_dataset(
            config=config_path,
            net_type='resnet_50'
        )

        if res is None:
            print('Failed to create training dataset')
            exit()

        end = time.time()
        print(f'Created in {end - start}ms')

    print('Training network')

    shuffle = detect_shuffle(project_path) + 1
    print(f'Shuffle number: {shuffle}')

    start = time.time()
    train_network(
        config=config_path,
        maxiters=max_iters,
        saveiters=display_iters,
        displayiters=display_iters,
        shuffle=shuffle
    )
    end = time.time()

    print(f'Training completed in {end - start}ms')

elif start == "eval":
    print('Attempting Evaluate...')

    start = time.time()

    shuffle = detect_shuffle(project_path)

    evaluate_network(
        config=config_path,
        Shuffles=[shuffle],
        plotting=True,
    )

    end = time.time()

    print(f'Finished eval in {end - start}ms')

elif start == 'analyze':
    print('Attempting Analyze...')

    videos = []

    # if not sys.argv[3] == '*':
      #  for x in sys.argv:
       #     index = x.find('.')
        #    if index == -1:
         #       continue
          #  ending = x[index+1:]
           # if ending == 'mp4':
            #    videos.append(x)
    # else:
    videos.append(project_path + slash_char + 'videos')
    print('Analyzing all videos')

    analyze_videos(
        config=config_path,
        videos=videos,
        save_as_csv=True,
        videotype='mp4'
    )

elif start == 'Calibrate':
    calibrate_cameras(
        config=config_path,
        calibrate=True
    )

elif start == 'Extract':
    extract_frames(
        config=config_path,
        algo='kmeans',
        mode='automatic',
        userfeedback=False
    )