from flask import Flask, request, jsonify
import win32print
import win32api

app = Flask(__name__)

@app.route('/print', methods=['POST'])
def print_zpl():
    data = request.json
    zpl = data.get('zpl')

    if not zpl:
        return jsonify({"error": "ZPL code required"}), 400

    # Get default printer
    printer_name = win32print.GetDefaultPrinter()
    if not printer_name:
        return jsonify({"error": "No default printer found"}), 500

    try:
        # Send ZPL as raw data
        hPrinter = win32print.OpenPrinter(printer_name)
        try:
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("ZPL Label", None, "RAW"))
            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, zpl.encode('utf-8'))
            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)
        finally:
            win32print.ClosePrinter(hPrinter)

        return jsonify({"status": "Print sent!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)