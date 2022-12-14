from random import choices
from string import ascii_letters, digits

ALL = ascii_letters + digits

def get_token():
	return ''.join(choices(ALL,k=16))