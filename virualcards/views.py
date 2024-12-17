import stripe
from django.conf import settings
from rest_framework.views import APIView
from utils.ResponseGenerator import ResponseGenerator
from utils.helpers import createVirtualCard
stripe.api_key = settings.STRIPE_SECRET_KEY




class CreateVirtualCard(APIView):
    def post(self, request):
        user = request.user
        create_card = createVirtualCard(user, 1000)
        card_id = create_card.get("card_id")
        card_holder_id = create_card.get("card_holder_id")
        card  = stripe.issuing.Card.retrieve(card_id)
        print(card)
        # cardholder = stripe.issuing.Cardholder.create(
        # name="Jenny Rosen",
        # email="jenny.rosen@example.com",
        # phone_number="+18008675309",
        # status="active",
        # type="individual",
        # individual={
        #     "first_name": "Jenny",
        #     "last_name": "Rosen",
        #     "dob": {"day": 1, "month": 11, "year": 1981},
        # },
        # billing={
        #     "address": {
        #     "line1": "123 Main Street",
        #     "city": "San Francisco",
        #     "state": "CA",
        #     "postal_code": "94111",
        #     "country": "GB",
        #     },
        # },
        # )
        
        
        # card = stripe.issuing.Card.create(
        #     cardholder=cardholder.id,
        #     currency="gbp",
        #     type="virtual",
        #     # authorization_controls={
        #     #      "blocked_categories": ["veterinary_services"],
        #     # },
        #     spending_controls={
        #         "allowed_categories":["general_services"],
        #         # "blocked_categories": ["veterinary_services"],
        #          "spending_limits": [{
        #              "amount":1000,
        #              "categories":["general_services"],
        #              "interval":"monthly",
        #              }],
        #     },
            
            
          
        # )
        
        
        # stripe.issuing.Card.modify(
        # card.id,
        # status="active",
        # )
        
        
        return ResponseGenerator.response(
            data={"card": card_id, "card_holder_id":card_holder_id},message="Card Created successfully", status=200
            )
        