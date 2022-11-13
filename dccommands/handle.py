import discord
from github.user import User
from github.repo import Repo


# INTERPRETE COMMAND AND EXECUTE
async def interpret(command):

  # Greet
  if command.content == '?greet':
    await command.channel.send('Hi! :hand_splayed:')
    return

  # Help
  if command.content == '?help':
    embed = discord.Embed()

    embed.description = '''
      List of available commands:

      :ballot_box_with_check: `?greet` :arrow_forward: Make Gitto greet.
      :ballot_box_with_check: `?register` :arrow_forward: Identify yourself as a Github user (receives the Github username as an argument).
      :ballot_box_with_check: `?unregister` :arrow_forward: Unregister yourself.
      :ballot_box_with_check: `?info` :arrow_forward: Displays info about the current registered user.
      :ballot_box_with_check: `?help` :arrow_forward: Displays this box.

      :ballot_box_with_check: `?git init` :arrow_forward: Initializes a Github repository in the current text channel (receives the Github repo link as an argument).
      :ballot_box_with_check: `?git info` :arrow_forward: Displays info about the current repository.
      :ballot_box_with_check: `?git close` :arrow_forward: Closes the current repository in the current text channel.

      '''

    await command.channel.send(embed=embed)
    return

  # Register user
  if command.content.split(' ')[0] == '?register':

    # Create and register new user
    if len(command.content.split(' ')) == 2:
      new_user = User.__new__(User)
      await new_user.register(command)

    # Failure on register
    elif len(command.content.split(' ')) == 1:
      await command.channel.send(
        ':exclamation: Please write your Github username next to the `?register` command.'
      )
    else:
      await command.channel.send(
        ':exclamation: Too many arguments. Type `?help` to read a list of available commands.'
      )

    return

  # Show info from the user
  if command.content == ('?info'):
    # Call class method
    if len(command.content.split(' ')) == 1:
      # Verify if the user is registered
      registered = User.isRegistered(command)

      if not registered:
        await command.channel.send(
          ':exclamation: Register first to see your info as a user.')
        return

      await User.showUserInfo(command)

    # Too many arguments
    else:
      await command.channel.send(
        ':exclamation: Too many arguments. Type `?help` to read a list of available commands.'
      )
    return

  # Unregister user
  if command.content == ('?unregister'):

    # Call class method
    if len(command.content.split(' ')) == 1:
      await User.unregister(command)

    # Failure on unregister
    else:
      await command.channel.send(
        ':exclamation: Too many arguments. Type `?help` to read a list of available commands.'
      )
    return

  # Git operations
  if command.content.split(' ')[0] == '?git':
    # Verify if the user is registered
    registered = User.isRegistered(command)

    if not registered:
      await command.channel.send(
        ':exclamation: Register first to use git commands.')
      return

    # Verify arguments quantity
    if len(command.content.split(' ')) == 1:
      await command.channel.send(
        ':exclamation: Not enough arguments. Type `?help` to read a list of available commands.'
      )
      return

    if len(command.content.split(' ')) > 3:
      await command.channel.send(
        ':exclamation: Too many arguments. Type `?help` to read a list of available commands.'
      )
      return

    # Init repo
    if command.content.split(' ')[1] == 'init':
      new_repo = Repo.__new__(Repo)
      await new_repo.initRepo(command)  #Init the repo
      return

    # Repo info
    if command.content.split(' ')[1] == 'info':
      if len(command.content.split(' ')) == 2:
        await Repo.showRepoInfo(command)  #Show repo info
      else:
        await command.channel.send(
          ':exclamation: Too many arguments. Type `?help` to read a list of available commands.'
        )
      return

    # Close repo
    if command.content.split(' ')[1] == 'close':
      if len(command.content.split(' ')) == 2:
        await Repo.closeRepo(command)
      else:
        await command.channel.send(
          ':exclamation: Too many arguments. Type `?help` to read a list of available commands.'
        )
      return

  # Command not found
  await command.channel.send(
    ":x: I don't recognize that command. Type `?help` to read a list of available commands."
  )
