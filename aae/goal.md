# AAE Mission 03: The Judge (Validation Engine)

## 🎯 Objective
Meningkatkan akurasi otonom dengan mengimplementasikan sistem pengujian fungsional otomatis sebelum kode dianggap "SUCCESS".

## 🛠️ Fitur Baru (Gen 3)
1. **Dynamic Test Runner**: AAE akan mencari file pengujian (misal: `test_gen.py`) dan menjalankannya secara otomatis.
2. **Dynamic Metric Scoring**: Skor metrik tidak lagi statis (85), melainkan dihitung berdasarkan persentase *test cases* yang lolos.
3. **API Integrity Check**: Melakukan "ping" ke endpoint lokal untuk memastikan server tidak mati setelah injeksi kode baru.
4. **Auto-Correction Loop**: Jika gagal tes, AAE akan mencoba memperbaiki dirinya sendiri satu kali sebelum menyerah (Rollback).

## 🧪 Success Criteria
- [ ] Mesin mampu menghitung skor metrik secara dinamis (0-100).
- [ ] Gagal tes fungsional memicu 'FAILED' meskipun sintaks benar.
- [ ] Log menunjukkan rincian tes mana yang gagal.
