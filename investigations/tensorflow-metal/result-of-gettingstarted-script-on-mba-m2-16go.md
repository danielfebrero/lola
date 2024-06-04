(venv-metal) ➜ metal python3 main  
2024-06-04 06:54:15.125374: I metal_plugin/src/device/metal_device.cc:1154] Metal device set to: Apple M2
2024-06-04 06:54:15.125404: I metal_plugin/src/device/metal_device.cc:296] systemMemory: 16.00 GB
2024-06-04 06:54:15.125411: I metal_plugin/src/device/metal_device.cc:313] maxCacheSize: 5.33 GB
2024-06-04 06:54:15.125620: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:305] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2024-06-04 06:54:15.125637: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:271] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
Epoch 1/5
2024-06-04 06:54:20.783083: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:117] Plugin optimizer for device_type GPU is enabled.
782/782 ━━━━━━━━━━━━━━━━━━━━ 409s 469ms/step - accuracy: 0.0504 - loss: 5.1754  
Epoch 2/5
782/782 ━━━━━━━━━━━━━━━━━━━━ 361s 461ms/step - accuracy: 0.1037 - loss: 4.4456
Epoch 3/5
782/782 ━━━━━━━━━━━━━━━━━━━━ 384s 491ms/step - accuracy: 0.1399 - loss: 3.9393
Epoch 4/5
782/782 ━━━━━━━━━━━━━━━━━━━━ 393s 503ms/step - accuracy: 0.1496 - loss: 3.9044
Epoch 5/5
782/782 ━━━━━━━━━━━━━━━━━━━━ 367s 470ms/step - accuracy: 0.1890 - loss: 3.5684
(venv-metal) ➜ metal pwd  
/Users/danielfebrero/Dev/metal
(venv-metal) ➜ metal cp main ../lola/investigations  
(venv-metal) ➜ metal pip lock
ERROR: unknown command "lock"
(venv-metal) ➜ metal pip freeze > requirements.txt
(venv-metal) ➜ metal mv requirements.txt ../lola/investigations/tensorflow-metal
(venv-metal) ➜ metal
