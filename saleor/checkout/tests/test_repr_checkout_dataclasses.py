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

def test_checkout_info_repr_is_reduced(checkout_with_item, customer_user, all_plugins_manager):
    checkout = checkout_with_item
    checkout.user = customer_user
    checkout.save()
    
    lines = checkout.lines.all()
    channel = checkout.channel
    
    lines_info = [
        CheckoutLineInfo(
            line=line,
            variant=line.variant,
            channel_listing=line.variant.channel_listings.get(channel_id=channel.id),
            product=line.variant.product,
            product_type=line.variant.product.product_type,
            collections=[],
            tax_class=line.variant.product.tax_class or line.variant.product.product_type.tax_class,
            discounts=list(line.discounts.all()),
            rules_info=[],
            channel=channel,
            voucher=None,
            voucher_code=None,
        )
        for line in lines
    ]
    
    checkout_info = CheckoutInfo(
        checkout=checkout,
        user=checkout.user,
        channel=channel,
        billing_address=checkout.billing_address,
        shipping_address=checkout.shipping_address,
        tax_configuration=channel.tax_configuration,
        discounts=list(checkout.discounts.all()),
        lines=lines_info,
        manager=all_plugins_manager,
        shipping_channel_listings=list(channel.shipping_method_listings.all()),
        shipping_method=checkout.shipping_method,
        collection_point=checkout.collection_point,
        voucher=None,
        voucher_code=None,
    )

    repr_str = repr(checkout_info)

    assert "CheckoutInfo" in repr_str
    assert str(checkout.pk) in repr_str
    assert str(checkout.user.pk) in repr_str
    assert channel.slug in repr_str
    assert str(len(lines_info)) in repr_str
    assert "<" not in repr_str or ">" not in repr_str

    assert len(repr_str) < 300, "repr should be concise and reduced"
