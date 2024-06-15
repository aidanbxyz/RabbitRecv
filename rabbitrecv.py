import PySimpleGUI as sg
import serial
import serial.tools.list_ports
from scipy import spatial
from datetime import datetime
from geographiclib.geodesic import Geodesic
import cities

tree = spatial.KDTree(cities.coords)

def getDir(closecity, currentloc):
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    tmpd = Geodesic.WGS84.Inverse(closecity[0], closecity[1], currentloc[0], currentloc[1])
    return str(round(tmpd['s12']*0.006213712)/10)+'mi '+dirs[int((tmpd['azi1']+11.25)/22.5)%16]+' of '+cities.cities[closecity[0],closecity[1]]

ports = []
for port in serial.tools.list_ports.comports():
    ports.append(port.name)

tabledata = [[      'T (C)', 'NoData', 'NoData', 'NoData'],
             [     'RH (%)', 'NoData', 'NoData', 'NoData'],
             [     'P (Pa)', 'NoData', 'NoData', 'NoData'],
             ['Speed (m/s)', 'NoData', 'NoData', 'NoData'],
             [  'Dir (deg)', 'NoData', 'NoData', 'NoData']]

sg.theme('Dark Grey 3')
layout = [[sg.Combo(ports, key='comport', size=(8,1)), sg.Button('REFRESH', key='refcom'), sg.Button('START', key='startstop')],
          [sg.Text('da:db:dc', key='time'), sg.Text('City, State', key='loc')],
          [sg.Table(tabledata, key='datatable', headings=['Field', 'Now', 'Min', 'Max'], hide_vertical_scroll=True, size=(None,5))],
          [sg.Text('Status:')],
          [sg.Text('', key='status')],
          [sg.Button('About', key='about'), sg.Button('Plotter', key='plotter'), sg.Checkbox('Require GPS to log', default=True, key='gpswait')]]

icon = b'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'

window = sg.Window('RabbitRecv', layout, icon=icon)

sensor = None
logfile = None
packetnum = 0
data = [ 'f', 'da', 'db', 'dc', 'ga', 'go', 't', 'h', 'p', 'ws', 'wd' ]

