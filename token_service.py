import tokenlib


class TokenService:
    def __init__(self):
        pass

    def get_user(self, headers):
        if 'token' in headers:
            token = headers['token']
            if not self.is_valid(token):
                return tokenlib.parse_token(token, secret='h5j43hl254jl8l7k68')['user_id']
        return 0

    @staticmethod
    def get_token(user_id):
        return tokenlib.make_token({'user_id': user_id}, secret='h5j43hl254jl8l7k68')

    @staticmethod
    def is_valid(token):
        try:
            tokenlib.parse_token(token, secret='h5j43hl254jl8l7k68')
            return False
        except Exception as e:
            return True