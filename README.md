# CU
CU <sub>( See You )</sub> is a python script that enables you to read plates off live feed and videos.

## Getting Started
- Clone this repository
    ```bash
    git clone https://github.com/YonLiud/CU.git
    cd CU/
    ```
- Install Python requirements:
    ```bash
    pip3 install -r requirements.txt
    ```
- Follow instructions and install [Tesseract](https://tesseract-ocr.github.io/tessdoc/Downloads)
    - For macOS: `brew install tesseract`

## How to run
- Run `detect.py`
  ```bash
  python detect.py --input-source <INPUT>
  python detect.py --input-source 0
  python detect.py --input-source "sample/test.mp4"
  ```
  - For Devices, use Device ID <sub>[INTEGER]</sub>
  - For Files, use full path **AND MAKE SURE THAT THE STRING IS DOES NOT CONTAIN SPECIAL CHARS**

## Demo
<a href="https://ibb.co/hsg6RnB"><img src="https://i.ibb.co/D41JD69/image.png" alt="image" border="0"></a>

## Contributing
PRs are always welcome and are appriciated!
_Hacktoberfest Tag is present :)_
