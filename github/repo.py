import discord
import requests


class Repo():

  def __new__(cls, *args, **kwargs):
    return super().__new__(cls)

  def __init__(self, dc_channel, owner, name, id, link, description, branch,
               forks, stars, language, webhook):
    self.dc_channel = dc_channel
    self.owner = owner
    self.name = name
    self.id = id
    self.link = link
    self.description = description
    self.branch = branch
    self.forks = forks
    self.stars = stars
    self.language = language
    self.webhook = webhook

  # INIT REPO
  async def initRepo(self, command):
    if len(command.content.split(' ')) != 3:
      await command.channel.send(
        ':exclamation: Pass a repository link as an argument.')
      return

    # Get repo link
    link = command.content.split(' ')[2]

    # If the repo is already active
    for dc_repo in repos:
      if link == dc_repo.link:
        await command.channel.send(
          f':exclamation: That repository is already active on the channel #{dc_repo.dc_channel}'
        )
        return

    # If the channel is being used for a repo
    for dc_repo in repos:
      if command.channel == dc_repo.dc_channel:
        await command.channel.send(
          f':exclamation: This channel is already being used for the repo: {dc_repo.name}'
        )
        return

    # Check if the link is valid
    try:
      if link.split('/')[2] != 'github.com':
        await command.channel.send(
          ':exclamation: Insert only a github.com repository link.')
        return
    except:
      await command.channel.send(
        ':exclamation: Insert only a github.com repository link.')
      return

    if len(link.split('/')) != 5:
      await command.channel.send(':x: Invalid link. Try adding https://...')
      return

    # Get the repo owner and name
    owner = link.split('/')[3]
    repo_name = link.split('/')[4]

    # Fetch repo data
    url = f'https://api.github.com/repos/{owner}/{repo_name}'
    response = requests.get(url)
    response_dict = response.json()

    # Get webhook avatar
    img_data = requests.get(
      'https://git-scm.com/images/logos/downloads/Git-Icon-1788C.png').content

    # Create webhook
    webhook = await command.channel.create_webhook(name=f'Gitto ({repo_name})',
                                                   avatar=img_data,
                                                   reason=None)

    # Set data to new repo
    try:
      self.__init__(command.channel, owner, repo_name, response_dict['id'],
                    response_dict['html_url'], response_dict['description'],
                    response_dict['default_branch'],
                    response_dict['forks_count'],
                    response_dict['stargazers_count'],
                    response_dict['language'], webhook)
    except:
      await command.channel.send(
        ':exclamation: An error has ocurred. Check if the link is correct and try again.'
      )
      return

    await command.channel.send('''
      :smile: The git repo has been initializated and this channel will be used to monitor it from now on.
      :mega: To start receiving notifications on this discord channel follow the intructions below:
      ''')

    embed = discord.Embed()
    embed.description = f"Go to the repo :gear: settings [here]({self.link}/settings/hooks/new), paste the given Webhook URL into the 'Payload URL' field and change 'Content type' to 'application/json', then click on 'Add webhook'."
    await command.channel.send(embed=embed)

    await command.channel.send(f'Webhook URL: `{self.webhook.url}/github`')

    repos.append(
      self)  # Append the new created repo to the list of active repos

  # REPO INFO
  @classmethod
  async def showRepoInfo(cls, command):
    for dc_repo in repos:
      if command.channel == dc_repo.dc_channel:
        embed = discord.Embed()
        embed.description = f'''
          :information_source: Repository information :information_source:
          
          :diamonds: Repository name: {dc_repo.name}
          :identification_card: Owner: {dc_repo.owner}
          :link: URL: {dc_repo.link}
          :label: Description: {dc_repo.description}
          :part_alternation_mark: Default branch: {dc_repo.branch}
          :fork_and_knife: Forks: {dc_repo.forks}
          :star: Stars: {dc_repo.stars}
          :chains: Webhook URL: {dc_repo.webhook.url}

          Currently active on #{dc_repo.dc_channel}
          '''
        await command.channel.send(embed=embed)
        return

    await command.channel.send(
      ':exclamation: There is no repository active on this channel.')

  # CLOSE REPO
  @classmethod
  async def closeRepo(cls, command):
    for dc_repo in repos:
      if command.channel == dc_repo.dc_channel:
        # Remove from the active repos
        repos.pop(repos.index(dc_repo))
        # Delete webhook
        await dc_repo.webhook.delete()

        await command.channel.send(
          f':exclamation: The repo on this channel ({dc_repo.name}) has been closed. Remember to remove the webhook from the repo.'
        )
        return
    await command.channel.send(
      ':x: There is not a repo active on this channel. Initialize one with the `?git init` command.'
    )


# List of active repos
repos = []
