import tempfile
import unittest
from pathlib import Path
from monitors.cpu import cpu_metrics

class CpuTests(unittest.TestCase):
    def test_proc_fallback_reports_shape(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d,'stat').write_text('cpu 100 0 50 850 0 0 0 0\ncpu0 100 0 50 850 0 0 0 0\n')
            Path(d,'loadavg').write_text('0.1 0.2 0.3 1/2 123')
            result=cpu_metrics(80,0,proc_root=d)
            self.assertEqual(result['cpu_count'],1)
            self.assertEqual(result['status'],'OK')
            self.assertEqual(result['load_average'],(0.1,0.2,0.3))

if __name__=='__main__': unittest.main()
