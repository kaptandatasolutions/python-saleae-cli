# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 13:57:16 2024

@author: Kayhan
"""
import datetime

from saleae import automation


timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


print("Connexion à l'API...")
with automation.Manager.connect() as manager:
    print("API connectée.")

    devices = manager.get_devices(include_simulation_devices=True)
    print("Périphériques disponibles :")
    for device in devices:
        print(f"Nom : {device.device_type}, ID : {device.device_id}, Simulation : {device.is_simulation}")


    simulation_device = next((d for d in devices if d.is_simulation), None)
    if not simulation_device:
        raise ValueError("Aucun périphérique simulé détecté.")

    print(f"Utilisation du périphérique : {simulation_device.device_type}")

    # Configurer la capture
    device_config = automation.LogicDeviceConfiguration(
        enabled_digital_channels=[0],
        digital_sample_rate=10_000_000
    )
    capture_config = automation.CaptureConfiguration(
        capture_mode=automation.TimedCaptureMode(duration_seconds=5)
    )
    print("Lancement de la capture...")
    capture = manager.start_capture(
        device_configuration=device_config,
        device_id=simulation_device.device_id,
        capture_configuration=capture_config
    )
    capture.wait()
    print("Capture terminée.")



    # Sauvegarder la capture dans un fichier
    capture.save_capture(f'C:/Users/Kayhan/python-saleae-cli/signal_test_{timestamp}.sal')
    print(f"Capture simulée sauvegardée sous 'C:/Users/Kayhan/python-saleae-cli/signal_test_{timestamp}.sal'")

