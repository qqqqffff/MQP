import deeplabcut
import os
import time
import sys

print(f'Using absolute path: {os.getcwd()}')
print(f'Max iterations: {sys.argv[1]}')
display_interval = int(sys.argv[1]) / 100
print(f'Display interval: {sys.argv[2]}')

project_path = os.getcwd() + '/MQP-Apollo-Rowe-2023-09-15/'
if not os.path.exists(project_path):
    print('Default project does not exist')
    exit()

config_path = project_path + 'config.yaml'
if not os.path.exists(config_path):
    print('Configuration file not detected')
    exit()

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

