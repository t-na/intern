# coding: utf-8
import subprocess
import time

def switch_ap():
    # Get an available AP list
    result = subprocess.run('/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s', shell = True, stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    # split Wi-Fi list based on a new line
    ap_list = output.split('\n')
    # Prepare an empty dictinary for SSID and RSSI pair
    SSID_RSSI = {}

    # Create the SSID-maxRSSI pair for the dictionary.
    for i in range(1, len(ap_list)):
        ap = ap_list[i]
        if ap == '':
            break
        # find SSID and RSSI, using the location of ':'
        start_RSSIindex = ap_list[i].rfind(':') + 4
        start_SSIDindex = ap_list[i].find(':')
        rssi_element = ap[start_RSSIindex : start_RSSIindex+5]
        ssid_element = ap[: start_SSIDindex-3]

        # Subsutitude SSID-RSSI pair for dictionary, overwriting the RSSI with max one.　
        if rssi_element[1:].strip().isdigit(): #　avoid the error derived from RSSI
            ssid = ssid_element.strip() # exclude the space and obtain SSID
            rssi = int(rssi_element) # obtain RSSI
            if ssid in SSID_RSSI:
                SSID_RSSI[ssid] = max(SSID_RSSI[ssid], rssi)
            else:
                SSID_RSSI[ssid] = rssi
    # Avoid the empty error.
    if SSID_RSSI == []:
        return
    # Sort the SSID-RSSI pair in descending order of RSSI
    sorted_ssid_rssi_pair = sorted(SSID_RSSI.items(), key = lambda x:x[1], reverse = True)

    for ap in sorted_ssid_rssi_pair:
        # list of available AP and its password
        password = {
            "HUMAX-A7F87-A":"dWG5M5N5NjE3L",
            "HUMAX-A7F87":"dWG5M5N5NjE3L",
            "Xperia Z1 f_11c37":"6680e7c7185d"
            }
        if ap[0] in password:
            subprocess.run('networksetup -setairportnetwork en0 max_ap password.get["max_ap"]', shell = True, stdout=subprocess.PIPE)
        # Switch the AP with max AP, password of which is known
            print('Changed AP to "{0}"'.format(ap[0]))
            break
# Switch the AP with max AP evry 5 seconds
time.sleep(5)
while True:
    switch_ap()
