# 起動手順
## 事前準備
1. Mysqlをインストール

## リポジトリクローンからrunserver
1. ルートフォルダ作成
2. ルートにvenv作成
3. ルートにリポジトリクローン
4. venvに入る[ xxx/Scripts/Activate.ps1 ] xxxはvenvの名前
5. cdでクローンしたリポジトリへ入る
6. [ pip install -r requirements.txt ]でパッケージインストール
7. settings.pyのDB関連情報をインストールしたMysqlに沿って修正（userやpass）
   
※mysqlではなくsqlite3を使用する場合は下記に書き換え（mysqlではなくベースディレクトリにdbを作成する）

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

9. [ python manage.py makemigrations ]でマイグレーションファイルを作成
10. [ python manage.py migrate ]でDBへマイグレーション情報を反映
11. [ python manage.py createsuperuser ] でスーパーユーザー（管理者アカウント）を作成
12. [python manage.py runserver ] でサーバー起動（エラー表記が出るがgcpデプロイ用の処理がコケてるだけなので無視）
13. 遊ぶ
