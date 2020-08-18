'''
Invite Manager Bot Written in discord.py 
'''

import discord
client=discord.Client()

role_ranks={
	'Gold':range(5,9),
	'Platinum':range(10,14),
	'Diamond':range(15,24),
	'Crown':range(25,49),
	'Ace':range(50,99),
	'Conqueror':range(100,100000)
}

@client.event
async def on_ready():
	global role_list
	print('Logged in as: '+client.user.name)
	print('Bot ID: '+client.user.id)
	await client.change_presence(game=discord.Game(name='TZ!invites - List your invites')) 
	print('------\n')
	for server in client.servers:
		role_list=dict((role.name,role) for role in server.roles)

@client.event
async def on_member_join(new_member):
	invites=await client.invites_from(new_member.server)
	for member in new_member.server.members:
		if member.bot==False:
			uses=0
			prole=None
			for invite in invites:
				if invite.max_age==0 and invite.inviter==member:
					uses += invite.uses
			for role,used in role_ranks.items():
				if uses in used and role_list[role] not in member.roles:
					for mrole in member.roles:
						if mrole.name in role_ranks.keys():
							await client.remove_roles(member,mrole)
					await client.send_message(member,"Congratulations  {}, you have been promoted to **{}**!".format(member.mention,role))
					await client.add_roles(member,role_list[role])

@client.event
async def on_message(message):
	if message.content=='TZ!invites': 
		total_uses=0
		embed=discord.Embed(title='__Invites from {}__'.format(message.author.name))
		invites = await client.invites_from(message.server)
		for invite in invites:
			if invite.inviter == message.author and invite.max_age==0:
				total_uses += invite.uses
				embed.add_field(name='Invite',value=invite.id)
				embed.add_field(name='Uses',value=invite.uses)
				embed.add_field(name='Expires',value='Never')
		embed.add_field(name='__Total Uses__',value=total_uses)
		await client.send_message(message.channel,embed=embed)


client.run('NjYzMjc5MzUyMzQyOTA0ODQz.Xi8SxQ.Apz8ltAL4n-QR-IuundmkgQQ2zo') 
