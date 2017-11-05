from django.conf.urls import url
from core.views import B2cResult, B2cTimeOut

urlpatterns = [
    url('^b2c/timeout$', B2cTimeOut.as_view(), name='b2c_timeout'),
    url('^b2c/result', B2cResult.as_view(), name='b2c_result'),
]
