"""Inspect supplied packaged workbook definitions without running Tableau or Hyper."""
from pathlib import Path
import hashlib
import json
import zipfile
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
results = []
for path in sorted((root / "Workbooks").glob("*.twbx")):
    with zipfile.ZipFile(path) as package:
        if package.testzip() is not None:
            raise ValueError(f"Corrupt package: {path.name}")
        names = package.namelist()
        definitions = [name for name in names if name.endswith(".twb")]
        if len(definitions) != 1:
            raise ValueError("Expected one workbook definition")
        document = ET.fromstring(package.read(definitions[0]))
        calculations = []
        for datasource in document.findall("./datasources/datasource"):
            for column in datasource.findall("column"):
                calculation = column.find("calculation")
                if calculation is not None and calculation.get("formula"):
                    calculations.append({"field": column.get("caption") or column.get("name"),
                                         "formula": calculation.get("formula")})
        actions = [action.get("caption") for action in document.findall("./actions/action")]
        results.append({
            "file": str(path.relative_to(root)),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "tableau_version": document.get("source-build"),
            "dashboards": [{"name": d.get("name"), "type": d.get("type", "dashboard")}
                           for d in document.findall("./dashboards/dashboard")],
            "worksheets": [s.get("name") for s in document.findall("./worksheets/worksheet")],
            "actions": actions,
            "calculated_fields": calculations,
            "embedded_extracts": [n for n in names if n.endswith(".hyper")],
            "validation": "ZIP CRC and XML parsing passed. No Tableau rendering, action clicks, or Hyper queries performed."
        })
output = root / "Reports/workbook_definition_review.json"
output.write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps([{ "file": r["file"], "worksheets": len(r["worksheets"]), "actions": len(r["actions"])} for r in results], indent=2))
