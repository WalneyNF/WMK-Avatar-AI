"""Testes HTTP do monitor sem executar inferencia pesada."""
import json
import sys
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError

sys.path.insert(0, str(Path(__file__).resolve().parent))
import server
import job_manager

class MonitorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        cls.port = cls.http.server_port
        cls.thread = threading.Thread(target=cls.http.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown()
        cls.http.server_close()

    def fetch(self, path):
        with urlopen("http://127.0.0.1:%d%s" % (self.port, path), timeout=5) as r:
            return r.status, r.read()

    def test_monitor_html(self):
        status, data = self.fetch("/monitor")
        self.assertEqual(status, 200)
        self.assertIn(b"Monitor", data)

    def test_audio_list(self):
        status, data = self.fetch("/api/audios")
        self.assertEqual(status, 200)
        self.assertIsInstance(json.loads(data)["audios"], list)

    def test_unknown_job(self):
        with self.assertRaises(HTTPError) as ctx:
            self.fetch("/api/jobs/" + "0" * 32)
        self.assertEqual(ctx.exception.code, 404)

    def test_job_status(self):
        job_id = "1" * 32
        with job_manager.LOCK:
            job_manager.JOBS[job_id] = {"id": job_id, "estado": "executando", "etapa": "Renderizacao", "etapa_indice": 5, "percentual_etapa": 17, "quadros_feitos": 18, "quadros_total": 105, "logs": __import__("collections").deque(["Face Renderer 18/105"]), "inicio": 1, "atualizado": 2}
        try:
            status, data = self.fetch("/api/jobs/" + job_id)
            result = json.loads(data)
            self.assertEqual(status, 200)
            self.assertEqual(result["quadros_feitos"], 18)
            self.assertEqual(result["percentual_etapa"], 17)
        finally:
            with job_manager.LOCK:
                job_manager.JOBS.pop(job_id, None)

    def test_reject_invalid_job(self):
        request = Request("http://127.0.0.1:%d/api/jobs" % self.port, data=b'{"audio":"../foo","avatar":"bad"}', headers={"Content-Type": "application/json"})
        with self.assertRaises(HTTPError) as ctx:
            urlopen(request, timeout=5)
        self.assertEqual(ctx.exception.code, 400)

if __name__ == "__main__":
    unittest.main(verbosity=2)
