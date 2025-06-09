## 1. Склонировать образ
```
git clone git@github.com:daniilvs/flask_api.git
```

## 2. Собрать образ 
```
docker build -t backend .
docker-compose up -d
```

## 3. Убедиться в работоспособности
```
curl http://127.0.0.1:5000/ping
curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"name": "Jerma", "score": 100}'
curl http://127.0.0.1:5000/results
```

## 4. CI/CD
в процессе настройки