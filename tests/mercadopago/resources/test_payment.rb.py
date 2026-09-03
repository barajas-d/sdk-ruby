# typed: true
# frozen_string_literal: true

require_relative '../lib/mercadopago'
require 'minitest/autorun'

class TestPaymentPost < Minitest::Test
  def test_post_creates_payment
    sdk = Mercadopago::SDK.new(ENV['ACCESS_TOKEN'])
    card_token_object = {
      card_number: '5031433215406351',
      expiration_year: 2030,
      expiration_month: 11,
      security_code: '123',
      cardholder: {
        name: 'APRO'
      }
    }
    result_card_token = sdk.card_token.create(card_token_object)

    payment_object = {
      token: result_card_token[:response]['id'],
      installments: 1,
      transaction_amount: 58.80,
      description: 'Payment via post method',
      payment_method_id: 'master',
      payer: {
        email: 'test_user_123456@testuser.com',
        identification: {
          number: '19119119100',
          type: 'CPF'
        }
      }
    }
    
    result = sdk.payment.post(payment_object)
    assert_equal 201, result[:status]
    assert result[:response]['id']
  end

  def test_post_is_alias_for_create
    sdk = Mercadopago::SDK.new(ENV['ACCESS_TOKEN'])
    card_token_object = {
      card_number: '5031433215406351',
      expiration_year: 2030,
      expiration_month: 11,
      security_code: '123',
      cardholder: {
        name: 'APRO'
      }
    }
    result_card_token = sdk.card_token.create(card_token_object)

    payment_object = {
      token: result_card_token[:response]['id'],
      installments: 1,
      transaction_amount: 75.00,
      description: 'Payment test',
      payment_method_id: 'master',
      payer: {
        email: 'test_user_789@testuser.com',
        identification: {
          number: '19119119100',
          type: 'CPF'
        }
      }
    }
    
    result_create = sdk.payment.create(payment_object)
    result_post = sdk.payment.post(payment_object)
    
    assert_equal 201, result_create[:status]
    assert_equal 201, result_post[:status]
    assert result_create[:response]['id']
    assert result_post[:response]['id']
  end

  def test_post_raises_on_non_hash
    sdk = Mercadopago::SDK.new('TEST_TOKEN')
    assert_raises(TypeError) { sdk.payment.post('not_a_hash') }
  end

  def test_post_with_request_options
    sdk = Mercadopago::SDK.new(ENV['ACCESS_TOKEN'])
    card_token_object = {
      card_number: '5031433215406351',
      expiration_year: 2030,
      expiration_month: 11,
      security_code: '123',
      cardholder: {
        name: 'APRO'
      }
    }
    result_card_token = sdk.card_token.create(card_token_object)

    payment_object = {
      token: result_card_token[:response]['id'],
      installments: 1,
      transaction_amount: 100.00,
      description: 'Payment with custom options',
      payment_method_id: 'master',
      payer: {
        email: 'test_user_456@testuser.com',
        identification: {
          number: '19119119100',
          type: 'CPF'
        }
      }
    }
    
    custom_headers = {
      'X-Idempotency-Key': 'unique-payment-key-123'
    }
    request_options = Mercadopago::RequestOptions.new(custom_headers: custom_headers)
    
    result = sdk.payment.post(payment_object, request_options: request_options)
    assert_equal 201, result[:status]
    assert result[:response]['id']
  end
end