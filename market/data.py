
import ccxt


class MarketData:
    def __init__(self):
        self.exchange = ccxt.binance({
            "enableRateLimit": True,
            "timeout": 10000
        })

    def get_ticker(self, symbol="BTC/USDT"):
        try:
            ticker = self.exchange.fetch_ticker(symbol)

            price = ticker.get("last")

            if price is None:
                return {"error": "Exchange returned no price data."}

            return {
                "symbol": symbol,
                "price": price,
                "change": ticker.get("percentage"),
                "high": ticker.get("high"),
                "low": ticker.get("low"),
                "volume": ticker.get("baseVolume")
            }

        except ccxt.BadSymbol:
            return {"error": f"Invalid trading pair: {symbol}"}

        except ccxt.NetworkError as error:
            return {"error": f"Network error: {error}"}

        except ccxt.ExchangeError as error:
            return {"error": f"Exchange error: {error}"}

        except Exception as error:
            return {"error": f"Unexpected error: {error}"}


market = MarketData()


def get_ticker(symbol="BTC/USDT"):
    return market.get_ticker(symbol)

