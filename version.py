#!/usr/bin/env python3
"""
Sistema de versionamento - AMS SSIM Converter
"""

VERSION = "1.0.1"
BUILD_DATE = "2025-10-15"
DESCRIPTION = "W25 Amsterdam Schedule to IATA SSIM Converter"

def get_version_info():
    """Retorna informações completas da versão"""
    return {
        "version": VERSION,
        "build_date": BUILD_DATE,
        "description": DESCRIPTION,
        "team": "AMS Team - Capacity Dnata Brasil"
    }
