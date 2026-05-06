import MetaTrader5 as mt5
import os

print("--- MT5 DIAGNOSTIC ---")
print(f"Current User: {os.getlogin()}")

path = r"C:\Program Files\MetaTrader 5 EXNESS\terminal64.exe"
print(f"Checking path: {path}")
print(f"Path exists: {os.path.exists(path)}")

print("Attempting silent initialize...")
res = mt5.initialize()
print(f"Silent Init Result: {res}")

if not res:
    print(f"MT5 Last Error: {mt5.last_error()}")
    print("Attempting path initialize...")
    res = mt5.initialize(path=path)
    print(f"Path Init Result: {res}")
    if not res:
        print(f"MT5 Last Error: {mt5.last_error()}")

if res:
    print("SUCCESS! Terminal Info:")
    print(mt5.terminal_info()._asdict())
    mt5.shutdown()
else:
    print("FAILURE! Could not connect to MT5.")
