# An Auto typing script for NEEP(National Entrance Examination for Postgraduates of China) English II Paper

- see [video](http://to_be_added)
## Prerequisites:

```
pip install python-docx
pip install pandas
pip install nltk
pip install argparse
pip install tqdm
```

## commands

```
optional arguments:
  -h, --help         show this help message and exit
  -d , --directory   required, directory for yaml surce files
  -n , --name        required, name prefix for output files'
  -t , --title       paper title suffix, default Empty

```
## Usage
Download the project to your local machine, install the prerequisites, and place source files under a relavent directory.

## Exec example

```
 python3 main.py -d ../inputs/source_dir/ -n output_name
 
```

9 source files must be placed under source_dir/. Give the directory a relavent name and it is recommended to place it under ../inputs/, although it's not required.

The source files are autodetected according to their names so make sure to name them properly.

More info watch the video linked at the top.

