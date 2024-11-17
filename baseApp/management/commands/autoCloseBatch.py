from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from baseApp.db.application.app_models import TestPost

class Command(BaseCommand):
    """
    テスト自動クローズバッチ処理
    毎日午前０時にバッチ実行を行う。
    """

    help = '自動クローズバッチ処理'

    def handle(self, *args, **options):

        todate = datetime.today()
        yesterday = todate - timedelta(days=1)

        all_tests = TestPost.objects.filter(CanAutoClose=True, DelFlg=False, RecrutingPeriodEnd__date=yesterday)

        for test in all_tests:
            test.RecrutingPeriodFlg = False
            test.save()