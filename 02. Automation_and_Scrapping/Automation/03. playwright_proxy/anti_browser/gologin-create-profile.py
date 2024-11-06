from gologin import GoLogin


def create_profile_id():
  gl = GoLogin({"token": token, })
  platform = choice(['mac', 'win', 'lin'])   # 'android'
  profile_id = gl.create({
    "name": choice(['profile1', 'profile2', 'profile3', 'profile4', 'profile5', 'profile6']),
    "os": platform,
    "navigator": {"language": 'en-US', "userAgent": 'random', "resolution": 'random', "platform": platform},
    'proxyEnabled': True,
    'proxy':
      {"mode": 'http',
       'host': host,
       'port': port,
       'username': username,
       'password': password
       },
    "webRTC": {"mode": "alerted", "enabled": True}
  })
  return profile_id

# gl.update({
#     "id": 'yU0Pr0f1leiD',
#     "name": 'profile_mac2',
# });

profile = gl.getProfile(profile_id);

print('new profile name=', profile.get("name"));

# gl.delete('yU0Pr0f1leiD')
