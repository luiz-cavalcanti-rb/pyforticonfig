from flask import Flask, render_template, request, send_from_directory, abort, jsonify
import os

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    generated_files = [file for file in os.listdir(os.path.join(app.root_path, 'static')) if file.endswith('.conf')]
    return render_template('index.html', files=generated_files)


@app.route('/generate', methods=['POST'])
def generate():
    data = {
        'fortigateSN': request.form['fortigateSN'],
        'obra': request.form['obra'],
        'wanIP': request.form['wanIP'],
        'wanMASK': request.form['wanMASK'],
        'wanGW': request.form['wanGW'],
        'vlan1IP': request.form['vlan1IP'],
        'vlan1MASK': request.form['vlan1MASK'],
        'wificorpVID': request.form['wificorpVID'],
        'wificorpIP': request.form['wificorpIP'],
        'wificorpMASK': request.form['wificorpMASK'],
        'wifiguestVID': request.form['wifiguestVID'],
        'wifiguestIP': request.form['wifiguestIP'],
        'wifiguestMASK': request.form['wifiguestMASK'],
        'devicesVID': request.form['devicesVID'],
        'devicesIP': request.form['devicesIP'],
        'devicesMASK': request.form['devicesMASK'],
        'wificeoVID': request.form['wificeoVID'],
        'wificeoIP': request.form['wificeoIP'],
        'wificeoMASK': request.form['wificeoMASK'],
        'looprbIP': request.form['looprbIP'],
        'rbrootPWD': request.form['rbrootPWD'],
        'ap01IP': request.form['ap01IP'],
        'ap01MAC': request.form['ap01MAC'],
        'ap02IP': request.form['ap02IP'],
        'ap02MAC': request.form['ap02MAC'],
        'hostNAME': request.form['fortigateSN']+"-"+request.form['obra'],
        'analyzerIP': request.form['analyzerIP']
    }
    # Generate hostname and configuration
    hostname, filename = generate_config_file(data)
    return render_template('result.html', hostname=hostname, filename=filename, files=get_generated_files())

def generate_config_file(data):
    # Generate hostname
    hostname = f"{data['fortigateSN']}-{data['obra']}"

    # Replace placeholders in template.conf
    with open('template.conf', 'r') as f:
        template = f.read()
    config = template.format(**data)

    # Write configuration to file
    filename = f"{hostname}.conf"
    with open(os.path.join('static', filename), 'w') as f:
        f.write(config)

    return hostname, filename

def get_generated_files():
    return [file for file in os.listdir(os.path.join(app.root_path, 'static')) if file.endswith('.conf')]

def get_file_content(filename):
    try:
        with open(os.path.join('static', filename), 'r') as f:
            return f.read()
    except FileNotFoundError:
        # Handle file not found error
        return None


@app.route('/static/<path:filename>')
def download_config(filename):
    return send_from_directory('static', filename, as_attachment=True)
    
@app.route('/view_raw', methods=['POST'])
def view_raw():
    filename = request.form.get('filename')
    if filename:
        try:
            with open(os.path.join('static', filename), 'r') as f:
                file_content = f.read()
            return "<pre>" + file_content + "</pre>"
        except FileNotFoundError:
            abort(404)
    else:
        abort(400)

@app.route('/save_file', methods=['POST'])
def save_file():
    filename = request.form.get('filename')
    content = request.form.get('content')

    if filename and content:
        try:
            with open(os.path.join('static', filename), 'w') as f:
                f.write(content)
            return jsonify({'success': True, 'message': 'File saved successfully.'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
    else:
        return jsonify({'success': False, 'message': 'Filename or content is missing.'})


@app.route('/edit')
def edit():
    filename = request.args.get('filename')
    content = get_file_content(filename)
    if content is not None:
        return render_template('editor.html', filename=filename, content=content)
    else:
        abort(404)  # Or handle the error appropriately


if __name__ == '__main__':
      app.run(debug=True, host='0.0.0.0')
     #app.run(host='0.0.0.0')