from rest_framework                       import status, views
from rest_framework.response              import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from authApp.serializers.userSerializer   import UserSerializer

class UserCreateView(views.APIView):
    def post(self, request, *args, **kwargs):

        #recive data from request (json), and convert the data json to python object
        serializer = UserSerializer(data=request.data)
        
        #validate if the object is valid
        serializer.is_valid(raise_exception=True)
        
        #save in the database
        serializer.save()

        #take username and password from the request
        token_data = {'username':request.data['username'], 'password': request.data['password']}

        #obtain the pair of token from the username and password
        token_serializer = TokenObtainPairSerializer(data=token_data)

        #validate if the tokens are valid
        token_serializer.is_valid(raise_exception=True)

        #generate a response with code http 200 = creation correct
        return Response(token_serializer.validated_data, status=status.HTTP_201_CREATED)  