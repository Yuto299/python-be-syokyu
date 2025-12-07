# Docker 起動エラーの原因と修正内容

## 問題の原因

### 1. `fastapi`コマンドが見つからないエラー

```
Error: exec: "fastapi": executable file not found in $PATH
```

- `docker-compose.yml`で`fastapi dev`コマンドを使用していた
- `fastapi-cli`パッケージがインストールされていなかった
- FastAPI 0.111.0 以降で利用可能な`fastapi` CLI コマンドには別途`fastapi-cli`パッケージが必要

### 2. モジュールパスの問題（主要因）

```
ModuleNotFoundError: No module named 'app'
```

- Dockerfile の`WORKDIR`が`/opt/python-be-syokyu-app/app`に設定されていた
- `main.py`は`app`ディレクトリ内に存在
- `main.py`内で`from app.const import ...`のように`app`モジュールをインポート
- `uvicorn main:app`で実行すると、`app`ディレクトリの中から`main.py`を探す
- この状態では、Python は`app`という名前のモジュールを見つけられない

## 修正内容

### Dockerfile (`infra/docker/app/Dockerfile`)

```dockerfile
# 修正前
WORKDIR /opt/python-be-syokyu-app/app
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "18008"]

# 修正後
WORKDIR /opt/python-be-syokyu-app
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "18008"]
```

### docker-compose.yml

```yaml
# 修正前
command: fastapi dev main.py --port=${APP_PORT:-18008} --host=0.0.0.0

# 修正後
command: uvicorn app.main:app --reload --host=0.0.0.0 --port=${APP_PORT:-18008}
```

## 解決策の説明

1. **uvicorn コマンドの使用**: 既にインストール済みの`uvicorn`を直接使用することで、追加パッケージ不要
2. **WORKDIR の変更**: プロジェクトルート(`/opt/python-be-syokyu-app`)をワーキングディレクトリに設定
3. **モジュールパスの修正**: `app.main:app`とすることで、Python が`app`ディレクトリをモジュールとして正しく認識できる

これにより、Python は`app`モジュール内の`main.py`ファイル内にある`app`オブジェクト（FastAPI インスタンス）を正しく見つけられるようになった。
