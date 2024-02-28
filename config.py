from collections import namedtuple

TOKEN = '6321263398:AAHm9vCZRmTlPRl39GTa-zsrXdMvEEl7G1c'

NetData = namedtuple('NetData', [
    'localhost',
    'localport',
    'remotehost',
    'remoteport'
])

NET_DATA = NetData(
    localhost='192.168.1.24',
    localport=504,
    remotehost=None,
    remoteport=None
)
