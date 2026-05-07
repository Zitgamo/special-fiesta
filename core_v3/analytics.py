import MetaTrader5 as mt5
import pandas as pd

class IronAnalytics:
    @staticmethod
    def get_bias(df):
        """
        Oracle Pattern Recognition Brain (SI v5.0).
        Works on any OHLCV dataframe (MT5, Binance, or VN30).
        Returns: bias (BULLISH/BEARISH/NEUTRAL), er (Efficiency), velocity
        """
        import talib
        try:
            close = df['c'].values
            ema_f = talib.EMA(close, timeperiod=20)
            ema_s = talib.EMA(close, timeperiod=50)
            
            last_f = ema_f[-1]
            last_s = ema_s[-1]
            last_price = close[-1]
            
            # Efficiency Ratio calculation
            net_change = abs(close[-1] - close[-20])
            sum_changes = sum([abs(close[i] - close[i-1]) for i in range(len(close)-19, len(close))])
            er = net_change / sum_changes if sum_changes > 0 else 0
            
            bias = "NEUTRAL"
            if last_price > last_f > last_s: bias = "BULLISH"
            elif last_price < last_f < last_s: bias = "BEARISH"
            
            return bias, er, 1.0 # Velocity placeholder
        except:
            return "NEUTRAL", 0.0, 1.0

    @staticmethod
    def get_atr(symbol, bridges, period=14):
        """
        Calculates the ATR for both MT5 and Binance symbols.
        """
        if "USDT" in symbol:
            try:
                ohlcv = bridges.binance.fetch_ohlcv(symbol, timeframe='1h', limit=period+1)
                if not ohlcv or len(ohlcv) < period: return None
                
                true_ranges = []
                for i in range(1, len(ohlcv)):
                    high, low, close = ohlcv[i][2], ohlcv[i][3], ohlcv[i][4]
                    prev_close = ohlcv[i-1][4]
                    tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
                    true_ranges.append(tr)
                return sum(true_ranges) / len(true_ranges)
            except:
                return None
        else:
            # MT5 ATR with Timeframe Fallback
            for tf in [mt5.TIMEFRAME_H1, mt5.TIMEFRAME_M15, mt5.TIMEFRAME_M5]:
                rates = mt5.copy_rates_from_pos(symbol, tf, 0, period + 1)
                if rates is not None and len(rates) >= period:
                    true_ranges = []
                    for i in range(1, len(rates)):
                        high, low, prev_close = rates[i]['high'], rates[i]['low'], rates[i-1]['close']
                        tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
                        true_ranges.append(tr)
                    
                    atr = sum(true_ranges) / len(true_ranges)
                    if atr > 0: return atr
            
            # Final Fallback: Use 0.1% of Price
            info = mt5.symbol_info(symbol)
            return (info.ask * 0.001) if info else None

    @staticmethod
    def get_macro_sentiment():
        dxy = mt5.symbol_info_tick("USDX")
        if not dxy: dxy = mt5.symbol_info_tick("DX")
        if not dxy: return "NEUTRAL"
        dxy_er = IronAnalytics.get_efficiency_ratio(dxy.symbol)
        if dxy_er > 0.6: return "RISK_OFF"
        return "RISK_ON"

    @staticmethod
    def get_efficiency_ratio(symbol, bridges=None, period=14):
        er_values = []
        
        # 1. TIMEFRAMES TO AUDIT
        timeframes = ['1h', '15m'] if "USDT" in symbol else [mt5.TIMEFRAME_H1, mt5.TIMEFRAME_M15]
        
        for tf in timeframes:
            try:
                if "USDT" in symbol and bridges:
                    ohlcv = bridges.binance.fetch_ohlcv(symbol, timeframe=tf, limit=period+1)
                    if not ohlcv or len(ohlcv) < period: continue
                    close_prices = [x[4] for x in ohlcv]
                else:
                    rates = mt5.copy_rates_from_pos(symbol, tf, 0, period + 1)
                    if rates is None or len(rates) < period: continue
                    close_prices = [x['close'] for x in rates]
                
                net_change = abs(close_prices[-1] - close_prices[0])
                sum_changes = sum([abs(close_prices[i] - close_prices[i-1]) for i in range(1, len(close_prices))])
                
                if sum_changes > 0:
                    er_values.append(net_change / sum_changes)
            except:
                continue
        
        if not er_values: return 0.5 # Default to neutral
        return round(sum(er_values) / len(er_values), 2)

    @staticmethod
    def get_correlation(symbol1, symbol2, period=30):
        rates1 = mt5.copy_rates_from_pos(symbol1, mt5.TIMEFRAME_H1, 0, period)
        rates2 = mt5.copy_rates_from_pos(symbol2, mt5.TIMEFRAME_H1, 0, period)
        if rates1 is None or rates2 is None or len(rates1) < period or len(rates2) < period:
            return 0.0
        df1 = pd.DataFrame(rates1)
        df2 = pd.DataFrame(rates2)
        corr = df1['close'].corr(df2['close'])
        return round(corr, 2)

    @staticmethod
    def get_velocity(symbol, bridges=None, period=5):
        if "USDT" in symbol and bridges:
            try:
                ohlcv = bridges.binance.fetch_ohlcv(symbol, timeframe='15m', limit=period+1)
                if not ohlcv or len(ohlcv) < period: return 1.0
                close_prices = [x[4] for x in ohlcv]
                roc = (close_prices[-1] - close_prices[0]) / close_prices[0]
                tr = [abs(x[2] - x[3]) for x in ohlcv] # high - low
                avg_tr = sum(tr) / len(tr)
                if avg_tr == 0: return 1.0
                velocity = abs(roc * 100) / (avg_tr / close_prices[0] * 100)
                return round(velocity, 2)
            except: return 1.0
            
        rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, period + 1)
        if rates is None or len(rates) < period: return 1.0
        roc = (rates[-1]['close'] - rates[0]['close']) / rates[0]['close']
        tr = [abs(rates[i]['high'] - rates[i]['low']) for i in range(len(rates))]
        avg_tr = sum(tr) / len(tr)
        if avg_tr == 0: return 1.0
        velocity = abs(roc * 100) / (avg_tr / rates[0]['close'] * 100)
        return round(velocity, 2)
