import unittest
from unittest.mock import patch
from monitors.disk import disk_metrics

class DiskTests(unittest.TestCase):
    def test_threshold(self):
        with patch('monitors.disk.shutil.disk_usage',return_value=(1000,900,100)):
            result=disk_metrics('/fake',85)
        self.assertEqual(result['usage_percent'],90.0)
        self.assertEqual(result['status'],'CRITICAL')

if __name__=='__main__': unittest.main()
