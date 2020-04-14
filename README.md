# NCU CSIE 2020 Spring Computational Intelligence HW1


## Getting Started

### Demo
<img src="https://i.imgur.com/yoetTME.gif" width="400">

### Prerequisites

This project use Python 3 and needs following packages.

```
matplotlib
numpy
shapely
```

### Installing

Clone this project and install by requirements.txt.


```
git clone https://github.com/ysam12345/ci_hw1
```

And install packages

```
cd ci_hw1
pip install -r requirement.txt
```


## Running
Just run the gui.py
```
cd src
python gui.py
```
or
```
python3 gui.py
```

If your see following error on windows
```
CDLL(os.path.join(sys.prefix, 'Library', 'bin', 'geos_c.dll'))
OSError: [WinError 126] 找不到指定的模組。
```
Please consider install shpely via conda.
```
conda install shapely
```

## GUI
Click Run. And the car will start running unitl crash or finish.
![](https://i.imgur.com/qJyidwT.png)




## Authors

* **Yochien** - *NCU CSIE* -  <yochien@g.ncu.edu.tw>