while True:
    sensorline = ''
    event, values = window.read(timeout=1)
    if event == sg.WIN_CLOSED:
        break
    elif event == 'about':
        sg.popup_no_buttons('SSWA RabbitRecv\nv1.0\n\nMade for the AMMETS project\nsswa.tv/projects/ammets\nby @aidanbxyz\n\nSupported Receivers:\nDusty I\n\nCities data:\nsimplemaps.com/data/us-cities\n\nMade with:\nPySimpleGUI, pyserial, and scipy', title='RabbitRecv About', icon=icon)
    elif event == 'refcom':
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append(port.name)
        window['comport'].update(ports)
    elif event == 'plotter':
        fig, ax = plt.subplots()
        
    elif event == 'startstop':
        if window['startstop'].get_text() == 'START':
            window['startstop'].update('STOP')
            try:
                sensor = serial.Serial(values['comport'], '115200', timeout=0.1)
                tabledata = [[      'T (C)', 'NoData', 'NoData', 'NoData'],
                             [     'RH (%)', 'NoData', 'NoData', 'NoData'],
                             [     'P (Pa)', 'NoData', 'NoData', 'NoData'],
                             ['Speed (m/s)', 'NoData', 'NoData', 'NoData'],
                             [  'Dir (deg)', 'NoData', 'NoData', 'NoData']]
                window['datatable'].update(tabledata)
                tabledata = [[      'T (C)', 0, 999999, -999999],
                             [     'RH (%)', 0, 999999, -999999],
                             [     'P (Pa)', 0, 999999, -999999],
                             ['Speed (m/s)', 0, 999999, -999999],
                             [  'Dir (deg)', 0, 999999, -999999]]
                lat = 0
                lon = 0
                window['status'].update('Running')
            except:
                window['status'].update('Error opening serial port')
        else:
            window['startstop'].update('START')
            try:
                sensor.close()
                sensor = None
                logfile.close()
                logfile = None
            except:
                window['status'].update('Sensor or log file not open')
        packetnum = 0
    if sensor is not None:
        sensorline = sensor.readline()[:-2].decode('utf-8')
        if sensorline != '':
            if 'f' in sensorline:
                data[0] = sensorline[1:]
            elif 'da' in sensorline:
                data[1] = sensorline[2:]
            elif 'db' in sensorline:
                data[2] = sensorline[2:]
            elif 'dc' in sensorline:
                data[3] = sensorline[2:]
            elif 'ga' in sensorline:
                data[4] = sensorline[2:]
            elif 'go' in sensorline:
                data[5] = sensorline[2:]
            elif 't' in sensorline:
                data[6] = sensorline[1:]
            elif 'h' in sensorline:
                data[7] = sensorline[1:]
            elif 'p' in sensorline:
                data[8] = sensorline[1:]
            elif 'ws' in sensorline:
                data[9] = sensorline[2:]
            elif 'wd' in sensorline:
                data[10] = sensorline[2:]
        else:
            if data != [ 'f', 'da', 'db', 'dc', 'ga', 'go', 't', 'h', 'p', 'ws', 'wd' ]:
                if data[1] != 'da' and data[2] != 'db' and data[3] != 'dc':
                    window['time'].update(('0'+data[1] if int(data[1]) < 10 else data[1])+':'+('0'+data[2] if int(data[2]) < 10 else data[2])+':'+('0'+data[3] if int(data[3]) < 10 else data[3])+'Z')
                if data[4] != 'ga' and data[5] != 'go':
                    try:
                        lat = float(data[4][0:2])
                        lat += float(data[4][2:])/60
                        lon = float(data[5][0:2])*-1
                        lon -= float(data[5][2:])/60
                        window['status'].update('Running')
                    except:
                        window['status'].update('Error converting GPS Coords')
                        lat = 0
                        lon = 0
                    window['loc'].update(cities.cities[cities.coords[tree.query([(lat,lon)])[1][0]]])
                if packetnum > 3:
                    try:
                        tmp = float(data[6])
                        if tabledata[0][2] > tmp:
                            tabledata[0][2] = tmp
                        if tabledata[0][3] < tmp:
                            tabledata[0][3] = tmp
                    except:
                        pass
                    try:
                        tmp = float(data[7])
                        if tabledata[1][2] > tmp:
                            tabledata[1][2] = tmp
                        if tabledata[1][3] < tmp:
                            tabledata[1][3] = tmp
                    except:
                        pass
                    try:
                        tmp = int(data[8][:-3])
                        if tabledata[2][2] > tmp:
                            tabledata[2][2] = tmp
                        if tabledata[2][3] < tmp:
                            tabledata[2][3] = tmp
                    except:
                        pass
                    try:
                        tmp = float(data[9])
                        if tabledata[3][2] > tmp:
                            tabledata[3][2] = tmp
                        if tabledata[3][3] < tmp:
                            tabledata[3][3] = tmp
                    except:
                        pass
                    try:
                        tmp = float(data[10])
                        if tabledata[4][2] > tmp:
                            tabledata[4][2] = tmp
                        if tabledata[4][3] < tmp:
                            tabledata[4][3] = tmp
                    except:
                        pass
                    tabledata[0][1] = data[6]
                    tabledata[1][1] = data[7]
                    tabledata[2][1] = data[8][:-3]
                    tabledata[3][1] = data[9]
                    tabledata[4][1] = data[10]
                    window['datatable'].update(tabledata)
                else:
                    packetnum += 1
                    window['status'].update('Waiting for five frames..')
                if values['gpswait']:
                    if lat != 0 and lon != 0 and data[1] != 'da' and data[2] != 'db' and data[3] != 'dc' and logfile == None:
                        logfile = open((cities.cities[cities.coords[tree.query([(lat,lon)])[1][0]]]+' '+('0'+data[1] if int(data[1]) < 10 else data[1])+('0'+data[2] if int(data[2]) < 10 else data[2])+('0'+data[3] if int(data[3]) < 10 else data[3])+'Z.log'), 'a')
                        logfile.write('# Start '+datetime.now().strftime('%b %d %Y')+' '+('0'+data[1] if int(data[1]) < 10 else data[1])+':'+('0'+data[2] if int(data[2]) < 10 else data[2])+':'+('0'+data[3] if int(data[3]) < 10 else data[3])+' UTC '+getDir(cities.coords[tree.query([(lat,lon)])[1][0]],(lat,lon))+'\n# Rabbit X,X\n# https://sswa.tv/wxlogs\n')
                else:
                    logfile = open('Unknown, NA 000000Z.log', 'a')
                if logfile != None:
                    logfile.write('['+','.join(data)+']\n')
            data = [ 'f', 'da', 'db', 'dc', 'ga', 'go', 't', 'h', 'p', 'ws', 'wd' ]
