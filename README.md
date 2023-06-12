# SPDML RAMP Tool

The SmartPartsDetector (SPD) component was designed for assisting the optical detection of small parts in manufacturing facilities, enabling manufacturers to utilize the technology in various tasks on the shop floor (e.g, QA, part sorting, part counting, etc.)

By design the component depends on a trained ML model that is able to recognise the parts of interest, and an external microservice that runs the ML
model on a given image and stores the predictions on the Orion Context Broker.

We distribute this command line python tool in order to facilitate use of the SPD microservice. 

The latest version of the tool can be downloaded at https://github.com/Algolysis/spd-ramp-tool


## Getting started

A user (e.g., factory) registers a model with the microservice, which deploys the model under the hood,
and then the model can be used to perform object detection tasks. 

```
python3 spd-ramp-tool.py --token AlgoFactory --registerModel ./some_YOLO_model.pt
```

The tool has few modes of operation and only demonstrates the basic capability of the SPD technology. Please refer to its usage(```--help```).

You can lest the available models:

```
python3 spd-ramp-tool.py --token AlgoFactory --list-models
```

To detect objects in an image you have to use a registered model by passing the ```--model <key>``` parameter:

```
python3 spd-ramp-tool.py --token AlgoFactory --model my_model_key_ --predict some_input_image.jpg
```

### Contact

   Please contact us at: [contact@algolysis.com](mailto:contact@algolysis.com)
Bugs & Feature requests: [https://github.com/Algolysis/spd-ramp-tool/issues](https://github.com/Algolysis/spd-ramp-tool/issues)

### LICENSE
[MIT](LICENSE)
