from rich.text import Text


def render_candles(ohlcv, height=16):
    if not ohlcv:
        return Text("No candle data available.", style="red")

    candles = ohlcv
    highs = [c[2] for c in candles]
    lows = [c[3] for c in candles]

    highest = max(highs)
    lowest = min(lows)

    if highest == lowest:
        highest += 0.5
        lowest -= 0.5

    width = len(candles) * 3

    chart = [
        [" " for _ in range(width)]
        for _ in range(height)
    ]

    colors = [
        [None for _ in range(width)]
        for _ in range(height)
    ]

    for index, candle in enumerate(candles):
        timestamp, open_price, high, low, close, volume = candle

        x = index * 3 + 1

        bullish = close >= open_price
        color = "green" if bullish else "red"

        def price_to_y(price):
            return round(
                (highest - price) /
                (highest - lowest) * (height - 1)
            )

        high_y = price_to_y(high)
        low_y = price_to_y(low)

        open_y = price_to_y(open_price)
        close_y = price_to_y(close)

        # Draw the wick
        for y in range(high_y, low_y + 1):
            chart[y][x] = "|"
            colors[y][x] = color

        # Draw the candle body
        body_top = min(open_y, close_y)
        body_bottom = max(open_y, close_y)

        for y in range(body_top, body_bottom + 1):
            chart[y][x] = "#"
            colors[y][x] = color

    output = Text()

    for row in range(height):
        price = highest - (
            row / (height - 1)
        ) * (highest - lowest)

        output.append(f"{price:>12,.2f} ", style="dim")

        for column in range(width):
            char = chart[row][column]
            color = colors[row][column]

            if color:
                output.append(char, style=color)
            else:
                output.append(char)

        output.append("\n")

    output.append(
        " " * 12 + "TIME →",
        style="dim"
    )

    return output
