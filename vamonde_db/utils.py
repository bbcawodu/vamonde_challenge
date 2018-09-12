# -*- coding: utf-8 -*-
import csv
import json


def open_csv_file_and_convert_data_to_list(csv_file, encoding=None):
  if encoding:
    with open(csv_file, encoding=encoding) as file_obj:
        reader = csv.reader(file_obj)
        data_list = list(reader)
  else:
    with open(csv_file) as file_obj:
        reader = csv.reader(file_obj)
        data_list = list(reader)

  return data_list
