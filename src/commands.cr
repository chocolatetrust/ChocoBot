# list all commands and memes in an embed
COMMANDS["memes"] = Proc(Discord::Message, Array(String), Void).new do |msg, args|
  embed = Discord::Embed.new(
    colour: 0xaf2e1a.to_u32,
    author: Discord::EmbedAuthor.new(
      name: "Chocobot",
      icon_url: CACHE.resolve_current_user.avatar_url
    ),
    thumbnail: Discord::EmbedThumbnail.new(
      CACHE.resolve_current_user.avatar_url
    ),
    fields: [
      Discord::EmbedField.new(
        "Memes",
        MEMES.keys.map { |x| "," + x }.join("\n"),
        true
      ),
      Discord::EmbedField.new(
        "Commands",
        COMMANDS.keys.map { |x| "," + x }.join("\n"),
        true
      ),
    ]
  )
  CLIENT.create_message(msg.channel_id, "", embed: embed)
end

# whAT Do YOu MeAn ThiS MeME iS OUtDaTed
COMMANDS["sponge"] = Proc(Discord::Message, Array(String), Void).new do |msg, args|
  rand = Random.new
  str = args.join(" ").downcase.chars.map { |x|
    if rand.next_bool
      x
    else
      x.upcase
    end
  }.join
  if str.empty?
    str = "yoU FoRGot a MesSagE"
  end
  CLIENT.create_message(msg.channel_id, str)
end

# KATCASE
COMMANDS["katcase"] = Proc(Discord::Message, Array(String), Void).new do |msg, args|
  str = args.join(" ").upcase
  if str.empty?
    str = "You forgot a message to KATCASE."
  end
  CLIENT.create_message(msg.channel_id, str)
end

# Generates a rename command for each of the users in the array
# This would be so much cleaner if we had a more lispy language ;_;
{% for command in [
                    {cmd: "katname", id: 371151824331210755, genitive: "Kat's"},
                    {cmd: "milkname", id: 515909580358942720, genitive: "Milk Cake's"},
                  ] %}
  COMMANDS[{{ command[:cmd] }}] = Proc(Discord::Message, Array(String), Void).new do |msg, args|
    begin
      new_name = args.join(" ")
      raise "Name must be ≥2 and ≤32 characters" unless new_name.size > 1 && new_name.size < 33
      old_name = CACHE.resolve_member(msg.guild_id.not_nil!, {{ command[:id] }}).nick || "nil"
      CLIENT.modify_guild_member(msg.guild_id.not_nil!, {{ command[:id] }}, nick: new_name)
      CLIENT.create_message(msg.channel_id, {{ command[:genitive] }} + " nickname updated from **#{old_name}** to **#{new_name}**!")
    rescue e
      LOG.warn e
      CLIENT.create_message(msg.channel_id, "Error: #{e}")
    end
  end
{% end %}

require "http/client"

# bigify emoji
COMMANDS["big"] = Proc(Discord::Message, Array(String), Void).new do |msg, args|
  # try to parse the first argument as an emoji, if there is none,
  # parse an empty string instead (guaranteed failure)
  emoji = /<?(a?):.+:([0-9]+)>?/.match(args[0]? || "")
  if emoji.nil?
    CLIENT.create_message(msg.channel_id, "Error: That doesn't look like a custom emoji")
    return
  end

  extension = emoji[1].empty? ? ".png" : ".gif"
  emoji_file = File.tempfile("emoji-#{emoji[2]}", extension)
  emoji_data = HTTP::Client.get("https://cdn.discordapp.com/emojis/#{emoji[2]}#{extension}").body
  File.write(emoji_file.path, emoji_data)
  CLIENT.upload_file(msg.channel_id, "", emoji_file)
  emoji_file.delete
end
