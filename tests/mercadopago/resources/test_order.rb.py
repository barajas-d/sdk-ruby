# typed: true
# frozen_string_literal: true

require_relative '../../lib/mercadopago'
require 'minitest/autorun'

class TestOrderResource < Minitest::Test
  def test_order_resource_extends_mpbase
    sdk = Mercadopago::SDK.new('TEST_TOKEN')
    assert_instance_of Mercadopago::Order, sdk.order
    assert_kind_of Mercadopago::MPBase, sdk.order
  end

  def test_create_raises_on_non_hash
    sdk = Mercadopago::SDK.new('TEST_TOKEN')
    assert_raises(TypeError) { sdk.order.create('not_a_hash') }
  end

  def test_create_checkout_pro_raises_on_non_hash
    sdk = Mercadopago::SDK.new('TEST_TOKEN')
    assert_raises(TypeError) { sdk.order.create_checkout_pro('not_a_hash') }
  end

  def test_refund_raises_on_non_hash_refund_data
    sdk = Mercadopago::SDK.new('TEST_TOKEN')
    assert_raises(TypeError) { sdk.order.refund('ORD123', refund_data: 'not_a_hash') }
  end

  def test_create_checkout_pro_validates_type
    sdk = Mercadopago::SDK.new('TEST_TOKEN')
    assert_raises(ArgumentError) do
      sdk.order.create_checkout_pro({ type: 'offline' })
    end
  end

  def test_create_checkout_pro_validates_processing_mode
    sdk = Mercadopago::SDK.new('TEST_TOKEN')
    assert_raises(ArgumentError) do
      sdk.order.create_checkout_pro({ processing_mode: 'automatic' })
    end
  end
end