import hikari
import lightbulb
import aiohttp
import os

# Define bot intents and prefix
bot = lightbulb.BotApp(token=os.getenv("DISCORD_BOT_TOKEN"), intents=hikari.Intents.ALL, prefix=os.getenv("BOT_PREFIX", "!"))

# Nitrado API credentials
NITRADO_API_TOKEN = os.getenv("NITRADO_API_TOKEN")

# Base Nitrado API URL
NITRADO_API_URL = "https://api.nitrado.net"

@bot.command
@lightbulb.command("costs", "Check Nitrado invoices and donation stats.")
@lightbulb.implements(lightbulb.SlashCommand)
async def costs(ctx: lightbulb.Context):
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"Bearer {NITRADO_API_TOKEN}"}
        
        # Fetch invoice data
        async with session.get(f"{NITRADO_API_URL}/services", headers=headers) as response:
            if response.status != 200:
                await ctx.respond("Failed to retrieve data from Nitrado. Please try again later.")
                return

            data = await response.json()

            try:
                services = data['data']['services']
                total_monthly_cost = 0

                for service in services:
                    monthly_cost = service.get('price', {}).get('monthly', 0)
                    total_monthly_cost += monthly_cost

                # Calculate donations (assumes you have a way to fetch donation data)
                # Replace the following with your actual donation logic
                total_donations = 0  # Replace with actual donation fetching logic

                await ctx.respond(
                    f"Total Monthly Costs: ${total_monthly_cost}\n"
                    f"Total Donations This Month: ${total_donations}\n"
                    f"Amount Covered: ${min(total_donations, total_monthly_cost)}\n"
                    f"Amount Remaining: ${max(total_monthly_cost - total_donations, 0)}"
                )

            except KeyError:
                await ctx.respond("Unexpected data format received from Nitrado API.")

# Run the bot
if __name__ == "__main__":
    bot.run()
