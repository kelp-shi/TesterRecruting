from django.db import models

class TestTypeSubclass (models.TextChoices):
    # アートとデザイン
    ART_AND_DESIGN            = "Art And Design"
    # 自動車と乗り物
    AUTO_AND_VEHICLES         = "Auto And Vehicles"
    # 美容
    BEAUTY                    = "Beauty"
    # 書籍と参照
    BOOKS_AND_REFERENCE       = "Books And Reference"
    # ビジネス
    BUSINESS                  = "Business"
    # コミック
    COMICS                    = "Comics"
    # 通信
    COMMUNICATIONS            = "Communications"
    # デート
    DATING                    = "Dating"
    # 教育
    EDUCATION                 = "Education"
    # エンターテイメント
    ENTERTAINMENT             = "Entertainment"
    # イベント
    EVENTS                    = "Events"
    # 財務
    FINANCE                   = "Finance"
    # 食品と飲料
    FOOD_AND_DRINK            = "Food And Drink"
    # 健康とフィットネス
    HEALTH_AND_FITNESS        = "Health And Fitness"
    # 家と家庭
    HOUSE_AND_HOME            = "House And Home"
    # ライブラリとデモ
    LIBRARIES_AND_DEMO        = "Libraries And Demo"
    # ライフスタイル
    LIFESTYLE                 = "Lifestyle"
    # 地図とナビゲーション
    MAPS_AND_NAVIGATION       = "Maps And Navigation"
    # 医療
    MEDICAL                   = "Medical"
    # 音楽と音声
    MUSIC_AND_AUDIO           = "Music And Audio"
    # ニュースと雑誌
    NEWS_AND_MAGAZINES        = "News And Magazines"
    # 親子
    PARENTING                 = "Parenting"
    # 個人化
    PERSONALIZATION           = "Personalization"
    # 写真撮影
    PHOTOGRAPHY               = "Photography"
    # 生産性
    PRODUCTIVITY              = "Productivity"
    # 買い物
    SHOPPING                  = "Shopping"
    # ソーシャル
    SOCIAL                    = "Social"
    # スポーツ
    SPORTS                    = "Sports"
    # ツール
    TOOLS                     = "Tools"
    # 旅行と地元
    TRAVEL_AND_LOCAL          = "Travel And Local"
    # ビデオプレイヤーとエディター
    VIDEO_PLAYERS_AND_EDITORS = "Video Players And Editors"
    # 天気
    WEATHER                   = "Weather"