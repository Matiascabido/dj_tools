"""
Motor de Adquisición Web de Samples (web_sample_acquisition_engine.py)
Responsabilidad: Buscar, descargar, analizar y organizar samples gratuitos.
"""

import os
import requests
import hashlib
from bs4 import BeautifulSoup
import librosa
import numpy as np
from pydub import AudioSegment
from config.config import (
    ENABLE_WEB_ACQUISITION, PIXABAY_API_KEY, ENABLE_LANDR, ENABLE_LOOPMASTERS,
    LOOPMASTERS_USERNAME, LOOPMASTERS_PASSWORD, SAMPLES_TO_DOWNLOAD, ANALYSIS_THRESHOLDS
)

class WebSampleAcquisitionEngine:
    def __init__(self):
        self.session = requests.Session()
        self.downloaded_hashes = set()  # Para evitar duplicados

    def acquire_samples(self):
        """Adquiere samples de fuentes configuradas."""
        if not ENABLE_WEB_ACQUISITION:
            return

        for instrument, count in SAMPLES_TO_DOWNLOAD.items():
            samples = []
            if PIXABAY_API_KEY:
                samples.extend(self._search_pixabay(instrument, count // 2))  # Mitad de Pixabay
            if ENABLE_LANDR:
                samples.extend(self._scrape_landr(instrument, count // 2))
            if ENABLE_LOOPMASTERS and LOOPMASTERS_USERNAME:
                samples.extend(self._scrape_loopmasters(instrument, count // 2))

            # Descargar y analizar
            for url in samples[:count]:
                self._download_and_analyze(url, instrument)

    def _search_pixabay(self, instrument, count):
        """Buscar en Pixabay via scraping (sin API key)."""
        query = f"techno {instrument} sample free"
        url = f"https://pixabay.com/es/sound-effects/search/{query.replace(' ', '%20')}/"
        try:
            response = self.session.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Buscar links de audio (ajustar selector basado en HTML real)
            audio_links = []
            for link in soup.find_all('a', href=True):
                if 'sound' in link['href'] and ('.wav' in link['href'] or '.mp3' in link['href']):
                    audio_links.append(link['href'])
            return audio_links[:count]
        except:
            return []

    def _login_pixabay(self):
        """Login a Pixabay por terminal (opcional)."""
        username = input("Pixabay Username (opcional): ")
        password = input("Pixabay Password (opcional): ")
        login_url = "https://pixabay.com/accounts/login/"  # Ajustar
        payload = {"username": username, "password": password}
        self.session.post(login_url, data=payload)

    def _scrape_landr(self, instrument, count):
        """Scraping de LANDR (con login si necesario)."""
        url = f"https://samples.landr.com/genres/techno/{instrument}"
        # Verificar si requiere login
        response = self.session.get(url)
        if "login" in response.text.lower() or response.status_code == 401:
            self._login_landr()
            response = self.session.get(url)
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            audio_links = [link['href'] for link in links if link['href'].endswith('.wav') or '.mp3' in link['href']]
            return audio_links[:count]
        except:
            return []

    def _login_landr(self):
        """Login a LANDR por terminal."""
        username = input("LANDR Username: ")
        password = input("LANDR Password: ")
        login_url = "https://samples.landr.com/login"  # Ajustar URL real
        payload = {"username": username, "password": password}
        self.session.post(login_url, data=payload)

    def _scrape_loopmasters(self, instrument, count):
        """Scraping de Loopmasters (con login)."""
        # Login primero
        self._login_loopmasters()
        url = f"https://www.loopmasters.com/myaccount"  # Ajustar a búsqueda
        try:
            response = self.session.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Parsear samples (placeholder)
            links = soup.find_all('a', href=True)
            audio_links = [link['href'] for link in links if 'sample' in link['href']]
            return audio_links[:count]
        except:
            return []

    def _login_loopmasters(self):
        """Login a Loopmasters por terminal."""
        username = input("Loopmasters Username: ")
        password = input("Loopmasters Password: ")
        login_url = "https://www.loopmasters.com/login"  # Ajustar URL real
        payload = {"username": username, "password": password}
        self.session.post(login_url, data=payload)

    def _download_and_analyze(self, url, instrument):
        """Descarga, valida, analiza y organiza."""
        try:
            response = self.session.get(url, stream=True)
            if response.status_code != 200:
                return

            # Calcular hash para evitar duplicados
            content = response.content
            file_hash = hashlib.md5(content).hexdigest()
            if file_hash in self.downloaded_hashes:
                return
            self.downloaded_hashes.add(file_hash)

            # Guardar temporalmente
            temp_path = f"/tmp/temp_{instrument}_{file_hash}.wav"
            with open(temp_path, 'wb') as f:
                f.write(content)

            # Convertir a WAV si necesario
            if not temp_path.endswith('.wav'):
                audio = AudioSegment.from_file(temp_path)
                temp_path = temp_path.replace('.mp3', '.wav')
                audio.export(temp_path, format='wav')

            # Analizar
            duration, rms, classification = self._analyze_sample(temp_path)

            # Filtrar por thresholds
            thresh = ANALYSIS_THRESHOLDS.get(instrument, {})
            if (duration < thresh.get('min_duration', 0) or duration > thresh.get('max_duration', 10) or
                rms < thresh.get('min_rms', 0)):
                os.remove(temp_path)
                return

            # Renombrar y mover
            folder = f"samples/{instrument}"
            os.makedirs(folder, exist_ok=True)
            new_name = f"{instrument}_{len(os.listdir(folder)) + 1}_{classification}.wav"
            final_path = os.path.join(folder, new_name)
            os.rename(temp_path, final_path)

            # Actualizar SOUND_PALETTE (simulado; en producción, modificar config.py)
            print(f"Sample adquirido: {final_path} (Dur: {duration:.2f}s, RMS: {rms:.2f}, Class: {classification})")

        except Exception as e:
            print(f"Error descargando {url}: {e}")

    def _analyze_sample(self, path):
        """Analiza duración, RMS y clasifica utilidad."""
        try:
            y, sr = librosa.load(path, sr=None)
            duration = librosa.get_duration(y=y, sr=sr)
            rms = np.mean(librosa.feature.rms(y=y))
            # Clasificación simple
            if rms > 0.5:
                classification = "fuerte"
            elif rms > 0.3:
                classification = "medio"
            else:
                classification = "suave"
            return duration, rms, classification
        except:
            return 0, 0, "invalido"