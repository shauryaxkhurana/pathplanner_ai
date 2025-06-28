import pdfkit

def save_roadmap_as_pdf(roadmap, filename="study_plan.pdf"):
    html = "<h1>PathPlanner.AI – Your Study Roadmap</h1>"
    for week, topics in roadmap.items():
        html += f"<h2>{week}</h2><ul>"
        for t in topics:
            html += f"<li>{t}</li>"
        html += "</ul>"
    pdfkit.from_string(html, filename)
