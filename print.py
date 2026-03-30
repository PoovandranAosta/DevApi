from flask import Flask, request, jsonify
import cups

app = Flask(__name__)

conn = cups.Connection()
default_printer = conn.getDefault()

@app.route('/print', methods=['POST'])
def print_zpl():
    data = request.json
    zpl = data.get('zpl')

    if not zpl:
        return jsonify({"error": "ZPL code required"}), 400

    if not default_printer:
        return jsonify({"error": "No default printer found"}), 500

    try:
        # Write ZPL to a temporary file
        with open("/tmp/label.zpl", "w") as f:
            f.write(zpl)
        # Send file to printer
        conn.printFile(default_printer, "/tmp/label.zpl", "ZPL Label", {"raw": "true"})
        return jsonify({"status": "Print sent!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)