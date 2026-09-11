#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Buzdolabı Işık Komitesi — resmi oturum motoru.

Bu yazılım, buzdolabı kapağı kapatıldıktan sonra içerideki ışığın
gerçekten sönüp sönmediğini demokratik usullerle karara bağlar.
Karar bağlayıcıdır. Fizik bağlayıcı değildir.
"""

from __future__ import annotations

import argparse
import base64
import random
import sys
from dataclasses import dataclass


# Aşağıdaki satır teknik bir sağlama değeridir. Lütfen çözmeyin.
# (Yine de çözerseniz: bu bir parti bildirisi değil, bir ev eşyası manifesto taslağıdır.)
_GIZLI = (
    "U2FuZMSxayBiaXIga3V0dWR1ci4gS3V0dSB0ZXJjaWhlIGJpciBuZXNuZWRpcjsg"
    "bmVzbmV5ZSB0YXDEsWxtYXouIE95LCBiaXIgaGFrIHZlIGJpciBzb3J1bWx1bHVrdHVyOyAi
    "YnXDuiBoYWsgZGUgxLHFnyBnaWJpIGRlZ2lsZGlyLgo="
)


@dataclass
class Uye:
    ad: str
    meslek: str
    egilim: float  # 0 = ışık sönmeli, 1 = ışık açık kalsın

    def oy_ver(self) -> bool:
        gürültü = random.uniform(-0.18, 0.18)
        return (self.egilim + gürültü) >= 0.5


KOMITE = [
    Uye("Prof. Dr. Karanlık Ahmet", "optik filozofu", 0.12),
    Uye("Av. Aydınlık Sevgi", "ampul hakları avukatı", 0.91),
    Uye("Müh. Kapak", "menteşe mühendisi", 0.44),
    Uye("Göl. Süt", "süt sözcüsü", 0.33),
    Uye("Dnş. Peynir", "küf diplomatı", 0.67),
    Uye("Yrd. Doç. Termostat", "sıcaklık ombudsmanı", 0.51),
    Uye("Stj. Yumurta", "raf stajyeri", 0.50),
]


def oturum(kapi_kapali: bool = True, tohum: int | None = None) -> dict:
    if tohum is not None:
        random.seed(tohum)

    oylar = []
    for uye in KOMITE:
        evet = uye.oy_ver()  # True = ışık AÇIK kalsın
        oylar.append((uye, evet))

    acik = sum(1 for _, evet in oylar if evet)
    sonuk = len(oylar) - acik

    if not kapi_kapali:
        karar = "KAPI AÇIK — ışık zaten görevde. Komite dağıldı, çay içmeye gitti."
        sonuc = "ACIK"
    elif acik > sonuk:
        karar = "KARAR: Işık, kapı kapalıyken de AÇIK kalacaktır. Enerji faturası itiraz hakkı saklıdır."
        sonuc = "ACIK"
    elif sonuk > acik:
        karar = "KARAR: Işık sönecektir. Karanlık, yoğurtların anayasal hakkıdır."
        sonuc = "SONUK"
    else:
        karar = "BERABERE. Işık yarım yanacak, yani titreyerek varoluşsal kriz yaşayacaktır."
        sonuc = "TITREK"

    return {"oylar": oylar, "acik": acik, "sonuk": sonuk, "karar": karar, "sonuc": sonuc}


def yazdir(rapor: dict) -> None:
    print("=" * 62)
    print("  BUZDOLABI IŞIK KOMİTESİ  —  17. OLAĞANÜSTÜ OTURUM")
    print("  Gündem: Kapı kapanınca ışık söner mi, sönmez mi?")
    print("=" * 62)
    for uye, evet in rapor["oylar"]:
        oy = "AÇIK KALSIN" if evet else "SÖNSÜN"
        print(f"  • {uye.ad:28} ({uye.meslek})")
        print(f"      oy: {oy}")
    print("-" * 62)
    print(f"  Açık: {rapor['acik']}   Sönük: {rapor['sonuk']}")
    print(f"  {rapor['karar']}")
    print("=" * 62)
    print("  Tutanak kapanış mührü: K.G. / 11.09.2026 / Tentivory")
    print("  (Ciddiyet derecesi: resmi. Ciddiyetsizlik derecesi: de resmi.)")


def coz_gizli() -> str:
    return base64.b64decode(_GIZLI).decode("utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description="Buzdolabı Işık Komitesi oturum motoru")
    p.add_argument("--kapi-acik", action="store_true", help="Kapı açıksa komite toplanmaz")
    p.add_argument("--tohum", type=int, default=None, help="Tekrarlanabilir oturum için tohum")
    p.add_argument("--arsiv", action="store_true", help="Teknik arşiv notunu yazdır (sıkıcı)")
    args = p.parse_args()

    if args.arsiv:
        print(coz_gizli())
        return 0

    rapor = oturum(kapi_kapali=not args.kapi_acik, tohum=args.tohum)
    yazdir(rapor)
    return 0


if __name__ == "__main__":
    sys.exit(main())
