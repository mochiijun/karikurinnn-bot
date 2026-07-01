import os
import sys
import asyncio
import random
import sqlite3
import aiohttp
from datetime import datetime, timedelta

# --- IMPORTAÇÃO OBRIGATÓRIA DA BIBLIOTECA DO DISCORD ---
try:
    import discord
    from discord.ext import commands
    from discord import app_commands
except ImportError:
    print("❌ A biblioteca 'discord.py' não está instalada! Execute no terminal: pip install discord.py")
    sys.exit(1)

# --- INSTALAÇÃO AUTOMÁTICA DO SERVIDOR WEB PASTEL ---
try:
    from quart import Quart, render_template_string
except ImportError:
    print("⏳ Instalando servidor web Quart... Por favor, aguarde.")
    os.system("pip install quart")
    from quart import Quart, render_template_string

# =======================================================
# 🪄 PARTE 1: GERADOR DO WEBSITE OFICIAL E DATABASES
# =======================================================

# Cria a pasta e o arquivo HTML do Site Oficial automaticamente
if not os.path.exists("site_templates"):
    os.makedirs("site_templates")

if not os.path.exists("site_templates/index.html"):
    with open("site_templates/index.html", "w", encoding="utf-8") as f:
        f.write("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Karikurinnn Oficial 🌸</title>
            <link href="https://googleapis.com" rel="stylesheet">
            <style>
                body { background-color: #FFF0F5; font-family: 'Quicksand', sans-serif; color: #5D4037; padding: 20px; text-align: center; }
                .container { background-color: #FFFFFF; border-radius: 25px; padding: 30px; box-shadow: 0 8px 20px rgba(255, 182, 193, 0.3); max-width: 700px; margin: 0 auto; border: 4px solid #FFB6C1; }
                h1 { font-family: 'Fredoka', sans-serif; color: #FF69B4; font-size: 2.2em; margin-bottom: 5px; }
                p { color: #8B7373; font-size: 1.1em; }
                .ranking-table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #FFF9FA; border-radius: 15px; overflow: hidden; border: 2px dashed #FFB6C1; }
                th { background-color: #FFB6C1; color: white; padding: 12px; font-family: 'Fredoka', sans-serif; }
                td { padding: 12px; border-bottom: 1px dashed #FFE4E1; font-weight: bold; color: #6D4C41; }
                tr:hover { background-color: #FFE4E1; }
                .divider { color: #FFB6C1; font-size: 1.5em; margin: 15px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🌸 Karikurinnn Bot Oficial 🌸</h1>
                <p>O robô mais fofo de economia de algodão-doce e interações do Discord!</p>
                <div class="divider">𖥸・┈┈┈┈・┈┈┈┈・𖥸</div>
                
                <h2>🏆 Placar Global de Ricaços (TOP 5)</h2>
                <p>Estes são os membros com as maiores carteiras de Algodão Doce atualmente:</p>
                
                <table class="ranking-table">
                    <thead>
                        <tr>
                            <th>Posição 🏅</th>
                            <th>ID do Usuário 👤</th>
                            <th>Saldo de Algodão Doce 🍧</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for jogador in ranking %}
                        <tr>
                            <td>{{ loop.index }}º Lugar</td>
                            <td>{{ jogador }}</td>
                            <td>{% if jogador >= 999999999999 %}∞ Infinitos{% else %}{{ jogador }} 🍧{% endif %}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                <div class="divider">𖥸・┈┈┈┈・┈┈┈┈・𖥸</div>
                <p style="font-size: 0.9em; color: #BA55D3;">Atualizado em tempo real • Desenvolvido com amor por Karikurinnn</p>
            </div>
        </body>
        </html>
        """)
    print("✨ Arquivos visuais do Website criados com sucesso!")

# =======================================================
# 🔌 PARTE 2: SERVIDOR WEB INTERNO (QUART)
# =======================================================

app = Quart(__name__)

@app.route('/')
async def home():
    conn = sqlite3.connect("karikurinnn_economia.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, algodao_doce FROM usuarios ORDER BY algodao_doce DESC LIMIT 5")
    dados_ranking = cursor.fetchall()
    conn.close()
    
    with open("site_templates/index.html", "r", encoding="utf-8") as f:
        template = f.read()
    return await render_template_string(template, ranking=dados_ranking)

# =======================================================
# 🌸 PARTE 3: CONFIGURAÇÃO CENTRAL DO BOT DO DISCORD
# =======================================================

MY_OWNER_ID = 1284950910312906854
intents = discord.Intents.all()

class KarikurinnnBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="k!", intents=intents, help_command=None)
        self.em_manutencao = False

    async def setup_hook(self):
        # Cria a base de dados unificada automaticamente
        conn = sqlite3.connect("karikurinnn_economia.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, algodao_doce INTEGER DEFAULT 0, ultimo_daily TEXT, ultimo_mensal TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS comandos_custom (nome TEXT PRIMARY KEY, resposta TEXT, criador_id INTEGER)")
        cursor.execute("CREATE TABLE IF NOT EXISTS inventarios (usuario_id INTEGER, item TEXT, data_compra TEXT)")
        conn.commit()
        conn.close()
        
        # 🚀 Linhas corrigidas e alinhadas sob a mesma margem (8 espaços/2 tabs)
        loop = asyncio.get_event_loop()
        porta_nuvem = int(os.environ.get("PORT", 5000))
        loop.create_task(app.run_task(host="0.0.0.0", port=porta_nuvem))
        
        print("⏳ Sincronizando novos comandos com o Discord...")
        await self.tree.sync()
        print("✅ Todos os comandos de moedas e website carregados!")

bot = KarikurinnnBot()
# =======================================================
# 🌸 PARTE 3: CONFIGURAÇÃO CENTRAL DO BOT DO DISCORD
# =======================================================

MY_OWNER_ID = 1284950910312906854
intents = discord.Intents.all()

class KarikurinnnBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="k!", intents=intents, help_command=None)
        self.em_manutencao = False

    async def setup_hook(self):
        # Cria a base de dados unificada automaticamente
        conn = sqlite3.connect("karikurinnn_economia.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, algodao_doce INTEGER DEFAULT 0, ultimo_daily TEXT, ultimo_mensal TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS comandos_custom (nome TEXT PRIMARY KEY, resposta TEXT, criador_id INTEGER)")
        cursor.execute("CREATE TABLE IF NOT EXISTS inventarios (usuario_id INTEGER, item TEXT, data_compra TEXT)")
        conn.commit()
        conn.close()
        
        # 🚀 Linhas corrigidas e alinhadas sob a mesma margem (8 espaços/2 tabs)
        loop = asyncio.get_event_loop()
        porta_nuvem = int(os.environ.get("PORT", 5000))
        loop.create_task(app.run_task(host="0.0.0.0", port=porta_nuvem))
        
        print("⏳ Sincronizando novos comandos com o Discord...")
        await self.tree.sync()
        print("✅ Todos os comandos de moedas e website carregados!")

bot = KarikurinnnBot()

# =======================================================
# 🧮 PARTE 4: FUNÇÕES AUXILIARES E EVENTOS DO CHAT
# =======================================================

def executar_query(query, parametros=()):
    conn = sqlite3.connect("karikurinnn_economia.db")
    cursor = conn.cursor()
    cursor.execute(query, parametros)
    conn.commit()
    conn.close()

def buscar_saldo(user_id):
    conn = sqlite3.connect("karikurinnn_economia.db")
    cursor = conn.cursor()
    cursor.execute("SELECT algodao_doce, ultimo_daily, ultimo_mensal FROM usuarios WHERE id = ?", (user_id,))
    resultado = cursor.fetchone()
    conn.close()
    if not resultado:
        executar_query("INSERT INTO usuarios (id, algodao_doce) VALUES (?, 0)", (user_id,))
        return (0, None, None)
    return resultado

def stylized_fonte(texto):
    resultado = []
    for c in texto:
        if 'a' <= c <= 'z': resultado.append(chr(0x1D5EE + (ord(c) - ord('a'))))
        elif 'A' <= c <= 'Z': resultado.append(chr(0x1D5D4 + (ord(c) - ord('A'))))
        else: resultado.append(c)
    return "".join(resultado)

def checar_dono():
    return commands.check(lambda ctx: ctx.author.id == MY_OWNER_ID)

@bot.event
async def on_ready():
    print(f"🌸 Karikurinnn está online! Acesse o site em: http://localhost:5000")
    await bot.change_presence(activity=discord.Game(name="k!moedas_ajuda | 💖"))
    
    # Carrega comandos dinâmicos salvos na database
    conn = sqlite3.connect("karikurinnn_economia.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome, resposta FROM comandos_custom")
    for nome, resposta in cursor.fetchall():
        try:
            @commands.command(name=nome)
            async def cmd_dinamico(ctx, resp=resposta): await ctx.send(resp)
            bot.add_command(cmd_dinamico)
        except Exception: pass
    conn.close()

@bot.event
async def on_message(message):
    if message.author.bot: return
    if bot.em_manutencao and message.author.id != MY_OWNER_ID: return
    
    if message.author.id == MY_OWNER_ID and message.content.strip().lower() == "abrir":
        if bot.em_manutencao:
            bot.em_manutencao = False
            await bot.change_presence(activity=discord.Game(name="k!moedas_ajuda | 💖"))
            await message.reply(f"🌸 **|** {stylized_fonte('Modo de manutencao encerrado')}!")
        return
    await bot.process_commands(message)

# =======================================================
# 🍬 PARTE 5: CENTRAL DE ECONOMIA DO ALGODÃO DOCE
# =======================================================

@bot.hybrid_command(name="moedas_ajuda", description="Lista de comandos da economia do bot.")
async def moedas_ajuda(ctx: commands.Context):
    embed = discord.Embed(title=f"🍧 {stylized_fonte('Karikurinnn Economia')} 🍧", description="Acesse nossa central de economia!", color=discord.Color.from_rgb(255, 182, 193))
    embed.add_field(name="💳 Carteira", value="`k!saldo` | `k!ranking`", inline=True)
    embed.add_field(name="`k!diario` | `k!mensal` | `k!aventura`", value="📆 Ganhar", inline=True)
    embed.add_field(name="`k!loteria` | `k!comprar`", value="🎲 Sorte & Lojas", inline=True)
    embed.add_field(name="`k!site` - Veja o ranking no navegador", value="🌐 Site Oficial", inline=True)
    await ctx.send(embed=embed)

@bot.hybrid_command(name="site", description="Mostra o link do site oficial estético do Karikurinnn.")
async def site(ctx: commands.Context):
    embed = discord.Embed(
        title=f"🌐 {stylized_fonte('Site Oficial Karikurinnn')}",
        description="Venha conferir nossa página oficial! Veja quem é o mais rico do servidor direto do seu navegador.\n\n🔗 **Acesse aqui:** [http://localhost:5000](http://localhost:5000)",
        color=discord.Color.from_rgb(186, 85, 211)
    )
    await ctx.send(embed=embed)

@bot.hybrid_command(name="saldo", description="Mostra sua quantidade atual de algodão-doce.")
async def saldo(ctx: commands.Context, usuario: discord.User = None):
    alvo = usuario or ctx.author
    doces, _, _ = buscar_saldo(alvo.id)
    exibicao = "∞" if doces >= 999999999999 else f"**{doces}**"
    await ctx.send(f"🍧 **|** {alvo.mention} possui atualmente {exibicao} {stylized_fonte('Algodoes Doces')}!")

@bot.hybrid_command(name="diario", description="Resgate seu bônus diário.")
async def diario(ctx: commands.Context):
    _, ult_daily, _ = buscar_saldo(ctx.author.id)
    agora = datetime.now()
    if ult_daily and datetime.strptime(ult_daily, "%Y-%m-%d %H:%M:%S") + timedelta(days=1) > agora:
        return await ctx.send("heyy!! ladrãozinho, ja pegou o daily hoje!! 🍓🐾")
    ganho = random.randint(200, 800)
    executar_query("UPDATE usuarios SET algodao_doce = algodao_doce + ?, ultimo_daily = ? WHERE id = ?", (ganho, agora.strftime("%Y-%m-%d %H:%M:%S"), ctx.author.id))
    await ctx.send(f"🍬 **|** {ctx.author.mention} ganhou **{ganho}** {stylized_fonte('Algodoes Doces')}!")

@bot.hybrid_command(name="mensal", description="Resgate sua mesada mensal.")
async def mensal(ctx: commands.Context):
    _, _, ult_mensal = buscar_saldo(ctx.author.id)
    agora = datetime.now()
    if ult_mensal and datetime.strptime(ult_mensal, "%Y-%m-%d %H:%M:%S") + timedelta(days=30) > agora:
        return await ctx.send("📅 **|** Sua mesada mensal ainda não está disponível!")
    ganho = random.randint(5000, 15000)
    executar_query("UPDATE usuarios SET algodao_doce = algodao_doce + ?, ultimo_mensal = ? WHERE id = ?", (ganho, agora.strftime("%Y-%m-%d %H:%M:%S"), ctx.author.id))
    await ctx.send(f"📦 **|** {ctx.author.mention} abriu a caixa mensal e faturou **{ganho}** 🍧!")

@bot.hybrid_command(name="transferir", description="Transfere algodões-doces para um amigo.")
async def transferir(ctx: commands.Context, amigo: discord.User, valor: int):
    if valor <= 0 or amigo == ctx.author: return await ctx.send("❌ Ação inválida.")
    doces, _, _ = buscar_saldo(ctx.author.id)
    if doces < valor: return await ctx.send("❌ Saldo insuficiente.")
    buscar_saldo(amigo.id)
    executar_query("UPDATE usuarios SET algodao_doce = algodao_doce - ? WHERE id = ?", (valor, ctx.author.id))
    executar_query("UPDATE usuarios SET algodao_doce = algodao_doce + ? WHERE id = ?", (valor, amigo.id))
    await ctx.send(f"💞 **|** {ctx.author.mention} enviou **{valor}** 🍧 para {amigo.mention}!")

@bot.hybrid_command(name="aventura", description="Roleplay para pegar doces.")
async def aventura(ctx: commands.Context):
    ganho = random.randint(100, 400)
    executar_query("UPDATE usuarios SET algodao_doce = algodao_doce + ?, ultimo_daily = ? WHERE id = ?", (ganho, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ctx.author.id))
    await ctx.send(f"🌟 **|** {ctx.author.mention} encontrou um baú de doces e pegou **{ganho}** 🍧!")

@bot.hybrid_command(name="loteria", description="Aposte uma quantia.")
async def loteria(ctx: commands.Context, valor: int):
    if valor <= 0: return await ctx.send("❌ Valor inválido.")
    doces, _, _ = buscar_saldo(ctx.author.id)
    if doces < valor: return await ctx.send("❌ Saldo insuficiente.")
    if random.choice([True, False]):
        executar_query("UPDATE usuarios SET algodao_doce = algodao_doce + ? WHERE id = ?", (valor, ctx.author.id))
        await ctx.send(f"🎉 **|** {ctx.author.mention} venceu e ganhou **+{valor}** 🍧!")
    else:
        executar_query("UPDATE usuarios SET algodao_doce = max(0, algodao_doce - ?) WHERE id = ?", (valor, ctx.author.id))
        await ctx.send(f"📉 **|** Você perdeu **-{valor}** 🍧.")

@bot.hybrid_command(name="ranking", description="Ranking local de ricaços do chat.")
async def ranking(ctx: commands.Context):
    conn = sqlite3.connect("karikurinnn_economia.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, algodao_doce FROM usuarios ORDER BY algodao_doce DESC LIMIT 5")
    dados = cursor.fetchall()
    conn.close()
    linhas = [f"🏅 `{i+1}º` ── **{(ctx.guild.get_member(uid).name if ctx.guild.get_member(uid) else uid)}**: {'∞' if d >= 999999999999 else d} 🍧" for i, (uid, d) in enumerate(dados)]
    embed = discord.Embed(title=f"📈 {stylized_fonte('Ranking de Algodao Doce')}", description="\n".join(linhas), color=discord.Color.blue())
    await ctx.send(embed=embed)

@bot.hybrid_command(name="comprar", description="Lojinha do servidor.")
async def comprar(ctx: commands.Context, item: str = None):
    itens_loja = {"anel": 5000, "badge": 2000, "tag": 10000}
    if not item:
        lista = "\n".join([f"• **{k.capitalize()}**: {v} 🍧" for k, v in itens_loja.items()])
        return await ctx.send(f"🛒 **| Lojinha**\nUse `/comprar <nome>`:\n\n{lista}")
    escolha = item.lower().strip()
    if escolha not in itens_loja: return await ctx.send("❌ Item indisponível.")
    preco = itens_loja[escolha]
    doces, _, _ = buscar_saldo(ctx.author.id)
    if doces < preco: return await ctx.send("❌ Saldo insuficiente.")
    executar_query("UPDATE usuarios SET algodao_doce = algodao_doce - ? WHERE id = ?", (preco, ctx.author.id))
    executar_query("INSERT INTO inventarios (usuario_id, item, data_compra) VALUES (?, ?, ?)", (ctx.author.id, escolha, datetime.now().strftime("%Y-%m-%d")))
    await ctx.send(f"🛍️ **|** COMPRA CONCLUÍDA! {ctx.author.mention} comprou um **{escolha.capitalize()}** por **{preco}** 🍧!")

# =======================================================
# 👑 PARTE 6: EXCLUSIVOS DE DONO E DIAGNÓSTICO
# =======================================================

@bot.hybrid_command(name="criar_comando", description="Cria um comando customizado (Apenas p/ o Dono).")
@app_commands.describe(nome="Nome do comando", resposta="Resposta em texto")
async def criar_comando(ctx: commands.Context, nome: str, *, resposta: str):
    if ctx.author.id != MY_OWNER_ID:
        return await ctx.send("❌ **[ACESSO NEGADO]** Apenas o dono supremo do Karikurinnn pode usar este comando! 🛡️")
        
    nome_limpo = nome.lower().strip().replace("k!", "").replace("/", "")
    try:
        executar_query("INSERT OR REPLACE INTO comandos_custom (nome, resposta, criador_id) VALUES (?, ?, ?)", (nome_limpo, resposta, ctx.author.id))
        
        @commands.command(name=nome_limpo)
        async def novo_comando(inner_ctx, resp=resposta): await inner_ctx.send(resp)
        bot.add_command(novo_comando)
        
        await ctx.send(f"✅ Comando hibridizado `k!{nome_limpo}` criado e salvo na database com sucesso!")
    except Exception as e:
        await ctx.send(f"❌ Erro ao registrar comando: {e}")

@bot.hybrid_command(name="ping", description="Mede a velocidade básica de resposta.")
async def ping(ctx: commands.Context): await ctx.send("🏓 **|** Pong!")

@bot.hybrid_command(name="latencia", description="Mostra a latência com a API.")
async def latencia(ctx: commands.Context):
    await ctx.send(f"📶 **|** Latência atual: `{round(bot.latency * 1000)}ms`")

@bot.command(name="manutenção")
@checar_dono()
async def manutencao(ctx):
    if bot.em_manutencao: return
    bot.em_manutencao = True
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="🛠️ Em Manutenção..."))
    await ctx.send("🛠️ Modo Manutenção Ativado! Todos os comandos públicos foram travados.")

@bot.command(name="infinito")
@checar_dono()
async def infinito(ctx, alvo: discord.User):
    buscar_saldo(alvo.id)
    executar_query("UPDATE usuarios SET algodao_doce = 999999999999 WHERE id = ?", (alvo.id,))
    await ctx.send(f"👑 O poder supremo foi concedido! {alvo.mention} agora possui moedas infinitas!")

@bot.command(name="tirar_infinito")
@checar_dono()
async def tirar_infinito(ctx, alvo: discord.User):
    executar_query("UPDATE usuarios SET algodao_doce = 0 WHERE id = ?", (alvo.id,))
    await ctx.send(f"👑 Poder infinito removido de {alvo.mention}.")


# ⚠️ SUBSTITUA PELO SEU TOKEN ATIV DO DISCORD AQUI EMBAIXO:
bot.run('MTQ1NTg4MzI5NDg4NDIzNzQ0OQ.G8mVKI.5CPNHfZUDtBA8MoElvqj-dAku18YHm8gbAn9o4')

# --- STATUS ROTATIVO FANTÁSTICO NO PERFIL ---
async def mudar_status_loop():
    await bot.wait_until_ready()
    while not bot.is_closed():
        # Status 1: Mostrando o site público
        await bot.change_presence(activity=discord.Streaming(name="🌐 karikurinnn.ngrok-free.app", url="https://twitch.tv"))
        await asyncio.sleep(15)
        # Status 2: Chamando para jogar
        await bot.change_presence(activity=discord.Game(name="🍧 Use k!moedas_ajuda | 💖"))
        await asyncio.sleep(15)

# Adicione essa linha logo no final da sua função on_ready para ativar o loop:
bot.loop.create_task(mudar_status_loop())

        # Inicia o Servidor do WebSite integrado adaptado para nuvens gratuitas
        loop = asyncio.get_event_loop()
        porta_nuvem = int(os.environ.get("PORT", 5000)) # Pega a porta da hospedagem automaticamente
        loop.create_task(app.run_task(host="0.0.0.0", port=porta_nuvem))

