# CU

CU <sub>( See You )</sub> is a python script that enables you to read plates off live feed and videos



## Install

1) Python Requirements:
```sh
pip3 install -r requirements.txt
```

2) Download Tesseract at [https://tesseract-ocr.github.io/tessdoc/Downloads](https://tesseract-ocr.github.io/tessdoc/Downloads)

## Configure

##### Configure Input Device / File
* For Devices use Device ID <sub>[INTEGER]</sub>
  ```sh
  echo INPUT="DeviceID" > .env
  ```
* For Files use full path **AND MAKE SURE THAT THE STRING IS DOES NOT CONTAIN SPECIAL CHARS**
  ```sh
  echo INPUT="Path\To\File" > .env
  ```
  ---
  Example of `.env` file  
  ```env
  INPUT="C:\Users\Yon\Videos\DataCU\\plate.mp4"
  ```

## Demo

<a href="https://ibb.co/hsg6RnB"><img src="https://i.ibb.co/D41JD69/image.png" alt="image" border="0"></a>

## Contributing

PRs are always welcome and are appriciated!
_Hacktoberfest Tag is present :)_
