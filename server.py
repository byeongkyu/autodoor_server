#!/usr/bin/env python
# -*- encoding: utf8 -*-

import yaml
import time
from flask import Flask, render_template, request, redirect
from pymodbus.client.sync import ModbusTcpClient as ModbusClient


app = Flask(__name__)
door_data = {}
with open("./config/door_data.yaml", "r") as f:
    data = f.read()
    door_data = yaml.load(data)

@app.route('/')
def index():
    return render_template('index.html', door_data=door_data)

@app.route('/control_by_button', methods=['POST'])
def control_door_by_button():
    if 'open' in request.form:
        target_door = request.form['open']
        for i in door_data:
            if i['door'] == target_door:
                client = ModbusClient(i['address'], port=502)
                client.connect()

                client.write_coil(16 + i['channel'], True)
                time.sleep(0.5)
                client.write_coil(16 + i['channel'], False)
                time.sleep(0.5)

    elif 'close' in request.form:
        target_door = request.form['close']

    return redirect('/')

@app.route('/control', methods=['POST', 'PUT', 'GET'])
def control_door():
    if 'name' in request.args:
        target_door = request.args['name']
        if 'ctrl' in request.args:
            if 'open' in request.args['ctrl']:
                for i in door_data:
                    if i['door'] == target_door:
                        client = ModbusClient(i['address'], port=502)
                        client.connect()

                        client.write_coil(16 + i['channel'], True)
                        time.sleep(0.5)
                        client.write_coil(16 + i['channel'], False)
                        time.sleep(0.5)
            else:
                pass
        else:
            pass

    return ''

if __name__ == "__main__":
    app.run('0.0.0.0', port=5050)