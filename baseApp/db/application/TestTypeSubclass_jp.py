from django.db import models

class TestTypeSubclass(models.TextChoices):
    # アートとデザイン
    ART_AND_DESIGN            = "アートとデザイン"
    # 自動車と乗り物
    AUTO_AND_VEHICLES         = "自動車と乗り物"
    # 美容
    BEAUTY                    = "美容"
    # 書籍と参照
    BOOKS_AND_REFERENCE       = "書籍と参照"
    # ビジネス
    BUSINESS                  = "ビジネス"
    # コミック
    COMICS                    = "コミック"
    # 通信
    COMMUNICATIONS            = "通信"
    # デート
    DATING                    = "デート"
    # 教育
    EDUCATION                 = "教育"
    # エンターテイメント
    ENTERTAINMENT             = "エンターテイメント"
    # イベント
    EVENTS                    = "イベント"
    # 財務
    FINANCE                   = "財務"
    # 食品と飲料
    FOOD_AND_DRINK            = "食品と飲料"
    # 健康とフィットネス
    HEALTH_AND_FITNESS        = "健康とフィットネス"
    # 家と家庭
    HOUSE_AND_HOME            = "家と家庭"
    # ライブラリとデモ
    LIBRARIES_AND_DEMO        = "ライブラリとデモ"
    # ライフスタイル
    LIFESTYLE                 = "ライフスタイル"
    # 地図とナビゲーション
    MAPS_AND_NAVIGATION       = "地図とナビゲーション"
    # 医療
    MEDICAL                   = "医療"
    # 音楽と音声
    MUSIC_AND_AUDIO           = "音楽と音声"
    # ニュースと雑誌
    NEWS_AND_MAGAZINES        = "ニュースと雑誌"
    # 親子
    PARENTING                 = "親子"
    # 個人化
    PERSONALIZATION           = "個人化"
    # 写真撮影
    PHOTOGRAPHY               = "写真撮影"
    # 生産性
    PRODUCTIVITY              = "生産性"
    # 買い物
    SHOPPING                  = "買い物"
    # ソーシャル
    SOCIAL                    = "ソーシャル"
    # スポーツ
    SPORTS                    = "スポーツ"
    # ツール
    TOOLS                     = "ツール"
    # 旅行と地元
    TRAVEL_AND_LOCAL          = "旅行と地元"
    # ビデオプレイヤーとエディター
    VIDEO_PLAYERS_AND_EDITORS = "ビデオプレイヤーとエディター"
    # 天気
    WEATHER                   = "天気"
