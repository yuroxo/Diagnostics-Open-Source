#Bot config
command_prefixes = ["진단아 "]
extension_list = ["extensions.admin", "extensions.event", "extensions.jindan", "extensions.support"]
bot_status = ["진단아 도움말", "{server_count}개의 서버에서", "{user_count}분의 명령어를"]  #-듣는중

#Db config
mongodb_username = ""
mongodb_password = ""
mongodb_host = "127.0.0.1"
mongodb_port = 27017
#Tokens
bot_token = '' #Put your own bot token here -> https://discord.com/developers
koreanbots_token = ''  #Put your KoreanBots.dev token here -> https://koreanbots.dev

yes_emoji = "<a:a_yes:805962647014342666>"
no_emoji = "<a:a_no:805962647907598356>"
#yes_emoji = "<a:yes:746234182581223544>"
#no_emoji = "<a:x_:745480777080242347>"

yes_emoji_int = int(yes_emoji[-19:-1])
no_emoji_int = int(no_emoji[-19:-1])