from fastapi import Request
from functions.functions_jwt import validate_token
from fastapi.routing import APIRoute

class VerifyTokenRoute(APIRoute):

  def get_route_handler(self):
    original_route = super().get_route_handler()

    async def verify_token_middleware(request: Request):
      try:
        token = request.headers["authorization"].split(" ")[1]
      except KeyError:
        token = ""
      
      validation_reponse = validate_token(token, output=False)

      if validation_reponse == None:
        return await original_route(request)
      else:
        return validation_reponse

    return verify_token_middleware