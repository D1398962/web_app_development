from flask import Blueprint, render_template, request

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/", methods=["GET"])
def index():
    """統計儀表板

    Query 參數：
        period (str): 時間範圍 'year'（今年，預設）/ 'all'（全部時間）

    回傳：
        渲染 dashboard/index.html，傳入統計數據 dict：
            - total_books      (int):   總書籍數
            - month_books      (int):   本月閱讀數
            - year_books       (int):   本年閱讀數
            - avg_rating       (float): 平均評分
            - top_books        (list):  Top 3 高分書籍
            - category_data    (dict):  各標籤書籍數（圓餅圖用）
            - monthly_trend    (list):  過去 12 個月閱讀量（折線圖用）
            - period           (str):   目前選擇的時間範圍
    """
    pass
