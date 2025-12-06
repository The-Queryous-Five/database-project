# Testing Guide - Customers Geo Analytics

Bu doküman, yeni eklenen Customers Geo Analytics endpoint'lerini test etmek için rehberdir.

## 🚀 Hızlı Başlangıç

### 1. Backend Test (Python Script)

```bash
# Flask uygulamasını başlat (bir terminal'de)
flask --app app/app.py run

# Başka bir terminal'de test scriptini çalıştır
python test_geo_analytics.py
```

Test scripti şunları kontrol eder:
- ✅ Health endpoint
- ✅ `/customers/by-city` - valid request
- ✅ `/customers/by-city` - missing parameters (400)
- ✅ `/customers/by-city` - invalid state format (422)
- ✅ `/customers/by-city` - limit out of range (422)
- ✅ `/geo/top-states` - valid request
- ✅ `/geo/top-states` - default limit
- ✅ `/geo/top-states` - limit out of range (422)

### 2. HTTP Test (VS Code REST Client / IntelliJ HTTP Client)

`docs/api_examples.http` dosyasını aç ve endpoint'leri test et:

```http
### Customers by City - Valid request
GET http://localhost:5000/customers/by-city?state=SP&city=sao_paulo&limit=10

### Top States by Customer Count
GET http://localhost:5000/geo/top-states?limit=10
```

### 3. cURL ile Test

```bash
# Health check
curl http://localhost:5000/health

# Customers by City
curl "http://localhost:5000/customers/by-city?state=SP&city=sao_paulo&limit=10"

# Top States
curl "http://localhost:5000/geo/top-states?limit=10"

# Error test - missing state
curl "http://localhost:5000/customers/by-city?city=sao_paulo&limit=10"
# Expected: 400 Bad Request

# Error test - invalid limit
curl "http://localhost:5000/customers/by-city?state=SP&city=sao_paulo&limit=100"
# Expected: 422 Unprocessable Entity
```

### 4. Frontend Test (Manuel)

1. Flask uygulamasını başlat:
   ```bash
   flask --app app/app.py run
   ```

2. `frontend/index.html` dosyasını tarayıcıda aç

3. Customers bölümüne scroll yap

4. "Geo Analytics" bölümünü bul

5. **"Customers by City" testi:**
   - "Use demo values" butonuna tıkla
   - "Get customers by city" butonuna tıkla
   - Sonuçların tablo halinde göründüğünü kontrol et

6. **"Top States" testi:**
   - "Use demo values" butonuna tıkla
   - "Get top states" butonuna tıkla
   - State'lerin customer_count'a göre sıralandığını kontrol et

7. **Error handling testi:**
   - State alanını boş bırak, "Get customers by city" tıkla
   - Kırmızı hata mesajı görünmeli
   - Limit'i 100 yap, hata mesajı görünmeli

## 📋 Test Senaryoları

### Backend Endpoint Testleri

#### `/customers/by-city`

| Senaryo | Parametreler | Beklenen Sonuç |
|---------|-------------|----------------|
| Valid request | `state=SP&city=sao_paulo&limit=10` | 200 OK, customer listesi |
| Missing state | `city=sao_paulo&limit=10` | 400 Bad Request |
| Missing city | `state=SP&limit=10` | 400 Bad Request |
| Invalid state (3 chars) | `state=SPA&city=sao_paulo&limit=10` | 422 Unprocessable Entity |
| Invalid state (lowercase) | `state=sp&city=sao_paulo&limit=10` | 200 OK (uppercase'e çevrilir) |
| Limit too high | `state=SP&city=sao_paulo&limit=100` | 422 Unprocessable Entity |
| Limit too low | `state=SP&city=sao_paulo&limit=0` | 422 Unprocessable Entity |
| Empty city | `state=SP&city=&limit=10` | 422 Unprocessable Entity |

#### `/geo/top-states`

| Senaryo | Parametreler | Beklenen Sonuç |
|---------|-------------|----------------|
| Valid request | `limit=10` | 200 OK, `{items: [...]}` formatında |
| Default limit | (no params) | 200 OK, limit=10 |
| Limit too high | `limit=50` | 422 Unprocessable Entity (max 27) |
| Limit too low | `limit=0` | 422 Unprocessable Entity |

### Frontend Test Senaryoları

1. **Form Validasyonu:**
   - Boş state → Error mesajı
   - Boş city → Error mesajı
   - Limit < 1 veya > 50 → Error mesajı

2. **Demo Butonları:**
   - "Use demo values" → Form alanları doldurulur
   - Otomatik olarak API çağrısı yapılır

3. **Sonuç Gösterimi:**
   - Başarılı response → Tablo formatında gösterilir
   - Boş sonuç → "No results found" mesajı
   - Hata → Kırmızı error mesajı

4. **Loading State:**
   - API çağrısı sırasında "Loading..." gösterilir

## 🔍 Debugging

### Backend Logları

Flask debug mode'da çalıştır:
```bash
flask --app app/app.py --debug run
```

### Database Kontrolü

Eğer endpoint'ler boş sonuç döndürüyorsa, veritabanını kontrol et:

```sql
-- Customers ve geo_zip join kontrolü
SELECT COUNT(*) 
FROM customers c
JOIN geo_zip g ON c.customer_zip_code_prefix = g.geolocation_zip_code_prefix
WHERE g.geolocation_state = 'SP' AND g.geolocation_city = 'sao_paulo';

-- Top states kontrolü
SELECT 
    g.geolocation_state AS state,
    COUNT(*) AS customer_count
FROM customers c
JOIN geo_zip g ON c.customer_zip_code_prefix = g.geolocation_zip_code_prefix
GROUP BY g.geolocation_state
ORDER BY customer_count DESC
LIMIT 10;
```

### Common Issues

1. **"database not available" hatası:**
   - `.env` dosyasını kontrol et
   - Database'in çalıştığından emin ol
   - Connection string'i doğrula

2. **Boş sonuçlar:**
   - ETL scriptlerinin çalıştırıldığından emin ol
   - `geo_zip` tablosunun dolu olduğunu kontrol et
   - City name'lerin doğru format'ta olduğunu kontrol et (örn: `sao_paulo` vs `São Paulo`)

3. **CORS hatası (frontend'den):**
   - Flask CORS middleware eklenmemiş olabilir
   - Frontend'i Flask'ın serve ettiği port'tan açmayı dene

## ✅ Acceptance Criteria Checklist

- [ ] `/customers/by-city` endpoint çalışıyor
- [ ] `/geo/top-states` endpoint çalışıyor
- [ ] Tüm validasyonlar doğru çalışıyor (400, 422 hataları)
- [ ] Frontend'de iki form görünüyor
- [ ] Demo butonları çalışıyor
- [ ] Sonuçlar tablo formatında gösteriliyor
- [ ] Error handling çalışıyor
- [ ] Loading state gösteriliyor
- [ ] Boş sonuçlar düzgün handle ediliyor

## 📝 Notlar

- Test scripti `requests` kütüphanesini kullanır. Yüklü değilse:
  ```bash
  pip install requests
  ```

- Frontend test için tarayıcı console'unu aç (F12) ve network tab'ını kontrol et

- Production'da daha kapsamlı testler için `pytest` kullanılabilir

