import deeplabcut

path = 'E:\MQP\MQP-Apollo-Rowe-2023-09-15\config.yaml'

# deeplabcut.create_training_dataset(
#     config=path,
#     net_type='resnet_50'
# )
deeplabcut.train_network(
    config=path,
    maxiters=10000,
)

