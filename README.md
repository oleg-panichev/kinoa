# Kinoa
[![GitHub release](https://img.shields.io/badge/Version-0.0.1-blue.svg)](https://github.com/oleg-panichev/kinoa)

Kinoa - a simple library to store your code and produced files after each run. It allows monitor, easily compare  and reproduce experiments with your code.

Tested on Python 3.6.1 only. 

## Installation
```sh
git clone https://github.com/oleg-panichev/kinoa.git
cd kinoa
python setup.py install
```

## Usage
```python
from kinoa import kinoa

# Your code here

kinoa.save(
    files,
    experiment_name=experiment_name,
    params=params,
    scores=scores,
    comments=comments,
    working_dir=''
)
```

Parameters:
```python
def save(files, experiment_name='', params={}, scores={}, comments='', working_dir='')
```

- **files** - list of files and directories to save.
- **experiment_name** - string with name of an experiment. If empty - date and time used to define the name in a format *%Y-%m-%d_%H-%M-%S*.
- **params** - dictionary with parameters of experiment.
- **scores** - dictionary with evaluation results.
- **comments** - string with comments to the experiment.
- **working_dir** - directory where log of experiments will be stored. *\_\_kinoa\_\_* directory will be created within working_dir.

See [examples/example.py](https://github.com/oleg-panichev/Kinoa/blob/master/examples/example.py) for more details.

## License
Apache License Version 2.0, January 2004

## Authors
- Oleg Panichev ([olegxpanichev@gmail.com](mailto:olegxpanichev@gmail.com))
