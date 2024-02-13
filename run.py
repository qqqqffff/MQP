import sys
import os
from deeplabcut import auxiliaryfunctions, train_network, create_training_dataset, evaluate_network, calibrate_cameras, analyze_videos, extract_frames, create_labeled_video
import time


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
    print('Verifying Video Paths')
    p = cfg['project_path']
    cfg_yaml = p + slash + 'config.yaml'

    cfg_videos = dict(cfg['video_sets'].copy())

    repairs: int = 0
    for vid in cfg_videos.copy():
        vid = str(vid)
        video_index = str(vid).find("videos")
        reconstruct = p + vid[video_index - 1:]
        if vid.find(p) == -1 and os.path.exists(reconstruct):
            cfg_videos[reconstruct] = cfg_videos.get(vid)
            cfg_videos.pop(vid, None)
            repairs = repairs + 1

    auxiliaryfunctions.edit_config(cfg_yaml, {'video_sets': cfg_videos})
    print(f'Paths verified with {repairs} repairs')
    return True


start = sys.argv[1].lower()
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

        res = create_training_dataset(
            config=config_path,
            net_type='resnet_152',
            augmenter_type='tensorpack'
        )

        if res is None:
            print('Failed to create training dataset')
            exit()

    print('Training network')

    shuffle = detect_shuffle(project_path)
    print(f'Shuffle number: {shuffle}')

    start = time.time()
    train_network(
        config=config_path,
        maxiters=max_iters,
        saveiters=display_iters,
        displayiters=display_iters,
        shuffle=shuffle,
        keepdeconvweights=True
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

elif start == 'calibrate':
    calibrate_cameras(
        config=config_path,
        calibrate=True
    )

elif start == 'extract':
    if project.__contains__('3d'):
        print('3d project detected!')
        camera = sys.argv[3]
        if camera is None:
            raise 'Camera not specified'
        i = 0

        for cam in config['camera_names']:
            if camera == cam:
                break
            i = i + 1

        video_set = []
        print(f'Using video subset for: {camera} camera index {i}')
        for video in config['video_sets']:
            if str(video).__contains__(camera):
                video_set.append(str(video))
                print(f'{str(video)} with crop: {config["video_sets"][video].get("crop")}')

        extract_frames(
            config=config_path,
            algo='kmeans',
            mode='automatic',
            userfeedback=False,
            crop=True,
            config3d=True,
            extracted_cam=i,
            videos_list=video_set,
        )

    extract_frames(
        config=config_path,
        algo='kmeans',
        mode='automatic',
        userfeedback=False,
        crop=True
    )

elif start == 'create':
    video = [project_path + slash_char + 'videos' + slash_char + sys.argv[3]]
    create_labeled_video(
        config=config_path,
        videos=video,
    )

