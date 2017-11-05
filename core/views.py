from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response


class B2cTimeOut(APIView):
    """
    Handle b2c time out
    """
    @csrf_exempt
    def post(self, request, format=None):
        """
        process the timeout
        :param request:
        :param format:
        :return:
        """
        data = request.data
        return Response(dict(success="0"))


class B2cResult(APIView):
    """
    Handle b2c result
    """
    @csrf_exempt
    def post(self, request, format=None):
        """
        process the timeout
        :param request:
        :param format:
        :return:
        """
        data = request.data
        return Response(dict(success="0"))