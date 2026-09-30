import tempfile
import unittest
from pathlib import Path
from monitors.memory import memory_metrics

class MemoryTests(unittest.TestCase):
    def test_meminfo_fallback_and_threshold(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d,'meminfo').write_text('MemTotal: 1000 kB\nMemAvailable: 100 kB\n')
            result=memory_metrics(80,proc_root=d)
            self.assertEqual(result['usage_percent'],90.0)
            self.assertEqual(result['status'],'CRITICAL')
            self.assertEqual(result['available_bytes'],102400)

if __name__=='__main__': unittest.main()
