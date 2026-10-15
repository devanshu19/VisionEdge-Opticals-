import urllib.request, json, os

base = 'http://127.0.0.1:5000/api'
with open('temp_rx.png', 'wb') as f:
    f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\rIDATx\x9cc`\x00\x00\x00\x02\x00\x01H\xafA4\x00\x00\x00\x00IEND\xaeB`\x82')

boundary = '====Boundary===='
header = f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="test.png"\r\nContent-Type: image/png\r\n\r\n'.encode('utf-8')
footer = f'\r\n--{boundary}--\r\n'.encode('utf-8')
body = header + open('temp_rx.png', 'rb').read() + footer

req = urllib.request.Request(base + '/ai/extract', data=body, headers={'Content-Type': f'multipart/form-data; boundary={boundary}'})

try:
    res = urllib.request.urlopen(req)
    result = json.loads(res.read())
    print('OCR Extract API Response:')
    print(json.dumps(result, indent=2))
finally:
    if os.path.exists('temp_rx.png'): os.remove('temp_rx.png')
