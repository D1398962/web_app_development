from flask import Blueprint, make_response

export_bp = Blueprint("export", __name__, url_prefix="/export")


@export_bp.route("/csv", methods=["GET"])
def export_csv():
    """匯出所有書籍資料為 CSV 檔案

    回傳：
        Content-Disposition: attachment
        檔名格式：reading_notes_YYYYMMDD.csv
        無資料時仍回傳含標題列的空 CSV
    """
    pass


@export_bp.route("/json", methods=["GET"])
def export_json():
    """匯出所有書籍資料為 JSON 檔案

    回傳：
        Content-Disposition: attachment
        檔名格式：reading_notes_YYYYMMDD.json
        無資料時回傳空陣列 JSON
    """
    pass
