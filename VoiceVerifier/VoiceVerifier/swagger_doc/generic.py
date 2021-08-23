from drf_yasg import openapi

class GenericResponse():
    swagger_400_response = openapi.Response(
        "Malformed request."
    )
    swagger_404_response = openapi.Response(
        "No such entity found."
    )
    swagger_500_response = openapi.Response(
        "Internal server error."
    )