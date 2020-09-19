# Convert Marmot Math Dataset to TFD-ICDAR 2019 compatible dataset [![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

The [Marmot Math Dataset ](http://www.icst.pku.edu.cn/cpdp/docs/20190424192347869700.zip) is a part of [Marmot Dataset](http://www.icst.pku.edu.cn/cpdp/sjzy/index.htm) for mathematical formula identification. Convertation this to TFD-ICDAR 2019 compatible dataset allow to use [Evaluation and Visualization tools](https://github.com/MaliParag/TFD-ICDAR2019/tree/master/TFD-ICDAR2019v2) for a [Dataset for Typeset Math Formula Detection](https://github.com/MaliParag/TFD-ICDAR2019).

## Usage
`marmot2ICDAR.py [-h] --xml_dir 'ground truth' --img_dir image --dest_img_dir  DEST_IMG_DIR --dest_math_dir DEST_MATH_DIR`
where:  
* 'ground truth' - the directory with bounding boxes info .xml files  
* image - the directory with images of doc pages  
* DEST_IMG_DIR - the directory of directories with ICDAR-style doc image files  
* DEST_MATH_DIR - the directory of ICDAR-style math groung truth .csv files (such as [
TFD-ICDAR2019/TFD-ICDAR2019v2/Train/math_gt/
](https://github.com/MaliParag/TFD-ICDAR2019/tree/master/TFD-ICDAR2019v2/Train/math_gt), for example)