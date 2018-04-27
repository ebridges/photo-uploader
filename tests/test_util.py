"""
Unit tests for photo_uploader.util
"""

from photo_uploader import util
from unittest import TestCase, main


class TestPhotoUploaderUtil(TestCase):
  def test_item_folder_normal_1(self):
    EXPECTED_RESULT='2017/2017-09-23'
    test_data = './2017/2017-09-23/20170923T123456.jpg'
    ACTUAL_RESULT = util.item_folder(test_data)
    self.assertEqual(EXPECTED_RESULT, ACTUAL_RESULT)


  def test_item_folder_normal_2(self):
    EXPECTED_RESULT='2017/2017-09-23'
    test_data = '2017/2017-09-23/20170923T123456.jpg'
    ACTUAL_RESULT = util.item_folder(test_data)
    self.assertEqual(EXPECTED_RESULT, ACTUAL_RESULT)


  def test_item_folder_none(self):
    EXPECTED_RESULT=None
    test_data=None
    ACTUAL_RESULT=util.item_folder(test_data)
    self.assertEqual(EXPECTED_RESULT, ACTUAL_RESULT)


  def test_item_folder_empty(self):
    EXPECTED_RESULT=None
    test_data=''
    ACTUAL_RESULT=util.item_folder(test_data)
    self.assertEqual(EXPECTED_RESULT, ACTUAL_RESULT)

