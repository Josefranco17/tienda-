import os
wallet = r'C:\Users\josej\Downloads\formativa proga\prueba\Nueva carpeta 3\Wallet_tienda'
os.environ['TNS_ADMIN'] = wallet
import oracledb
print('WALLET_EXISTS', os.path.isdir(wallet))
for dsn in ['tienda_tp','tienda_high','tienda_medium','tienda_low']:
    try:
        print('TRY', dsn)
        con = oracledb.connect(user='tienda', password='Inacap.2026$', dsn=dsn)
        print('OK', dsn, con.version)
        con.close()
    except Exception as e:
        print('FAIL', dsn, type(e).__name__, e)
