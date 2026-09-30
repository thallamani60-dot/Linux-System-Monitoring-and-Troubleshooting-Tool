import unittest
from troubleshooting.incident_detector import detect_incidents
from troubleshooting.recommendations import recommendations
from monitors.services import service_status
from unittest.mock import patch
from types import SimpleNamespace

class MonitorTests(unittest.TestCase):
    def test_incident_generation_and_guidance(self):
        s={'cpu':{'status':'CRITICAL','usage_percent':95,'threshold':80},'services':[]}
        incidents=detect_incidents(s)
        self.assertEqual(len(incidents),1)
        self.assertEqual(incidents[0]['component'],'cpu')
        self.assertTrue(recommendations('cpu'))

    @patch('monitors.services.subprocess.run',return_value=SimpleNamespace(stdout='active\n',stderr='',returncode=0))
    def test_active_service_state(self,_):
        self.assertEqual(service_status('ssh')['status'],'ACTIVE')

    @patch('monitors.services.subprocess.run',return_value=SimpleNamespace(stdout='failed\n',stderr='',returncode=3))
    def test_failed_service_state(self,_):
        self.assertEqual(service_status('nginx')['status'],'FAILED')

if __name__=='__main__': unittest.main()
