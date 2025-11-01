# Stripe Payment Integration

## Setup Instructions

1. Install the Stripe Python library:
```bash
pip3 install stripe
```

2. Get your Stripe API keys from https://dashboard.stripe.com/test/apikeys

3. Set your Stripe keys in the code:

### Frontend (js/script.js line 69):
```javascript
this.stripe = Stripe('pk_test_YOUR_PUBLISHABLE_KEY_HERE');
```

### Backend (scripts/game_api.py line 21):
```python
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_YOUR_SECRET_KEY_HERE')
```

Or set as environment variable:
```bash
export STRIPE_SECRET_KEY=sk_test_YOUR_SECRET_KEY_HERE
```

## Features Added

✅ Stripe Checkout integration
✅ Payment processing endpoints  
✅ Purchase tracking in database
✅ Secure transaction handling
✅ Shop items now require real payment

## Files Modified

- index.html - Added Stripe.js script tag
- js/script.js - Added Stripe initialization and checkout flow
- scripts/game_api.py - Added payment endpoints and database table


