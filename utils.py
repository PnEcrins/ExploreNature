def format_columns(data, html_cols=["lb_nom"]):
    if data and len(data) > 0:
        first_row = data[0]
        cols = []
        for col in first_row.keys():

            col_def = {"id": col, "name": col}
            if col in html_cols:
                col_def["presentation"] = "markdown"
            cols.append(col_def)
        return cols
    return None


pointToLayer = """
    function (feature, latlng) {
        return L.circleMarker(latlng);
    }
"""
