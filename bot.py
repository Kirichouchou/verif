import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
from dotenv import load_dotenv

# Active le .env
load_dotenv()
keep_alive()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

ROLE_ID = 1389935085158928444  # ID du rôle Visiteur

class VerificationButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Vérifier", style=discord.ButtonStyle.green, custom_id="verify_button")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(ROLE_ID)
        if role:
            try:
                await interaction.user.add_roles(role)
                await interaction.response.send_message("✅ Tu as été vérifié. Bienvenue sur le serveur.", ephemeral=True)
            except discord.Forbidden:
                await interaction.response.send_message("❌ Permission refusée. Contacte un admin.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Rôle introuvable. Contacte un admin.", ephemeral=True)

@bot.command()
@commands.has_permissions(administrator=True)
async def verifmsg(ctx):
    embed = discord.Embed(
        title="🛡️ CC Poutinique – Vérification",
        description=(
            "**Bienvenue sur le shop officiel CC Poutinique !**\n\n"
            "🔒 *Clique sur le bouton ci-dessous pour confirmer que tu n'es pas un robot.*\n"
            "🎫 Une fois vérifié, tu recevras l'accès complet au serveur via le rôle `Visiteur`.\n\n"
            "⚡ __Vérification instantanée__\n"
        ),
        color=0x9B59B6
    )

    embed.set_image(url="attachment://banner.png")
    embed.set_footer(text="© CC Poutinique | Sécurité & rapidité avant tout.")
    file = discord.File("banner.png", filename="banner.png")
    view = VerificationButton()

    await ctx.send(file=file, embed=embed, view=view)

@bot.event
async def on_ready():
    print(f"✅ Bot en ligne : {bot.user}")

bot.run(os.getenv("TOKEN"))
