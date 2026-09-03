# typed: true
# frozen_string_literal: true

require_relative '../lib/mercadopago'

require 'minitest/autorun'

class TestOrderSimulateEvents < Minitest::Test
  class CaptureHttpClient < Mercadopago::HttpClient
    attr_reader :last_post

    def post(url:, data:, headers:, timeout: nil)
      @last_post = {
        url: url,
        data: data,
        headers: headers,
        timeout: timeout
      }

      {
        status: 200,
        response: {
          'id' => 'ORD123',
          'status' => 'processed',
          'events' => [
            {
              'type' => 'payment_completed',
              'timestamp' => '2024-01-15T10:30:00Z'
            }
          ]
        }
      }
    end
  end

  def test_simulate_events_success
    http_client = CaptureHttpClient.new
    sdk = Mercadopago::SDK.new('ACCESS_TOKEN', http_client: http_client)
    
    request_body = {
      event: 'payment_completed'
    }
    
    result = sdk.order.simulate_events('ORD123', request_body)
    
    assert_equal 200, result[:status]
    assert_equal 'https://api.mercadopago.com/v1/orders/ORD123/events', http_client.last_post[:url]
    assert_equal '{"event":"payment_completed"}', http_client.last_post[:data]
    assert_equal 'processed', result[:response]['status']
  end

  def test_simulate_events_with_request_options
    http_client = CaptureHttpClient.new
    sdk = Mercadopago::SDK.new('ACCESS_TOKEN', http_client: http_client)
    request_options = Mercadopago::RequestOptions.new(
      custom_headers: { 'X-Idempotency-Key': 'simulate-events-key' }
    )
    
    request_body = {
      event: 'order_cancelled'
    }
    
    result = sdk.order.simulate_events('ORD456', request_body, request_options: request_options)
    
    assert_equal 200, result[:status]
    assert_equal 'https://api.mercadopago.com/v1/orders/ORD456/events', http_client.last_post[:url]
    assert_equal 'simulate-events-key', http_client.last_post[:headers]['X-Idempotency-Key']
    refute http_client.last_post[:headers].key?('x-idempotency-key')
  end

  def test_simulate_events_requires_hash
    sdk = Mercadopago::SDK.new('ACCESS_TOKEN')
    
    assert_raises(TypeError) do
      sdk.order.simulate_events('ORD123', 'not_a_hash')
    end
  end

  def test_simulate_events_with_complex_payload
    http_client = CaptureHttpClient.new
    sdk = Mercadopago::SDK.new('ACCESS_TOKEN', http_client: http_client)
    
    request_body = {
      event: 'payment_completed',
      metadata: {
        source: 'test',
        timestamp: '2024-01-15T10:30:00Z'
      },
      transaction_id: 'TXN789'
    }
    
    result = sdk.order.simulate_events('ORD123', request_body)
    payload = JSON.parse(http_client.last_post[:data])
    
    assert_equal 200, result[:status]
    assert_equal 'payment_completed', payload['event']
    assert_equal 'test', payload['metadata']['source']
    assert_equal 'TXN789', payload['transaction_id']
  end
end