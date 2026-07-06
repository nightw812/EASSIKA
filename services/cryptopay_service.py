from decimal import Decimal

from aiocryptopay import AioCryptoPay, Networks
from aiocryptopay.models.invoice import Invoice

import config

_network = Networks.TEST_NET if config.CRYPTOBOT_TESTNET else Networks.MAIN_NET


def _client() -> AioCryptoPay:
    return AioCryptoPay(token=config.CRYPTOBOT_TOKEN, network=_network)


def apply_cryptobot_fee(amount_rub: Decimal) -> Decimal:
    """Накидывает комиссию CryptoBot (config.CRYPTOBOT_FEE_PERCENT %) на сумму счёта."""
    fee_multiplier = Decimal("1") + Decimal(str(config.CRYPTOBOT_FEE_PERCENT)) / Decimal("100")
    return (amount_rub * fee_multiplier).quantize(Decimal("1"))


async def create_invoice(amount_rub: Decimal, description: str, payload: str) -> Invoice:
    """Создаёт инвойс в рублях (курс на USDT считает сам CryptoBot). Комиссия уже должна быть включена в amount_rub."""
    async with _client() as client:
        invoice = await client.create_invoice(
            amount=float(amount_rub),
            currency_type="fiat",
            fiat="RUB",
            accepted_assets="USDT",
            description=description,
            payload=payload,
            expires_in=config.INVOICE_EXPIRES_MINUTES * 60,
        )
        return invoice


async def get_invoice_status(invoice_id: int) -> str:
    """Возвращает статус инвойса: active | paid | expired."""
    async with _client() as client:
        invoices = await client.get_invoices(invoice_ids=invoice_id)
        if not invoices:
            return "expired"
        invoice = invoices[0] if isinstance(invoices, list) else invoices
        return invoice.status
