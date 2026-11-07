"""Testes do Estudio sem iniciar inferencia neural demorada."""
import json
import unittest
from unittest.mock import patch
from urllib.request import urlopen
from pathlib import Path
import job_manager

BASE='http://127.0.0.1:18765'

class EstudioTests(unittest.TestCase):
    def test_pagina(self):
        with urlopen(BASE+'/estudio',timeout=5) as r:
            body=r.read().decode('utf-8')
            self.assertEqual(r.status,200)
            self.assertIn('Gerar teste real de 2 s',body)
            self.assertIn('Salvar JSON',body)
            self.assertIn('Importar JSON',body)
    def test_listas(self):
        with urlopen(BASE+'/api/avatares',timeout=5) as r:
            av=json.load(r)['avatares']
        with urlopen(BASE+'/api/audios',timeout=5) as r:
            au=json.load(r)['audios']
        self.assertGreater(len(av),0)
        self.assertGreater(len(au),0)
    def test_opcoes_validas_sem_renderizar(self):
        avatar=next(job_manager.AVATARS.glob('avatar-*')).name
        audio=next(job_manager.OUT.glob('wmk-*.wav')).name
        options={'preview_seconds':2,'threads':4,'batch_size':1,'preprocess':'crop','still':False,'pose_style':5,'expression_scale':1.2,'yaw':5,'pitch':0,'roll':0,'face3dvis':False,'verbose':False}
        with patch.object(job_manager.threading.Thread,'start',lambda self:None):
            j=job_manager.start(audio,avatar,options)
        self.assertEqual(j['estado'],'executando')
        self.assertRegex(j['id'],r'^[a-f0-9]{32}$')
        with job_manager.LOCK:
            job_manager.JOBS.pop(j['id'],None)
    def test_valores_invalidos(self):
        avatar=next(job_manager.AVATARS.glob('avatar-*')).name
        audio=next(job_manager.OUT.glob('wmk-*.wav')).name
        for options in ({'pose_style':46},{'expression_scale':2.5},{'threads':8},{'preview_seconds':1},{'yaw':90},{'batch_size':9}):
            with self.subTest(options=options),self.assertRaises(ValueError):
                job_manager.start(audio,avatar,options)

if __name__=='__main__': unittest.main(verbosity=2)
