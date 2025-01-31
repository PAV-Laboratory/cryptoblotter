from decimal import Decimal

from cryptofeed.defines import TRADES
from cryptofeed.exchanges import Upbit
from cryptofeed.standards import timestamp_normalize


class UpbitBlotter(Upbit):
    async def _trade(self, msg: dict, timestamp: float):
        """
        Doc : https://docs.upbit.com/v1.0.7/reference#시세-체결-조회
        {
            'ty': 'trade'             // Event type
            'cd': 'KRW-BTC',          // Symbol
            'tp': 6759000.0,          // Trade Price
            'tv': 0.03243003,         // Trade volume(amount)
            'tms': 1584257228806,     // Timestamp
            'ttms': 1584257228000,    // Trade Timestamp
            'ab': 'BID',              // 'BID' or 'ASK'
            'cp': 64000.0,            // Change of price
            'pcp': 6823000.0,         // Previous closing price
            'sid': 1584257228000000,  // Sequential ID
            'st': 'SNAPSHOT',         // 'SNAPSHOT' or 'REALTIME'
            'td': '2020-03-15',       // Trade date utc
            'ttm': '07:27:08',        // Trade time utc
            'c': 'FALL',              // Change - 'FALL' / 'RISE' / 'EVEN'
        }
        """

        price = Decimal(msg["tp"])
        notional = Decimal(msg["tv"])
        volume = price * notional
        await self.callback(
            TRADES,
            feed=self.id,
            uid=msg["sid"],
            symbol=msg["cd"],  # Do not normalize
            timestamp=timestamp_normalize(self.id, msg["ttms"]),
            price=price,
            volume=volume,
            notional=notional,
            tickRule=1 if msg["ab"] == "BID" else -1,
        )
