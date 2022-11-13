import discord
import requests


class User():

  def __new__(cls, *args, **kwargs):
    return super().__new__(cls)

  def __init__(self, dc_username, git_username, id, repos, email, avatar,
               link):
    self.dc_username = dc_username
    self.git_username = git_username
    self.id = id
    self.repos = repos
    self.email = email
    self.avatar = avatar
    self.link = link

  # REGISTER
  async def register(self, command):
    # Fetch user data on Github
    query = command.content.split(' ')[1]
    url = f'https://api.github.com/users/{query}'
    response = requests.get(url)
    response_dict = response.json()

    # If the user is not found
    try:
      if response_dict['message'] == 'Not Found':
        await command.channel.send(f':x: User `{query}` not found.')
        return
    except:
      pass

    # If the user is already registered
    # 1. Verify for the current user
    for dc_user in users:
      if dc_user.dc_username == command.author:
        await command.channel.send(':exclamation: You are already registered.')
        return
    # 2. Verify for someone else
    for dc_user in users:
      if dc_user.git_username == response_dict['login']:
        await command.channel.send(
          ':exclamation: That user is already registered.')
        return

    # Set data to new user
    self.__init__(command.author, response_dict['login'], response_dict['id'],
                  response_dict['public_repos'], response_dict['email'],
                  response_dict['avatar_url'], response_dict['html_url'])

    # Get profile picture (profile_picture.jpg)
    img_data = requests.get(self.avatar).content
    with open('misc/profile_picture.jpg', 'wb') as handler:
      handler.write(img_data)

    # Display registered status
    await command.channel.send(
      f':white_check_mark: Registered as `{self.git_username}`')
    await command.channel.send(file=discord.File('misc/profile_picture.jpg'))

    users.append(
      self)  # Append the new created user to the list of registered users

  # USER INFO
  @classmethod
  async def showUserInfo(cls, command):
    for dc_user in users:
      if dc_user.dc_username == command.author:
        embed = discord.Embed()

        img_data = requests.get(dc_user.avatar).content
        with open('misc/profile_picture.jpg', 'wb') as handler:
          handler.write(img_data)
        
        embed.description = f'''
          :information_source: User information :information_source:
          
          :identification_card: Github username: {dc_user.git_username}
          :link: Profile URL: {dc_user.link}
          :email: Email: {dc_user.email}

          Currently registered with @{dc_user.dc_username}
          '''
        
        await command.channel.send(embed=embed)
        await command.channel.send(file=discord.File('misc/profile_picture.jpg'))
        return

    await command.channel.send(
      ':x: You are not registered. Register with the `?register` command.')

  # UNREGISTER
  @classmethod
  async def unregister(cls, command):
    for dc_user in users:
      if dc_user.dc_username == command.author:
        users.pop(users.index(dc_user))
        await command.channel.send(':exclamation: Unregistered.')
        return
    await command.channel.send(
      ':x: You are not registered. Register with the `?register` command.')

  # isRegistered?
  @classmethod
  def isRegistered(cls, command):
    registered = False
    for dc_user in users:
      if dc_user.dc_username == command.author:
        registered = True

    return registered


# List of registered users
users = []
