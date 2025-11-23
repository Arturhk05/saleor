import pytest

from ..fetch import CheckoutLineInfo, CheckoutInfo

def test_checkout_line_info_repr_is_reduced(checkout_with_item):
    checkout_line = checkout_with_item.lines.first()
    channel = checkout_with_item.channel
    variant = checkout_line.variant
    variant_channel_listing = variant.channel_listings.get(channel_id=channel.id)
    product = variant.product
    product_type = product.product_type
    discounts = list(checkout_line.discounts.all())

    checkout_line_info = CheckoutLineInfo(
        line=checkout_line,
        variant=variant,
        channel_listing=variant_channel_listing,
        product=product,
        product_type=product_type,
        collections=[],
        tax_class=product.tax_class or product_type.tax_class,
        discounts=discounts,
        rules_info=[],
        channel=channel,
        voucher=None,
        voucher_code=None,
    )

    repr_str = repr(checkout_line_info)

    assert "CheckoutLineInfo" in repr_str
    assert str(checkout_line.pk) in repr_str
    assert str(variant.pk) in repr_str
    assert str(product.pk) in repr_str
    assert str(checkout_line.quantity) in repr_str
    
    assert "<" not in repr_str or ">" not in repr_str
    
    assert len(repr_str) < 200, "repr should be concise and reduced"
