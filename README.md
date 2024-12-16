# BurnMD dataset
## Summary
This is a repository for hosting the BurnMD database. It contains the burnmd database, as well as a cleaned version of the dataset and several scripts for evaluating a simulator against the dataset. [Dotter, M., Schambach, L., Bedford, M. A., Smith, S., & Welsh, T. (2023). Burnmd: A fire projection and mitigation modeling dataset. In ICLR 2023 Workshop on Tackling Climate Change with Machine Learning](https://s3.us-east-1.amazonaws.com/climate-change-ai/papers/iclr2023/19/paper.pdf))
## Definitions
* Projection - predicted fire burned area
* Mitigation - method used/line placed to prevent the spread of fire
    - Fireline - mitigation involving digging ditch to prevent fire from burning through area
    - Wetline - mitigation involving creating wet area to prevent fire from spreading through line
    - Scratchline - Unfinished preliminary Fireline
* Perimeter - outer edge of burned area
## Organization
* BurnMD.zip - zip containing entire burnmd database
* BurnMD\_cleaned.zip - zip containing cleaned burnmd database
    - data has been cleaned to only fires that can successfully run with simfire (add citation?)
    - folders are stored as state-\>year of fire
* scripts/ directory containing various evaluation scripts
## Installation
* Install pyenv
```
curl https://pyenv.run | bash

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
```
* install python version
```
pyenv install 3.9.19
pyenv local 3.9.19
```
* install poetry
```
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```
* install repository
```
poetry shell
poetry install
```
* unzip database
```
unzip BurnMD.zip
unzip BurnMD\_cleaned.zip
```
## Examples
* To run an example script, run the following:
```
python scripts/get_historical_error.py
```
This will output a series of gifs showing errors on the historical fires, and an errors.csv file showing data metrics on these fires over time. Columns are summarized below:
* total\_error: mismatched burn pixels as a percentage of the overall image
* normalized\_error: mismatched burn pixels as a percentage of burned area in both historical and simulated
* false\_positive\_error: burned pixels in simulation that aren't burned in historical as a percentage of simulated burned pixels
* false\_negative\_error: burned historical pixels that aren't burned in simulation as a percentage of historical burned pixels
## Copyright
Copyright ©2023 The MITRE Corporation. ALL RIGHTS RESERVED. Approved for Public Release; Distribution Unlimited. Public Release Case Number 22-3261. (note to savanah, is this the same?)
